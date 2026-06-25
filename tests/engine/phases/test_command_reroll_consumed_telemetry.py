"""Телеметрия command_reroll: fired (consumed=True) — wasted считается арифметикой applied−fired.

Подзадача 3.1: legacy pay-on-apply — CP списывается на consume (через _charge_cp), не на arm.
"""
from tests.engine.phases._helpers import build_env


def _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound"):
    """Создаёт запись command_reroll в active_stratagem_effects (как stratagem_engine.apply).

    paid=False — armed, не оплачен (новые записи от apply после подзадачи 2.1).
    """
    env.active_stratagem_effects.append(
        {
            "effect_id": "command_reroll",
            "consumed": False,
            "paid": False,
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
        env.modelCP = 1  # CP для legacy pay-on-apply на consume
        assert env._cmd_reroll_fired == 0

        _make_reroll_record(env, side="model", unit_idx=0, phase="charge", reroll_roll="charge")
        rec = env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert rec is not None
        assert rec["consumed"] is True
        assert env._cmd_reroll_fired == 1

    def test_fired_not_in_attack_stratagem_effects(self):
        """Подзадача 3.2: command_reroll hit/wound НЕ идёт через _stratagem_effects_for_attacker.
        fired не инкрементируется на setup — только через _build_reroll_decider при failed die."""
        env = build_env()
        env.modelCP = 1
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound")

        eff = env._stratagem_effects_for_attacker("model", 0, "fight")
        assert eff is None  # command_reroll пропущен (идёт через decider)
        assert env._cmd_reroll_fired == 0  # fired не вырос на setup

    def test_fired_in_build_reroll_decider(self):
        """fired через _build_reroll_decider (save/hit/wound decider в attack)."""
        env = build_env()
        env.modelCP = 1  # CP для legacy pay-on-apply на consume
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("hit", 3, 4)

        assert result is True
        assert env._cmd_reroll_fired == 1


class TestSimulationModeDoesNotCount:
    """Внутри simulation_mode() счётчик fired НЕ инкрементируется.

    CP под симуляцией списывается (откатывается snapshot/restore вызывающим кодом),
    но _cmd_reroll_fired не инкрементируется.
    """

    def test_simulation_mode_does_not_count_fired(self):
        env = build_env()
        env.modelCP = 1  # CP списывается под сим, fired — нет
        with env.simulation_mode():
            _make_reroll_record(env, side="model", unit_idx=0, phase="charge", reroll_roll="charge")
            env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert env._cmd_reroll_fired == 0

    def test_simulation_mode_does_not_count_attack_effects(self):
        """Подзадача 3.2: command_reroll не проходит через _stratagem_effects_for_attacker,
        поэтому fired не растёт ни в sim, ни вне sim (consume только через decider)."""
        env = build_env()
        env.modelCP = 1
        with env.simulation_mode():
            _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound")
            env._stratagem_effects_for_attacker("model", 0, "fight")

        assert env._cmd_reroll_fired == 0

    def test_simulation_mode_does_not_count_decider(self):
        env = build_env()
        env.modelCP = 1
        with env.simulation_mode():
            _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")
            decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
            decider("hit", 3, 4)

        assert env._cmd_reroll_fired == 0


class TestResetZeroesCounters:
    """reset() обнуляет fired."""

    def test_reset_zeroes_fired(self):
        env = build_env()
        env._cmd_reroll_fired = 5

        env.reset()

        assert env._cmd_reroll_fired == 0


# ---------------------------------------------------------------------------
# Подзадача 3.1: legacy pay-on-apply (CP списывается на consume, не на arm).
# ---------------------------------------------------------------------------


class TestLegacyPayOnApplyConsume:
    """_consume_command_reroll_record: CP списывается на consume через _charge_cp."""

    def test_consume_charges_cp_when_paid(self):
        """CP=1, rec paid=False → consume: rec returned, CP=0, paid=True, consumed=True, fired=1."""
        env = build_env()
        env.modelCP = 1
        _make_reroll_record(env, side="model", unit_idx=0, phase="charge", reroll_roll="charge")

        rec = env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert rec is not None
        assert rec["consumed"] is True
        assert rec["paid"] is True
        assert env.modelCP == 0
        assert env._cmd_reroll_fired == 1

    def test_consume_no_cp_does_not_reroll(self):
        """CP=0, rec paid=False → returns None, CP=0, paid=False, consumed=False, fired unchanged."""
        env = build_env()
        env.modelCP = 0
        fired_before = env._cmd_reroll_fired
        _make_reroll_record(env, side="model", unit_idx=0, phase="charge", reroll_roll="charge")

        rec = env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert rec is None
        assert env.modelCP == 0  # не ушёл в минус
        assert env._cmd_reroll_fired == fired_before
        # rec не изменён (не consumed, не paid)
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["consumed"] is False
        assert rr["paid"] is False


class TestAttackEffectsSkipsCommandReroll:
    """Подзадача 3.2: _stratagem_effects_for_attacker НЕ обрабатывает command_reroll hit/wound.
    CP не списывается, rec не consumed/paid, fired не растёт — reroll идёт через decider."""

    def test_attack_effects_skips_command_reroll_with_cp(self):
        """CP=1, rec paid=False, wound → None, CP=1, paid+consumed False, fired unchanged."""
        env = build_env()
        env.modelCP = 1
        fired_before = env._cmd_reroll_fired
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound")

        eff = env._stratagem_effects_for_attacker("model", 0, "fight")

        assert eff is None
        assert env.modelCP == 1  # CP не списан на setup
        assert env._cmd_reroll_fired == fired_before
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["paid"] is False
        assert rr["consumed"] is False

    def test_attack_effects_skips_command_reroll_no_cp(self):
        """CP=0 → None, no consumed/fired (как и при CP>0 — setup не трогает command_reroll)."""
        env = build_env()
        env.modelCP = 0
        fired_before = env._cmd_reroll_fired
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="wound")

        eff = env._stratagem_effects_for_attacker("model", 0, "fight")

        assert eff is None
        assert env.modelCP == 0
        assert env._cmd_reroll_fired == fired_before
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["consumed"] is False
        assert rr["paid"] is False


class TestLegacyPayOnApplyDecider:
    """_build_reroll_decider: CP списывается на consume (save/hit/wound/damage/attacks)."""

    def test_decider_save_charges_enemy_cp_when_paid(self):
        """enemyCP=1, defender rec paid=False, save → True, enemyCP=0, paid+consumed True, fired+1."""
        env = build_env()
        env.enemyCP = 1
        _make_reroll_record(env, side="enemy", unit_idx=0, phase="fight", reroll_roll="save")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("save", 2, 4)

        assert result is True
        assert env.enemyCP == 0
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["paid"] is True
        assert rr["consumed"] is True
        assert env._cmd_reroll_fired == 1

    def test_decider_save_no_enemy_cp_returns_false(self):
        """enemyCP=0 → False, no consumed/fired."""
        env = build_env()
        env.enemyCP = 0
        fired_before = env._cmd_reroll_fired
        _make_reroll_record(env, side="enemy", unit_idx=0, phase="fight", reroll_roll="save")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("save", 2, 4)

        assert result is False
        assert env.enemyCP == 0
        assert env._cmd_reroll_fired == fired_before
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["consumed"] is False
        assert rr["paid"] is False

    def test_decider_save_no_fail_returns_false(self):
        """Подзадача 3.2: save без failed die (6 >= 4) → False, CP/consume/fired без мутаций."""
        import numpy as np

        env = build_env()
        env.enemyCP = 1
        fired_before = env._cmd_reroll_fired
        _make_reroll_record(env, side="enemy", unit_idx=0, phase="fight", reroll_roll="save")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("save", np.array([6]), 4)

        assert result is False
        assert env.enemyCP == 1  # CP не списан — нет failed die
        assert env._cmd_reroll_fired == fired_before
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["consumed"] is False
        assert rr["paid"] is False


class TestDeciderFailedDieGate:
    """Подзадача 3.2: оплата/consume command_reroll только при actual eligible failed die.
    decider(stage, dice, threshold): failed die = int(d) < int(threshold)."""

    def test_decider_hit_no_fail_returns_false(self):
        """hit, dice=[6], threshold=3 → нет failed die → False, CP=1, rec not paid/consumed, fired unchanged."""
        import numpy as np

        env = build_env()
        env.modelCP = 1
        fired_before = env._cmd_reroll_fired
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("hit", np.array([6]), 3)

        assert result is False
        assert env.modelCP == 1
        assert env._cmd_reroll_fired == fired_before
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["paid"] is False
        assert rr["consumed"] is False

    def test_decider_hit_failed_returns_true_and_charges(self):
        """hit, dice=[2], threshold=4 → failed die → True, CP=0, paid+consumed True, fired+1."""
        import numpy as np

        env = build_env()
        env.modelCP = 1
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("hit", np.array([2]), 4)

        assert result is True
        assert env.modelCP == 0
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["paid"] is True
        assert rr["consumed"] is True
        assert env._cmd_reroll_fired == 1

    def test_decider_hit_failed_no_cp_returns_false(self):
        """hit, dice=[2], threshold=4, CP=0 → failed die, но CP нет → False, CP=0, rec not paid/consumed."""
        import numpy as np

        env = build_env()
        env.modelCP = 0
        fired_before = env._cmd_reroll_fired
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")

        decider = env._build_reroll_decider("model", 0, "enemy", 0, phase="fight")
        result = decider("hit", np.array([2]), 4)

        assert result is False
        assert env.modelCP == 0  # не ушёл в минус
        assert env._cmd_reroll_fired == fired_before
        rr = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"][0]
        assert rr["paid"] is False
        assert rr["consumed"] is False


class TestBackwardCompatPaidFlag:
    """Backward compatibility: rec без поля paid или paid=True не требует списания."""

    def test_rec_paid_true_does_not_charge(self):
        """rec paid=True (уже оплачен) → consume без повторного списания CP."""
        env = build_env()
        env.modelCP = 1
        env.active_stratagem_effects.append(
            {
                "effect_id": "command_reroll",
                "consumed": False,
                "paid": True,  # уже оплачен
                "phase": "charge",
                "side": "model",
                "unit_idx": 0,
                "reroll_roll": "charge",
                "round": int(env.battle_round),
            }
        )

        rec = env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert rec is not None
        assert rec["consumed"] is True
        assert env.modelCP == 1  # CP не списан повторно
        assert env._cmd_reroll_fired == 1

    def test_rec_without_paid_field_does_not_charge(self):
        """rec без поля paid (старая запись, CP списан на arm) → consume без списания."""
        env = build_env()
        env.modelCP = 1
        env.active_stratagem_effects.append(
            {
                "effect_id": "command_reroll",
                "consumed": False,
                # поле paid отсутствует (legacy-запись до подзадачи 2.1)
                "phase": "charge",
                "side": "model",
                "unit_idx": 0,
                "reroll_roll": "charge",
                "round": int(env.battle_round),
            }
        )

        rec = env._consume_command_reroll_record("model", 0, "charge", "charge")

        assert rec is not None
        assert rec["consumed"] is True
        assert env.modelCP == 1  # CP не списан (legacy-запись уже оплачена на arm)
        assert env._cmd_reroll_fired == 1


class TestEndOfPhaseCleanup:
    """End-of-phase cleanup удаляет armed-not-fired без списания CP."""

    def test_clear_phase_removes_armed_not_fired_without_cp_loss(self):
        env = build_env()
        env.modelCP = 1
        _make_reroll_record(env, side="model", unit_idx=0, phase="fight", reroll_roll="hit")
        env.active_stratagem_effects.append(
            {
                "effect_id": "command_reroll",
                "consumed": False,
                "paid": False,
                "phase": "shooting",
                "side": "model",
                "unit_idx": 0,
                "reroll_roll": "hit",
                "round": int(env.battle_round),
            }
        )

        env._clear_phase_stratagem_effects("fight")

        assert env.modelCP == 1
        assert all(str(rec.get("phase")) != "fight" for rec in env.active_stratagem_effects)
        assert any(str(rec.get("phase")) == "shooting" for rec in env.active_stratagem_effects)
