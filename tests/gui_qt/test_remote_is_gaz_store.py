"""GAZ GUI store: remote_is_gaz.json (отдельно от AZ/SMZ) + префикс QSettings-ключа.

Файловый путь уже параметризован (filename) — как у SMZ (remote_is_smz.json).
Здесь фиксируем, что GAZ-конфиг не пересекается с AZ ни в файле, ни в QSettings.
"""

from __future__ import annotations

from app.gui_qt.remote_is_store import (
    apply_remote_is_to_qsettings,
    load_remote_is,
    load_remote_is_from_qsettings,
    save_remote_is,
)


def test_gaz_file_roundtrip_separate_from_az(tmp_path):
    save_remote_is(tmp_path, {"user_enabled_lan": True, "host": "192.168.0.55", "port": 5565},
                   "remote_is_gaz.json")
    # AZ-файл не затронут
    az = load_remote_is(tmp_path, "remote_is.json")
    assert az.get("user_enabled_lan") is False
    gaz = load_remote_is(tmp_path, "remote_is_gaz.json")
    assert gaz["host"] == "192.168.0.55"
    assert gaz["port"] == 5565
    assert gaz["user_enabled_lan"] is True


class _FakeSettings:
    def __init__(self):
        self._d = {}

    def setValue(self, k, v):
        self._d[k] = v

    def contains(self, k):
        return k in self._d

    def value(self, k, default=None):
        return self._d.get(k, default)


def test_gaz_qsettings_prefix_isolated_from_az():
    s = _FakeSettings()
    apply_remote_is_to_qsettings(s, {"enabled": True, "host": "10.0.0.2", "port": 5565},
                                 prefix="remote_is_gaz")
    # ключи лежат под remote_is_gaz/, не под remote_is/
    assert s.contains("remote_is_gaz/host")
    assert not s.contains("remote_is/host")
    loaded = load_remote_is_from_qsettings(s, prefix="remote_is_gaz")
    assert loaded["host"] == "10.0.0.2"
    assert loaded["port"] == 5565


def test_az_qsettings_default_prefix_unchanged():
    s = _FakeSettings()
    apply_remote_is_to_qsettings(s, {"enabled": True, "host": "10.0.0.9", "port": 5555})
    assert s.contains("remote_is/host")
    loaded = load_remote_is_from_qsettings(s)
    assert loaded["host"] == "10.0.0.9"
