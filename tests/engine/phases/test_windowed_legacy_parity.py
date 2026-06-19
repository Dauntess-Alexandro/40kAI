import random

import numpy as np
import pytest

from core.engine.phases.windowed_selfplay import (
    run_model_charge_from_action,
    run_model_command_from_action,
    run_model_fight_from_action,
    run_model_movement_from_action,
    run_model_shooting_from_action,
    run_model_turn_from_action,
)
from tests.engine.phases._helpers import build_env


def _engaged_setup(env):
    """Юниты модели в дальности стрельбы и чарджа от врага."""
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.unit_coords[1] = [11, 11]
    env.enemy_coords[0] = [14, 12]
    env.enemy_coords[1] = [16, 13]
    env.enemyCP = 0
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env._invalidate_target_cache("test")


def _legal_move_num(env, u: int) -> int:
    overlay = env.get_unit_movement_overlay("model", int(u))
    move_cells = list(overlay.get("move_cells") or [])
    return 1 if move_cells else 0


from tests.engine.phases._helpers import build_env, flat_default_action


def _action(env, n: int, *, move_num_override: int | None = None) -> dict:
    a = flat_default_action(n, move=0, attack=1)
    for i in range(n):
        a[f"move_num_{i}"] = move_num_override if move_num_override is not None else _legal_move_num(env, i)
    return a


def _snap(env) -> dict:
    return {
        "unit_coords": [list(c) for c in env.unit_coords],
        "enemy_health": [round(float(h), 2) for h in env.enemy_health],
        "unit_health": [round(float(h), 2) for h in env.unit_health],
        "unit_in_attack": [list(x) for x in env.unitInAttack],
        "enemy_in_attack": [list(x) for x in env.enemyInAttack],
        "model_cp": int(env.modelCP),
    }


def _run_legacy_phase(env, phase: str, action, n):
    if phase == "command":
        env.command_phase("model", action=action)
    elif phase == "movement":
        bs = [False] * n
        env.movement_phase("model", action=action, battle_shock=bs)
    elif phase == "shooting":
        env.shooting_phase("model", advanced_flags=[False] * n, action=action)
    elif phase == "charge":
        env.charge_phase("model", advanced_flags=[False] * n, action=action)
    elif phase == "fight":
        env.fight_phase("model")


def _run_windowed_phase(env, phase: str, action):
    if phase == "command":
        run_model_command_from_action(env, action)
    elif phase == "movement":
        run_model_movement_from_action(env, action)
    elif phase == "shooting":
        run_model_shooting_from_action(env, action)
    elif phase == "charge":
        run_model_charge_from_action(env, action)
    elif phase == "fight":
        run_model_fight_from_action(env, action)


@pytest.mark.parametrize("move_num_override", [None, 999], ids=["legal", "out_of_range"])
@pytest.mark.parametrize("phase", ["command", "movement", "shooting", "charge", "fight"])
def test_parity_per_phase(monkeypatch, phase, move_num_override):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _engaged_setup(env)
    n = len(env.unit_health)
    action = _action(env, n, move_num_override=move_num_override)
    snap = env.snapshot_state()

    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        _run_legacy_phase(env, phase, action, n)
        legacy = _snap(env)
    env.restore_state(snap)

    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        _run_windowed_phase(env, phase, action)
        windowed = _snap(env)
    env.restore_state(snap)

    assert legacy == windowed, f"расхождение в фазе {phase}: legacy != windowed"


@pytest.mark.parametrize("move_num_override", [None, 999], ids=["legal", "out_of_range"])
def test_parity_full_turn(monkeypatch, move_num_override):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _engaged_setup(env)
    n = len(env.unit_health)
    action = _action(env, n, move_num_override=move_num_override)
    snap = env.snapshot_state()

    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        bs, _ = env.command_phase("model", action=action)
        advanced_flags, _, _ = env.movement_phase("model", action=action, battle_shock=bs)
        env.shooting_phase("model", advanced_flags=advanced_flags, action=action)
        env.charge_phase("model", advanced_flags=advanced_flags, action=action)
        env.fight_phase("model")
        legacy = _snap(env)
    env.restore_state(snap)

    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        run_model_turn_from_action(env, action)
        windowed = _snap(env)
    env.restore_state(snap)

    assert legacy == windowed


def test_movement_out_of_range_is_logged(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _engaged_setup(env)
    n = len(env.unit_health)
    action = _action(env, n, move_num_override=999)

    captured: list[str] = []
    monkeypatch.setattr(env, "_log", lambda msg: captured.append(str(msg)))

    with env.simulation_mode():
        run_model_movement_from_action(env, action)

    assert any("move_num" in m and "вне диапазона reachable" in m for m in captured), (
        "out-of-range move_num должен быть объяснён в логе (не тихий пропуск)"
    )
