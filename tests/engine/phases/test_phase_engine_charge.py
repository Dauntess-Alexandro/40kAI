import random

import numpy as np

from core.engine.phases import phase_engine
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env


def _caction(n: int, attack: int = 1, charge: int = 0) -> dict:
    a = {"move": 4, "attack": int(attack), "shoot": 0, "charge": int(charge), "use_cp": 0, "cp_on": 0}
    for i in range(n):
        a[f"move_num_{i}"] = 0
    return a


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.unit_health[1] = 0.0  # только юнит 0 чарджит
    env.enemy_coords[0] = [14, 10]  # дистанция 4 → в пределах чарджа
    env.enemy_coords[1] = [29, 29]
    env.enemyCP = 0  # без Heroic Intervention реакции
    # unitCharged/enemyCharged сайзятся в step()/enemyTurn(); при прямом вызове charge_phase — инициализируем сами
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env._invalidate_target_cache("test")
    assert 0 in env.get_charge_targets_for_unit("model", 0)


def _state_after(env):
    return (
        list(env.unitInAttack[0]),
        list(env.unit_coords[0]),
        [round(float(h), 2) for h in env.enemy_health],
        int(env.modelCP),
    )


def test_decide_charge_equivalent_to_action():
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    snap = env.snapshot_state()

    env.restore_state(snap)
    random.seed(5)
    np.random.seed(5)
    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * n, action=_caction(n, attack=1, charge=0))
    s_action = _state_after(env)

    env.restore_state(snap)
    random.seed(5)
    np.random.seed(5)
    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * n, action=_caction(n, attack=1, charge=0),
                         decide_charge=lambda i: 0 if i == 0 else None)
    s_decide = _state_after(env)

    env.restore_state(snap)
    assert s_action == s_decide


def test_decide_charge_none_skips_charge():
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    snap = env.snapshot_state()
    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * n, action=_caction(n, attack=1, charge=0),
                         decide_charge=lambda i: None)
        engaged = env.unitInAttack[0][0]
    env.restore_state(snap)
    assert engaged == 0  # юнит не вступил в бой (чардж не объявлен)


def _pick_charge_target(unit_idx, target):
    def decide(window):
        if window.cursor_unit_idx == unit_idx:
            for o in window.options:
                if o.kind is ActionKind.CHARGE and o.target_idx == target:
                    return o
        return window.options[0]  # PASS

    return decide


def test_run_charge_matches_decide_charge():
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    snap = env.snapshot_state()

    random.seed(8)
    np.random.seed(8)
    with env.simulation_mode():
        phase_engine.run_charge(env, "model", _pick_charge_target(0, 0))
    s_engine = _state_after(env)

    env.restore_state(snap)
    random.seed(8)
    np.random.seed(8)
    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * n, action=_caction(n, attack=1, charge=0),
                         decide_charge=lambda i: 0 if i == 0 else None)
    s_seam = _state_after(env)

    env.restore_state(snap)
    assert s_engine == s_seam
