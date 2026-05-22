"""QML ListView model for coloured viewer log lines (virtualized delegate recycling)."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt


_LOG_KIND_PATTERNS = [
    ("movement", re.compile(r"\[MOVE\]|движен|movement", re.I)),
    ("shooting", re.compile(r"\[SHOOT\]|стрель|shoot|FIRE|📌 --- ОТЧЁТ", re.I)),
    ("charge", re.compile(r"\[CHARGE\]|заряд|charge", re.I)),
    ("fight", re.compile(r"\[FIGHT\]|бой|fight|melee", re.I)),
    ("result", re.compile(r"\[RESULT\]|🏁|итог|заверш", re.I)),
    ("errors", re.compile(r"\[ERROR\]|⚠|ошибк|invalid|пропущ", re.I)),
    ("debug", re.compile(r"\[DEBUG\]|🧪|VIEWER_DEBUG", re.I)),
]


def classify_log_kind(text: str) -> str:
    raw = str(text or "")
    for kind, pattern in _LOG_KIND_PATTERNS:
        if pattern.search(raw):
            return kind
    return "system"


def extract_log_timestamp(raw: str) -> str:
    match = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", str(raw or ""))
    if match:
        return match.group(1)[11:16]
    return ""


class ViewerLogListModel(QAbstractListModel):
    """Roles: logText, logColor, logEntryIdx, logIsAux, logKind, logTimestamp, logIsHeader, logHeaderText."""

    TextRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2
    EntryIdxRole = Qt.UserRole + 3
    IsAuxRole = Qt.UserRole + 4
    KindRole = Qt.UserRole + 5
    TimestampRole = Qt.UserRole + 6
    IsHeaderRole = Qt.UserRole + 7
    HeaderTextRole = Qt.UserRole + 8
    UnitIdRole = Qt.UserRole + 9
    IsCurrentTurnRole = Qt.UserRole + 10

    _KIND_ICONS = {
        "movement": "👣",
        "shooting": "🎯",
        "charge": "⚡",
        "fight": "⚔️",
        "result": "🏁",
        "errors": "⚠️",
        "debug": "🧪",
        "system": "•",
    }

    def __init__(self, parent: Any = None) -> None:
        super().__init__(parent)
        self._rows: List[Dict[str, Any]] = []
        self._search_text = ""
        self._filters: Dict[str, bool] = {
            "movement": True,
            "shooting": True,
            "charge": True,
            "fight": True,
            "result": True,
            "errors": True,
            "debug": False,
        }
        self._current_turn_key: Optional[str] = None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def roleNames(self) -> Dict[int, bytes]:
        return {
            self.TextRole: b"logText",
            self.ColorRole: b"logColor",
            self.EntryIdxRole: b"logEntryIdx",
            self.IsAuxRole: b"logIsAux",
            self.KindRole: b"logKind",
            self.TimestampRole: b"logTimestamp",
            self.IsHeaderRole: b"logIsHeader",
            self.HeaderTextRole: b"logHeaderText",
            self.UnitIdRole: b"logUnitId",
            self.IsCurrentTurnRole: b"logIsCurrentTurn",
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
        if role == self.KindRole:
            return str(row.get("kind") or "system")
        if role == self.TimestampRole:
            return str(row.get("timestamp") or "")
        if role == self.IsHeaderRole:
            return bool(row.get("is_header", False))
        if role == self.HeaderTextRole:
            return str(row.get("header_text") or "")
        if role == self.UnitIdRole:
            return int(row.get("unit_id", -1))
        if role == self.IsCurrentTurnRole:
            return bool(row.get("is_current_turn", False))
        return None

    def set_filters(self, filters: Dict[str, bool]) -> None:
        self._filters = dict(filters)

    def set_search(self, text: str) -> None:
        self._search_text = str(text or "").strip().lower()

    def set_current_turn_key(self, key: Optional[str]) -> None:
        self._current_turn_key = key

    @staticmethod
    def kind_icon(kind: str) -> str:
        return ViewerLogListModel._KIND_ICONS.get(str(kind or ""), "•")

    def set_rows(self, rows: List[Dict[str, Any]]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def build_rows_from_entries(
        self,
        entries: List[dict],
        *,
        color_resolver,
        unit_id_resolver=None,
    ) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        last_header_key: Optional[str] = None
        for entry_idx, entry in enumerate(entries):
            raw = str(entry.get("raw") or entry.get("text") or "")
            kind = classify_log_kind(raw)
            if not self._filters.get(kind, True) and kind != "system":
                continue
            if self._search_text and self._search_text not in raw.lower():
                continue
            turn_key = str(entry.get("turn_key") or "")
            if turn_key and turn_key != last_header_key:
                last_header_key = turn_key
                header = str(entry.get("turn_header") or turn_key)
                out.append(
                    {
                        "text": "",
                        "color": color_resolver("header"),
                        "entry_idx": -1,
                        "is_aux": True,
                        "kind": "system",
                        "timestamp": "",
                        "is_header": True,
                        "header_text": header,
                        "unit_id": -1,
                        "is_current_turn": turn_key == self._current_turn_key,
                    }
                )
            unit_id = -1
            if unit_id_resolver is not None:
                unit_id = int(unit_id_resolver(raw) or -1)
            out.append(
                {
                    "text": raw,
                    "color": color_resolver(kind),
                    "entry_idx": entry_idx,
                    "is_aux": bool(entry.get("is_aux")),
                    "kind": kind,
                    "timestamp": extract_log_timestamp(raw),
                    "is_header": False,
                    "header_text": "",
                    "unit_id": unit_id,
                    "is_current_turn": turn_key == self._current_turn_key if turn_key else False,
                }
            )
        return out
