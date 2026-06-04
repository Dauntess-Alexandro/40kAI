from __future__ import annotations

import platform
from typing import Any, Optional

from core.telemetry.gpu_backend import GpuBackend
from app.gui_qt.telemetry.process_meter import ProcessMeter


def _detect_local_cpu_name() -> str:
    """Human-readable CPU label for the local telemetry card."""
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        ) as key:
            value, _kind = winreg.QueryValueEx(key, "ProcessorNameString")
            name = str(value or "").strip()
            if name:
                return name
    except Exception:
        pass

    try:
        name = str(platform.processor() or "").strip()
        if name:
            return name
    except Exception:
        pass
    return "CPU"


class LocalTelemetryProbe:
    def __init__(self, proc_meter: Any = None, gpu_backend: Any = None) -> None:
        self._proc = proc_meter if proc_meter is not None else ProcessMeter()
        self._gpu = gpu_backend if gpu_backend is not None else GpuBackend()
        self._cpu_name = _detect_local_cpu_name()

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
            "cpu_name": self._cpu_name,
            "cpu_pct": cpu_ram["cpu_pct"],
            "ram_pct": cpu_ram["ram_pct"],
            "ram_gb": cpu_ram["ram_gb"],
            "cpu_pct_system": cpu_ram.get("cpu_pct_system"),
            "ram_pct_system": cpu_ram.get("ram_pct_system"),
            "ram_gb_system": cpu_ram.get("ram_gb_system"),
            "ok": cpu_ram["ok"],
            "gpus": gpus,
        }
