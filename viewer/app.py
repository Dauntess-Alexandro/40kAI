import torch
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from PySide6 import QtCore, QtGui, QtWidgets

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GYM_PATH = os.path.join(ROOT_DIR, "gym_mod")
if GYM_PATH not in sys.path:
    sys.path.insert(0, GYM_PATH)

from viewer.opengl_view import OpenGLBoardWidget
from viewer.state import StateWatcher
from viewer.styles import Theme

from gym_mod.engine.game_controller import GameController
from gym_mod.engine.game_io import parse_dice_values


@dataclass
class AiStep:
    phase: str
    unit_key: Tuple[str, int]
    action_type: str
    from_pos: Optional[Tuple[int, int]] = None
    to_pos: Optional[Tuple[int, int]] = None
    meta: Dict = field(default_factory=dict)
    duration_ms: int = 300


@dataclass
class AiTurnPlayback:
    mode: str = "live"
    phases: List[str] = field(
        default_factory=lambda: ["command", "move", "shoot", "charge", "fight"]
    )
    steps: List[AiStep] = field(default_factory=list)
    current_step_index: int = 0
    play_state: str = "paused"
    speed: float = 1.0

    def is_active(self) -> bool:
        return self.mode == "playback" and bool(self.steps)


class ViewerWindow(QtWidgets.QMainWindow):
    def __init__(self, state_path, model_path=None):
        super().__init__()
        self.state_path = state_path
        self.setWindowTitle("40kAI Viewer")
        self.resize(1200, 800)

        self.controller = GameController(model_path=model_path, state_path=state_path)
        self._pending_request = None
        self._active_unit_id = None
        self._active_unit_side = None
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
        self._log_tail_snapshot = None
        self._log_tabs = {}
        self._log_tab_defs = [
            ("all", "Все"),
            ("turn", "Ход"),
            ("shooting", "Стрельба"),
            ("fight", "Ближний бой"),
            ("dice", "Кубы"),
            ("errors", "Ошибки"),
        ]
        self._max_log_lines = 5000
        self._log_file_path = os.path.join(ROOT_DIR, "LOGS_FOR_AGENTS.md")
        self._log_file_max_bytes = 5 * 1024 * 1024
        self._init_log_viewer()
        self.add_log_line("[VIEWER] Рендер: OpenGL (QOpenGLWidget).")
        self.add_log_line("[VIEWER] Фоллбэк-рендер не активирован.")

        self._playback = AiTurnPlayback()
        self._playback_timer = QtCore.QTimer(self)
        self._playback_timer.setSingleShot(True)
        self._playback_timer.timeout.connect(self._playback_next_step)
        self._ai_prev_snapshot = None
        self._last_active = None

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
        self.command_prompt = QtWidgets.QLabel("Ожидаю команду...")
        self.command_prompt.setWordWrap(True)
        command_layout.addWidget(self.command_prompt)
        self.command_hint = QtWidgets.QLabel("Горячие клавиши: —")
        self.command_hint.setStyleSheet(f"color: {Theme.muted.name()};")
        command_layout.addWidget(self.command_hint)

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
        layout.addLayout(self._legend_row("Подсветка хода", Theme.selection))
        layout.addLayout(self._legend_row("Подсветка стрельбы", Theme.accent))
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
        self._pending_request = request
        if request is None:
            if self.controller.is_finished:
                self.command_prompt.setText("Игра завершена.")
            else:
                if self._playback.is_active():
                    self.command_prompt.setText(
                        "Playback ИИ активен. Используйте команды ai.* в окне."
                    )
                    self.command_stack.setEnabled(True)
                    self.command_stack.setCurrentIndex(self._command_pages["text"])
                    self.command_hint.setText("Подсказка: ai.next, ai.prev, ai.play, ai.pause")
                else:
                    self.command_prompt.setText("Команда не требуется.")
                    self.command_stack.setEnabled(False)
                    self.command_hint.setText("Горячие клавиши: —")
            self._refresh_active_context()
            return

        self.command_prompt.setText(request.prompt)
        self.command_stack.setEnabled(True)
        kind = getattr(request, "kind", "text")
        if self._playback.is_active():
            self.command_stack.setCurrentIndex(self._command_pages["text"])
            self.command_input.setPlaceholderText("Введите команду...")
        elif kind == "direction":
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
        if self._playback.is_active():
            self.command_hint.setText("Подсказка: ai.next, ai.prev, ai.play, ai.pause")
        self._refresh_active_context()

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
        for key, label in self._log_tab_defs:
            view = QtWidgets.QPlainTextEdit()
            view.setReadOnly(True)
            view.setFont(fixed_font)
            view.setMaximumBlockCount(self._max_log_lines)
            self._log_tabs[key] = view
            self.log_tabs.addTab(view, label)

        self.log_only_current_turn = QtWidgets.QCheckBox("Показать только текущий ход")
        self.log_only_current_turn.toggled.connect(self._refresh_log_views)

        self.log_copy_turn = QtWidgets.QPushButton("Копировать ход")
        self.log_copy_turn.clicked.connect(self._copy_current_turn)
        self.log_clear = QtWidgets.QPushButton("Очистить")
        self.log_clear.clicked.connect(self._clear_log_viewer)

        self._log_controls_layout = QtWidgets.QHBoxLayout()
        self._log_controls_layout.addWidget(self.log_only_current_turn)
        self._log_controls_layout.addStretch()
        self._log_controls_layout.addWidget(self.log_copy_turn)
        self._log_controls_layout.addWidget(self.log_clear)

    def _append_log(self, messages):
        if not messages:
            return
        for msg in messages:
            self.add_log_line(str(msg))

    def _start_controller(self):
        messages, request = self.controller.start()
        self._append_log(messages)
        self._set_request(request)
        self._poll_state()

    def _playback_debug_enabled(self) -> bool:
        return os.getenv("VIEW_PLAYBACK_DEBUG", "0") == "1"

    def _snapshot_state(self, state: Dict) -> Dict:
        snapshot = {
            "turn": state.get("turn"),
            "round": state.get("round"),
            "phase": state.get("phase"),
            "active": state.get("active"),
            "units": [],
        }
        for unit in state.get("units", []) or []:
            snapshot["units"].append(
                {
                    "side": unit.get("side"),
                    "id": unit.get("id"),
                    "x": unit.get("x"),
                    "y": unit.get("y"),
                    "hp": unit.get("hp"),
                    "models": unit.get("models"),
                }
            )
        return snapshot

    def _build_ai_steps(
        self,
        prev_snapshot: Dict,
        next_snapshot: Dict,
        log_tail: Optional[List[str]] = None,
    ) -> List[AiStep]:
        steps: List[AiStep] = []
        phases = self._playback.phases
        prev_units = {
            (unit.get("side"), unit.get("id")): unit for unit in prev_snapshot.get("units", [])
        }
        next_units = [
            unit
            for unit in next_snapshot.get("units", [])
            if unit.get("side") == "model"
        ]
        next_units.sort(key=lambda item: item.get("id", 0))

        phase_counts = {phase: 0 for phase in phases}

        for phase in phases:
            for unit in next_units:
                unit_key = (unit.get("side"), unit.get("id"))
                if unit_key[0] is None or unit_key[1] is None:
                    continue
                if phase == "command":
                    steps.append(
                        AiStep(
                            phase=phase,
                            unit_key=unit_key,
                            action_type="highlight",
                            duration_ms=320,
                        )
                    )
                elif phase == "move":
                    steps.append(
                        AiStep(
                            phase=phase,
                            unit_key=unit_key,
                            action_type="highlight",
                            duration_ms=240,
                        )
                    )
                    prev_unit = prev_units.get(unit_key, {})
                    from_pos = (prev_unit.get("x"), prev_unit.get("y"))
                    to_pos = (unit.get("x"), unit.get("y"))
                    if (
                        None not in from_pos
                        and None not in to_pos
                        and from_pos != to_pos
                    ):
                        steps.append(
                            AiStep(
                                phase=phase,
                                unit_key=unit_key,
                                action_type="move",
                                from_pos=(int(from_pos[0]), int(from_pos[1])),
                                to_pos=(int(to_pos[0]), int(to_pos[1])),
                                duration_ms=650,
                            )
                        )
                else:
                    steps.append(
                        AiStep(
                            phase=phase,
                            unit_key=unit_key,
                            action_type="highlight",
                            duration_ms=260,
                        )
                    )
            phase_counts[phase] = sum(1 for step in steps if step.phase == phase)

        if self._playback_debug_enabled():
            self.add_log_line(
                f"[PLAYBACK] Построено шагов: {len(steps)}. "
                + ", ".join(f"{phase}={phase_counts[phase]}" for phase in phases)
            )
            for step in steps:
                if step.action_type == "move":
                    self.add_log_line(
                        "[PLAYBACK] move: "
                        f"{step.unit_key} {step.from_pos} -> {step.to_pos}"
                    )
        return steps

    def _start_ai_playback(self, prev_snapshot: Dict, next_snapshot: Dict, log_tail=None):
        steps = self._build_ai_steps(prev_snapshot, next_snapshot, log_tail=log_tail)
        if not steps:
            self._playback.mode = "live"
            self._playback.steps = []
            return
        self._playback.mode = "playback"
        self._playback.steps = steps
        self._playback.current_step_index = 0
        self._playback.play_state = "paused"
        self.map_scene.prepare_playback_positions()
        self.map_scene.clear_playback_overlays()
        self._playback_run_current_step(schedule_next=False)
        self._set_request(self._pending_request)

    def _reset_playback(self):
        if self._playback_timer.isActive():
            self._playback_timer.stop()
        self._playback.mode = "live"
        self._playback.steps = []
        self._playback.current_step_index = 0
        self._playback.play_state = "paused"
        self.map_scene.clear_playback_overlays()

    def _playback_effective_duration(self, duration_ms: int) -> int:
        speed = max(0.1, float(self._playback.speed or 1.0))
        return max(40, int(duration_ms / speed))

    def _playback_run_current_step(self, schedule_next: bool = True):
        if not self._playback.is_active():
            return
        index = max(0, min(self._playback.current_step_index, len(self._playback.steps) - 1))
        self._playback.current_step_index = index
        step = self._playback.steps[index]
        self._playback_execute_step(step, allow_animation=True)
        if self._playback_debug_enabled():
            self.add_log_line(
                "[PLAYBACK] Шаг "
                f"{index + 1}/{len(self._playback.steps)}: "
                f"{step.phase} {step.unit_key} {step.action_type} "
                f"{step.duration_ms}мс"
            )
        if schedule_next and self._playback.play_state == "playing":
            duration = self._playback_effective_duration(step.duration_ms)
            self._playback_timer.start(duration)

    def _playback_execute_step(self, step: AiStep, *, allow_animation: bool):
        self.map_scene.set_playback_phase(step.phase)
        self.map_scene.set_playback_active_unit(step.unit_key)
        self.status_phase.setText(f"Фаза (playback): {step.phase}")
        if step.action_type == "move" and allow_animation:
            self.map_scene.play_move_animation(
                step.unit_key,
                step.from_pos,
                step.to_pos,
                self._playback_effective_duration(step.duration_ms),
            )
        elif step.action_type in {"shoot", "charge", "fight"} and allow_animation:
            target_key = step.meta.get("target_key")
            if target_key:
                self.map_scene.play_shoot_effect(
                    step.unit_key,
                    target_key,
                    self._playback_effective_duration(step.duration_ms),
                )
        self.map_scene.update()

    def _playback_next_step(self):
        if not self._playback.is_active():
            return
        if self._playback.current_step_index >= len(self._playback.steps) - 1:
            self._playback.play_state = "paused"
            return
        self._playback.current_step_index += 1
        self._playback_run_current_step(schedule_next=True)

    def _playback_prev_step(self):
        if not self._playback.is_active():
            return
        if self._playback_timer.isActive():
            self._playback_timer.stop()
        if self._playback.current_step_index <= 0:
            self._playback.current_step_index = 0
        else:
            self._playback.current_step_index -= 1
        step = self._playback.steps[self._playback.current_step_index]
        self._playback_execute_step(step, allow_animation=False)

    def _playback_find_phase_index(self, phase: str) -> Optional[int]:
        phase_list = self._playback.phases
        try:
            return phase_list.index(phase)
        except ValueError:
            return None

    def _playback_goto_phase(self, direction: int):
        if not self._playback.is_active():
            return
        current_phase = self._playback.steps[self._playback.current_step_index].phase
        current_idx = self._playback_find_phase_index(current_phase)
        if current_idx is None:
            return
        next_idx = current_idx + direction
        if next_idx < 0 or next_idx >= len(self._playback.phases):
            return
        next_phase = self._playback.phases[next_idx]
        for idx, step in enumerate(self._playback.steps):
            if step.phase == next_phase:
                self._playback.current_step_index = idx
                self._playback_run_current_step(schedule_next=False)
                return

    def _playback_goto_unit(self, phase: str, unit_index: int):
        if not self._playback.is_active():
            return
        highlight_steps = [
            (idx, step)
            for idx, step in enumerate(self._playback.steps)
            if step.phase == phase and step.action_type == "highlight"
        ]
        if not highlight_steps:
            self.add_log_line(
                "Playback: фаза не найдена. Где: ai.goto. "
                "Что делать дальше: используйте command/move/shoot/charge/fight."
            )
            return
        target_idx = unit_index - 1
        if target_idx < 0 or target_idx >= len(highlight_steps):
            self.add_log_line(
                "Playback: неверный индекс юнита. Где: ai.goto. "
                "Что делать дальше: используйте индекс 1..N."
            )
            return
        self._playback.current_step_index = highlight_steps[target_idx][0]
        self._playback_run_current_step(schedule_next=False)

    def _playback_status(self):
        if not self._playback.is_active():
            self.add_log_line(
                "Playback не активен. Где: viewer/app.py. "
                "Что делать дальше: дождитесь хода ИИ и попробуйте снова."
            )
            return
        step = self._playback.steps[self._playback.current_step_index]
        self.add_log_line(
            "Playback: шаг "
            f"{self._playback.current_step_index + 1}/{len(self._playback.steps)}, "
            f"фаза={step.phase}, unit={step.unit_key}, "
            f"state={self._playback.play_state}, speed={self._playback.speed}"
        )

    def _handle_ai_command(self, text: str) -> bool:
        lowered = text.strip().lower()
        if not lowered.startswith("ai."):
            return False
        if not self._playback.is_active():
            self.add_log_line(
                "Playback не активен. Где: командное окно. "
                "Что делать дальше: дождитесь завершения хода ИИ."
            )
            return True
        if lowered == "ai.next":
            self._playback_next_step()
            return True
        if lowered == "ai.prev":
            self._playback_prev_step()
            return True
        if lowered == "ai.phase.next":
            self._playback_goto_phase(1)
            return True
        if lowered == "ai.phase.prev":
            self._playback_goto_phase(-1)
            return True
        if lowered == "ai.play":
            self._playback.play_state = "playing"
            self._playback_run_current_step(schedule_next=True)
            return True
        if lowered == "ai.pause":
            self._playback.play_state = "paused"
            if self._playback_timer.isActive():
                self._playback_timer.stop()
            return True
        if lowered.startswith("ai.speed"):
            parts = lowered.split()
            if len(parts) < 2:
                self.add_log_line(
                    "Playback: не задана скорость. Где: ai.speed. "
                    "Что делать дальше: укажите число 0.25..4.0."
                )
                return True
            try:
                speed = float(parts[1])
            except ValueError:
                self.add_log_line(
                    "Playback: неверная скорость. Где: ai.speed. "
                    "Что делать дальше: используйте число 0.25..4.0."
                )
                return True
            speed = max(0.25, min(4.0, speed))
            self._playback.speed = speed
            self.add_log_line(f"Playback: скорость установлена на {speed:.2f}x.")
            return True
        if lowered.startswith("ai.goto"):
            parts = lowered.split()
            if len(parts) < 3:
                self.add_log_line(
                    "Playback: неверная команда goto. Где: ai.goto. "
                    "Что делать дальше: ai.goto PHASE INDEX."
                )
                return True
            phase = parts[1]
            try:
                unit_index = int(parts[2])
            except ValueError:
                self.add_log_line(
                    "Playback: неверный индекс. Где: ai.goto. "
                    "Что делать дальше: укажите целое число."
                )
                return True
            self._playback_goto_unit(phase, unit_index)
            return True
        if lowered == "ai.status":
            self._playback_status()
            return True
        if lowered == "ai.skip":
            self._reset_playback()
            self.add_log_line("Playback отключён. Показ финального состояния активен.")
            self._set_request(self._pending_request)
            return True
        self.add_log_line(
            "Playback: неизвестная команда. Где: командное окно. "
            "Что делать дальше: используйте ai.next/ai.prev/ai.play/ai.pause."
        )
        return True

    def _submit_text(self):
        text = self.command_input.text().strip()
        if not text:
            return
        if self._handle_ai_command(text):
            self.command_input.clear()
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
        self._submit_answer(value)

    def _submit_answer(self, value):
        if self._pending_request is None:
            return
        messages, request = self.controller.answer(value)
        self._append_log(messages)
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
        prev_active = self._last_active
        current_active = state.get("active")
        start_ai_turn = current_active == "model" and prev_active != "model"
        end_ai_turn = prev_active == "model" and current_active != "model"
        if start_ai_turn:
            self._ai_prev_snapshot = self._snapshot_state(state)
            self._reset_playback()
        self.map_scene.update_state(state)
        if end_ai_turn:
            if self._ai_prev_snapshot:
                self._start_ai_playback(
                    self._ai_prev_snapshot,
                    self._snapshot_state(state),
                    log_tail=state.get("log_tail", []),
                )
            self._ai_prev_snapshot = None
        self._last_active = current_active

        self._units_by_key = {}
        for unit in state.get("units", []) or []:
            self._units_by_key[(unit.get("side"), unit.get("id"))] = unit

        self.status_round.setText(f"Раунд: {state.get('round', '—')}")
        self.status_turn.setText(f"Ход: {state.get('turn', '—')}")
        if self._playback.is_active():
            step = self._playback.steps[self._playback.current_step_index]
            self.status_phase.setText(f"Фаза (playback): {step.phase}")
        else:
            self.status_phase.setText(f"Фаза: {state.get('phase', '—')}")
        active = state.get("active")
        active_label = "Игрок" if active == "player" else "Модель" if active == "model" else "—"
        self.status_active.setText(f"Активен: {active_label}")

        vp = state.get("vp", {})
        cp = state.get("cp", {})
        self.points_vp_player.setText(f"Player VP: {vp.get('player', '—')}")
        self.points_vp_model.setText(f"Model VP: {vp.get('model', '—')}")
        self.points_cp_player.setText(f"Player CP: {cp.get('player', '—')}")
        self.points_cp_model.setText(f"Model CP: {cp.get('model', '—')}")

        self._populate_units_table(state.get("units", []))
        self._update_log(state.get("log_tail", []))
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
            existing = [entry["text"] for entry in self._log_entries]
            if len(text_lines) >= len(existing) and text_lines[: len(existing)] == existing:
                for line in text_lines[len(existing) :]:
                    self.add_log_line(line)
                self._log_tail_snapshot = text_lines
                return
            self._reset_log_lines(text_lines, write_to_file=False)
            self._log_tail_snapshot = text_lines

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

    def add_log_line(self, line: str):
        text = str(line)
        new_turn = self._detect_turn_number(text)
        if new_turn is not None:
            self._current_turn_number = new_turn
        categories = self._classify_line(text)
        entry = {
            "text": text,
            "turn": self._current_turn_number,
            "categories": categories,
        }
        self._log_entries.append(entry)
        self._append_log_to_file(text)
        if len(self._log_entries) > self._max_log_lines:
            self._log_entries = self._log_entries[-self._max_log_lines :]
            self._refresh_log_views()
            return
        if new_turn is not None and self.log_only_current_turn.isChecked():
            self._refresh_log_views()
            return
        for key, _ in self._log_tab_defs:
            if self._should_show_entry(entry, key):
                self._append_to_view(self._log_tabs[key], text)

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
                "боевого раунда",
                "фаза",
                "===",
                "iteration",
                "раунд",
                "turn",
            ],
        ):
            categories.add("turn")
        if self._matches_any(
            lowered,
            [
                "[shoot]",
                "отчёт по стрельбе",
                "hit rolls",
                "wound",
                "save",
                "оружие",
                "стрельб",
            ],
        ):
            categories.add("shooting")
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
        return categories

    def _matches_any(self, lowered: str, tokens):
        return any(token in lowered for token in tokens)

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

    def _should_show_entry(self, entry, tab_key):
        if tab_key != "all" and tab_key not in entry["categories"]:
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
                    grouped_lines[key].append(entry["text"])
        for key, lines in grouped_lines.items():
            if lines:
                self._log_tabs[key].setPlainText("\n".join(lines))
                scrollbar = self._log_tabs[key].verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())

    def _reset_log_lines(self, lines, write_to_file: bool):
        self._log_entries = []
        self._current_turn_number = None
        for line in lines:
            if write_to_file:
                self.add_log_line(line)
            else:
                text = str(line)
                new_turn = self._detect_turn_number(text)
                if new_turn is not None:
                    self._current_turn_number = new_turn
                self._log_entries.append(
                    {
                        "text": text,
                        "turn": self._current_turn_number,
                        "categories": self._classify_line(text),
                    }
                )
        self._refresh_log_views()

    def _clear_log_viewer(self):
        self._log_entries = []
        self._current_turn_number = None
        self._log_tail_snapshot = None
        for view in self._log_tabs.values():
            view.clear()

    def _collect_current_turn_logs(self):
        if self._current_turn_number is None:
            return "\n".join(entry["text"] for entry in self._log_entries)
        return "\n".join(
            entry["text"]
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
        match = re.search(r"(?:юнит|unit)\\s*#?\\s*(\\d+)", prompt, re.IGNORECASE)
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

    def _refresh_active_context(self):
        unit_id, side = self._resolve_active_unit()
        self._active_unit_id = unit_id
        self._active_unit_side = side
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
