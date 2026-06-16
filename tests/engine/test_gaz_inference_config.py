"""GAZ env-резолв: приоритет GAZ_* → AZ_* → default (тонкий слой на AZ-инфре).

GAZ едет на общей AZ-инфраструктуре, но управляется своими GAZ_* env, чтобы не
пересекаться с AZ-запусками. Для не-GAZ алго GAZ_* игнорируется (AZ без изменений).
"""

from __future__ import annotations

from core.models.az_family_env import resolve_az_family_env


def _getter(mapping):
    return mapping.get


def test_gaz_env_has_priority_over_az():
    env = {"GAZ_INFERENCE_SERVER": "1", "AZ_INFERENCE_SERVER": "0"}
    val = resolve_az_family_env(
        "GAZ_INFERENCE_SERVER", "AZ_INFERENCE_SERVER", "0",
        is_gumbel=True, getenv=_getter(env),
    )
    assert val == "1"


def test_az_env_used_when_gaz_absent_for_gumbel():
    env = {"AZ_INFERENCE_SERVER": "1"}
    val = resolve_az_family_env(
        "GAZ_INFERENCE_SERVER", "AZ_INFERENCE_SERVER", "0",
        is_gumbel=True, getenv=_getter(env),
    )
    assert val == "1"


def test_non_gumbel_ignores_gaz_env():
    # Для AZ/прочих GAZ_* не учитывается — поведение AZ без изменений.
    env = {"GAZ_INFERENCE_SERVER": "1", "AZ_INFERENCE_SERVER": "0"}
    val = resolve_az_family_env(
        "GAZ_INFERENCE_SERVER", "AZ_INFERENCE_SERVER", "0",
        is_gumbel=False, getenv=_getter(env),
    )
    assert val == "0"


def test_default_when_nothing_set():
    val = resolve_az_family_env(
        "GAZ_INFERENCE_REMOTE_PORT", "AZ_INFERENCE_REMOTE_PORT", "5565",
        is_gumbel=True, getenv=_getter({}),
    )
    assert val == "5565"


def test_non_gumbel_falls_back_to_az_then_default():
    val = resolve_az_family_env(
        "GAZ_X", "AZ_X", "deflt", is_gumbel=False, getenv=_getter({}),
    )
    assert val == "deflt"


def test_empty_string_env_is_respected_not_skipped():
    # Пустая строка в env — это явно заданное значение, не None → используется.
    env = {"GAZ_AUTH": ""}
    val = resolve_az_family_env(
        "GAZ_AUTH", "AZ_AUTH", "fallback", is_gumbel=True, getenv=_getter(env),
    )
    assert val == ""
