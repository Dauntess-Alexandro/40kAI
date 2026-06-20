"""PPO ↔ стратагемы: critic-V, fight-plan builder, side-generic policy install.

Переиспользует AZ-инфру (reaction_value_policy, attach_fight_stratagem_plan)
поверх ActorCriticMultiHead.infer_with_value (честный critic V).
"""

from __future__ import annotations

import os

import numpy as np
import torch

from core.engine.phases.stratagem_engine import apply as _apply_stratagem
from core.engine.phases.stratagems import for_phase, usage_limit_reached
from core.engine.phases.types import Phase
from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def ppo_reaction_value_policy_enabled(default: str = "1") -> bool:
    raw = str(os.getenv("PPO_REACTION_VALUE_POLICY", default)).strip().lower()
    return raw in _TRUTHY


def install_ppo_stratagem_policy(env, device, net_by_side: dict) -> None:
    """Value-gate для стратагем. Side-generic: net_by_side = {side: net}.

    v1 кладёт {"model": ac_net}. Both-sides (честный p1/p2) — тот же вызов с
    {"model": p1, "enemy": p2}, без правок движка/bridge. Сторона без сети → legacy.
    """
    from core.models.reaction_value_policy import make_stratagem_value_policy

    e = unwrap_env(env)
    e._reaction_net_by_side = dict(net_by_side)
    e.reaction_policy = make_stratagem_value_policy(e._reaction_net_by_side, device=device)


def ppo_value(env, ac_net, device, side: str) -> float:
    """critic V(s) для стороны side. Маски не нужны — critic mask-независим."""
    e = unwrap_env(env)
    obs = torch.tensor(
        np.asarray([e.get_observation_for_side(side)], dtype=np.float32),
        device=device,
    )
    with torch.no_grad():
        _, v = ac_net.infer_with_value(obs, masks_by_head=None)
    return float(v.reshape(-1)[0].item())


def ppo_build_fight_plan(env, ac_net, device, side: str = "model") -> dict[int, str]:
    """Hungry Void / Command Re-roll план через critic-V lookahead (2 ветки на юнит).

    Структура 1:1 с dqn_build_fight_plan: snapshot → apply/pass → critic V → выбор.
    eps=1e-3: greedy per-unit planner без MCTS-joint → лёгкий уклон в PASS.
    """
    e = unwrap_env(env)
    if getattr(e, "_reaction_sim_active", False):
        return {}  # recursion guard
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
                    v_apply = ppo_value(e, ac_net, device, side)
                    e.restore_state(snap)
                    v_pass = ppo_value(e, ac_net, device, side)
            finally:
                e.restore_state(snap)
            if v_apply > v_pass + eps:
                plan[u] = d.id
    return plan
