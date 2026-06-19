"""DQN ↔ стратагемы: V-proxy (masked max-Q), fight-plan builder, policy install.

Переиспользует AZ-инфру (reaction_value_policy, attach_fight_stratagem_plan)
поверх DQN.infer_with_value.
"""

from __future__ import annotations

import os

import numpy as np
import torch

from core.engine.phases.stratagem_engine import apply as _apply_stratagem
from core.engine.phases.stratagems import for_phase, usage_limit_reached
from core.engine.phases.types import Phase
from core.models.action_contract import ordered_action_keys
from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def dqn_reaction_value_policy_enabled(default: str = "1") -> bool:
    raw = str(os.getenv("DQN_REACTION_VALUE_POLICY", default)).strip().lower()
    return raw in _TRUTHY


def install_dqn_stratagem_policy(env, policy_net, device) -> None:
    """Learner-only value-gate для стратагем (model side)."""
    from core.models.reaction_value_policy import make_stratagem_value_policy

    e = unwrap_env(env)
    e._reaction_net_by_side = {"model": policy_net}
    e.reaction_policy = make_stratagem_value_policy(e._reaction_net_by_side, device=device)


def _masks_for_side(env, side: str, device) -> list:
    """Legal action masks в порядке ordered_action_keys — для masked max-Q."""
    e = unwrap_env(env)
    legal = e.get_legal_action_masks_by_head(side=side)
    n_units = len(e.unit_data) if side == "model" else len(e.enemy_data)
    keys = ordered_action_keys(int(n_units))
    return [
        torch.tensor(legal[k], dtype=torch.bool, device=device).unsqueeze(0)
        for k in keys
    ]


def dqn_value(env, policy_net, device, side: str) -> float:
    """max-Q V(s) для стороны side (masked infer_with_value)."""
    e = unwrap_env(env)
    obs = torch.tensor(
        np.asarray([e.get_observation_for_side(side)], dtype=np.float32),
        device=device,
    )
    masks = _masks_for_side(e, side, device)
    with torch.no_grad():
        _, v = policy_net.infer_with_value(obs, masks_by_head=masks)
    return float(v.reshape(-1)[0].item())


def dqn_build_fight_plan(env, policy_net, device, side: str = "model") -> dict[int, str]:
    """Hungry Void / Command Re-roll план через max-Q lookahead (2 ветки на юнит)."""
    e = unwrap_env(env)
    if getattr(e, "_reaction_sim_active", False):
        return {}
    health = e.unit_health if side == "model" else e.enemy_health
    in_attack = e.unitInAttack if side == "model" else e.enemyInAttack
    plan: dict[int, str] = {}
    eps = 1e-3
    for d in for_phase(Phase.FIGHT):
        cp = int(e.modelCP if side == "model" else e.enemyCP)
        if cp < d.cp_cost:
            continue
        if usage_limit_reached(e, side, d, phase="fight"):
            continue
        for u in range(len(health)):
            if health[u] <= 0 or in_attack[u][0] != 1:
                continue
            if u in plan:
                continue
            snap = e.snapshot_state()
            try:
                with e.simulation_mode():
                    e.restore_state(snap)
                    _apply_stratagem(e, side, d.id, u, phase="fight")
                    v_apply = dqn_value(e, policy_net, device, side)
                    e.restore_state(snap)
                    v_pass = dqn_value(e, policy_net, device, side)
            finally:
                e.restore_state(snap)
            if v_apply > v_pass + eps:
                plan[u] = d.id
    return plan
