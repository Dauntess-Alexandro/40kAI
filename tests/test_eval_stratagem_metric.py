"""Тесты stratagem_attempt_from_action после удаления контракта use_cp/cp_on (task-4).

Контракт-ключи use_cp/cp_on удалены из action_dict в task-4 (коммит b2673e11).
Функция stratagem_attempt_from_action теперь всегда возвращает (None, None) —
стратагемы идут через strat_command-голову и журнал stratagem_used, не через flat-head.
"""
from core.telemetry.stratagem_trace import (
    collect_stratagem_attempt_specs,
    stratagem_attempt_from_action,
)


def test_attempt_from_action_always_none_without_use_cp():
    """use_cp/cp_on удалены из контракта → функция возвращает (None, None) для любого dict."""
    assert stratagem_attempt_from_action({}) == (None, None)
    assert stratagem_attempt_from_action({"move": 0, "attack": 1}) == (None, None)


def test_attempt_from_action_ignores_stale_use_cp_key():
    """Если в action_dict случайно попал старый ключ use_cp — всё равно (None, None)."""
    sid, unit = stratagem_attempt_from_action({"use_cp": 1, "cp_on": 0})
    assert sid is None
    assert unit is None


def test_collect_attempt_specs_fight_plan_only():
    """fight_plan по-прежнему попадает в specs; use_cp-ветка мертва."""
    specs = collect_stratagem_attempt_specs(
        {"move": 0, "attack": 0},
        {1: "hungry_void"},
    )
    assert specs == [("hungry_void", 1, "fight_plan")]


def test_collect_attempt_specs_empty_action():
    """Без fight_plan и без use_cp-контракта — пустой список."""
    specs = collect_stratagem_attempt_specs({}, None)
    assert specs == []
