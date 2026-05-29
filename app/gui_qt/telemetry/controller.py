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
            def __init__(self, outer):
                super().__init__()
                self.outer = outer

            def run(self):
                self.outer._refresh_sync()

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
