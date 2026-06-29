"""GUI train prefs: сохранение выбранной миссии между сессиями."""

from __future__ import annotations

import json

from app.gui_qt.gui_train_prefs import (
    QSETTINGS_MISSION_KEY,
    load_selected_mission,
    save_selected_mission,
)


class _FakeSettings:
    def __init__(self) -> None:
        self._d: dict[str, object] = {}

    def setValue(self, key: str, value: object) -> None:
        self._d[key] = value

    def contains(self, key: str) -> bool:
        return key in self._d

    def value(self, key: str, default: object = None) -> object:
        return self._d.get(key, default)


def test_save_and_load_selected_mission_roundtrip() -> None:
    settings = _FakeSettings()
    saved = save_selected_mission(settings, "annihilation")
    assert saved == "annihilation"
    assert settings._d[QSETTINGS_MISSION_KEY] == "annihilation"
    assert load_selected_mission(settings) == "annihilation"


def test_load_prefers_qsettings_over_data_json(tmp_path) -> None:
    settings = _FakeSettings()
    save_selected_mission(settings, "annihilation")
    data_path = tmp_path / "data.json"
    data_path.write_text(json.dumps({"mission": "only_war"}), encoding="utf-8")
    assert load_selected_mission(settings, data_json_path=data_path) == "annihilation"


def test_load_falls_back_to_data_json(tmp_path) -> None:
    settings = _FakeSettings()
    data_path = tmp_path / "data.json"
    data_path.write_text(json.dumps({"mission": "annihilation"}), encoding="utf-8")
    assert load_selected_mission(settings, data_json_path=data_path) == "annihilation"


def test_invalid_mission_falls_back_to_default(tmp_path) -> None:
    settings = _FakeSettings()
    settings.setValue(QSETTINGS_MISSION_KEY, "unknown_mission")
    assert load_selected_mission(settings, data_json_path=tmp_path / "missing.json") == "only_war"
