from __future__ import annotations

from typing import Any

from PySide6 import QtCore


class TelemetryCardsModel(QtCore.QAbstractListModel):
    """ListModel для QML: обновляет строки на месте, чтобы полоски анимировались."""

    _ROLES = {
        QtCore.Qt.UserRole + 1: b"cardId",
        QtCore.Qt.UserRole + 2: b"label",
        QtCore.Qt.UserRole + 3: b"valueText",
        QtCore.Qt.UserRole + 4: b"sub",
        QtCore.Qt.UserRole + 5: b"pct",
        QtCore.Qt.UserRole + 6: b"barColor",
        QtCore.Qt.UserRole + 7: b"warn",
        QtCore.Qt.UserRole + 8: b"variant",
    }

    countChanged = QtCore.Signal()

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._rows: list[dict[str, Any]] = []

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._rows)

    def roleNames(self) -> dict[int, bytes]:
        return self._ROLES

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if not index.isValid() or not (0 <= index.row() < len(self._rows)):
            return None
        row = self._rows[index.row()]
        if role == QtCore.Qt.UserRole + 1:
            return row.get("id", "")
        if role == QtCore.Qt.UserRole + 2:
            return row.get("label", "")
        if role == QtCore.Qt.UserRole + 3:
            return row.get("valueText", "")
        if role == QtCore.Qt.UserRole + 4:
            return row.get("sub", "")
        if role == QtCore.Qt.UserRole + 5:
            return row.get("pct", 0)
        if role == QtCore.Qt.UserRole + 6:
            return row.get("color", "#ffffff")
        if role == QtCore.Qt.UserRole + 7:
            return row.get("warn", False)
        if role == QtCore.Qt.UserRole + 8:
            return row.get("variant", "local")
        return None

    @QtCore.Property(int, notify=countChanged)
    def count(self) -> int:
        return len(self._rows)

    def as_list(self) -> list[dict[str, Any]]:
        return list(self._rows)

    def set_cards(self, cards: list[dict[str, Any]]) -> None:
        new_ids = [c.get("id") for c in cards]
        old_ids = [r.get("id") for r in self._rows]
        if new_ids == old_ids:
            for i, card in enumerate(cards):
                if card != self._rows[i]:
                    self._rows[i] = card
                    idx = self.index(i, 0)
                    self.dataChanged.emit(idx, idx)
            return

        self.beginResetModel()
        self._rows = list(cards)
        self.endResetModel()
        self.countChanged.emit()
