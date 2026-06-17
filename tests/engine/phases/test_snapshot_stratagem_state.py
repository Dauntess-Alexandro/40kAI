from core.engine.phases import stratagem_engine
from tests.engine.phases._helpers import build_env


def test_snapshot_restore_preserves_stratagem_journal_and_enemy_cp():
    env = build_env()
    env.modelCP = 3
    env.stratagem_used = []
    env._enemy_cp_on = 1
    env._enemy_use_cp = 2

    snap = env.snapshot_state()

    # мутации после снимка
    stratagem_engine.apply(env, "model", "insane_bravery", 0)
    env._enemy_cp_on = 9
    env._enemy_use_cp = 0
    assert env.stratagem_used == [("model", "insane_bravery", env.battle_round)]

    env.restore_state(snap)

    assert env.stratagem_used == []
    assert env.modelCP == 3
    assert env._enemy_cp_on == 1
    assert env._enemy_use_cp == 2
