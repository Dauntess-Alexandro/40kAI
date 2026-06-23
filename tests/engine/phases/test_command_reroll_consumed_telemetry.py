"""Телеметрия command_reroll: fired (consumed=True) vs wasted (стёрт без consumed)."""
import pytest

from core.engine.phases import stratagem_engine
from tests.engine.phases._helpers import build_env


def _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound"):
    """Создаёт запись command_reroll в active_stratagem_effects (как stratagem_engine.apply)."""
    env.active_stratagem_effects.append(
        {
            "effect_id": "command_reroll",
            "consumed": False,
            "phase": phase,
            "side": side,
            "unit_idx": unit_idx,
            "reroll_roll": reroll_roll,
            "round": int(env.battle_round),
        }
    )


class TestFiredCountedOnConsume:
    """fired инкрементируется при consumed=True (через _consume_command_reroll_record)."""

    def test_fired_counted_on_consume(self):
        env = build_env()
        assert env._cmd_reroll_fired == 0
        assert env._cmd_reroll_wasted == 0

        _make_reroll_record(env, side="model", unit_idx=0, phase="charge", reroll_roll="charge")
        rec = env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert rec is not None
        assert rec["consumed"] is True
        assert env._cmd_reroll_fired == 1
        assert env._cmd_reroll_wasted == 0

    def test_fired_in_attack_stratagem_effects(self):
        """fired через _stratagem_effects_for_attacker (hit/wound reroll в attack)."""
        env = build_env()
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound")

        eff = env._stratagem_effects_for_attacker("model", 0, "fight")
        assert eff is not None
        assert env._cmd_reroll_fired == 1
        assert env._cmd_reroll_wasted == 0

    def test_fired_in_build_reroll_decider(self):
        """fired через _build_reroll_decider (save/hit/wound decider в attack)."""
        env = build_env()
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("hit", 3, 4)

        assert result is True
        assert env._cmd_reroll_fired == 1
        assert env._cmd_reroll_wasted == 0


class TestWastedCountedOnPhaseClear:
    """wasted инкрементируется при _clear_phase_stratagem_effects для consumed=False."""

    def test_wasted_counted_on_phase_clear(self):
        env = build_env()
        _make_reroll_record(env, side="model", unit_idx=0, phase="shooting")

        env._clear_phase_stratagem_effects("shooting")

        assert env._cmd_reroll_wasted == 1
        assert env._cmd_reroll_fired == 0

    def test_consumed_record_not_counted_as_wasted(self):
        """Уже consumed запись НЕ считается wasted при очистке."""
        env = build_env()
        _make_reroll_record(env, side="model", unit_idx=0, phase="shooting")
        # Пометить consumed вручную
        env.active_stratagem_effects[0]["consumed"] = True

        env._clear_phase_stratagem_effects("shooting")

        assert env._cmd_reroll_wasted == 0

    def test_multiple_wasted_counted(self):
        """Несколько неиспользованных записей за одну фазу."""
        env = build_env()
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")
        _make_reroll_record(env, side="model", unit_idx=1, phase="fight", reroll_roll="wound")

        env._clear_phase_stratagem_effects("fight")

        assert env._cmd_reroll_wasted == 2


class TestSimulationModeDoesNotCount:
    """Внутри simulation_mode() счётчики НЕ инкрементируются."""

    def test_simulation_mode_does_not_count_fired(self):
        env = build_env()
        with env.simulation_mode():
            _make_reroll_record(env, side="model", unit_idx=0, phase="charge", reroll_roll="charge")
            env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert env._cmd_reroll_fired == 0

    def test_simulation_mode_does_not_count_wasted(self):
        env = build_env()
        with env.simulation_mode():
            _make_reroll_record(env, side="model", unit_idx=0, phase="shooting")
            env._clear_phase_stratagem_effects("shooting")

        assert env._cmd_reroll_wasted == 0

    def test_simulation_mode_does_not_count_attack_effects(self):
        env = build_env()
        with env.simulation_mode():
            _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound")
            env._stratagem_effects_for_attacker("model", 0, "fight")

        assert env._cmd_reroll_fired == 0

    def test_simulation_mode_does_not_count_decider(self):
        env = build_env()
        with env.simulation_mode():
            _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")
            decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
            decider("hit", 3, 4)

        assert env._cmd_reroll_fired == 0


class TestResetZeroesCounters:
    """reset() обнуляет оба счётчика."""

    def test_reset_zeroes_counters(self):
        env = build_env()
        env._cmd_reroll_fired = 5
        env._cmd_reroll_wasted = 3

        env.reset()

        assert env._cmd_reroll_fired == 0
        assert env._cmd_reroll_wasted == 0
