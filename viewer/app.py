import torch
import json
import os
import queue
import re
import sys
import time
from collections import OrderedDict, deque
from dataclasses import dataclass
from typing import Callable, Deque, Optional, Tuple
from datetime import datetime
from PySide6 import QtCore, QtGui, QtWidgets

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VIEWER_CONFIG_PATH = os.path.join(ROOT_DIR, "viewer", "viewer_config.json")
GYM_PATH = os.path.join(ROOT_DIR, "gym_mod")
if GYM_PATH not in sys.path:
    sys.path.insert(0, GYM_PATH)


def load_viewer_config() -> dict:
    defaults = {
        "cell_size": 24,
        "unit_icon_scale": 2.75,
        "model_icon_scale": 0.75,
    }
    try:
        with open(VIEWER_CONFIG_PATH, "r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return defaults
    if not isinstance(loaded, dict):
        return defaults
    cfg = dict(defaults)
    cfg.update(loaded)
    return cfg

from viewer.opengl_view import OpenGLBoardWidget
from viewer.gun_fx import get_gun_fx_config
from viewer.state import StateWatcher
from viewer.styles import Theme
from viewer.model_log_tree import render_model_log_flat

from gym_mod.engine.game_controller import GameController
from gym_mod.engine.game_io import parse_dice_values
from gym_mod.engine.event_bus import get_event_bus


@dataclass
class PendingReport:
    ts: str
    report_type: str
    attacker_id: Optional[int] = None
    target_id: Optional[int] = None
    weapon_name: Optional[str] = None
    damage: Optional[float] = None


@dataclass
class FxShotEvent:
    ts: str
    report_type: str
    attacker_id: int
    target_id: int
    weapon_name: str
    damage: float


class FxLogParser:
    def __init__(
        self,
        on_event: Callable[[FxShotEvent], None],
        debug: Callable[[str], None],
        seen_max: int = 300,
    ) -> None:
        self._on_event = on_event
        self._debug = debug
        self._pending: Deque[PendingReport] = deque()
        self._seen: OrderedDict[Tuple, None] = OrderedDict()
        self._seen_max = seen_max

    def reset(self, preserve_seen: bool = True) -> None:
        self._pending.clear()
        if not preserve_seen:
            self._seen.clear()

    def replay_lines(self, lines) -> None:
        if not lines:
            return
        self._debug(f"FX: перепроигрываю {len(lines)} строк(и) лога.")
        for line in lines:
            self.consume_line(str(line))

    def consume_line(self, line: str) -> None:
        if not line:
            return
        ts, text = self._split_timestamp(line)
        if "📌 --- ОТЧЁТ ПО" in text:
            report_type = "overwatch" if "OVERWATCH" in text.upper() else "shooting"
            self._pending.append(PendingReport(ts=ts, report_type=report_type))
            self._debug(f"FX: старт отчёта ({report_type}), ts={ts}.")
            return

        if not self._pending:
            return
        current = self._pending[-1]

        shot_match = re.search(r"Стреляет:\s*Unit\s+(\d+).*?цель:\s*Unit\s+(\d+)", text, re.IGNORECASE)
        if shot_match:
            current.attacker_id = int(shot_match.group(1))
            current.target_id = int(shot_match.group(2))
            self._debug(
                "FX: найдена строка стрельбы "
                f"(attacker={current.attacker_id}, target={current.target_id})."
            )
            return

        weapon_match = re.search(r"Оружие:\s*(.+)", text, re.IGNORECASE)
        if weapon_match:
            current.weapon_name = weapon_match.group(1).strip()
            self._debug(f"FX: найдена строка оружия: {current.weapon_name}.")
            return

        damage_match = re.search(r"Итог по движку:.*?=\s*([-+]?\d+(?:\.\d+)?)", text)
        if damage_match:
            current.damage = float(damage_match.group(1))
            self._debug(f"FX: найден итог урона = {current.damage}.")
            self._finalize_report(current, reason="damage")
            return

        if "📌 -------------------------" in text:
            if current.damage is None:
                self._debug("FX: разделитель отчёта без итога, используем урон 0.0.")
            self._finalize_report(current, reason="separator")

    def _split_timestamp(self, line: str) -> Tuple[str, str]:
        match = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*(.+)$", line)
        if match:
            return match.group(1), match.group(2)
        return "no-ts", line

    def _finalize_report(self, report: PendingReport, reason: str) -> None:
        if report.attacker_id is None or report.target_id is None or not report.weapon_name:
            self._debug("FX: отчёт неполный, эффект пропущен.")
            self._pending.pop()
            return
        damage = report.damage if report.damage is not None else 0.0
        event = FxShotEvent(
            ts=report.ts,
            report_type=report.report_type,
            attacker_id=report.attacker_id,
            target_id=report.target_id,
            weapon_name=report.weapon_name,
            damage=damage,
        )
        key = (
            event.ts,
            event.report_type,
            event.attacker_id,
            event.target_id,
            event.weapon_name,
            event.damage,
        )
        if key in self._seen:
            self._debug("FX: дубликат отчёта, эффект не создаём.")
            self._pending.pop()
            return
        self._seen[key] = None
        if len(self._seen) > self._seen_max:
            self._seen.popitem(last=False)
        self._debug(
            "FX: создан FxShotEvent "
            f"(attacker={event.attacker_id}, target={event.target_id}, "
            f"weapon={event.weapon_name}, damage={event.damage})."
        )
        self._on_event(event)
        self._pending.pop()


class ViewerWindow(QtWidgets.QMainWindow):
    def __init__(self, state_path, model_path=None):
        super().__init__()
        self.state_path = state_path
        self.setWindowTitle("40kAI Viewer")
        self.resize(2560, 1440)

        self.controller = GameController(model_path=model_path, state_path=state_path)
        self._pending_request = None
        self._pending_requests: Deque = deque()
        self._awaiting_player_action = False
        self._active_unit_id = None
        self._active_unit_side = None
        self._selected_unit_id = None
        self._selected_unit_side = None
        self._syncing_table_selection = False
        self._current_target_id = None
        self._last_shooter_id = None
        self._show_objective_radius = True
        self._units_by_key = {}
        self._unit_row_by_key = {}
        self._did_initial_fit = False
        self._board_debug_logged = False

        self._viewer_config = load_viewer_config()
        cell_size = int(self._viewer_config.get("cell_size", 24))
        unit_icon_scale = float(self._viewer_config.get("unit_icon_scale", 2.75))
        model_icon_scale = float(self._viewer_config.get("model_icon_scale", 0.75))

        self.state_watcher = StateWatcher(self.state_path)
        self.map_scene = OpenGLBoardWidget(
            cell_size=max(8, cell_size),
            unit_icon_scale=max(0.25, unit_icon_scale),
            model_icon_scale=max(0.2, model_icon_scale),
        )
        self.map_scene.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.map_scene.unit_selected.connect(self._select_row_for_unit)

        self.status_round = QtWidgets.QLabel("Раунд: —")
        self.status_turn = QtWidgets.QLabel("Ход: —")
        self.status_phase = QtWidgets.QLabel("Фаза: —")
        self.status_active = QtWidgets.QLabel("Активен: —")
        self.status_deployment = QtWidgets.QLabel("Деплой: ожидание ролл-оффа")

        self.points_vp_player = QtWidgets.QLabel("Player VP: —")
        self.points_vp_model = QtWidgets.QLabel("Model VP: —")
        self.points_cp_player = QtWidgets.QLabel("Player CP: —")
        self.points_cp_model = QtWidgets.QLabel("Model CP: —")

        self.units_table = QtWidgets.QTableWidget(0, 5)
        self.units_table.setHorizontalHeaderLabels(["Сторона", "ID", "Имя", "HP", "Модели"])
        header = self.units_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.sortIndicatorChanged.connect(self._rebuild_unit_row_mapping)
        self.units_table.verticalHeader().setVisible(False)
        self.units_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.units_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.units_table.setAlternatingRowColors(True)
        self.units_table.itemSelectionChanged.connect(self._sync_selection_from_table)
        self._apply_units_table_font()

        self._log_entries = []
        self._current_turn_number = None
        self._current_turn_side = None
        self._log_tail_snapshot = None
        self._model_events_snapshot = None
        self._model_event_queue: queue.Queue = queue.Queue()
        self._model_log_source = None
        self._model_events_stream = []
        self._model_events_current = []
        self._log_tabs = {}
        self._log_tab_indices = {}
        self._log_tab_programmatic_switch = False
        self._last_manual_log_tab_index = None
        self._fx_shot_queue: Deque[FxShotEvent] = deque()
        self._fx_parser = FxLogParser(self._enqueue_fx_event, self._fx_debug, seen_max=400)
        self._log_tab_defs = [
            ("player", "Все ходы игрока"),
            ("model", "Все ходы модели"),
            ("key", "Ключевые события"),
        ]
        self._max_log_lines = 5000
        self._log_file_path = os.path.join(ROOT_DIR, "LOGS_FOR_AGENTS.md")
        self._log_file_max_bytes = 5 * 1024 * 1024
        self._last_active_side = None
        self._init_log_viewer()
        self.add_log_line("[VIEWER] Рендер: OpenGL (QOpenGLWidget).")
        self.add_log_line("[VIEWER] Фоллбэк-рендер не активирован.")
        try:
            get_event_bus().subscribe(self._on_event_bus_event)
        except Exception:
            pass

        fit_button = QtWidgets.QPushButton("Fit")
        fit_button.clicked.connect(self._fit_view)

        left_widget = QtWidgets.QWidget()
        left_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)
        left_layout.addWidget(fit_button, alignment=QtCore.Qt.AlignLeft)
        left_layout.addWidget(self.map_scene, 1)

        log_group = QtWidgets.QGroupBox("ЖУРНАЛ")
        log_layout = QtWidgets.QVBoxLayout(log_group)
        log_layout.addLayout(self._log_controls_layout)
        log_layout.addWidget(self.log_tabs)
        log_group.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        command_group = QtWidgets.QGroupBox("КОМАНДЫ")
        command_layout = QtWidgets.QVBoxLayout(command_group)
        self.command_prompt = QtWidgets.QLabel("Ожидаю команду...")
        self.command_prompt.setWordWrap(True)
        command_layout.addWidget(self.command_prompt)
        self.command_hint = QtWidgets.QLabel("Горячие клавиши: —")
        self.command_hint.setStyleSheet(f"color: {Theme.muted.name()};")
        command_layout.addWidget(self.command_hint)

        self.command_stack = QtWidgets.QStackedWidget()
        self._build_command_pages()
        command_layout.addWidget(self.command_stack)

        right_top_widget = QtWidgets.QWidget()
        right_top_layout = QtWidgets.QVBoxLayout(right_top_widget)
        right_top_layout.setSpacing(8)
        right_top_layout.addWidget(self._group_status())
        right_top_layout.addWidget(self._group_points())
        right_top_layout.addWidget(self._group_units())
        right_top_layout.addWidget(self._group_legend())
        right_top_layout.addWidget(command_group)
        right_top_layout.addStretch()

        self._right_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self._right_splitter.addWidget(right_top_widget)
        self._right_splitter.addWidget(log_group)
        self._right_splitter.setStretchFactor(0, 3)
        self._right_splitter.setStretchFactor(1, 2)
        self._right_splitter.setChildrenCollapsible(False)

        self._top_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self._top_splitter.addWidget(left_widget)
        self._top_splitter.addWidget(self._right_splitter)
        self._top_splitter.setStretchFactor(0, 1)
        self._top_splitter.setStretchFactor(1, 0)
        self._top_splitter.setChildrenCollapsible(False)
        self._right_splitter.setMinimumWidth(380)
        self._right_splitter.setMaximumWidth(450)

        central = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_layout.addWidget(self._top_splitter)
        self.setCentralWidget(central)

        self._apply_dark_theme()
        self._build_toolbar()
        QtCore.QTimer.singleShot(0, self._apply_initial_splitter_sizes)
        app = QtWidgets.QApplication.instance()
        if app is not None:
            app.installEventFilter(self)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self._poll_state)
        self.timer.start()

        self._poll_state()
        QtCore.QTimer.singleShot(0, self._start_controller)

    def _build_toolbar(self):
        toolbar = self.addToolBar("Вид")
        toolbar.setMovable(False)
        self.toggle_objective_radius = QtGui.QAction("Показать радиус целей", self)
        self.toggle_objective_radius.setCheckable(True)
        self.toggle_objective_radius.setChecked(True)
        self.toggle_objective_radius.toggled.connect(self._toggle_objective_radius)
        toolbar.addAction(self.toggle_objective_radius)

    def _toggle_objective_radius(self, checked):
        self._show_objective_radius = checked
        self.map_scene.set_objective_radius_visible(checked)
        self.map_scene.refresh_overlays()

    def _apply_dark_theme(self):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Theme.background)
        palette.setColor(QtGui.QPalette.Base, Theme.panel)
        palette.setColor(QtGui.QPalette.Text, Theme.text)
        palette.setColor(QtGui.QPalette.Button, Theme.panel)
        palette.setColor(QtGui.QPalette.ButtonText, Theme.text)
        palette.setColor(QtGui.QPalette.Highlight, Theme.model)
        palette.setColor(QtGui.QPalette.HighlightedText, Theme.text)
        palette.setColor(QtGui.QPalette.PlaceholderText, Theme.muted)
        self.setPalette(palette)
        self.setStyleSheet(Theme.stylesheet())

    def _apply_units_table_font(self):
        body_font = Theme.font(size=11)
        header_font = Theme.font(size=10, bold=True)
        self.units_table.setFont(body_font)
        header = self.units_table.horizontalHeader()
        header.setFont(header_font)
        self.units_table.verticalHeader().setDefaultSectionSize(22)

    def _group_status(self):
        box = QtWidgets.QGroupBox("СТАТУС")
        layout = QtWidgets.QVBoxLayout(box)
        layout.addWidget(self.status_round)
        layout.addWidget(self.status_turn)
        layout.addWidget(self.status_phase)
        layout.addWidget(self.status_active)
        layout.addWidget(self.status_deployment)
        return box

    def _group_points(self):
        box = QtWidgets.QGroupBox("ОЧКИ")
        layout = QtWidgets.QVBoxLayout(box)
        layout.addWidget(self.points_vp_player)
        layout.addWidget(self.points_vp_model)
        layout.addWidget(self.points_cp_player)
        layout.addWidget(self.points_cp_model)
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

    def _build_command_pages(self):
        self._command_pages = {}

        text_page = QtWidgets.QWidget()
        text_layout = QtWidgets.QHBoxLayout(text_page)
        self.command_input = QtWidgets.QLineEdit()
        self.command_input.setPlaceholderText("Введите команду...")
        self.command_send = QtWidgets.QPushButton("Отправить")
        self.command_input.returnPressed.connect(self._submit_text)
        self.command_send.clicked.connect(self._submit_text)
        text_layout.addWidget(self.command_input)
        text_layout.addWidget(self.command_send)
        self._command_pages["text"] = self.command_stack.addWidget(text_page)

        direction_page = QtWidgets.QWidget()
        direction_layout = QtWidgets.QGridLayout(direction_page)
        self.direction_buttons = {}
        direction_map = {
            "up": "↑",
            "down": "↓",
            "left": "←",
            "right": "→",
            "none": "Нет",
        }
        self.direction_buttons["up"] = QtWidgets.QPushButton(direction_map["up"])
        self.direction_buttons["down"] = QtWidgets.QPushButton(direction_map["down"])
        self.direction_buttons["left"] = QtWidgets.QPushButton(direction_map["left"])
        self.direction_buttons["right"] = QtWidgets.QPushButton(direction_map["right"])
        self.direction_buttons["none"] = QtWidgets.QPushButton(direction_map["none"])
        self.direction_buttons["up"].clicked.connect(lambda: self._submit_answer("up"))
        self.direction_buttons["down"].clicked.connect(lambda: self._submit_answer("down"))
        self.direction_buttons["left"].clicked.connect(lambda: self._submit_answer("left"))
        self.direction_buttons["right"].clicked.connect(lambda: self._submit_answer("right"))
        self.direction_buttons["none"].clicked.connect(lambda: self._submit_answer("none"))
        direction_layout.addWidget(self.direction_buttons["up"], 0, 1)
        direction_layout.addWidget(self.direction_buttons["left"], 1, 0)
        direction_layout.addWidget(self.direction_buttons["none"], 1, 1)
        direction_layout.addWidget(self.direction_buttons["right"], 1, 2)
        direction_layout.addWidget(self.direction_buttons["down"], 2, 1)
        self._command_pages["direction"] = self.command_stack.addWidget(direction_page)

        bool_page = QtWidgets.QWidget()
        bool_layout = QtWidgets.QHBoxLayout(bool_page)
        self.bool_yes = QtWidgets.QPushButton("Да")
        self.bool_no = QtWidgets.QPushButton("Нет")
        self.bool_yes.clicked.connect(lambda: self._submit_answer(True))
        self.bool_no.clicked.connect(lambda: self._submit_answer(False))
        bool_layout.addWidget(self.bool_yes)
        bool_layout.addWidget(self.bool_no)
        self._command_pages["bool"] = self.command_stack.addWidget(bool_page)

        int_page = QtWidgets.QWidget()
        int_layout = QtWidgets.QHBoxLayout(int_page)
        self.int_spin = QtWidgets.QSpinBox()
        self.int_spin.setRange(0, 999)
        self.int_ok = QtWidgets.QPushButton("ОК")
        self.int_ok.clicked.connect(lambda: self._submit_answer(self.int_spin.value()))
        int_layout.addWidget(self.int_spin)
        int_layout.addWidget(self.int_ok)
        self._command_pages["int"] = self.command_stack.addWidget(int_page)

        choice_page = QtWidgets.QWidget()
        choice_layout = QtWidgets.QHBoxLayout(choice_page)
        self.choice_combo = QtWidgets.QComboBox()
        self.choice_combo.currentTextChanged.connect(self._on_choice_target_changed)
        self.choice_ok = QtWidgets.QPushButton("ОК")
        self.choice_ok.clicked.connect(self._submit_choice)
        choice_layout.addWidget(self.choice_combo)
        choice_layout.addWidget(self.choice_ok)
        self._command_pages["choice"] = self.command_stack.addWidget(choice_page)

        self.command_stack.setCurrentIndex(self._command_pages["text"])

    def _set_request(self, request):
        if request is None and self._pending_requests:
            next_request = self._pending_requests.popleft()
            current_unit = self._extract_unit_id(getattr(self._pending_request, "prompt", ""))
            next_unit = self._extract_unit_id(getattr(next_request, "prompt", ""))
            if current_unit is not None or next_unit is not None:
                current_label = self._format_unit_label(current_unit)
                next_label = self._format_unit_label(next_unit)
                self.add_log_line(
                    f"REQ: finished request for Unit {current_label}, "
                    f"dequeued next request Unit {next_label}"
                )
            self._pending_request = None
            self._awaiting_player_action = False
            self._set_request(next_request)
            return
        if request is not None and self._awaiting_player_action:
            current_unit = self._extract_unit_id(getattr(self._pending_request, "prompt", ""))
            next_unit = self._extract_unit_id(getattr(request, "prompt", ""))
            if current_unit is not None or next_unit is not None:
                current_label = self._format_unit_label(current_unit)
                next_label = self._format_unit_label(next_unit)
                self.add_log_line(
                    f"REQ: queued request for Unit {next_label} (waiting for Unit {current_label})"
                )
            self._pending_requests.append(request)
            return

        self._pending_request = request
        self._awaiting_player_action = request is not None
        if request is None:
            if self.controller.is_finished:
                self.command_prompt.setText("Игра завершена.")
            else:
                self.command_prompt.setText("Команда не требуется.")
            self.command_stack.setEnabled(False)
            self.command_hint.setText("Горячие клавиши: —")
            self._refresh_active_context()
            return

        self._maybe_reset_target_for_request(request)
        self.command_prompt.setText(request.prompt)
        self.command_stack.setEnabled(True)
        kind = getattr(request, "kind", "text")
        if kind == "direction":
            self.command_input.setPlaceholderText("Введите команду...")
            self.command_stack.setCurrentIndex(self._command_pages["direction"])
        elif kind == "bool":
            self.command_input.setPlaceholderText("Введите команду...")
            self.command_stack.setCurrentIndex(self._command_pages["bool"])
        elif kind == "int":
            min_value = request.min_value if request.min_value is not None else 0
            max_value = request.max_value if request.max_value is not None else 999
            self.int_spin.setRange(min_value, max_value)
            self.int_spin.setValue(min_value)
            self.command_input.setPlaceholderText("Введите команду...")
            self.command_stack.setCurrentIndex(self._command_pages["int"])
        elif kind == "choice":
            self.choice_combo.clear()
            if request.options:
                self.choice_combo.addItems([str(opt) for opt in request.options])
                self.command_stack.setCurrentIndex(self._command_pages["choice"])
                if self._is_target_request(request):
                    self._sync_target_from_choice(self.choice_combo.currentText())
                    self._set_confirm_enabled(self._current_target_id is not None)
            else:
                self.command_stack.setCurrentIndex(self._command_pages["text"])
            self.command_input.setPlaceholderText("Введите команду...")
        elif kind == "dice":
            count = request.count or 0
            example_values = [str((idx % 6) + 1) for idx in range(count)]
            spaced = " ".join(example_values)
            comma = ",".join(example_values)
            compact = "".join(example_values)
            self.command_input.setPlaceholderText(
                f"Например: {spaced} или {comma}"
                + (f" или {compact}" if compact else "")
            )
            self.command_stack.setCurrentIndex(self._command_pages["text"])
        else:
            self.command_input.setPlaceholderText("Введите команду...")
            self.command_stack.setCurrentIndex(self._command_pages["text"])
        self._update_command_hint(kind)
        self._refresh_active_context()

    def _finish_active_request(self) -> None:
        self._awaiting_player_action = False

    def _is_target_request(self, request) -> bool:
        if request is None:
            return False
        prompt = str(getattr(request, "prompt", "")).lower()
        return (
            "выберите цель" in prompt
            or (
                "цель" in prompt
                and (
                    "стрель" in prompt
                    or "shoot" in prompt
                    or "чардж" in prompt
                    or "charge" in prompt
                )
            )
        )

    def _maybe_reset_target_for_request(self, request) -> None:
        if not self._is_target_request(request):
            self._set_confirm_enabled(True)
            return
        shooter_id = self._extract_unit_id(getattr(request, "prompt", ""))
        if shooter_id != self._last_shooter_id:
            previous = self._last_shooter_id
            if shooter_id is not None and previous is not None:
                previous_label = self._format_unit_label(previous)
                shooter_label = self._format_unit_label(shooter_id)
                self.add_log_line(
                    f"REQ: shooter changed Unit {previous_label}->Unit {shooter_label}, target reset"
                )
            self._last_shooter_id = shooter_id
        self._reset_target_selection()
        self._set_confirm_enabled(False)

    def _reset_target_selection(self) -> None:
        self._current_target_id = None
        self.map_scene.clear_target_selection()

    def _format_unit_label(self, unit_id: Optional[int]) -> str:
        if unit_id is None:
            return "—"
        return str(unit_id)

    def _set_confirm_enabled(self, enabled: bool) -> None:
        self.command_send.setEnabled(enabled)
        self.command_input.setEnabled(enabled)
        self.bool_yes.setEnabled(enabled)
        self.bool_no.setEnabled(enabled)
        self.int_spin.setEnabled(enabled)
        self.int_ok.setEnabled(enabled)
        self.choice_combo.setEnabled(enabled)
        self.choice_ok.setEnabled(enabled)

    def _on_choice_target_changed(self, value: str) -> None:
        if not self._is_target_request(self._pending_request):
            return
        self._sync_target_from_choice(value)
        self._set_confirm_enabled(self._current_target_id is not None)

    def _sync_target_from_choice(self, value: str) -> None:
        parsed_id = self._extract_unit_id(value)
        if parsed_id is None:
            self._current_target_id = None
            return
        self._current_target_id = parsed_id
        self.map_scene.set_target_unit(parsed_id)

    def _on_target_selected(self, unit_id: int) -> None:
        if not self._is_target_request(self._pending_request):
            return
        if unit_id is None:
            return
        self._current_target_id = unit_id
        self.map_scene.set_target_unit(unit_id)
        self._set_confirm_enabled(True)
        target_label = self._format_unit_label(unit_id)
        self.add_log_line(f"REQ: target selected Unit {target_label}, confirm enabled")

    def _update_command_hint(self, kind):
        if kind == "direction":
            self.command_hint.setText("Горячие клавиши: ↑ ↓ ← →, пробел/0 — нет")
        elif kind == "bool":
            self.command_hint.setText("Горячие клавиши: Y — да, N — нет")
        elif kind == "int":
            self.command_hint.setText("Горячие клавиши: Enter — отправить")
        elif kind == "choice":
            self.command_hint.setText("Горячие клавиши: Enter — выбрать")
        else:
            self.command_hint.setText("Горячие клавиши: Enter — отправить")

    def _init_log_viewer(self):
        fixed_font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        fixed_font.setPointSize(10)

        self.log_tabs = QtWidgets.QTabWidget()
        for index, (key, label) in enumerate(self._log_tab_defs):
            view = QtWidgets.QPlainTextEdit()
            view.setReadOnly(True)
            view.setFont(fixed_font)
            view.setMaximumBlockCount(self._max_log_lines)
            self._log_tabs[key] = view
            self._log_tab_indices[key] = index
            self.log_tabs.addTab(view, label)
        self.log_tabs.currentChanged.connect(self._on_log_tab_changed)

        self.log_only_current_turn = QtWidgets.QCheckBox("Показать только текущий ход")
        self.log_only_current_turn.toggled.connect(self._refresh_log_views)

        self.log_model_verbose = QtWidgets.QCheckBox("Подробно (verbose)")
        self.log_model_verbose.toggled.connect(self._refresh_model_log_view)

        self.log_copy_turn = QtWidgets.QPushButton("Копировать ход")
        self.log_copy_turn.clicked.connect(self._copy_current_turn)
        self.log_clear = QtWidgets.QPushButton("Очистить")
        self.log_clear.clicked.connect(self._clear_log_viewer)

        self._log_controls_layout = QtWidgets.QHBoxLayout()
        self._log_controls_layout.addWidget(self.log_only_current_turn)
        self._log_controls_layout.addWidget(self.log_model_verbose)
        self._log_controls_layout.addStretch()
        self._log_controls_layout.addWidget(self.log_copy_turn)
        self._log_controls_layout.addWidget(self.log_clear)

    def _append_log(self, messages):
        if not messages:
            return
        for msg in messages:
            self.add_log_line(str(msg))

    def _on_event_bus_event(self, event):
        try:
            self._model_event_queue.put_nowait(event)
        except queue.Full:
            return

    def _drain_event_queue(self):
        drained = []
        while True:
            try:
                drained.append(self._model_event_queue.get_nowait())
            except queue.Empty:
                break
        if not drained:
            return
        if self._model_log_source in (None, "stream"):
            self._model_log_source = "stream"
            self._model_events_stream.extend(self._filter_model_events(drained))
            self._model_events_current = list(self._model_events_stream)
            self._refresh_model_log_view()

    def _start_controller(self):
        messages, request = self.controller.start()
        self._append_log(messages)
        self._set_request(request)
        self._poll_state()

    def _submit_text(self):
        text = self.command_input.text().strip()
        if self._is_target_request(self._pending_request) and self._current_target_id is None:
            return
        if not text:
            return
        if self._pending_request and getattr(self._pending_request, "kind", "") == "dice":
            count = self._pending_request.count or 0
            min_value = self._pending_request.min_value or 1
            max_value = self._pending_request.max_value or 6
            try:
                values = parse_dice_values(text, count=count, min_value=min_value, max_value=max_value)
            except ValueError as exc:
                entered = self._count_dice_entries(text)
                self.command_prompt.setText(
                    "Ошибка ввода кубов в панели «Команды»: "
                    f"{exc}. Нужно {count}, введено {entered}. "
                    "Что делать дальше: исправьте ввод и отправьте снова.\n"
                    f"{self._pending_request.prompt}"
                )
                return
            self.command_input.clear()
            self._submit_answer(values)
            return
        self.command_input.clear()
        self._submit_answer(text)

    def _submit_choice(self):
        value = self.choice_combo.currentText()
        if self._is_target_request(self._pending_request) and self._current_target_id is None:
            self._sync_target_from_choice(value)
            if self._current_target_id is None:
                return
        self._submit_answer(value)

    def _submit_answer(self, value):
        if self._pending_request is None:
            return
        finished_request = self._pending_request
        self._finish_active_request()
        messages, request = self.controller.answer(value)
        self._append_log(messages)
        if self._pending_requests:
            if request is not None:
                queued_unit = self._extract_unit_id(getattr(request, "prompt", ""))
                waiting_unit = self._extract_unit_id(getattr(finished_request, "prompt", ""))
                self._pending_requests.append(request)
                queued_label = self._format_unit_label(queued_unit)
                waiting_label = self._format_unit_label(waiting_unit)
                self.add_log_line(
                    f"REQ: queued request for Unit {queued_label} (waiting for Unit {waiting_label})"
                )
            self._set_request(None)
        else:
            self._set_request(request)
        self._poll_state()

    def _apply_initial_splitter_sizes(self) -> None:
        total_w = max(self.width(), 2560)
        right_w = max(380, min(450, int(total_w * 0.2)))
        left_w = max(1400, total_w - right_w)
        self._top_splitter.setSizes([left_w, right_w])

        total_h = max(self.height(), 800)
        top_h = int(total_h * 0.72)
        bottom_h = max(180, total_h - top_h)
        self._right_splitter.setSizes([top_h, bottom_h])

    def _fit_view(self):
        self.map_scene.fit_to_view()

    def _poll_state(self):
        if not os.path.exists(self.state_watcher.path):
            self.map_scene.set_error_message(
                "Состояние игры недоступно. Где: viewer/state.json. "
                "Что делать дальше: запустите игру и дождитесь генерации state.json."
            )
            return
        if self.state_watcher.load_if_changed():
            self._apply_state(self.state_watcher.state)

    def _apply_state(self, state):
        self.map_scene.update_state(state)
        if not self._did_initial_fit:
            self._did_initial_fit = True
            QtCore.QTimer.singleShot(0, self._fit_view)

        self._units_by_key = {}
        for unit in state.get("units", []) or []:
            self._units_by_key[(unit.get("side"), unit.get("id"))] = unit

        self.status_round.setText(f"Раунд: {state.get('round', '—')}")
        self.status_turn.setText(f"Ход: {state.get('turn', '—')}")
        self.status_phase.setText(f"Фаза: {state.get('phase', '—')}")
        active = state.get("active") or state.get("active_side")
        active_label = "Игрок" if active == "player" else "Модель" if active == "model" else "—"
        self.status_active.setText(f"Активен: {active_label}")

        deployment = state.get("deployment", {}) if isinstance(state.get("deployment", {}), dict) else {}
        attacker = deployment.get("attacker") or state.get("attacker_side")
        defender = deployment.get("defender") or state.get("defender_side")
        attacker_label = "Модель" if attacker == "model" else "Игрок" if attacker == "enemy" else None
        defender_label = "Модель" if defender == "model" else "Игрок" if defender == "enemy" else None
        if attacker_label and defender_label:
            self.status_deployment.setText(
                f"Деплой: атакующий слева — {attacker_label}, защитник справа — {defender_label}"
            )
        else:
            self.status_deployment.setText("Деплой: ожидание ролл-оффа")

        self._auto_switch_log_tab(active)

        vp = state.get("vp", {})
        cp = state.get("cp", {})
        self.points_vp_player.setText(f"Player VP: {vp.get('player', '—')}")
        self.points_vp_model.setText(f"Model VP: {vp.get('model', '—')}")
        self.points_cp_player.setText(f"Player CP: {cp.get('player', '—')}")
        self.points_cp_model.setText(f"Model CP: {cp.get('model', '—')}")

        self._populate_units_table(state.get("units", []))
        self._update_log(state.get("log_tail", []))
        self._update_model_events(state.get("model_events", []))
        self._drain_event_queue()
        self._refresh_active_context()

    def _populate_units_table(self, units):
        self.units_table.setRowCount(len(units))
        self.units_table.setSortingEnabled(False)
        self._unit_row_by_key = {}
        for row, unit in enumerate(units):
            side_label = "Игрок" if unit.get("side") == "player" else "Модель"
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

    def _update_log(self, lines):
        if isinstance(lines, list):
            text_lines = [str(line) for line in lines]
            if self._log_tail_snapshot == text_lines:
                return
            if not self._log_entries:
                self._reset_log_lines(text_lines, write_to_file=True)
                self._log_tail_snapshot = text_lines
                return
            existing = [entry["raw"] for entry in self._log_entries]
            if len(text_lines) >= len(existing) and text_lines[: len(existing)] == existing:
                for line in text_lines[len(existing) :]:
                    self.add_log_line(line)
                self._log_tail_snapshot = text_lines
                return
            self._reset_log_lines(text_lines, write_to_file=False)
            self._log_tail_snapshot = text_lines

    def _update_model_events(self, events):
        if not isinstance(events, list):
            return
        if events:
            if self._model_events_snapshot == events:
                return
            filtered = self._filter_model_events(events)
            self._model_events_snapshot = list(events)
            self._model_log_source = "state"
            self._model_events_current = list(filtered)
            self._refresh_model_log_view()
        elif self._model_log_source is None:
            self._drain_event_queue()

    def _filter_model_events(self, events):
        filtered = []
        for event in events:
            if not isinstance(event, dict):
                continue
            side = str(event.get("side", "")).lower()
            if side in ("enemy", "model"):
                filtered.append(event)
        return filtered

    def _set_selected_unit(self, side, unit_id, *, source: str, select_row: bool = False):
        self._selected_unit_side = side
        self._selected_unit_id = unit_id
        self.map_scene.set_selected_unit(side, unit_id)
        if select_row:
            self._select_row_for_unit_id(unit_id, side=side)
        if source == "map":
            unit_name = self._units_by_key.get((side, unit_id), {}).get("name", "—")
            self._append_log([f"Выбрано на карте: unit_id={unit_id}, name={unit_name}"])
        elif source == "table":
            row = self._unit_row_by_key.get((side, unit_id))
            if row is not None:
                self._append_log([f"Выбрано в таблице: row={row} -> unit_id={unit_id}"])

    def _select_row_for_unit(self, side, unit_id):
        unit_key = (side, unit_id)
        row = self._unit_row_by_key.get(unit_key)
        if row is None:
            row = self._find_row_for_unit(unit_key)
        if row is None:
            return
        self._set_selected_unit(side, unit_id, source="map", select_row=True)
        self._on_target_selected(unit_id)

    def _sync_selection_from_table(self):
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
            self._on_target_selected(unit_id)

    def add_log_line(self, line: str):
        raw_text = str(line)
        new_turn = self._update_turn_context(raw_text)
        categories = self._classify_line(raw_text)
        if self._should_assign_shooting_side(raw_text, categories):
            categories.add(self._current_turn_side)
        display_text = self._decorate_log_line(raw_text, categories)
        entry = {
            "raw": raw_text,
            "display": display_text,
            "turn": self._current_turn_number,
            "categories": categories,
        }
        self._log_entries.append(entry)
        self._append_log_to_file(raw_text)
        self._fx_parser.consume_line(raw_text)
        self._drain_fx_queue()
        if len(self._log_entries) > self._max_log_lines:
            self._log_entries = self._log_entries[-self._max_log_lines :]
            self._refresh_log_views()
            return
        if new_turn is not None and self.log_only_current_turn.isChecked():
            self._refresh_log_views()
            return
        for key, _ in self._log_tab_defs:
            if self._should_show_entry(entry, key):
                if key == "model":
                    continue
                self._append_to_view(self._log_tabs[key], display_text)

    def _append_to_view(self, view: QtWidgets.QPlainTextEdit, text: str):
        scrollbar = view.verticalScrollBar()
        at_bottom = scrollbar.value() >= scrollbar.maximum()
        view.appendPlainText(text)
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    def _classify_line(self, line: str):
        lowered = line.lower()
        categories = set()
        if self._matches_any(
            lowered,
            [
                "player",
                "[player]",
                "ход player",
                "enemy",
                "[enemy]",
            ],
        ):
            categories.add("player")
        if self._matches_any(
            lowered,
            [
                "model",
                "[model]",
                "ход model",
            ],
        ):
            categories.add("model")
        if self._matches_any(
            lowered,
            [
                "боевого раунда",
                "фаза",
                "===",
                "iteration",
                "раунд",
                "turn",
            ],
        ):
            categories.add("turn")
            categories.add("key")
        if self._matches_any(
            lowered,
            [
                "[shoot]",
                "отчёт по стрельбе",
                "hit rolls",
                "wound",
                "save",
                "оружие",
                "bs оружия",
                "s vs t",
                "save цели",
                "правило",
                "итог по движку",
                "стрельб",
            ],
        ):
            categories.add("shooting")
            categories.add("key")
        if "shooting" not in categories and self._is_shooting_report_line(line):
            categories.add("shooting")
            categories.add("key")
        if self._matches_any(
            lowered,
            [
                "[fight]",
                "фаза боя",
                "melee",
                "атаки",
                "удар",
            ],
        ):
            categories.add("fight")
            categories.add("key")
        if self._matches_any(
            lowered,
            [
                "d6",
                "2d6",
                "d3",
                "бросок",
                "roll",
                "rolling",
                "🎲",
            ],
        ):
            categories.add("dice")
            categories.add("key")
        if self._matches_any(
            lowered,
            [
                "error",
                "traceback",
                "exception",
                "warn",
                "warning",
                "недоступен",
                "ошибка",
            ],
        ):
            categories.add("errors")
            categories.add("key")
        if self._matches_any(
            lowered,
            [
                "vp",
                "cp",
                "побед",
                "winner",
                "game over",
                "мисси",
                "deploy",
                "раунд",
                "фаза",
                "ход",
                "end",
                "start",
            ],
        ):
            categories.add("key")
        return categories

    def _matches_any(self, lowered: str, tokens):
        return any(token in lowered for token in tokens)

    def _has_explicit_side_tag(self, text: str) -> bool:
        if "🧑" in text or "🤖" in text:
            return True
        lowered = text.lower()
        return any(token in lowered for token in ("[player]", "[model]", "[enemy]"))

    def _is_shooting_report_line(self, text: str) -> bool:
        lowered = text.lower()
        if any(
            token in lowered
            for token in (
                "🎲 бросок",
                "📌 --- отчёт по стрельбе ---",
                "оружие:",
                "bs оружия:",
                "s vs t:",
                "save цели:",
                "правило:",
                "hit rolls",
                "wound rolls",
                "save rolls",
                "✅ итог по движку",
            )
        ):
            return True
        return re.search(r"\bunit\s+\d+.*нан[её]с.*по\s+unit\s+\d+", lowered) is not None

    def _should_assign_shooting_side(self, text: str, categories: set) -> bool:
        if self._current_turn_side is None:
            return False
        if self._has_explicit_side_tag(text):
            return False
        if "player" in categories or "model" in categories:
            return False
        return self._is_shooting_report_line(text)

    def _decorate_log_line(self, text: str, categories: set) -> str:
        if not categories:
            return text
        icons = []
        if "errors" in categories:
            icons.append("⚠️")
        if "dice" in categories:
            icons.append("🎲")
        if "fight" in categories:
            icons.append("⚔️")
        if "shooting" in categories:
            icons.append("🎯")
        if "turn" in categories or "key" in categories:
            icons.append("⭐")
        if "player" in categories:
            icons.append("🧑")
        if "model" in categories:
            icons.append("🤖")
        prefix = " ".join(icons)
        if prefix:
            return f"{prefix} {text}"
        return text

    def _detect_turn_number(self, line: str):
        match = re.search(r"боевого раунда\\s*(\\d+)", line, re.IGNORECASE)
        if match:
            return int(match.group(1))
        match = re.search(r"\\bturn\\s*(\\d+)", line, re.IGNORECASE)
        if match:
            return int(match.group(1))
        match = re.search(r"\\bраунд\\s*(\\d+)", line, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def _detect_turn_side(self, line: str):
        lowered = line.lower()
        if "ход player" in lowered:
            return "player"
        if "ход model" in lowered:
            return "model"
        if "ход enemy" in lowered:
            return "model"
        return None

    def _update_turn_context(self, line: str):
        new_turn = self._detect_turn_number(line)
        if new_turn is not None:
            self._current_turn_number = new_turn
        new_side = self._detect_turn_side(line)
        if new_side is not None:
            self._current_turn_side = new_side
        return new_turn

    def _should_show_entry(self, entry, tab_key):
        if tab_key == "key":
            if "key" not in entry["categories"]:
                return False
        elif tab_key in ("player", "model"):
            if tab_key not in entry["categories"]:
                if "player" in entry["categories"] or "model" in entry["categories"]:
                    return False
        if not self.log_only_current_turn.isChecked():
            return True
        if self._current_turn_number is None:
            return True
        return entry["turn"] == self._current_turn_number

    def _refresh_log_views(self):
        for view in self._log_tabs.values():
            view.clear()
        grouped_lines = {key: [] for key, _ in self._log_tab_defs}
        for entry in self._log_entries:
            for key, _ in self._log_tab_defs:
                if self._should_show_entry(entry, key):
                    grouped_lines[key].append(entry["display"])
        for key, lines in grouped_lines.items():
            if lines:
                if key == "model":
                    continue
                self._log_tabs[key].setPlainText("\n".join(lines))
                scrollbar = self._log_tabs[key].verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
        self._refresh_model_log_view()

    def _refresh_model_log_view(self):
        view = self._log_tabs.get("model")
        if view is None:
            return
        include_verbose = self.log_model_verbose.isChecked()
        only_round = self._current_turn_number if self.log_only_current_turn.isChecked() else None
        text = render_model_log_flat(
            self._model_events_current,
            include_verbose=include_verbose,
            only_round=only_round,
        )
        view.setPlainText(text if text else "Пока нет событий модели.")
        scrollbar = view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _reset_log_lines(self, lines, write_to_file: bool):
        self._log_entries = []
        self._current_turn_number = None
        self._current_turn_side = None
        for line in lines:
            if write_to_file:
                self.add_log_line(line)
            else:
                raw_text = str(line)
                self._update_turn_context(raw_text)
                categories = self._classify_line(raw_text)
                if self._should_assign_shooting_side(raw_text, categories):
                    categories.add(self._current_turn_side)
                self._log_entries.append(
                    {
                        "raw": raw_text,
                        "display": self._decorate_log_line(raw_text, categories),
                        "turn": self._current_turn_number,
                        "categories": categories,
                    }
                )
        self._refresh_log_views()
        if not write_to_file:
            self._replay_fx_from_log_lines(lines)

    def _replay_fx_from_log_lines(self, lines) -> None:
        if not lines:
            return
        self._fx_parser.reset(preserve_seen=True)
        self._fx_parser.replay_lines(lines)
        self._drain_fx_queue()

    def _clear_log_viewer(self):
        self._log_entries = []
        self._current_turn_number = None
        self._current_turn_side = None
        self._log_tail_snapshot = None
        self._model_events_snapshot = None
        self._model_events_stream = []
        self._model_events_current = []
        self._fx_shot_queue.clear()
        self._fx_parser.reset(preserve_seen=False)
        for view in self._log_tabs.values():
            view.clear()

    def _collect_current_turn_logs(self):
        if self._current_turn_number is None:
            return "\n".join(entry["display"] for entry in self._log_entries)
        return "\n".join(
            entry["display"]
            for entry in self._log_entries
            if entry["turn"] == self._current_turn_number
        )

    def _copy_current_turn(self):
        QtWidgets.QApplication.clipboard().setText(self._collect_current_turn_logs())

    def _append_log_to_file(self, line: str):
        self._rotate_log_file_if_needed()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self._log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"{timestamp} | {line}\n")
        except OSError:
            pass

    def _rotate_log_file_if_needed(self):
        if not os.path.exists(self._log_file_path):
            return
        try:
            size = os.path.getsize(self._log_file_path)
        except OSError:
            return
        if size <= self._log_file_max_bytes:
            return
        rotated = os.path.join(ROOT_DIR, "LOGS_FOR_AGENTS.old.md")
        try:
            if os.path.exists(rotated):
                os.remove(rotated)
            os.replace(self._log_file_path, rotated)
        except OSError:
            pass

    def _count_dice_entries(self, text: str) -> int:
        stripped = text.strip()
        if not stripped:
            return 0
        if stripped.isdigit():
            return len(stripped)
        parts = [part for part in re.split(r"[,\s]+", stripped) if part]
        return len(parts)

    def _rebuild_unit_row_mapping(self):
        self._unit_row_by_key = {}
        for row in range(self.units_table.rowCount()):
            item = self.units_table.item(row, 0)
            if item is None:
                continue
            unit_key = item.data(QtCore.Qt.UserRole)
            if unit_key:
                self._unit_row_by_key[unit_key] = row

    def _find_row_for_unit(self, unit_key):
        for row in range(self.units_table.rowCount()):
            item = self.units_table.item(row, 0)
            if item is None:
                continue
            if item.data(QtCore.Qt.UserRole) == unit_key:
                return row
        return None

    def _extract_unit_id(self, prompt):
        if not prompt:
            return None
        match = re.search(r"(?:юнит|unit)\s*#?\s*(\d+)", prompt, re.IGNORECASE)
        if match:
            return int(match.group(1))
        raw = str(prompt).strip()
        if raw.isdigit():
            return int(raw)
        return None

    def _resolve_move_range(self, unit):
        if not unit:
            return None
        for key in ("move", "movement", "move_range", "speed"):
            value = unit.get(key)
            if isinstance(value, (int, float)):
                return int(value)
        if self._pending_request and getattr(self._pending_request, "kind", "") == "int":
            max_value = getattr(self._pending_request, "max_value", None)
            if max_value is not None:
                return int(max_value)
        return 6

    def _resolve_weapon_range(self, unit):
        if not unit:
            return None
        for key in ("range", "weapon_range", "shoot_range", "shooting_range"):
            value = unit.get(key)
            if isinstance(value, (int, float)):
                return int(value)
        return 12

    def _resolve_active_unit(self):
        unit_id = self._extract_unit_id(getattr(self._pending_request, "prompt", ""))
        if unit_id is None:
            return None, None
        for (side, candidate_id), unit in self._units_by_key.items():
            if candidate_id == unit_id:
                return unit_id, side
        return unit_id, None

    def _select_row_for_unit_id(self, unit_id, side=None):
        if unit_id is None:
            return
        row = None
        if side is not None:
            unit_key = (side, unit_id)
            row = self._unit_row_by_key.get(unit_key)
            if row is None:
                row = self._find_row_for_unit(unit_key)
        else:
            for (candidate_side, candidate_id), candidate_row in self._unit_row_by_key.items():
                if candidate_id == unit_id:
                    row = candidate_row
                    break
        if row is None:
            return
        self._syncing_table_selection = True
        try:
            self.units_table.selectRow(row)
        finally:
            self._syncing_table_selection = False

    def _refresh_active_context(self):
        unit_id, side = self._resolve_active_unit()
        self._active_unit_id = unit_id
        self._active_unit_side = side
        if self._selected_unit_id is None and unit_id is not None:
            self._set_selected_unit(side, unit_id, source="auto", select_row=True)
        active_unit = self._units_by_key.get((side, unit_id))
        phase = None
        if self.state_watcher and self.state_watcher.state:
            phase = self.state_watcher.state.get("phase")
        move_range = None
        shoot_range = None
        if self._is_movement_phase(phase):
            move_range = self._resolve_move_range(active_unit)
        if self._is_shooting_phase(phase):
            shoot_range = self._resolve_weapon_range(active_unit)
        self.map_scene.set_active_context(
            active_unit_id=unit_id,
            active_unit_side=side,
            selected_unit_id=self._selected_unit_id,
            selected_unit_side=self._selected_unit_side,
            phase=phase,
            move_range=move_range,
            shoot_range=shoot_range,
            show_objective_radius=self._show_objective_radius,
            targets=self.state_watcher.state.get("available_targets")
            if self.state_watcher and self.state_watcher.state
            else None,
        )

    def _enqueue_fx_event(self, event: FxShotEvent) -> None:
        self._fx_shot_queue.append(event)

    def _drain_fx_queue(self) -> None:
        while self._fx_shot_queue:
            event = self._fx_shot_queue.popleft()
            self._spawn_fx_for_event(event)

    def _spawn_fx_for_event(self, event: FxShotEvent) -> None:
        if "gauss flayer" not in event.weapon_name.lower():
            self._fx_debug("FX: оружие не gauss, эффект пропущен.")
            return
        attacker_side = self._side_from_unit_id(event.attacker_id)
        target_side = self._side_from_unit_id(event.target_id)
        start = self._unit_world_center_by_key(attacker_side, event.attacker_id)
        end = self._unit_world_center_by_key(target_side, event.target_id)
        if start is None or end is None:
            self._fx_debug(
                "FX: не удалось получить координаты для эффекта "
                f"(attacker={event.attacker_id}, target={event.target_id})."
            )
            return
        self._spawn_gauss_effect(start, end, event)

    def _spawn_gauss_effect(
        self, start: QtCore.QPointF, end: QtCore.QPointF, event: FxShotEvent
    ) -> None:
        t0 = time.monotonic()
        seed = hash((event.attacker_id, event.target_id, int(t0 * 1000))) & 0xFFFFFFFF
        config = get_gun_fx_config("Gauss flayer")
        duration = float(config.get("duration", 6.5))
        effect = self.map_scene.build_gauss_effect(
            start,
            end,
            t0=t0,
            duration=duration,
            seed=seed,
            config=config,
        )
        self.map_scene.add_effect(effect)
        self._fx_debug(
            "FX: позиция эффекта "
            f"start=({start.x():.1f},{start.y():.1f}) "
            f"end=({end.x():.1f},{end.y():.1f})."
        )
        self._fx_debug(
            "FX: эффект добавлен в рендер "
            f"(attacker={event.attacker_id}, target={event.target_id})."
        )

    def _unit_world_center_by_key(
        self, side: Optional[str], unit_id: int
    ) -> Optional[QtCore.QPointF]:
        if side:
            unit = self._units_by_key.get((side, unit_id))
            if unit:
                return self._unit_to_world_center(unit)
        return self._unit_world_center(unit_id)

    def _unit_world_center(self, unit_id: int) -> Optional[QtCore.QPointF]:
        cell = self.map_scene.cell_size
        for (_, candidate_id), unit in self._units_by_key.items():
            if candidate_id != unit_id:
                continue
            return self._unit_to_world_center(unit)
        return None

    def _unit_to_world_center(self, unit: dict) -> Optional[QtCore.QPointF]:
        cell = self.map_scene.cell_size
        anchor_x = unit.get("anchor_x") if isinstance(unit, dict) else None
        anchor_y = unit.get("anchor_y") if isinstance(unit, dict) else None
        if self.map_scene._safe_int(anchor_x) is not None and self.map_scene._safe_int(anchor_y) is not None:
            view_xy = self.map_scene._state_xy_to_view_xy(anchor_x, anchor_y)
        else:
            view_xy = self.map_scene._state_xy_to_view_xy(unit.get("x"), unit.get("y"))
        if view_xy is None:
            return None
        x, y = view_xy
        return QtCore.QPointF(x * cell + cell / 2, y * cell + cell / 2)

    def _side_from_unit_id(self, unit_id: int) -> Optional[str]:
        unit_str = str(unit_id)
        if unit_str.startswith("1"):
            return "player"
        if unit_str.startswith("2"):
            return "model"
        return None

    def _fx_debug(self, message: str) -> None:
        if not message:
            return
        self._append_log_to_file(message)

    def _auto_switch_log_tab(self, active_side):
        if active_side not in ("player", "model"):
            return
        if active_side == self._last_active_side:
            return
        self._last_active_side = active_side
        target_index = self._log_tab_indices.get(active_side)
        if target_index is None:
            return
        self._log_tab_programmatic_switch = True
        try:
            self.log_tabs.setCurrentIndex(target_index)
        finally:
            self._log_tab_programmatic_switch = False

    def _on_log_tab_changed(self, index):
        if self._log_tab_programmatic_switch:
            return
        self._last_manual_log_tab_index = index

    def _is_movement_phase(self, phase):
        phase_text = str(phase or "").lower()
        return "move" in phase_text or "движ" in phase_text or "movement" in phase_text

    def _is_shooting_phase(self, phase):
        phase_text = str(phase or "").lower()
        return "shoot" in phase_text or "стрел" in phase_text or "shooting" in phase_text

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and self._pending_request:
            kind = getattr(self._pending_request, "kind", "")
            key = event.key()
            text = event.text().lower()
            if kind == "direction":
                if key == QtCore.Qt.Key_Up:
                    self._submit_answer("up")
                    return True
                if key == QtCore.Qt.Key_Down:
                    self._submit_answer("down")
                    return True
                if key == QtCore.Qt.Key_Left:
                    self._submit_answer("left")
                    return True
                if key == QtCore.Qt.Key_Right:
                    self._submit_answer("right")
                    return True
                if key in (QtCore.Qt.Key_Space, QtCore.Qt.Key_0):
                    self._submit_answer("none")
                    return True
            elif kind == "bool":
                if text == "y":
                    self._submit_answer("y")
                    return True
                if text == "n":
                    self._submit_answer("n")
                    return True
                if key == QtCore.Qt.Key_Escape:
                    self.command_input.clear()
                    return True
            elif kind == "int":
                if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                    self._submit_answer(self.int_spin.value())
                    return True
            elif kind == "choice":
                if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                    self._submit_choice()
                    return True
        return super().eventFilter(obj, event)


def launch(state_path, model_path=None):
    app = QtWidgets.QApplication([])
    window = ViewerWindow(state_path, model_path=model_path)
    window.setGeometry(0, 0, 2560, 1440)
    window.showMaximized()
    app.exec()
