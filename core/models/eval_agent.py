"""EvalAgent: единый путь действия+реакции для обеих сторон eval (P1 ≡ P2).

Резолвер конфига читает общие EVAL-флаги (без *_OPPONENT_*); при наличии
*_OPPONENT_* поднимает opponent_override_active (честный 1:1 нарушен).
"""
from __future__ import annotations

import os
import random
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import torch

from core.models.action_contract import action_tensor_to_dict, ordered_action_keys
from core.models.alphazero_ids import (
    is_alphazero_net_algo,
    is_gumbel_az_algo,
)
from core.models.utils import (
    build_action_masks_by_head,
    greedy_action_list_from_decision,
    normalize_state_dict,
    sample_action_list_from_space,
    unwrap_env,
)

_TRUTHY = frozenset({"1", "true", "yes", "on"})
_OPPONENT_KEYS = (
    "AZ_EVAL_OPPONENT_MODE", "AZ_EVAL_OPPONENT_MCTS_SIMS", "AZ_EVAL_OPPONENT_MCTS_TEMPERATURE",
    "GAZ_EVAL_OPPONENT_MODE", "GMZ_OPPONENT_MODE", "GMZ_EVAL_OPPONENT_SIMS",
    "GMZ_EVAL_OPPONENT_TEMPERATURE", "SMZ_OPPONENT_MODE", "SMZ_EVAL_OPPONENT_NUM_SAMPLES",
    "SMZ_EVAL_OPPONENT_TEMPERATURE",
)


def _bool_env(name: str, default: str) -> bool:
    return str(os.getenv(name, default)).strip().lower() in _TRUTHY


def _clamped_float(value: Any, default: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = float(default)
    return max(-1.0, min(1.0, float(parsed)))


@dataclass
class EvalSearchCfg:
    algo: str
    deterministic: bool
    epsilon: float
    search: dict[str, Any] = field(default_factory=dict)
    opponent_override_active: bool = False


def resolve_eval_search_cfg(algo: str) -> EvalSearchCfg:
    algo = str(algo or "").strip().lower()
    deterministic = _bool_env("EVAL_DETERMINISTIC", "1")
    epsilon = float(os.getenv("EVAL_EPSILON", "0"))
    override = any(os.getenv(k) is not None for k in _OPPONENT_KEYS)
    search: dict[str, Any] = {}

    if is_alphazero_net_algo(algo):
        terminal_values = {
            "terminal_value_win": _clamped_float(os.getenv("AZ_OUTCOME_VALUE_WIN", "1.0"), 1.0),
            "terminal_value_loss": _clamped_float(os.getenv("AZ_OUTCOME_VALUE_LOSS", "-1.0"), -1.0),
            "terminal_value_draw": _clamped_float(os.getenv("AZ_OUTCOME_VALUE_DRAW", "0.0"), 0.0),
        }
        if is_gumbel_az_algo(algo):
            search.update(
                mode=str(os.getenv("GAZ_EVAL_MODE", "gumbel")).strip().lower(),
                num_simulations=max(1, int(os.getenv("GAZ_EVAL_SIMS", "32"))),
                num_considered_actions=max(2, int(os.getenv("GAZ_EVAL_NUM_CONSIDERED", "8"))),
                joint_action=str(os.getenv("GAZ_JOINT_ACTION", "1")).strip() == "1",
                temperature=float(os.getenv("GAZ_EVAL_TEMPERATURE", "0.05")),
                **terminal_values,
            )
        else:
            search.update(
                mode=str(os.getenv("AZ_EVAL_MODE", "mcts")).strip().lower(),
                simulations=max(1, int(os.getenv("AZ_EVAL_MCTS_SIMS", "32"))),
                c_puct=float(os.getenv("AZ_EVAL_MCTS_C_PUCT", "1.5")),
                dirichlet_alpha=float(os.getenv("AZ_EVAL_MCTS_DIR_ALPHA", "0.3")),
                dirichlet_eps=float(os.getenv("AZ_EVAL_MCTS_DIR_EPS", "0.0")),
                top_k_per_head=max(1, int(os.getenv("AZ_EVAL_MCTS_TOP_K_PER_HEAD", "8"))),
                max_depth=max(1, int(os.getenv("AZ_EVAL_MCTS_MAX_DEPTH", "1"))),
                mcts_mode=str(os.getenv("AZ_EVAL_MCTS_MODE", "tree")).strip().lower(),
                candidate_mode=str(os.getenv("AZ_EVAL_MCTS_CANDIDATE_MODE", os.getenv("MCTS_CANDIDATE_MODE", "option"))).strip().lower(),
                window_nodes=_bool_env("AZ_EVAL_MCTS_WINDOW_NODES", os.getenv("MCTS_WINDOW_NODES", "0")),
                joint_best_child=_bool_env("AZ_EVAL_MCTS_JOINT_BEST_CHILD", os.getenv("AZ_MCTS_JOINT_BEST_CHILD", "0")),
                temperature=float(os.getenv("AZ_EVAL_MCTS_TEMPERATURE", "0.06")),
                **terminal_values,
            )
    elif algo == "gumbel_muzero":
        search.update(
            mode=str(os.getenv("GMZ_EVAL_MODE", "search")).strip().lower(),
            num_simulations=max(1, int(os.getenv("GMZ_EVAL_SIMS", "32"))),
            root_top_k=max(1, int(os.getenv("GMZ_EVAL_ROOT_TOP_K", "8"))),
            temperature=float(os.getenv("GMZ_EVAL_TEMPERATURE", "0.10")),
        )
    elif algo == "sampled_muzero":
        search.update(
            mode=str(os.getenv("SMZ_EVAL_MODE", "search")).strip().lower(),
            num_samples=int(os.getenv("SMZ_EVAL_NUM_SAMPLES", "24")),
            temperature=float(os.getenv("SMZ_EVAL_TEMPERATURE", "0.10")),
            sample_temperature=float(os.getenv("SMZ_EVAL_SAMPLE_TEMPERATURE", "1.0")),
            discount=float(os.getenv("SMZ_DISCOUNT", "0.997")),
        )
    elif algo in {"dqn", "phoenix"}:
        # DQN/Phoenix→epsilon: режимы greedy/epsilon (по аналогии с mode у старших алго).
        # greedy — argmax (как раньше); epsilon — epsilon-greedy по легальным маскам.
        mode = str(os.getenv("DQN_EVAL_MODE", "greedy")).strip().lower()
        if mode not in {"greedy", "epsilon"}:
            mode = "greedy"
        # В epsilon-режиме значение из DQN_EVAL_EPSILON (CLI-fallback на EVAL_EPSILON).
        eps = float(os.getenv("DQN_EVAL_EPSILON", str(epsilon))) if mode == "epsilon" else 0.0
        eps = max(0.0, min(1.0, eps))
        epsilon = eps
        deterministic = mode == "greedy"
        search.update(mode=mode, epsilon=eps)
    elif algo == "ppo":
        # PPO→temperature: режимы greedy/stochastic. greedy — argmax (как раньше);
        # stochastic — сэмпл из политики с температурой.
        mode = str(os.getenv("PPO_EVAL_MODE", "greedy")).strip().lower()
        if mode not in {"greedy", "stochastic"}:
            mode = "greedy"
        temp = max(0.001, min(2.0, float(os.getenv("PPO_EVAL_TEMPERATURE", "1.0"))))
        deterministic = mode == "greedy"
        search.update(mode=mode, temperature=temp)
    return EvalSearchCfg(algo=algo, deterministic=deterministic, epsilon=epsilon, search=search, opponent_override_active=override)


def _reaction_net_for_algo(algo: str, net):
    """GMZ/SMZ → None (legacy-симметрия реакций); остальные → net (value-gate)."""
    a = str(algo or "").strip().lower()
    if a in ("gumbel_muzero", "sampled_muzero"):
        return None
    return net


class EvalAgent:
    """Единый агент eval: net + (опц.) search-обёртка + reaction_net.

    select_action(env, side) -> (action_dict, fight_plan|None) — действие фазы
    и план реакций (file-страт. бой); as_policy_fn(env, side) — адаптер под
    enemyTurn(..., policy_fn=...), прикрепляющий fight-plan к env.
    """

    def __init__(self, *, algo, net, reaction_net, search, cfg, len_model):
        self.algo = str(algo).strip().lower()
        self.net = net
        self.reaction_net = reaction_net
        self.search = search
        self.cfg = cfg
        self.len_model = int(len_model)
        # Устройство берём от самой сети: build_eval_agent кладёт net на device
        # (cuda при наличии), а obs/маски обязаны быть на том же устройстве —
        # иначе RuntimeError "tensors on different devices" в net.forward.
        try:
            self.device = next(net.parameters()).device
        except (StopIteration, AttributeError):
            self.device = torch.device("cpu")

    def select_action(self, env, side: str) -> tuple[dict, dict | None]:
        obs_np = np.asarray(env.get_observation_for_side(side), dtype=np.float32)
        obs_t = torch.tensor(obs_np, dtype=torch.float32, device=self.device).unsqueeze(0)
        # Честный eval: маски строятся для стороны side (model/enemy), а не всегда "model".
        masks_cpu = build_action_masks_by_head(env, self.len_model, log_fn=None, debug=False, side=side)
        if self.algo in {"dqn", "phoenix"}:
            return self._select_dqn(env, obs_t, masks_cpu, side)
        if self.algo == "ppo":
            return self._select_ppo(env, obs_t, masks_cpu, side)
        if is_alphazero_net_algo(self.algo):
            return self._select_az(env, obs_np, masks_cpu, side)
        if self.algo in ("gumbel_muzero", "sampled_muzero"):
            return self._select_muzero(env, obs_np, masks_cpu, side)
        raise ValueError(f"EvalAgent: неподдержанный algo={self.algo}")

    def as_policy_fn(self, env, side: str) -> Callable[[Any], dict]:
        # Воркеры self-play (GMZ/PPO vs снапшот-оппонент) передают env, обёрнутый gym.make
        # в OrderEnforcing; в текущей версии Gymnasium обёртки не проксируют кастомные методы
        # движка (get_observation_for_side и т.п.) → AttributeError. Снимаем обёртки до
        # Warhammer40kEnv (как eval: env_unwrapped). Идемпотентно для уже-развёрнутого env.
        base_env = unwrap_env(env)

        def _fn(_obs_any):
            act, _plan = self.select_action(base_env, side)
            return act

        return _fn

    # --- per-algo действия (тела 1:1 с opponent_adapter.build_policy_fn) ---
    def _select_dqn(self, env, obs_t, masks_cpu, side):
        # epsilon-greedy (DQN→epsilon): с вероятностью cfg.epsilon — случайное легальное
        # действие (по per-head маскам стороны side), иначе argmax (как раньше).
        epsilon = float(getattr(self.cfg, "epsilon", 0.0) or 0.0)
        if epsilon > 0.0 and random.random() < epsilon:
            action_list = sample_action_list_from_space(env, self.len_model, masks_seq=masks_cpu)
            return action_tensor_to_dict(torch.tensor([action_list], device="cpu"), len_model=self.len_model), None
        with torch.no_grad():
            if self.algo == "phoenix":
                decision = self.net.iqn_q(obs_t)
            else:
                decision = self.net(obs_t)
        ordered_keys = ordered_action_keys(self.len_model)
        legal_by_head = {key: mask for key, mask in zip(ordered_keys, masks_cpu)}
        action = greedy_action_list_from_decision(decision, ordered_keys, legal_by_head)
        return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=self.len_model), None

    def _select_ppo(self, env, obs_t, masks_cpu, side):
        # PPO→temperature: в stochastic-режиме сэмпл из политики с температурой;
        # в greedy (deterministic) — argmax, температура игнорируется в net.act.
        temperature = float(self.cfg.search.get("temperature", 1.0)) if self.cfg.search else 1.0
        masks = [m.to(self.device).unsqueeze(0) for m in masks_cpu]
        with torch.no_grad():
            action_t, _lp, _v = self.net.act(
                obs_t,
                masks_by_head=masks,
                deterministic=self.cfg.deterministic,
                temperature=temperature,
            )
        action_np = action_t.squeeze(0).detach().cpu().numpy().tolist()
        return action_tensor_to_dict(torch.tensor([action_np], device="cpu"), len_model=self.len_model), None

    def _select_az(self, env, obs_np, masks_cpu, side):
        legal = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
        if self.search is None:
            # Greedy-режим: argmax (детерминированно). Opponent-only AZ_OPPONENT_STOCHASTIC_EPS
            # намеренно убран — честный 1:1 eval; для стохастики использовать mcts/gumbel-режим.
            masks = [m.to(self.device).unsqueeze(0) for m in masks_cpu]
            with torch.no_grad():
                probs, _value = self.net.infer(
                    torch.tensor(obs_np, dtype=torch.float32, device=self.device).unsqueeze(0),
                    masks_by_head=masks,
                )
            action = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
            return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=self.len_model), None
        s = self.search
        # Важно для честного P1/P2 eval: AZ/GAZ env-search умеет симулировать только
        # model-half через env.step(action_dict). Когда EvalAgent вызывается из
        # enemyTurn(policy_fn=...), действие относится к стороне enemy, поэтому env-search
        # на этом env дал бы семантически неверный rollout за model. Для enemy используем
        # тот же ordered/masked policy contract, но без env rollout (proxy/root-eval);
        # GMZ/SMZ ниже не используют env.rollout и потому остаются side-neutral.
        search_env = env if str(side).strip().lower() == "model" else None
        pi, selected, _v = s.run(
            obs=obs_np,
            legal_masks_by_head=legal,
            temperature=float(self.cfg.search.get("temperature", 0.06)),
            env=search_env,
            len_model=(self.len_model if search_env is not None else None),
            enemy_policy_fn=None,
        )
        if self.cfg.search.get("joint_best_child") or self.cfg.deterministic is False:
            action = [int(x) for x in selected]
        else:
            action = [int(np.argmax(p)) for p in pi] or [int(x) for x in selected]
        return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=self.len_model), None

    def _select_muzero(self, env, obs_np, masks_cpu, side):
        legal = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
        if self.search is None:
            # Greedy-режим: argmax (детерминированно). Честный 1:1 eval без opponent-specific флагов.
            masks = [m.to(self.device).unsqueeze(0) for m in masks_cpu]
            with torch.no_grad():
                probs, _value = self.net.infer(
                    torch.tensor(obs_np, dtype=torch.float32, device=self.device).unsqueeze(0),
                    masks_by_head=masks,
                )
            action = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
            return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=self.len_model), None
        pi, _bl, selected, _v = self.search.run(
            obs=obs_np,
            legal_masks_by_head=legal,
            deterministic=self.cfg.deterministic,
        )
        if self.cfg.deterministic:
            action = [int(np.argmax(p)) for p in pi] or [int(x) for x in selected]
        else:
            action = [int(x) for x in selected]
        return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=self.len_model), None


def _parse_contract_sizes(contract: dict[str, Any]) -> tuple[int, list[int]]:
    """Разбор контракта: obs_space_signature=vec:N, action_space_signature=heads:a,b,c."""
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


def _apply_az_terminal_metadata(search_cfg: dict[str, Any], metadata: dict[str, Any] | None) -> dict[str, Any]:
    out = dict(search_cfg or {})
    meta = metadata if isinstance(metadata, dict) else {}
    pairs = (
        ("terminal_value_win", "outcome_value_win", "AZ_OUTCOME_VALUE_WIN", 1.0),
        ("terminal_value_loss", "outcome_value_loss", "AZ_OUTCOME_VALUE_LOSS", -1.0),
        ("terminal_value_draw", "outcome_value_draw", "AZ_OUTCOME_VALUE_DRAW", 0.0),
    )
    for terminal_key, outcome_key, env_key, default in pairs:
        if os.getenv(env_key) is not None:
            out[terminal_key] = _clamped_float(os.getenv(env_key), default)
            continue
        if outcome_key in meta:
            out[terminal_key] = _clamped_float(meta.get(outcome_key), default)
        elif terminal_key in meta:
            out[terminal_key] = _clamped_float(meta.get(terminal_key), default)
        else:
            out[terminal_key] = _clamped_float(out.get(terminal_key, default), default)
    return out


def resolve_arch_for_algo(algo: str, payload: dict | None) -> dict | None:
    """Единый резолв арки сети для eval (learner и opponent — один путь).

    payload — dict с ключом 'arch' (checkpoint .pth ИЛИ registry meta). Для dqn
    арка инферится из state_dict в build_eval_agent → возвращаем None. Если payload
    без 'arch' — резолвер вернёт env-дефолты (как и для legacy learner).
    """
    a = str(algo or "").strip().lower()
    if not isinstance(payload, dict) or not payload.get("arch"):
        return None
    if a == "ppo":
        from core.models.PPO import ppo_arch_from_payload

        return ppo_arch_from_payload(payload)
    if is_alphazero_net_algo(a):
        from core.models.alphazero_model import alphazero_arch_from_payload

        return alphazero_arch_from_payload(payload)
    if a == "gumbel_muzero":
        from core.models.gumbel_muzero_model import gumbel_muzero_arch_from_payload

        return gumbel_muzero_arch_from_payload(payload)
    if a == "sampled_muzero":
        from core.models.sampled_muzero_model import sampled_muzero_arch_from_payload

        return sampled_muzero_arch_from_payload(payload)
    return None  # dqn и прочее


def _safe_load(load_fn, net, state, *, algo, log_fn):
    """Lenient-загрузка (missing/unexpected → WARN), но size-mismatch → понятная RU-ошибка.

    PyTorch load_state_dict(strict=False) пропускает только missing/unexpected; на совпадающих
    ключах с разным shape он всё равно падает RuntimeError('... size mismatch ...'). Для честного
    eval не маскируем это мусорной сетью — отдаём явную причину/действие.
    """
    try:
        return load_fn(net, state, log_fn=log_fn)
    except RuntimeError as exc:
        if "size mismatch" in str(exc):
            raise RuntimeError(
                f"build_eval_agent: арка сети не совпадает с весами агента (algo={algo}). "
                "Где: core/models/eval_agent.py (_safe_load → load_state_dict). "
                "Что делать: переобучите/перерегистрируйте агента так, чтобы 'arch' попал в "
                "registry-meta (train.py save_agent_artifact extra_meta), либо выставьте env-арку "
                f"под чекпойнт. Детали: {exc}"
            ) from exc
        raise


def build_eval_agent(
    *,
    algo: str,
    policy_state: dict,
    contract: dict,
    len_model: int,
    cfg: EvalSearchCfg | None = None,
    device=torch.device("cpu"),
    arch: dict | None = None,
    metadata: dict | None = None,
    log_fn=None,
) -> EvalAgent:
    """Фабрика EvalAgent: строит net + (опц.) search из контракта и cfg.search.

    Конструкторы сетей/поиска — те же, что в opponent_adapter.build_policy_fn
    (make_dqn/make_actor_critic/make_alphazero_net/GumbelMuZeroNet/
    make_sampled_muzero_net + MCTSConfig/build_gumbel_inference_search/
    GumbelMuZeroSearch/SampledMuZeroSearch), но числа симуляций/temp/mode
    берутся из cfg.search (Task 3), а не из *_OPPONENT_* env.

    arch: архитектура сети из payload learner-чекпойнта (latent/hidden/...);
    нужна чтобы недефолтные LEARNER-чекпойнты грузились 1:1 (PPO/AZ/GAZ/SMZ).
    arch=None → opponent-путь: поведение ровно как раньше (env/дефолт-арка).
    DQN арку выводит из state_dict сам — для него arch игнорируется.
    """
    algo = str(algo or "").strip().lower()
    if cfg is None:
        cfg = resolve_eval_search_cfg(algo)
    n_obs, n_actions = _parse_contract_sizes(contract)
    if n_obs <= 0 or not n_actions:
        raise ValueError(
            f"build_eval_agent: invalid env_contract signatures (algo={algo}). "
            f"obs={contract.get('obs_space_signature')!r}, act={contract.get('action_space_signature')!r}"
        )
    search_cfg = dict(cfg.search or {})
    if is_alphazero_net_algo(algo):
        search_cfg = _apply_az_terminal_metadata(search_cfg, metadata)
        cfg.search = dict(search_cfg)

    if algo == "dqn":
        from core.models.DQN import infer_dqn_arch_from_state_dict, make_dqn

        state = normalize_state_dict(policy_state)
        arch = infer_dqn_arch_from_state_dict(state)
        net = make_dqn(n_obs, n_actions, **arch).to(device)
        net.load_state_dict(state)
        net.eval()
        return EvalAgent(
            algo=algo,
            net=net,
            reaction_net=_reaction_net_for_algo(algo, net),
            search=None,
            cfg=cfg,
            len_model=len_model,
        )

    if algo == "phoenix":
        import dataclasses
        import json

        from core.models.phoenix_config import resolve_phoenix_config
        from core.models.phoenix_model import PhoenixNet, infer_phoenix_arch_from_state_dict

        state = normalize_state_dict(policy_state)
        arch_from_sd = infer_phoenix_arch_from_state_dict(state)
        hp: dict = {}
        try:
            with open("hyperparams.json", encoding="utf-8") as handle:
                loaded = json.load(handle)
            if isinstance(loaded, dict):
                hp = loaded
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            pass
        phoenix_cfg = resolve_phoenix_config(hp, os.environ)
        phoenix_cfg = dataclasses.replace(
            phoenix_cfg,
            **{k: v for k, v in arch_from_sd.items() if v is not None},
        )
        net = PhoenixNet(n_obs, n_actions, phoenix_cfg).to(device)
        try:
            net.load_state_dict(state, strict=False)
        except RuntimeError as exc:
            raise RuntimeError(
                f"[PHOENIX][EVAL] не удалось загрузить чекпойнт: {exc}. "
                "Где: core/models/eval_agent.py (build_eval_agent, phoenix loader). "
                "Что делать дальше: проверьте, что форма RL-пути (encoder+IQN-голова) "
                "совпадает с обучающей; SPR/dynamics ключи допускают strict=False."
            ) from exc
        net.eval()
        return EvalAgent(
            algo=algo,
            net=net,
            reaction_net=_reaction_net_for_algo(algo, net),
            search=None,
            cfg=cfg,
            len_model=len_model,
        )

    if algo == "ppo":
        from core.models.PPO import load_actor_critic_state_dict, make_actor_critic, ppo_kwargs_from_env

        # arch из payload (learner) → недефолтные чекпойнты грузятся 1:1; иначе env-дефолт (opponent).
        ppo_kwargs = dict(arch) if arch else ppo_kwargs_from_env()
        net = make_actor_critic(n_obs, n_actions, **ppo_kwargs).to(device)
        _safe_load(load_actor_critic_state_dict, net, normalize_state_dict(policy_state), algo=algo, log_fn=log_fn)
        net.eval()
        return EvalAgent(
            algo=algo,
            net=net,
            reaction_net=_reaction_net_for_algo(algo, net),
            search=None,
            cfg=cfg,
            len_model=len_model,
        )

    if is_alphazero_net_algo(algo):
        from core.models.alphazero_ids import az_mcts_mode_from_payload
        from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
        from core.models.alphazero_model import load_alphazero_state_dict, make_alphazero_net
        from core.models.gumbel_alphazero_search import build_gumbel_inference_search

        # arch из payload (learner) → недефолтные чекпойнты грузятся 1:1; иначе env-дефолт (opponent).
        if arch:
            net = make_alphazero_net(n_obs, n_actions, **arch).to(device)
        else:
            net = make_alphazero_net(n_obs, n_actions).to(device)
        # log_fn → расхождения ключей всплывают WARN'ом (нет тихой случайной сети); size-mismatch → понятная RU-ошибка.
        _safe_load(load_alphazero_state_dict, net, normalize_state_dict(policy_state), algo=algo, log_fn=log_fn)
        net.eval()
        mode = str(search_cfg.get("mode", "mcts")).strip().lower()
        search = None
        if is_gumbel_az_algo(algo):
            if mode == "gumbel":
                search = build_gumbel_inference_search(
                    net,
                    num_simulations=max(1, int(search_cfg.get("num_simulations", 32))),
                    num_considered_actions=max(2, int(search_cfg.get("num_considered_actions", 8))),
                    joint_action=bool(search_cfg.get("joint_action", True)),
                    terminal_value_win=float(search_cfg.get("terminal_value_win", 1.0)),
                    terminal_value_loss=float(search_cfg.get("terminal_value_loss", -1.0)),
                    terminal_value_draw=float(search_cfg.get("terminal_value_draw", 0.0)),
                    device=device,
                )
            # mode != gumbel → greedy (search=None)
        elif mode == "mcts":
            mcts_cfg = MCTSConfig(
                simulations=max(1, int(search_cfg.get("simulations", 32))),
                c_puct=float(search_cfg.get("c_puct", 1.5)),
                dirichlet_alpha=float(search_cfg.get("dirichlet_alpha", 0.3)),
                dirichlet_eps=float(search_cfg.get("dirichlet_eps", 0.0)),
                top_k_per_head=max(1, int(search_cfg.get("top_k_per_head", 8))),
                max_depth=max(1, int(search_cfg.get("max_depth", 1))),
                mode=az_mcts_mode_from_payload(algo),
                root_dirichlet_only=True,
                terminal_value_win=float(search_cfg.get("terminal_value_win", 1.0)),
                terminal_value_loss=float(search_cfg.get("terminal_value_loss", -1.0)),
                terminal_value_draw=float(search_cfg.get("terminal_value_draw", 0.0)),
            )
            search = AlphaZeroFactorizedMCTS(net, config=mcts_cfg, device=device)
        return EvalAgent(
            algo=algo,
            net=net,
            reaction_net=_reaction_net_for_algo(algo, net),
            search=search,
            cfg=cfg,
            len_model=len_model,
        )

    if algo == "gumbel_muzero":
        from core.models.gumbel_muzero_model import (
            load_gumbel_muzero_state_dict,
            make_gumbel_muzero_net,
        )
        from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig

        # arch из payload (learner/opponent) → недефолтные чекпойнты грузятся 1:1; иначе env-дефолт.
        net = make_gumbel_muzero_net(
            int(n_obs), [int(x) for x in n_actions], **(arch or {})
        ).to(device)
        # Lenient-загрузка вместо strict net.load_state_dict; size-mismatch → понятная RU-ошибка (_safe_load).
        _safe_load(load_gumbel_muzero_state_dict, net, normalize_state_dict(policy_state), algo=algo, log_fn=log_fn)
        net.eval()
        mode = str(search_cfg.get("mode", "search")).strip().lower()
        search = None
        if mode != "greedy":
            search = GumbelMuZeroSearch(
                net=net,
                config=GumbelMuZeroSearchConfig(
                    num_simulations=max(1, int(search_cfg.get("num_simulations", 32))),
                    root_top_k=max(1, int(search_cfg.get("root_top_k", 8))),
                    temperature=float(search_cfg.get("temperature", 0.10)),
                ),
                device=device,
            )
        return EvalAgent(
            algo=algo,
            net=net,
            reaction_net=_reaction_net_for_algo(algo, net),
            search=search,
            cfg=cfg,
            len_model=len_model,
        )

    if algo == "sampled_muzero":
        from core.models.sampled_muzero_model import load_sampled_muzero_state_dict, make_sampled_muzero_net
        from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig

        # arch из payload (learner) → недефолтные чекпойнты грузятся 1:1; иначе env-дефолт (opponent).
        if arch:
            net = make_sampled_muzero_net(
                obs_dim=int(n_obs),
                action_sizes=[int(x) for x in n_actions],
                **arch,
            ).to(device)
        else:
            net = make_sampled_muzero_net(
                obs_dim=int(n_obs),
                action_sizes=[int(x) for x in n_actions],
                latent_dim=int(os.getenv("SMZ_LATENT_DIM", "256")),
                hidden_dim=int(os.getenv("SMZ_HIDDEN_DIM", "256")),
                action_embed_dim=int(os.getenv("SMZ_ACTION_EMBED_DIM", "64")),
            ).to(device)
        # Лениентный загрузчик (strict=False) через _safe_load: missing/unexpected → WARN, size-mismatch → RU-ошибка.
        _safe_load(load_sampled_muzero_state_dict, net, normalize_state_dict(policy_state), algo=algo, log_fn=log_fn)
        net.eval()
        mode = str(search_cfg.get("mode", "search")).strip().lower()
        search = None
        if mode != "greedy":
            search = SampledMuZeroSearch(
                net=net,
                config=SampledMuZeroSearchConfig(
                    num_samples=max(1, int(search_cfg.get("num_samples", 24))),
                    temperature=float(search_cfg.get("temperature", 0.10)),
                    sample_temperature=float(search_cfg.get("sample_temperature", 1.0)),
                    prior_weight=0.0,
                    dedup=True,
                    discount=float(search_cfg.get("discount", 0.997)),
                ),
                device=device,
            )
        return EvalAgent(
            algo=algo,
            net=net,
            reaction_net=_reaction_net_for_algo(algo, net),
            search=search,
            cfg=cfg,
            len_model=len_model,
        )

    raise ValueError(f"build_eval_agent: неподдержанный algo={algo}")
