from core.engine.phases.stratagems import (
    STRATAGEM_PHASES,
    stratagem_action_choices,
    stratagem_choice_index,
    stratagem_choice_str,
)
from core.engine.phases.types import Phase


def test_phases_set():
    assert STRATAGEM_PHASES == (Phase.COMMAND, Phase.MOVEMENT, Phase.SHOOTING, Phase.CHARGE, Phase.FIGHT)


def test_choices_index0_is_none_all_phases():
    for ph in STRATAGEM_PHASES:
        assert stratagem_action_choices(ph)[0] == "none"


def test_fight_choices_have_command_reroll_subtypes_and_hungry_void():
    ch = stratagem_action_choices(Phase.FIGHT)
    assert "command_reroll:hit" in ch
    assert "command_reroll:wound" in ch
    assert "hungry_void" in ch
    assert "command_reroll" not in ch  # только подтипы, не голый id


def test_shooting_choices_command_reroll_subtypes_no_reactions():
    ch = stratagem_action_choices(Phase.SHOOTING)
    assert "command_reroll:hit" in ch and "command_reroll:wound" in ch
    # реакции (REACTION-timing) исключены
    assert "go_to_ground" not in ch
    assert "smokescreen" not in ch


def test_charge_and_movement_subtypes():
    assert "command_reroll:charge" in stratagem_action_choices(Phase.CHARGE)
    assert "command_reroll:advance" in stratagem_action_choices(Phase.MOVEMENT)
    # heroic_intervention/overwatch (REACTION) исключены
    assert "heroic_intervention" not in stratagem_action_choices(Phase.CHARGE)
    assert "overwatch" not in stratagem_action_choices(Phase.MOVEMENT)


def test_command_has_insane_bravery():
    ch = stratagem_action_choices(Phase.COMMAND)
    assert "insane_bravery" in ch


def test_index_str_roundtrip():
    for ph in STRATAGEM_PHASES:
        for i, s in enumerate(stratagem_action_choices(ph)):
            assert stratagem_choice_index(ph, s) == i
            assert stratagem_choice_str(ph, i) == s
    assert stratagem_choice_str(Phase.FIGHT, 999) == "none"
