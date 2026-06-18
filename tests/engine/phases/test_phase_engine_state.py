import math

from core.engine.phases import phase_engine
from core.engine.phases.option_generator import movement_options_for_unit, shooting_options_for_unit
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 0
    env.modelCP = 0
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.unit_coords[0] = [15, 15]
    env.enemy_coords[0] = [20, 20]
    env._sync_model_positions_to_anchors()
    env._invalidate_target_cache("test")


def _pick_movement_kind(env, kind):
    opts = movement_options_for_unit(env, "model", 0)
    for opt in opts:
        if opt.kind is kind:
            return opt
    raise AssertionError(f"no movement option with kind={kind}")


def _decide_option_for_unit(unit_idx, chosen):
    def decide(window):
        if window.cursor_unit_idx == unit_idx:
            return chosen
        return window.options[0]

    return decide


def _first_shoot(window):
    for opt in window.options:
        if opt.kind is ActionKind.SHOOT:
            return opt
    return window.options[0]


def _first_charge(window):
    for opt in window.options:
        if opt.kind is ActionKind.CHARGE:
            return opt
    return window.options[0]


def test_advance_state_blocks_windowed_shooting_without_assault():
    env = build_env()
    _setup(env)
    advance = _pick_movement_kind(env, ActionKind.ADVANCE)

    snap = env.snapshot_state()
    with env.simulation_mode():
        state = phase_engine.run_movement(env, "model", _decide_option_for_unit(0, advance))
        assert state.advanced_flags[0] is True
        env.enemy_coords[0] = [env.unit_coords[0][0], min(env.b_hei - 1, env.unit_coords[0][1] + 1)]
        env._sync_model_positions_to_anchors()
        env._invalidate_target_cache("test_after_manual_target_place")
        hp_before = list(env.enemy_health)

        state = phase_engine.run_shooting(env, "model", _first_shoot, state)

        assert env.enemy_health == hp_before
        assert state.advanced_flags[0] is True
    env.restore_state(snap)


def test_advance_state_blocks_windowed_charge():
    env = build_env()
    _setup(env)
    advance = _pick_movement_kind(env, ActionKind.ADVANCE)

    snap = env.snapshot_state()
    with env.simulation_mode():
        state = phase_engine.run_movement(env, "model", _decide_option_for_unit(0, advance))
        assert state.advanced_flags[0] is True
        env.enemy_coords[0] = [env.unit_coords[0][0], min(env.b_hei - 1, env.unit_coords[0][1] + 1)]
        env._sync_model_positions_to_anchors()
        env._invalidate_target_cache("test_after_manual_target_place")

        phase_engine.run_charge(env, "model", _first_charge, state)

        assert env.unitInAttack[0][0] == 0
    env.restore_state(snap)


def test_shooting_window_is_built_from_post_movement_state():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 0
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.unit_weapon[0]["Range"] = 3
    env.unit_coords[0] = [15, 7]
    env.enemy_coords[0] = [15, 15]
    env._sync_model_positions_to_anchors()
    env._invalidate_target_cache("test")

    assert all(opt.kind is not ActionKind.SHOOT for opt in shooting_options_for_unit(env, "model", 0))

    enemy_row, enemy_col = env.enemy_coords[0]
    move_to_range = None
    for opt in movement_options_for_unit(env, "model", 0):
        if opt.kind is not ActionKind.MOVE:
            continue
        dest_col, dest_row = opt.param["dest"]
        if math.dist((dest_row, dest_col), (enemy_row, enemy_col)) <= 3:
            move_to_range = opt
            break
    assert move_to_range is not None

    snap = env.snapshot_state()
    with env.simulation_mode():
        phase_engine.run_movement(env, "model", _decide_option_for_unit(0, move_to_range))

        opts_after = shooting_options_for_unit(env, "model", 0)
        assert any(opt.kind is ActionKind.SHOOT and opt.target_idx == 0 for opt in opts_after)
    env.restore_state(snap)
