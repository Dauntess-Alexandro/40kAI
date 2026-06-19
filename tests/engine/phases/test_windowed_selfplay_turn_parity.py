import random

import numpy as np
import pytest

from core.engine.phases.windowed_selfplay import run_model_turn_from_action
from tests.engine.phases._helpers import build_env, flat_default_action


def _action(n: int) -> dict:
    return flat_default_action(n)


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.unit_coords[1] = [8, 8]
    env.enemy_coords[0] = [14, 10]
    env.enemy_coords[1] = [29, 29]
    env.enemyCP = 0
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env._invalidate_target_cache("test")


def _snapshot_metrics(env):
    return {
        "unit_coords": [list(c) for c in env.unit_coords],
        "enemy_health": [round(float(h), 2) for h in env.enemy_health],
        "unit_health": [round(float(h), 2) for h in env.unit_health],
        "unit_in_attack": [list(x) for x in env.unitInAttack],
        "model_cp": int(env.modelCP),
    }


def test_windowed_turn_matches_legacy_phases(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _setup(env)
    n = len(env.unit_health)
    action = _action(n)
    snap = env.snapshot_state()

    random.seed(42)
    np.random.seed(42)
    with env.simulation_mode():
        bs, _ = env.command_phase("model", action=action)
        env.movement_phase("model", action=action, battle_shock=bs)
        env.shooting_phase("model", advanced_flags=[False] * n, action=action)
        env.charge_phase("model", advanced_flags=[False] * n, action=action)
        env.fight_phase("model")
        legacy = _snapshot_metrics(env)
    env.restore_state(snap)

    random.seed(42)
    np.random.seed(42)
    with env.simulation_mode():
        run_model_turn_from_action(env, action)
        windowed = _snapshot_metrics(env)
    env.restore_state(snap)

    assert legacy == windowed


@pytest.mark.parametrize("windowed_flag", ["0", "1"])
def test_step_legacy_path_unchanged_when_flag_off(monkeypatch, windowed_flag):
    monkeypatch.setenv("WINDOWED_SELFPLAY", windowed_flag)
    env = build_env()
    _setup(env)
    action = _action(len(env.unit_health))
    snap = env.snapshot_state()

    random.seed(99)
    np.random.seed(99)
    with env.simulation_mode():
        env.step(action)
        metrics_a = _snapshot_metrics(env)
    env.restore_state(snap)

    random.seed(99)
    np.random.seed(99)
    with env.simulation_mode():
        env.step(action)
        metrics_b = _snapshot_metrics(env)
    env.restore_state(snap)

    assert metrics_a == metrics_b
