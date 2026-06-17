import random

import numpy as np

from core.engine.phases import phase_engine
from core.engine.phases.types import ActionKind, Phase, PhaseTurnState
from tests.engine.phases._helpers import _default_window_decide, build_env


def _extended_state(env):
    return (
        list(env.unit_health),
        list(env.enemy_health),
        int(env.modelCP),
        int(env.enemyCP),
        int(env.modelVP),
        int(env.enemyVP),
        [list(c) for c in env.unit_coords],
        [list(c) for c in env.enemy_coords],
        [list(x) for x in env.unitInAttack],
        [list(x) for x in env.enemyInAttack],
        list(env.stratagem_used),
    )


def _legacy_default_action(n):
    a = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0}
    for i in range(n):
        a[f"move_num_{i}"] = 0
    return a


def test_run_turn_default_matches_legacy_step():
    """run_turn с legacy-дефолтными выборами == env.step по итоговому состоянию (фикс. seed)."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.unit_health)
    snap = env.snapshot_state()

    random.seed(123)
    np.random.seed(123)
    with env.simulation_mode():
        env.step(_legacy_default_action(n))
        legacy = _extended_state(env)
    env.restore_state(snap)

    random.seed(123)
    np.random.seed(123)
    with env.simulation_mode():
        phase_engine.run_turn(env, "model", _default_window_decide)
        windowed = _extended_state(env)
    env.restore_state(snap)

    assert windowed == legacy


def test_run_turn_returns_phase_turn_state():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    with env.simulation_mode():
        state = phase_engine.run_turn(env, "model", _default_window_decide)
    assert isinstance(state, PhaseTurnState)
    assert state.side == "model"


def test_run_turn_command_stratagem_decision_flows():
    """run_turn с decide, выбирающим Bravery в command-окне → запись в журнал."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_data[0]["Ld"] = 13
    env.unit_health[0] = 1.0
    env.modelCP = 2

    def decide(window):
        if window.phase is Phase.COMMAND:
            for o in window.options:
                if o.kind is ActionKind.USE_STRATAGEM and o.unit_idx == 0:
                    return o
        return _default_window_decide(window)

    with env.simulation_mode():
        phase_engine.run_turn(env, "model", decide)
    assert any(rec[1] == "insane_bravery" for rec in env.stratagem_used)
