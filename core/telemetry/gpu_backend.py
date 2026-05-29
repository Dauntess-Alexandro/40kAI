from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class GpuSample:
    index: int
    name: str
    util: Optional[int]            # % устройства целиком; None если недоступно
    mem_used_mb: int
    mem_total_mb: int
    temp_c: Optional[int]
    proc_mem_mb: int = 0           # VRAM, занятая нашим процессом+детьми (заполняется отдельно)


def _to_int(token: str) -> Optional[int]:
    t = token.strip()
    if not t or t.upper().startswith("[N/A") or t.upper() == "N/A":
        return None
    try:
        return int(float(t))
    except ValueError:
        return None


def parse_nvidia_smi_csv(text: str) -> list[GpuSample]:
    """Парс строк: index, name, util.gpu, mem.used, mem.total, temp (--format=csv,noheader,nounits)."""
    out: list[GpuSample] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 6:
            continue
        idx = _to_int(parts[0])
        if idx is None:
            continue
        out.append(
            GpuSample(
                index=idx,
                name=parts[1],
                util=_to_int(parts[2]),
                mem_used_mb=_to_int(parts[3]) or 0,
                mem_total_mb=_to_int(parts[4]) or 0,
                temp_c=_to_int(parts[5]),
            )
        )
    return out


class GpuBackend:
    """NVML, с fallback на nvidia-smi. Инициализирует NVML один раз."""

    def __init__(self) -> None:
        self._nvml = None
        self._nvml_ok = False
        try:
            import pynvml

            pynvml.nvmlInit()
            self._nvml = pynvml
            self._nvml_ok = True
        except Exception:
            self._nvml = None
            self._nvml_ok = False

    def available(self) -> bool:
        return self._nvml_ok or self._nvml_smi_available()

    @staticmethod
    def _nvml_smi_available() -> bool:
        try:
            subprocess.run(["nvidia-smi", "-L"], capture_output=True, timeout=3, check=False)
            return True
        except Exception:
            return False

    def read_devices(self) -> list[GpuSample]:
        if self._nvml_ok:
            try:
                return self._read_nvml()
            except Exception:
                pass
        return self._read_smi()

    def _read_nvml(self) -> list[GpuSample]:
        p = self._nvml
        out: list[GpuSample] = []
        for i in range(p.nvmlDeviceGetCount()):
            h = p.nvmlDeviceGetHandleByIndex(i)
            name = p.nvmlDeviceGetName(h)
            if isinstance(name, bytes):
                name = name.decode("utf-8", "replace")
            mem = p.nvmlDeviceGetMemoryInfo(h)
            try:
                util = int(p.nvmlDeviceGetUtilizationRates(h).gpu)
            except Exception:
                util = None
            try:
                temp = int(p.nvmlDeviceGetTemperature(h, p.NVML_TEMPERATURE_GPU))
            except Exception:
                temp = None
            out.append(
                GpuSample(
                    index=i, name=str(name), util=util,
                    mem_used_mb=int(mem.used // (1024 * 1024)),
                    mem_total_mb=int(mem.total // (1024 * 1024)),
                    temp_c=temp,
                )
            )
        return out

    def _read_smi(self) -> list[GpuSample]:
        try:
            res = subprocess.run(
                ["nvidia-smi",
                 "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu",
                 "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=4, check=False,
            )
            return parse_nvidia_smi_csv(res.stdout or "")
        except Exception:
            return []

    def process_memory_mb(self, pids: set[int]) -> dict[int, int]:
        """gpu_index -> суммарная VRAM (MB) процессов из pids. Только NVML; иначе пусто."""
        if not self._nvml_ok or not pids:
            return {}
        p = self._nvml
        out: dict[int, int] = {}
        try:
            for i in range(p.nvmlDeviceGetCount()):
                h = p.nvmlDeviceGetHandleByIndex(i)
                total = 0
                try:
                    procs = p.nvmlDeviceGetComputeRunningProcesses(h)
                except Exception:
                    procs = []
                for pr in procs:
                    if int(getattr(pr, "pid", -1)) in pids:
                        used = getattr(pr, "usedGpuMemory", 0) or 0
                        total += int(used) // (1024 * 1024)
                out[i] = total
        except Exception:
            return {}
        return out
