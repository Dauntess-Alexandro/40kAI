import os
from PySide6 import QtCore, QtGui, QtWidgets

from viewer.scene import MapScene
from viewer.state import StateWatcher
from viewer.styles import Theme


class MapView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.TextAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
        )
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.SmartViewportUpdate)

    def wheelEvent(self, event):
        zoom_in = 1.15
        zoom_out = 1 / zoom_in
        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)


class ViewerWindow(QtWidgets.QMainWindow):
    def __init__(self, state_path):
        super().__init__()
        self.state_path = state_path
        self.setWindowTitle("40kAI Viewer")
        self.resize(1200, 800)

        self.state_watcher = StateWatcher(self.state_path)
        self.map_scene = MapScene(cell_size=18)
        self.map_scene.unit_selected.connect(self._select_row_for_unit)

        self.map_view = MapView(self.map_scene)
        self.map_view.setBackgroundBrush(Theme.brush(Theme.background))

        self.status_round = QtWidgets.QLabel("Раунд: —")
        self.status_turn = QtWidgets.QLabel("Ход: —")
        self.status_phase = QtWidgets.QLabel("Фаза: —")
        self.status_active = QtWidgets.QLabel("Активен: —")

        self.points_vp = QtWidgets.QLabel("VP: — / —")
        self.points_cp = QtWidgets.QLabel("CP: — / —")

        self.units_table = QtWidgets.QTableWidget(0, 5)
        self.units_table.setHorizontalHeaderLabels(["Сторона", "ID", "Имя", "HP", "Модели"])
        self.units_table.horizontalHeader().setStretchLastSection(True)
        self.units_table.verticalHeader().setVisible(False)
        self.units_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.units_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.units_table.setAlternatingRowColors(True)
        self.units_table.itemSelectionChanged.connect(self._sync_selection_from_table)

        self.log_view = QtWidgets.QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(500)

        copy_button = QtWidgets.QPushButton("Copy")
        clear_button = QtWidgets.QPushButton("Clear")
        copy_button.clicked.connect(self._copy_log)
        clear_button.clicked.connect(self.log_view.clear)

        fit_button = QtWidgets.QPushButton("Fit")
        fit_button.clicked.connect(self._fit_view)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.addWidget(fit_button, alignment=QtCore.Qt.AlignLeft)
        left_layout.addWidget(self.map_view)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.addWidget(self._group_status())
        right_layout.addWidget(self._group_points())
        right_layout.addWidget(self._group_units())
        right_layout.addWidget(self._group_legend())
        right_layout.addStretch()

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        log_group = QtWidgets.QGroupBox("ЖУРНАЛ")
        log_layout = QtWidgets.QVBoxLayout(log_group)
        log_layout.addWidget(self.log_view)
        log_buttons = QtWidgets.QHBoxLayout()
        log_buttons.addStretch()
        log_buttons.addWidget(copy_button)
        log_buttons.addWidget(clear_button)
        log_layout.addLayout(log_buttons)

        central = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central)
        central_layout.addWidget(splitter, stretch=3)
        central_layout.addWidget(log_group, stretch=1)
        self.setCentralWidget(central)

        self._apply_dark_theme()
        self._fit_view()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self._poll_state)
        self.timer.start()

        self._poll_state()

    def _apply_dark_theme(self):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Theme.background)
        palette.setColor(QtGui.QPalette.Base, Theme.panel)
        palette.setColor(QtGui.QPalette.Text, Theme.text)
        palette.setColor(QtGui.QPalette.Button, Theme.panel)
        palette.setColor(QtGui.QPalette.ButtonText, Theme.text)
        palette.setColor(QtGui.QPalette.Highlight, Theme.model)
        palette.setColor(QtGui.QPalette.HighlightedText, Theme.text)
        self.setPalette(palette)
        self.setStyleSheet(
            "QGroupBox { font-weight: bold; }"
            "QHeaderView::section { background-color: #2a2d31; padding: 4px; }"
            "QTableWidget { gridline-color: #3a3d41; }"
        )

    def _group_status(self):
        box = QtWidgets.QGroupBox("СТАТУС")
        layout = QtWidgets.QVBoxLayout(box)
        layout.addWidget(self.status_round)
        layout.addWidget(self.status_turn)
        layout.addWidget(self.status_phase)
        layout.addWidget(self.status_active)
        return box

    def _group_points(self):
        box = QtWidgets.QGroupBox("ОЧКИ")
        layout = QtWidgets.QVBoxLayout(box)
        layout.addWidget(self.points_vp)
        layout.addWidget(self.points_cp)
        return box

    def _group_units(self):
        box = QtWidgets.QGroupBox("ОТРЯДЫ")
        layout = QtWidgets.QVBoxLayout(box)
        layout.addWidget(self.units_table)
        return box

    def _group_legend(self):
        box = QtWidgets.QGroupBox("ЛЕГЕНДА")
        layout = QtWidgets.QVBoxLayout(box)
        layout.addLayout(self._legend_row("Игрок", Theme.player))
        layout.addLayout(self._legend_row("Модель", Theme.model))
        layout.addLayout(self._legend_row("Цель", Theme.objective))
        return box

    def _legend_row(self, label, color):
        row = QtWidgets.QHBoxLayout()
        swatch = QtWidgets.QLabel()
        swatch.setFixedSize(14, 14)
        swatch.setStyleSheet(f"background-color: {color.name()}; border-radius: 7px;")
        row.addWidget(swatch)
        row.addWidget(QtWidgets.QLabel(label))
        row.addStretch()
        return row

    def _fit_view(self):
        rect = self.map_scene.sceneRect()
        if rect.width() > 0 and rect.height() > 0:
            self.map_view.fitInView(rect, QtCore.Qt.KeepAspectRatio)

    def _copy_log(self):
        QtWidgets.QApplication.clipboard().setText(self.log_view.toPlainText())

    def _poll_state(self):
        if self.state_watcher.load_if_changed():
            self._apply_state(self.state_watcher.state)

    def _apply_state(self, state):
        board = state.get("board", {})
        self.map_scene.update_state(state)

        self.status_round.setText(f"Раунд: {state.get('round', '—')}")
        self.status_turn.setText(f"Ход: {state.get('turn', '—')}")
        self.status_phase.setText(f"Фаза: {state.get('phase', '—')}")
        active = state.get("active")
        active_label = "Игрок" if active == "player" else "Модель" if active == "model" else "—"
        self.status_active.setText(f"Активен: {active_label}")

        vp = state.get("vp", {})
        cp = state.get("cp", {})
        self.points_vp.setText(f"VP: {vp.get('player', '—')} / {vp.get('model', '—')}")
        self.points_cp.setText(f"CP: {cp.get('player', '—')} / {cp.get('model', '—')}")

        self._populate_units_table(state.get("units", []))
        self._update_log(state.get("log_tail", []))

    def _populate_units_table(self, units):
        self.units_table.setRowCount(len(units))
        self.units_table.setSortingEnabled(False)
        self._row_lookup = []
        for row, unit in enumerate(units):
            side_label = "Игрок" if unit.get("side") == "player" else "Модель"
            values = [
                side_label,
                str(unit.get("id", "—")),
                unit.get("name", "—"),
                str(unit.get("hp", "—")),
                str(unit.get("models", "—")),
            ]
            for col, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                self.units_table.setItem(row, col, item)
            self._row_lookup.append((unit.get("side"), unit.get("id")))
        self.units_table.setSortingEnabled(True)

    def _update_log(self, lines):
        if isinstance(lines, list):
            self.log_view.setPlainText("\n".join(lines))
            self.log_view.verticalScrollBar().setValue(self.log_view.verticalScrollBar().maximum())

    def _select_row_for_unit(self, side, unit_id):
        if not hasattr(self, "_row_lookup"):
            return
        for row, key in enumerate(self._row_lookup):
            if key == (side, unit_id):
                self.units_table.selectRow(row)
                return

    def _sync_selection_from_table(self):
        selected = self.units_table.selectionModel().selectedRows()
        if not selected:
            return
        row = selected[0].row()
        if not hasattr(self, "_row_lookup") or row >= len(self._row_lookup):
            return
        side, unit_id = self._row_lookup[row]
        if side and unit_id is not None:
            self.map_scene.select_unit(side, unit_id)


def launch(state_path):
    app = QtWidgets.QApplication([])
    window = ViewerWindow(state_path)
    window.show()
    app.exec()
