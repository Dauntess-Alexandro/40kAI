"""QML ListView model for squad cards in the right panel."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, Slot


class ViewerUnitsListModel(QAbstractListModel):
    """Roles for ``UnitCard.qml`` delegate."""

    IdRole = Qt.UserRole + 1
    SideRole = Qt.UserRole + 2
    NameRole = Qt.UserRole + 3
    HpRole = Qt.UserRole + 4
    ModelsRole = Qt.UserRole + 5
    IconPathRole = Qt.UserRole + 6
    FactionLabelRole = Qt.UserRole + 7
    IsActiveRole = Qt.UserRole + 8
    IsSelectedRole = Qt.UserRole + 9
    IsDamagedRole = Qt.UserRole + 10
    SectionRole = Qt.UserRole + 11

    def __init__(self, parent: Any = None) -> None:
        super().__init__(parent)
        self._rows: List[Dict[str, Any]] = []
        self._icon_resolver: Optional[Callable[[str], str]] = None

    def set_icon_resolver(self, resolver: Optional[Callable[[str], str]]) -> None:
        self._icon_resolver = resolver

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def roleNames(self) -> Dict[int, QByteArray]:
        return {
            self.IdRole: QByteArray(b"unitId"),
            self.SideRole: QByteArray(b"unitSide"),
            self.NameRole: QByteArray(b"unitName"),
            self.HpRole: QByteArray(b"unitHp"),
            self.ModelsRole: QByteArray(b"unitModels"),
            self.IconPathRole: QByteArray(b"unitIconPath"),
            self.FactionLabelRole: QByteArray(b"unitFactionLabel"),
            self.IsActiveRole: QByteArray(b"unitIsActive"),
            self.IsSelectedRole: QByteArray(b"unitIsSelected"),
            self.IsDamagedRole: QByteArray(b"unitIsDamaged"),
            self.SectionRole: QByteArray(b"unitSection"),
        }

    @Slot(int, result="QVariantMap")
    def rowAt(self, row: int) -> Dict[str, Any]:
        """Stable row payload for QML delegates (avoids missing model.* roles)."""
        idx = self.index(int(row), 0)
        if not idx.isValid():
            return {}
        return {
            "unitId": int(self.data(idx, self.IdRole) or -1),
            "unitSide": str(self.data(idx, self.SideRole) or ""),
            "unitName": str(self.data(idx, self.NameRole) or "—"),
            "unitHp": str(self.data(idx, self.HpRole) or "—"),
            "unitModels": str(self.data(idx, self.ModelsRole) or "—"),
            "unitIconPath": str(self.data(idx, self.IconPathRole) or ""),
            "unitFactionLabel": str(self.data(idx, self.FactionLabelRole) or ""),
            "unitIsActive": bool(self.data(idx, self.IsActiveRole)),
            "unitIsSelected": bool(self.data(idx, self.IsSelectedRole)),
            "unitIsDamaged": bool(self.data(idx, self.IsDamagedRole)),
            "unitSection": str(self.data(idx, self.SectionRole) or ""),
        }

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        if role == self.IdRole:
            return int(row.get("id", -1))
        if role == self.SideRole:
            return str(row.get("side") or "")
        if role == self.NameRole:
            return str(row.get("name") or "—")
        if role == self.HpRole:
            return str(row.get("hp") or "—")
        if role == self.ModelsRole:
            return str(row.get("models") or "—")
        if role == self.IconPathRole:
            return str(row.get("icon_path") or "")
        if role == self.FactionLabelRole:
            return str(row.get("faction_label") or "")
        if role == self.IsActiveRole:
            return bool(row.get("is_active"))
        if role == self.IsSelectedRole:
            return bool(row.get("is_selected"))
        if role == self.IsDamagedRole:
            return bool(row.get("is_damaged"))
        if role == self.SectionRole:
            return str(row.get("section") or "")
        return None

    def populate(
        self,
        units: List[dict],
        *,
        player_label: str,
        model_label: str,
        active_side: Optional[str],
        active_unit_id: Optional[int],
        selected_side: Optional[str],
        selected_unit_id: Optional[int],
    ) -> None:
        player_rows: List[Dict[str, Any]] = []
        model_rows: List[Dict[str, Any]] = []
        for unit in units:
            if not isinstance(unit, dict):
                continue
            side = str(unit.get("side") or "")
            uid = unit.get("id")
            try:
                uid_int = int(uid)
            except (TypeError, ValueError):
                continue
            hp_raw = str(unit.get("hp") or "")
            is_damaged = "/" in hp_raw and not hp_raw.strip().endswith("/0")
            if "/" in hp_raw:
                try:
                    cur, mx = hp_raw.split("/", 1)
                    is_damaged = float(cur.strip()) < float(mx.strip())
                except ValueError:
                    pass
            icon_path = ""
            if self._icon_resolver is not None:
                icon_path = str(self._icon_resolver(str(unit.get("name") or "")) or "")
            row = {
                "id": uid_int,
                "side": side,
                "name": unit.get("name", "—"),
                "hp": hp_raw or "—",
                "models": str(unit.get("models") or "—"),
                "icon_path": icon_path,
                "faction_label": player_label if side == "player" else model_label,
                "is_active": side == active_side and uid_int == active_unit_id,
                "is_selected": side == selected_side and uid_int == selected_unit_id,
                "is_damaged": is_damaged,
            }
            if side == "player":
                player_rows.append(row)
            else:
                model_rows.append(row)

        def _sort_key(r: Dict[str, Any]) -> Tuple[int, int, str]:
            return (
                0 if r.get("is_active") else 1,
                0 if r.get("is_selected") else 1,
                0 if r.get("is_damaged") else 1,
                str(r.get("name") or ""),
            )

        player_rows.sort(key=_sort_key)
        model_rows.sort(key=_sort_key)
        ordered: List[Dict[str, Any]] = []
        for r in player_rows:
            r["section"] = "player"
            ordered.append(r)
        for r in model_rows:
            r["section"] = "model"
            ordered.append(r)

        self.beginResetModel()
        self._rows = ordered
        self.endResetModel()

    def update_selection(
        self,
        selected_side: Optional[str],
        selected_unit_id: Optional[int],
    ) -> None:
        """Refresh is_selected flags without rebuilding the whole list."""
        if not self._rows:
            return
        changed: List[int] = []
        for idx, row in enumerate(self._rows):
            new_sel = (
                row.get("side") == selected_side
                and int(row.get("id", -1)) == int(selected_unit_id or -1)
            )
            if bool(row.get("is_selected")) != new_sel:
                row["is_selected"] = new_sel
                changed.append(idx)
        for idx in changed:
            model_idx = self.index(idx, 0)
            self.dataChanged.emit(model_idx, model_idx, [self.IsSelectedRole])

    def row_for_unit(self, side: str, unit_id: int) -> int:
        for idx, row in enumerate(self._rows):
            if row.get("side") == side and int(row.get("id", -1)) == int(unit_id):
                return idx
        return -1
