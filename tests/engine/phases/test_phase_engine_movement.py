from core.engine.phases import phase_engine
from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases.types import ActionKind
from core.engine.utils import distance
from tests.engine.phases._helpers import build_env, flat_default_action


def _move_action(n: int, overrides: dict) -> dict:
    a = flat_default_action(n)
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


def test_move_head_nonstay_repairs_zero_move_num_toward_objective(monkeypatch):
    env = build_env()
    _setup(env)
    env.unit_health[1] = 0
    n = len(env.unit_health)
    action = _move_action(n, {})
    action["move"] = 0
    before = min(distance(env.unit_coords[0], obj) for obj in env.coordsOfOM)
    captured: list[str] = []
    monkeypatch.setattr(env, "_log", lambda msg: captured.append(str(msg)))

    snap = env.snapshot_state()
    with env.simulation_mode():
        _advanced, _reward, meta = env.movement_phase("model", action=action, battle_shock=[False] * n)
        coords = list(env.unit_coords[0])
        after = min(distance(env.unit_coords[0], obj) for obj in env.coordsOfOM)
        info = env.get_info()
    env.restore_state(snap)

    assert coords != [2, 2]
    assert after < before
    assert int(meta["zero_stay_repaired"]) == 1
    assert int(info["movement_meta"]["zero_stay_repaired"]) == 1
    assert any("[MOVE][ZERO_STAY]" in msg and "repaired" in msg for msg in captured)


def test_move_head_nonstay_keeps_zero_move_num_on_objective(monkeypatch):
    env = build_env()
    _setup(env)
    env.unit_health[1] = 0
    env.unit_coords[0] = [int(env.coordsOfOM[0][0]), int(env.coordsOfOM[0][1])]
    n = len(env.unit_health)
    action = _move_action(n, {})
    action["move"] = 0
    captured: list[str] = []
    monkeypatch.setattr(env, "_log", lambda msg: captured.append(str(msg)))

    snap = env.snapshot_state()
    with env.simulation_mode():
        _advanced, _reward, meta = env.movement_phase("model", action=action, battle_shock=[False] * n)
        coords = list(env.unit_coords[0])
    env.restore_state(snap)

    assert coords == [int(env.coordsOfOM[0][0]), int(env.coordsOfOM[0][1])]
    assert int(meta["zero_stay_repaired"]) == 0
    assert int(meta["zero_stay_kept"]) == 1
    assert meta["zero_stay_keep_reasons"].get("on_objective") == 1
    assert any("[MOVE][ZERO_STAY]" in msg and "reason=on_objective" in msg for msg in captured)


def _pick_index_for(unit_idx, k):
    def decide(window):
        if window.cursor_unit_idx == unit_idx:
            for o in window.options:
                if o.param.get("reachable_index") == k:
                    return o
        return window.options[0]  # stay (index 0)

    return decide


def test_run_movement_moves_unit():
    env = build_env()
    _setup(env)
    chosen = _pick_last_move(env)
    k = chosen.param["reachable_index"]
    dest_x, dest_y = chosen.param["dest"]

    snap = env.snapshot_state()
    with env.simulation_mode():
        phase_engine.run_movement(env, "model", _pick_index_for(0, k))
        coords = list(env.unit_coords[0])
    env.restore_state(snap)
    assert coords == [int(dest_y), int(dest_x)]


def test_run_movement_stay_keeps_position():
    env = build_env()
    _setup(env)
    snap = env.snapshot_state()
    with env.simulation_mode():
        phase_engine.run_movement(env, "model", lambda window: window.options[0])
        coords = list(env.unit_coords[0])
    env.restore_state(snap)
    assert coords == [2, 2]
