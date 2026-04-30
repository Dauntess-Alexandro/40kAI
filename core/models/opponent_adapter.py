from __future__ import annotations

import collections
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np
import torch

from core.engine.agent_registry import compatible_contracts, load_agent_by_id
from core.models.DQN import DQN
from core.models.PPO import ActorCriticMultiHead
from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.action_contract import action_tensor_to_dict
from core.models.utils import build_action_masks_by_head, build_shoot_action_mask, convertToDict, normalize_state_dict


@dataclass(frozen=True)
class OpponentSpec:
    agent_id: str
    algo: str  # "dqn" | "ppo" | "alphazero"
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
    if algo not in {"dqn", "ppo", "alphazero"}:
        # Backward-compatible inference for older artifacts:
        # - DQN artifacts usually have target_state saved
        # - PPO artifacts usually don't
        target_state = payload.get("target_state") if isinstance(payload, dict) else None
        if isinstance(target_state, dict):
            algo = "dqn"
        else:
            # last-resort heuristic by key prefixes
            policy_state_guess = payload.get("policy_state") if isinstance(payload, dict) else None
            if isinstance(policy_state_guess, dict) and any(str(k).startswith("policy_heads.") for k in policy_state_guess.keys()):
                algo = "ppo"
            else:
                # AlphaZero artifacts usually store policy-value key.
                if isinstance(policy_state_guess, dict) and any(str(k).startswith("policy_heads.") for k in policy_state_guess.keys()):
                    algo = "alphazero"
                else:
                    raise ValueError(f"agent '{agent_id}' has unsupported algo='{algo}' (expected dqn/ppo/alphazero).")

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
        dist_type = str(os.getenv("DIST_TYPE", "iqn")).strip().lower() or "iqn"
        iqn_n_quant = int(os.getenv("IQN_N_QUANTILES", "32"))
        iqn_n_target = int(os.getenv("IQN_N_TARGET_QUANTILES", "32"))
        iqn_n_tau = int(os.getenv("IQN_N_TAU_SAMPLES", "32"))
        iqn_embed = int(os.getenv("IQN_EMBED_DIM", "64"))
        noisy_sigma0 = float(os.getenv("NOISY_SIGMA0", "0.5"))
        net = DQN(
            n_obs, n_actions, dueling=dueling, noisy=True,
            noisy_sigma0=noisy_sigma0, distributional=dist_type,
            iqn_num_quantiles=iqn_n_quant, iqn_num_target_quantiles=iqn_n_target,
            iqn_num_tau_samples=iqn_n_tau, iqn_embed_dim=iqn_embed
        ).to(torch.device("cpu"))
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
        net = ActorCriticMultiHead(n_obs, n_actions).to(torch.device("cpu"))
        net.load_state_dict(normalize_state_dict(opponent.policy_state))
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

    if opponent.algo == "alphazero":
        net = AlphaZeroPolicyValueNet(n_obs, n_actions).to(torch.device("cpu"))
        net.load_state_dict(normalize_state_dict(opponent.policy_state))
        net.eval()

        def _policy_fn(obs_any) -> dict:
            obs_np = _to_np_state(obs_any)
            obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
            masks_cpu = build_action_masks_by_head(env, int(len_model), log_fn=None, debug=False)
            masks = [m.to(torch.device("cpu")).unsqueeze(0) for m in masks_cpu]
            with torch.no_grad():
                probs, _value = net.infer(obs_t, masks_by_head=masks)
            action = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
            action_dict = action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=int(len_model))
            return action_dict

        return _policy_fn

    raise ValueError(f"Unsupported opponent algo: {opponent.algo}")

