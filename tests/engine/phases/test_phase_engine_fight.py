import random

import numpy as np

from core.engine.phases import phase_engine
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env


def _engaged(env):
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env.modelCP = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("test")


def _pick_hungry(unit_idx):
    def decide(window):
        for o in window.options:
            if o.kind is ActionKind.USE_STRATAGEM and o.meta.get("stratagem_id") == "hungry_void" and o.unit_idx == unit_idx:
                return o
        return window.options[0]

    return decide


def _pick_pass(window):
    return window.options[0]


def test_run_fight_pass_does_not_spend_cp():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    _engaged(env)
    random.seed(3)
    np.random.seed(3)
    with env.simulation_mode():
        phase_engine.run_fight(env, "model", _pick_pass)
    assert env.modelCP == 1
    assert env.stratagem_used == []


def test_run_fight_hungry_void_spends_cp_and_records_journal():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    _engaged(env)
    env.unit_data[0]["Keywords"] = ["Necrons"]
    random.seed(3)
    np.random.seed(3)
    with env.simulation_mode():
        phase_engine.run_fight(env, "model", _pick_hungry(0))
    assert env.modelCP == 0  # 1 - 1 (Hungry Void)
    assert ("model", "hungry_void", env.battle_round, "fight", 0) in env.stratagem_used


def test_run_fight_pass_is_behavior_neutral_vs_direct_fight_phase():
    """PASS-путь run_fight == прямой env.fight_phase по итоговому состоянию (фикс. seed)."""
    env_a = build_env()
    env_a.reset(options={"m": env_a.model, "e": env_a.enemy, "trunc": True})
    _engaged(env_a)
    random.seed(21)
    np.random.seed(21)
    with env_a.simulation_mode():
        phase_engine.run_fight(env_a, "model", _pick_pass)
    state_engine = (
        round(float(env_a.enemy_health[0]), 3),
        round(float(env_a.unit_health[0]), 3),
        int(env_a.modelCP),
    )

    env_b = build_env()
    env_b.reset(options={"m": env_b.model, "e": env_b.enemy, "trunc": True})
    _engaged(env_b)
    random.seed(21)
    np.random.seed(21)
    with env_b.simulation_mode():
        env_b.fight_phase("model")
    state_direct = (
        round(float(env_b.enemy_health[0]), 3),
        round(float(env_b.unit_health[0]), 3),
        int(env_b.modelCP),
    )

    assert state_engine == state_direct
