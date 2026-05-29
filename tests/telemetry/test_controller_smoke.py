import pytest

pytest.importorskip("PySide6")

from app.gui_qt.telemetry.controller import TelemetryController


class _FakeLocal:
    def sample(self, pid, child_pids=None):
        return {"cpu_pct": 50.0, "ram_pct": 40.0, "ram_gb": 3.2, "ok": True,
                "gpus": [{"index": 0, "name": "GPU", "util": 80, "mem_used_mb": 4000,
                          "mem_total_mb": 16000, "proc_mem_mb": 3000, "temp_c": 60}]}


def test_controller_refresh_builds_cards_property():
    c = TelemetryController(local_probe=_FakeLocal())
    c.set_context(pid=123, algo="gumbel_muzero", active=True, remote_cfg=None)
    c.feed_log_line("[GMZ][INF_SERVER] batch=10 inference_ms=12 total_reqs=5")
    c._refresh_sync()  # синхронный прогон без QThreadPool для теста
    cards = c.cards
    ids = [x["id"] for x in cards]
    assert "gpu0" in ids and "cpu" in ids and "ram" in ids and "batch" in ids
    assert c.active is True
