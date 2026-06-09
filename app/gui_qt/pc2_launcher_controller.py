"""Qt-контроллер PC2 Launcher: связывает чистый backend с QML (QProcess + лог)."""

from __future__ import annotations

import os

from PySide6 import QtCore

from app.gui_qt.pc2_launcher_backend import (
    build_launch_env,
    pc2_roles,
    resolve_role,
    validate_share_root,
)
from project_paths import ARTIFACTS_MODELS_DIR, PROJECT_ROOT, resolve_share_models_root

_DECODE_CANDIDATES = ("utf-8-sig", "utf-8", "cp1251", "latin-1")


def _decode(raw: bytes) -> str:
    best, best_score = "", None
    for enc in _DECODE_CANDIDATES:
        text = raw.decode(enc, errors="replace")
        score = text.count("�")
        if best_score is None or score < best_score:
            best, best_score = text, score
        if score == 0:
            return text
    return best


class Pc2LauncherController(QtCore.QObject):
    shareRootChanged = QtCore.Signal()
    runningChanged = QtCore.Signal()
    activeRoleChanged = QtCore.Signal()
    logLine = QtCore.Signal(str)
    smbChecked = QtCore.Signal(bool, str)

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        # При старте подставляем уже настроенную шару (env/MODELS_DIR), если есть.
        guess = resolve_share_models_root()
        self._share_root = "" if guess == str(ARTIFACTS_MODELS_DIR) else guess
        self._active_role = ""
        self._process: QtCore.QProcess | None = None

    # --- Свойства для QML ---
    @QtCore.Property("QVariantList", constant=True)
    def rolesModel(self) -> list[dict]:
        return [
            {
                "id": r.id,
                "label": r.label,
                "note": r.note,
                "requiresGpu": r.requires_gpu,
                "port": r.port if r.port is not None else 0,
            }
            for r in pc2_roles()
        ]

    def _get_share_root(self) -> str:
        return self._share_root

    def _set_share_root(self, value: str) -> None:
        value = str(value or "").strip()
        if value != self._share_root:
            self._share_root = value
            self.shareRootChanged.emit()

    shareRoot = QtCore.Property(str, _get_share_root, _set_share_root, notify=shareRootChanged)

    @QtCore.Property(bool, notify=runningChanged)
    def running(self) -> bool:
        return self._process is not None and self._process.state() != QtCore.QProcess.NotRunning

    @QtCore.Property(str, notify=activeRoleChanged)
    def activeRole(self) -> str:
        return self._active_role

    # --- Слоты ---
    @QtCore.Slot()
    def checkSmb(self) -> None:
        res = validate_share_root(self._share_root)
        self.smbChecked.emit(bool(res.ok), str(res.message))

    @QtCore.Slot(str)
    def start(self, role_id: str) -> None:
        if self.running:
            self.logLine.emit("[GUI] Уже запущено — сначала Стоп.")
            return
        role = resolve_role(role_id)
        if role is None:
            self.logLine.emit(f"[GUI][ERROR] Неизвестная роль: {role_id}")
            return
        if not self._share_root:
            self.logLine.emit("[GUI][ERROR] Сначала задайте общую папку (40KAI_SHARE_ROOT).")
            return

        bat = os.path.join(str(PROJECT_ROOT), role.script.replace("/", os.sep))
        if not os.path.isfile(bat):
            self.logLine.emit(f"[GUI][ERROR] Не найден скрипт: {bat}")
            return

        proc = QtCore.QProcess(self)
        proc.setWorkingDirectory(str(PROJECT_ROOT))
        proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)

        qenv = QtCore.QProcessEnvironment.systemEnvironment()
        for key, val in build_launch_env(self._share_root, base={}).items():
            qenv.insert(key, str(val))
        proc.setProcessEnvironment(qenv)

        proc.readyReadStandardOutput.connect(self._on_output)
        proc.finished.connect(self._on_finished)
        proc.start("cmd.exe", ["/c", bat])

        self._process = proc
        self._active_role = role.id
        self.activeRoleChanged.emit()
        self.runningChanged.emit()
        self.logLine.emit(f"[GUI] Старт: {role.label} (порт {role.port}, шара {self._share_root}).")

    @QtCore.Slot()
    def stop(self) -> None:
        if self._process is None:
            return
        self.logLine.emit("[GUI] Останавливаю…")
        self._process.kill()
        self._process.waitForFinished(3000)

    # --- Внутреннее ---
    def _on_output(self) -> None:
        if self._process is None:
            return
        raw = bytes(self._process.readAllStandardOutput())
        text = _decode(raw)
        for line in text.splitlines():
            if line.strip():
                self.logLine.emit(line)

    def _on_finished(self, exit_code: int, _status) -> None:
        self.logLine.emit(f"[GUI] Процесс завершён (код {exit_code}).")
        self._process = None
        self._active_role = ""
        self.activeRoleChanged.emit()
        self.runningChanged.emit()
