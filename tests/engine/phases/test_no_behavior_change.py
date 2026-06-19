import random

import numpy as np

from core.engine.phases import compile_options_to_action_dict, default_action_dict
from tests.engine.phases._helpers import build_env, run_windowed_default_turn


def _state_tuple(env):
    return (
        list(env.unit_health),
        list(env.enemy_health),
        int(env.modelCP),
        int(env.enemyCP),
        int(env.modelVP),
        int(env.enemyVP),
        [list(c) for c in env.unit_coords],
        [list(c) for c in env.enemy_coords],
    )


def _extended_state_tuple(env):
    return _state_tuple(env) + (
        [list(x) for x in env.unitInAttack],
        [list(x) for x in env.enemyInAttack],
        list(env.model_used_advance),
        list(env.enemy_used_advance),
        list(env.unitFellBack),
        list(env.enemyFellBack),
        list(env.stratagem_used),
    )


def test_compiled_default_equals_manual_default_step():
    """Скомпилированный нейтральный ход == рукописный дефолт: идентичная траектория step.

    Оба прогона стартуют из одного snapshot (тот же rng), поэтому исход детерминирован.
    Доказывает: компилятор отдаёт валидный для env.step action и не меняет поведение.
    """
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.unit_health)

    manual = default_action_dict(n)
    compiled = compile_options_to_action_dict([], len_model=n)
    assert compiled == manual

    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            _, r_m, done_m, res_m, _ = env.step(dict(manual))
            state_m = _state_tuple(env)
        finally:
            env.restore_state(snap)

    with env.simulation_mode():
        try:
            _, r_c, done_c, res_c, _ = env.step(dict(compiled))
            state_c = _state_tuple(env)
        finally:
            env.restore_state(snap)

    assert state_m == state_c
    assert float(r_m) == float(r_c)
    assert bool(done_m) == bool(done_c)
    assert int(res_m) == int(res_c)


def test_default_action_dict_matches_action_contract_keys():
    from core.models.action_contract import ordered_action_keys

    d = default_action_dict(2)
    assert set(d.keys()) == set(ordered_action_keys(2))


def test_windowed_default_turn_matches_legacy_default_step_state():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.unit_health)
    action = compile_options_to_action_dict([], len_model=n)
    snap = env.snapshot_state()

    random.seed(123)
    np.random.seed(123)
    with env.simulation_mode():
        env.step(dict(action))
        legacy_state = _extended_state_tuple(env)
    env.restore_state(snap)

    random.seed(123)
    np.random.seed(123)
    with env.simulation_mode():
        run_windowed_default_turn(env, "model")
        windowed_state = _extended_state_tuple(env)
    env.restore_state(snap)

    assert windowed_state == legacy_state
