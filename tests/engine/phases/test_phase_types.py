from core.engine.phases.types import (
    ActionKind,
    ActionOption,
    DecisionWindow,
    Phase,
    PhaseResult,
    PhaseState,
    PhaseTurnState,
    SubStep,
    Timing,
)


def test_enums_have_expected_values():
    assert Phase.MOVEMENT.value == "movement"
    assert SubStep.PICK_SHOOT_TARGET.value == "pick_shoot_target"
    assert Timing.REACTION.value == "reaction"
    assert ActionKind.USE_STRATAGEM.value == "use_stratagem"


def test_action_option_defaults_are_independent():
    a = ActionOption(kind=ActionKind.MOVE, unit_idx=0)
    b = ActionOption(kind=ActionKind.SHOOT, unit_idx=1)
    a.param["x"] = 1
    a.legacy_patch["move_num_0"] = 3
    assert b.param == {}
    assert b.legacy_patch == {}
    assert a.target_idx is None
    assert a.meta == {}


def test_decision_window_holds_options():
    opt = ActionOption(kind=ActionKind.PASS)
    win = DecisionWindow(
        window_id="movement:model:0",
        owner_side="model",
        phase=Phase.MOVEMENT,
        sub_step=SubStep.MOVE_UNIT,
        timing=Timing.MAIN,
        cursor_unit_idx=0,
        options=[opt],
    )
    assert win.options[0].kind is ActionKind.PASS
    assert win.context == {}


def test_phase_state_and_result_defaults():
    st = PhaseState(
        battle_round=1,
        active_side="model",
        phase=Phase.COMMAND,
        sub_step=SubStep.BATTLE_SHOCK,
        timing=Timing.MAIN,
    )
    assert st.cursor_unit_idx is None
    res = PhaseResult()
    assert res.reward_delta == 0.0
    assert res.next_window is None
    assert res.done is False
    assert res.events == [] and res.info_patch == {}


def test_phase_turn_state_defaults_are_independent():
    a = PhaseTurnState(side="model")
    b = PhaseTurnState(side="enemy")
    a.battle_shock.append(True)
    a.advanced_flags.append(True)
    a.info["phase"] = "movement"
    assert b.battle_shock == []
    assert b.advanced_flags == []
    assert b.info == {}
