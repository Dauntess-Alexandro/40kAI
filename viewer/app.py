import torch
import os
import queue
import re
import sys
import time
import copy
from collections import OrderedDict, deque
from dataclasses import dataclass, field
from typing import Callable, Deque, Optional, Tuple
from datetime import datetime
from PySide6 import QtCore, QtGui, QtWidgets

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GYM_PATH = os.path.join(ROOT_DIR, "gym_mod")
if GYM_PATH not in sys.path:
    sys.path.insert(0, GYM_PATH)

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


@dataclass
class PhaseBuffer:
    phase: str
    active_side: str
    unit_actions: list = field(default_factory=list)
    summary: Optional[dict] = None
    snapshot: Optional[dict] = None


@dataclass
class PhaseScriptStep:
    kind: str
    payload: dict = field(default_factory=dict)
    duration_s: float = 0.0


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


class PhaseScriptPlayer(QtCore.QObject):
    def __init__(self, owner: "ViewerWindow") -> None:
        super().__init__()
        self._owner = owner
        self._queue: Deque[list[PhaseScriptStep]] = deque()
        self._active_script: list[PhaseScriptStep] = []
        self._step_index = 0
        self._playing = False
        self._checkpoint_seen = False
        self._waiting = False
        self._paused = False
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._play_next_step)

    def enqueue(self, script: list[PhaseScriptStep]) -> None:
        if not script:
            return
        self._queue.append(script)
        if not self._playing:
            self._start_next_script()

    def _start_next_script(self) -> None:
        if not self._queue:
            self._playing = False
            self._owner._end_cinematic_playback()
            return
        self._active_script = self._queue.popleft()
        self._step_index = 0
        self._playing = True
        self._checkpoint_seen = False
        self._waiting = False
        self._paused = False
        self._play_next_step()

    def _play_next_step(self) -> None:
        if self._paused:
            return
        if self._step_index >= len(self._active_script):
            if not self._checkpoint_seen:
                self._owner._apply_phase_checkpoint()
            self._start_next_script()
            return
        step = self._active_script[self._step_index]
        self._step_index += 1
        manual = self._owner._is_cinematic_manual()
        duration_ms = 0 if manual else max(0, int(step.duration_s * 1000))
        if step.kind == "checkpoint":
            self._checkpoint_seen = True
            self._owner._apply_phase_checkpoint(step.payload.get("snapshot"))
            if manual:
                self._play_next_step()
            else:
                QtCore.QTimer.singleShot(0, self._play_next_step)
            return
        self._owner._execute_phase_step(step)
        if manual and step.kind in ("unit_action", "phase_done"):
            self._waiting = True
            next_label = self._next_unit_label() if step.kind == "unit_action" else None
            self._owner._request_cinematic_continue(
                reason="unit_done" if step.kind == "unit_action" else "phase_done",
                next_label=next_label,
                phase_label=step.payload.get("next_phase_label"),
            )
            return
        if duration_ms <= 0:
            if manual:
                self._play_next_step()
            else:
                QtCore.QTimer.singleShot(0, self._play_next_step)
        else:
            self._timer.start(duration_ms)

    def _next_unit_label(self) -> Optional[str]:
        for idx in range(self._step_index, len(self._active_script)):
            step = self._active_script[idx]
            if step.kind == "unit_action":
                payload = step.payload or {}
                unit_id = payload.get("unit_id")
                unit_name = payload.get("unit_name") or "—"
                action_line = self._owner._format_unit_action_line(payload)
                return f"Unit {unit_id} — {unit_name} ({action_line})"
        return None

    def continue_play(self, accepted: bool) -> None:
        if self._waiting:
            self._waiting = False
        if not accepted:
            self._paused = True
            self._playing = False
            return
        self._paused = False
        self._playing = True
        self._play_next_step()


class ViewerWindow(QtWidgets.QMainWindow):
    def __init__(self, state_path, model_path=None):
        super().__init__()
        self.state_path = state_path
        self.setWindowTitle("40kAI Viewer")
        self.resize(1200, 800)

        self.controller = GameController(model_path=model_path, state_path=state_path)
        self._pending_request = None
        self._pending_requests: Deque = deque()
        self._awaiting_player_action = False
        self._active_unit_id = None
        self._active_unit_side = None
        self._current_target_id = None
        self._last_shooter_id = None
        self._show_objective_radius = True
        self._units_by_key = {}
        self._unit_row_by_key = {}

        self.state_watcher = StateWatcher(self.state_path)
        self.map_scene = OpenGLBoardWidget(cell_size=18)
        self.map_scene.unit_selected.connect(self._select_row_for_unit)

        self.status_round = QtWidgets.QLabel("Раунд: —")
        self.status_turn = QtWidgets.QLabel("Ход: —")
        self.status_phase = QtWidgets.QLabel("Фаза: —")
        self.status_active = QtWidgets.QLabel("Активен: —")

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
        self._last_state = None
        self._phase_buffer: Optional[PhaseBuffer] = None
        self._phase_player = PhaseScriptPlayer(self)
        self._model_event_cursor: Optional[int] = None
        self._cinematic_active = False
        self._cinematic_manual = True
        self._cinematic_waiting = False
        self._cinematic_lines: list[str] = []
        self._cinematic_playback_active = False
        self._visual_state: Optional[dict] = None
        self._pending_snapshot: Optional[dict] = None
        self._pending_state_json: Optional[dict] = None
        self._grid_axes_swapped: Optional[bool] = None
        self._cinematic_history: Deque[str] = deque(maxlen=30)
        self._deferred_moves: list[dict] = []
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
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.addWidget(fit_button, alignment=QtCore.Qt.AlignLeft)
        left_layout.addWidget(self.map_scene)

        log_group = QtWidgets.QGroupBox("ЖУРНАЛ")
        log_layout = QtWidgets.QVBoxLayout(log_group)
        log_layout.addLayout(self._log_controls_layout)
        log_layout.addWidget(self.log_tabs)
        log_group.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        command_group = QtWidgets.QGroupBox("КОМАНДЫ")
        command_layout = QtWidgets.QVBoxLayout(command_group)
        self.cinematic_label = QtWidgets.QLabel("")
        self.cinematic_label.setWordWrap(True)
        self.cinematic_label.setStyleSheet(f"color: {Theme.accent.name()}; font-weight: 600;")
        command_layout.addWidget(self.cinematic_label)
        self.command_prompt = QtWidgets.QLabel("Ожидаю команду...")
        self.command_prompt.setWordWrap(True)
        command_layout.addWidget(self.command_prompt)
        self.command_hint = QtWidgets.QLabel("Горячие клавиши: —")
        self.command_hint.setStyleSheet(f"color: {Theme.muted.name()};")
        command_layout.addWidget(self.command_hint)
        self.cinematic_controls = QtWidgets.QWidget()
        cinematic_controls_layout = QtWidgets.QHBoxLayout(self.cinematic_controls)
        cinematic_controls_layout.setContentsMargins(0, 0, 0, 0)
        self.cinematic_prompt = QtWidgets.QLabel("")
        self.cinematic_prompt.setStyleSheet(f"color: {Theme.muted.name()};")
        cinematic_controls_layout.addWidget(self.cinematic_prompt)
        self.cinematic_yes = QtWidgets.QPushButton("Да (Y)")
        self.cinematic_no = QtWidgets.QPushButton("Нет (N)")
        self.cinematic_yes.clicked.connect(lambda: self._handle_cinematic_continue(True))
        self.cinematic_no.clicked.connect(lambda: self._handle_cinematic_continue(False))
        cinematic_controls_layout.addWidget(self.cinematic_yes)
        cinematic_controls_layout.addWidget(self.cinematic_no)
        cinematic_controls_layout.addStretch()
        command_layout.addWidget(self.cinematic_controls)
        self._set_cinematic_waiting(False)

        self.cinematic_history_group = QtWidgets.QGroupBox("История")
        self.cinematic_history_group.setCheckable(True)
        self.cinematic_history_group.setChecked(False)
        history_layout = QtWidgets.QVBoxLayout(self.cinematic_history_group)
        self.cinematic_history_view = QtWidgets.QPlainTextEdit()
        self.cinematic_history_view.setReadOnly(True)
        history_layout.addWidget(self.cinematic_history_view)
        command_layout.addWidget(self.cinematic_history_group)

        self.command_stack = QtWidgets.QStackedWidget()
        self._build_command_pages()
        command_layout.addWidget(self.command_stack)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setSpacing(8)
        right_layout.addWidget(self._group_status())
        right_layout.addWidget(self._group_points())
        right_layout.addWidget(self._group_units())
        right_layout.addWidget(self._group_legend())
        right_layout.addWidget(command_group)
        right_layout.addStretch()

        top_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        top_splitter.addWidget(left_widget)
        top_splitter.addWidget(right_widget)
        top_splitter.setStretchFactor(0, 4)
        top_splitter.setStretchFactor(1, 1)

        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(log_group)
        main_splitter.setStretchFactor(0, 3)
        main_splitter.setStretchFactor(1, 2)

        central = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central)
        central_layout.addWidget(main_splitter)
        self.setCentralWidget(central)

        self._apply_dark_theme()
        self._build_toolbar()
        self._fit_view()
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
        if "ход юнита" in prompt:
            return True
        return ("цель" in prompt and ("стрель" in prompt or "shoot" in prompt)) or "выберите цель" in prompt

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
            filtered = self._filter_model_events(drained)
            self._consume_model_events(filtered)
            self._model_events_stream.extend(filtered)
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
        if self._is_target_request(self._pending_request) and self._current_target_id is None:
            return
        value = self.choice_combo.currentText()
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
        self._last_state = state
        active = state.get("active") or state.get("active_side")
        active_side = str(active or "").lower()
        defer_state_update = (
            self._cinematic_playback_active
            and self._cinematic_manual
            and active_side in ("model", "enemy")
        )
        if defer_state_update:
            self._pending_state_json = copy.deepcopy(state)
            self.add_log_line("FX: state update deferred during playback")
        if not defer_state_update:
            self._apply_visual_state(state)
        elif self._visual_state is None:
            self._apply_visual_state(state)
        self._process_deferred_moves()

        if defer_state_update and self._visual_state is not None:
            state_for_ui = self._visual_state
            self.add_log_line("FX: UI/FX используют визуальное состояние во время playback")
        else:
            state_for_ui = state if defer_state_update else (self._visual_state or state)
        self._units_by_key = {}
        for unit in state_for_ui.get("units", []) or []:
            self._units_by_key[(unit.get("side"), unit.get("id"))] = unit

        self.status_round.setText(f"Раунд: {state.get('round', '—')}")
        self.status_turn.setText(f"Ход: {state.get('turn', '—')}")
        self.status_phase.setText(f"Фаза: {state.get('phase', '—')}")
        active = state.get("active") or state.get("active_side")
        active_label = "Игрок" if active == "player" else "Модель" if active == "model" else "—"
        self.status_active.setText(f"Активен: {active_label}")
        self._auto_switch_log_tab(active)
        if active != "model" and self._cinematic_active:
            self._cinematic_active = False
            self.cinematic_label.setText("")
            self._set_cinematic_waiting(False)

        vp = state.get("vp", {})
        cp = state.get("cp", {})
        self.points_vp_player.setText(f"Player VP: {vp.get('player', '—')}")
        self.points_vp_model.setText(f"Model VP: {vp.get('model', '—')}")
        self.points_cp_player.setText(f"Player CP: {cp.get('player', '—')}")
        self.points_cp_model.setText(f"Model CP: {cp.get('model', '—')}")

        self._populate_units_table(state_for_ui.get("units", []))
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
            self._consume_model_events(filtered)
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

    def _consume_model_events(self, events):
        if not events:
            return
        ordered = list(events)
        if any(event.get("event_id") is not None for event in ordered):
            ordered.sort(key=lambda item: int(item.get("event_id", 0)))
        for event in ordered:
            event_id = event.get("event_id")
            if event_id is not None:
                try:
                    event_id = int(event_id)
                except (TypeError, ValueError):
                    event_id = None
            if event_id is not None and self._model_event_cursor is not None:
                if event_id <= self._model_event_cursor:
                    continue
            if event_id is not None:
                self._model_event_cursor = max(self._model_event_cursor or 0, event_id)
            self._process_phase_event(event)

    def _process_phase_event(self, event: dict) -> None:
        if not self._is_model_cinematic_event(event):
            return
        event_type = str(event.get("type") or "")
        phase = str(event.get("phase") or "")
        if event_type == "phase_start":
            self._phase_buffer = PhaseBuffer(
                phase=phase,
                active_side=str(event.get("active_side") or "model"),
            )
            self._cinematic_playback_active = True
            if self._visual_state is None and self._last_state:
                self._visual_state = copy.deepcopy(self._last_state)
                self.map_scene.update_state(self._visual_state)
            self.add_log_line(f"FX: buffer phase {phase} (model)")
            return
        if event_type == "unit_action":
            if self._phase_buffer and self._phase_buffer.phase == phase:
                self._phase_buffer.unit_actions.append(event)
            return
        if event_type == "phase_summary":
            if self._phase_buffer and self._phase_buffer.phase == phase:
                self._phase_buffer.summary = event
            return
        if event_type == "phase_end":
            if not self._phase_buffer:
                return
            if phase and self._phase_buffer.phase != phase:
                return
            snapshot = event.get("snapshot")
            if snapshot is None and isinstance(event.get("data"), dict):
                snapshot = event.get("data", {}).get("snapshot")
            if snapshot is not None:
                self._phase_buffer.snapshot = snapshot
                self._pending_snapshot = snapshot
            script = self._build_phase_script(self._phase_buffer)
            unit_count = len(self._phase_buffer.unit_actions)
            self.add_log_line(f"FX: enqueue phase script {phase}: units={unit_count}")
            self._phase_player.enqueue(script)
            self._phase_buffer = None

    def _is_model_cinematic_event(self, event: dict) -> bool:
        if str(event.get("active_side") or "").lower() != "model":
            return False
        return str(event.get("type") or "") in {
            "phase_start",
            "unit_action",
            "phase_summary",
            "phase_end",
        }

    def _build_phase_script(self, buffer: PhaseBuffer) -> list[PhaseScriptStep]:
        steps: list[PhaseScriptStep] = []
        phase_summary_text = self._format_phase_summary(buffer.phase, buffer.summary or {})
        next_phase_label = self._phase_label(self._next_phase(buffer.phase))
        steps.append(
            PhaseScriptStep(
                kind="phase_header",
                payload={"phase": buffer.phase},
                duration_s=0.0,
            )
        )
        steps.append(
            PhaseScriptStep(
                kind="summary",
                payload={
                    "phase": buffer.phase,
                    "summary": buffer.summary or {},
                    "summary_text": phase_summary_text,
                },
                duration_s=1.0,
            )
        )
        for event in buffer.unit_actions:
            steps.append(
                PhaseScriptStep(
                    kind="unit_action",
                    payload=event,
                    duration_s=1.0,
                )
            )
        steps.append(
            PhaseScriptStep(
                kind="phase_done",
                payload={
                    "phase": buffer.phase,
                    "summary_text": phase_summary_text,
                    "next_phase_label": next_phase_label,
                },
                duration_s=0.0,
            )
        )
        steps.append(
            PhaseScriptStep(
                kind="checkpoint",
                payload={"snapshot": buffer.snapshot},
                duration_s=0.0,
            )
        )
        return steps

    def _execute_phase_step(self, step: PhaseScriptStep) -> None:
        kind = step.kind
        payload = step.payload or {}
        if kind == "phase_header":
            phase = payload.get("phase") or ""
            label = self._phase_label(phase)
            self._set_cinematic_text([f"Фаза: {label}"])
            self.map_scene.set_active_phase(phase)
            return
        if kind == "summary":
            phase = payload.get("phase") or ""
            summary_text = payload.get("summary_text") or self._format_phase_summary(phase, payload.get("summary") or {})
            phase_label = self._phase_label(phase)
            lines = [f"Фаза: {phase_label}"]
            if summary_text:
                lines.append(f"📌 Итог: {summary_text}")
            self._set_cinematic_text(lines)
            if summary_text:
                self.add_log_line(f"FX: show summary {phase} {summary_text}")
            self._record_cinematic_history(lines)
            return
        if kind == "unit_action":
            unit_id = payload.get("unit_id")
            unit_name = payload.get("unit_name") or "—"
            action = payload.get("action")
            reason = payload.get("reason")
            title = f"Unit {unit_id} — {unit_name}"
            detail = self._format_unit_action_line(payload)
            phase_label = self._phase_label(payload.get("phase") or "")
            summary_text = self._format_phase_summary(payload.get("phase") or "", payload.get("summary") or {})
            lines = [f"Фаза: {phase_label}"]
            if summary_text:
                lines.append(f"📌 Итог: {summary_text}")
            lines.extend([title, detail])
            self._set_cinematic_text(lines)
            self._play_unit_action_fx(payload)
            if unit_id is not None:
                self.add_log_line(f"FX: play unit_action unit={unit_id} action={action}")
            self._record_cinematic_history([title, detail])
            return
        if kind == "phase_done":
            summary_text = payload.get("summary_text") or ""
            phase_label = self._phase_label(payload.get("phase") or "")
            lines = [f"Фаза: {phase_label}"]
            if summary_text:
                lines.append(f"📌 Итог: {summary_text}")
            self._set_cinematic_text(lines)
            self._record_cinematic_history(lines)
            return

    def _set_cinematic_text(self, lines: list[str]) -> None:
        self._cinematic_active = True
        self._cinematic_lines = [line for line in lines if line]
        text = "\n".join(self._cinematic_lines)
        self.cinematic_label.setText(text)
        if not self._cinematic_waiting:
            self.cinematic_prompt.setText("")

    def _request_cinematic_continue(
        self,
        reason: str,
        next_label: Optional[str],
        phase_label: Optional[str] = None,
    ) -> None:
        if not self._cinematic_manual:
            return
        self._set_cinematic_waiting(True)
        if reason == "unit_done":
            prompt = (
                f"Следующий юнит: {next_label}. Продолжить? (y/n)"
                if next_label
                else "Следующий юнит. Продолжить? (y/n)"
            )
            self.add_log_line(
                f"FX: wait_continue reason=unit_done next={next_label or 'unit'}"
            )
        else:
            phase_text = phase_label or "—"
            prompt = f"Следующая фаза: {phase_text}. Продолжить? (y/n)"
            self.add_log_line(
                f"FX: wait_continue reason=phase_done next={phase_text}"
            )
        self.cinematic_prompt.setText(f"{prompt} | Hotkeys: Y/N")

    def _handle_cinematic_continue(self, accepted: bool) -> None:
        if not self._cinematic_waiting:
            return
        self.add_log_line(f"FX: continue={'Y' if accepted else 'N'}")
        if not accepted:
            self._set_cinematic_waiting(False)
            self._phase_player.continue_play(False)
            return
        self._set_cinematic_waiting(False)
        self._phase_player.continue_play(True)

    def _set_cinematic_waiting(self, waiting: bool) -> None:
        self._cinematic_waiting = waiting
        self.cinematic_controls.setVisible(waiting)
        self.cinematic_yes.setEnabled(waiting)
        self.cinematic_no.setEnabled(waiting)
        if not hasattr(self, "command_stack"):
            if not waiting:
                self.cinematic_prompt.setText("")
            return
        if waiting:
            self.command_stack.setEnabled(False)
        else:
            self.command_stack.setEnabled(self._pending_request is not None)
            self.cinematic_prompt.setText("")

    def _record_cinematic_history(self, lines: list[str]) -> None:
        for line in lines:
            self._cinematic_history.append(line)
        if self.cinematic_history_group.isChecked():
            self.cinematic_history_view.setPlainText("\n".join(self._cinematic_history))

    def _is_cinematic_manual(self) -> bool:
        return bool(self._cinematic_manual)

    def _next_phase(self, phase: str) -> str:
        order = ["command", "movement", "shooting", "charge", "fight"]
        if phase in order:
            idx = order.index(phase)
            if idx + 1 < len(order):
                return order[idx + 1]
        return phase

    def _play_unit_action_fx(self, payload: dict) -> None:
        unit_id = payload.get("unit_id")
        event_id = payload.get("event_id")
        if unit_id is not None:
            self.map_scene.set_active_unit(unit_id)
            self.map_scene.select_unit("model", unit_id)
            self.map_scene.focus_unit(unit_id)
            self._select_row_for_unit_id(unit_id, side="model")
        action = payload.get("action")
        movement = payload.get("movement") or {}
        shooting = payload.get("shooting") or {}
        charge = payload.get("charge") or {}
        fight = payload.get("fight") or {}
        if action == "move":
            self._apply_visual_unit_move(payload, movement, event_id=event_id)
        target_id = (
            shooting.get("target_id")
            or charge.get("target_id")
            or fight.get("target_id")
        )
        if target_id is not None:
            self.map_scene.set_target_unit(target_id)
        else:
            self.map_scene.clear_target_selection()
        if action == "move":
            dest = movement.get("to")
            if isinstance(dest, (list, tuple)) and len(dest) >= 2:
                self.map_scene.set_target_cell((int(dest[0]), int(dest[1])))
        if action == "shoot":
            weapon_name = shooting.get("weapon_name")
            damage = shooting.get("damage")
            if unit_id is not None and target_id is not None and weapon_name:
                event = FxShotEvent(
                    ts=datetime.utcnow().isoformat(),
                    report_type="shooting",
                    attacker_id=int(unit_id),
                    target_id=int(target_id),
                    weapon_name=str(weapon_name),
                    damage=float(damage) if damage is not None else 0.0,
                )
                self._spawn_fx_for_event(event)

    def _apply_phase_checkpoint(self, snapshot: Optional[dict] = None) -> None:
        state = snapshot if isinstance(snapshot, dict) else self._last_state
        if not state:
            return
        self._apply_visual_state(state)
        self._pending_snapshot = None
        self._cinematic_playback_active = False
        self._apply_pending_state_after_playback()

    def _end_cinematic_playback(self) -> None:
        self._cinematic_playback_active = False
        self._apply_pending_state_after_playback()

    def _apply_pending_state_after_playback(self) -> None:
        if not self._pending_state_json:
            return
        self.add_log_line("FX: apply pending state after playback end")
        self._apply_visual_state(self._pending_state_json)
        self._pending_state_json = None

    def _phase_label(self, phase: str) -> str:
        mapping = {
            "command": "ФАЗА КОМАНДОВАНИЯ",
            "movement": "ФАЗА ДВИЖЕНИЯ",
            "shooting": "ФАЗА СТРЕЛЬБЫ",
            "charge": "ФАЗА ЧАРДЖА",
            "fight": "ФАЗА БОЯ",
        }
        return mapping.get(str(phase), f"ФАЗА {str(phase).upper()}")

    def _apply_visual_unit_move(self, payload: dict, movement: dict, event_id: Optional[int] = None) -> None:
        unit_id_raw = payload.get("unit_id")
        side = self._side_from_unit_id(unit_id_raw) if unit_id_raw is not None else "model"
        try:
            unit_id = int(unit_id_raw) if unit_id_raw is not None else None
        except (TypeError, ValueError):
            unit_id = None
        if unit_id is None or not self._visual_state:
            return
        src = movement.get("from")
        dest = movement.get("to")
        src_xy = (
            self._normalize_grid_xy(src[0], src[1])
            if isinstance(src, (list, tuple)) and len(src) >= 2
            else None
        )
        dest_xy = (
            self._normalize_grid_xy(dest[0], dest[1])
            if isinstance(dest, (list, tuple)) and len(dest) >= 2
            else None
        )
        src_types = (type(src[0]).__name__, type(src[1]).__name__) if isinstance(src, (list, tuple)) and len(src) >= 2 else None
        dest_types = (type(dest[0]).__name__, type(dest[1]).__name__) if isinstance(dest, (list, tuple)) and len(dest) >= 2 else None
        key = (side, unit_id)
        render_found = key in getattr(self.map_scene, "_unit_by_key", {})
        self.add_log_line(
            "FX: move apply "
            f"event_id={event_id} unit_id={unit_id} side={side} action={payload.get('action')} "
            f"from={src} types={src_types} to={dest} types={dest_types} "
            f"key={key} render_found={int(render_found)}"
        )
        if dest_xy is None:
            return
        if not render_found:
            self._defer_move(payload, movement, event_id=event_id)
            return
        x_grid, y_grid = dest_xy
        before = None
        for unit in self._visual_state.get("units", []) or []:
            if unit.get("id") == unit_id and unit.get("side") == side:
                before = (unit.get("x"), unit.get("y"))
                unit["x"] = x_grid
                unit["y"] = y_grid
                break
        if before is not None and src_xy is not None and before != src_xy:
            if before == dest_xy:
                self.add_log_line(
                    "WARNING: move state mismatch "
                    f"key=({side},{unit_id}) before={before} ожидается from={src_xy} "
                    "причина=уже_на_цели"
                )
            else:
                self.add_log_line(
                    "WARNING: move state mismatch "
                    f"key=({side},{unit_id}) before={before} ожидается from={src_xy}"
                )
        stored_grid = None
        for unit in self._visual_state.get("units", []) or []:
            if unit.get("id") == unit_id and unit.get("side") == side:
                stored_grid = (unit.get("x"), unit.get("y"))
                break
        self.add_log_line(
            "FX: move applied "
            f"unit={unit_id} from={src} to={dest} stored_grid=({x_grid},{y_grid})"
        )
        if stored_grid is not None and stored_grid != (x_grid, y_grid):
            self.add_log_line(
                "WARNING: move stored_grid mismatch "
                f"key=({side},{unit_id}) expected=({x_grid},{y_grid}) actual={stored_grid}"
            )
        self.add_log_line(
            "FX: move write "
            f"unit_id={unit_id} side={side} grid=({x_grid},{y_grid}) "
            f"before={before} after=({x_grid},{y_grid}) cell_size={self.map_scene.cell_size} "
            "conversion=grid->world(cell_size)"
        )
        dest_world = self.map_scene.grid_to_world(x_grid, y_grid)
        self.add_log_line(
            "FX: move grid->world "
            f"raw_from={src} raw_to={dest} normalized=({x_grid},{y_grid}) "
            f"world=({dest_world.x():.1f},{dest_world.y():.1f})"
        )
        self.map_scene.update_unit_position(side, unit_id, x_grid, y_grid)

    def _defer_move(self, payload: dict, movement: dict, event_id: Optional[int] = None) -> None:
        attempts = payload.get("_defer_attempts", 0) + 1
        payload["_defer_attempts"] = attempts
        self._deferred_moves.append({"payload": payload, "movement": movement, "event_id": event_id})
        unit_id = payload.get("unit_id")
        self.add_log_line(f"FX: defer move (missing render unit) unit={unit_id} attempts={attempts}")

    def _process_deferred_moves(self) -> None:
        if not self._deferred_moves:
            return
        pending = list(self._deferred_moves)
        self._deferred_moves = []
        remaining = []
        for item in pending:
            payload = item.get("payload", {})
            attempts = payload.get("_defer_attempts", 0)
            if attempts >= 3:
                unit_id = payload.get("unit_id")
                self.add_log_line(f"FX: drop deferred move unit={unit_id} attempts={attempts}")
                continue
            self._apply_visual_unit_move(payload, item.get("movement", {}), event_id=item.get("event_id"))
            if payload.get("_defer_attempts", 0) <= attempts:
                remaining.append(item)
        self._deferred_moves = remaining

    def _format_phase_summary(self, phase: str, summary: dict) -> str:
        if phase == "command":
            vp = summary.get("vp", 0)
            cp = summary.get("cp", 0)
            return f"VP={vp}, CP={cp}"
        if phase == "movement":
            moved = summary.get("moved", 0)
            total = summary.get("total_units", 0)
            advanced = summary.get("advanced_count", 0)
            dist = summary.get("dist_total", 0.0)
            if total == 0:
                return ""
            return f"двигались {moved}/{total}, advance={advanced}, dist={dist:.1f}"
        if phase in ("shooting", "charge", "fight"):
            main_label = "shots" if phase == "shooting" else "charges" if phase == "charge" else "fights"
            main_value = summary.get(main_label, 0)
            skipped = summary.get("skipped", 0)
            reasons = summary.get("reasons", {}) or {}
            reasons_text = ", ".join(f"{key}={value}" for key, value in sorted(reasons.items()))
            reason_part = f" (reasons: {reasons_text})" if reasons_text else ""
            return f"{main_label}={main_value}, skipped={skipped}{reason_part}"
        return ""

    def _format_unit_action_line(self, payload: dict) -> str:
        action = payload.get("action")
        reason = payload.get("reason")
        reason_text = f" ({reason})" if reason else ""
        if action == "no_move":
            movement = payload.get("movement") or {}
            dist = movement.get("dist", 0)
            return f"⏭️ No move: dist={dist}{reason_text}"
        if action == "move":
            movement = payload.get("movement") or {}
            dist = movement.get("dist", 0)
            advanced = "да" if movement.get("advanced") else "нет"
            start = movement.get("from")
            end = movement.get("to")
            if isinstance(start, (list, tuple)) and isinstance(end, (list, tuple)):
                return f"🚶 Движение: {start} → {end}, dist={dist}, advance={advanced}"
            return f"🚶 Движение: dist={dist}, advance={advanced}"
        if action == "skip_shoot":
            return f"⏭️ Skip shoot{reason_text}"
        if action == "shoot":
            shooting = payload.get("shooting") or {}
            target = shooting.get("target_id")
            weapon = shooting.get("weapon_name") or "—"
            damage = shooting.get("damage")
            damage_text = f"{damage:.1f}" if isinstance(damage, (int, float)) else "0.0"
            target_text = f"Unit {target}" if target is not None else "—"
            return f"🎯 Стрельба: цель {target_text}, {weapon}, урон={damage_text}"
        if action == "skip_charge":
            return f"⏭️ Skip charge{reason_text}"
        if action == "charge":
            charge = payload.get("charge") or {}
            target = charge.get("target_id")
            result = charge.get("result") or "—"
            target_text = f"Unit {target}" if target is not None else "—"
            return f"⚡ Чардж: цель {target_text}, результат={result}"
        if action == "skip_fight":
            return f"⏭️ Skip fight{reason_text}"
        if action == "fight":
            fight = payload.get("fight") or {}
            target = fight.get("target_id")
            result = fight.get("result") or "атака"
            target_text = f"Unit {target}" if target is not None else "—"
            return f"⚔️ Бой: цель {target_text}, {result}"
        return f"⏭️ Действие пропущено{reason_text}"

    def _select_row_for_unit(self, side, unit_id):
        unit_key = (side, unit_id)
        row = self._unit_row_by_key.get(unit_key)
        if row is None:
            row = self._find_row_for_unit(unit_key)
        if row is None:
            return
        self.units_table.selectRow(row)
        unit_name = self._units_by_key.get(unit_key, {}).get("name", "—")
        self._append_log([f"Выбрано на карте: unit_id={unit_id}, name={unit_name}"])
        self._on_target_selected(unit_id)

    def _sync_selection_from_table(self):
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
            self.map_scene.select_unit(side, unit_id)
            self._append_log([f"Выбрано в таблице: row={row} -> unit_id={unit_id}"])
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
        self._phase_buffer = None
        self._model_event_cursor = None
        self._set_cinematic_waiting(False)
        self._cinematic_playback_active = False
        self._visual_state = None
        self._pending_snapshot = None
        self._cinematic_history.clear()
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

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if self._cinematic_waiting:
            key = event.key()
            if key in (QtCore.Qt.Key_Y, QtCore.Qt.Key_Yes):
                self._handle_cinematic_continue(True)
                return
            if key in (QtCore.Qt.Key_N, QtCore.Qt.Key_No):
                self._handle_cinematic_continue(False)
                return
        super().keyPressEvent(event)

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
        self.units_table.selectRow(row)

    def _refresh_active_context(self):
        unit_id, side = self._resolve_active_unit()
        self._active_unit_id = unit_id
        self._active_unit_side = side
        if unit_id is not None:
            self._select_row_for_unit_id(unit_id, side=side)
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
        attacker_unit = self._units_by_key.get((attacker_side, event.attacker_id))
        target_unit = self._units_by_key.get((target_side, event.target_id))
        attacker_grid = None
        target_grid = None
        if attacker_unit is not None:
            attacker_grid = self._normalize_grid_xy(attacker_unit.get("x"), attacker_unit.get("y"))
        if target_unit is not None:
            target_grid = self._normalize_grid_xy(target_unit.get("x"), target_unit.get("y"))
        start = self._unit_world_center_by_key(attacker_side, event.attacker_id)
        end = self._unit_world_center_by_key(target_side, event.target_id)
        if start is None or end is None:
            self._fx_debug(
                "FX: не удалось получить координаты для эффекта "
                f"(attacker={event.attacker_id}, target={event.target_id})."
            )
            return
        if attacker_grid is not None or target_grid is not None:
            self.add_log_line(
                "FX: shot grid->world "
                f"attacker_grid={attacker_grid} target_grid={target_grid} "
                f"start=({start.x():.1f},{start.y():.1f}) end=({end.x():.1f},{end.y():.1f})"
            )
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
        for (_, candidate_id), unit in self._units_by_key.items():
            if candidate_id != unit_id:
                continue
            return self._unit_to_world_center(unit)
        return None

    def _unit_to_world_center(self, unit: dict) -> Optional[QtCore.QPointF]:
        x = unit.get("x")
        y = unit.get("y")
        if x is None or y is None:
            return None
        normalized = self._normalize_grid_xy(x, y)
        if normalized is None:
            return None
        x_grid, y_grid = normalized
        return self.map_scene.grid_to_world(x_grid, y_grid)

    def _apply_visual_state(self, state: dict) -> None:
        self._visual_state = copy.deepcopy(state)
        if self._grid_axes_swapped:
            self._swap_state_axes(self._visual_state)
        self._normalize_units_grid_positions(self._visual_state)
        self.map_scene.update_state(self._visual_state)

    def _normalize_units_grid_positions(self, state: dict) -> None:
        units = state.get("units", []) or []
        for unit in units:
            x = unit.get("x")
            y = unit.get("y")
            normalized = self._normalize_grid_xy(x, y)
            if normalized is None:
                continue
            unit["x"], unit["y"] = normalized

    def _swap_state_axes(self, state: dict) -> None:
        for unit in state.get("units", []) or []:
            x = unit.get("x")
            y = unit.get("y")
            if x is None or y is None:
                continue
            unit["x"], unit["y"] = y, x
        for objective in state.get("objectives", []) or []:
            x = objective.get("x")
            y = objective.get("y")
            if x is None or y is None:
                continue
            objective["x"], objective["y"] = y, x

    def _normalize_grid_xy(
        self, x_value: Optional[float], y_value: Optional[float]
    ) -> Optional[Tuple[int, int]]:
        if x_value is None or y_value is None:
            return None
        try:
            return int(x_value), int(y_value)
        except (TypeError, ValueError):
            return None

    def _set_unit_position_to_source(
        self, side: str, unit_id: int, src_xy: Optional[Tuple[int, int]]
    ) -> None:
        if src_xy is None or not self._visual_state:
            return
        src_x, src_y = src_xy
        for unit in self._visual_state.get("units", []) or []:
            if unit.get("id") == unit_id and unit.get("side") == side:
                unit["x"] = src_x
                unit["y"] = src_y
                break
        self.map_scene.set_unit_position_immediate(side, unit_id, src_x, src_y)

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
    window.showMaximized()
    app.exec()
