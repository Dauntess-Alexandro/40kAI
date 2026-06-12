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
            run_dir = (
                _PROJECT_ROOT / "artifacts" / "metrics" / "heur_calibration" / self._run_id
            )
            summary_path = run_dir / "summary.json"
            summary: dict = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
            patch_md = run_dir / "best_reward_config_patch.md"
            if patch_md.exists():
                md_text = patch_md.read_text(encoding="utf-8")
                pm = re.search(r"```python\n(.*?)```", md_text, re.DOTALL)
                summary["patch_lines"] = pm.group(1).strip() if pm else ""
            else:
                summary["patch_lines"] = ""
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
