from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from core.engine.agent_registry import compatible_contracts, load_agent_by_id, resolve_agent_algo
from core.models.utils import normalize_state_dict


@dataclass(frozen=True)
class OpponentSpec:
    agent_id: str
    algo: str  # "dqn" | "ppo" | "alphazero_tree" | "alphazero_proxy" | "gumbel_muzero" | "sampled_muzero"
    contract: dict[str, Any]
    policy_state: dict[str, Any]
    metadata: dict[str, Any] | None = None
    arch: dict[str, Any] | None = None  # арка сети из registry-meta (resolve_arch_for_algo); None для legacy/обратной совместимости


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


def load_agent_opponent(*, agent_id: str, expected_contract: dict[str, Any] | None = None) -> OpponentSpec:
    payload = load_agent_by_id(str(agent_id))
    meta = payload.get("meta") if isinstance(payload, dict) else {}
    policy_state_guess = payload.get("policy_state") if isinstance(payload, dict) else None
    target_state_guess = payload.get("target_state") if isinstance(payload, dict) else None
    algo = resolve_agent_algo(
        meta=meta if isinstance(meta, dict) else {},
        policy_state=policy_state_guess if isinstance(policy_state_guess, dict) else None,
        target_state=target_state_guess if isinstance(target_state_guess, dict) else None,
        agent_id=str(agent_id),
    )

    contract = payload.get("contract") if isinstance(payload, dict) else None
    if expected_contract is not None:
        ok, reason = compatible_contracts(expected_contract, contract or {})
        if not ok:
            raise ValueError(f"agent '{agent_id}' contract mismatch: {reason}")

    policy_state = payload.get("policy_state") if isinstance(payload, dict) else None
    if not isinstance(policy_state, dict):
        raise ValueError(f"agent '{agent_id}' policy_state missing or invalid.")

    # Арка сети из registry-meta через единый резолвер (learner и opponent — один путь).
    # meta без 'arch' → None (legacy-агенты строятся на env-дефолте, симметрично для обеих сторон).
    from core.models.eval_agent import resolve_arch_for_algo

    arch = resolve_arch_for_algo(str(algo), meta if isinstance(meta, dict) else {})

    return OpponentSpec(
        agent_id=str(agent_id),
        algo=str(algo),
        contract=dict(contract or {}),
        policy_state=normalize_state_dict(policy_state),
        metadata=dict(meta) if isinstance(meta, dict) else {},
        arch=arch,
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

    Тонкая обёртка над `build_eval_agent` (единый путь действия+реакции, Task 4):
    конструкция net+search вынесена в фабрику EvalAgent, здесь — только адаптер
    под legacy-сигнатуру. Числа симуляций/temp/mode берёт из `resolve_eval_search_cfg`.
    """
    from core.models.eval_agent import build_eval_agent, resolve_eval_search_cfg

    cfg = resolve_eval_search_cfg(opponent.algo)
    cfg.deterministic = bool(deterministic)
    agent = build_eval_agent(
        algo=opponent.algo,
        policy_state=opponent.policy_state,
        contract=opponent.contract,
        len_model=int(len_model),
        cfg=cfg,
        metadata=opponent.metadata,
    )
    return agent.as_policy_fn(env, "enemy")
