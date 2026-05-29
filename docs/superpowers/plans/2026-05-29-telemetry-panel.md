# Live Telemetry Panel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Живая лента телеметрии на вкладке «Главная» под прогресс-баром: util% локальных GPU + GPU ПК2 (LAN), CPU/RAM по процессу train.py, средний батч поиска — обновление раз в секунду.

**Architecture:** Чистые (без Qt) пробники в `core/telemetry/` (GPU через pynvml/nvidia-smi) и `app/gui_qt/telemetry/` (CPU/RAM через psutil, парсер батча, сборка карточек). Тонкий `TelemetryController(QObject)` крутит `QTimer`, гоняет пробинг в `QThreadPool`, отдаёт в QML готовый список карточек через свойство. Новый `TelemetryStrip.qml` рисует карточки; ПК2 отдаёт GPU-поля через расширенный `health_check`.

**Tech Stack:** PySide6 + QML (`QQmlApplicationEngine`, `controller` как context property), psutil, pynvml (`nvidia-ml-py`) с fallback на `nvidia-smi`, ZMQ+msgpack (health_check), pytest.

**Поправка к спеку:** UI на QML → лента это QML-компонент (не `QWidget`); общий GPU-бэкенд живёт в `core/telemetry/gpu_backend.py` (импортируется и GUI, и сервером ПК2).

---

## File Structure

| Файл | Ответственность | Действие |
|---|---|---|
| `core/telemetry/__init__.py` | пакет | Create |
| `core/telemetry/gpu_backend.py` | `GpuSample`, `GpuBackend` (NVML + nvidia-smi fallback), `parse_nvidia_smi_csv` | Create |
| `app/gui_qt/telemetry/__init__.py` | пакет | Create |
| `app/gui_qt/telemetry/process_meter.py` | `ProcessMeter` — CPU/RAM по дереву PID (psutil) | Create |
| `app/gui_qt/telemetry/batch_meter.py` | `BatchMeter` — скользящее среднее `batch=N` из stdout | Create |
| `app/gui_qt/telemetry/local_probe.py` | `LocalTelemetryProbe` — снимок local (CPU/RAM/GPU) | Create |
| `app/gui_qt/telemetry/remote_probe.py` | `RemoteTelemetryProbe` — снимок ПК2 через health_check | Create |
| `app/gui_qt/telemetry/cards.py` | `build_cards(...)` — чистая сборка списка карточек для QML | Create |
| `app/gui_qt/telemetry/controller.py` | `TelemetryController(QObject)` — таймер/threadpool/свойство | Create |
| `tools/gmz_remote_inference_server.py` | `_handle_health_check` + средний батч сервера | Modify |
| `app/gui_qt/main.py` | проводка: context property, start/stop, feed_line | Modify |
| `app/gui_qt/qml/components/TelemetryStrip.qml` | лента карточек | Create |
| `app/gui_qt/qml/Main.qml` | вставка `TelemetryStrip` после прогресс-бара | Modify |
| `requirements.txt` / installer | `psutil`, `nvidia-ml-py` | Modify |
| `tests/telemetry/test_*.py` | юнит-тесты модулей | Create |

---

### Task 1: ProcessMeter — CPU/RAM по дереву процессов

**Files:**
- Create: `app/gui_qt/telemetry/__init__.py` (пустой)
- Create: `app/gui_qt/telemetry/process_meter.py`
- Create: `tests/telemetry/__init__.py` (пустой)
- Create: `tests/telemetry/test_process_meter.py`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/telemetry/test_process_meter.py
from app.gui_qt.telemetry.process_meter import ProcessMeter, aggregate_tree


def test_aggregate_tree_sums_and_normalizes():
    # cpu_percent уже нормализован per-process (может быть >100 на многоядерных)
    samples = [
        {"cpu": 120.0, "rss": 2_000_000_000},
        {"cpu": 80.0, "rss": 1_000_000_000},
    ]
    out = aggregate_tree(samples, ncpu=4, total_ram=8_000_000_000)
    assert abs(out["cpu_pct"] - 50.0) < 1e-6   # (120+80)/4 = 50
    assert abs(out["ram_gb"] - 3.0) < 1e-6
    assert abs(out["ram_pct"] - 37.5) < 1e-6   # 3/8 *100
    assert out["ok"] is True


def test_aggregate_tree_clamps_cpu_to_100():
    samples = [{"cpu": 800.0, "rss": 0}]
    out = aggregate_tree(samples, ncpu=4, total_ram=8_000_000_000)
    assert out["cpu_pct"] == 100.0


def test_aggregate_tree_empty_is_not_ok():
    out = aggregate_tree([], ncpu=4, total_ram=8_000_000_000)
    assert out["ok"] is False
    assert out["cpu_pct"] == 0.0
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_process_meter.py -q`
Expected: FAIL — `ModuleNotFoundError`/`ImportError`.

- [ ] **Step 3: Реализовать**

```python
# app/gui_qt/telemetry/process_meter.py
from __future__ import annotations

from typing import Any, Optional


def aggregate_tree(samples: list[dict[str, Any]], *, ncpu: int, total_ram: int) -> dict[str, Any]:
    """Свести список {cpu, rss} процессов дерева в нормализованные cpu_pct/ram."""
    if not samples:
        return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False}
    cpu_sum = sum(float(s.get("cpu", 0.0)) for s in samples)
    rss_sum = sum(int(s.get("rss", 0)) for s in samples)
    ncpu = max(1, int(ncpu))
    cpu_pct = min(100.0, cpu_sum / ncpu)
    ram_gb = rss_sum / 1e9
    ram_pct = min(100.0, (rss_sum / float(total_ram)) * 100.0) if total_ram else 0.0
    return {"cpu_pct": cpu_pct, "ram_pct": ram_pct, "ram_gb": ram_gb, "ok": True}


class ProcessMeter:
    """Stateful: кэширует psutil.Process для корректного cpu_percent между тиками."""

    def __init__(self) -> None:
        self._cache: dict[int, Any] = {}
        self._psutil = None
        try:
            import psutil  # noqa: F401

            self._psutil = psutil
        except Exception:
            self._psutil = None

    def available(self) -> bool:
        return self._psutil is not None

    def sample(self, pid: Optional[int]) -> dict[str, Any]:
        ps = self._psutil
        if ps is None or pid is None:
            return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False}
        try:
            root = ps.Process(int(pid))
            procs = [root] + root.children(recursive=True)
        except Exception:
            return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False}

        samples: list[dict[str, Any]] = []
        live_pids = set()
        for p in procs:
            live_pids.add(p.pid)
            cached = self._cache.get(p.pid)
            if cached is None:
                cached = p
                self._cache[p.pid] = p
                try:
                    cached.cpu_percent(None)  # прайминг, вернёт 0 в первый раз
                except Exception:
                    pass
            try:
                cpu = cached.cpu_percent(None)
                rss = cached.memory_info().rss
            except Exception:
                continue
            samples.append({"cpu": cpu, "rss": rss})
        # вычистить мёртвые pid'ы из кэша
        for dead in [k for k in self._cache if k not in live_pids]:
            self._cache.pop(dead, None)

        return aggregate_tree(samples, ncpu=ps.cpu_count() or 1, total_ram=ps.virtual_memory().total)
```

- [ ] **Step 4: Запустить — проходит**

Run: `python -m pytest tests/telemetry/test_process_meter.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/telemetry/__init__.py app/gui_qt/telemetry/process_meter.py tests/telemetry/__init__.py tests/telemetry/test_process_meter.py
git commit -m "feat: ProcessMeter for per-process-tree CPU/RAM telemetry"
```

---

### Task 2: GpuBackend — NVML + nvidia-smi fallback

**Files:**
- Create: `core/telemetry/__init__.py` (пустой)
- Create: `core/telemetry/gpu_backend.py`
- Create: `tests/telemetry/test_gpu_backend.py`

- [ ] **Step 1: Написать падающий тест (парсер nvidia-smi CSV — чистая функция)**

```python
# tests/telemetry/test_gpu_backend.py
from core.telemetry.gpu_backend import parse_nvidia_smi_csv, GpuSample


def test_parse_nvidia_smi_csv():
    text = (
        "0, NVIDIA GeForce RTX 5060 Ti, 81, 4096, 16384, 64\n"
        "1, NVIDIA GeForce RTX 2060 SUPER, 40, 2048, 8192, 55\n"
    )
    out = parse_nvidia_smi_csv(text)
    assert len(out) == 2
    g0 = out[0]
    assert isinstance(g0, GpuSample)
    assert g0.index == 0
    assert g0.name == "NVIDIA GeForce RTX 5060 Ti"
    assert g0.util == 81
    assert g0.mem_used_mb == 4096
    assert g0.mem_total_mb == 16384
    assert g0.temp_c == 64


def test_parse_nvidia_smi_csv_handles_na_and_blank():
    text = "0, GPU, [N/A], 100, 8192, [N/A]\n\n"
    out = parse_nvidia_smi_csv(text)
    assert len(out) == 1
    assert out[0].util is None
    assert out[0].temp_c is None
    assert out[0].mem_used_mb == 100
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_gpu_backend.py -q`
Expected: FAIL — ImportError.

- [ ] **Step 3: Реализовать**

```python
# core/telemetry/gpu_backend.py
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
```

- [ ] **Step 4: Запустить — проходит**

Run: `python -m pytest tests/telemetry/test_gpu_backend.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add core/telemetry/__init__.py core/telemetry/gpu_backend.py tests/telemetry/test_gpu_backend.py
git commit -m "feat: GpuBackend (NVML + nvidia-smi fallback) for GPU telemetry"
```

---

### Task 3: BatchMeter — скользящее среднее размера батча

**Files:**
- Create: `app/gui_qt/telemetry/batch_meter.py`
- Create: `tests/telemetry/test_batch_meter.py`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/telemetry/test_batch_meter.py
from app.gui_qt.telemetry.batch_meter import BatchMeter


def test_batch_meter_average_of_parsed_lines():
    m = BatchMeter(window=10)
    m.feed_line("[GMZ][INF_SERVER] batch=10 inference_ms=12.0 total_reqs=100")
    m.feed_line("[GMZ][INF_SERVER] batch=8 inference_ms=11.0 total_reqs=108")
    assert m.average() == 9.0


def test_batch_meter_ignores_non_batch_lines():
    m = BatchMeter(window=10)
    m.feed_line("some unrelated log line")
    m.feed_line("[GMZ][INF_SERVER] started batch=10 device=cuda")  # 'batch=10' тоже распарсится
    assert m.average() == 10.0


def test_batch_meter_empty_average_is_none():
    assert BatchMeter().average() is None


def test_batch_meter_window_evicts_old():
    m = BatchMeter(window=2)
    for v in (2, 4, 6):
        m.feed_line(f"batch={v}")
    assert m.average() == 5.0  # только последние два: (4+6)/2
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_batch_meter.py -q`
Expected: FAIL — ImportError.

- [ ] **Step 3: Реализовать**

```python
# app/gui_qt/telemetry/batch_meter.py
from __future__ import annotations

import re
from collections import deque
from typing import Optional

_BATCH_RE = re.compile(r"batch=(\d+)")


class BatchMeter:
    """Скользящее среднее размера батча inference-сервера из строк stdout."""

    def __init__(self, window: int = 30) -> None:
        self._vals: deque[int] = deque(maxlen=max(1, int(window)))

    def feed_line(self, line: str) -> None:
        m = _BATCH_RE.search(line or "")
        if m:
            self._vals.append(int(m.group(1)))

    def average(self) -> Optional[float]:
        if not self._vals:
            return None
        return sum(self._vals) / len(self._vals)

    def reset(self) -> None:
        self._vals.clear()
```

- [ ] **Step 4: Запустить — проходит**

Run: `python -m pytest tests/telemetry/test_batch_meter.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/telemetry/batch_meter.py tests/telemetry/test_batch_meter.py
git commit -m "feat: BatchMeter sliding-average of inference batch size"
```

---

### Task 4: LocalTelemetryProbe — снимок локального железа

**Files:**
- Create: `app/gui_qt/telemetry/local_probe.py`
- Create: `tests/telemetry/test_local_probe.py`

- [ ] **Step 1: Написать падающий тест (с фейковыми бэкендами через инъекцию)**

```python
# tests/telemetry/test_local_probe.py
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
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_local_probe.py -q`
Expected: FAIL — ImportError.

- [ ] **Step 3: Реализовать**

```python
# app/gui_qt/telemetry/local_probe.py
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
        proc_mem = self._gpu.process_memory_mb(child_pids or ({int(pid)} if pid else set()))
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
```

- [ ] **Step 4: Запустить — проходит**

Run: `python -m pytest tests/telemetry/test_local_probe.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/telemetry/local_probe.py tests/telemetry/test_local_probe.py
git commit -m "feat: LocalTelemetryProbe combines CPU/RAM and GPU samples"
```

---

### Task 5: Расширить health_check ПК2 (GPU-поля + средний батч)

**Files:**
- Modify: `tools/gmz_remote_inference_server.py` (`__init__` — счётчик батча; `_collect_batch`/`_process_and_reply` — учёт; `_handle_health_check` — GPU-поля)
- Create: `tests/telemetry/test_remote_health_payload.py`

- [ ] **Step 1: Написать падающий тест на сборку payload (чистая функция-хелпер)**

```python
# tests/telemetry/test_remote_health_payload.py
from tools.gmz_remote_inference_server import build_health_payload


def test_build_health_payload_includes_gpu_and_batch():
    payload = build_health_payload(
        protocol_version=1, policy_version=42, gpu_name="RTX 2060 SUPER",
        queue_depth=3, uptime_s=120, avg_batch=9.5,
        gpu_util=40, gpu_mem_used_mb=2048, gpu_mem_total_mb=8192, gpu_temp_c=55,
    )
    assert payload["kind"] == "health_check"
    assert payload["status"] == "ok"
    assert payload["gpu_util"] == 40
    assert payload["gpu_mem_used_mb"] == 2048
    assert payload["gpu_mem_total_mb"] == 8192
    assert payload["gpu_temp_c"] == 55
    assert payload["avg_batch"] == 9.5
    assert payload["policy_version"] == 42


def test_build_health_payload_tolerates_missing_gpu():
    payload = build_health_payload(
        protocol_version=1, policy_version=0, gpu_name="cpu",
        queue_depth=0, uptime_s=1, avg_batch=None,
        gpu_util=None, gpu_mem_used_mb=None, gpu_mem_total_mb=None, gpu_temp_c=None,
    )
    assert payload["status"] == "ok"
    assert payload["gpu_util"] is None
    assert payload["avg_batch"] is None
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_remote_health_payload.py -q`
Expected: FAIL — `ImportError: cannot import name 'build_health_payload'`.

- [ ] **Step 3: Реализовать — добавить хелпер + учёт батча + GPU в health_check**

В `tools/gmz_remote_inference_server.py` добавить функцию верхнего уровня (рядом с `_load_search_config`):

```python
def build_health_payload(
    *,
    protocol_version: int,
    policy_version: int,
    gpu_name: str,
    queue_depth: int,
    uptime_s: int,
    avg_batch,
    gpu_util,
    gpu_mem_used_mb,
    gpu_mem_total_mb,
    gpu_temp_c,
) -> dict:
    return {
        "kind": "health_check",
        "status": "ok",
        "protocol_version": int(protocol_version),
        "policy_version": int(policy_version),
        "gpu_name": str(gpu_name),
        "queue_depth": int(queue_depth),
        "uptime_s": int(uptime_s),
        "avg_batch": (None if avg_batch is None else float(avg_batch)),
        "gpu_util": gpu_util,
        "gpu_mem_used_mb": gpu_mem_used_mb,
        "gpu_mem_total_mb": gpu_mem_total_mb,
        "gpu_temp_c": gpu_temp_c,
    }
```

В `GMZRemoteInferenceServer.__init__` после создания `self._engine` добавить счётчики и GPU-бэкенд:

```python
        from collections import deque as _deque
        from core.telemetry.gpu_backend import GpuBackend

        self._batch_window: _deque = _deque(maxlen=30)
        self._gpu_backend = GpuBackend()
        self._gpu_index = 0
        if ":" in str(device):
            try:
                self._gpu_index = int(str(device).split(":")[-1])
            except ValueError:
                self._gpu_index = 0
```

В `_process_and_reply`, в начале (после `if not batch: return`), учитывать размер батча:

```python
        self._batch_window.append(len(batch))
```

Заменить тело `_handle_health_check` (формирование `resp`) на использование хелпера с реальными GPU-данными:

```python
    def _handle_health_check(self, identity: bytes, msg: dict[str, Any]) -> None:
        err = self._check_auth(msg) or self._check_protocol(msg)
        if err:
            self._send_error(identity, err)
            return
        avg_batch = (sum(self._batch_window) / len(self._batch_window)) if self._batch_window else None
        gpu_util = gpu_used = gpu_total = gpu_temp = None
        try:
            devices = self._gpu_backend.read_devices()
            for d in devices:
                if d.index == self._gpu_index:
                    gpu_util, gpu_used, gpu_total, gpu_temp = d.util, d.mem_used_mb, d.mem_total_mb, d.temp_c
                    break
        except Exception:
            pass
        resp = build_health_payload(
            protocol_version=PROTOCOL_VERSION,
            policy_version=int(self._engine.weight_version),
            gpu_name=str(self._gpu_name),
            queue_depth=int(self._queue_depth),
            uptime_s=int(time.time() - self._started_at),
            avg_batch=avg_batch,
            gpu_util=gpu_util, gpu_mem_used_mb=gpu_used,
            gpu_mem_total_mb=gpu_total, gpu_temp_c=gpu_temp,
        )
        self._router_send(self._router, identity, encode_message(resp))
```

(Новые ключи опциональны — старые клиенты их просто игнорируют; `PROTOCOL_VERSION` не меняем.)

- [ ] **Step 4: Запустить — проходит + регресс remote-сервера**

Run: `python -m pytest tests/telemetry/test_remote_health_payload.py tests/engine/test_gmz_remote_server.py -q`
Expected: PASS (все).

- [ ] **Step 5: Commit**

```bash
git add tools/gmz_remote_inference_server.py tests/telemetry/test_remote_health_payload.py
git commit -m "feat: PC2 health_check reports GPU util/mem/temp and avg batch"
```

---

### Task 6: RemoteTelemetryProbe — снимок ПК2 через health_check

**Files:**
- Create: `app/gui_qt/telemetry/remote_probe.py`
- Create: `tests/telemetry/test_remote_probe.py`

- [ ] **Step 1: Написать падающий тест (инъекция health-функции)**

```python
# tests/telemetry/test_remote_probe.py
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
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_remote_probe.py -q`
Expected: FAIL — ImportError.

- [ ] **Step 3: Реализовать**

```python
# app/gui_qt/telemetry/remote_probe.py
from __future__ import annotations

from typing import Any, Callable, Optional


class RemoteTelemetryProbe:
    def __init__(
        self, *, host: str, port: int, auth_token: str = "", timeout: float = 2.0,
        health_fn: Optional[Callable[..., dict]] = None,
    ) -> None:
        self.host = str(host)
        self.port = int(port)
        self.auth_token = str(auth_token or "")
        self.timeout = float(timeout)
        if health_fn is not None:
            self._health_fn = health_fn
        else:
            from core.models.gmz_inference_transport import remote_health_check

            self._health_fn = remote_health_check

    def sample(self) -> Optional[dict[str, Any]]:
        try:
            hc = self._health_fn(
                host=self.host, port=self.port,
                auth_token=self.auth_token, timeout=self.timeout,
            )
        except Exception:
            return None
        if not isinstance(hc, dict) or str(hc.get("status", "")).lower() != "ok":
            return None
        return {
            "name": str(hc.get("gpu_name", "remote GPU")),
            "util": hc.get("gpu_util"),
            "mem_used_mb": hc.get("gpu_mem_used_mb"),
            "mem_total_mb": hc.get("gpu_mem_total_mb"),
            "proc_mem_mb": hc.get("gpu_mem_used_mb") or 0,
            "temp_c": hc.get("gpu_temp_c"),
            "avg_batch": hc.get("avg_batch"),
            "queue_depth": hc.get("queue_depth"),
        }
```

- [ ] **Step 4: Запустить — проходит**

Run: `python -m pytest tests/telemetry/test_remote_probe.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/telemetry/remote_probe.py tests/telemetry/test_remote_probe.py
git commit -m "feat: RemoteTelemetryProbe maps PC2 health_check to telemetry card"
```

---

### Task 7: build_cards — чистая сборка карточек для QML

**Files:**
- Create: `app/gui_qt/telemetry/cards.py`
- Create: `tests/telemetry/test_cards.py`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/telemetry/test_cards.py
from app.gui_qt.telemetry.cards import build_cards


def _local():
    return {
        "cpu_pct": 58.0, "ram_pct": 42.0, "ram_gb": 11.2, "ok": True,
        "gpus": [{"index": 0, "name": "RTX 5060 Ti", "util": 81,
                  "mem_used_mb": 4096, "mem_total_mb": 16384,
                  "proc_mem_mb": 3500, "temp_c": 64}],
    }


def test_cards_local_only_gmz_active():
    cards = build_cards(local=_local(), remote=None, batch_avg=9.7,
                        batch_size_hint=10, algo="gumbel_muzero", active=True)
    ids = [c["id"] for c in cards]
    assert ids == ["gpu0", "cpu", "ram", "batch"]
    gpu = cards[0]
    assert gpu["pct"] == 81 and gpu["variant"] == "local"
    assert "16384" not in gpu["valueText"]  # value = util%, не память
    batch = cards[-1]
    assert batch["valueText"].startswith("9.7")


def test_cards_hide_batch_for_non_gmz():
    cards = build_cards(local=_local(), remote=None, batch_avg=None,
                        batch_size_hint=None, algo="dqn", active=True)
    assert "batch" not in [c["id"] for c in cards]


def test_cards_remote_inserted_after_local_gpus():
    remote = {"name": "RTX 2060 SUPER", "util": 40, "mem_used_mb": 2048,
              "mem_total_mb": 8192, "proc_mem_mb": 2048, "temp_c": 55, "avg_batch": 9.5}
    cards = build_cards(local=_local(), remote=remote, batch_avg=9.7,
                        batch_size_hint=10, algo="gumbel_muzero", active=True)
    ids = [c["id"] for c in cards]
    assert ids == ["gpu0", "pc2", "cpu", "ram", "batch"]
    assert cards[1]["variant"] == "remote"


def test_cards_idle_dashes_project_metrics():
    cards = build_cards(local=_local(), remote=None, batch_avg=None,
                        batch_size_hint=None, algo="gumbel_muzero", active=False)
    cpu = next(c for c in cards if c["id"] == "cpu")
    assert cpu["valueText"] == "—"
    assert cpu["pct"] == 0


def test_cards_high_util_warns():
    local = _local()
    local["gpus"][0]["util"] = 95
    cards = build_cards(local=local, remote=None, batch_avg=None,
                        batch_size_hint=None, algo="dqn", active=True)
    assert cards[0]["warn"] is True
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_cards.py -q`
Expected: FAIL — ImportError.

- [ ] **Step 3: Реализовать**

```python
# app/gui_qt/telemetry/cards.py
from __future__ import annotations

from typing import Any, Optional

COLOR_GPU = "#3fae6e"
COLOR_CPU = "#4a90d9"
COLOR_RAM = "#d9a441"
COLOR_TEMP = "#e06a4a"
COLOR_WARN = "#e0524a"
WARN_PCT = 90


def _gb(mb: Optional[int]) -> str:
    if not mb:
        return "0.0G"
    return f"{mb / 1024.0:.1f}G"


def _gpu_card(card_id: str, name: str, util, used_mb, total_mb, temp, variant: str, active: bool) -> dict[str, Any]:
    has = active and util is not None
    pct = int(util) if has else 0
    return {
        "id": card_id,
        "icon": "server" if variant == "remote" else "gpu",
        "label": name,
        "valueText": (f"{pct}%" if has else "—"),
        "sub": (f"{_gb(used_mb)}/{_gb(total_mb)}" + (f" · {temp}°" if temp is not None else "")) if active else "—",
        "pct": pct,
        "color": COLOR_WARN if (has and pct >= WARN_PCT) else COLOR_GPU,
        "warn": bool(has and pct >= WARN_PCT),
        "variant": variant,
    }


def build_cards(
    *, local: dict[str, Any], remote: Optional[dict[str, Any]],
    batch_avg: Optional[float], batch_size_hint: Optional[int],
    algo: str, active: bool,
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []

    for g in local.get("gpus", []):
        cards.append(_gpu_card(
            f"gpu{g['index']}", g.get("name", "GPU"), g.get("util"),
            g.get("mem_used_mb"), g.get("mem_total_mb"), g.get("temp_c"),
            variant="local", active=active,
        ))

    if remote is not None:
        cards.append(_gpu_card(
            "pc2", f"ПК2 · {remote.get('name', 'GPU')}", remote.get("util"),
            remote.get("mem_used_mb"), remote.get("mem_total_mb"), remote.get("temp_c"),
            variant="remote", active=active,
        ))

    cpu_pct = int(round(local.get("cpu_pct", 0.0))) if active else 0
    cards.append({
        "id": "cpu", "icon": "cpu", "label": "CPU",
        "valueText": (f"{cpu_pct}%" if active else "—"),
        "sub": "процесс", "pct": cpu_pct,
        "color": COLOR_WARN if (active and cpu_pct >= WARN_PCT) else COLOR_CPU,
        "warn": bool(active and cpu_pct >= WARN_PCT), "variant": "local",
    })

    ram_pct = int(round(local.get("ram_pct", 0.0))) if active else 0
    cards.append({
        "id": "ram", "icon": "ram", "label": "RAM",
        "valueText": (f"{ram_pct}%" if active else "—"),
        "sub": (f"{local.get('ram_gb', 0.0):.1f}G" if active else "—"), "pct": ram_pct,
        "color": COLOR_WARN if (active and ram_pct >= WARN_PCT) else COLOR_RAM,
        "warn": bool(active and ram_pct >= WARN_PCT), "variant": "local",
    })

    if str(algo).lower() == "gumbel_muzero":
        avg = remote.get("avg_batch") if (remote and remote.get("avg_batch") is not None) else batch_avg
        hint = int(batch_size_hint) if batch_size_hint else None
        if active and avg is not None:
            pct = int(min(100.0, (avg / hint) * 100.0)) if hint else 0
            vtext = f"{avg:.1f}" + (f"/{hint}" if hint else "")
        else:
            pct, vtext = 0, "—"
        cards.append({
            "id": "batch", "icon": "batch", "label": "Батч поиска",
            "valueText": vtext, "sub": "ср. размер", "pct": pct,
            "color": COLOR_GPU, "warn": False, "variant": "local",
        })

    return cards
```

- [ ] **Step 4: Запустить — проходит**

Run: `python -m pytest tests/telemetry/test_cards.py -q`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/telemetry/cards.py tests/telemetry/test_cards.py
git commit -m "feat: build_cards pure assembly of telemetry strip cards"
```

---

### Task 8: TelemetryController(QObject) — таймер, threadpool, свойство

**Files:**
- Create: `app/gui_qt/telemetry/controller.py`
- Create: `tests/telemetry/test_controller_smoke.py`

- [ ] **Step 1: Написать smoke-тест (без реального железа, инъекция проб)**

```python
# tests/telemetry/test_controller_smoke.py
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
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/telemetry/test_controller_smoke.py -q`
Expected: FAIL — ImportError.

- [ ] **Step 3: Реализовать**

```python
# app/gui_qt/telemetry/controller.py
from __future__ import annotations

from typing import Any, Optional

from PySide6 import QtCore

from app.gui_qt.telemetry.batch_meter import BatchMeter
from app.gui_qt.telemetry.cards import build_cards
from app.gui_qt.telemetry.local_probe import LocalTelemetryProbe
from app.gui_qt.telemetry.remote_probe import RemoteTelemetryProbe


class TelemetryController(QtCore.QObject):
    cardsChanged = QtCore.Signal()
    activeChanged = QtCore.Signal()

    def __init__(self, parent: Optional[QtCore.QObject] = None, local_probe: Any = None) -> None:
        super().__init__(parent)
        self._local = local_probe if local_probe is not None else LocalTelemetryProbe()
        self._batch = BatchMeter(window=30)
        self._cards: list[dict] = []
        self._active = False
        self._pid: Optional[int] = None
        self._algo = "dqn"
        self._remote_cfg: Optional[dict] = None
        self._batch_size_hint: Optional[int] = None
        self._pool = QtCore.QThreadPool.globalInstance()
        self._busy = False

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

    # --- QML-facing ---
    @QtCore.Property("QVariant", notify=cardsChanged)
    def cards(self) -> list:
        return self._cards

    @QtCore.Property(bool, notify=activeChanged)
    def active(self) -> bool:
        return self._active

    # --- lifecycle (вызывается GUIController) ---
    def set_context(self, *, pid: Optional[int], algo: str, active: bool,
                    remote_cfg: Optional[dict], batch_size_hint: Optional[int] = None) -> None:
        self._pid = pid
        self._algo = str(algo or "dqn")
        self._remote_cfg = remote_cfg
        self._batch_size_hint = batch_size_hint
        if active != self._active:
            self._active = active
            self.activeChanged.emit()

    def start(self) -> None:
        self._batch.reset()
        if not self._timer.isActive():
            self._timer.start()
        self._tick()

    def stop(self) -> None:
        self._timer.stop()

    def feed_log_line(self, line: str) -> None:
        self._batch.feed_line(line)

    # --- internals ---
    def _tick(self) -> None:
        if self._busy:
            return
        self._busy = True

        class _Job(QtCore.QRunnable):
            def __init__(self, outer): super().__init__(); self.outer = outer
            def run(self): self.outer._refresh_sync()

        self._pool.start(_Job(self))

    def _refresh_sync(self) -> None:
        try:
            local = self._local.sample(self._pid)
            remote = None
            if self._remote_cfg:
                remote = RemoteTelemetryProbe(
                    host=self._remote_cfg.get("host", "127.0.0.1"),
                    port=int(self._remote_cfg.get("port", 5555)),
                    auth_token=self._remote_cfg.get("auth_token", ""),
                ).sample()
            cards = build_cards(
                local=local, remote=remote, batch_avg=self._batch.average(),
                batch_size_hint=self._batch_size_hint, algo=self._algo, active=self._active,
            )
            self._cards = cards
            self.cardsChanged.emit()
        finally:
            self._busy = False
```

- [ ] **Step 4: Запустить — проходит**

Run: `python -m pytest tests/telemetry/test_controller_smoke.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/telemetry/controller.py tests/telemetry/test_controller_smoke.py
git commit -m "feat: TelemetryController QObject (timer, threadpool, cards property)"
```

---

### Task 9: Проводка в GUIController + QML-лента + зависимости

Это интеграционная задача — без юнит-теста, проверка ручным запуском приложения.

**Files:**
- Modify: `app/gui_qt/main.py` (создание контроллера, context property, start/stop, feed_line, set_context)
- Create: `app/gui_qt/qml/components/TelemetryStrip.qml`
- Modify: `app/gui_qt/qml/Main.qml` (вставка после прогресс-Item)
- Modify: `requirements.txt`

- [ ] **Step 1: Добавить зависимости**

В `requirements.txt` добавить строки:
```
psutil>=5.9
nvidia-ml-py>=12.535
```
Установить: `python -m pip install psutil nvidia-ml-py`

- [ ] **Step 2: Создать TelemetryController в GUIController и context property**

В `app/gui_qt/main.py`, в `GUIController.__init__` (рядом с `self._training_ui_timer`, ~строка 192) добавить:

```python
        from app.gui_qt.telemetry.controller import TelemetryController

        self._telemetry = TelemetryController(self)
```

В функции запуска QML (рядом со строкой 7212, где `setContextProperty("controller", ...)`) добавить:

```python
    engine.rootContext().setContextProperty("telemetry", _GUI_CONTROLLER_REF._telemetry)
```

- [ ] **Step 3: Завести телеметрию по жизненному циклу процесса**

В `_read_stdout` (строка ~4934, внутри цикла по строкам, после `self._handle_progress_line(line)`) добавить:
```python
                self._telemetry.feed_log_line(line)
```

В обоих местах старта процесса (после `self._process.start(...)` — строки ~4213 и ~4837) добавить установку контекста и старт. Для GMZ-пути (первый, ~4213):
```python
        self._telemetry.set_context(
            pid=self._process.processId() or None,
            algo=str(self._train_algo),
            active=True,
            remote_cfg=self._gmz_remote_cfg_for_telemetry(),
            batch_size_hint=self._gmz_batch_size_hint(),
        )
        self._telemetry.start()
```
Для второго пути (bat/остальные, ~4840) — то же, но `remote_cfg=None`, `batch_size_hint=None`.

Добавить два хелпера в `GUIController` (рядом, например, после `_read_stdout`):
```python
    def _gmz_remote_cfg_for_telemetry(self):
        try:
            from app.gui_qt.remote_is_store import load_remote_is, remote_is_lan_active
        except Exception:
            return None
        try:
            data = load_remote_is(self._repo_root)
            if not remote_is_lan_active(data):
                return None
            return {
                "host": data.get("host", "127.0.0.1"),
                "port": int(data.get("port", 5555)),
                "auth_token": data.get("auth_token", ""),
            }
        except Exception:
            return None

    def _gmz_batch_size_hint(self):
        try:
            from app.gui_qt.gmz_hyperparams_defaults import DEFAULT_GMZ_HYPERPARAMS
            return int(DEFAULT_GMZ_HYPERPARAMS.get("inference_batch_size", 10))
        except Exception:
            return None
```

(`load_remote_is`/`remote_is_lan_active` — реальное API из `app/gui_qt/remote_is_store.py`; ключи `host`/`port`/`auth_token`. `self._repo_root` уже есть в `GUIController`.)

В `_on_finished` (строка ~5112, рядом с `self._training_ui_timer.stop()`) добавить:
```python
        self._telemetry.stop()
        self._telemetry.set_context(pid=None, algo=str(getattr(self, "_train_algo", "dqn")),
                                    active=False, remote_cfg=None)
```

- [ ] **Step 4: Создать QML-компонент ленты**

```qml
// app/gui_qt/qml/components/TelemetryStrip.qml
import QtQuick
import QtQuick.Layouts

RowLayout {
    id: strip
    spacing: 8
    Layout.fillWidth: true
    visible: telemetry.cards.length > 0

    property color cardBg: "#0d1521"
    property color cardBorder: "#243650"
    property color pc2Border: "#3a6ea5"
    property color trackBg: "#16202f"
    property color textMain: "#e7edf5"
    property color textMuted: "#7d8ba0"

    Repeater {
        model: telemetry.cards
        delegate: Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 64
            radius: 6
            color: strip.cardBg
            border.width: 1
            border.color: modelData.variant === "remote" ? strip.pc2Border : strip.cardBorder

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 3

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 6
                    Rectangle {  // иконка-плейсхолдер (цветная точка по типу метрики)
                        width: 10; height: 10; radius: 5; color: modelData.color
                        Layout.alignment: Qt.AlignVCenter
                    }
                    Text {
                        Layout.fillWidth: true
                        text: modelData.label
                        color: strip.textMuted
                        font.pixelSize: 11
                        elide: Text.ElideRight
                    }
                    Text {
                        text: modelData.valueText
                        color: strip.textMain
                        font.pixelSize: 16
                        font.bold: true
                    }
                }

                Text {
                    text: modelData.sub
                    color: strip.textMuted
                    font.pixelSize: 10
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }

                Rectangle {  // прогресс-трек
                    Layout.fillWidth: true
                    height: 5
                    radius: 2.5
                    color: strip.trackBg
                    Rectangle {
                        height: parent.height
                        radius: 2.5
                        width: parent.width * Math.max(0, Math.min(100, modelData.pct)) / 100.0
                        color: modelData.color
                        Behavior on width { NumberAnimation { duration: 400; easing.type: Easing.OutCubic } }
                    }
                }
            }
        }
    }
}
```

> Иконки: на первом проходе — цветная точка по типу метрики (как выше). Финальные инлайн-SVG (видеокарта/чип/память/сервер/молния) добавляются на этапе визуальной доводки (browser), заменяя `Rectangle`-точку на `Image { source: "../icons/<name>.svg" }`.

- [ ] **Step 5: Вставить ленту в Main.qml после прогресс-бара**

В `app/gui_qt/qml/Main.qml`, после закрывающей `}` блока `Item { ... ProgressBar ... }` (строка 682) и **перед** `ChamferPanel { ... КОНТЕКСТ ТРЕНИРОВКИ` (строка 684) вставить:

```qml
                        Loader {
                            Layout.fillWidth: true
                            active: true
                            sourceComponent: TelemetryStrip {}
                        }
```

Убедиться, что `TelemetryStrip` доступен: компоненты из `qml/components/` уже подключаются в проекте (см. использование `GmzInferenceServerPanel`); если нужен импорт — добавить `import "components"` в начало `Main.qml` (проверить Grep `import "components"`; если уже есть — ничего не делать).

- [ ] **Step 6: Ручная проверка приложения**

Run: `python -m app.gui_qt.main` (или штатный лаунчер проекта).
Проверить глазами:
1. На «Главной» под прогресс-баром видна лента карточек.
2. В простое значения показывают «—», бар пустой.
3. Запустить тренировку DQN → карточки CPU/RAM/GPU0 оживают, батч-карточки НЕТ.
4. Запустить тренировку Gumbel MuZero (вариант B) → появляется карточка «Батч поиска».
5. При LAN remote IS (если поднят ПК2) → появляется синяя карточка «ПК2».
6. Значения обновляются ~раз в секунду, UI не подвисает.

Если что-то не так — отладка перед коммитом (UI-корректность тестами не проверяется).

- [ ] **Step 7: Прогнать весь telemetry-набор тестов на регресс**

Run: `python -m pytest tests/telemetry/ -q`
Expected: PASS (все юнит-тесты).

- [ ] **Step 8: Commit**

```bash
git add app/gui_qt/main.py app/gui_qt/qml/components/TelemetryStrip.qml app/gui_qt/qml/Main.qml requirements.txt
git commit -m "feat: wire telemetry strip into Главная page (QML + controller lifecycle)"
```

---

## Self-Review (выполнено автором плана)

**1. Spec coverage:**
- Размещение (лента под прогрессом) → Task 9 (Main.qml вставка). ✓
- GPU% карты + VRAM процесса → Task 2 (`read_devices` util device-wide; `process_memory_mb` per-pid) + Task 4. ✓
- CPU/RAM по процессу → Task 1. ✓
- ПК2 через health_check → Task 5 (сервер) + Task 6 (клиент). ✓
- Батч (локально из stdout; ПК2 из health_check) → Task 3 + Task 7 (`build_cards` берёт remote.avg_batch при наличии). ✓
- Поведение idle/активно, батч только для GMZ, карточка ПК2 только при remote → Task 7 (`build_cards`) + Task 9 (`set_context`). ✓
- Визуал (цвета, бары, рамка ПК2) → Task 7 (цвета) + Task 9 (QML). ✓
- Зависимости psutil/pynvml + fallback nvidia-smi → Task 9 (requirements) + Task 2 (fallback). ✓
- Ошибки → «N/A»/None во всех пробниках (Task 1/2/4/6), UI не падает. ✓
- Тесты → есть в Task 1-8. ✓

**2. Placeholder scan:** Код в Task 1-8 полный. В Task 9 одно ПРИМЕЧАНИЕ про точное имя функции в `remote_is_store.py` — это запрос на проверку реального API при интеграции (не выдуманный код), структура хелпера дана полностью. QML-иконки сознательно поэтапны (точка → SVG на доводке).

**3. Type consistency:** Ключи снапшота (`cpu_pct/ram_pct/ram_gb/ok/gpus[]` с `index/name/util/mem_used_mb/mem_total_mb/temp_c/proc_mem_mb`) согласованы между Task 2/4/7. Карточка (`id/icon/label/valueText/sub/pct/color/warn/variant`) согласована между Task 7 (`build_cards`) и Task 9 (QML `modelData.*`). Remote-снапшот (`name/util/mem_used_mb/mem_total_mb/proc_mem_mb/temp_c/avg_batch/queue_depth`) согласован между Task 6 и Task 7. `health_check` payload (`gpu_util/gpu_mem_used_mb/gpu_mem_total_mb/gpu_temp_c/avg_batch`) согласован между Task 5 (сервер) и Task 6 (клиент).
