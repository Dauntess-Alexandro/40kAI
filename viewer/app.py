import importlib.util
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


def apply_theme(app):
    base_font = app.font()
    base_font.setPointSize(12)
    app.setFont(base_font)

    if importlib.util.find_spec("qdarktheme") is not None:
        import qdarktheme  # type: ignore
        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
        return

    palette = app.palette()
    palette.setColor(QtGui.QPalette.Window, Theme.background)
    palette.setColor(QtGui.QPalette.Base, Theme.panel)
    palette.setColor(QtGui.QPalette.Text, Theme.text)
    palette.setColor(QtGui.QPalette.Button, Theme.panel)
    palette.setColor(QtGui.QPalette.ButtonText, Theme.text)
    palette.setColor(QtGui.QPalette.Highlight, Theme.model)
    palette.setColor(QtGui.QPalette.HighlightedText, Theme.text)
    app.setPalette(palette)


class ViewerWindow(QtWidgets.QMainWindow):
    def __init__(self, state_path):
        super().__init__()
        self.state_path = state_path
        self.setWindowTitle("40kAI — Поле боя")
        self.resize(1200, 800)

        self.state_watcher = StateWatcher(self.state_path)
        self.map_scene = MapScene(cell_size=18)
        self.map_scene.unit_selected.connect(self._select_row_for_unit)

        self.map_view = MapView(self.map_scene)
        self.map_view.setBackgroundBrush(Theme.brush(Theme.background))

        self._selected_unit_key = None
        self._units_by_key = {}
        self._row_lookup = []
        self._syncing_selection = False

        self.status_line = QtWidgets.QLabel("Раунд — • Ход — • Фаза: — • Активен: —")
        self.status_line.setWordWrap(True)

        self.points_vp = QtWidgets.QLabel("VP —–—")
        self.points_cp = QtWidgets.QLabel("CP —–—")
        self.points_vp.setAlignment(QtCore.Qt.AlignCenter)
        self.points_cp.setAlignment(QtCore.Qt.AlignCenter)

        self.units_table = QtWidgets.QTableWidget(0, 7)
        self.units_table.setHorizontalHeaderLabels(
            ["Сторона", "ID", "Имя", "HP", "Модели", "X", "Y"]
        )
        self.units_table.horizontalHeader().setStretchLastSection(False)
        self.units_table.verticalHeader().setVisible(False)
        self.units_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.units_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.units_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.units_table.setAlternatingRowColors(True)
        self.units_table.setTextElideMode(QtCore.Qt.ElideRight)
        self.units_table.setWordWrap(False)
        self.units_table.verticalHeader().setDefaultSectionSize(30)
        header = self.units_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.units_table.itemSelectionChanged.connect(self._sync_selection_from_table)
        self.units_table.itemDoubleClicked.connect(self._center_on_unit_from_table)

        self.log_view = QtWidgets.QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(500)
        self.log_view.setPlaceholderText("Журнал событий пуст")
        self.log_view.setWordWrapMode(QtGui.QTextOption.NoWrap)

        copy_button = QtWidgets.QPushButton("Копировать")
        clear_button = QtWidgets.QPushButton("Очистить")
        copy_button.clicked.connect(self._copy_log)
        clear_button.clicked.connect(self.log_view.clear)

        fit_button = QtWidgets.QPushButton("Уместить")
        fit_button.clicked.connect(self._fit_view)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(12)
        left_layout.addWidget(fit_button, alignment=QtCore.Qt.AlignLeft)
        left_layout.addWidget(self.map_view)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(12)
        right_layout.addWidget(self._section_header("КОМАНДНЫЙ ПУНКТ"))
        right_layout.addWidget(self._group_status())
        right_layout.addWidget(self._group_points())
        right_layout.addWidget(self._group_selected_unit())
        right_layout.addWidget(self._group_units())
        right_layout.addWidget(self._group_legend())
        right_layout.addWidget(self._group_hints())
        right_layout.addStretch()

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        self.autoscroll_checkbox = QtWidgets.QCheckBox("Автопрокрутка")
        self.autoscroll_checkbox.setChecked(True)
        self.log_filter = QtWidgets.QComboBox()
        self.log_filter.addItems(["Все", "Ходы", "Бой", "Ошибки"])

        log_group = self._group_log(copy_button, clear_button)

        vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        vertical_splitter.addWidget(splitter)
        vertical_splitter.addWidget(log_group)
        vertical_splitter.setStretchFactor(0, 4)
        vertical_splitter.setStretchFactor(1, 1)
        vertical_splitter.setSizes([700, 220])

        central = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central)
        central_layout.addWidget(vertical_splitter)
        self.setCentralWidget(central)

        self._apply_styles()
        self._update_selected_panel()
        self._fit_view()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self._poll_state)
        self.timer.start()

        self._poll_state()

    def _apply_styles(self):
        card_style = f"""
        QFrame#Card {{
            background-color: {Theme.card.name()};
            border: 1px solid #32363c;
            border-radius: 12px;
        }}
        QLabel#CardTitle {{
            color: {Theme.text.name()};
            font-weight: 700;
        }}
        QLabel#SectionHeader {{
            color: {Theme.text.name()};
            font-weight: 700;
        }}
        QLabel#MutedText {{
            color: {Theme.muted.name()};
        }}
        QLabel#PointsValue {{
            color: {Theme.text.name()};
            font-weight: 700;
        }}
        QLabel#Badge {{
            padding: 2px 8px;
            border-radius: 8px;
            font-weight: 700;
            color: #0b0c0f;
        }}
        QHeaderView::section {{
            background-color: {Theme.panel.name()};
            padding: 6px;
            border: none;
        }}
        QTableWidget {{
            background-color: {Theme.panel.name()};
            gridline-color: #2f3236;
            border: none;
        }}
        QTableWidget::item {{
            padding: 6px;
        }}
        QPlainTextEdit {{
            background-color: {Theme.panel.name()};
            border: 1px solid #2f3236;
            border-radius: 8px;
        }}
        """
        self.setStyleSheet(card_style)
        self._apply_fonts()

    def _apply_fonts(self):
        header_font = QtGui.QFont(self.font())
        header_font.setPointSize(15)
        header_font.setBold(True)
        section_font = QtGui.QFont(self.font())
        section_font.setPointSize(14)
        section_font.setBold(True)
        points_font = QtGui.QFont(self.font())
        points_font.setPointSize(16)
        points_font.setBold(True)

        self.status_line.setFont(self.font())
        self.points_vp.setFont(points_font)
        self.points_cp.setFont(points_font)

        for label in self.findChildren(QtWidgets.QLabel, "CardTitle"):
            label.setFont(section_font)
        for label in self.findChildren(QtWidgets.QLabel, "SectionHeader"):
            label.setFont(header_font)

        fixed_font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        fixed_font.setPointSize(11)
        self.log_view.setFont(fixed_font)

    def _section_header(self, title):
        label = QtWidgets.QLabel(title)
        label.setObjectName("SectionHeader")
        return label

    def _build_card(self, title):
        frame = QtWidgets.QFrame()
        frame.setObjectName("Card")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("CardTitle")
        layout.addWidget(title_label)
        return frame, layout

    def _group_status(self):
        box, layout = self._build_card("СТАТУС")
        layout.addWidget(self.status_line)
        return box

    def _group_points(self):
        box, layout = self._build_card("ОЧКИ")
        points_layout = QtWidgets.QHBoxLayout()
        points_layout.setSpacing(16)
        points_layout.addWidget(self.points_vp)
        points_layout.addWidget(self.points_cp)
        layout.addLayout(points_layout)
        return box

    def _group_units(self):
        box, layout = self._build_card("ОТРЯДЫ")
        layout.addWidget(self.units_table)
        return box

    def _group_selected_unit(self):
        box, layout = self._build_card("ВЫБРАННЫЙ ОТРЯД")
        grid = QtWidgets.QGridLayout()

        self.selected_name = QtWidgets.QLabel("—")
        self.selected_name.setObjectName("MutedText")
        self.selected_side = QtWidgets.QLabel("—")
        self.selected_id = QtWidgets.QLabel("—")
        self.selected_hp = QtWidgets.QLabel("—")
        self.selected_models = QtWidgets.QLabel("—")
        self.selected_pos = QtWidgets.QLabel("—")

        grid.addWidget(QtWidgets.QLabel("Имя:"), 0, 0)
        grid.addWidget(self.selected_name, 0, 1)
        grid.addWidget(QtWidgets.QLabel("Сторона:"), 1, 0)
        grid.addWidget(self.selected_side, 1, 1)
        grid.addWidget(QtWidgets.QLabel("ID:"), 2, 0)
        grid.addWidget(self.selected_id, 2, 1)
        grid.addWidget(QtWidgets.QLabel("HP:"), 3, 0)
        grid.addWidget(self.selected_hp, 3, 1)
        grid.addWidget(QtWidgets.QLabel("Модели:"), 4, 0)
        grid.addWidget(self.selected_models, 4, 1)
        grid.addWidget(QtWidgets.QLabel("Координаты:"), 5, 0)
        grid.addWidget(self.selected_pos, 5, 1)

        layout.addLayout(grid)

        button_row = QtWidgets.QHBoxLayout()
        self.center_button = QtWidgets.QPushButton("Центрировать")
        self.clear_selection_button = QtWidgets.QPushButton("Сбросить выделение")
        self.center_button.clicked.connect(self._center_on_selected_unit)
        self.clear_selection_button.clicked.connect(self._clear_selection)
        button_row.addWidget(self.center_button)
        button_row.addWidget(self.clear_selection_button)
        layout.addLayout(button_row)
        return box

    def _group_legend(self):
        box, layout = self._build_card("ЛЕГЕНДА")
        layout.addLayout(self._legend_row("Игрок", Theme.player))
        layout.addLayout(self._legend_row("Модель", Theme.model))
        layout.addLayout(self._legend_row("Цель", Theme.objective))
        return box

    def _group_hints(self):
        box, layout = self._build_card("ПОДСКАЗКИ")
        hint = QtWidgets.QLabel(
            "• Клик по отряду на карте выделяет его в таблице.\n"
            "• Двойной клик по строке — центрирование камеры.\n"
            "• Колесо мыши — масштаб, перетаскивание — панорама."
        )
        hint.setWordWrap(True)
        hint.setObjectName("MutedText")
        layout.addWidget(hint)
        return box

    def _group_log(self, copy_button, clear_button):
        box, layout = self._build_card("ЖУРНАЛ СОБЫТИЙ")
        controls = QtWidgets.QHBoxLayout()
        controls.addWidget(copy_button)
        controls.addWidget(clear_button)
        controls.addWidget(self.autoscroll_checkbox)
        controls.addStretch()
        controls.addWidget(self.log_filter)
        layout.addLayout(controls)
        layout.addWidget(self.log_view)
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

    @staticmethod
    def _side_label(side):
        if side in ("player", "enemy"):
            return "Игрок"
        if side == "model":
            return "Модель"
        return "—"

    @staticmethod
    def _side_color(side):
        if side in ("player", "enemy"):
            return Theme.player
        if side == "model":
            return Theme.model
        return Theme.muted

    def _apply_state(self, state):
        self.map_scene.update_state(state)

        active = state.get("active")
        active_label = self._side_label(active)
        self.status_line.setText(
            "Раунд {round} • Ход {turn} • Фаза: {phase} • Активен: {active}".format(
                round=state.get("round", "—"),
                turn=state.get("turn", "—"),
                phase=state.get("phase", "—"),
                active=active_label,
            )
        )

        vp = state.get("vp", {})
        cp = state.get("cp", {})
        self.points_vp.setText(f"VP {vp.get('player', '—')}–{vp.get('model', '—')}")
        self.points_cp.setText(f"CP {cp.get('player', '—')}–{cp.get('model', '—')}")

        self._populate_units_table(state.get("units", []))
        self._update_log(state.get("log_tail", []))

        if self._selected_unit_key and self._selected_unit_key in self._units_by_key:
            self._select_unit_by_key(*self._selected_unit_key, update_table=True)
        else:
            self._clear_selection(update_table=True)

    def _populate_units_table(self, units):
        self.units_table.setSortingEnabled(False)
        self.units_table.setRowCount(len(units))
        self._row_lookup = []
        self._units_by_key = {}
        for row, unit in enumerate(units):
            side = unit.get("side")
            side_label = self._side_label(side)
            side_color = self._side_color(side)

            badge = QtWidgets.QLabel(side_label)
            badge.setObjectName("Badge")
            badge.setAlignment(QtCore.Qt.AlignCenter)
            badge.setStyleSheet(
                f"background-color: {side_color.name()}; color: #0c0f12; font-weight: 700;"
            )
            self.units_table.setCellWidget(row, 0, badge)

            values = [
                str(unit.get("id", "—")),
                unit.get("name", "—"),
                str(unit.get("hp", "—")),
                str(unit.get("models", "—")),
                str(unit.get("x", "—")),
                str(unit.get("y", "—")),
            ]
            for col, value in enumerate(values, start=1):
                item = QtWidgets.QTableWidgetItem(value)
                if col == 2:
                    item.setToolTip(value)
                if col in (1, 3, 4, 5, 6):
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.units_table.setItem(row, col, item)
            key = (side, unit.get("id"))
            self._row_lookup.append(key)
            if key[0] is not None and key[1] is not None:
                self._units_by_key[key] = unit

    def _update_log(self, lines):
        if isinstance(lines, list):
            self.log_view.setPlainText("\n".join(lines))
            if self.autoscroll_checkbox.isChecked():
                self.log_view.verticalScrollBar().setValue(
                    self.log_view.verticalScrollBar().maximum()
                )

    def _select_row_for_unit(self, side, unit_id):
        if self._syncing_selection:
            return
        self._syncing_selection = True
        try:
            self._selected_unit_key = (side, unit_id)
            self._update_selected_panel()
            if not hasattr(self, "_row_lookup"):
                return
            for row, key in enumerate(self._row_lookup):
                if key == (side, unit_id):
                    self.units_table.selectRow(row)
                    return
        finally:
            self._syncing_selection = False

    def _select_unit_by_key(self, side, unit_id, update_table=False):
        if side is None or unit_id is None:
            return
        self._selected_unit_key = (side, unit_id)
        self._update_selected_panel()
        self._syncing_selection = True
        try:
            self.map_scene.select_unit(side, unit_id)
            if update_table:
                for row, key in enumerate(self._row_lookup):
                    if key == (side, unit_id):
                        self.units_table.selectRow(row)
                        break
        finally:
            self._syncing_selection = False

    def _center_on_unit(self, side, unit_id):
        item = self.map_scene.unit_items.get((side, unit_id))
        if item:
            self.map_view.centerOn(item)

    def _center_on_unit_from_table(self, item):
        row = item.row()
        if row >= len(self._row_lookup):
            return
        side, unit_id = self._row_lookup[row]
        if side is None or unit_id is None:
            return
        self._center_on_unit(side, unit_id)

    def _center_on_selected_unit(self):
        if not self._selected_unit_key:
            return
        self._center_on_unit(*self._selected_unit_key)

    def _sync_selection_from_table(self):
        selected = self.units_table.selectionModel().selectedRows()
        if not selected or self._syncing_selection:
            return
        row = selected[0].row()
        if not hasattr(self, "_row_lookup") or row >= len(self._row_lookup):
            return
        side, unit_id = self._row_lookup[row]
        if side and unit_id is not None:
            self._select_unit_by_key(side, unit_id)

    def _clear_selection(self, update_table=True):
        self._selected_unit_key = None
        self.map_scene.clearSelection()
        if update_table:
            self.units_table.clearSelection()
        self._update_selected_panel()

    def _update_selected_panel(self):
        if not self._selected_unit_key:
            self.selected_name.setText("—")
            self.selected_side.setText("—")
            self.selected_id.setText("—")
            self.selected_hp.setText("—")
            self.selected_models.setText("—")
            self.selected_pos.setText("—")
            self.center_button.setEnabled(False)
            self.clear_selection_button.setEnabled(False)
            return
        unit = self._units_by_key.get(self._selected_unit_key)
        if not unit:
            return
        side = unit.get("side")
        self.selected_name.setText(unit.get("name", "—"))
        self.selected_side.setText(self._side_label(side))
        self.selected_id.setText(str(unit.get("id", "—")))
        self.selected_hp.setText(str(unit.get("hp", "—")))
        self.selected_models.setText(str(unit.get("models", "—")))
        self.selected_pos.setText(
            "({x}, {y})".format(x=unit.get("x", "—"), y=unit.get("y", "—"))
        )
        self.center_button.setEnabled(True)
        self.clear_selection_button.setEnabled(True)


def launch(state_path):
    app = QtWidgets.QApplication([])
    apply_theme(app)
    window = ViewerWindow(state_path)
    window.show()
    app.exec()
