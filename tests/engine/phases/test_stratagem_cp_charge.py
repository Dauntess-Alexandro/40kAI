"""TDD-тесты для единой точки CP-расхода `charge_cp` (подзадача 1.1).

Покрывает:
- прямые сценарии списания CP для model/enemy;
- защиту от ухода CP в минус (недостаточно CP → noop);
- cost<=0 → noop-success;
- интеграцию с `apply()` без смены поведения для не-reroll стратагем
  (insane_bravery): успех списывает CP и пишет в stratagem_used;
  нехватка CP → ok=False, reason="not_enough_cp", журнал не меняется.
"""

from core.engine.phases import stratagem_engine
from core.engine.phases.stratagem_engine import charge_cp
from tests.engine.phases._helpers import build_env


def test_charge_cp_model_success():
    env = build_env()
    env.modelCP = 3
    env.enemyCP = 5
    ok = charge_cp(env, "model", 1)
    assert ok is True
    assert env.modelCP == 2
    assert env.enemyCP == 5


def test_charge_cp_enemy_success():
    env = build_env()
    env.modelCP = 4
    env.enemyCP = 2
    ok = charge_cp(env, "enemy", 2)
    assert ok is True
    assert env.enemyCP == 0
    assert env.modelCP == 4


def test_charge_cp_not_enough_cp_noop():
    env = build_env()
    env.modelCP = 0
    env.enemyCP = 7
    ok = charge_cp(env, "model", 1)
    assert ok is False
    assert env.modelCP == 0
    assert env.enemyCP == 7


def test_charge_cp_zero_cost_noop_success():
    env = build_env()
    env.modelCP = 0
    ok = charge_cp(env, "model", 0)
    assert ok is True
    assert env.modelCP == 0


def test_apply_uses_charge_cp_for_non_reroll_without_behavior_change():
    env = build_env()
    env.modelCP = 3
    env.battle_round = 2
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "model", "insane_bravery", 0, phase="command")
    assert res == {"ok": True, "cp_spent": 1, "reason": None}
    assert env.modelCP == 2
    assert env.stratagem_used == [("model", "insane_bravery", 2, "command", 0)]


def test_apply_no_cp_still_noop():
    env = build_env()
    env.modelCP = 0
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "model", "insane_bravery", 0)
    assert res == {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
    assert env.modelCP == 0
    assert env.stratagem_used == []
