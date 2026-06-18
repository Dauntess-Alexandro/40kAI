import random

import numpy as np

from core.engine.phases.windowed_selfplay import (
    run_model_charge_from_action,
    run_model_shooting_from_action,
)
from tests.engine.phases._helpers import build_env


def _action(n: int, *, shoot: int = 0, attack: int = 1, charge: int = 0) -> dict:
    a = {
        "move": 4,
        "attack": int(attack),
        "shoot": int(shoot),
        "charge": int(charge),
        "use_cp": 0,
        "cp_on": 0,
    }
    for i in range(n):
        a[f"move_num_{i}"] = 0
    return a


def _setup_shoot(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.unit_health[1] = 0.0
    env.enemy_coords[0] = [11, 10]
    env.enemy_coords[1] = [12, 10]
    env.enemyCP = 0
    env._invalidate_target_cache("test")


def _setup_charge(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.unit_health[1] = 0.0
    env.enemy_coords[0] = [14, 10]
    env.enemy_coords[1] = [29, 29]
    env.enemyCP = 0
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env._invalidate_target_cache("test")


def test_run_model_shooting_equivalent_to_shooting_phase():
    env = build_env()
    _setup_shoot(env)
    n = len(env.unit_health)
    action = _action(n, shoot=1)
    snap = env.snapshot_state()

    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * n, action=action)
        hp_a = [round(float(h), 2) for h in env.enemy_health]
    env.restore_state(snap)

    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        from core.engine.phases.types import PhaseTurnState

        state = PhaseTurnState(side="model", battle_shock=[False] * n, advanced_flags=[False] * n)
        run_model_shooting_from_action(env, action, state)
        hp_b = [round(float(h), 2) for h in env.enemy_health]
    env.restore_state(snap)

    assert hp_a == hp_b


def test_run_model_charge_equivalent_to_charge_phase():
    env = build_env()
    _setup_charge(env)
    n = len(env.unit_health)
    action = _action(n, attack=1, charge=0)
    snap = env.snapshot_state()

    random.seed(11)
    np.random.seed(11)
    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * n, action=action)
        state_a = (
            list(env.unitInAttack[0]),
            list(env.unit_coords[0]),
        )
    env.restore_state(snap)

    random.seed(11)
    np.random.seed(11)
    with env.simulation_mode():
        from core.engine.phases.types import PhaseTurnState

        state = PhaseTurnState(side="model", battle_shock=[False] * n, advanced_flags=[False] * n)
        run_model_charge_from_action(env, action, state)
        state_b = (
            list(env.unitInAttack[0]),
            list(env.unit_coords[0]),
        )
    env.restore_state(snap)

    assert state_a == state_b
