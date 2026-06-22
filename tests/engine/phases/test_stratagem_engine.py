import pytest

from core.engine.phases import stratagem_engine
from tests.engine.phases._helpers import build_env


def test_apply_spends_cp_and_records_model():
    env = build_env()
    env.modelCP = 3
    env.battle_round = 2
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "model", "insane_bravery", 0, phase="command")
    assert res == {"ok": True, "cp_spent": 1, "reason": None}
    assert env.modelCP == 2
    assert env.stratagem_used == [("model", "insane_bravery", 2, "command", 0)]


def test_apply_spends_cp_enemy_side():
    env = build_env()
    env.enemyCP = 1
    env.battle_round = 1
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "enemy", "insane_bravery", 1, phase="command")
    assert res["ok"] is True
    assert env.enemyCP == 0
    assert env.stratagem_used == [("enemy", "insane_bravery", 1, "command", 1)]


def test_apply_no_cp_is_noop():
    env = build_env()
    env.modelCP = 0
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "model", "insane_bravery", 0)
    assert res == {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
    assert env.modelCP == 0
    assert env.stratagem_used == []


def test_apply_unknown_id_raises():
    env = build_env()
    env.modelCP = 3
    with pytest.raises(KeyError):
        stratagem_engine.apply(env, "model", "does_not_exist", 0)


def test_command_reroll_payload_records_roll_subtype():
    env = build_env()
    env.modelCP = 3
    env.battle_round = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="fight", reroll_roll="hit")
    rec = [r for r in env.active_stratagem_effects if r["effect_id"] == "command_reroll"][0]
    assert rec["reroll_roll"] == "hit"
    assert rec["consumed"] is False
