from pathlib import Path
import re

p = Path(r"C:\40kAI\app\viewer\app.py")
text = p.read_text(encoding="utf-8")

# Replace _populate_units_table body
old_pop = """    def _populate_units_table(self, units):
        self.units_table.setRowCount(len(units))
        self.units_table.setSortingEnabled(False)
        self._unit_row_by_key = {}
        for row, unit in enumerate(units):
            side_label = (
                self._viewer_player_role_label
                if unit.get("side") == "player"
                else self._viewer_model_role_label
            )
            unit_key = (unit.get("side"), unit.get("id"))
            values = [
                side_label,
                str(unit.get("id", "—")),
                unit.get("name", "—"),
                str(unit.get("hp", "—")),
                str(unit.get("models", "—")),
            ]
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                if col == 0:
                    item.setData(QtCore.Qt.UserRole, unit_key)
                self.units_table.setItem(row, col, item)
            self._unit_row_by_key[unit_key] = row
        self.units_table.setSortingEnabled(True)
        self._rebuild_unit_row_mapping()
        self._sync_qml_units_summary()"""

new_pop = """    def _populate_units_table(self, units):
        self._populate_units_model(units)

    def _populate_units_model(self, units):
        self._unit_row_by_key = {}
        if self._viewer_units_model is None:
            return
        active_side = self._active_unit_side
        active_id = self._active_unit_id
        self._viewer_units_model.populate(
            list(units or []),
            player_label=self._viewer_player_role_label,
            model_label=self._viewer_model_role_label,
            active_side=active_side,
            active_unit_id=active_id,
            selected_side=self._selected_unit_side,
            selected_unit_id=self._selected_unit_id,
        )
        for row_idx in range(self._viewer_units_model.rowCount()):
            side = self._viewer_units_model.data(self._viewer_units_model.index(row_idx, 0), ViewerUnitsListModel.SideRole)
            uid = self._viewer_units_model.data(self._viewer_units_model.index(row_idx, 0), ViewerUnitsListModel.IdRole)
            if side and uid is not None:
                self._unit_row_by_key[(side, int(uid))] = row_idx
        self._sync_qml_units_summary()"""

if old_pop in text:
    text = text.replace(old_pop, new_pop)
else:
    print("WARN: populate block not found")

# _sync_selection_from_table stub
text = text.replace(
    """    def _sync_selection_from_table(self):
        if self._syncing_table_selection:
            return
        selected = self.units_table.selectionModel().selectedRows()
        if not selected:
            return
        row = selected[0].row()
        item = self.units_table.item(row, 0)
        if item is None:
            return
        unit_key = item.data(QtCore.Qt.UserRole)
        if not unit_key:
            return
        side, unit_id = unit_key
        if side and unit_id is not None:
            self._set_selected_unit(side, unit_id, source="table")
            self._on_target_selected(unit_id)""",
    """    def _sync_selection_from_table(self):
        pass""",
)

# _rebuild and _find_row stubs
text = re.sub(
    r"    def _rebuild_unit_row_mapping\(self\):.*?return row\n",
    "    def _rebuild_unit_row_mapping(self):\n        self._unit_row_by_key = {}\n        if self._viewer_units_model is None:\n            return\n        for row in range(self._viewer_units_model.rowCount()):\n            side = self._viewer_units_model.data(self._viewer_units_model.index(row, 0), ViewerUnitsListModel.SideRole)\n            uid = self._viewer_units_model.data(self._viewer_units_model.index(row, 0), ViewerUnitsListModel.IdRole)\n            if side and uid is not None:\n                self._unit_row_by_key[(side, int(uid))] = row\n\n    def _find_row_for_unit(self, unit_key):\n        return self._unit_row_by_key.get(unit_key)\n",
    text,
    count=1,
    flags=re.DOTALL,
)

# _apply_state else branch
text = text.replace(
    """            self.status_round.setText(labels.round_text)
            self.status_turn.setText(labels.turn_text)
            self.status_phase.setText(labels.phase_text)
            self.status_active.setText(labels.active_label_text)
            self.status_deployment.setText(labels.deployment_text)
            self.points_vp_player.setText(labels.vp_player_text)
            self.points_vp_model.setText(labels.vp_model_text)
            self.points_cp_player.setText(labels.cp_player_text)
            self.points_cp_model.setText(labels.cp_model_text)""",
    """            self.viewer_controller.apply_labels(
                labels,
                phase_raw=phase_raw_val,
                active_side_raw=active_raw,
            )""",
)

# timeline label
text = text.replace(
    'return f"{self.status_round.text()} • {self.status_active.text()} • {self.status_phase.text()}"',
    'vc = self.viewer_controller\n            return f"{vc.roundText} • {vc.activeLabelText} • {vc.phaseText}"',
)

# command_input refs
text = text.replace("self.command_input.setEnabled(enabled)", "pass  # command UI in QML")
text = text.replace('getattr(self, "shoot_popover", None) and self.shoot_popover.isVisible()', "self.viewer_controller.shootPopoverOpen")
text = text.replace("self.command_input.setText", "# removed command_input.setText")
text = text.replace("self.units_table.selectRow(row)", "self.viewer_controller.scrollUnitsListToUnit(unit_id)")

# _select_row_for_unit_id
text = re.sub(
    r"def _select_row_for_unit_id\(self, unit_id, side=None\):.*?(?=\n    def )",
    """def _select_row_for_unit_id(self, unit_id, side=None):
        if side is None:
            for (s, uid) in self._unit_row_by_key:
                if uid == unit_id:
                    side = s
                    break
        if side is None:
            return
        self._set_selected_unit(side, unit_id, source="table", select_row=True)

    """,
    text,
    count=1,
    flags=re.DOTALL,
)

p.write_text(text, encoding="utf-8")
print("patch2 done")
