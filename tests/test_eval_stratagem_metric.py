"""Характеризационные тесты хелпера stratagem_attempt_from_action.

Фиксируем текущее поведение маппинга USE_CP_STRATAGEM_HEAD до переименования
метрики cp_used → use_cp_head_set.

Heads 2/3/4 (overwatch/smokescreen/heroic_intervention) — только для трейс-логов;
в плоском action_dict они НЕ исполняются (реакции идут через value-gate).
"""
from core.telemetry.stratagem_trace import stratagem_attempt_from_action


def test_use_cp_head_maps_only_known_ids():
    # head 1 → insane_bravery (единственный реально исполняемый в плоском пути)
    assert stratagem_attempt_from_action({"use_cp": 1, "cp_on": 0})[0] == "insane_bravery"
    # head 0 → нет стратагемы
    assert stratagem_attempt_from_action({"use_cp": 0})[0] is None


def test_cp_on_unit_propagated():
    sid, unit = stratagem_attempt_from_action({"use_cp": 1, "cp_on": 2})
    assert sid == "insane_bravery"
    assert unit == 2


def test_head_2_3_4_mapped_for_trace():
    """heads 2/3/4 — трейс-маппинг присутствует (хотя в flat-path не исполняются)."""
    assert stratagem_attempt_from_action({"use_cp": 2})[0] == "overwatch"
    assert stratagem_attempt_from_action({"use_cp": 3})[0] == "smokescreen"
    assert stratagem_attempt_from_action({"use_cp": 4})[0] == "heroic_intervention"


def test_missing_use_cp_key():
    # нет ключа use_cp → None
    sid, unit = stratagem_attempt_from_action({})
    assert sid is None
    assert unit is None
