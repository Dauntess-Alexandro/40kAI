from core.engine.phases.option_generator import _unwrap, command_reroll_options_for_unit
from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env


def _eu_with_cp(cp=5):
    env = build_env()
    eu = _unwrap(env)
    eu.modelCP = cp
    eu.enemyCP = cp
    return env, eu


def test_reroll_gated_when_no_shoot_target(monkeypatch):
    env, eu = _eu_with_cp()
    monkeypatch.setattr(eu, "get_shoot_targets_for_unit", lambda side, idx: [])
    assert command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound")) == []


def test_reroll_offered_when_has_shoot_target(monkeypatch):
    env, eu = _eu_with_cp()
    monkeypatch.setattr(eu, "get_shoot_targets_for_unit", lambda side, idx: [1])
    opts = command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound"))
    assert len(opts) == 2  # hit + wound


def test_reroll_gated_when_no_charge_target(monkeypatch):
    env, eu = _eu_with_cp()
    monkeypatch.setattr(eu, "get_charge_targets_for_unit", lambda side, idx: [])
    assert command_reroll_options_for_unit(env, "model", 0, phase=Phase.CHARGE, rolls=("charge",)) == []


def test_reroll_offered_when_has_charge_target(monkeypatch):
    env, eu = _eu_with_cp()
    monkeypatch.setattr(eu, "get_charge_targets_for_unit", lambda side, idx: [2])
    opts = command_reroll_options_for_unit(env, "model", 0, phase=Phase.CHARGE, rolls=("charge",))
    assert len(opts) == 1


def test_cp_gate_still_blocks_even_with_target(monkeypatch):
    env, eu = _eu_with_cp(cp=0)
    monkeypatch.setattr(eu, "get_shoot_targets_for_unit", lambda side, idx: [1])
    assert command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound")) == []


def test_movement_advance_option_not_offered():
    """Подзадача 3.3A: command_reroll:advance — нелегальная опция в movement-окне.

    advance не имеет pass/fail-критерия, поэтому option_generator не должен
    предлагать его даже при CP и живом юните (action-контракт не меняется).
    """
    env, eu = _eu_with_cp(cp=5)
    assert command_reroll_options_for_unit(env, "model", 0, phase=Phase.MOVEMENT, rolls=("advance",)) == []
