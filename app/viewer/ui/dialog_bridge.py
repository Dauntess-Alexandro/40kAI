"""QML overlays: toast + modal confirm (non-blocking from engine POV)."""

from __future__ import annotations

from typing import Any, Optional

from PySide6.QtCore import QObject, Property, Signal, Slot, QTimer


class ViewerDialogBridge(QObject):
    """Context object: ``toastVisible``, ``toastText``; confirm dialog props + signals."""

    toastTextChanged = Signal()
    toastVisibleChanged = Signal()
    confirmOpenChanged = Signal()
    confirmTitleChanged = Signal()
    confirmBodyChanged = Signal()
    confirmAccepted = Signal()
    confirmRejected = Signal()

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._toast_text = ""
        self._toast_visible = False
        self._confirm_open = False
        self._confirm_title = ""
        self._confirm_body = ""
        self._toast_timer = QTimer(self)
        self._toast_timer.setSingleShot(True)
        self._toast_timer.timeout.connect(self._hide_toast)

    def _hide_toast(self) -> None:
        if self._toast_visible:
            self._toast_visible = False
            self.toastVisibleChanged.emit()

    def _get_toast_text(self) -> str:
        return self._toast_text

    toastText = Property(str, _get_toast_text, notify=toastTextChanged)

    def _get_toast_visible(self) -> bool:
        return self._toast_visible

    toastVisible = Property(bool, _get_toast_visible, notify=toastVisibleChanged)

    def _get_confirm_open(self) -> bool:
        return self._confirm_open

    confirmOpen = Property(bool, _get_confirm_open, notify=confirmOpenChanged)

    def _get_confirm_title(self) -> str:
        return self._confirm_title

    confirmTitle = Property(str, _get_confirm_title, notify=confirmTitleChanged)

    def _get_confirm_body(self) -> str:
        return self._confirm_body

    confirmBody = Property(str, _get_confirm_body, notify=confirmBodyChanged)

    @Slot(str, int)
    def showToast(self, text: str, duration_ms: int = 2800) -> None:
        self._toast_timer.stop()
        self._toast_text = str(text or "")
        self.toastTextChanged.emit()
        self._toast_visible = True
        self.toastVisibleChanged.emit()
        ms = max(600, min(12000, int(duration_ms)))
        self._toast_timer.start(ms)

    @Slot()
    def dismissToast(self) -> None:
        self._toast_timer.stop()
        self._hide_toast()

    @Slot(str, str)
    def openConfirm(self, title: str, body: str) -> None:
        self._confirm_title = str(title or "")
        self._confirm_body = str(body or "")
        self.confirmTitleChanged.emit()
        self.confirmBodyChanged.emit()
        self._confirm_open = True
        self.confirmOpenChanged.emit()

    @Slot()
    def acceptConfirm(self) -> None:
        self._confirm_open = False
        self.confirmOpenChanged.emit()
        self.confirmAccepted.emit()

    @Slot()
    def rejectConfirm(self) -> None:
        self._confirm_open = False
        self.confirmOpenChanged.emit()
        self.confirmRejected.emit()
