from PySide6 import QtCore, QtGui, QtWidgets

from viewer.styles import Theme


class UnitItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, unit, radius, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unit = unit
        self.setRect(-radius, -radius, radius * 2, radius * 2)
        self.setBrush(Theme.brush(color))
        self.setPen(Theme.pen(QtGui.QColor("#111"), 0.8))
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
        super().hoverEnterEvent(event)

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
        self.label_items = []
        self.selectionChanged.connect(self._emit_selection)

    def _emit_selection(self):
        for item in self.selectedItems():
            if isinstance(item, UnitItem):
                side = item.unit.get("side")
                unit_id = item.unit.get("id")
                if side and unit_id:
                    self.unit_selected.emit(side, unit_id)
                    return

    def _clear_dynamic_items(self):
        for item in self.objective_items + list(self.unit_items.values()) + self.label_items:
            self.removeItem(item)
        self.objective_items = []
        self.unit_items = {}
        self.label_items = []

    def _draw_grid(self, width, height):
        for item in self.grid_items:
            self.removeItem(item)
        self.grid_items = []
        pen = Theme.pen(Theme.grid, 0.6)
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
        board = state.get("board", {})
        width = int(board.get("width") or 60)
        height = int(board.get("height") or 40)
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
            item = UnitItem(unit, radius, color)
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
            item.setPen(Theme.pen(QtGui.QColor("#111"), 0.8))
            item.setPos(x * self.cell_size + self.cell_size / 2,
                        y * self.cell_size + self.cell_size / 2)
            self.addItem(item)
            self.objective_items.append(item)

    def select_unit(self, side, unit_id):
        item = self.unit_items.get((side, unit_id))
        if not item:
            return
        self.clearSelection()
        item.setSelected(True)
