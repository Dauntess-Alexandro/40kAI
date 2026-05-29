from core.telemetry.gpu_backend import GpuSample
from app.gui_qt.telemetry.local_probe import LocalTelemetryProbe


class _FakeProc:
    def sample(self, pid):
        return {"cpu_pct": 50.0, "ram_pct": 40.0, "ram_gb": 3.2, "ok": True}


class _FakeGpu:
    def read_devices(self):
        return [GpuSample(index=0, name="RTX 5060 Ti", util=81,
                          mem_used_mb=4096, mem_total_mb=16384, temp_c=64)]

    def process_memory_mb(self, pids):
        return {0: 3500}


def test_local_probe_builds_snapshot():
    probe = LocalTelemetryProbe(proc_meter=_FakeProc(), gpu_backend=_FakeGpu())
    snap = probe.sample(pid=1234, child_pids={1234, 5678})
    assert snap["cpu_pct"] == 50.0
    assert snap["ram_gb"] == 3.2
    assert len(snap["gpus"]) == 1
    g = snap["gpus"][0]
    assert g["name"] == "RTX 5060 Ti"
    assert g["util"] == 81
    assert g["proc_mem_mb"] == 3500
    assert g["mem_total_mb"] == 16384
