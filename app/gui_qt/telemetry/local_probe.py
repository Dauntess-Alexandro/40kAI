from __future__ import annotations

from typing import Any, Optional

from core.telemetry.gpu_backend import GpuBackend
from app.gui_qt.telemetry.process_meter import ProcessMeter


class LocalTelemetryProbe:
    def __init__(self, proc_meter: Any = None, gpu_backend: Any = None) -> None:
        self._proc = proc_meter if proc_meter is not None else ProcessMeter()
        self._gpu = gpu_backend if gpu_backend is not None else GpuBackend()

    def sample(self, pid: Optional[int], child_pids: Optional[set[int]] = None) -> dict[str, Any]:
        cpu_ram = self._proc.sample(pid)
        gpus_raw = self._gpu.read_devices()
        # PID процесса train — это cmd.exe; реальные GPU-процессы это его дети,
        # поэтому для NVML-сопоставления берём весь набор живых PID дерева.
        match_pids = child_pids or cpu_ram.get("pids") or ({int(pid)} if pid else set())
        proc_mem = self._gpu.process_memory_mb(match_pids)
        gpus = []
        for g in gpus_raw:
            gpus.append(
                {
                    "index": g.index,
                    "name": g.name,
                    "util": g.util,
                    "mem_used_mb": g.mem_used_mb,
                    "mem_total_mb": g.mem_total_mb,
                    "temp_c": g.temp_c,
                    "proc_mem_mb": int(proc_mem.get(g.index, 0)),
                }
            )
        return {
            "cpu_pct": cpu_ram["cpu_pct"],
            "ram_pct": cpu_ram["ram_pct"],
            "ram_gb": cpu_ram["ram_gb"],
            "ok": cpu_ram["ok"],
            "gpus": gpus,
        }
