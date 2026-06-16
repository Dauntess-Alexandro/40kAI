"""PC2 → PC1 телеметрия через SMB-файл (Qt-free).

ПК2 (distributed actors, без inference-сервера) сэмплит СИСТЕМНУЮ нагрузку
(не процесс) и пишет JSON в общую папку. ПК1 читает и отдаёт в готовые карточки
«ПК2 · GPU/CPU» (app/gui_qt/telemetry/cards.py). Имена железа определяются сами.
"""

from __future__ import annotations

import json
import os
import platform
import tempfile
import time
from typing import Any

TELEMETRY_FILENAME = "pc2_telemetry.json"


def detect_cpu_name() -> str:
    """Человекочитаемое имя CPU (Windows: реестр, иначе platform)."""
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


def sample_cpu_ram_system() -> dict[str, Any]:
    """Мгновенные системные CPU%/RAM% (psutil). Без имени CPU (его кэшируют отдельно).
    Все значения None, если psutil недоступен."""
    cpu_pct = None
    ram_pct = None
    ram_gb = None
    try:
        import psutil

        cpu_pct = float(psutil.cpu_percent(interval=None))
        vm = psutil.virtual_memory()
        ram_pct = float(vm.percent)
        ram_gb = round(float(vm.used) / (1024**3), 1)
    except Exception:
        pass
    return {
        "cpu_pct_system": cpu_pct,
        "ram_pct_system": ram_pct,
        "ram_gb_system": ram_gb,
    }


def sample_system_telemetry() -> dict[str, Any]:
    """Системные CPU/RAM (psutil) + первый GPU (GpuBackend) в форме карточек ПК2."""
    gpu: dict[str, Any] = {
        "name": None,
        "util": None,
        "mem_used_mb": None,
        "mem_total_mb": None,
        "temp_c": None,
    }
    try:
        from core.telemetry.gpu_backend import GpuBackend

        devices = GpuBackend().read_devices()
        if devices:
            g = devices[0]
            gpu = {
                "name": g.name,
                "util": g.util,
                "mem_used_mb": g.mem_used_mb,
                "mem_total_mb": g.mem_total_mb,
                "temp_c": g.temp_c,
            }
    except Exception:
        pass

    return {
        "name": gpu["name"] or "GPU",
        "util": gpu["util"],
        "mem_used_mb": gpu["mem_used_mb"],
        "mem_total_mb": gpu["mem_total_mb"],
        "temp_c": gpu["temp_c"],
        "cpu_name": detect_cpu_name(),
        **sample_cpu_ram_system(),
    }


def write_pc2_telemetry(path: str, sample: dict[str, Any]) -> None:
    """Атомарно записать сэмпл (со штампом _ts) — чтобы ПК1 не прочитал полуфайл."""
    body = dict(sample or {})
    body["_ts"] = time.time()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    try:
        fd, tmp = tempfile.mkstemp(dir=parent or ".", prefix=".pc2tel_", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(body, handle, ensure_ascii=False)
        os.replace(tmp, path)
    except OSError:
        pass


def read_pc2_telemetry(path: str, max_age_sec: float = 10.0) -> dict[str, Any] | None:
    """Прочитать сэмпл ПК2; None если файла нет или он устарел (ПК2 отвалился)."""
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    ts = data.get("_ts")
    if not isinstance(ts, (int, float)) or (time.time() - float(ts)) > float(max_age_sec):
        return None
    return data
