from tests.engine.phases._helpers import build_env, flat_default_action


def _action(use_cp: int, cp_on: int, n: int) -> dict:
    return flat_default_action(n, use_cp=int(use_cp), cp_on=int(cp_on))


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
            battle_shock, _reward = env.command_phase("model", action=_action(1, 0, n))
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
            battle_shock, _reward = env.command_phase("model", action=_action(0, 0, n))
            # Bravery не запрошена → юнит 0 в battle-shock, журнал пуст
            assert battle_shock[0] is True
            assert env.stratagem_used == []
        finally:
            env.restore_state(snap)
