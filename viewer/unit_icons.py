from __future__ import annotations

import base64
import os
from functools import lru_cache

from PySide6 import QtCore, QtGui


ICON_DIR = os.path.join(os.path.dirname(__file__), "assets", "icons")
PLACEHOLDER_NAME = "unit_placeholder.png"
TABLE_ICON_SIZE = 18
LOG_ICON_SIZE = 16


def icon_for_unit(unit_name: str | None) -> QtGui.QIcon:
    return _icon_for_unit_cached((unit_name or "").strip().lower())


def icon_src_for_unit(unit_name: str | None, size: int = LOG_ICON_SIZE) -> str:
    normalized = (unit_name or "").strip().lower()
    filename = _resolve_icon_filename(normalized)
    path = os.path.join(ICON_DIR, filename)
    if os.path.exists(path):
        return QtCore.QUrl.fromLocalFile(path).toString()
    pixmap = _placeholder_pixmap(size)
    return _pixmap_to_data_uri(pixmap)


@lru_cache(maxsize=64)
def _icon_for_unit_cached(unit_name: str) -> QtGui.QIcon:
    filename = _resolve_icon_filename(unit_name)
    path = os.path.join(ICON_DIR, filename)
    if os.path.exists(path):
        return QtGui.QIcon(path)
    return QtGui.QIcon(_placeholder_pixmap(TABLE_ICON_SIZE))


@lru_cache(maxsize=8)
def _placeholder_pixmap(size: int) -> QtGui.QPixmap:
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtGui.QColor("#555555"))
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    pen = QtGui.QPen(QtGui.QColor("#888888"))
    pen.setWidth(max(1, size // 8))
    painter.setPen(pen)
    margin = max(2, size // 5)
    painter.drawLine(margin, margin, size - margin, size - margin)
    painter.drawLine(size - margin, margin, margin, size - margin)
    painter.end()
    return pixmap


def _pixmap_to_data_uri(pixmap: QtGui.QPixmap) -> str:
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")
    data = bytes(buffer.data())
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _resolve_icon_filename(unit_name: str) -> str:
    if "necron warriors" in unit_name:
        return "necron_warriors_icon.png"
    if "royal warden" in unit_name:
        return "royal_warden_icon.png"
    if "canoptek scarab swarms" in unit_name or "scarab swarms" in unit_name:
        return "canoptek_scarab_swarms_icon.png"
    return PLACEHOLDER_NAME
