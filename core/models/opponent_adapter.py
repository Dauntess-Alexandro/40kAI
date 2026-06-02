from __future__ import annotations

import collections
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np
import torch

from core.engine.agent_registry import compatible_contracts, load_agent_by_id
from core.models.DQN import DQN
from core.models.PPO import make_actor_critic, load_actor_critic_state_dict, ppo_kwargs_from_env
from core.models.alphazero_ids import az_mcts_mode_for, is_az_algo
from core.models.alphazero_model import load_alphazero_state_dict, make_alphazero_net
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig
from core.models.action_contract import action_tensor_to_dict
from core.models.utils import build_action_masks_by_head, build_shoot_action_mask, convertToDict, normalize_state_dict


@dataclass(frozen=True)
class OpponentSpec:
    agent_id: str
    algo: str  # "dqn" | "ppo" | "alphazero_tree" | "alphazero_proxy" | "gumbel_muzero"
    contract: dict[str, Any]
    policy_state: dict[str, Any]


def _to_np_state(state: Any) -> np.ndarray:
    if isinstance(state, (dict, collections.OrderedDict)):
        return np.array(list(state.values()), dtype=np.float32)
    return np.asarray(state, dtype=np.float32)


def _parse_contract_sizes(contract: dict[str, Any]) -> tuple[int, list[int]]:
    obs_sig = str((contract or {}).get("obs_space_signature", "") or "")
    act_sig = str((contract or {}).get("action_space_signature", "") or "")
    n_obs = 0
    if obs_sig.startswith("vec:"):
        try:
            n_obs = int(obs_sig.split(":", 1)[1])
        except Exception:
            n_obs = 0
    n_actions: list[int] = []
    if act_sig.startswith("heads:"):
        tail = act_sig.split(":", 1)[1]
        for part in tail.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                n_actions.append(int(part))
            except Exception:
                continue
    return int(n_obs), [int(x) for x in n_actions]


def load_agent_opponent(*, agent_id: str, expected_contract: Optional[dict[str, Any]] = None) -> OpponentSpec:
    payload = load_agent_by_id(str(agent_id))
    meta = payload.get("meta") if isinstance(payload, dict) else {}
    algo = str((meta or {}).get("algo", "")).strip().lower()
    if algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
        # Backward-compatible inference for older artifacts:
        # - DQN artifacts usually have target_state saved
        # - PPO artifacts usually don't
        target_state = payload.get("target_state") if isinstance(payload, dict) else None
        if isinstance(target_state, dict):
            algo = "dqn"
        else:
            # last-resort heuristic by key prefixes
            policy_state_guess = payload.get("policy_state") if isinstance(payload, dict) else None
            if isinstance(policy_state_guess, dict):
                keys = [str(k) for k in policy_state_guess.keys()]
                if any(k.startswith("actor.") for k in keys):
                    algo = "ppo"
                elif any(k.startswith("policy_heads.") for k in keys):
                    mm = str((meta or {}).get("mcts_mode", "") or "").strip().lower()
                    if mm == "proxy":
                        algo = "alphazero_proxy"
                    elif mm == "tree":
                        algo = "alphazero_tree"
                    else:
                        raise ValueError(
                            f"agent '{agent_id}' has legacy/unknown AlphaZero meta (algo={algo!r}, mcts_mode={mm!r}). "
                            "Переобучите агента как alphazero_tree или alphazero_proxy."
                        )
                else:
                    raise ValueError(
                        f"agent '{agent_id}' has unsupported algo='{algo}' "
                        "(expected dqn/ppo/alphazero_tree/alphazero_proxy/gumbel_muzero)."
                    )
            else:
                raise ValueError(
                    f"agent '{agent_id}' has unsupported algo='{algo}' "
                    "(expected dqn/ppo/alphazero_tree/alphazero_proxy/gumbel_muzero)."
                )

    contract = payload.get("contract") if isinstance(payload, dict) else None
    if expected_contract is not None:
        ok, reason = compatible_contracts(expected_contract, contract or {})
        if not ok:
            raise ValueError(f"agent '{agent_id}' contract mismatch: {reason}")

    policy_state = payload.get("policy_state") if isinstance(payload, dict) else None
    if not isinstance(policy_state, dict):
        raise ValueError(f"agent '{agent_id}' policy_state missing or invalid.")

    return OpponentSpec(
        agent_id=str(agent_id),
        algo=str(algo),
        contract=dict(contract or {}),
        policy_state=normalize_state_dict(policy_state),
    )


def build_policy_fn(
    *,
    env,
    len_model: int,
    opponent: OpponentSpec,
    deterministic: bool = True,
) -> Callable[[Any], dict]:
    """
    Возвращает policy_fn(obs)->action_dict для enemyTurn(..., policy_fn=...).
    Делает кеширование сети в замыкании (CPU).
    """
    n_obs, n_actions = _parse_contract_sizes(opponent.contract)
    if n_obs <= 0 or not n_actions:
        raise ValueError(f"agent '{opponent.agent_id}' has invalid env_contract signatures.")

    if opponent.algo == "dqn":
        policy_state = normalize_state_dict(opponent.policy_state)
        dueling = any(str(k).startswith("value_heads.") for k in policy_state.keys())
        from core.models.DQN import make_dqn

        net = make_dqn(n_obs, n_actions, dueling=dueling).to(torch.device("cpu"))
        net.load_state_dict(policy_state)
        net.eval()

        def _policy_fn(obs_any) -> dict:
            obs_np = _to_np_state(obs_any)
            obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
            with torch.no_grad():
                decision = net(obs_t)
            shoot_mask = build_shoot_action_mask(env, log_fn=None, debug=False)
            action = []
            for head_idx, head in enumerate(decision):
                head_row = head.squeeze(0)
                if head_idx == 2 and shoot_mask is not None:
                    mask = torch.as_tensor(shoot_mask, dtype=torch.bool, device=head_row.device)
                    if mask.numel() == head_row.numel() and bool(mask.any()):
                        masked = head_row.clone()
                        masked[~mask] = -1e9
                        action.append(int(masked.argmax().item()))
                        continue
                action.append(int(head_row.argmax().item()))
            action_dict = convertToDict(torch.tensor([action], device="cpu"))
            for i_u in range(int(len_model)):
                action_dict[f"move_num_{i_u}"] = int(action[6 + i_u])
            return action_dict

        return _policy_fn

    if opponent.algo == "ppo":
        net = make_actor_critic(n_obs, n_actions, **ppo_kwargs_from_env()).to(torch.device("cpu"))
        load_actor_critic_state_dict(net, normalize_state_dict(opponent.policy_state))
        net.eval()

        def _policy_fn(obs_any) -> dict:
            obs_np = _to_np_state(obs_any)
            obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
            masks_cpu = build_action_masks_by_head(env, int(len_model), log_fn=None, debug=False)
            masks = [m.to(torch.device("cpu")).unsqueeze(0) for m in masks_cpu]
            with torch.no_grad():
                action_t, _logp_t, _val_t = net.act(obs_t, masks_by_head=masks, deterministic=bool(deterministic))
            action_np = action_t.squeeze(0).detach().cpu().numpy().tolist()
            action_dict = convertToDict(torch.tensor([action_np], device="cpu"))
            for i_u in range(int(len_model)):
                action_dict[f"move_num_{i_u}"] = int(action_np[6 + i_u])
            return action_dict

        return _policy_fn

    if is_az_algo(opponent.algo):
        net = make_alphazero_net(n_obs, n_actions).to(torch.device("cpu"))
        load_alphazero_state_dict(net, normalize_state_dict(opponent.policy_state))
        net.eval()
        az_eval_mode = str(os.getenv("AZ_EVAL_OPPONENT_MODE", "greedy")).strip().lower() or "greedy"
        if az_eval_mode not in {"greedy", "mcts"}:
            az_eval_mode = "greedy"
        mcts = None
        if az_eval_mode == "mcts":
            mcts_mode = az_mcts_mode_for(opponent.algo)
            mcts_cfg = MCTSConfig(
                simulations=max(
                    1,
                    int(
                        os.getenv(
                            "AZ_EVAL_OPPONENT_MCTS_SIMS",
                            os.getenv("AZ_EVAL_MCTS_SIMS", "32"),
                        )
                    ),
                ),
                c_puct=float(os.getenv("AZ_EVAL_MCTS_C_PUCT", "1.5")),
                dirichlet_alpha=float(os.getenv("AZ_EVAL_MCTS_DIR_ALPHA", "0.3")),
                dirichlet_eps=float(os.getenv("AZ_EVAL_MCTS_DIR_EPS", "0.0")),
                top_k_per_head=max(1, int(os.getenv("AZ_EVAL_MCTS_TOP_K_PER_HEAD", "8"))),
                max_depth=max(1, int(os.getenv("AZ_EVAL_MCTS_MAX_DEPTH", "1"))),
                mode=mcts_mode,
                root_dirichlet_only=True,
            )
            mcts = AlphaZeroFactorizedMCTS(net, config=mcts_cfg, device=torch.device("cpu"))

        def _policy_fn(obs_any) -> dict:
            obs_np = _to_np_state(obs_any)
            obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
            masks_cpu = build_action_masks_by_head(env, int(len_model), log_fn=None, debug=False)
            masks = [m.to(torch.device("cpu")).unsqueeze(0) for m in masks_cpu]
            if az_eval_mode == "mcts" and mcts is not None:
                legal_masks = [m.squeeze(0).detach().cpu().numpy().astype(bool) for m in masks]
                pi_targets, selected, _value = mcts.run(
                    obs=obs_np,
                    legal_masks_by_head=legal_masks,
                    temperature=float(
                        os.getenv(
                            "AZ_EVAL_OPPONENT_MCTS_TEMPERATURE",
                            os.getenv("AZ_EVAL_MCTS_TEMPERATURE", "0.10"),
                        )
                    ),
                    env=env,
                    len_model=int(len_model),
                    enemy_policy_fn=None,
                )
                if bool(deterministic):
                    action = [int(np.argmax(pi)) for pi in pi_targets]
                else:
                    action = [int(x) for x in selected]
            else:
                with torch.no_grad():
                    probs, _value = net.infer(obs_t, masks_by_head=masks)
                action = []
                stochastic_eps = float(os.getenv("AZ_OPPONENT_STOCHASTIC_EPS", "0.10"))
                stochastic_eps = max(0.0, min(1.0, stochastic_eps))
                for p in probs:
                    row = p.squeeze(0).detach().cpu()
                    arg = int(torch.argmax(row, dim=0).item())
                    if bool(deterministic):
                        action.append(arg)
                        continue
                    if np.random.rand() < stochastic_eps:
                        try:
                            sample = int(torch.multinomial(row, num_samples=1).item())
                            action.append(sample)
                            continue
                        except Exception:
                            pass
                    action.append(arg)
            action_dict = action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=int(len_model))
            return action_dict

        return _policy_fn

    if opponent.algo == "gumbel_muzero":
        net = GumbelMuZeroNet(
            obs_dim=int(n_obs),
            action_sizes=[int(x) for x in n_actions],
            latent_dim=int(os.getenv("GMZ_LATENT_DIM", "256")),
            hidden_dim=int(os.getenv("GMZ_HIDDEN_DIM", "256")),
            action_embed_dim=int(os.getenv("GMZ_ACTION_EMBED_DIM", "64")),
        ).to(torch.device("cpu"))
        net.load_state_dict(normalize_state_dict(opponent.policy_state))
        net.eval()
        gmz_mode = str(os.getenv("GMZ_OPPONENT_MODE", "search")).strip().lower() or "search"
        if gmz_mode not in {"search", "greedy"}:
            gmz_mode = "search"
        search = GumbelMuZeroSearch(
            net=net,
            config=GumbelMuZeroSearchConfig(
                num_simulations=max(
                    1,
                    int(
                        os.getenv(
                            "GMZ_EVAL_OPPONENT_SIMS",
                            os.getenv("GMZ_EVAL_SIMS", "32"),
                        )
                    ),
                ),
                root_top_k=max(1, int(os.getenv("GMZ_EVAL_ROOT_TOP_K", "8"))),
                temperature=float(
                    os.getenv(
                        "GMZ_EVAL_OPPONENT_TEMPERATURE",
                        os.getenv("GMZ_EVAL_TEMPERATURE", "0.10"),
                    )
                ),
            ),
            device=torch.device("cpu"),
        )

        def _policy_fn(obs_any) -> dict:
            obs_np = _to_np_state(obs_any)
            masks_cpu = build_action_masks_by_head(env, int(len_model), log_fn=None, debug=False)
            legal_masks = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
            obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
            if gmz_mode == "greedy":
                with torch.no_grad():
                    probs, _value = net.infer(obs_t, masks_by_head=[m.unsqueeze(0) for m in masks_cpu])
                action = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
            else:
                pi_targets, _behavior_logits, selected, _value = search.run(
                    obs=obs_np,
                    legal_masks_by_head=legal_masks,
                    deterministic=bool(deterministic),
                )
                if bool(deterministic):
                    action = [int(np.argmax(pi)) for pi in pi_targets]
                else:
                    action = [int(x) for x in selected]
            return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=int(len_model))

        return _policy_fn

    raise ValueError(f"Unsupported opponent algo: {opponent.algo}")

