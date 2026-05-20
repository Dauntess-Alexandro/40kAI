"""QML ListView model for coloured viewer log lines (virtualized delegate recycling)."""

from __future__ import annotations

from typing import Any, Dict, List

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt


class ViewerLogListModel(QAbstractListModel):
    """Roles: ``logText``, ``logColor``, ``logEntryIdx``, ``logIsAux``."""

    TextRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2
    EntryIdxRole = Qt.UserRole + 3
    IsAuxRole = Qt.UserRole + 4

    def __init__(self, parent: Any = None) -> None:
        super().__init__(parent)
        self._rows: List[Dict[str, Any]] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.TextRole: b"logText",
            self.ColorRole: b"logColor",
            self.EntryIdxRole: b"logEntryIdx",
            self.IsAuxRole: b"logIsAux",
        }

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        if role in (self.TextRole, Qt.DisplayRole):
            return str(row.get("text") or "")
        if role == self.ColorRole:
            return str(row.get("color") or "#d7dde7")
        if role == self.EntryIdxRole:
            return int(row.get("entry_idx", -1))
        if role == self.IsAuxRole:
            return bool(row.get("is_aux", False))
        return None

    def set_rows(self, rows: List[Dict[str, Any]]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()
