from app.gui_qt.telemetry.remote_probe import RemoteTelemetryProbe


def _fake_health_ok(**kwargs):
    return {
        "kind": "health_check", "status": "ok", "gpu_name": "RTX 2060 SUPER",
        "gpu_util": 40, "gpu_mem_used_mb": 2048, "gpu_mem_total_mb": 8192,
        "gpu_temp_c": 55, "avg_batch": 9.5, "queue_depth": 2,
    }


def _fake_health_fail(**kwargs):
    raise RuntimeError("unreachable")


def test_remote_probe_maps_payload():
    p = RemoteTelemetryProbe(host="10.0.0.2", port=5555, health_fn=_fake_health_ok)
    snap = p.sample()
    assert snap is not None
    assert snap["name"] == "RTX 2060 SUPER"
    assert snap["util"] == 40
    assert snap["proc_mem_mb"] == 2048  # для удалённого = занятая на карте
    assert snap["mem_total_mb"] == 8192
    assert snap["avg_batch"] == 9.5


def test_remote_probe_returns_none_on_error():
    p = RemoteTelemetryProbe(host="10.0.0.2", port=5555, health_fn=_fake_health_fail)
    assert p.sample() is None
