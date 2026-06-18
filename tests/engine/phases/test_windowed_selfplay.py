import pytest

from core.engine.phases.option_generator import command_window
from core.engine.phases.types import ActionKind
from core.engine.phases.windowed_selfplay import (
    make_command_decide_from_action_dict,
    merge_command_meta_into,
    run_model_command_from_action,
    windowed_selfplay_enabled,
)
from tests.engine.phases._helpers import build_env
from tests.engine.phases.test_phase_engine_command import _action, _setup_failing_unit0


def test_windowed_selfplay_disabled_by_default(monkeypatch):
    monkeypatch.delenv("WINDOWED_SELFPLAY", raising=False)
    assert windowed_selfplay_enabled() is False


def test_windowed_selfplay_enabled_from_env(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    assert windowed_selfplay_enabled() is True


def test_command_decide_maps_use_cp_to_stratagem():
    env = build_env()
    env.modelCP = 2
    win = command_window(env, "model")
    decide = make_command_decide_from_action_dict(_action(1, 0, len(env.unit_health)))
    opt = decide(win)
    assert opt.kind is ActionKind.USE_STRATAGEM
    assert opt.unit_idx == 0
    assert opt.meta["stratagem_id"] == "insane_bravery"


def test_command_decide_pass_when_no_bravery():
    env = build_env()
    win = command_window(env, "model")
    decide = make_command_decide_from_action_dict(_action(0, 0, len(env.unit_health)))
    opt = decide(win)
    assert opt.kind is ActionKind.PASS


def test_run_model_command_equivalent_to_command_phase_action():
    env = build_env()
    _setup_failing_unit0(env)
    n = len(env.unit_health)
    action = _action(1, 0, n)
    snap = env.snapshot_state()

    with env.simulation_mode():
        bs_a, r_a = env.command_phase("model", action=action)
        cp_a = env.modelCP
        used_a = list(env.stratagem_used)
    env.restore_state(snap)

    with env.simulation_mode():
        st = run_model_command_from_action(env, action)
        bs_b = st.battle_shock
        r_b = float(st.info.get("command_reward_delta", 0.0))
        cp_b = env.modelCP
        used_b = list(env.stratagem_used)
    env.restore_state(snap)

    assert bs_a == bs_b
    assert r_a == r_b
    assert cp_a == cp_b
    assert used_a == used_b


def test_command_replay_meta_when_windowed(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _setup_failing_unit0(env)
    action = _action(1, 0, len(env.unit_health))
    meta = merge_command_meta_into(None, env, action, cp_before=2)
    assert meta is not None
    assert meta.window_id == "command:model"
    assert meta.stratagem_id == "insane_bravery"
    assert meta.sub_step == "battle_shock"


def test_merge_command_meta_noop_when_disabled(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "0")
    env = build_env()
    out = merge_command_meta_into(None, env, _action(1, 0, 2), cp_before=1)
    assert out is None
