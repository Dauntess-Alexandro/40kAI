from core.engine.phases.stratagems import stratagem_action_choices
from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env, flat_default_action


def _bravery_idx():
    return stratagem_action_choices(Phase.COMMAND).index("insane_bravery")


def _action_bravery(n: int, unit: int = 0) -> dict:
    """Action с strat_command=insane_bravery, нацеленный на юнит `unit`."""
    a = flat_default_action(n)
    a["strat_command"] = _bravery_idx()
    a["strat_command_unit"] = unit
    return a


def _action_no_bravery(n: int) -> dict:
    """Action без bravery (strat_command=0 → none)."""
    return flat_default_action(n)


def test_command_bravery_routed_through_engine_records_journal():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.unit_health)

    # Юнит 0 ниже половины состава + невозможный Ld(13): 2D6<=12 → battle-shock всегда провален.
    env.unit_data[0]["Ld"] = 13
    env.unit_health[0] = 1.0
    env.modelCP = 2
    start_cp = env.modelCP

    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            battle_shock, _reward = env.command_phase("model", action=_action_bravery(n, unit=0))
            # Bravery спасла юнит 0
            assert battle_shock[0] is False
            # запись в журнале появилась
            assert ("model", "insane_bravery", env.battle_round, "command", 0) in env.stratagem_used
            # нетто CP: +1 (командование) -1 (bravery) = без изменений
            assert env.modelCP == start_cp
        finally:
            env.restore_state(snap)

    # restore вернул журнал и CP
    assert env.stratagem_used == []
    assert env.modelCP == start_cp


def test_command_no_bravery_when_not_requested():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.unit_health)
    env.unit_data[0]["Ld"] = 13
    env.unit_health[0] = 1.0
    env.modelCP = 2

    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            battle_shock, _reward = env.command_phase("model", action=_action_no_bravery(n))
            # Bravery не запрошена → юнит 0 в battle-shock, журнал пуст
            assert battle_shock[0] is True
            assert env.stratagem_used == []
        finally:
            env.restore_state(snap)
