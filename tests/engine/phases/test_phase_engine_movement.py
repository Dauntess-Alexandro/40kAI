from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env


def _move_action(n: int, overrides: dict) -> dict:
    a = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0}
    for i in range(n):
        a[f"move_num_{i}"] = int(overrides.get(i, 0))
    return a


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [2, 2]
    env.enemyCP = 0  # отключаем реакции (overwatch) → движение детерминированно
    env._invalidate_target_cache("test")


def _pick_last_move(env):
    opts = movement_options_for_unit(env, "model", 0)
    move_opts = [o for o in opts if o.kind in (ActionKind.MOVE, ActionKind.ADVANCE)]
    chosen = move_opts[-1] if move_opts else opts[0]
    return chosen


def test_decide_move_equivalent_to_action():
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    chosen = _pick_last_move(env)
    k = chosen.param["reachable_index"]
    dest_x, dest_y = chosen.param["dest"]

    snap = env.snapshot_state()
    with env.simulation_mode():
        env.movement_phase("model", action=_move_action(n, {0: k}), battle_shock=[False] * n)
        coords_a = list(env.unit_coords[0])
    env.restore_state(snap)

    with env.simulation_mode():
        env.movement_phase(
            "model", action=_move_action(n, {}), battle_shock=[False] * n,
            decide_move=lambda i: k if i == 0 else 0,
        )
        coords_b = list(env.unit_coords[0])
    env.restore_state(snap)

    assert coords_a == coords_b == [int(dest_y), int(dest_x)]


def test_decide_move_zero_keeps_position():
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    snap = env.snapshot_state()
    with env.simulation_mode():
        env.movement_phase(
            "model", action=_move_action(n, {}), battle_shock=[False] * n,
            decide_move=lambda i: 0,
        )
        coords = list(env.unit_coords[0])
    env.restore_state(snap)
    assert coords == [2, 2]
