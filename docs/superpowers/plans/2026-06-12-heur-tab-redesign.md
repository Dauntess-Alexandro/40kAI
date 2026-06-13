# Heur Tab Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Редизайн вкладки «Метрики эвристики» — три внутренних подвкладки (Сводка / Бенчмарк / Калибровка) с запуском Phase 8 инструментов прямо из GUI, живой таблицей кандидатов и применением патча весов.

**Architecture:** Два новых QObject-runner'а (`HeurBenchmarkRunner`, `HeurCalibrateRunner`) запускают `tools/heur_benchmark.py` и `tools/heur_calibrate.py` как subprocesses из `QThread`. `QTimer` на главном потоке опрашивает `candidates.jsonl` каждые 2 сек для live-обновлений. Новый QML-компонент `HeurMetricsPanel.qml` заменяет текущий `Item` во вкладке. Патч `reward_config.py` применяется Python-методом через regex.

**Tech Stack:** PySide6 (QObject, QThread, QTimer, Signal, Slot, Property), Python subprocess, QML TabBar + StackLayout + ListModel, JetBrains Mono theme.

---

## File Map

| Файл | Действие | Ответственность |
|------|----------|-----------------|
| `app/gui_qt/heur_benchmark_runner.py` | Создать | QObject runner для `heur_benchmark.py` |
| `app/gui_qt/heur_calibrate_runner.py` | Создать | QObject runner для `heur_calibrate.py` + apply patch |
| `app/gui_qt/qml/components/HeurMetricsPanel.qml` | Создать | Три подвкладки: Сводка/Бенчмарк/Калибровка |
| `app/gui_qt/main.py` | Изменить | Добавить `heuristicMetricsDict` property + зарегистрировать runners |
| `app/gui_qt/qml/Main.qml` | Изменить | Заменить Item строки 4195–4238 на `HeurMetricsPanel` |
| `tests/gui/test_heur_benchmark_runner.py` | Создать | Тест runner'а с mock subprocess |
| `tests/gui/test_heur_calibrate_runner.py` | Создать | Тест polling + apply_patch |

---

## Task 1: `heuristicMetricsDict` property в GUIController

**Files:**
- Modify: `app/gui_qt/main.py:145` (signals) и `main.py:269–270` (init) и `main.py:7037–7118` (_load_latest_heuristic_metrics) и `main.py:1077–1079` (property)
- Test: `tests/gui/test_heur_metrics_dict_property.py`

- [ ] **Шаг 1: написать падающий тест**

```python
# tests/gui/test_heur_metrics_dict_property.py
"""Контракт: GUIController выставляет heuristicMetricsDict как QVariantMap с нужными ключами."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestHeuristicMetricsDictProperty(unittest.TestCase):
    def _make_metrics_json(self, tmp_dir: str) -> str:
        data = {
            "run_id": "test_run",
            "updated_at": "2026-06-12T10:00:00",
            "train_heur_winrate": 0.503,
            "train_draw_rate": 0.012,
            "train_total_games": 100,
            "invalid_rate_total": 0.0,
            "avg_risk": 0.42,
            "avg_cover": 0.05,
            "charge_success_rate": 0.88,
            "shoot_overkill_rate": 0.01,
            "fallback_rate": 0.00,
            "style_entropy_norm": 0.889,
            "mode_usage": {"kite": 30, "hold": 50, "commit": 20},
            "role_usage": {"ranged": 80, "hybrid": 0, "melee": 20},
        }
        path = os.path.join(tmp_dir, "heur_metrics_latest.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def test_load_builds_flat_dict(self):
        from app.gui_qt.main import GUIController
        # Patch ARTIFACTS_METRICS_DIR so controller reads our file
        import app.gui_qt.main as m_mod
        with tempfile.TemporaryDirectory() as tmp:
            self._make_metrics_json(tmp)
            orig = m_mod.ARTIFACTS_METRICS_DIR
            try:
                m_mod.ARTIFACTS_METRICS_DIR = Path(tmp)
                # instantiate is heavy — test the helper method directly
                ctrl = object.__new__(GUIController)
                ctrl._heuristic_metrics = {}
                ctrl._heuristic_metrics_text = ""
                ctrl._heuristic_metrics_dict = {}
                # Monkey-patch emit so it doesn't crash
                ctrl.heuristicMetricsChanged = type("S", (), {"emit": lambda self: None})()
                m_mod.GUIController._load_latest_heuristic_metrics(ctrl)
                d = ctrl._heuristic_metrics_dict
                self.assertAlmostEqual(d["winrate"], 0.503, places=3)
                self.assertAlmostEqual(d["draw_rate"], 0.012, places=3)
                self.assertAlmostEqual(d["entropy"], 0.889, places=3)
                self.assertEqual(d["mode_kite"], 30)
                self.assertEqual(d["mode_hold"], 50)
                self.assertIn("run_id", d)
            finally:
                m_mod.ARTIFACTS_METRICS_DIR = orig


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Шаг 2: запустить тест — убедиться что падает**

```
python -m pytest tests/gui/test_heur_metrics_dict_property.py -v
```
Ожидается: `AttributeError: _heuristic_metrics_dict` или `KeyError`.

- [ ] **Шаг 3: реализация — добавить в `GUIController`**

В `main.py` в секции сигналов (после строки 145):
```python
heuristicMetricsDictChanged = QtCore.Signal()
```

В `__init__` (после строки 270):
```python
self._heuristic_metrics_dict: dict = {}
```

В конце метода `_load_latest_heuristic_metrics` (перед `self.heuristicMetricsChanged.emit()`), дополнить метод чтобы он собирал плоский словарь. Найти строку `self._heuristic_metrics_text = "\n".join(lines)` и добавить после неё:

```python
        mu = mode_usage  # уже вычислен выше в методе
        ru = role_usage  # уже вычислен выше
        self._heuristic_metrics_dict = {
            "winrate": float(self._heuristic_metrics.get("train_heur_winrate", 0.0)),
            "draw_rate": float(self._heuristic_metrics.get("train_draw_rate", 0.0)),
            "entropy": float(self._heuristic_metrics.get("style_entropy_norm", 0.0)),
            "total_games": int(self._heuristic_metrics.get("train_total_games", 0)),
            "avg_risk": float(self._heuristic_metrics.get("avg_risk", 0.0)),
            "avg_cover": float(self._heuristic_metrics.get("avg_cover", 0.0)),
            "charge_success_rate": float(self._heuristic_metrics.get("charge_success_rate", 0.0)),
            "shoot_overkill_rate": float(self._heuristic_metrics.get("shoot_overkill_rate", 0.0)),
            "fallback_rate": float(self._heuristic_metrics.get("fallback_rate", 0.0)),
            "invalid_rate": float(self._heuristic_metrics.get("invalid_rate_total", 0.0)),
            "mode_kite": int(mu.get("kite", 0)),
            "mode_hold": int(mu.get("hold", 0)),
            "mode_commit": int(mu.get("commit", 0)),
            "role_ranged": int(ru.get("ranged", 0)),
            "role_hybrid": int(ru.get("hybrid", 0)),
            "role_melee": int(ru.get("melee", 0)),
            "run_id": str(self._heuristic_metrics.get("run_id", "-")),
            "updated_at": str(self._heuristic_metrics.get("updated_at", "-")),
        }
        self.heuristicMetricsDictChanged.emit()
```

Добавить property после строки `def heuristicMetricsText`:
```python
    @QtCore.Property("QVariantMap", notify=heuristicMetricsDictChanged)
    def heuristicMetricsDict(self) -> dict:
        return self._heuristic_metrics_dict
```

В обоих `except`/early-return ветках `_load_latest_heuristic_metrics` добавить:
```python
self._heuristic_metrics_dict = {}
self.heuristicMetricsDictChanged.emit()
```

- [ ] **Шаг 4: запустить тест — убедиться что проходит**

```
python -m pytest tests/gui/test_heur_metrics_dict_property.py -v
```
Ожидается: `PASSED`.

- [ ] **Шаг 5: коммит**

```
git add app/gui_qt/main.py tests/gui/test_heur_metrics_dict_property.py
git commit -m "feat(gui): heuristicMetricsDict QVariantMap property в controller"
```

---

## Task 2: `HeurBenchmarkRunner`

**Files:**
- Create: `app/gui_qt/heur_benchmark_runner.py`
- Test: `tests/gui/test_heur_benchmark_runner.py`

- [ ] **Шаг 1: написать падающий тест**

```python
# tests/gui/test_heur_benchmark_runner.py
"""Контракт HeurBenchmarkRunner: signals, isRunning, stop."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestParseBenchmarkStdout(unittest.TestCase):
    def test_parses_json_block(self):
        from app.gui_qt.heur_benchmark_runner import _parse_benchmark_stdout
        stdout = (
            "[HEUR-BENCH] games=30 winrate_all=0.503\n"
            '{"games": 30, "heur_winrate_all": 0.503, "draw_rate": 0.02, '
            '"style_entropy_norm": 0.891, "heur_winrate": 0.503}\n'
        )
        result = _parse_benchmark_stdout(stdout)
        self.assertAlmostEqual(result["heur_winrate_all"], 0.503, places=3)
        self.assertAlmostEqual(result["style_entropy_norm"], 0.891, places=3)

    def test_fallback_to_heur_bench_line(self):
        from app.gui_qt.heur_benchmark_runner import _parse_benchmark_stdout
        stdout = "[HEUR-BENCH] games=20 winrate_all=0.480 draw_rate=0.015 style_entropy_norm=0.870\n"
        result = _parse_benchmark_stdout(stdout)
        self.assertAlmostEqual(result.get("winrate_all", result.get("heur_winrate_all", 0)), 0.480, places=2)

    def test_empty_returns_empty_dict(self):
        from app.gui_qt.heur_benchmark_runner import _parse_benchmark_stdout
        self.assertEqual(_parse_benchmark_stdout(""), {})


class TestHeurBenchmarkRunnerContract(unittest.TestCase):
    def test_module_importable(self):
        from app.gui_qt import heur_benchmark_runner  # noqa: F401

    def test_runner_has_required_signals(self):
        src = Path("app/gui_qt/heur_benchmark_runner.py").read_text(encoding="utf-8")
        self.assertIn("benchmarkStarted", src)
        self.assertIn("benchmarkFinished", src)
        self.assertIn("benchmarkFailed", src)
        self.assertIn("isRunningChanged", src)

    def test_runner_has_run_and_stop_slots(self):
        src = Path("app/gui_qt/heur_benchmark_runner.py").read_text(encoding="utf-8")
        self.assertIn("def run(", src)
        self.assertIn("def stop(", src)

    def test_runner_has_is_running_property(self):
        src = Path("app/gui_qt/heur_benchmark_runner.py").read_text(encoding="utf-8")
        self.assertIn("isRunning", src)
        self.assertIn("lastResult", src)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Шаг 2: запустить — убедиться что падает**

```
python -m pytest tests/gui/test_heur_benchmark_runner.py -v
```
Ожидается: `ModuleNotFoundError`.

- [ ] **Шаг 3: создать `app/gui_qt/heur_benchmark_runner.py`**

```python
# app/gui_qt/heur_benchmark_runner.py
"""QObject runner для heur_benchmark.py (Phase 8)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtCore import Property, Signal, Slot

_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])


def _parse_benchmark_stdout(stdout: str) -> dict:
    """Парсит вывод heur_benchmark.py. Пробует JSON-блок, fallback — [HEUR-BENCH] строка."""
    lines = (stdout or "").strip().splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("{"):
            try:
                return json.loads("\n".join(lines[i:]))
            except json.JSONDecodeError:
                pass
    result: dict = {}
    for line in lines:
        if "[HEUR-BENCH]" not in line:
            continue
        for token in line.split():
            if "=" in token:
                k, v = token.split("=", 1)
                try:
                    result[k] = float(v)
                except ValueError:
                    result[k] = v
    return result


class _BenchmarkWorker(QtCore.QThread):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, games: int, opponent_policy: str) -> None:
        super().__init__()
        self._games = games
        self._opponent_policy = opponent_policy
        self._proc: subprocess.Popen | None = None  # type: ignore[type-arg]

    def run(self) -> None:
        cmd = [
            sys.executable, "-u", "tools/heur_benchmark.py",
            "--games", str(self._games),
            "--opponent-policy", self._opponent_policy,
        ]
        try:
            self._proc = subprocess.Popen(
                cmd, capture_output=True, text=True, cwd=_PROJECT_ROOT
            )
            stdout, stderr = self._proc.communicate()
            if self._proc.returncode != 0:
                self.failed.emit(
                    f"heur_benchmark завершился с кодом {self._proc.returncode}. "
                    f"{stderr[:300]}"
                )
                return
            result = _parse_benchmark_stdout(stdout)
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))

    def stop(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()


class HeurBenchmarkRunner(QtCore.QObject):
    benchmarkStarted = Signal()
    benchmarkFinished = Signal("QVariantMap")
    benchmarkFailed = Signal(str)
    isRunningChanged = Signal(bool)

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._is_running = False
        self._last_result: dict = {}
        self._worker: _BenchmarkWorker | None = None

    @Property(bool, notify=isRunningChanged)
    def isRunning(self) -> bool:
        return self._is_running

    @Property("QVariantMap", notify=benchmarkFinished)
    def lastResult(self) -> dict:
        return self._last_result

    @Slot(int, str)
    def run(self, games: int, opponent_policy: str) -> None:
        if self._is_running:
            return
        self._worker = _BenchmarkWorker(int(games), str(opponent_policy))
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._set_running(True)
        self.benchmarkStarted.emit()
        self._worker.start()

    @Slot()
    def stop(self) -> None:
        if self._worker:
            self._worker.stop()

    def _set_running(self, val: bool) -> None:
        if self._is_running != val:
            self._is_running = val
            self.isRunningChanged.emit(val)

    def _on_finished(self, result: dict) -> None:
        self._last_result = result
        self._set_running(False)
        self.benchmarkFinished.emit(result)

    def _on_failed(self, error: str) -> None:
        self._set_running(False)
        self.benchmarkFailed.emit(error)
```

- [ ] **Шаг 4: запустить тест — убедиться что проходит**

```
python -m pytest tests/gui/test_heur_benchmark_runner.py -v
```
Ожидается: все `PASSED`.

- [ ] **Шаг 5: коммит**

```
git add app/gui_qt/heur_benchmark_runner.py tests/gui/test_heur_benchmark_runner.py
git commit -m "feat(gui): HeurBenchmarkRunner QObject для запуска Phase 8 бенчмарка"
```

---

## Task 3: `HeurCalibrateRunner` с `applyPatch`

**Files:**
- Create: `app/gui_qt/heur_calibrate_runner.py`
- Test: `tests/gui/test_heur_calibrate_runner.py`

- [ ] **Шаг 1: написать падающий тест**

```python
# tests/gui/test_heur_calibrate_runner.py
"""Контракт HeurCalibrateRunner: polling candidates.jsonl, applyPatch."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestApplyPatch(unittest.TestCase):
    """applyPatch парсит best_reward_config_patch.md и обновляет reward_config.py."""

    def _make_patch_md(self, tmp_dir: str) -> Path:
        content = (
            "# Phase 8 best reward_config patch\n\n"
            "baseline_score=0.812000\n"
            "candidate=7\n"
            "score=0.847000\n\n"
            "```python\n"
            "ENEMY_HEUR_RISK_W = 0.312000  # baseline 0.180000, delta +0.132000\n"
            "ENEMY_HEUR_OBJECTIVE_CONTROL_W = 0.501000  # baseline 0.420000, delta +0.081000\n"
            "```\n"
        )
        p = Path(tmp_dir) / "best_reward_config_patch.md"
        p.write_text(content, encoding="utf-8")
        return p

    def _make_reward_config(self, tmp_dir: str) -> Path:
        content = (
            "# reward_config.py\n"
            "ENEMY_HEUR_RISK_W = 0.18\n"
            "ENEMY_HEUR_OBJECTIVE_CONTROL_W = 0.42\n"
            "OTHER_PARAM = 1.0\n"
        )
        p = Path(tmp_dir) / "reward_config.py"
        p.write_text(content, encoding="utf-8")
        return p

    def test_apply_patch_updates_values(self):
        from app.gui_qt.heur_calibrate_runner import _apply_patch_to_reward_config
        with tempfile.TemporaryDirectory() as tmp:
            patch_md = self._make_patch_md(tmp)
            rc_path = self._make_reward_config(tmp)
            changed = _apply_patch_to_reward_config(str(patch_md), str(rc_path))
            result = rc_path.read_text(encoding="utf-8")
            self.assertIn("ENEMY_HEUR_RISK_W = 0.312000", result)
            self.assertIn("ENEMY_HEUR_OBJECTIVE_CONTROL_W = 0.501000", result)
            self.assertIn("OTHER_PARAM = 1.0", result)
            self.assertIn("ENEMY_HEUR_RISK_W", changed)
            self.assertIn("ENEMY_HEUR_OBJECTIVE_CONTROL_W", changed)

    def test_apply_patch_missing_file_raises(self):
        from app.gui_qt.heur_calibrate_runner import _apply_patch_to_reward_config
        with self.assertRaises(FileNotFoundError):
            _apply_patch_to_reward_config("/nonexistent/patch.md", "/nonexistent/rc.py")

    def test_apply_patch_no_python_block_raises(self):
        from app.gui_qt.heur_calibrate_runner import _apply_patch_to_reward_config
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "patch.md"
            p.write_text("no python block here\n", encoding="utf-8")
            rc = Path(tmp) / "reward_config.py"
            rc.write_text("X = 1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                _apply_patch_to_reward_config(str(p), str(rc))


class TestCalibrateRunnerContract(unittest.TestCase):
    def test_module_importable(self):
        from app.gui_qt import heur_calibrate_runner  # noqa: F401

    def test_runner_has_required_signals(self):
        src = Path("app/gui_qt/heur_calibrate_runner.py").read_text(encoding="utf-8")
        for sig in ["calibrationStarted", "candidateResult", "calibrationFinished",
                    "calibrationFailed", "progressChanged", "patchApplied", "patchFailed"]:
            self.assertIn(sig, src, f"Сигнал {sig} не найден")

    def test_runner_has_slots(self):
        src = Path("app/gui_qt/heur_calibrate_runner.py").read_text(encoding="utf-8")
        for name in ["def run(", "def stop(", "def applyPatch("]:
            self.assertIn(name, src, f"Слот {name} не найден")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Шаг 2: запустить — убедиться что падает**

```
python -m pytest tests/gui/test_heur_calibrate_runner.py -v
```
Ожидается: `ModuleNotFoundError`.

- [ ] **Шаг 3: создать `app/gui_qt/heur_calibrate_runner.py`**

```python
# app/gui_qt/heur_calibrate_runner.py
"""QObject runner для heur_calibrate.py (Phase 8 random-search калибровка)."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtCore import Property, QTimer, Signal, Slot

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_REWARD_CONFIG_PATH = _PROJECT_ROOT / "reward_config.py"


def _apply_patch_to_reward_config(patch_md_path: str, reward_config_path: str) -> list[str]:
    """Читает python-блок из patch .md и regex-патчит reward_config.py.

    Возвращает список изменённых ключей.
    Raises FileNotFoundError если файл не найден.
    Raises ValueError если python-блок не найден в патч-файле.
    """
    md = Path(patch_md_path)
    if not md.exists():
        raise FileNotFoundError(f"Патч-файл не найден: {patch_md_path}")
    content = md.read_text(encoding="utf-8")
    m = re.search(r"```python\n(.*?)```", content, re.DOTALL)
    if not m:
        raise ValueError(f"Блок ```python не найден в {patch_md_path}")

    rc_path = Path(reward_config_path)
    rc_text = rc_path.read_text(encoding="utf-8")
    changed: list[str] = []

    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m2 = re.match(r"^(\w+)\s*=\s*([\d.eE+\-]+)", stripped)
        if not m2:
            continue
        key, value = m2.group(1), m2.group(2)
        pattern = rf"^({re.escape(key)}\s*=\s*)[\d.eE+\-]+([ \t]*.*)$"
        new_text, n = re.subn(pattern, rf"\g<1>{value}\2", rc_text, flags=re.MULTILINE)
        if n > 0:
            rc_text = new_text
            changed.append(key)

    rc_path.write_text(rc_text, encoding="utf-8")
    return changed


class _CalibrateWorker(QtCore.QThread):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, candidates: int, games: int, seed: int, dry_run: bool, run_id: str) -> None:
        super().__init__()
        self._candidates = candidates
        self._games = games
        self._seed = seed
        self._dry_run = dry_run
        self._run_id = run_id
        self._proc: subprocess.Popen | None = None  # type: ignore[type-arg]

    def run(self) -> None:
        cmd = [
            sys.executable, "-u", "tools/heur_calibrate.py",
            "--candidates", str(self._candidates),
            "--games", str(self._games),
            "--seed", str(self._seed),
            "--run-id", self._run_id,
        ]
        if self._dry_run:
            cmd.append("--dry-run")
        try:
            self._proc = subprocess.Popen(
                cmd, capture_output=True, text=True, cwd=str(_PROJECT_ROOT)
            )
            _, stderr = self._proc.communicate()
            if self._proc.returncode != 0:
                self.failed.emit(
                    f"heur_calibrate завершился с кодом {self._proc.returncode}. {stderr[:300]}"
                )
                return
            summary_path = (
                _PROJECT_ROOT / "artifacts" / "metrics" / "heur_calibration"
                / self._run_id / "summary.json"
            )
            summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
            self.finished.emit(summary)
        except Exception as exc:
            self.failed.emit(str(exc))

    def stop(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()


class HeurCalibrateRunner(QtCore.QObject):
    calibrationStarted = Signal(str)
    candidateResult = Signal("QVariantMap")
    calibrationFinished = Signal("QVariantMap")
    calibrationFailed = Signal(str)
    progressChanged = Signal(int, int)
    patchApplied = Signal("QStringList")
    patchFailed = Signal(str)
    isRunningChanged = Signal(bool)

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._is_running = False
        self._worker: _CalibrateWorker | None = None
        self._timer = QTimer(self)
        self._timer.setInterval(2000)
        self._timer.timeout.connect(self._poll_candidates)
        self._candidates_path = ""
        self._seen: int = 0
        self._total: int = 0
        self._run_dir = ""

    @Property(bool, notify=isRunningChanged)
    def isRunning(self) -> bool:
        return self._is_running

    @Property(str, notify=calibrationStarted)
    def currentRunDir(self) -> str:
        return self._run_dir

    @Slot(int, int, int, bool)
    def run(self, candidates: int, games: int, seed: int, dry_run: bool) -> None:
        if self._is_running:
            return
        run_id = f"gui_{time.strftime('%Y%m%d_%H%M%S')}"
        self._run_dir = str(
            _PROJECT_ROOT / "artifacts" / "metrics" / "heur_calibration" / run_id
        )
        self._candidates_path = str(Path(self._run_dir) / "candidates.jsonl")
        self._seen = 0
        self._total = int(candidates)

        self._worker = _CalibrateWorker(int(candidates), int(games), int(seed), bool(dry_run), run_id)
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._set_running(True)
        self.calibrationStarted.emit(run_id)
        self._worker.start()
        self._timer.start()

    @Slot()
    def stop(self) -> None:
        if self._worker:
            self._worker.stop()
        self._timer.stop()
        self._set_running(False)

    @Slot(str)
    def applyPatch(self, run_dir: str) -> None:
        patch_md = str(Path(run_dir) / "best_reward_config_patch.md")
        try:
            changed = _apply_patch_to_reward_config(patch_md, str(_REWARD_CONFIG_PATH))
            self.patchApplied.emit(changed)
        except (FileNotFoundError, ValueError, OSError) as exc:
            self.patchFailed.emit(str(exc))

    def _poll_candidates(self) -> None:
        if not os.path.exists(self._candidates_path):
            return
        try:
            with open(self._candidates_path, encoding="utf-8") as f:
                lines = f.readlines()
        except OSError:
            return
        for line in lines[self._seen:]:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
                self.candidateResult.emit(row)
                self._seen += 1
                self.progressChanged.emit(self._seen, self._total)
            except json.JSONDecodeError:
                pass

    def _on_finished(self, summary: dict) -> None:
        self._poll_candidates()
        self._timer.stop()
        self._set_running(False)
        self.calibrationFinished.emit(summary)

    def _on_failed(self, error: str) -> None:
        self._timer.stop()
        self._set_running(False)
        self.calibrationFailed.emit(error)

    def _set_running(self, val: bool) -> None:
        if self._is_running != val:
            self._is_running = val
            self.isRunningChanged.emit(val)
```

- [ ] **Шаг 4: запустить тест**

```
python -m pytest tests/gui/test_heur_calibrate_runner.py -v
```
Ожидается: все `PASSED`.

- [ ] **Шаг 5: коммит**

```
git add app/gui_qt/heur_calibrate_runner.py tests/gui/test_heur_calibrate_runner.py
git commit -m "feat(gui): HeurCalibrateRunner с live-polling и applyPatch"
```

---

## Task 4: Зарегистрировать runners в `main.py`

**Files:**
- Modify: `app/gui_qt/main.py:8231–8249`

- [ ] **Шаг 1: добавить импорты в начало `main.py`** (после существующих `from app.gui_qt.*` импортов)

```python
from app.gui_qt.heur_benchmark_runner import HeurBenchmarkRunner
from app.gui_qt.heur_calibrate_runner import HeurCalibrateRunner
```

- [ ] **Шаг 2: создать и зарегистрировать runners** (после строки `engine.rootContext().setContextProperty("telemetry", ...)`)

```python
    _heur_bench_runner = HeurBenchmarkRunner()
    _heur_cal_runner = HeurCalibrateRunner()
    QtQml.QQmlEngine.setObjectOwnership(_heur_bench_runner, ownership)
    QtQml.QQmlEngine.setObjectOwnership(_heur_cal_runner, ownership)
    app._heur_bench_runner_ref = _heur_bench_runner
    app._heur_cal_runner_ref = _heur_cal_runner
    engine.rootContext().setContextProperty("heurBenchRunner", _heur_bench_runner)
    engine.rootContext().setContextProperty("heurCalRunner", _heur_cal_runner)
```

- [ ] **Шаг 3: быстрая проверка — GUI запускается без ошибок**

```
python app/gui_qt/main.py
```
Открыть GUI, убедиться что нет `AttributeError`/`ImportError` в консоли. Закрыть.

- [ ] **Шаг 4: коммит**

```
git add app/gui_qt/main.py
git commit -m "feat(gui): регистрация HeurBenchmarkRunner и HeurCalibrateRunner в QML контексте"
```

---

## Task 5: `HeurMetricsPanel.qml` — Сводка + Бенчмарк вкладки

**Files:**
- Create: `app/gui_qt/qml/components/HeurMetricsPanel.qml`
- Test: `tests/gui/test_heur_metrics_panel_contract.py`

- [ ] **Шаг 1: написать контрактный тест**

```python
# tests/gui/test_heur_metrics_panel_contract.py
"""Контракт HeurMetricsPanel.qml: структура, API, подключение к runners."""
import unittest
from pathlib import Path

QML_PATH = Path("app/gui_qt/qml/components/HeurMetricsPanel.qml")


class TestHeurMetricsPanelContract(unittest.TestCase):
    def setUp(self):
        self.assertTrue(QML_PATH.exists(), f"Нет компонента: {QML_PATH}")
        self.src = QML_PATH.read_text(encoding="utf-8")

    def test_has_three_subtabs(self):
        self.assertIn("Сводка", self.src)
        self.assertIn("Бенчмарк", self.src)
        self.assertIn("Калибровка", self.src)

    def test_uses_stacklayout(self):
        self.assertIn("StackLayout", self.src)

    def test_references_heur_bench_runner(self):
        self.assertIn("heurBenchRunner", self.src)

    def test_references_heur_cal_runner(self):
        self.assertIn("heurCalRunner", self.src)

    def test_references_heuristic_metrics_dict(self):
        self.assertIn("heuristicMetricsDict", self.src)

    def test_benchmark_has_run_and_stop(self):
        self.assertIn("heurBenchRunner.run(", self.src)
        self.assertIn("heurBenchRunner.stop(", self.src)

    def test_calibration_has_run_stop_apply(self):
        self.assertIn("heurCalRunner.run(", self.src)
        self.assertIn("heurCalRunner.stop(", self.src)
        self.assertIn("heurCalRunner.applyPatch(", self.src)

    def test_candidate_list_model(self):
        self.assertIn("ListModel", self.src)
        self.assertIn("candidateResult", self.src)

    def test_patch_block_visible_condition(self):
        # Патч-блок показывается только когда есть лучший кандидат
        self.assertIn("bestCandidateIdx", self.src)

    def test_stat_cards_winrate_entropy_draws(self):
        for metric in ["winrate", "entropy", "draw_rate"]:
            self.assertIn(metric, self.src)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Шаг 2: запустить — убедиться что падает**

```
python -m pytest tests/gui/test_heur_metrics_panel_contract.py -v
```
Ожидается: `AssertionError: Нет компонента`.

- [ ] **Шаг 3: создать `HeurMetricsPanel.qml`**

```qml
// app/gui_qt/qml/components/HeurMetricsPanel.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: heurPanel

    // ── состояние бенчмарка ──────────────────────────────────────────────
    property string benchStatusText: "Нет данных."
    property bool   benchHasError:   false
    property var    benchHistory:     []   // последние 5 прогонов {time, winrate, entropy, draws, games}

    // ── состояние калибровки ─────────────────────────────────────────────
    property int    calDone:          0
    property int    calTotal:         40
    property int    bestCandidateIdx: -1
    property real   bestScore:        0.0
    property string currentRunDir:    ""
    property string patchText:        ""   // diff-строки для показа

    // ── helpers ──────────────────────────────────────────────────────────
    function _colorForValue(val, good, warn) {
        if (val >= good)  return "#4caf6e"
        if (val >= warn)  return "#b88a26"
        return "#cf3f3f"
    }
    function _fmt(val, dec) {
        if (val === undefined || val === null) return "—"
        return Number(val).toFixed(dec !== undefined ? dec : 3)
    }

    // ── сигналы runners ──────────────────────────────────────────────────
    Connections {
        target: heurBenchRunner
        function onBenchmarkFinished(result) {
            var w  = _fmt(result.heur_winrate || result.heur_winrate_all, 3)
            var e  = _fmt(result.style_entropy_norm, 3)
            var dr = _fmt((result.draw_rate || 0) * 100, 1)
            benchStatusText = "winrate=" + w + "  entropy=" + e + "  draws=" + dr + "%"
            benchHasError   = false
            var now = Qt.formatDateTime(new Date(), "dd.MM hh:mm")
            if (benchHistory.length >= 5) benchHistory.splice(0, 1)
            benchHistory.push({time: now, winrate: w, entropy: e, draws: dr + "%", games: result.games || 0})
            benchHistoryModel.clear()
            for (var i = benchHistory.length - 1; i >= 0; i--) {
                benchHistoryModel.append(benchHistory[i])
            }
        }
        function onBenchmarkFailed(error) {
            benchStatusText = "Ошибка: " + error
            benchHasError   = true
        }
    }

    Connections {
        target: heurCalRunner
        function onCandidateResult(row) {
            var status = row.status || "…"
            var reasons = (row.reject_reasons || []).join(", ")
            var isBest = false
            var score = row.score !== undefined && row.score !== null ? row.score : -1
            if (status === "ok" && score > heurPanel.bestScore) {
                heurPanel.bestScore = score
                heurPanel.bestCandidateIdx = row.candidate_idx || 0
                // Обновляем флаг isBest у предыдущего лучшего
                for (var i = 0; i < candidatesModel.count; i++) {
                    candidatesModel.setProperty(i, "isBest", false)
                }
                isBest = true
            }
            candidatesModel.append({
                idx:      "" + (row.candidate_idx !== undefined ? row.candidate_idx : "?"),
                score:    score >= 0 ? _fmt(score, 3) : "…",
                winrate:  _fmt(row.heur_winrate, 3),
                entropy:  _fmt(row.style_entropy_norm, 3),
                draws:    row.draw_rate !== undefined ? _fmt(row.draw_rate * 100, 1) + "%" : "…",
                status:   status,
                reason:   reasons,
                isBest:   isBest
            })
        }
        function onCalibrationFinished(summary) {
            heurPanel.currentRunDir = summary.run_dir || heurCalRunner.currentRunDir
            // Читаем патч
            var idx = summary.best_candidate_idx
            if (idx !== null && idx !== undefined) {
                heurPanel.bestCandidateIdx = idx
                patchText = "Кандидат #" + idx + " · score=" + _fmt(summary.baseline_score, 3) +
                            " → " + _fmt(heurPanel.bestScore, 3)
            }
        }
        function onCalibrationFailed(error) {
            benchStatusText = "Калибровка: ошибка — " + error
        }
        function onPatchApplied(keys) {
            patchStatusText.text = "✓ Применено: " + keys.join(", ")
            patchStatusText.color = "#4caf6e"
        }
        function onPatchFailed(error) {
            patchStatusText.text = "Ошибка патча: " + error
            patchStatusText.color = "#cf3f3f"
        }
    }

    // ════════════════════════════════════════════════════════════════════
    //  Layout
    // ════════════════════════════════════════════════════════════════════
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: root.spacingLg
        spacing: 0

        // Заголовок
        Text {
            text: "Метрики эвристики"
            font.pixelSize: Math.round(20 * root.uiScale)
            font.bold: true
            color: root.textPrimary
        }
        Text {
            text: "ENEMY heuristic · Сводка, бенчмарк и калибровка весов"
            font.pixelSize: root.evalCaptionSize
            color: root.textSecondary
            Layout.bottomMargin: root.spacingMd
        }

        // ── подвкладки ───────────────────────────────────────────────────
        TabBar {
            id: innerTabs
            Layout.fillWidth: true
            background: Rectangle { color: root.bgSurface; border.width: 0 }
            TabButton {
                text: "Сводка"
                font.pixelSize: root.evalCaptionSize
                background: Rectangle {
                    color: innerTabs.currentIndex === 0 ? root.bgElevated : "transparent"
                    border.width: 0
                    Rectangle {
                        anchors.bottom: parent.bottom; width: parent.width; height: 2
                        color: innerTabs.currentIndex === 0 ? root.accentPrimaryAction : "transparent"
                    }
                }
                contentItem: Text {
                    text: parent.text; color: innerTabs.currentIndex === 0 ? root.textPrimary : root.textSecondary
                    font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }
            }
            TabButton {
                text: "Бенчмарк"
                font.pixelSize: root.evalCaptionSize
                background: Rectangle {
                    color: innerTabs.currentIndex === 1 ? root.bgElevated : "transparent"
                    border.width: 0
                    Rectangle {
                        anchors.bottom: parent.bottom; width: parent.width; height: 2
                        color: innerTabs.currentIndex === 1 ? root.accentP1 : "transparent"
                    }
                }
                contentItem: Text {
                    text: parent.text; color: innerTabs.currentIndex === 1 ? root.textPrimary : root.textSecondary
                    font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }
            }
            TabButton {
                text: "Калибровка"
                font.pixelSize: root.evalCaptionSize
                background: Rectangle {
                    color: innerTabs.currentIndex === 2 ? root.bgElevated : "transparent"
                    border.width: 0
                    Rectangle {
                        anchors.bottom: parent.bottom; width: parent.width; height: 2
                        color: innerTabs.currentIndex === 2 ? root.accentP1 : "transparent"
                    }
                }
                contentItem: Text {
                    text: parent.text; color: innerTabs.currentIndex === 2 ? root.textPrimary : root.textSecondary
                    font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }
            }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: root.borderMuted }

        StackLayout {
            id: innerStack
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: innerTabs.currentIndex

            // ══════════════════════════════════════
            // ВКЛАДКА 0: СВОДКА
            // ══════════════════════════════════════
            ScrollView {
                clip: true
                Column {
                    width: innerStack.width
                    spacing: root.spacingMd
                    topPadding: root.spacingMd

                    // Stat-карточки
                    Row {
                        spacing: root.spacingSm
                        width: parent.width

                        Repeater {
                            model: [
                                { label: "Winrate",        key: "winrate",    good: 0.46, warn: 0.40 },
                                { label: "Entropy (стили)",key: "entropy",    good: 0.86, warn: 0.80 },
                                { label: "Draw rate %",    key: "draw_rate",  good: 0,    warn: 0     },
                            ]
                            delegate: Rectangle {
                                width: (innerStack.width - 2 * root.spacingSm) / 3
                                height: Math.round(60 * root.uiScale)
                                color: root.bgElevated
                                border.color: root.borderMuted
                                border.width: 1
                                radius: 2

                                property real rawVal: {
                                    var d = controller.heuristicMetricsDict
                                    if (!d) return 0
                                    var v = d[modelData.key]
                                    return v !== undefined ? (modelData.key === "draw_rate" ? v * 100 : v) : 0
                                }
                                property string displayVal: modelData.key === "draw_rate"
                                    ? _fmt(rawVal, 1) + "%"
                                    : _fmt(rawVal, 3)
                                property color valColor: {
                                    if (modelData.key === "draw_rate")
                                        return rawVal < 3.0 ? "#4caf6e" : rawVal < 5.0 ? "#b88a26" : "#cf3f3f"
                                    return _colorForValue(rawVal, modelData.good, modelData.warn)
                                }

                                Column {
                                    anchors.centerIn: parent
                                    spacing: 2
                                    Text {
                                        text: displayVal
                                        font.pixelSize: Math.round(20 * root.uiScale)
                                        font.bold: true
                                        color: valColor
                                        anchors.horizontalCenter: parent.horizontalCenter
                                    }
                                    Text {
                                        text: modelData.label.toUpperCase()
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                        color: root.textSecondary
                                        font.letterSpacing: 0.8
                                        anchors.horizontalCenter: parent.horizontalCenter
                                    }
                                }
                            }
                        }
                    }

                    // Детальные метрики
                    GroupBox {
                        width: parent.width
                        title: "Показатели"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        property var md: controller.heuristicMetricsDict || {}

                        Grid {
                            columns: 2
                            columnSpacing: Math.round(24 * root.uiScale)
                            rowSpacing: Math.round(3 * root.uiScale)

                            Repeater {
                                model: [
                                    ["Ран",          String(parent.parent.md.run_id || "—")],
                                    ["Обновлено",    String(parent.parent.md.updated_at || "—")],
                                    ["Всего игр",    String(parent.parent.md.total_games || 0)],
                                    ["Invalid rate", _fmt(parent.parent.md.invalid_rate, 4)],
                                    ["Avg risk",     _fmt(parent.parent.md.avg_risk, 3)],
                                    ["Avg cover",    _fmt(parent.parent.md.avg_cover, 3)],
                                    ["Charge succ.", _fmt(parent.parent.md.charge_success_rate, 3)],
                                    ["Shoot overkill",_fmt(parent.parent.md.shoot_overkill_rate, 3)],
                                    ["Fallback rate",_fmt(parent.parent.md.fallback_rate, 3)],
                                    ["Mode kite",    String(parent.parent.md.mode_kite || 0)],
                                    ["Mode hold",    String(parent.parent.md.mode_hold || 0)],
                                    ["Mode commit",  String(parent.parent.md.mode_commit || 0)],
                                    ["Role ranged",  String(parent.parent.md.role_ranged || 0)],
                                    ["Role hybrid",  String(parent.parent.md.role_hybrid || 0)],
                                    ["Role melee",   String(parent.parent.md.role_melee || 0)],
                                ]
                                delegate: Row {
                                    spacing: root.spacingSm
                                    Text { text: modelData[0] + ":"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize; width: Math.round(110 * root.uiScale) }
                                    Text { text: modelData[1]; color: root.textPrimary;    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono" }
                                }
                            }
                        }
                    }

                    // Текстовый резерв (старый heuristicMetricsText, например профили)
                    GroupBox {
                        width: parent.width
                        title: "Сводный отчёт"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }
                        TextArea {
                            width: parent.width
                            height: Math.round(160 * root.uiScale)
                            text: controller.heuristicMetricsText
                            readOnly: true
                            wrapMode: Text.WordWrap
                            selectByMouse: true
                            color: root.textSecondary
                            font.pixelSize: root.evalCaptionSize
                            font.family: "JetBrains Mono"
                            background: Rectangle { color: root.bgSurface }
                        }
                    }
                }
            }

            // ══════════════════════════════════════
            // ВКЛАДКА 1: БЕНЧМАРК
            // ══════════════════════════════════════
            ScrollView {
                clip: true
                Column {
                    width: innerStack.width
                    spacing: root.spacingMd
                    topPadding: root.spacingMd

                    GroupBox {
                        width: parent.width
                        title: "Параметры"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        RowLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            Text { text: "Игр:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                            TextField {
                                id: benchGamesInput
                                text: "30"
                                validator: IntValidator { bottom: 1; top: 9999 }
                                font.pixelSize: root.evalCaptionSize
                                font.family: "JetBrains Mono"
                                color: root.textPrimary
                                background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                implicitWidth: Math.round(60 * root.uiScale)
                                enabled: !heurBenchRunner.isRunning
                            }

                            Text { text: "Оппонент:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                            ComboBox {
                                id: benchPolicyCombo
                                model: ["heuristic_auto"]
                                font.pixelSize: root.evalCaptionSize
                                enabled: !heurBenchRunner.isRunning
                                implicitWidth: Math.round(150 * root.uiScale)
                                contentItem: Text {
                                    text: benchPolicyCombo.displayText
                                    color: root.textPrimary
                                    font: benchPolicyCombo.font
                                    verticalAlignment: Text.AlignVCenter
                                    leftPadding: root.spacingSm
                                }
                                background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                            }

                            Item { Layout.fillWidth: true }

                            Button {
                                visible: !heurBenchRunner.isRunning
                                text: "▶ Запустить бенчмарк"
                                font.pixelSize: root.evalCaptionSize
                                onClicked: heurBenchRunner.run(parseInt(benchGamesInput.text), benchPolicyCombo.currentText)
                                contentItem: Text { text: parent.text; color: "#7db4f5"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                background: Rectangle { color: parent.down ? "#0a1525" : "#0e1f3a"; border.color: parent.hovered ? "#5090d0" : "#2f6ed8"; border.width: 1 }
                            }
                            Button {
                                visible: heurBenchRunner.isRunning
                                text: "■ Стоп"
                                font.pixelSize: root.evalCaptionSize
                                onClicked: heurBenchRunner.stop()
                                contentItem: Text { text: parent.text; color: "#c05050"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                background: Rectangle { color: "#1a0c0c"; border.color: "#6b2020"; border.width: 1 }
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        title: "Результат"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ColumnLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            Rectangle {
                                Layout.fillWidth: true
                                height: Math.round(28 * root.uiScale)
                                color: root.bgSurface
                                border.color: heurPanel.benchHasError ? "#6b2020" : root.borderMuted
                                border.width: 1
                                Text {
                                    anchors.fill: parent; anchors.leftMargin: root.spacingSm
                                    text: heurBenchRunner.isRunning ? "Запущен…" : heurPanel.benchStatusText
                                    color: heurPanel.benchHasError ? "#cf3f3f" : root.textSecondary
                                    font.pixelSize: root.evalCaptionSize
                                    font.family: "JetBrains Mono"
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        title: "История прогонов"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ListModel { id: benchHistoryModel }

                        Column {
                            width: parent.width
                            spacing: 0

                            // Заголовок
                            Row {
                                width: parent.width
                                height: Math.round(20 * root.uiScale)
                                Rectangle { width: parent.width; height: parent.height; color: root.bgSurface }
                                Repeater {
                                    model: ["Время", "Winrate", "Entropy", "Draws", "Игр"]
                                    delegate: Text {
                                        text: modelData; color: root.textSecondary
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                        width: [100, 70, 70, 60, 50][index] * root.uiScale
                                        leftPadding: root.spacingSm
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }
                            }

                            Repeater {
                                model: benchHistoryModel
                                delegate: Row {
                                    width: parent.width
                                    height: Math.round(22 * root.uiScale)
                                    Rectangle { width: parent.width; height: parent.height; color: index % 2 === 0 ? root.bgElevated : root.bgSurface; z: -1 }
                                    Repeater {
                                        model: [model.time, model.winrate, model.entropy, model.draws, String(model.games)]
                                        delegate: Text {
                                            text: modelData; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize
                                            font.family: "JetBrains Mono"
                                            width: [100, 70, 70, 60, 50][index] * root.uiScale
                                            leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                }
                            }

                            Text {
                                visible: benchHistoryModel.count === 0
                                text: "Нет прогонов в этой сессии."
                                color: root.textSecondary
                                font.pixelSize: root.evalCaptionSize
                                leftPadding: root.spacingSm
                                topPadding: root.spacingSm
                            }
                        }
                    }
                }
            }

            // ══════════════════════════════════════
            // ВКЛАДКА 2: КАЛИБРОВКА
            // ══════════════════════════════════════
            ScrollView {
                clip: true
                Column {
                    width: innerStack.width
                    spacing: root.spacingMd
                    topPadding: root.spacingMd

                    // Параметры + кнопки
                    GroupBox {
                        width: parent.width
                        title: "Параметры"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ColumnLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Text { text: "Кандидатов:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calCandidatesInput; text: "40"
                                    validator: IntValidator { bottom: 1; top: 999 }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(55 * root.uiScale)
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Text { text: "Игр/кандидат:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calGamesInput; text: "50"
                                    validator: IntValidator { bottom: 1; top: 9999 }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(55 * root.uiScale)
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Text { text: "Seed:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calSeedInput; text: "1390520"
                                    validator: IntValidator { bottom: 0 }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(75 * root.uiScale)
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Item { Layout.fillWidth: true }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm

                                Button {
                                    visible: !heurCalRunner.isRunning
                                    text: "▶ Калибровать"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: {
                                        candidatesModel.clear()
                                        heurPanel.bestCandidateIdx = -1
                                        heurPanel.bestScore = 0.0
                                        heurPanel.patchText = ""
                                        heurPanel.calDone = 0
                                        heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                        heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                          parseInt(calGamesInput.text),
                                                          parseInt(calSeedInput.text), false)
                                    }
                                    contentItem: Text { text: parent.text; color: "#e8c060"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: parent.down ? "#100e00" : "#1a1508"; border.color: parent.hovered ? "#d0a030" : "#b88a26"; border.width: 1 }
                                }
                                Button {
                                    visible: !heurCalRunner.isRunning
                                    text: "Dry run"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: {
                                        candidatesModel.clear()
                                        heurPanel.bestCandidateIdx = -1
                                        heurPanel.calDone = 0
                                        heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                        heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                          parseInt(calGamesInput.text),
                                                          parseInt(calSeedInput.text), true)
                                    }
                                    contentItem: Text { text: parent.text; color: root.textSecondary; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Button {
                                    visible: heurCalRunner.isRunning
                                    text: "■ Стоп"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: heurCalRunner.stop()
                                    contentItem: Text { text: parent.text; color: "#c05050"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: "#1a0c0c"; border.color: "#6b2020"; border.width: 1 }
                                }

                                Item { Layout.fillWidth: true }
                                Text {
                                    visible: heurCalRunner.isRunning
                                    text: heurPanel.calDone + " / " + heurPanel.calTotal
                                    color: root.textSecondary; font.pixelSize: root.evalCaptionSize
                                    font.family: "JetBrains Mono"
                                }
                            }

                            // Прогресс-бар
                            Rectangle {
                                Layout.fillWidth: true
                                height: Math.round(8 * root.uiScale)
                                visible: heurCalRunner.isRunning || heurPanel.calDone > 0
                                color: root.bgSurface
                                border.color: root.borderMuted; border.width: 1
                                Rectangle {
                                    width: heurPanel.calTotal > 0
                                        ? parent.width * heurPanel.calDone / heurPanel.calTotal
                                        : 0
                                    height: parent.height
                                    color: "#b88a26"
                                    Behavior on width { NumberAnimation { duration: 300 } }
                                }
                            }
                        }
                    }

                    // Живая таблица кандидатов
                    GroupBox {
                        width: parent.width
                        title: "Кандидаты — live"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ListModel { id: candidatesModel }

                        Column {
                            width: parent.width
                            spacing: 0

                            // Заголовок таблицы
                            Row {
                                width: parent.width
                                height: Math.round(20 * root.uiScale)
                                Rectangle { anchors.fill: parent; color: root.bgSurface }
                                Repeater {
                                    model: [["#", 36], ["score", 60], ["winrate", 64], ["entropy", 64], ["draws", 56], ["статус", 0]]
                                    delegate: Text {
                                        text: modelData[0]; color: root.textSecondary
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                        width: modelData[1] > 0 ? Math.round(modelData[1] * root.uiScale) : parent.width - Math.round(340 * root.uiScale)
                                        leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter
                                    }
                                }
                            }

                            ListView {
                                width: parent.width
                                height: Math.min(candidatesModel.count * Math.round(22 * root.uiScale), Math.round(260 * root.uiScale))
                                model: candidatesModel
                                clip: true
                                ScrollBar.vertical: ScrollBar {}

                                delegate: Rectangle {
                                    width: ListView.view.width
                                    height: Math.round(22 * root.uiScale)
                                    color: model.isBest ? "#0d2010"
                                         : index % 2 === 0 ? root.bgElevated : root.bgSurface

                                    Row {
                                        anchors.fill: parent
                                        Repeater {
                                            model: [
                                                [model.idx,     36,  model.isBest ? "#b88a26" : root.textSecondary],
                                                [model.score,   60,  model.isBest ? "#4caf6e" : root.textPrimary],
                                                [model.winrate, 64,  root.textPrimary],
                                                [model.entropy, 64,  parseFloat(model.entropy) >= 0.86 ? "#4caf6e" : parseFloat(model.entropy) >= 0.84 ? "#b88a26" : "#cf3f3f"],
                                                [model.draws,   56,  root.textPrimary],
                                            ]
                                            delegate: Text {
                                                text: modelData[0]; color: modelData[2]
                                                font.pixelSize: root.evalCaptionSize
                                                font.family: "JetBrains Mono"
                                                font.bold: modelData[1] === 60 && model.isBest
                                                width: Math.round(modelData[1] * root.uiScale)
                                                leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter
                                            }
                                        }
                                        // Статус тег
                                        Rectangle {
                                            height: Math.round(16 * root.uiScale)
                                            width: statusTagText.implicitWidth + Math.round(10 * root.uiScale)
                                            anchors.verticalCenter: parent.verticalCenter
                                            color: model.isBest ? "#0d2918"
                                                 : model.status === "ok" ? "#0d2918"
                                                 : model.status === "dry_run" ? "#0e1f3a"
                                                 : "#1a0808"
                                            border.color: model.isBest ? "#1f5030"
                                                        : model.status === "ok" ? "#1f5030"
                                                        : model.status === "dry_run" ? "#2f6ed8"
                                                        : "#5a1515"
                                            border.width: 1
                                            Text {
                                                id: statusTagText
                                                anchors.centerIn: parent
                                                text: model.isBest ? "★ лучший"
                                                    : model.status === "ok" ? "✓"
                                                    : model.status === "dry_run" ? "dry"
                                                    : model.status === "в работе" ? "⟳"
                                                    : model.reason.length > 0 ? model.reason.substring(0, 12)
                                                    : model.status
                                                color: model.isBest ? "#4caf6e"
                                                     : model.status === "ok" ? "#4caf6e"
                                                     : model.status === "dry_run" ? "#7db4f5"
                                                     : "#cf3f3f"
                                                font.pixelSize: Math.round(8 * root.uiScale)
                                            }
                                        }
                                    }
                                }
                            }

                            Text {
                                visible: candidatesModel.count === 0
                                text: "Нет данных. Запустите калибровку."
                                color: root.textSecondary; font.pixelSize: root.evalCaptionSize
                                leftPadding: root.spacingSm; topPadding: root.spacingSm
                            }
                        }
                    }

                    // Патч-блок
                    GroupBox {
                        width: parent.width
                        visible: heurPanel.bestCandidateIdx >= 0
                        title: "Лучший патч — кандидат #" + heurPanel.bestCandidateIdx
                        label: Text { text: parent.title; color: "#4caf6e"; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: "#0d2010"; border.color: "#1f5030"; border.width: 1 }

                        ColumnLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            // Резюме score
                            Text {
                                text: "score=" + _fmt(heurPanel.bestScore, 3)
                                color: "#4caf6e"
                                font.pixelSize: root.evalCaptionSize
                                font.family: "JetBrains Mono"
                                font.bold: true
                            }

                            // Патч-текст (заполняется из best_reward_config_patch.md по завершении)
                            TextArea {
                                Layout.fillWidth: true
                                height: Math.round(80 * root.uiScale)
                                text: heurPanel.patchText.length > 0
                                    ? heurPanel.patchText
                                    : "(Завершите калибровку для просмотра патча)"
                                readOnly: true
                                color: "#7db4f5"
                                font.pixelSize: Math.round(9 * root.uiScale)
                                font.family: "JetBrains Mono"
                                background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                            }

                            RowLayout {
                                spacing: root.spacingSm
                                Button {
                                    text: "✓ Применить патч"
                                    font.pixelSize: root.evalCaptionSize
                                    enabled: heurPanel.currentRunDir.length > 0 && !heurCalRunner.isRunning
                                    onClicked: heurCalRunner.applyPatch(heurPanel.currentRunDir)
                                    contentItem: Text { text: parent.text; color: parent.enabled ? "#e8c060" : "#6b5010"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: parent.down ? "#100e00" : "#1a1508"; border.color: parent.enabled ? (parent.hovered ? "#d0a030" : "#b88a26") : "#3a3010"; border.width: 1 }
                                }
                                Button {
                                    text: "Открыть папку"
                                    font.pixelSize: root.evalCaptionSize
                                    enabled: heurPanel.currentRunDir.length > 0
                                    onClicked: Qt.openUrlExternally("file:///" + heurPanel.currentRunDir)
                                    contentItem: Text { text: parent.text; color: parent.enabled ? root.textSecondary : "#3a4a5a"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Text {
                                    id: patchStatusText
                                    text: ""
                                    font.pixelSize: root.evalCaptionSize
                                    font.family: "JetBrains Mono"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

- [ ] **Шаг 4: запустить контрактный тест**

```
python -m pytest tests/gui/test_heur_metrics_panel_contract.py -v
```
Ожидается: все `PASSED`.

- [ ] **Шаг 5: коммит**

```
git add app/gui_qt/qml/components/HeurMetricsPanel.qml tests/gui/test_heur_metrics_panel_contract.py
git commit -m "feat(gui): HeurMetricsPanel.qml — три подвкладки Сводка/Бенчмарк/Калибровка"
```

---

## Task 6: Wire `HeurMetricsPanel` в `Main.qml`

**Files:**
- Modify: `app/gui_qt/qml/Main.qml:4195–4238`

- [ ] **Шаг 1: заменить старый Item**

В `Main.qml` найти блок начиная со строки 4195:
```qml
            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ScrollView {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg
                    clip: true

                    Column {
                        width: Math.max(parent ? parent.width : 0, root.width - 2 * root.spacingLg)
                        spacing: root.spacingMd

                        Text {
                            text: "Метрики эвристики"
```
... до закрывающего `}` этого `Item` на строке 4238.

Заменить весь блок (строки 4195–4238) на:
```qml
            HeurMetricsPanel {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
```

- [ ] **Шаг 2: запустить GUI и проверить вручную**

```
python app/gui_qt/main.py
```

Открыть вкладку «Метрики эвристики». Убедиться:
1. Три подвкладки отображаются: Сводка / Бенчмарк / Калибровка
2. Вкладка «Сводка» показывает stat-карточки и метрики (те же данные что раньше)
3. Вкладка «Бенчмарк» — поле «Игр», кнопка «Запустить»
4. Вкладка «Калибровка» — поля параметров, кнопки «Калибровать» / «Dry run»
5. Нет ошибок в консоли

- [ ] **Шаг 3: быстрый smoke-тест бенчмарка**

На вкладке «Бенчмарк» нажать «▶ Запустить бенчмарк» (games=5 для скорости — изменить поле вручную).
Ожидается: кнопка меняется на «■ Стоп», после завершения появляется строка с winrate/entropy/draws.

- [ ] **Шаг 4: коммит**

```
git add app/gui_qt/qml/Main.qml
git commit -m "feat(gui): заменяем старый heuristic metrics Item на HeurMetricsPanel с тремя вкладками"
```

---

## Task 7: Читать `patchText` из файла по завершении калибровки

**Files:**
- Modify: `app/gui_qt/heur_calibrate_runner.py`
- Modify: `app/gui_qt/qml/components/HeurMetricsPanel.qml`

По завершении калибровки `calibrationFinished` должен включать текст патча, чтобы QML мог его отобразить.

- [ ] **Шаг 1: добавить `patchLines` в `calibrationFinished` payload**

В `_CalibrateWorker.run()` после чтения `summary.json`, добавить:
```python
            patch_md = run_dir / "best_reward_config_patch.md"
            if patch_md.exists():
                md_text = patch_md.read_text(encoding="utf-8")
                m = re.search(r"```python\n(.*?)```", md_text, re.DOTALL)
                summary["patch_lines"] = m.group(1).strip() if m else ""
            else:
                summary["patch_lines"] = ""
```

- [ ] **Шаг 2: читать `patchText` в QML из `calibrationFinished`**

В `HeurMetricsPanel.qml` в `onCalibrationFinished`:
```qml
        function onCalibrationFinished(summary) {
            heurPanel.currentRunDir = summary.run_dir || heurCalRunner.currentRunDir
            heurPanel.patchText = summary.patch_lines || ""
            var idx = summary.best_candidate_idx
            if (idx !== null && idx !== undefined) {
                heurPanel.bestCandidateIdx = idx
            }
        }
```

- [ ] **Шаг 3: запустить dry-run калибровки чтобы проверить patch_lines**

```
python -m pytest tests/gui/test_heur_calibrate_runner.py -v
python app/gui_qt/main.py
```
Запустить «Dry run» в GUI, дождаться завершения — патч-блок должен появиться с текстом `(Завершите калибровку...)` или реальными строками.

- [ ] **Шаг 4: коммит**

```
git add app/gui_qt/heur_calibrate_runner.py app/gui_qt/qml/components/HeurMetricsPanel.qml
git commit -m "feat(gui): patch_lines в calibrationFinished payload — текст патча в GUI"
```

---

## Self-review

**Проверка покрытия спека:**

| Требование | Task |
|---|---|
| Три подвкладки Сводка/Бенчмарк/Калибровка | Task 5 |
| `heuristicMetricsDict` property | Task 1 |
| Stat-карточки winrate/entropy/draws | Task 5 |
| HeurBenchmarkRunner signals/slots | Task 2 |
| HeurCalibrateRunner signals/slots | Task 3 |
| Регистрация runners в main.py | Task 4 |
| Прогресс-бар калибровки | Task 5 (QML) |
| Живая таблица кандидатов | Task 5 (QML) |
| applyPatch → reward_config.py | Task 3 + Task 7 |
| Wire в Main.qml | Task 6 |
| Обработка ошибок (failed signals → UI) | Task 5 (Connections) |
| Кнопка «Стоп» | Task 5 (QML) |
| История бенчмарков in-memory | Task 5 (QML benchHistoryModel) |
| Открыть папку run_dir | Task 5 (Qt.openUrlExternally) |

**Placeholder scan:** Нет TBD/TODO.

**Типы:** `applyPatch(run_dir: str)` → `heurCalRunner.applyPatch(heurPanel.currentRunDir)` ✓. `run(int,int,int,bool)` → `heurCalRunner.run(parseInt(...), ..., false)` ✓.
