"""Фасад reward-конфигурации: делегирует константы на активный профиль миссии.

Профиль выбирается configure_for_mission() (зовётся из mission.apply_mission_layout).
Контракт:
- ЧТЕНИЕ идёт как reward_config.X — делегируется на активный профиль (__getattr__);
- ЗАПИСЬ reward_config.X = v (рантайм-автотюнинг в train.py, monkeypatch в тестах)
  делегируется на активный профиль (__setattr__), а НЕ в namespace фасада — иначе
  запись осела бы в __dict__ фасада и навсегда затенила __getattr__ (переживая reload).
- прямой `from reward_config import NAME` НЕ использовать (захват по значению не видит
  смену профиля).
Реализация: модуль на старте меняет свой __class__ на _RewardConfigFacade (паттерн
PEP 562 + делегирующий __setattr__). __class__-swap (а не подмена sys.modules) сохраняет
корректную работу importlib.reload(reward_config)."""
import importlib
import sys
import types

import reward_config_annihilation as _profile_annihilation
import reward_config_onlywar as _profile_only_war

# При reload фасада (importlib.reload(reward_config)) перезагружаем профили, чтобы
# env-override HEUR_CALIBRATION_OVERRIDES_JSON применился к активному профилю.
# Контракт: reload(reward_config) должен видеть свежие значения констант активного профиля.
_profile_only_war = importlib.reload(_profile_only_war)
_profile_annihilation = importlib.reload(_profile_annihilation)

_PROFILES = {
    "only_war": _profile_only_war,
    "training_grounds": _profile_only_war,
    "annihilation": _profile_annihilation,
}
_active = _profile_only_war
_active_name = "only_war"

# Имена, принадлежащие самому фасаду: пишутся/читаются в его собственном __dict__,
# не делегируются на профиль.
_FACADE_OWN = frozenset({
    "_active", "_active_name", "_PROFILES", "_FACADE_OWN",
    "configure_for_mission", "active_profile_name",
})


def configure_for_mission(mission_name):
    """Ставит активный reward-профиль по имени миссии. Возвращает имя профиля."""
    global _active, _active_name
    key = (mission_name or "only_war").strip().lower().replace("-", "_").replace(" ", "_")
    profile = _PROFILES.get(key, _profile_only_war)
    _active = profile
    _active_name = "annihilation" if profile is _profile_annihilation else "only_war"
    return _active_name


def active_profile_name():
    return _active_name


class _RewardConfigFacade(types.ModuleType):
    def __getattr__(self, name):
        # Вызывается только если name нет в __dict__ модуля.
        # Делегируем ВСЁ (константы + apply_heur_calibration_overrides) на активный профиль.
        return getattr(_active, name)

    def __setattr__(self, name, value):
        # Внешние записи (reward_config.X = v / setattr / monkeypatch) уходят в активный
        # профиль, а не в __dict__ фасада — иначе они затенят __getattr__ и переживут reload.
        if name in _FACADE_OWN or name.startswith("__"):
            object.__setattr__(self, name, value)
        else:
            setattr(_active, name, value)


# Сменить класс существующего модуля (reload-safe, в отличие от подмены sys.modules).
sys.modules[__name__].__class__ = _RewardConfigFacade
