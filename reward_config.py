"""Фасад reward-конфигурации: делегирует константы на активный профиль миссии.

Профиль выбирается configure_for_mission() (зовётся из mission.apply_mission_layout).
Контракт: все чтения идут как reward_config.X (атрибут); прямой `from reward_config import NAME`
не использовать (захват по значению не увидит смену профиля)."""
import importlib

import reward_config_onlywar as _profile_only_war
import reward_config_annihilation as _profile_annihilation

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


def __getattr__(name):
    # Делегируем ВСЁ (константы + apply_heur_calibration_overrides) на активный профиль.
    return getattr(_active, name)
