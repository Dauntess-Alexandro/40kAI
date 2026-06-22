from core.engine.utils import attack
from tests.engine.test_attack_effects import StubRoller, _ATT_DATA, _ranged_weapon


def test_reroll_decider_rerolls_worst_failed_wound():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    calls = []

    def decider(stage, dice, threshold):
        calls.append(stage)
        return stage == "wound"

    dmg, _ = attack(
        1,
        weapon,
        _ATT_DATA,
        10,
        defender,
        roller=StubRoller(hit=[5, 5], wound=[2, 3, 6]),
        reroll_decider=decider,
    )
    assert "wound" in calls
    assert float(sum(dmg)) == 1.0


def test_die_not_rerolled_twice_effect_then_decider():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}

    def decider(stage, dice, threshold):
        return True

    dmg, _ = attack(
        1,
        weapon,
        _ATT_DATA,
        10,
        defender,
        effects={"reroll_wounds": "one"},
        roller=StubRoller(hit=[5, 5], wound=[2, 3, 5, 6]),
        reroll_decider=decider,
    )
    assert float(sum(dmg)) == 2.0


def test_save_die_not_rerolled_twice_effect_then_decider():
    weapon = _ranged_weapon(S=4, Attacks=2, Damage="D6")
    defender = {"Sv": 4, "T": 4, "IVSave": 0}

    def decider(stage, dice, threshold):
        return stage == "save"

    dmg, _ = attack(
        1,
        weapon,
        _ATT_DATA,
        10,
        defender,
        effects={"reroll_save": "all"},
        roller=StubRoller(hit=[5, 5], wound=[6, 6], save=[2, 3, 1, 3, 6], damage=[5, 1]),
        reroll_decider=decider,
    )
    assert float(sum(dmg)) == 6.0
