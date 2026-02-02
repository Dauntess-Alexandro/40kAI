from PySide6 import QtCore, QtGui, QtWidgets

from viewer.styles import Theme


class UnitItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, unit, radius, color, hover_callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit = unit
        self._hover_callback = hover_callback
        self.setRect(-radius, -radius, radius * 2, radius * 2)
        self.setBrush(Theme.brush(color))
        self.setPen(Theme.pen(Theme.outline, 0.8))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setToolTip(
            "ID: {id}\n{label}\nHP: {hp}\nМодели: {models}\nКоорд: ({x}, {y})".format(
                id=self.unit.get("id", "—"),
                label=self.unit.get("name", "—"),
                hp=self.unit.get("hp", "—"),
                models=self.unit.get("models", "—"),
                x=self.unit.get("x", "—"),
                y=self.unit.get("y", "—"),
            )
        )
        if self._hover_callback:
            self._hover_callback(self.unit, True)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self._hover_callback:
            self._hover_callback(self.unit, False)
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            painter.setPen(Theme.pen(Theme.selection, 2))
        super().paint(painter, option, widget)


class MapScene(QtWidgets.QGraphicsScene):
    unit_selected = QtCore.Signal(str, int)

    def __init__(self, cell_size=18, parent=None):
        super().__init__(parent)
        self.cell_size = cell_size
        self.grid_items = []
        self.unit_items = {}
        self.objective_items = []
        self.objective_radius_items = []
        self.objective_label_items = []
        self.label_items = []
        self.move_highlight_items = []
        self.target_highlight_items = []
        self._board_width = 0
        self._board_height = 0
        self._active_unit_id = None
        self._active_unit_side = None
        self._hovered_unit_key = None
        self._selected_unit_key = None
        self._phase = None
        self._move_range = None
        self._shoot_range = None
        self._show_objective_radius = True
        self._state = {}
        self._targets = None
        self._error_item = None
        self.selectionChanged.connect(self._emit_selection)

    def set_error_message(self, message):
        if self._error_item is not None:
            self.removeItem(self._error_item)
            self._error_item = None
        if not message:
            return
        text_item = QtWidgets.QGraphicsTextItem(str(message))
        text_item.setDefaultTextColor(Theme.text)
        text_item.setTextWidth(420)
        text_item.setPos(20, 20)
        self.addItem(text_item)
        self._error_item = text_item

    def _emit_selection(self):
        self._selected_unit_key = None
        for item in self.selectedItems():
            if isinstance(item, UnitItem):
                side = item.unit.get("side")
                unit_id = item.unit.get("id")
                if side and unit_id:
                    self._selected_unit_key = (side, unit_id)
                    self.unit_selected.emit(side, unit_id)
                    break
        self.refresh_overlays()

    def _clear_dynamic_items(self):
        for item in (
            self.objective_items
            + self.objective_radius_items
            + self.objective_label_items
            + list(self.unit_items.values())
            + self.label_items
        ):
            self.removeItem(item)
        self.objective_items = []
        self.objective_radius_items = []
        self.objective_label_items = []
        self.unit_items = {}
        self.label_items = []
        self._clear_overlay_items()

    def _clear_overlay_items(self):
        for item in self.move_highlight_items + self.target_highlight_items:
            self.removeItem(item)
        self.move_highlight_items = []
        self.target_highlight_items = []

    def _draw_grid(self, width, height):
        for item in self.grid_items:
            self.removeItem(item)
        self.grid_items = []
        pen = Theme.pen(Theme.grid, 0.5)
        for x in range(width + 1):
            line = self.addLine(
                x * self.cell_size, 0, x * self.cell_size, height * self.cell_size, pen
            )
            self.grid_items.append(line)
        for y in range(height + 1):
            line = self.addLine(
                0, y * self.cell_size, width * self.cell_size, y * self.cell_size, pen
            )
            self.grid_items.append(line)

    def update_state(self, state):
        self._state = state or {}
        board = state.get("board", {})
        width = int(board.get("width") or 60)
        height = int(board.get("height") or 40)
        self._board_width = width
        self._board_height = height
        self._draw_grid(width, height)
        self.setSceneRect(0, 0, width * self.cell_size, height * self.cell_size)
        self._clear_dynamic_items()

        units = state.get("units", []) or []
        occupied = {}
        for unit in units:
            key = (unit.get("x"), unit.get("y"))
            occupied.setdefault(key, []).append(unit)

        for unit in units:
            x = unit.get("x")
            y = unit.get("y")
            if x is None or y is None:
                continue
            stack = occupied.get((x, y), [])
            offset = 0
            if len(stack) > 1:
                offset = (stack.index(unit) - (len(stack) - 1) / 2) * (self.cell_size * 0.15)
            center_x = x * self.cell_size + self.cell_size / 2 + offset
            center_y = y * self.cell_size + self.cell_size / 2 - offset

            color = Theme.player if unit.get("side") == "player" else Theme.model
            radius = self.cell_size * 0.35
            item = UnitItem(unit, radius, color, hover_callback=self._on_unit_hover)
            item.setPos(center_x, center_y)
            self.addItem(item)
            self.unit_items[(unit.get("side"), unit.get("id"))] = item

            label = QtWidgets.QGraphicsSimpleTextItem(str(unit.get("id", "")))
            label.setBrush(Theme.brush(Theme.text))
            label.setFont(Theme.font(size=8, bold=True))
            label.setPos(center_x - radius, center_y - radius - 8)
            self.addItem(label)
            self.label_items.append(label)

        for objective in state.get("objectives", []) or []:
            x = objective.get("x")
            y = objective.get("y")
            if x is None or y is None:
                continue
            radius = self.cell_size * 0.2
            item = QtWidgets.QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
            item.setBrush(Theme.brush(Theme.objective))
            item.setPen(Theme.pen(Theme.outline, 0.8))
            item.setPos(x * self.cell_size + self.cell_size / 2,
                        y * self.cell_size + self.cell_size / 2)
            self.addItem(item)
            self.objective_items.append(item)

            label = QtWidgets.QGraphicsSimpleTextItem(str(objective.get("id", "")))
            label.setBrush(Theme.brush(Theme.text))
            label.setFont(Theme.font(size=8, bold=True))
            label.setPos(
                x * self.cell_size + self.cell_size / 2 + radius,
                y * self.cell_size + self.cell_size / 2 + radius,
            )
            self.addItem(label)
            self.objective_label_items.append(label)

            control_color = Theme.objective
            owner = objective.get("owner")
            if owner == "player":
                control_color = Theme.player
            elif owner == "model":
                control_color = Theme.model
            control_pen = QtGui.QPen(control_color)
            control_pen.setWidthF(1.2)
            control_pen.setStyle(QtCore.Qt.DashLine)
            control_radius_cells = 3
            circle_radius = control_radius_cells * self.cell_size
            circle = QtWidgets.QGraphicsEllipseItem(
                -circle_radius,
                -circle_radius,
                circle_radius * 2,
                circle_radius * 2,
            )
            circle.setPen(control_pen)
            circle.setBrush(QtCore.Qt.NoBrush)
            circle.setPos(
                x * self.cell_size + self.cell_size / 2,
                y * self.cell_size + self.cell_size / 2,
            )
            circle.setZValue(-1)
            circle.setVisible(self._show_objective_radius)
            self.addItem(circle)
            self.objective_radius_items.append(circle)
        self.refresh_overlays()

    def _on_unit_hover(self, unit, is_hovering):
        if is_hovering:
            self._hovered_unit_key = (unit.get("side"), unit.get("id"))
        else:
            if self._hovered_unit_key == (unit.get("side"), unit.get("id")):
                self._hovered_unit_key = None
        self.refresh_overlays()

    def select_unit(self, side, unit_id):
        item = self.unit_items.get((side, unit_id))
        if not item:
            return
        self.clearSelection()
        item.setSelected(True)

    def set_active_context(
        self,
        active_unit_id=None,
        active_unit_side=None,
        phase=None,
        move_range=None,
        shoot_range=None,
        show_objective_radius=True,
        targets=None,
    ):
        self._active_unit_id = active_unit_id
        self._active_unit_side = active_unit_side
        self._phase = phase or ""
        self._move_range = move_range
        self._shoot_range = shoot_range
        self._show_objective_radius = bool(show_objective_radius)
        self._targets = targets
        for item in self.objective_radius_items:
            item.setVisible(self._show_objective_radius)
        self.refresh_overlays()

    def set_objective_radius_visible(self, visible):
        self._show_objective_radius = bool(visible)
        for item in self.objective_radius_items:
            item.setVisible(self._show_objective_radius)

    def refresh_overlays(self):
        self._clear_overlay_items()
        active_key = (self._active_unit_side, self._active_unit_id)
        if not active_key[0] or active_key[1] is None:
            return
        force_active = self._should_show_movement() or self._should_show_shooting()
        if (
            self._hovered_unit_key != active_key
            and self._selected_unit_key != active_key
            and not force_active
        ):
            return
        unit = self._state_unit(active_key)
        if unit is None:
            return
        if self._should_show_movement():
            self._draw_movement_overlay(unit)
        if self._should_show_shooting():
            self._draw_target_overlay(unit)

    def _state_unit(self, unit_key):
        units = self._state.get("units", []) or []
        for unit in units:
            if (unit.get("side"), unit.get("id")) == unit_key:
                return unit
        return None

    def _should_show_movement(self):
        phase = str(self._phase or "").lower()
        return "move" in phase or "движ" in phase or "movement" in phase or self._move_range is not None

    def _should_show_shooting(self):
        phase = str(self._phase or "").lower()
        return "shoot" in phase or "стрел" in phase or "shooting" in phase

    def _draw_movement_overlay(self, unit):
        move_range = self._move_range
        if move_range is None:
            return
        x = unit.get("x")
        y = unit.get("y")
        if x is None or y is None:
            return
        highlight = QtGui.QColor(Theme.selection)
        highlight.setAlpha(80)
        brush = QtGui.QBrush(highlight)
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        for dx in range(-move_range, move_range + 1):
            for dy in range(-move_range, move_range + 1):
                if abs(dx) + abs(dy) > move_range:
                    continue
                cell_x = x + dx
                cell_y = y + dy
                if cell_x < 0 or cell_y < 0 or cell_x >= self._board_width or cell_y >= self._board_height:
                    continue
                rect = QtWidgets.QGraphicsRectItem(
                    cell_x * self.cell_size,
                    cell_y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                rect.setBrush(brush)
                rect.setPen(pen)
                rect.setZValue(-0.5)
                self.addItem(rect)
                self.move_highlight_items.append(rect)

    def _draw_target_overlay(self, unit):
        shoot_range = self._shoot_range
        if shoot_range is None:
            return
        source_x = unit.get("x")
        source_y = unit.get("y")
        if source_x is None or source_y is None:
            return
        target_keys = self._resolve_targets(unit, shoot_range)
        for key in target_keys:
            item = self.unit_items.get(key)
            if not item:
                continue
            radius = item.rect().width() / 2 + self.cell_size * 0.1
            outline = QtWidgets.QGraphicsEllipseItem(
                -radius,
                -radius,
                radius * 2,
                radius * 2,
            )
            outline.setPos(item.pos())
            outline.setBrush(QtCore.Qt.NoBrush)
            outline.setPen(Theme.pen(Theme.accent, 2))
            outline.setZValue(1.5)
            self.addItem(outline)
            self.target_highlight_items.append(outline)

    def _resolve_targets(self, unit, shoot_range):
        targets = set()
        if isinstance(self._targets, list):
            for entry in self._targets:
                if isinstance(entry, dict):
                    side = entry.get("side")
                    target_id = entry.get("id")
                    if side and target_id is not None:
                        targets.add((side, target_id))
                elif isinstance(entry, (list, tuple)) and len(entry) >= 2:
                    targets.add((entry[0], entry[1]))
                elif isinstance(entry, int):
                    for candidate in self._state.get("units", []) or []:
                        if candidate.get("id") == entry:
                            targets.add((candidate.get("side"), candidate.get("id")))
        if targets:
            return targets
        source_x = unit.get("x")
        source_y = unit.get("y")
        if source_x is None or source_y is None:
            return targets
        for target in self._state.get("units", []) or []:
            if target.get("side") == unit.get("side"):
                continue
            target_x = target.get("x")
            target_y = target.get("y")
            if target_x is None or target_y is None:
                continue
            distance = abs(target_x - source_x) + abs(target_y - source_y)
            if distance <= shoot_range:
                targets.add((target.get("side"), target.get("id")))
        return targets
