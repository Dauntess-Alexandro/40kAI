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
        "terrain_barrel_cell_scale": 0.92,
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
from gym_mod.engine.mission import validate_deploy_coord


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
        os.environ.setdefault("DEPLOYMENT_MODE", "manual_player")
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
        self._shoot_targets_valid: set[int] = set()
        self._shoot_request_flow_active = False
        self._shoot_popover_target_id: Optional[int] = None
        self._shoot_resolver_active = False
        self._shoot_resolver_step = 0
        self._shoot_resolver_attacker_id: Optional[int] = None
        self._shoot_locked_target_id: Optional[int] = None
        self._active_weapon_name: Optional[str] = None
        self._active_weapon_range: Optional[int] = None
        self._active_weapon_unit_id: Optional[int] = None
        self._show_objective_radius = True
        self._units_by_key = {}
        self._unit_row_by_key = {}
        self._did_initial_fit = False
        self._board_debug_logged = False
        self._deploy_status_text = ""
        self._deploy_context = None
        self._deploy_hover_cell = None
        self._deploy_visual_reset_done = False
        self._movement_skip_sent = False
        self._rolloff_attacker_side: Optional[str] = None
        self._rolloff_defender_side: Optional[str] = None

        self._viewer_config = load_viewer_config()
        cell_size = int(self._viewer_config.get("cell_size", 24))
        unit_icon_scale = float(self._viewer_config.get("unit_icon_scale", 2.75))
        model_icon_scale = float(self._viewer_config.get("model_icon_scale", 0.75))
        terrain_barrel_cell_scale = float(self._viewer_config.get("terrain_barrel_cell_scale", 0.92))

        self.state_watcher = StateWatcher(self.state_path)
        self.map_scene = OpenGLBoardWidget(
            cell_size=max(8, cell_size),
            unit_icon_scale=max(0.25, unit_icon_scale),
            model_icon_scale=max(0.2, model_icon_scale),
            terrain_barrel_cell_scale=max(0.1, min(1.0, terrain_barrel_cell_scale)),
        )
        self.map_scene.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.map_scene.unit_selected.connect(self._select_row_for_unit)
        self.map_scene.cell_clicked.connect(self._on_cell_clicked)
        self.map_scene.cell_right_clicked.connect(self._on_cell_right_clicked)
        self.map_scene.cell_hovered.connect(self._on_cell_hovered)
        self.map_scene.unit_right_clicked.connect(self._on_unit_right_clicked)
        self.map_scene.shoot_overlay_mode_changed.connect(self._on_shoot_overlay_mode_changed)

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
        self._log_file_path = os.path.join(ROOT_DIR, "LOGS_FOR_AGENTS_PLAY.md")
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
        self.command_group = command_group
        command_layout = QtWidgets.QVBoxLayout(command_group)
        self.command_prompt = QtWidgets.QLabel("Ожидаю команду...")
        self.command_prompt.setWordWrap(True)
        command_layout.addWidget(self.command_prompt)
        self.command_hint = QtWidgets.QLabel("Горячие клавиши: —")
        self.command_hint.setStyleSheet(f"color: {Theme.muted.name()};")
        command_layout.addWidget(self.command_hint)

        self.command_stack = QtWidgets.QStackedWidget()
        self._build_command_pages()
        self._build_shoot_popover()
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

    def _build_shoot_popover(self) -> None:
        self.shoot_popover = QtWidgets.QFrame(self, QtCore.Qt.Popup)
        self.shoot_popover.setObjectName("shootPopover")
        self.shoot_popover.setStyleSheet(
            f"QFrame#shootPopover {{ background: {Theme.panel.name()}; border: 1px solid {Theme.outline.name()}; border-radius: 12px; }}"
        )
        if not sys.platform.startswith("win"):
            shadow = QtWidgets.QGraphicsDropShadowEffect(self.shoot_popover)
            shadow.setBlurRadius(18)
            shadow.setOffset(0, 6)
            shadow.setColor(QtGui.QColor(0, 0, 0, 130))
            self.shoot_popover.setGraphicsEffect(shadow)

        layout = QtWidgets.QVBoxLayout(self.shoot_popover)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)
        # На Windows popup может пересчитать minimum size после show() (DPI/font metrics),
        # поэтому не форсим resize вручную и просим layout держать фиксированный sizeHint.
        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.shoot_popover_title = QtWidgets.QLabel("FIRE")
        self.shoot_popover_title.setStyleSheet(f"font-size: 17px; font-weight: 700; color: {Theme.text.name()};")
        self.shoot_popover_units = QtWidgets.QLabel("Unit — → Unit —")
        self.shoot_popover_units.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Theme.text.name()};")
        self.shoot_popover_meta = QtWidgets.QLabel("Weapon: — • Range — • LoS —")
        self.shoot_popover_meta.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        self.shoot_popover_meta.setWordWrap(False)
        layout.addWidget(self.shoot_popover_title)
        layout.addWidget(self.shoot_popover_units)
        layout.addWidget(self.shoot_popover_meta)

        self.shoot_stepper = QtWidgets.QLabel("Hit • Wound • Allocate • Save • Damage")
        self.shoot_stepper.setWordWrap(False)
        self.shoot_stepper.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        layout.addWidget(self.shoot_stepper)

        self.shoot_popover_step_title = QtWidgets.QLabel("STEP 1/5: Hit Roll")
        self.shoot_popover_step_title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Theme.text.name()};")
        self.shoot_popover_step_summary = QtWidgets.QLabel("Need: — dice")
        self.shoot_popover_step_summary.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        layout.addWidget(self.shoot_popover_step_title)
        layout.addWidget(self.shoot_popover_step_summary)

        self.shoot_popover_input_label = QtWidgets.QLabel("Кубы (D6):")
        self.shoot_popover_input_label.setStyleSheet(f"font-size: 12px; color: {Theme.text.name()};")
        layout.addWidget(self.shoot_popover_input_label)

        input_row = QtWidgets.QHBoxLayout()
        input_row.setSpacing(8)
        self.shoot_popover_dice_input = QtWidgets.QLineEdit()
        self.shoot_popover_dice_input.setPlaceholderText("например: 4 1 6 2 3 5 2 6")
        self.shoot_popover_dice_input.textChanged.connect(self._on_shoot_dice_input_changed)
        self.shoot_popover_dice_counter = QtWidgets.QLabel("0/0")
        self.shoot_popover_dice_counter.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()}; min-width: 42px;")
        input_row.addWidget(self.shoot_popover_dice_input, 1)
        input_row.addWidget(self.shoot_popover_dice_counter, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addLayout(input_row)

        self.shoot_popover_info = QtWidgets.QLabel("ℹ Нажмите Roll Hit, чтобы начать")
        self.shoot_popover_info.setWordWrap(True)
        self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        layout.addWidget(self.shoot_popover_info)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(8)
        self.shoot_popover_action = QtWidgets.QPushButton("Roll Hit")
        self.shoot_popover_cancel = QtWidgets.QPushButton("Cancel")
        self.shoot_popover_action.setStyleSheet(
            "QPushButton { background: #2b7cff; color: #ffffff; border: 1px solid #3d8cff; border-radius: 8px; padding: 7px 12px; font-weight: 600; }"
            "QPushButton:hover { background: #3d8cff; }"
            "QPushButton:disabled { background: #334b77; color: #9bb3d8; border-color: #415980; }"
        )
        self.shoot_popover_cancel.setStyleSheet(
            f"QPushButton {{ background: {Theme.panel_alt.name() if hasattr(Theme, 'panel_alt') else Theme.panel.name()}; color: {Theme.text.name()}; border: 1px solid {Theme.outline.name()}; border-radius: 8px; padding: 7px 12px; }}"
            f"QPushButton:hover {{ border-color: {Theme.accent.name() if hasattr(Theme, 'accent') else Theme.text.name()}; }}"
        )
        self.shoot_popover_action.setMinimumHeight(34)
        self.shoot_popover_cancel.setMinimumHeight(34)
        self.shoot_popover_action.clicked.connect(self._shoot_step_action)
        self.shoot_popover_cancel.clicked.connect(self._close_shoot_popover)
        btn_row.addWidget(self.shoot_popover_action)
        btn_row.addWidget(self.shoot_popover_cancel)
        layout.addLayout(btn_row)

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self.shoot_popover, activated=self._shoot_step_action)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self.shoot_popover, activated=self._shoot_step_action)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self.shoot_popover, activated=self._close_shoot_popover)
        self.shoot_popover.hide()

    def _is_shooting_target_request(self, request) -> bool:
        if not self._is_target_request(request):
            return False
        prompt = str(getattr(request, "prompt", "") or "").lower()
        return ("стрель" in prompt) or ("shoot" in prompt)

    def _is_shooting_dice_request(self, request) -> bool:
        if request is None:
            return False
        return bool(getattr(request, "kind", "") == "dice" and self._shoot_request_flow_active)

    def _shoot_instruction_text(self) -> str:
        unit_id, side = self._resolve_active_unit()
        if unit_id is None:
            unit_id = self._shoot_resolver_attacker_id or self._last_shooter_id
            side = self._side_from_unit_id(int(unit_id)) if unit_id is not None else side
        unit = self._units_by_key.get((side, unit_id)) if unit_id is not None and side is not None else None
        weapon = "—"
        weapon_range = None
        if isinstance(unit, dict):
            weapon, weapon_range = self._resolve_active_weapon(unit)
        unit_label = str(unit_id) if unit_id is not None else "—"
        weapon_suffix = f" (R{weapon_range})" if isinstance(weapon_range, int) and weapon_range > 0 else ""
        overlay_mode = "Targets"
        if hasattr(self, "map_scene") and hasattr(self.map_scene, "shooting_overlay_mode_label"):
            overlay_mode = str(self.map_scene.shooting_overlay_mode_label())
        return (
            f"Стрельба: Unit {unit_label}\n"
            f"Weapon: {weapon}{weapon_suffix} • Overlay: {overlay_mode}\n"
            "ПКМ по врагу: выбрать цель • R: показать/скрыть клетки\n"
            "Enter: Continue • Esc: Cancel"
        )

    def _valid_target_ids_from_request(self, request) -> set[int]:
        ids: set[int] = set()
        for opt in list(getattr(request, "options", []) or []):
            parsed = self._extract_unit_id(str(opt))
            if parsed is not None:
                ids.add(int(parsed))
        return ids

    def _shoot_stepper_text(self) -> str:
        names = ["Hit", "Wound", "Allocate", "Save", "Damage"]
        parts = []
        for idx, name in enumerate(names):
            if idx < self._shoot_resolver_step:
                parts.append(f"✓ {name}")
            elif idx == self._shoot_resolver_step:
                parts.append(f"[{name}]")
            else:
                parts.append(name)
        return " • ".join(parts)

    def _count_dice_tokens(self, raw: str) -> tuple[int, bool, bool]:
        cleaned = str(raw or "").strip()
        if not cleaned:
            return 0, False, False
        if re.search(r"[^0-9,\s]", cleaned):
            return 0, True, False
        normalized = re.sub(r"[\s,]+", " ", cleaned).strip()
        if not normalized:
            return 0, False, False
        tokens = [tok for tok in normalized.split(" ") if tok]
        invalid_value = any((not tok.isdigit()) or int(tok) < 1 or int(tok) > 6 for tok in tokens)
        return len(tokens), invalid_value, True

    def _on_shoot_dice_input_changed(self, _text: str) -> None:
        self._update_shoot_input_feedback()

    def _update_shoot_input_feedback(self) -> None:
        if not hasattr(self, "shoot_popover") or not self._shoot_resolver_active:
            return
        req = self._pending_request
        expects_dice = bool(getattr(req, "kind", "") == "dice" and self._shoot_resolver_step in (0, 1, 3))
        if not expects_dice:
            self.shoot_popover_dice_counter.setText("0/0")
            self.shoot_popover_info.setText("ℹ На этом шаге ввод кубов не требуется")
            self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
            return

        count = int(getattr(req, "count", 0) or 0)
        lock_suffix = ""
        if self._is_shooting_dice_request(req) and self._shoot_locked_target_id is not None:
            lock_suffix = f" • Цель Unit {int(self._shoot_locked_target_id)} зафиксирована"
        entered, has_error, has_tokens = self._count_dice_tokens(self.shoot_popover_dice_input.text())
        self.shoot_popover_dice_counter.setText(f"{entered}/{count}")
        if has_error:
            self.shoot_popover_info.setText("⚠ Допустимы только значения 1..6 через пробел или запятую")
            self.shoot_popover_info.setStyleSheet("font-size: 12px; color: #e06c75;")
            return

        if count <= 0:
            self.shoot_popover_info.setText(f"ℹ Движок не запросил количество кубов{lock_suffix}")
            self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
            return

        if entered < count:
            rest = count - entered
            if has_tokens:
                self.shoot_popover_info.setText(f"ℹ Нужно: {count} значений d6 • Осталось: {rest}{lock_suffix}")
            else:
                self.shoot_popover_info.setText(f"ℹ Нужно: {count} значений d6. Пример: 4 1 6 2 3 5 2 6{lock_suffix}")
            self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        elif entered > count:
            extra = entered - count
            self.shoot_popover_info.setText(f"⚠ Лишних: {extra}. Нужно ровно {count} значений d6{lock_suffix}")
            self.shoot_popover_info.setStyleSheet("font-size: 12px; color: #d8b26e;")
        else:
            self.shoot_popover_info.setText(f"ℹ Готово к броску{lock_suffix}")
            self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")

    def _parse_popover_dice_values(self, request) -> Optional[list[int]]:
        count = int(getattr(request, "count", 0) or 0)
        min_value = int(getattr(request, "min_value", 1) or 1)
        max_value = int(getattr(request, "max_value", 6) or 6)
        raw = self.shoot_popover_dice_input.text().strip()
        if not raw:
            self.shoot_popover_info.setText(f"ℹ Нужно: {count} значений d6")
            self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
            return None
        try:
            return parse_dice_values(raw, count=count, min_value=min_value, max_value=max_value)
        except ValueError as exc:
            self.shoot_popover_info.setText(f"⚠ Ошибка ввода: {exc}")
            self.shoot_popover_info.setStyleSheet("font-size: 12px; color: #e06c75;")
            if os.getenv("VIEWER_DEBUG", "0") == "1":
                self.add_log_line(f"[VIEWER_DEBUG] FIRE input parse error: {exc}")
            return None

    def _update_shoot_popover_ui(self) -> None:
        if not self._shoot_resolver_active or self._shoot_popover_target_id is None:
            return
        attacker = self._shoot_resolver_attacker_id
        request = self._pending_request
        locked_target = self._shoot_locked_target_id
        if self._is_shooting_dice_request(request) and locked_target is not None:
            target = int(locked_target)
            self._shoot_popover_target_id = int(locked_target)
        else:
            target = int(self._shoot_popover_target_id)
        self.shoot_popover_title.setText("FIRE")
        self.shoot_popover_units.setText(f"Unit {attacker} → Unit {target}")
        weapon = "—"
        weapon_range = None
        if attacker is not None:
            shooter_side = self._side_from_unit_id(int(attacker))
            if shooter_side is not None:
                unit = self._units_by_key.get((shooter_side, int(attacker)))
                if isinstance(unit, dict):
                    weapon, weapon_range = self._resolve_active_weapon(unit)
                    self._remember_active_weapon(attacker, weapon, weapon_range)
        range_text = f"R{weapon_range}" if isinstance(weapon_range, int) and weapon_range > 0 else "—"
        overlay_mode = "Targets"
        if hasattr(self, "map_scene") and hasattr(self.map_scene, "shooting_overlay_mode_label"):
            overlay_mode = str(self.map_scene.shooting_overlay_mode_label())
        self.shoot_popover_meta.setText(f"Weapon: {weapon} ({range_text}) • Overlay: {overlay_mode} • LoS OK")
        self.shoot_stepper.setText(self._shoot_stepper_text())

        step = self._shoot_resolver_step
        dice_mode = getattr(request, "kind", "") == "dice"
        count = int(getattr(request, "count", 0) or 0)

        needs_input = dice_mode and step in (0, 1, 3)
        self.shoot_popover_input_label.setVisible(needs_input)
        self.shoot_popover_dice_input.setVisible(needs_input)
        self.shoot_popover_dice_counter.setVisible(needs_input)
        if needs_input and count > 0:
            self.shoot_popover_dice_input.setPlaceholderText("например: 4 1 6 2 3 5 2 6")

        if step == 0:
            self.shoot_popover_step_title.setText("STEP 1/5: Hit Roll")
            self.shoot_popover_step_summary.setText(f"Need: {count if dice_mode else '—'} dice")
            self.shoot_popover_action.setText("Roll Hit")
            if not dice_mode:
                self.shoot_popover_info.setText("ℹ Нажмите Roll Hit, чтобы выбрать цель и перейти к броску")
                self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        elif step == 1:
            self.shoot_popover_step_title.setText("STEP 2/5: Wound Roll")
            self.shoot_popover_step_summary.setText(f"Need: {count if dice_mode else '—'} dice")
            self.shoot_popover_action.setText("Roll Wound")
            if not dice_mode:
                self.shoot_popover_info.setText("ℹ Ожидаю запрос кубов Wound от движка")
                self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        elif step == 2:
            self.shoot_popover_step_title.setText("STEP 3/5: Allocate Attack")
            self.shoot_popover_step_summary.setText("Need: — dice")
            self.shoot_popover_action.setText("Continue")
            self.shoot_popover_info.setText("ℹ Allocate Attack — skipped for now")
            self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        elif step == 3:
            self.shoot_popover_step_title.setText("STEP 4/5: Saving Throw")
            self.shoot_popover_step_summary.setText(f"Need: {count if dice_mode else '—'} dice")
            self.shoot_popover_action.setText("Roll Save")
            if not dice_mode:
                self.shoot_popover_info.setText("ℹ Ожидаю запрос кубов Save от движка")
                self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
        else:
            self.shoot_popover_step_title.setText("STEP 5/5: Inflict Damage")
            self.shoot_popover_step_summary.setText("Need: — dice")
            self.shoot_popover_action.setText("Finish")
            self.shoot_popover_info.setText("ℹ Inflict Damage — skipped for now")
            self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")

        if needs_input:
            if self._is_shooting_dice_request(request) and self._shoot_locked_target_id is not None:
                self.shoot_popover_info.setText(
                    "ℹ Цель зафиксирована для текущего выстрела. Чтобы сменить цель: Cancel и выберите заново."
                )
                self.shoot_popover_info.setStyleSheet(f"font-size: 12px; color: {Theme.muted.name()};")
            self._update_shoot_input_feedback()

    def _open_shoot_popover(self, target_id: int, global_pos: Optional[QtCore.QPoint] = None) -> None:
        if target_id not in self._shoot_targets_valid:
            return
        req = self._pending_request
        if self._is_shooting_dice_request(req) and self._shoot_locked_target_id is not None:
            locked = int(self._shoot_locked_target_id)
            if int(target_id) != locked:
                self.add_log_line(
                    f"REQ: цель Unit {int(target_id)} отклонена. Где: viewer/app.py (_open_shoot_popover). "
                    f"Что случилось: на шаге кубов цель уже зафиксирована как Unit {locked}. "
                    "Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново."
                )
                return
        if not self._shoot_resolver_active:
            self._shoot_resolver_step = 0
        self._shoot_resolver_active = True
        if self._shoot_resolver_attacker_id is None:
            self._shoot_resolver_attacker_id = self._active_unit_id or self._last_shooter_id
        if getattr(req, "kind", "") == "dice" and self._shoot_popover_target_id is not None:
            self._shoot_resolver_step = max(self._shoot_resolver_step, 1)
        self._current_target_id = int(target_id)
        self.map_scene.set_target_unit(int(target_id))
        self._shoot_popover_target_id = int(target_id)
        self.shoot_popover_dice_input.clear()
        self._update_shoot_popover_ui()
        anchor = global_pos or QtGui.QCursor.pos()
        self.shoot_popover.adjustSize()
        self.shoot_popover.show()
        popup_h = self.shoot_popover.frameGeometry().height()
        pos = QtCore.QPoint(anchor.x() + 18, anchor.y() - popup_h - 12)
        self.shoot_popover.move(pos)
        self.shoot_popover.raise_()
        self.shoot_popover.activateWindow()
        self.shoot_popover_action.setFocus()

    def _close_shoot_popover(self) -> None:
        self._shoot_popover_target_id = None
        self._shoot_locked_target_id = None
        self._shoot_resolver_active = False
        self._shoot_resolver_step = 0
        self._shoot_resolver_attacker_id = None
        if hasattr(self, "shoot_popover"):
            self.shoot_popover.hide()
        if self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(self._pending_request):
            self.command_prompt.setText(self._shoot_instruction_text())

    def _shoot_step_action(self) -> None:
        if not self._shoot_resolver_active:
            return
        req = self._pending_request
        step = self._shoot_resolver_step
        target_id = self._shoot_popover_target_id
        if target_id is None:
            self._close_shoot_popover()
            return

        if step == 0:
            if self._is_shooting_target_request(req):
                self._shoot_locked_target_id = int(target_id)
                self._submit_answer(str(int(target_id)))
                req = self._pending_request
            if getattr(req, "kind", "") != "dice":
                self._update_shoot_popover_ui()
                return
            values = self._parse_popover_dice_values(req)
            if values is None:
                return
            self._submit_answer(values)
            self._shoot_resolver_step = 1
            self.shoot_popover_dice_input.clear()
        elif step == 1:
            if getattr(req, "kind", "") != "dice":
                self._update_shoot_popover_ui()
                return
            values = self._parse_popover_dice_values(req)
            if values is None:
                return
            self._submit_answer(values)
            self._shoot_resolver_step = 2
            self.shoot_popover_dice_input.clear()
        elif step == 2:
            self._shoot_resolver_step = 3
        elif step == 3:
            if getattr(req, "kind", "") != "dice":
                self._update_shoot_popover_ui()
                return
            values = self._parse_popover_dice_values(req)
            if values is None:
                return
            self._submit_answer(values)
            self._shoot_resolver_step = 4
            self.shoot_popover_dice_input.clear()
        else:
            self._close_shoot_popover()
            return

        if self._shoot_resolver_active:
            self._update_shoot_popover_ui()

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
        self._movement_skip_sent = False
        if request is None:
            self._deploy_visual_reset_done = False
            self._deploy_context = None
            self._deploy_hover_cell = None
            self._deploy_status_text = ""
            self._clear_deploy_overlays()
            self.map_scene.clear_temporary_deploy_units()
            if self.controller.is_finished:
                self.command_prompt.setText("Игра завершена.")
            else:
                self.command_prompt.setText("Команда не требуется.")
            self.command_stack.setEnabled(False)
            self.command_stack.setVisible(True)
            self.command_hint.setText("Горячие клавиши: —")
            self.map_scene.set_target_cell(None)
            self._shoot_targets_valid = set()
            self._shoot_request_flow_active = False
            self._close_shoot_popover()
            self._refresh_active_context()
            return

        if self._is_deploy_request(request):
            meta = getattr(request, "meta", {}) or {}
            deploy_index = int(meta.get("deploy_index") or 0)
            if deploy_index <= 1 and not self._deploy_visual_reset_done:
                self._reset_viewer_session_visuals(reason="manual_deploy_start")
                self._deploy_visual_reset_done = True
        else:
            self._deploy_visual_reset_done = False
            self._clear_deploy_overlays()
            self.map_scene.clear_temporary_deploy_units()

        self._maybe_reset_target_for_request(request)
        if self._is_shooting_target_request(request):
            self._shoot_request_flow_active = True
            self._shoot_locked_target_id = None
            self._shoot_targets_valid = self._valid_target_ids_from_request(request)
            shooter_id = self._extract_unit_id(getattr(request, "prompt", ""))
            shooter_label = self._format_unit_label(shooter_id)
            targets_label = ", ".join(str(v) for v in sorted(self._shoot_targets_valid)) if self._shoot_targets_valid else "—"
            meta = getattr(request, "meta", {}) or {}
            filtered = list(meta.get("shoot_filtered") or []) if isinstance(meta, dict) else []
            filtered_chunks: list[str] = []
            for item in filtered:
                if not isinstance(item, dict):
                    continue
                target_id = item.get("target_id")
                reason = str(item.get("reason") or "").strip()
                if target_id is None or not reason:
                    continue
                try:
                    filtered_chunks.append(f"{int(target_id)}: {reason}")
                except (TypeError, ValueError):
                    continue
            filtered_label = "; ".join(filtered_chunks) if filtered_chunks else "—"
            self.add_log_line(
                f"REQ: валидные цели стрельбы для Unit {shooter_label}: [{targets_label}] | отфильтрованы: [{filtered_label}]"
            )
        elif self._is_shooting_dice_request(request):
            pass
        else:
            self._shoot_request_flow_active = False
            self._shoot_locked_target_id = None
            self._shoot_targets_valid = set()
        self._update_deploy_status_from_request(request)
        display_prompt = self._deploy_status_text if self._deploy_status_text else request.prompt
        self.command_prompt.setText(display_prompt)
        self.command_stack.setEnabled(True)
        self.command_stack.setVisible(True)
        kind = getattr(request, "kind", "text")
        if self._is_movement_move_request(request):
            self.command_prompt.setText(self._move_instruction_text())
            self.command_stack.setEnabled(False)
            self.command_stack.setVisible(False)
            self.command_hint.setText("Горячие клавиши: ПКМ — идти, Backspace — stay")
        elif self._is_shooting_target_request(request) or self._is_shooting_dice_request(request):
            self.command_prompt.setText(self._shoot_instruction_text())
            self.command_stack.setEnabled(False)
            self.command_stack.setVisible(False)
            self.command_hint.setText("Горячие клавиши: ПКМ — Fire, Enter — Shoot, Esc — отмена")
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
        elif kind == "deploy_coord":
            meta = getattr(request, "meta", {}) or {}
            if self._is_movement_move_request(request):
                self._deploy_context = dict(meta)
                self._refresh_deploy_preview()
                self._refresh_active_context()
                return
            x_min = meta.get("x_min", "?")
            x_max = meta.get("x_max", "?")
            y_min = meta.get("y_min", "?")
            y_max = meta.get("y_max", "?")
            self.command_input.setPlaceholderText(f"X Y (X={x_min}..{x_max}, Y={y_min}..{y_max})")
            self.command_stack.setCurrentIndex(self._command_pages["text"])
            self._deploy_context = dict(meta)
            current_side = self._deploy_context.get("deploy_side")
            current_unit_id = self._deploy_context.get("deploy_unit_id")
            if current_unit_id is not None:
                side_for_table = "player" if current_side == "enemy" else "model"
                self._set_selected_unit(side_for_table, int(current_unit_id), source="deploy", select_row=True)
            self._refresh_deploy_preview()
        else:
            self.command_input.setPlaceholderText("Введите команду...")
            self.command_stack.setCurrentIndex(self._command_pages["text"])
        self._update_command_hint(kind)
        self._refresh_active_context()
        if self._shoot_resolver_active and (self._is_shooting_target_request(request) or self._is_shooting_dice_request(request)):
            self._update_shoot_popover_ui()

    def _move_instruction_text(self) -> str:
        unit_id, side = self._resolve_active_unit()
        unit = self._units_by_key.get((side, unit_id)) if unit_id is not None else None
        unit_name = str(unit.get("name") or unit.get("unit_name") or "—") if isinstance(unit, dict) else "—"
        unit_label = str(unit_id) if unit_id is not None else "—"
        return (
            f"Ходьба: Unit {unit_label} — {unit_name}\n"
            "ЛКМ: выделить/hover клетку\n"
            "ПКМ: идти в клетку\n"
            "Backspace: stay (остаться на месте)\n"
            "Синий: обычный Move (до M)\n"
            "Жёлтый: Advance (до M+6)"
        )

    def _is_movement_move_request(self, request) -> bool:
        # В viewer move_request используется только для ручного Movement UX.
        # Не привязываемся к текущему state.phase (может запаздывать на один poll),
        # иначе иногда всплывает старый command stack с вводом координат.
        return self._is_move_cell_request(request)

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

    def _is_deploy_request(self, request) -> bool:
        if request is None:
            return False
        if str(getattr(request, "kind", "")).strip().lower() != "deploy_coord":
            return False
        meta = getattr(request, "meta", {}) or {}
        return not bool(meta.get("move_request"))

    def _is_move_cell_request(self, request) -> bool:
        if request is None:
            return False
        if str(getattr(request, "kind", "")).strip().lower() != "deploy_coord":
            return False
        meta = getattr(request, "meta", {}) or {}
        return bool(meta.get("move_request"))

    def _maybe_reset_target_for_request(self, request) -> None:
        if self._is_deploy_request(request):
            self._set_confirm_enabled(True)
            return
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
        if self._is_shooting_target_request(self._pending_request) and int(unit_id) not in self._shoot_targets_valid:
            allowed = ", ".join(str(v) for v in sorted(self._shoot_targets_valid)) if self._shoot_targets_valid else "—"
            self.add_log_line(
                f"REQ: цель Unit {int(unit_id)} отклонена. Где: viewer/app.py (_on_target_selected). Что дальше: выберите цель из [{allowed}]"
            )
            return
        self._current_target_id = unit_id
        self.map_scene.set_target_unit(unit_id)
        self._set_confirm_enabled(True)
        target_label = self._format_unit_label(unit_id)
        self.add_log_line(f"REQ: target selected Unit {target_label}")

    def _on_shoot_overlay_mode_changed(self, _mode: str) -> None:
        req = self._pending_request
        if self._is_shooting_target_request(req) or self._is_shooting_dice_request(req):
            self.command_prompt.setText(self._shoot_instruction_text())
            if getattr(self, "shoot_popover", None) and self.shoot_popover.isVisible():
                self._update_shoot_popover_ui()

    def _on_unit_right_clicked(self, side: str, unit_id: int, global_pos) -> None:
        req = self._pending_request
        if not (self._is_shooting_target_request(req) or self._is_shooting_dice_request(req)):
            return
        if side != "model":
            self._close_shoot_popover()
            return
        if int(unit_id) not in self._shoot_targets_valid:
            allowed = ", ".join(str(v) for v in sorted(self._shoot_targets_valid)) if self._shoot_targets_valid else "—"
            self.add_log_line(
                f"REQ: ПКМ по Unit {int(unit_id)} отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [{allowed}]"
            )
            self._close_shoot_popover()
            return
        self._open_shoot_popover(int(unit_id), global_pos)

    def _on_cell_clicked(self, x: int, y: int) -> None:
        if self._is_shooting_target_request(self._pending_request):
            self._close_shoot_popover()
        if self._is_movement_move_request(self._pending_request):
            self.map_scene.set_target_cell((x, y))
            return
        if not self._is_deploy_request(self._pending_request):
            return
        self.map_scene.set_target_cell((x, y))
        self.command_input.setText(f"{x} {y}")
        ok, reason, _ghost_cells = self._validate_deploy_cell(x, y)
        if ok:
            self.add_log_line(f"REQ: deploy cell accepted x={x}, y={y}")
            self._submit_answer({"x": x, "y": y})
        else:
            self.add_log_line(
                f"Ошибка деплоя: reason={reason}, x={x}, y={y}. Где: viewer/app.py (_on_cell_clicked). "
                "Что делать дальше: выберите клетку в зоне деплоя без коллизий."
            )

    def _on_cell_right_clicked(self, x: int, y: int) -> None:
        if not self._is_move_cell_request(self._pending_request):
            return
        self._submit_movement_target_cell(x, y, source="RMB")

    def _submit_movement_target_cell(self, x: int, y: int, *, source: str) -> bool:
        if not self._is_move_cell_request(self._pending_request):
            return False
        if not self.map_scene.is_reachable_cell(x, y):
            return False
        move_mode = "normal" if self.map_scene.is_move_cell(x, y) else "advance" if self.map_scene.is_advance_cell(x, y) else None
        if move_mode is None:
            return False
        self.map_scene.set_target_cell((x, y))
        self.command_input.setText(f"{x} {y}")
        self.add_log_line(f"REQ: move cell accepted ({source}) x={x}, y={y}, mode={move_mode}")
        self._submit_answer({"x": x, "y": y, "mode": move_mode})
        return True

    def _submit_skip_movement_for_active_unit(self) -> bool:
        if not self._is_move_cell_request(self._pending_request):
            return False
        if self._movement_skip_sent:
            return True
        req_meta = getattr(self._pending_request, "meta", {}) or {}
        req_unit_id = req_meta.get("unit_id")
        current_cell = None
        for candidate_side in ("player", "model"):
            try:
                key = (candidate_side, int(req_unit_id))
            except (TypeError, ValueError):
                continue
            unit = self._units_by_key.get(key)
            if not isinstance(unit, dict):
                continue
            try:
                current_cell = (int(unit.get("x")), int(unit.get("y")))
            except (TypeError, ValueError):
                current_cell = None
            if current_cell is not None:
                break

        self._movement_skip_sent = True
        unit_label = int(req_unit_id) if str(req_unit_id).isdigit() else "—"
        if current_cell is None:
            self.add_log_line(
                f"Unit {unit_label}: movement stay (координаты юнита в UI не найдены, передан mode=stay)."
            )
            self._submit_answer({"mode": "stay", "skip_movement": True})
        else:
            self.add_log_line(
                f"Unit {unit_label}: movement stay (позиция сохранена x={int(current_cell[0])}, y={int(current_cell[1])})."
            )
            self._submit_answer({"mode": "stay", "skip_movement": True, "x": int(current_cell[0]), "y": int(current_cell[1])})
        self.map_scene.set_target_cell(None)
        self.map_scene.clear_target_selection()
        return True

    def _on_cell_hovered(self, state_pos) -> None:
        if self._is_movement_move_request(self._pending_request):
            return
        if state_pos is None:
            self._deploy_hover_cell = None
        else:
            try:
                self._deploy_hover_cell = (int(state_pos[0]), int(state_pos[1]))
            except (TypeError, ValueError, IndexError):
                self._deploy_hover_cell = None
        self._refresh_deploy_preview()

    def _update_deploy_status_from_request(self, request) -> None:
        self._deploy_status_text = ""
        if not self._is_deploy_request(request):
            return
        meta = getattr(request, "meta", {}) or {}
        label = str(meta.get("deploy_unit_label") or "—")
        idx = int(meta.get("deploy_index") or 0)
        total = int(meta.get("deploy_total") or 0)
        remain = int(meta.get("deploy_remaining") or max(0, total - idx + 1))
        next_label = meta.get("deploy_next_label")
        line = f"Расставьте юнита: {label} [{idx}/{total}] • Осталось расставить: {remain}"
        if next_label:
            line += f" • Следом: {next_label} [{idx + 1}/{total}]"
        self._deploy_status_text = line

    def _refresh_deploy_preview(self) -> None:
        if not self._is_deploy_request(self._pending_request):
            self.map_scene.set_deploy_ghost([], None, "")
            return
        meta = self._deploy_context if isinstance(self._deploy_context, dict) else {}
        if self._deploy_hover_cell is None:
            self.map_scene.set_deploy_ghost([], None, "")
            return

        x, y = self._deploy_hover_cell
        ok, reason, ghost_cells = self._validate_deploy_cell(x, y)
        unit_name = str((self._deploy_context or {}).get("deploy_unit_name") or (self._deploy_context or {}).get("deploy_unit_label") or "")
        self.map_scene.set_deploy_ghost(ghost_cells, ok, unit_name)
        if not ok:
            self.command_hint.setText(f"Клик заблокирован: {reason}. Выберите валидную клетку.")

    def _validate_deploy_cell(self, x: int, y: int):
        offsets = [
            (int(pair[0]), int(pair[1]))
            for pair in ((self._deploy_context or {}).get("model_offsets") or [[0, 0]])
            if isinstance(pair, (list, tuple)) and len(pair) >= 2
        ]
        if not offsets:
            offsets = [(0, 0)]
        ghost_cells = [(x + dc, y + dr) for dr, dc in offsets]

        meta = self._deploy_context if isinstance(self._deploy_context, dict) else {}
        occupied = [tuple(pair) for pair in (meta.get("occupied") or []) if isinstance(pair, (list, tuple)) and len(pair) >= 2]
        occupied_model_cells = [tuple(pair) for pair in (meta.get("occupied_model_cells") or []) if isinstance(pair, (list, tuple)) and len(pair) >= 2]
        terrain_cells = [tuple(pair) for pair in (meta.get("terrain_cells") or []) if isinstance(pair, (list, tuple)) and len(pair) >= 2]
        zone_side = str(meta.get("deploy_zone_side") or "enemy")
        b_len = int(meta.get("deploy_b_len") or 40)
        b_hei = int(meta.get("deploy_b_hei") or 60)
        ok, reason = validate_deploy_coord(
            zone_side,
            (y, x),
            b_len,
            b_hei,
            occupied,
            model_offsets=offsets,
            occupied_model_cells=occupied_model_cells,
            terrain_cells=terrain_cells,
        )
        return ok, reason, ghost_cells

    def _extract_manual_deploy_cells(self, request_meta, submitted_value):
        meta = request_meta if isinstance(request_meta, dict) else {}
        if not isinstance(submitted_value, dict):
            return []
        try:
            anchor_x = int(submitted_value.get("x"))
            anchor_y = int(submitted_value.get("y"))
        except (TypeError, ValueError):
            return []
        offsets = [
            (int(pair[0]), int(pair[1]))
            for pair in (meta.get("model_offsets") or [[0, 0]])
            if isinstance(pair, (list, tuple)) and len(pair) >= 2
        ]
        if not offsets:
            offsets = [(0, 0)]
        return [(anchor_x + dc, anchor_y + dr) for dr, dc in offsets]

    def _resolve_deploy_facing(self, request_meta, placed_cells):
        meta = request_meta if isinstance(request_meta, dict) else {}
        zone_side = str(meta.get("deploy_zone_side") or "").strip().lower()
        if zone_side == "model":
            return "right"
        if zone_side == "enemy":
            return "left"
        if placed_cells:
            board_w = int(meta.get("deploy_b_hei") or 60)
            anchor_x = int(placed_cells[0][0])
            return "right" if anchor_x < (board_w / 2.0) else "left"
        return "right"

    def _update_command_hint(self, kind):
        if kind == "direction":
            self.command_hint.setText("Горячие клавиши: ↑ ↓ ← →, пробел/0 — нет")
        elif kind == "bool":
            self.command_hint.setText("Горячие клавиши: Y — да, N — нет")
        elif kind == "int":
            self.command_hint.setText("Горячие клавиши: Enter — отправить")
        elif kind == "choice":
            if self._is_shooting_target_request(self._pending_request):
                self.command_hint.setText("ПКМ по валидной цели откроет Fire popover")
            else:
                self.command_hint.setText("Горячие клавиши: Enter — выбрать")
        elif kind == "deploy_coord":
            if self._is_movement_move_request(self._pending_request):
                self.command_hint.setText("ПКМ по подсвеченной клетке. ЛКМ — hover/выбор, Backspace — stay")
            elif self._is_move_cell_request(self._pending_request):
                self.command_hint.setText("RMB по подсвеченной клетке или введите X Y, затем Enter")
            else:
                self.command_hint.setText("Кликните клетку на поле или введите X Y, затем Enter")
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
        self._reset_viewer_session_visuals(reason="new_game_start")
        messages, request = self.controller.start()
        self._append_log(messages)
        self._set_request(request)
        self._poll_state()

    def _reset_viewer_session_visuals(self, reason: str) -> None:
        self.add_log_line(
            f"[VIEWER][RESET] reason={reason}. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии."
        )
        self.map_scene.reset_runtime_visuals(clear_units=True, clear_state=False)
        self._units_by_key = {}
        self._unit_row_by_key = {}
        self._fx_shot_queue.clear()
        self._fx_parser.reset(preserve_seen=False)
        self._current_target_id = None
        self._last_shooter_id = None
        self._shoot_targets_valid: set[int] = set()
        self._shoot_request_flow_active = False
        self._shoot_popover_target_id: Optional[int] = None
        self._shoot_resolver_active = False
        self._shoot_resolver_step = 0
        self._shoot_resolver_attacker_id: Optional[int] = None
        self._shoot_locked_target_id: Optional[int] = None
        self._active_weapon_name = None
        self._active_weapon_range = None
        self._active_weapon_unit_id = None
        self._deploy_context = None
        self._deploy_hover_cell = None
        self._deploy_status_text = ""
        self._rolloff_attacker_side = None
        self._rolloff_defender_side = None

    def _submit_text(self):
        text = self.command_input.text().strip()
        if self._is_movement_move_request(self._pending_request):
            self.add_log_line("Ходьба: ввод с клавиатуры отключён. Что делать дальше: используйте ПКМ по подсвеченной клетке.")
            return
        if self._is_shooting_target_request(self._pending_request):
            self.add_log_line("Стрельба: выбор цели делается ПКМ по врагу (Fire popover).")
            return
        if self._is_deploy_request(self._pending_request) or self._is_move_cell_request(self._pending_request):
            parts = [p for p in re.split(r"[\s,;:]+", text) if p]
            if len(parts) != 2:
                self.add_log_line(
                    "Ошибка деплоя: нужно ввести X и Y. Где: viewer/app.py (_submit_text). "
                    "Что делать дальше: кликните клетку на поле или введите два числа."
                )
                return
            try:
                x = int(parts[0])
                y = int(parts[1])
            except ValueError:
                self.add_log_line(
                    "Ошибка деплоя: X/Y должны быть целыми. Где: viewer/app.py (_submit_text). "
                    "Что делать дальше: введите целые координаты."
                )
                return
            self.map_scene.set_target_cell((x, y))
            if self._is_move_cell_request(self._pending_request):
                if not self.map_scene.is_reachable_cell(x, y):
                    self.add_log_line(
                        f"Ошибка движения: клетка недостижима x={x}, y={y}. Где: viewer/app.py (_submit_text). "
                        "Что делать дальше: выберите подсвеченную reachable-клетку."
                    )
                    return
            else:
                ok, reason, _ghost = self._validate_deploy_cell(x, y)
                if not ok:
                    self.add_log_line(
                        f"Ошибка деплоя: reason={reason}, x={x}, y={y}. Где: viewer/app.py (_submit_text). "
                        "Что делать дальше: выберите валидную клетку деплоя."
                    )
                    return
            self._submit_answer({"x": x, "y": y})
            return
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
        if self._is_shooting_target_request(self._pending_request):
            target_id = self._extract_unit_id(value)
            if target_id is None:
                return
            self._open_shoot_popover(int(target_id))
            return
        if self._is_target_request(self._pending_request) and self._current_target_id is None:
            self._sync_target_from_choice(value)
            if self._current_target_id is None:
                return
        self._submit_answer(value)

    def _submit_answer(self, value):
        if self._pending_request is None:
            return
        finished_request = self._pending_request
        finished_meta = getattr(finished_request, "meta", {}) or {}
        if self._is_deploy_request(finished_request):
            placed_cells = self._extract_manual_deploy_cells(finished_meta, value)
            deploy_side = str(finished_meta.get("deploy_side") or "enemy")
            unit_side = "player" if deploy_side == "enemy" else "model"
            unit_id = finished_meta.get("deploy_unit_id")
            unit_name = str(finished_meta.get("deploy_unit_name") or finished_meta.get("deploy_unit_label") or "")
            if placed_cells and unit_id is not None:
                try:
                    self.map_scene.add_temporary_deploy_unit(
                        unit_side=unit_side,
                        unit_id=int(unit_id),
                        unit_name=unit_name,
                        model_cells=placed_cells,
                        facing=self._resolve_deploy_facing(finished_meta, placed_cells),
                    )
                    self.map_scene.trigger_deploy_snap_flash(placed_cells, duration_s=0.22)
                except (TypeError, ValueError):
                    pass
            # Placement confirmed: remove preview/marker immediately.
            self._clear_deploy_overlays()
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

    def _clear_deploy_overlays(self) -> None:
        self._deploy_context = None
        self._deploy_hover_cell = None
        self.map_scene.set_deploy_ghost([], None, "")
        self.map_scene.clear_target_selection()

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

        def _side_label(raw):
            side = str(raw or "").strip().lower()
            if side == "model":
                return "Модель"
            if side in {"enemy", "player"}:
                return "Игрок"
            return None

        attacker_label = _side_label(attacker)
        defender_label = _side_label(defender)
        deploy_phase_text = str(state.get("phase") or "").strip().lower()
        deploy_active = ("deploy" in deploy_phase_text) or ("расст" in deploy_phase_text)
        rolloff_done = bool(attacker_label and defender_label)
        if not rolloff_done and not deploy_active:
            # Fallback: используем последнее корректное значение roll-off из логов Viewer.
            attacker_fallback = _side_label(self._rolloff_attacker_side)
            defender_fallback = _side_label(self._rolloff_defender_side)
            if attacker_fallback and defender_fallback:
                attacker_label = attacker_fallback
                defender_label = defender_fallback
                rolloff_done = True
        if deploy_active:
            if not rolloff_done:
                deploy_text = "Деплой: ожидание roll-off"
            else:
                deploy_text = f"Деплой: расстановка (Attacker={attacker_label} • Defender={defender_label})"
        else:
            if not rolloff_done:
                deploy_text = "Деплой: ожидание roll-off"
            else:
                deploy_text = f"Деплой завершён: Attacker = {attacker_label} • Defender = {defender_label}"
        self.status_deployment.setText(deploy_text)
        if self._deploy_status_text:
            self.status_deployment.setText(f"{self.status_deployment.text()} • {self._deploy_status_text}")
        if os.getenv("VIEWER_DEBUG", "0") == "1":
            self.add_log_line(
                f"[STATUS] phase={state.get('phase')} deploy_state={'active' if deploy_active else 'completed'} "
                f"attacker={attacker} defender={defender} text=\"{self.status_deployment.text()}\""
            )

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
        if not (self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(self._pending_request)):
            self._close_shoot_popover()
        elif self._shoot_popover_target_id is not None and int(self._shoot_popover_target_id) not in self._shoot_targets_valid:
            self._close_shoot_popover()

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

    def _capture_rolloff_sides_from_log(self, raw_text: str) -> None:
        text = str(raw_text or "")
        if "roll-off attacker/defender" not in text.lower():
            return
        match = re.search(r"attacker\s*=\s*(model|enemy|player)", text, re.IGNORECASE)
        if not match:
            return
        attacker = str(match.group(1) or "").strip().lower()
        if attacker not in {"model", "enemy", "player"}:
            return
        defender = "model" if attacker in {"enemy", "player"} else "enemy"
        self._rolloff_attacker_side = attacker
        self._rolloff_defender_side = defender

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
        self._capture_rolloff_sides_from_log(raw_text)
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
                self._capture_rolloff_sides_from_log(raw_text)
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
        rotated = os.path.join(ROOT_DIR, "LOGS_FOR_AGENTS_PLAY.old.md")
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

    def _resolve_weapon_name_and_range(self, unit) -> tuple[str, Optional[int]]:
        if not unit:
            return "—", None

        name = str(unit.get("weapon_name") or unit.get("weapon") or "—")

        status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
        for key in ("selected_weapon_range", "weapon_range", "shoot_range", "shooting_range"):
            value = status.get(key)
            if isinstance(value, (int, float)):
                return name, int(value)

        for key in ("range", "weapon_range", "shoot_range", "shooting_range"):
            value = unit.get(key)
            if isinstance(value, (int, float)):
                return name, int(value)

        weapons = unit.get("weapons")
        if isinstance(weapons, list):
            ranged = []
            for item in weapons:
                if not isinstance(item, dict):
                    continue
                rng = item.get("range") or item.get("Range") or item.get("shoot_range")
                if not isinstance(rng, (int, float)):
                    continue
                rng_i = int(rng)
                if rng_i <= 0:
                    continue
                ranged.append((str(item.get("name") or item.get("Name") or name), rng_i))
            if ranged:
                best_name, best_rng = max(ranged, key=lambda it: it[1])
                return best_name, best_rng

        return name, None

    def _remember_active_weapon(self, unit_id: Optional[int], weapon_name: Optional[str], weapon_range: Optional[int]) -> None:
        self._active_weapon_unit_id = int(unit_id) if isinstance(unit_id, (int, float)) else None
        self._active_weapon_name = str(weapon_name).strip() if weapon_name else None
        self._active_weapon_range = int(weapon_range) if isinstance(weapon_range, (int, float)) else None

    def _resolve_active_weapon(self, unit) -> tuple[str, Optional[int]]:
        weapon, weapon_range = self._resolve_weapon_name_and_range(unit)
        unit_id = int(unit.get("id")) if isinstance(unit, dict) and str(unit.get("id")).isdigit() else None
        if (
            unit_id is not None
            and isinstance(self._active_weapon_unit_id, int)
            and int(self._active_weapon_unit_id) == int(unit_id)
            and isinstance(self._active_weapon_range, int)
            and self._active_weapon_range > 0
        ):
            remembered_name = self._active_weapon_name or weapon
            return remembered_name, int(self._active_weapon_range)
        return weapon, weapon_range

    def _resolve_weapon_range(self, unit):
        _name, rng = self._resolve_weapon_name_and_range(unit)
        return rng

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
        if unit_id is None:
            unit_id = self._shoot_resolver_attacker_id or self._last_shooter_id or self._selected_unit_id
            if unit_id is not None:
                side = self._side_from_unit_id(int(unit_id)) or self._selected_unit_side

        self._active_unit_id = unit_id
        self._active_unit_side = side
        if self._selected_unit_id is None and unit_id is not None:
            self._set_selected_unit(side, unit_id, source="auto", select_row=True)

        active_unit = self._units_by_key.get((side, unit_id)) if unit_id is not None and side is not None else None
        phase = None
        if self.state_watcher and self.state_watcher.state:
            phase = self.state_watcher.state.get("phase")

        req = self._pending_request
        phase_for_overlay = phase
        if self._is_movement_move_request(req):
            phase_for_overlay = "movement"
        elif self._is_shooting_target_request(req) or self._is_shooting_dice_request(req):
            phase_for_overlay = "shooting"

        move_range = None
        shoot_range = None
        if self._is_movement_phase(phase_for_overlay):
            move_range = self._resolve_move_range(active_unit)
        if self._is_shooting_phase(phase_for_overlay):
            weapon_name, shoot_range = self._resolve_active_weapon(active_unit)
            self._remember_active_weapon(unit_id, weapon_name, shoot_range)

        targets_ctx = None
        if self.state_watcher and self.state_watcher.state:
            targets_ctx = self.state_watcher.state.get("available_targets")
        if (self._is_shooting_target_request(req) or self._is_shooting_dice_request(req)) and self._shoot_targets_valid:
            targets_ctx = sorted(self._shoot_targets_valid)

        self.map_scene.set_active_context(
            active_unit_id=unit_id,
            active_unit_side=side,
            selected_unit_id=self._selected_unit_id,
            selected_unit_side=self._selected_unit_side,
            phase=phase_for_overlay,
            move_range=move_range,
            shoot_range=shoot_range,
            show_objective_radius=self._show_objective_radius,
            targets=targets_ctx,
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
            if event.isAutoRepeat():
                return True
            kind = getattr(self._pending_request, "kind", "")
            key = event.key()
            text = event.text().lower()
            if self._is_movement_move_request(self._pending_request) and key == QtCore.Qt.Key_Escape:
                self.map_scene.set_target_cell(None)
                return True
            if self._is_movement_move_request(self._pending_request) and key == QtCore.Qt.Key_Backspace:
                if self._submit_skip_movement_for_active_unit():
                    return True
                return True
            if self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(self._pending_request):
                if key == QtCore.Qt.Key_Escape:
                    self._close_shoot_popover()
                    self.map_scene.clear_target_selection()
                    self._current_target_id = None
                    return True
                if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter) and getattr(self, "shoot_popover", None) and self.shoot_popover.isVisible():
                    self._shoot_step_action()
                    return True
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
