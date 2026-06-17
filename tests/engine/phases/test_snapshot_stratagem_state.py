from core.engine.phases import stratagem_engine
from tests.engine.phases._helpers import build_env


def _action(use_cp: int, cp_on: int, n: int) -> dict:
    a = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": use_cp, "cp_on": cp_on}
    for i in range(n):
        a[f"move_num_{i}"] = 0
    return a


def test_snapshot_restore_preserves_stratagem_journal_and_enemy_cp():
    env = build_env()
    env.modelCP = 3
    env.stratagem_used = []
    env._enemy_cp_on = 1
    env._enemy_use_cp = 2

    snap = env.snapshot_state()

    # мутации после снимка
    stratagem_engine.apply(env, "model", "insane_bravery", 0, phase="command")
    env._enemy_cp_on = 9
    env._enemy_use_cp = 0
    assert env.stratagem_used == [("model", "insane_bravery", env.battle_round, "command", 0)]

    env.restore_state(snap)

    assert env.stratagem_used == []
    assert env.modelCP == 3
    assert env._enemy_cp_on == 1
    assert env._enemy_use_cp == 2


def test_enemy_insane_bravery_records_journal_and_snapshot_restore_preserves_it():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.enemy_health)
    env.enemy_data[0]["Ld"] = 13
    env.enemy_health[0] = 1.0
    env.enemyCP = 1
    env.stratagem_used = []

    with env.simulation_mode():
        battle_shock = env.command_phase("enemy", action=_action(1, 0, n))

    expected = ("enemy", "insane_bravery", env.battle_round, "command", 0)
    assert battle_shock[0] is False
    assert expected in env.stratagem_used
    assert env.enemyCP == 1

    snap = env.snapshot_state()
    env.stratagem_used = []
    env.enemyCP = 99

    env.restore_state(snap)

    assert expected in env.stratagem_used
    assert env.enemyCP == 1
