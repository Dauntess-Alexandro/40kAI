from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases.types import ActionKind
from core.engine.phases.windowed_selfplay import (
    make_movement_decide_from_action_dict,
    run_model_movement_from_action,
)
from tests.engine.phases._helpers import build_env


def _move_action(n: int, overrides: dict) -> dict:
    a = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0}
    for i in range(n):
        a[f"move_num_{i}"] = int(overrides.get(i, 0))
    return a


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [2, 2]
    env.enemyCP = 0
    env._invalidate_target_cache("test")


def test_movement_decide_maps_reachable_index():
    env = build_env()
    _setup(env)
    opts = movement_options_for_unit(env, "model", 0)
    move_opts = [o for o in opts if o.kind in (ActionKind.MOVE, ActionKind.ADVANCE)]
    chosen = move_opts[-1] if move_opts else opts[0]
    k = int(chosen.param["reachable_index"])
    n = len(env.unit_health)
    win = type("W", (), {"cursor_unit_idx": 0, "options": opts})()
    decide = make_movement_decide_from_action_dict(_move_action(n, {0: k}))
    opt = decide(win)
    assert int(opt.param.get("reachable_index", -1)) == k


def test_run_model_movement_equivalent_to_movement_phase():
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    opts = movement_options_for_unit(env, "model", 0)
    move_opts = [o for o in opts if o.kind in (ActionKind.MOVE, ActionKind.ADVANCE)]
    chosen = move_opts[-1] if move_opts else opts[0]
    k = int(chosen.param["reachable_index"])
    action = _move_action(n, {0: k})
    snap = env.snapshot_state()

    with env.simulation_mode():
        env.movement_phase("model", action=action, battle_shock=[False] * n)
        coords_a = list(env.unit_coords[0])
    env.restore_state(snap)

    with env.simulation_mode():
        from core.engine.phases import phase_engine

        state = phase_engine.run_command(env, "model", lambda w: w.options[0])
        run_model_movement_from_action(env, action, state)
        coords_b = list(env.unit_coords[0])
    env.restore_state(snap)

    assert coords_a == coords_b


def test_windowed_turn_meta_contains_movement(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    action = _move_action(n, {0: 0})
    from core.engine.phases.windowed_selfplay import turn_replay_meta_from_action

    meta = turn_replay_meta_from_action(env, action, cp_before=0)
    assert meta is not None
    assert "movement:model:0" in (meta.chosen_option or "")
