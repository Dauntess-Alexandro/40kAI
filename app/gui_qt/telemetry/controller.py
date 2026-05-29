from __future__ import annotations

from typing import Any, Optional

from PySide6 import QtCore

from app.gui_qt.telemetry.batch_meter import BatchMeter
from app.gui_qt.telemetry.cards import build_cards
from app.gui_qt.telemetry.cards_model import TelemetryCardsModel
from app.gui_qt.telemetry.local_probe import LocalTelemetryProbe
from app.gui_qt.telemetry.remote_probe import RemoteTelemetryProbe


class TelemetryController(QtCore.QObject):
    cardsChanged = QtCore.Signal()
    activeChanged = QtCore.Signal()
    _cardsReady = QtCore.Signal(object)

    def __init__(self, parent: Optional[QtCore.QObject] = None, local_probe: Any = None) -> None:
        super().__init__(parent)
        self._local = local_probe if local_probe is not None else LocalTelemetryProbe()
        self._batch = BatchMeter(window=30)
        self._cards_model = TelemetryCardsModel(self)
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
        self._cardsReady.connect(self._apply_cards)

    # --- QML-facing ---
    @QtCore.Property(QtCore.QObject, constant=True)
    def cardsModel(self) -> TelemetryCardsModel:
        return self._cards_model

    @QtCore.Property("QVariant", notify=cardsChanged)
    def cards(self) -> list:
        return self._cards_model.as_list()

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
        self._busy = False
        # финальный пересбор карточек под idle (прочерки), на GUI-потоке
        self._refresh_sync()

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
                try:
                    cards = self.outer._collect_cards()
                except Exception:
                    self.outer._busy = False
                    return
                self.outer._cardsReady.emit(cards)

        self._pool.start(_Job(self))

    def _collect_cards(self) -> list:
        local = self._local.sample(self._pid)
        remote = None
        if self._remote_cfg:
            remote = RemoteTelemetryProbe(
                host=self._remote_cfg.get("host", "127.0.0.1"),
                port=int(self._remote_cfg.get("port", 5555)),
                auth_token=self._remote_cfg.get("auth_token", ""),
            ).sample()
        return build_cards(
            local=local, remote=remote, batch_avg=self._batch.average(),
            batch_size_hint=self._batch_size_hint, algo=self._algo, active=self._active,
        )

    @QtCore.Slot(object)
    def _apply_cards(self, cards: list) -> None:
        self._cards_model.set_cards(cards)
        self.cardsChanged.emit()
        self._busy = False

    def _refresh_sync(self) -> None:
        self._apply_cards(self._collect_cards())
