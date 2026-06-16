"""PC2 → PC1 телеметрия через SMB-файл: запись/чтение/свежесть + форма сэмпла."""

from __future__ import annotations

import json
import time

from core.telemetry.pc2_telemetry import (
    read_pc2_telemetry,
    sample_system_telemetry,
    write_pc2_telemetry,
)


def test_write_read_roundtrip(tmp_path):
    path = str(tmp_path / "pc2_telemetry.json")
    sample = {"name": "RTX 2060 SUPER", "util": 42, "cpu_name": "Ryzen 5 1600", "cpu_pct_system": 30}
    write_pc2_telemetry(path, sample)
    got = read_pc2_telemetry(path, max_age_sec=10.0)
    assert got is not None
    assert got["name"] == "RTX 2060 SUPER"
    assert got["cpu_name"] == "Ryzen 5 1600"


def test_read_missing_returns_none(tmp_path):
    assert read_pc2_telemetry(str(tmp_path / "nope.json")) is None


def test_read_stale_returns_none(tmp_path):
    path = str(tmp_path / "pc2_telemetry.json")
    # ts в прошлом → за пределами max_age → None (ПК2 встал/отвалился).
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"name": "GPU", "_ts": time.time() - 60.0}, f)
    assert read_pc2_telemetry(path, max_age_sec=10.0) is None


def test_write_stamps_ts(tmp_path):
    path = str(tmp_path / "pc2_telemetry.json")
    write_pc2_telemetry(path, {"name": "GPU"})
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert "_ts" in data and isinstance(data["_ts"], (int, float))


def test_telemetry_file_produces_pc2_cards(tmp_path):
    # ПК2 пишет файл → ПК1 читает → build_cards рисует карточки «ПК2 · GPU/CPU».
    from app.gui_qt.telemetry.cards import build_cards

    path = str(tmp_path / "pc2_telemetry.json")
    write_pc2_telemetry(path, {
        "name": "RTX 2060 SUPER", "util": 55,
        "cpu_name": "AMD Ryzen 5 1600", "cpu_pct_system": 40, "ram_pct_system": 33,
    })
    remote = read_pc2_telemetry(path, max_age_sec=10.0)
    cards = build_cards(
        local={"cpu_name": "PC1", "cpu_pct": 5, "cpu_pct_system": 5, "ram_pct": 10, "ram_gb": 2, "ok": True, "gpus": []},
        remote=remote, batch_avg=None, batch_size_hint=None, algo="dqn", active=True, labels={},
    )
    pc2_labels = [str(c.get("label", "")) for c in cards if str(c.get("variant")) == "remote"]
    assert any("RTX 2060 SUPER" in s for s in pc2_labels)
    assert any("Ryzen 5 1600" in s for s in pc2_labels)


def test_sample_system_telemetry_shape():
    s = sample_system_telemetry()
    # Должны быть ключи под карточки ПК2 (cards.py: name/util + cpu_name/cpu_pct_system).
    for key in ("name", "util", "cpu_name", "cpu_pct_system", "ram_pct_system"):
        assert key in s
    assert isinstance(s["cpu_name"], str) and s["cpu_name"]


def test_sample_cpu_ram_system_shape():
    from core.telemetry.pc2_telemetry import sample_cpu_ram_system

    s = sample_cpu_ram_system()
    assert set(s.keys()) == {"cpu_pct_system", "ram_pct_system", "ram_gb_system"}
    for v in s.values():
        assert v is None or isinstance(v, float)
