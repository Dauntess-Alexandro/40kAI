import random

import numpy as np

from core.engine.phases import phase_engine
from core.engine.phases.option_generator import shooting_options_for_unit
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env, flat_default_action


def _action(n: int, shoot: int = 0, unit_idx: int = 0) -> dict:
    return flat_default_action(n, **{f"shoot_num_{int(unit_idx)}": int(shoot)})


def _setup_two_targets(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.unit_health[1] = 0.0  # юнит 1 мёртв → стреляет только юнит 0
    env.enemy_coords[0] = [11, 10]
    env.enemy_coords[1] = [12, 10]
    env.enemyCP = 0
    env._invalidate_target_cache("test")
    # требуем 2 цели в дальности у юнита 0
    assert len(env.get_shoot_targets_for_unit("model", 0)) >= 2


def test_decide_shoot_equivalent_to_action():
    env = build_env()
    _setup_two_targets(env)
    n = len(env.unit_health)
    snap = env.snapshot_state()

    env.restore_state(snap)
    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * n, action=_action(n, shoot=1))
    health_action = list(env.enemy_health)

    env.restore_state(snap)
    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * n, action=_action(n, shoot=0),
                           decide_shoot=lambda i: 1)
    health_decide = list(env.enemy_health)

    env.restore_state(snap)
    assert health_action == health_decide


def test_decide_shoot_is_consulted():
    env = build_env()
    _setup_two_targets(env)
    n = len(env.unit_health)
    seen = []

    def decide(i):
        seen.append(int(i))
        return 0

    snap = env.snapshot_state()
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * n, action=_action(n), decide_shoot=decide)
    env.restore_state(snap)
    assert 0 in seen  # стрелявший юнит 0 спросил политику


def _pick_shoot_rank(unit_idx, rank):
    def decide(window):
        if window.cursor_unit_idx == unit_idx:
            for o in window.options:
                if o.kind is ActionKind.SHOOT and o.param.get("local_rank") == rank:
                    return o
        return window.options[0]  # PASS

    return decide


def test_run_shooting_matches_decide_shoot():
    env = build_env()
    _setup_two_targets(env)
    n = len(env.unit_health)
    # rank=1 у юнита 0
    opts = shooting_options_for_unit(env, "model", 0)
    assert any(o.kind is ActionKind.SHOOT and o.param.get("local_rank") == 1 for o in opts)
    snap = env.snapshot_state()

    random.seed(11)
    np.random.seed(11)
    with env.simulation_mode():
        phase_engine.run_shooting(env, "model", _pick_shoot_rank(0, 1))
    health_engine = list(env.enemy_health)

    env.restore_state(snap)
    random.seed(11)
    np.random.seed(11)
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * n, action=_action(n), decide_shoot=lambda i: 1 if i == 0 else 0)
    health_seam = list(env.enemy_health)

    env.restore_state(snap)
    assert health_engine == health_seam
