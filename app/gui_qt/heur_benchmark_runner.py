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
