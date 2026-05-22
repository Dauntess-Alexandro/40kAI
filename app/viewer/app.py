import torch
import json
import html
import os
import queue
import re
import sys
import time
from collections import OrderedDict, deque
from dataclasses import dataclass
from typing import Callable, Deque, Optional, Tuple, Dict
from datetime import datetime

# Qt Quick выбирает RHI до создания QApplication. На Windows по умолчанию это D3D11 и он несовместим
# с композицией QOpenGLWidget → чёрное поле доски и спам в консоли. OpenGL‑бэкенд RHI совпадает с GL‑виджетом.
_qsg_override = os.environ.get("VIEWER_QSG_RHI_BACKEND", "").strip()
if _qsg_override:
    os.environ["QSG_RHI_BACKEND"] = _qsg_override
elif sys.platform == "win32":
    os.environ.setdefault("QSG_RHI_BACKEND", "opengl")

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QFileSystemWatcher, QStringListModel, QUrl
from PySide6.QtQml import QQmlEngine
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget
from project_paths import AGENT_PLAY_LOG_PATH, APP_DIR, CORE_DIR, PROJECT_ROOT, ensure_runtime_dirs

# Qt 6 renamed this; PySide6 6.5+ exposes ResizeMode.SizeRootObjectToView.
try:
    _QQUICK_RESIZE_ROOT_TO_VIEW = QQuickWidget.ResizeMode.SizeRootObjectToView
except AttributeError:
    _QQUICK_RESIZE_ROOT_TO_VIEW = QQuickWidget.SizeRootObjectToViewSize

ROOT_DIR = str(PROJECT_ROOT)
GYM_PATH = str(CORE_DIR)
if GYM_PATH not in sys.path:
    sys.path.insert(0, GYM_PATH)

from app.viewer.config import load_viewer_config, viewer_flag

from app.viewer.controller.viewer_controller import (
    ViewerController,
    ViewerPresentationContext,
    compute_status_labels,
)
from app.viewer.opengl_view import OpenGLBoardWidget
from app.viewer.ui.dialog_bridge import ViewerDialogBridge
from app.viewer.ui.log_model import ViewerLogListModel, classify_log_kind, extract_log_timestamp
from app.viewer.ui.units_model import ViewerUnitsListModel
from app.viewer.gun_fx import get_gun_fx_config, resolve_fx_profile
from app.viewer.state import StateWatcher
from app.viewer.styles import Theme

from core.engine.game_controller import GameController
from core.engine.game_io import DICE_CANCEL_TOKEN, dice_values_from_user_text, parse_dice_values
from core.engine.event_bus import get_event_bus
from core.engine.mission import validate_deploy_coord


@dataclass
class PendingReport:
    ts: str
    report_type: str
    attacker_id: Optional[int] = None
    target_id: Optional[int] = None
    weapon_name: Optional[str] = None
    damage: Optional[float] = None
    failed_saves: Optional[int] = None
    has_save_rolls: bool = False


@dataclass
class FxShotEvent:
    ts: str
    report_type: str
    attacker_id: int
    target_id: int
    weapon_name: str
    damage: float
    outcome_type: str
    failed_saves: Optional[int] = None
    hp_before: Optional[float] = None
    hp_after: Optional[float] = None
    hp_max: Optional[float] = None
    popup_key: str = ""


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
        heal_match = re.search(
            r"\[HEAL\]\s*Unit\s+(\d+)\s*•\s*([^:]+):\s*\+([\d.]+)\s*HP",
            text,
            re.IGNORECASE,
        )
        if heal_match:
            self._finalize_heal_report(ts, heal_match)
            return
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
        save_match = re.search(r"Save rolls:.*failed saves:\s*(\d+)", text, re.IGNORECASE)
        if save_match:
            current.failed_saves = int(save_match.group(1))
            current.has_save_rolls = True
            self._debug(f"FX: найден failed saves = {current.failed_saves}.")
            return
        if re.search(r"Save rolls:", text, re.IGNORECASE):
            current.has_save_rolls = True

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
        outcome_type = "damage"
        if damage <= 0:
            if report.has_save_rolls and report.failed_saves == 0:
                outcome_type = "save"
            else:
                outcome_type = "miss"
        event = FxShotEvent(
            ts=report.ts,
            report_type=report.report_type,
            attacker_id=report.attacker_id,
            target_id=report.target_id,
            weapon_name=report.weapon_name,
            damage=damage,
            outcome_type=outcome_type,
            failed_saves=report.failed_saves,
        )
        key = (
            event.ts,
            event.report_type,
            event.attacker_id,
            event.target_id,
            event.weapon_name,
            event.damage,
            event.outcome_type,
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
            f"weapon={event.weapon_name}, damage={event.damage}, outcome={event.outcome_type})."
        )
        self._on_event(event)
        self._pending.pop()

    def _finalize_heal_report(self, ts: str, heal_match: re.Match) -> None:
        unit_id = int(heal_match.group(1))
        ability = str(heal_match.group(2)).strip()
        amount = float(heal_match.group(3))
        key = (ts, "heal", unit_id, ability, round(amount, 4))
        if key in self._seen:
            self._debug("FX: дубликат [HEAL], pop-up пропущен.")
            return
        self._seen[key] = None
        if len(self._seen) > self._seen_max:
            self._seen.popitem(last=False)
        event = FxShotEvent(
            ts=ts,
            report_type="heal",
            attacker_id=unit_id,
            target_id=unit_id,
            weapon_name=ability or "Heal",
            damage=max(0.0, amount),
            outcome_type="heal",
        )
        self._debug(
            f"FX: [HEAL] Unit {unit_id} • {ability}: +{amount} HP → FxShotEvent (report_type=heal)."
        )
        self._on_event(event)


class HoverLogListWidget(QtWidgets.QListWidget):
    """List widget with explicit hover/leave signals for transient map previews."""

    itemHovered = QtCore.Signal(object)
    hoverLeft = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_hover_row = -1
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        item = self.itemAt(event.pos())
        if item is None:
            if self._last_hover_row != -1:
                self._last_hover_row = -1
                self.hoverLeft.emit()
            return
        row = self.row(item)
        if row == self._last_hover_row:
            return
        self._last_hover_row = row
        self.itemHovered.emit(item)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        super().leaveEvent(event)
        if self._last_hover_row != -1:
            self._last_hover_row = -1
            self.hoverLeft.emit()


class ViewerWindow(QtWidgets.QMainWindow):
    def __init__(self, state_path, model_path=None):
        super().__init__()
        self.state_path = state_path
        self.setWindowTitle("40kAI Viewer")
        self.resize(2560, 1440)

        self.controller = GameController(model_path=model_path, state_path=state_path)
        os.environ.setdefault("DEPLOYMENT_MODE", "manual_player")
        # GUI может подсказать, за кого играет человек и за кого ИИ (P1/P2 + фракция).
        # Если переменные не заданы — используем старые подписи.
        self._viewer_player_role_label = os.getenv("VIEWER_PLAYER_ROLE_LABEL", "Игрок")
        self._viewer_model_role_label = os.getenv("VIEWER_MODEL_ROLE_LABEL", "Модель")
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
        self._shoot_request_target_id: Optional[int] = None
        self._shoot_ui_stage: str = "target"
        self._last_shoot_stage_debug_sig: Optional[tuple] = None
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
        # При старте можем прочитать state.json от прошлой сессии.
        # Чтобы не мигали старые юниты, скрываем их до первого запроса текущего матча.
        self._hide_stale_units_on_bootstrap = True

        self._viewer_config = load_viewer_config()
        Theme.apply_from_config(self._viewer_config)
        self._controller_v1 = viewer_flag("viewer.controller.v1", self._viewer_config)
        self._qml_panels = viewer_flag("viewer.ui.qml_panels", self._viewer_config)
        self._qml_quick_widget = None
        self._qml_command_payloads = []
        self._qml_command_label_model = None
        self._qml_fs_watcher = None
        self._qml_reload_timer = None
        self._qml_log_model = None
        self._viewer_units_model = None
        self._command_prompt_text = "Ожидаю команду..."
        self._command_hint_text = "Горячие клавиши: —"
        self._shoot_dice_input_text = ""
        self._choice_options: list = []
        self._int_spin_min = 0
        self._int_spin_max = 999
        self._int_spin_value = 0
        self._last_command_text = ""
        self._last_choice_text = ""
        self.viewer_controller = ViewerController(parent=self)
        self.viewer_controller.attach_window(self)
        self.viewer_controller.set_role_labels(
            self._viewer_player_role_label,
            self._viewer_model_role_label,
        )
        self.viewer_dialogs = ViewerDialogBridge(self)
        self._pending_confirm_action: Optional[str] = None
        self.viewer_dialogs.confirmAccepted.connect(self._on_viewer_confirm_accepted)
        self._retain_qml_context_objects()
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
        self.map_scene.set_move_animation_config(self._viewer_config)
        self._apply_viewer_fx_quality()
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

        self._log_entries = []
        self._current_turn_number = None
        self._current_turn_side = None
        self._log_tail_snapshot = None
        self._model_events_snapshot = None
        self._model_event_queue: queue.Queue = queue.Queue()
        self._model_log_source = None
        self._model_events_stream = []
        self._model_events_current = []
        self._log_view = None
        self._visible_log_entries: list[dict] = []
        self._log_filter_buttons = {}
        self._log_status_label = None
        self._fx_shot_queue: Deque[FxShotEvent] = deque()
        self._fx_parser = FxLogParser(self._enqueue_fx_event, self._fx_debug, seen_max=400)
        self._model_shot_target_flash_gen = 0
        self._hp_snapshot_by_unit: Dict[Tuple[str, int], Tuple[Optional[float], Optional[float]]] = {}
        self._popup_seen: OrderedDict[str, float] = OrderedDict()
        self._popup_seen_ttl_s = 3.0
        self._popup_seen_max = 1500
        self._max_log_lines = 5000
        ensure_runtime_dirs()
        self._log_file_path = str(AGENT_PLAY_LOG_PATH)
        os.makedirs(os.path.dirname(self._log_file_path), exist_ok=True)
        self._log_file_max_bytes = 5 * 1024 * 1024
        self._last_active_side = None
        self._init_log_viewer()
        self.add_log_line("[VIEWER] Рендер: OpenGL (QOpenGLWidget).")
        self.add_log_line("[VIEWER] Фоллбэк-рендер не активирован.")
        if self._controller_v1:
            self.add_log_line("[VIEWER] Режим controller.v1: статус через ViewerController.")
        if viewer_flag("viewer.fx.v2", self._viewer_config):
            self.add_log_line("[VIEWER] FX v2 включён (viewer.fx.v2), качество эффектов: high.")
        if self._qml_panels:
            self.add_log_line("[VIEWER] UI: QML RightPanel (viewer.ui.qml_panels).")
        try:
            get_event_bus().subscribe(self._on_event_bus_event)
        except Exception:
            pass

        left_widget = QtWidgets.QWidget()
        left_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        left_layout.addWidget(self.map_scene, 1)

        self._right_panel_host = QtWidgets.QWidget()
        self._right_panel_host.setMinimumWidth(360)
        right_panel_layout = QtWidgets.QVBoxLayout(self._right_panel_host)
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        if self._qml_panels:
            try:
                self._qml_quick_widget = self._create_qml_side_panel_widget()
                right_panel_layout.addWidget(self._qml_quick_widget)
                self._maybe_install_qml_hot_reload(self._qml_quick_widget)
            except Exception as exc:
                self._qml_panels = False
                err = QtWidgets.QLabel(f"QML недоступен: {exc}")
                err.setWordWrap(True)
                right_panel_layout.addWidget(err)
                self.add_log_line(f"[VIEWER] QML панели недоступны ({exc}).")
        else:
            err = QtWidgets.QLabel("QML отключён (viewer.ui.qml_panels=false)")
            right_panel_layout.addWidget(err)

        self._top_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self._top_splitter.addWidget(left_widget)
        self._top_splitter.addWidget(self._right_panel_host)
        self._top_splitter.setStretchFactor(0, 1)
        self._top_splitter.setStretchFactor(1, 0)
        self._top_splitter.setChildrenCollapsible(False)

        central = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_layout.addWidget(self._top_splitter)
        self.setCentralWidget(central)

        self._apply_dark_theme()
        self._build_toolbar()
        self.viewer_controller.load_ui_settings()
        QtCore.QTimer.singleShot(0, self._apply_initial_splitter_sizes)
        QtCore.QTimer.singleShot(0, lambda: self._apply_map_only_mode(False))
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
        fit_action = QtGui.QAction("Fit", self)
        fit_action.triggered.connect(self._fit_view)
        toolbar.addAction(fit_action)
        toolbar.addSeparator()
        view_menu = self.menuBar().addMenu("Вид")
        view_menu.addAction(fit_action)
        scale_menu = view_menu.addMenu("Масштаб")
        self._ui_scale_group = QtGui.QActionGroup(self)
        for pct, scale in (("100%", 1.0), ("125%", 1.25), ("150%", 1.5)):
            act = QtGui.QAction(pct, self, checkable=True)
            act.setData(scale)
            self._ui_scale_group.addAction(act)
            scale_menu.addAction(act)
            act.triggered.connect(lambda checked=False, s=scale: self._set_ui_scale(s) if checked else None)
        self._ui_scale_actions = {1.0: None, 1.25: None, 1.5: None}
        for act in self._ui_scale_group.actions():
            self._ui_scale_actions[float(act.data())] = act
        self._load_ui_scale_settings()
        self._set_objective_radius_visible(True)

    def _set_objective_radius_visible(self, visible: bool) -> None:
        self._show_objective_radius = bool(visible)
        self.map_scene.set_objective_radius_visible(self._show_objective_radius)
        self.map_scene.refresh_overlays()

    def _apply_viewer_fx_quality(self) -> None:
        """Визуальные эффекты всегда на максимальном качестве (настройка убрана из UI)."""
        self.viewer_controller.set_fx_quality_high()
        self.map_scene.set_fx_quality("high")

    def _set_ui_scale(self, scale: float, *, persist: bool = True) -> None:
        Theme.set_ui_scale(scale)
        Theme._ui_font_size = Theme.scaled_ui_font_size()
        Theme._header_font_size = Theme.scaled_header_font_size()
        Theme._mono_font_size = Theme.scaled_mono_font_size()
        if persist:
            QtCore.QSettings("40kAI", "Viewer").setValue("uiScale", float(scale))
        actions = getattr(self, "_ui_scale_actions", None)
        if isinstance(actions, dict):
            for s, act in actions.items():
                if act is not None:
                    act.setChecked(abs(float(s) - float(scale)) < 0.01)
        qw = getattr(self, "_qml_quick_widget", None)
        if qw is not None:
            self._bind_viewer_main_qml_context(qw)

    def _load_ui_scale_settings(self) -> None:
        settings = QtCore.QSettings("40kAI", "Viewer")
        if not settings.contains("uiScale"):
            default = 1.5
        else:
            try:
                default = float(settings.value("uiScale", 1.0))
            except (TypeError, ValueError):
                default = 1.0
        self._set_ui_scale(default, persist=False)

    def _on_viewer_confirm_accepted(self) -> None:
        if self._pending_confirm_action == "log_clear":
            self._clear_log_viewer()
        self._pending_confirm_action = None

    def _apply_dark_theme(self):
        Theme.apply_from_config(self._viewer_config)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, Theme.background)
        palette.setColor(QtGui.QPalette.Base, Theme.panel)
        palette.setColor(QtGui.QPalette.AlternateBase, Theme.panel_alt)
        palette.setColor(QtGui.QPalette.Text, Theme.text)
        palette.setColor(QtGui.QPalette.WindowText, Theme.text)
        palette.setColor(QtGui.QPalette.Button, Theme.panel_alt)
        palette.setColor(QtGui.QPalette.ButtonText, Theme.text)
        palette.setColor(QtGui.QPalette.Highlight, Theme.highlight)
        palette.setColor(QtGui.QPalette.HighlightedText, Theme.text)
        palette.setColor(QtGui.QPalette.PlaceholderText, Theme.muted)
        self.setPalette(palette)
        self.setStyleSheet(Theme.stylesheet())
        if Theme.is_v2(self._viewer_config):
            self.add_log_line("[VIEWER] Тема: tokens v2 (theme/tokens.json).")

    def _controller_resolve_select_unit(self, unit_id: int) -> None:
        for (side, uid), _unit in list(self._units_by_key.items()):
            if uid == unit_id:
                self._select_row_for_unit(side, unit_id)
                return

    def _controller_submit_choice(self, token: str) -> None:
        self._submit_answer(str(token))

    def _controller_cancel_pending(self) -> None:
        pass

    def _unit_icon_path_for_qml(self, unit_name: str) -> str:
        pix = self.map_scene._icon_for_unit_name(str(unit_name or ""))
        if pix is None or pix.isNull():
            return ""
        cache_dir = APP_DIR / "gui_qt" / ".icon_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^a-zA-Z0-9_]+", "_", str(unit_name or "unit")).strip("_") or "unit"
        path = cache_dir / f"{safe}_28.png"
        if not path.is_file():
            pix.scaled(28, 28, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation).save(str(path))
        return str(path.resolve()).replace("\\", "/")

    def _apply_map_only_mode(self, enabled: Optional[bool] = None) -> None:
        host = getattr(self, "_right_panel_host", None)
        if host is not None:
            host.setVisible(not bool(enabled))

    def _apply_side_highlights(self) -> None:
        vc = self.viewer_controller
        sides = []
        if vc.sideHighlightPlayer:
            sides.append("player")
        if vc.sideHighlightModel:
            sides.append("model")
        fn = getattr(self.map_scene, "set_highlighted_sides", None)
        if callable(fn):
            fn(sides)

    def _center_camera_on_unit(self, unit_id: int) -> None:
        for (side, uid), unit in list(self._units_by_key.items()):
            if int(uid) == int(unit_id):
                self._set_selected_unit(side, unit_id, source="list", select_row=True)
                fn = getattr(self.map_scene, "center_on_unit", None)
                if callable(fn):
                    fn(side, unit_id)
                return

    def _preview_unit_on_map(self, unit_id: int) -> None:
        for (side, uid), _ in list(self._units_by_key.items()):
            if int(uid) == int(unit_id):
                fn = getattr(self.map_scene, "highlight_unit_preview", None)
                if callable(fn):
                    fn(side, unit_id)
                return

    def _retain_qml_context_objects(self) -> None:
        """Keep bridge QObjects owned by C++ so QML never sees null context props."""
        QQmlEngine.setObjectOwnership(self.viewer_controller, QQmlEngine.CppOwnership)
        QQmlEngine.setObjectOwnership(self.viewer_dialogs, QQmlEngine.CppOwnership)

    def _bind_viewer_main_qml_context(self, qw: QQuickWidget) -> None:
        self._retain_qml_context_objects()
        if self._viewer_units_model is None:
            self._viewer_units_model = ViewerUnitsListModel(self)
            self._viewer_units_model.set_icon_resolver(self._unit_icon_path_for_qml)
        if self._qml_log_model is None:
            self._qml_log_model = ViewerLogListModel(self)
        if self._qml_command_label_model is None:
            self._qml_command_label_model = QStringListModel(self)
        ctx = qw.rootContext()
        ctx.setContextProperty("viewerController", self.viewer_controller)
        ctx.setContextProperty("viewerDialogs", self.viewer_dialogs)
        ctx.setContextProperty("commandLabelModel", self._qml_command_label_model)
        ctx.setContextProperty("viewerUnitsModel", self._viewer_units_model)
        ctx.setContextProperty("viewerLogModel", self._qml_log_model)
        ctx.setContextProperty("bgSurfaceColor", Theme.panel.name())
        ctx.setContextProperty("bgElevatedColor", Theme.panel_alt.name())
        ctx.setContextProperty("borderMutedColor", Theme.accent_dark.name())
        ctx.setContextProperty("textPrimaryColor", Theme.text.name())
        ctx.setContextProperty("textSecondaryColor", Theme.muted.name())
        ctx.setContextProperty("accentColor", Theme.accent.name())
        ctx.setContextProperty("accentPrimaryColor", Theme.accent.name())
        scale = Theme.ui_scale()
        body = Theme.scaled_ui_font_size()
        mono = Theme.scaled_mono_font_size()
        ctx.setContextProperty("bodyFontSize", body)
        ctx.setContextProperty("monoFontSize", mono)
        ctx.setContextProperty("fontXs", max(8, round(body * 0.82)))
        ctx.setContextProperty("fontSm", max(9, round(body * 0.91)))
        ctx.setContextProperty("fontMd", body)
        ctx.setContextProperty("fontLg", max(body + 1, round(body * 1.18)))
        ctx.setContextProperty("selectionColor", Theme.selection.name())
        ctx.setContextProperty("playerColor", Theme.player.name())
        ctx.setContextProperty("modelColor", Theme.model.name())
        ctx.setContextProperty("objectiveColor", Theme.objective.name())
        ctx.setContextProperty("legendPlayer", self._viewer_player_role_label)
        ctx.setContextProperty("legendModel", self._viewer_model_role_label)
        ctx.setContextProperty("headerFontFamily", Theme._header_font_family)
        ctx.setContextProperty("headerFontSize", Theme.scaled_header_font_size())
        ctx.setContextProperty("monoFontFamily", Theme._mono_font_family)
        ctx.setContextProperty("radiusSm", Theme.radius_sm)
        ctx.setContextProperty("radiusMd", Theme.radius_md)
        ctx.setContextProperty("radiusBtn", Theme.radius_btn)
        ctx.setContextProperty("spacingXs", Theme.spacing_xs)
        ctx.setContextProperty("spacingSm", Theme.spacing_sm)
        ctx.setContextProperty("spacingMd", Theme.spacing_md)
        ctx.setContextProperty("spacingLg", Theme.spacing_lg)
        ctx.setContextProperty("spacingXl", Theme.spacing_xl)
        ctx.setContextProperty(
            "phaseColors",
            {
                "movement": Theme.player.name(),
                "shooting": Theme.objective.name(),
                "charge": "#d97706",
                "fight": Theme.model.name(),
                "command": Theme.muted.name(),
                "defaultPhase": Theme.muted.name(),
            },
        )

    def _create_qml_side_panel_widget(self) -> QQuickWidget:
        self._qml_command_payloads = []
        qml_dir = (APP_DIR / "viewer" / "ui" / "qml").resolve()
        qw = QQuickWidget(self)
        qw.setResizeMode(_QQUICK_RESIZE_ROOT_TO_VIEW)
        qw.setClearColor(QtGui.QColor(Theme.panel.name()))
        eng = qw.engine()
        eng.addImportPath(str(qml_dir))
        self._bind_viewer_main_qml_context(qw)
        qw.setSource(QUrl.fromLocalFile(str(qml_dir / "RightPanel.qml")))
        if qw.status() == QQuickWidget.Status.Error:
            errs = qw.errors()
            raise RuntimeError("; ".join(str(e) for e in errs) if errs else "QML Error")
        self._bind_viewer_main_qml_context(qw)
        self._sync_qml_side_state()
        return qw

    def _maybe_install_qml_hot_reload(self, qw: QQuickWidget) -> None:
        if str(os.getenv("VIEWER_QML_RELOAD", "")).strip() != "1":
            return
        qml_dir = (APP_DIR / "viewer" / "ui" / "qml").resolve()
        self._qml_fs_watcher = QFileSystemWatcher(self)
        self._qml_fs_watcher.addPath(str(qml_dir))
        timer = QtCore.QTimer(self)
        timer.setSingleShot(True)
        timer.setInterval(220)
        self._qml_reload_timer = timer

        def _do_reload():
            self._bind_viewer_main_qml_context(qw)
            eng = qw.engine()
            if eng is not None:
                eng.clearComponentCache()
            qw.setSource(qw.source())
            self._bind_viewer_main_qml_context(qw)
            self._sync_qml_side_state()

        timer.timeout.connect(_do_reload)

        def _debounce():
            timer.stop()
            timer.start()

        self._qml_fs_watcher.directoryChanged.connect(lambda _path: _debounce())

    def _sync_qml_side_state(self) -> None:
        if not self._qml_panels:
            return
        self.viewer_controller.set_command_prompt_text(self._command_prompt_text)
        self.viewer_controller.set_command_hint_text(self._command_hint_text)
        self._sync_qml_command_models()
        self._emit_command_state()

    def _sync_qml_units_summary(self) -> None:
        return

    def _sync_qml_command_models(self) -> None:
        if not self._qml_panels or self._qml_command_label_model is None:
            return
        labels: list[str] = []
        payloads: list = []
        req = self._pending_request
        if req is None:
            self._qml_command_payloads = []
            self._qml_command_label_model.setStringList([])
            return
        if self._is_movement_move_request(req) or self._is_shooting_target_request(req) or self._is_shooting_dice_request(req):
            self._qml_command_payloads = []
            self._qml_command_label_model.setStringList([])
            return

        kind = getattr(req, "kind", "text")
        if kind == "direction":
            mapping = [
                ("↑", "up"),
                ("↓", "down"),
                ("←", "left"),
                ("→", "right"),
                ("Нет", "none"),
            ]
            labels = [m[0] for m in mapping]
            payloads = [m[1] for m in mapping]
        elif kind == "bool":
            labels = ["Да", "Нет"]
            payloads = [True, False]
        elif kind == "pace":
            labels = ["Далее"]
            payloads = [True]
        elif kind == "int":
            labels = [f"ОК ({self._int_spin_value})"]
            payloads = [self._int_spin_value]
        elif kind == "choice":
            raw_opts = list(getattr(req, "options", None) or [])
            labels = [str(o) for o in raw_opts]
            payloads = list(labels)
        else:
            labels = []
            payloads = []

        self._qml_command_payloads = payloads
        self._qml_command_label_model.setStringList(labels)

    def _controller_submit_answer_object(self, value: object) -> None:
        self._submit_answer(value)

    def _emit_command_state(self) -> None:
        req = self._pending_request
        vc = self.viewer_controller
        if req is None:
            vc.set_command_kind("idle")
            vc.set_command_hotkeys([])
            vc.set_command_choices([])
            vc.set_engine_busy(False)
            return
        vc.set_engine_busy(True)
        kind = getattr(req, "kind", "text")
        if self._is_movement_move_request(req):
            kind = "move"
        elif self._is_shooting_target_request(req) or self._is_shooting_dice_request(req):
            kind = "shoot"
        vc.set_command_kind(str(kind))
        hotkeys: list = []
        if kind == "move":
            hotkeys = [
                {"label": "ПКМ", "key": "Move", "secondary": True},
                {"label": "Stay", "key": "Backspace", "secondary": True},
            ]
        elif kind == "shoot":
            hotkeys = [
                {"label": "Fire", "key": "ПКМ", "secondary": True},
                {"label": "Cancel", "key": "Esc", "secondary": True},
            ]
        elif kind == "pace":
            hotkeys = [{"label": "Далее", "key": "Enter"}]
        elif kind == "bool":
            hotkeys = [{"label": "Да", "key": ""}, {"label": "Нет", "key": ""}]
        vc.set_command_hotkeys(hotkeys)
        if kind == "int":
            min_v = int(getattr(req, "min_value", 0) or 0)
            max_v = int(getattr(req, "max_value", 999) or 999)
            vc.set_int_spin_range(min_v, max_v, min_v)
        if kind == "choice":
            raw_opts = list(getattr(req, "options", None) or [])
            vc.set_command_choices([{"label": str(o), "value": str(o)} for o in raw_opts])

    def _set_command_prompt(self, text: str) -> None:
        self._command_prompt_text = str(text or "")
        self.viewer_controller.set_command_prompt_text(self._command_prompt_text)

    def _set_command_hint(self, text: str) -> None:
        self._command_hint_text = str(text or "")
        self.viewer_controller.set_command_hint_text(self._command_hint_text)

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
        weapon_suffix = f" (R{weapon_range})" if isinstance(weapon_range, int) and weapon_range > 0 else ""
        overlay_mode = "Targets"
        if hasattr(self, "map_scene") and hasattr(self.map_scene, "shooting_overlay_mode_label"):
            overlay_mode = str(self.map_scene.shooting_overlay_mode_label())
        return (
            f"Выберите цель ({weapon}{weapon_suffix})\n"
            f"Overlay: {overlay_mode} • ПКМ — Fire • Enter — Shoot • Esc — отмена"
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

    def _shoot_stage_to_step(self, stage: str) -> int:
        stage_norm = str(stage or "").strip().lower()
        if stage_norm in {"target", "hit"}:
            return 0
        if stage_norm == "wound":
            return 1
        if stage_norm == "allocate":
            return 2
        if stage_norm == "save":
            return 3
        if stage_norm in {"damage", "resolve"}:
            return 4
        return max(0, int(self._shoot_resolver_step or 0))

    def _resolve_shoot_stage(self, request) -> str:
        if self._is_shooting_target_request(request):
            return "target"
        if not self._is_shooting_dice_request(request):
            return "resolve"

        meta = getattr(request, "meta", {}) or {}
        for key in ("shoot_stage", "dice_stage", "roll_stage", "stage"):
            raw = meta.get(key) if isinstance(meta, dict) else None
            if not raw:
                continue
            token = str(raw).strip().lower()
            if token in {"hit", "to_hit", "hit_roll"}:
                return "hit"
            if token in {"wound", "to_wound", "wound_roll"}:
                return "wound"
            if token in {"save", "saving_throw", "save_roll"}:
                return "save"

        prompt = str(getattr(request, "prompt", "") or "").strip().lower()
        if any(tok in prompt for tok in ("to hit", "на попад", "попадан")):
            return "hit"
        if any(tok in prompt for tok in ("to wound", "на ранен", "ранени")):
            return "wound"
        if any(tok in prompt for tok in ("saving throw", "save", "сейв", "бросок сейв")):
            return "save"

        # Fallback: если движок не прислал явный stage, сохраняем совместимость,
        # но пишем диагностику о рискованном распознавании.
        fallback = "hit" if self._shoot_resolver_step <= 0 else "wound" if self._shoot_resolver_step <= 1 else "save"
        sig = (
            str(getattr(request, "kind", "")),
            int(getattr(request, "count", 0) or 0),
            prompt,
            fallback,
        )
        if sig != self._last_shoot_stage_debug_sig:
            self._last_shoot_stage_debug_sig = sig
            self.add_log_line(
                "REQ: stage popover определён по fallback. Где: viewer/app.py (_resolve_shoot_stage). "
                f"Что случилось: не удалось явно распознать этап dice-request (prompt='{prompt or '—'}'), выбран fallback={fallback}. "
                "Что делать дальше: добавить в meta запроса явный stage (hit/wound/save), чтобы исключить рассинхрон UI."
            )
        return fallback

    def _count_dice_tokens(self, raw: str, *, min_value: int = 1, max_value: int = 6) -> tuple[int, bool, bool]:
        cleaned = str(raw or "").strip()
        if not cleaned:
            return 0, False, False
        try:
            values = dice_values_from_user_text(cleaned, min_value=min_value, max_value=max_value)
        except ValueError:
            return 0, True, True
        return len(values), False, len(values) > 0

    def _on_shoot_dice_input_changed(self, _text: str) -> None:
        self._update_shoot_input_feedback()

    def _update_shoot_input_feedback(self) -> None:
        if not self._shoot_resolver_active:
            return
        vc = self.viewer_controller
        req = self._pending_request
        stage = self._resolve_shoot_stage(req)
        expects_dice = bool(getattr(req, "kind", "") == "dice" and stage in {"hit", "wound", "save"})
        if not expects_dice:
            vc.update_shoot_ui(dice_counter="0/0", info_text="ℹ На этом шаге ввод кубов не требуется", needs_dice=False)
            return
        count = int(getattr(req, "count", 0) or 0)
        min_v = int(getattr(req, "min_value", 1) or 1)
        max_v = int(getattr(req, "max_value", 6) or 6)
        lock_suffix = ""
        if self._is_shooting_dice_request(req) and self._shoot_locked_target_id is not None:
            lock_suffix = f" • Цель Unit {int(self._shoot_locked_target_id)} зафиксирована"
        entered, has_error, has_tokens = self._count_dice_tokens(
            self._shoot_dice_input_text, min_value=min_v, max_value=max_v
        )
        info = ""
        if has_error:
            info = f"⚠ Только цифры {min_v}–{max_v}: «1 2 3» или слитно «123»"
        elif count <= 0:
            info = f"ℹ Движок не запросил количество кубов{lock_suffix}"
        elif entered < count:
            rest = count - entered
            info = f"ℹ Нужно: {count} d6 • Осталось: {rest}{lock_suffix}" if has_tokens else f"ℹ Нужно: {count} d6{lock_suffix}"
        elif entered > count:
            info = f"⚠ Лишних: {entered - count}. Нужно ровно {count}{lock_suffix}"
        else:
            info = f"ℹ Готово к броску{lock_suffix}"
        vc.update_shoot_ui(dice_counter=f"{entered}/{count}", info_text=info, needs_dice=True)

    def _parse_popover_dice_values(self, request) -> Optional[list[int]]:
        count = int(getattr(request, "count", 0) or 0)
        min_value = int(getattr(request, "min_value", 1) or 1)
        max_value = int(getattr(request, "max_value", 6) or 6)
        raw = self._shoot_dice_input_text.strip()
        if not raw:
            self.viewer_controller.update_shoot_ui(info_text=f"ℹ Нужно: {count} значений d6")
            return None
        try:
            return parse_dice_values(raw, count=count, min_value=min_value, max_value=max_value)
        except ValueError as exc:
            self.viewer_controller.update_shoot_ui(info_text=f"⚠ Ошибка ввода: {exc}")
            return None

    def _update_shoot_popover_ui(self) -> None:
        if not self._shoot_resolver_active or self._shoot_popover_target_id is None:
            self.viewer_controller.set_shoot_popover_open(False)
            return
        attacker = self._shoot_resolver_attacker_id
        request = self._pending_request
        locked_target = self._shoot_locked_target_id
        if self._is_shooting_dice_request(request) and locked_target is not None:
            target = int(locked_target)
            self._shoot_popover_target_id = int(locked_target)
        else:
            target = int(self._shoot_popover_target_id)
        if self._is_shooting_dice_request(request):
            req_target = self._shoot_request_target_id
            if req_target is not None and int(target) != int(req_target):
                self._close_shoot_popover(reset_lock=True, keep_request_target=False)
                self.map_scene.clear_target_selection()
                self._current_target_id = None
                self._shoot_request_flow_active = False
                return
        weapon, weapon_range = "—", None
        if attacker is not None:
            shooter_side = self._side_from_unit_id(int(attacker))
            if shooter_side is not None:
                unit = self._units_by_key.get((shooter_side, int(attacker)))
                if isinstance(unit, dict):
                    weapon, weapon_range = self._resolve_active_weapon(unit)
                    self._remember_active_weapon(attacker, weapon, weapon_range)
        range_text = f"R{weapon_range}" if isinstance(weapon_range, int) and weapon_range > 0 else "—"
        overlay_mode = str(self.map_scene.shooting_overlay_mode_label()) if hasattr(self.map_scene, "shooting_overlay_mode_label") else "Targets"
        stage = self._resolve_shoot_stage(request)
        self._shoot_ui_stage = stage
        self._shoot_resolver_step = self._shoot_stage_to_step(stage)
        dice_mode = getattr(request, "kind", "") == "dice"
        count = int(getattr(request, "count", 0) or 0)
        needs_input = dice_mode and stage in {"hit", "wound", "save"}
        action = "Roll Hit"
        step_title = "STEP 1/5: Hit Roll"
        if stage == "wound":
            action, step_title = "Roll Wound", "STEP 2/5: Wound Roll"
        elif stage == "save":
            action, step_title = "Roll Save", "STEP 4/5: Saving Throw"
        elif stage not in {"target", "hit", "wound", "save"}:
            action, step_title = "Continue", "STEP 5/5: Inflict Damage"
        info = "ℹ Нажмите Roll Hit, чтобы выбрать цель" if stage == "target" else "ℹ Введите кубы и подтвердите"
        self.viewer_controller.set_shoot_popover_open(True)
        self.viewer_controller.update_shoot_ui(
            stage=stage,
            step_title=step_title,
            stepper=self._shoot_stepper_text(),
            target_text=f"Unit {attacker} → Unit {target}",
            meta_text=f"Weapon: {weapon} ({range_text}) • Overlay: {overlay_mode}",
            action_label=action,
            info_text=info,
            needs_dice=needs_input,
        )
        if needs_input:
            self._update_shoot_input_feedback()

    def _open_shoot_popover(self, target_id: int, global_pos: Optional[QtCore.QPoint] = None) -> None:
        if target_id not in self._shoot_targets_valid:
            return
        req = self._pending_request
        if self._is_shooting_dice_request(req) and self._shoot_locked_target_id is not None:
            if int(target_id) != int(self._shoot_locked_target_id):
                self.viewer_dialogs.showToast(
                    f"Цель Unit {target_id} недоступна — зафиксирована Unit {self._shoot_locked_target_id}"
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
        self._shoot_dice_input_text = ""
        self.viewer_controller.setShootDiceInput("")
        self._update_shoot_popover_ui()

    def _close_shoot_popover(self, *, reset_lock: bool = True, keep_request_target: bool = True) -> None:
        self._shoot_popover_target_id = None
        if reset_lock:
            self._shoot_locked_target_id = None
        self._shoot_resolver_active = False
        self._shoot_resolver_step = 0
        self._shoot_resolver_attacker_id = None
        self._shoot_ui_stage = "target"
        if not keep_request_target:
            self._shoot_request_target_id = None
        self.viewer_controller.set_shoot_popover_open(False)
        if self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(self._pending_request):
            self._set_command_prompt(self._shoot_instruction_text())

    def _cancel_shoot_sequence(self) -> None:
        req = self._pending_request
        if not (self._is_shooting_target_request(req) or self._is_shooting_dice_request(req)):
            self._close_shoot_popover(reset_lock=True, keep_request_target=False)
            return

        if self._is_shooting_dice_request(req) and self._shoot_request_target_id is not None:
            self.add_log_line(
                "REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). "
                f"Что случилось: отменяем текущий dice-request для Unit {int(self._shoot_request_target_id)} и сбрасываем выбор цели. "
                "Что делать дальше: выберите новую цель в следующем запросе стрельбы."
            )
            self._close_shoot_popover(reset_lock=True, keep_request_target=False)
            self.map_scene.clear_target_selection()
            self._current_target_id = None
            self._shoot_request_flow_active = False
            self._submit_answer(DICE_CANCEL_TOKEN)
            return

        self._close_shoot_popover(reset_lock=True, keep_request_target=False)
        self.map_scene.clear_target_selection()
        self._current_target_id = None

    def _shoot_step_action(self) -> None:
        if not self._shoot_resolver_active:
            return
        req = self._pending_request
        stage = self._resolve_shoot_stage(req)
        target_id = self._shoot_popover_target_id
        if target_id is None:
            self._close_shoot_popover()
            return

        if stage == "target":
            if self._is_shooting_target_request(req):
                self._shoot_locked_target_id = int(target_id)
                self._submit_answer(str(int(target_id)))
                req = self._pending_request
                stage = self._resolve_shoot_stage(req)
            if stage not in {"hit", "wound", "save"} or getattr(req, "kind", "") != "dice":
                self._update_shoot_popover_ui()
                return

        if stage in {"hit", "wound", "save"}:
            if getattr(req, "kind", "") != "dice":
                self._update_shoot_popover_ui()
                return
            values = self._parse_popover_dice_values(req)
            if values is None:
                return
            self._submit_answer(values)
            self._shoot_dice_input_text = ""
        else:
            self._update_shoot_popover_ui()
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
            self._sync_qml_side_state()
            return

        self._pending_request = request
        self._awaiting_player_action = request is not None
        self._movement_skip_sent = False
        if request is not None:
            self._hide_stale_units_on_bootstrap = False
        if request is None:
            self._deploy_visual_reset_done = False
            self._deploy_context = None
            self._deploy_hover_cell = None
            self._deploy_status_text = ""
            self._clear_deploy_overlays()
            self.map_scene.clear_temporary_deploy_units()
            if self.controller.is_finished:
                self._set_command_prompt("Игра завершена.")
            else:
                self._set_command_prompt("Команда не требуется.")
            self._set_command_hint("Горячие клавиши: —")
            self.map_scene.set_target_cell(None)
            self._shoot_targets_valid = set()
            self._shoot_request_flow_active = False
            self._close_shoot_popover(reset_lock=True, keep_request_target=False)
            self._refresh_active_context()
            self._sync_qml_side_state()
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
            self._shoot_ui_stage = "target"
            self._shoot_resolver_step = 0
            self._shoot_locked_target_id = None
            self._shoot_request_target_id = None
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
            if self._shoot_locked_target_id is not None:
                self._shoot_request_target_id = int(self._shoot_locked_target_id)
            self._shoot_ui_stage = self._resolve_shoot_stage(request)
            self._shoot_resolver_step = self._shoot_stage_to_step(self._shoot_ui_stage)
            self.add_log_line(
                "REQ: движок запросил кубы стрельбы"
                f" (target={self._shoot_request_target_id if self._shoot_request_target_id is not None else '—'}, "
                f"count={int(getattr(request, 'count', 0) or 0)}, stage={self._shoot_ui_stage})."
            )
        else:
            self._shoot_request_flow_active = False
            self._shoot_locked_target_id = None
            self._shoot_request_target_id = None
            self._shoot_targets_valid = set()
        self._update_deploy_status_from_request(request)
        display_prompt = self._deploy_status_text if self._deploy_status_text else request.prompt
        self._set_command_prompt(display_prompt)
        kind = getattr(request, "kind", "text")
        if self._is_movement_move_request(request):
            self._set_command_prompt(self._move_instruction_text())
            self._set_command_hint("Горячие клавиши: ПКМ — идти, Backspace — stay")
        elif self._is_shooting_target_request(request) or self._is_shooting_dice_request(request):
            self._set_command_prompt(self._shoot_instruction_text())
            self._set_command_hint("Горячие клавиши: ПКМ — Fire, Enter — Shoot, Esc — отмена")
        elif kind == "int":
            min_value = request.min_value if request.min_value is not None else 0
            max_value = request.max_value if request.max_value is not None else 999
            self._int_spin_min = int(min_value)
            self._int_spin_max = int(max_value)
            self._int_spin_value = int(min_value)
        elif kind == "choice":
            self._choice_options = [str(o) for o in list(getattr(request, "options", None) or [])]
            if self._choice_options:
                self._last_choice_text = self._choice_options[0]
                if self._is_target_request(request):
                    self._sync_target_from_choice(self._last_choice_text)
                    self._set_confirm_enabled(self._current_target_id is not None)
        elif kind == "deploy_coord":
            meta = getattr(request, "meta", {}) or {}
            if self._is_movement_move_request(request):
                self._deploy_context = dict(meta)
                self._refresh_deploy_preview()
                self._refresh_active_context()
                self._sync_qml_side_state()
                return
            current_side = self._deploy_context.get("deploy_side") if self._deploy_context else None
            current_unit_id = self._deploy_context.get("deploy_unit_id") if self._deploy_context else None
            if current_unit_id is not None:
                side_for_table = "player" if current_side == "enemy" else "model"
                self._set_selected_unit(side_for_table, int(current_unit_id), source="deploy", select_row=True)
            self._refresh_deploy_preview()
        self._refresh_active_context()
        if self._shoot_resolver_active and (
            self._is_shooting_target_request(request) or self._is_shooting_dice_request(request)
        ):
            self._update_shoot_popover_ui()
        self._sync_qml_side_state()

    def _move_instruction_text(self) -> str:
        return (
            "Выберите клетку для хода\n"
            "ЛКМ: hover • ПКМ: идти • Backspace: stay"
        )

    def _build_map_overlay_legend(
        self,
        phase_for_overlay: Optional[str],
        move_range: Optional[object],
        shoot_range: Optional[object],
    ) -> list:
        phase_norm = str(phase_for_overlay or "").strip().lower()
        items: list = []
        if self._is_movement_phase(phase_for_overlay):
            mr = move_range if move_range is not None else "M"
            items.append({"key": "move", "color": "#4882ff", "label": f'Move {mr}"'})
            items.append({"key": "advance", "color": "#ecc240", "label": "Advance +D6"})
        elif self._is_shooting_phase(phase_for_overlay):
            sr = shoot_range if shoot_range is not None else "?"
            items.append({"key": "in_range", "color": Theme.player.name(), "label": f'В range {sr}"'})
            items.append({"key": "out_range", "color": Theme.muted.name(), "label": "Вне range"})
        elif "charge" in phase_norm:
            items.append({"key": "charge", "color": "#d97706", "label": "Charge 2D6"})
        return items

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
        vc = getattr(self, "viewer_controller", None)
        if vc is not None:
            vc.set_command_confirm_enabled(bool(enabled))

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
            self._set_command_prompt(self._shoot_instruction_text())
            if self.viewer_controller.shootPopoverOpen:
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
        # removed command_input.setText(f"{x} {y}")
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
        # removed command_input.setText(f"{x} {y}")
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
            self._set_command_hint(f"Клик заблокирован: {reason}. Выберите валидную клетку.")

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
            self._set_command_hint("Горячие клавиши: ↑ ↓ ← →, пробел/0 — нет")
        elif kind == "bool":
            self._set_command_hint("Горячие клавиши: Y — да, N — нет")
        elif kind == "pace":
            self._set_command_hint("Горячие клавиши: Enter / Пробел — далее")
        elif kind == "int":
            self._set_command_hint("Горячие клавиши: Enter — отправить")
        elif kind == "choice":
            if self._is_shooting_target_request(self._pending_request):
                self._set_command_hint("ПКМ по валидной цели откроет Fire popover")
            else:
                self._set_command_hint("Горячие клавиши: Enter — выбрать")
        elif kind == "deploy_coord":
            if self._is_movement_move_request(self._pending_request):
                self._set_command_hint("ПКМ по подсвеченной клетке. ЛКМ — hover/выбор, Backspace — stay")
            elif self._is_move_cell_request(self._pending_request):
                self._set_command_hint("RMB по подсвеченной клетке или введите X Y, затем Enter")
            else:
                self._set_command_hint("Кликните клетку на поле или введите X Y, затем Enter")
        else:
            self._set_command_hint("Горячие клавиши: Enter — отправить")

    def _init_log_viewer(self) -> None:
        self._log_status_label = None
        self._log_controls_layout = QtWidgets.QHBoxLayout()
        self._log_filter_buttons = {}
        self.log_view = None
        self._log_panel_widget = None
        self._qml_log_model = ViewerLogListModel(self)
        self._qml_log_model.set_filters(self.viewer_controller._log_filters)

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
            self._refresh_log_views()

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
        self._shoot_request_target_id: Optional[int] = None
        self._shoot_ui_stage: str = "target"
        self._last_shoot_stage_debug_sig: Optional[tuple] = None
        self._active_weapon_name = None
        self._active_weapon_range = None
        self._active_weapon_unit_id = None
        self._deploy_context = None
        self._deploy_hover_cell = None
        self._deploy_status_text = ""
        self._rolloff_attacker_side = None
        self._rolloff_defender_side = None
        self._hp_snapshot_by_unit = {}
        self._popup_seen = OrderedDict()

    def _submit_text(self):
        text = self._last_command_text.strip()
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
                entered = self._count_dice_entries(text, min_value=min_value, max_value=max_value)
                self._set_command_prompt(
                    "Ошибка ввода кубов в панели «Команды»: "
                    f"{exc}. Нужно {count}, введено {entered}. "
                    "Что делать дальше: исправьте ввод и отправьте снова.\n"
                    f"{self._pending_request.prompt}"
                )
                return
            self._last_command_text = ""
            self._submit_answer(values)
            return
        self._last_command_text = ""
        self._submit_answer(text)

    def _submit_choice(self):
        value = self._last_choice_text
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
        settings = QtCore.QSettings("40kAI", "Viewer")
        saved = settings.value("topSplitterSizes")
        if isinstance(saved, list) and len(saved) >= 2:
            try:
                self._top_splitter.setSizes([int(v) for v in saved])
                return
            except (TypeError, ValueError):
                pass
        total_w = max(self.width(), 2560)
        right_w = max(360, min(520, int(total_w * 0.22)))
        left_w = max(1200, total_w - right_w)
        self._top_splitter.setSizes([left_w, right_w])

    def _fit_view(self):
        self.map_scene.fit_to_view()

    def _poll_state(self):
        if not os.path.exists(self.state_watcher.path):
            self.map_scene.set_error_message(
                "Состояние игры недоступно. Где: viewer/state.json. "
                "Что делать дальше: запустите игру и дождитесь генерации state.json."
            )
            return
        if not self.state_watcher.load_if_changed():
            return
        for _ in range(64):
            if not self.state_watcher.load_if_changed():
                break
        self._apply_state(self.state_watcher.state)

    def _pace_activation_summary_ru(self, state: dict) -> Tuple[str, str]:
        """Краткое RU-описание viewer.activation (ожидающий шаг или уже показанное для legacy)."""
        vinfo = state.get("viewer") if isinstance(state.get("viewer"), dict) else {}
        act = vinfo.get("activation")
        if not isinstance(act, dict) or not act:
            return "", ""
        phase = str(act.get("phase") or "").strip().lower()
        step_kind = str(act.get("step_kind") or "").strip().lower()
        uid = act.get("unit_id")
        unit_tail = ""
        if uid is not None:
            try:
                unit_tail = f"юнит {int(uid)}"
            except (TypeError, ValueError):
                unit_tail = ""
        elif act.get("unit_index") is not None:
            try:
                unit_tail = f"отряд #{int(act.get('unit_index'))}"
            except (TypeError, ValueError):
                unit_tail = ""

        phase_ru = {
            "command": "командование",
            "movement": "движение",
            "shooting": "стрельба",
            "charge": "заряд",
            "fight": "бой",
        }.get(phase, phase or "шаг")

        if step_kind == "command_resolve":
            detail = f"{phase_ru} · завершение фазы"
            short = detail[:72] + ("…" if len(detail) > 72 else "")
            return detail, short

        if step_kind == "phase_end":
            detail = f"конец фазы · {phase_ru}"
        elif step_kind == "before_unit" and unit_tail:
            detail = f"{phase_ru} · {unit_tail}"
        elif step_kind == "before_unit":
            detail = phase_ru
        elif step_kind == "unit" and unit_tail:
            detail = f"{phase_ru} · {unit_tail}"
        elif step_kind == "unit":
            detail = phase_ru
        else:
            detail = f"{phase_ru}" + (f" · {unit_tail}" if unit_tail else "")
        short = detail[:72] + ("…" if len(detail) > 72 else "")
        return detail, short

    def _pace_action_caption_from_state(self, state: dict) -> str:
        """Компактная кнопка: «Далее: суть шага» (фаза/юнит), без «ход ИИ» и без дублирования."""
        vinfo = state.get("viewer") if isinstance(state.get("viewer"), dict) else {}
        act = vinfo.get("activation")
        if not isinstance(act, dict) or not act:
            return "Далее"
        _, short = self._pace_activation_summary_ru(state)
        if not short:
            return "Далее"
        return f"Далее: {short}"

    def _pace_action_tooltip_from_state(self, state: dict) -> str:
        vinfo = state.get("viewer") if isinstance(state.get("viewer"), dict) else {}
        act = vinfo.get("activation")
        step_kind = str(act.get("step_kind") or "").strip().lower() if isinstance(act, dict) else ""
        detail, _ = self._pace_activation_summary_ru(state)
        if not detail:
            return (
                "Продолжить сценарий ИИ (Viewer pacing). "
                "Кнопка снимает паузу: для микрошага по юниту движок применит его к полю после нажатия."
            )
        if step_kind == "command_resolve":
            return (
                f"Следующий шаг: {detail}. "
                f"После «Далее» применится конец фазы командования (эффекты на конец фазы, при наличии — в т.ч. восстановление моделей) и обновится поле."
            )
        if step_kind == "before_unit":
            return (
                f"Следующий шаг: {detail}. "
                f"После «Далее» движок применит его к полю."
            )
        if step_kind == "unit":
            return (
                f"Уже показано на поле: {detail}. "
                f"«Далее» не повторяет этот ход — он уже выполнен движком; кнопка переводит к следующему микрошагу ИИ."
            )
        return (
            f"Уже показано на поле: {detail}. "
            f"«Далее» переводит к следующему микрошагу ИИ."
        )

    def _update_pace_next_button_from_state(self, state: dict) -> None:
        if not hasattr(self, "pace_next_button"):
            return
        self.pace_next_button.setText(self._pace_action_caption_from_state(state))
        self.pace_next_button.setToolTip(self._pace_action_tooltip_from_state(state))

    def _apply_state(self, state):
        state_for_view = state
        if self._hide_stale_units_on_bootstrap:
            state_for_view = dict(state or {})
            state_for_view["units"] = []
        self.map_scene.update_state(state_for_view)
        if not self._did_initial_fit:
            self._did_initial_fit = True
            QtCore.QTimer.singleShot(0, self._fit_view)

        self._units_by_key = {}
        for unit in state_for_view.get("units", []) or []:
            self._units_by_key[(unit.get("side"), unit.get("id"))] = unit
        self._refresh_hp_snapshot()

        hdr_ctx = ViewerPresentationContext(
            player_role_label=self._viewer_player_role_label,
            model_role_label=self._viewer_model_role_label,
            rolloff_attacker_side=self._rolloff_attacker_side,
            rolloff_defender_side=self._rolloff_defender_side,
            deploy_status_suffix=self._deploy_status_text or "",
        )
        labels = compute_status_labels(state, hdr_ctx)
        active_raw = str(state.get("active") or state.get("active_side") or "").strip().lower()
        phase_raw_val = str(state.get("phase") or "").strip().lower()

        self.viewer_controller.apply_labels(
            labels,
            phase_raw=phase_raw_val,
            active_side_raw=active_raw,
        )

        if os.getenv("VIEWER_DEBUG", "0") == "1":
            deployment = state.get("deployment", {}) if isinstance(state.get("deployment", {}), dict) else {}
            attacker = deployment.get("attacker") or state.get("attacker_side")
            defender = deployment.get("defender") or state.get("defender_side")
            deploy_phase_text = str(state.get("phase") or "").strip().lower()
            deploy_active = ("deploy" in deploy_phase_text) or ("расст" in deploy_phase_text)
            self.add_log_line(
                f"[STATUS] phase={state.get('phase')} deploy_state={'active' if deploy_active else 'completed'} "
                f"attacker={attacker} defender={defender} text=\"{self.viewer_controller.deploymentText}\""
            )

        self._populate_units_table(state_for_view.get("units", []))
        self._update_log(state.get("log_tail", []))
        self._update_pace_next_button_from_state(state)
        # Move overlay на карте только при наведении на строку лога (hover), не после «Далее»/state.
        self.map_scene.set_log_movement_overlay(None, persistent=True)
        self._update_model_events(state.get("model_events", []))
        self._clear_stale_target_marker_during_model_turn(state)
        self._drain_event_queue()
        self._refresh_active_context()
        if not (self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(self._pending_request)):
            self._close_shoot_popover()
        elif self._shoot_popover_target_id is not None and int(self._shoot_popover_target_id) not in self._shoot_targets_valid:
            self._close_shoot_popover()

    def _populate_units_table(self, units):
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
        self._sync_qml_units_summary()

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
            self._refresh_log_views()
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
        if self._controller_v1:
            self.viewer_controller.set_selection_source(source)
            self.viewer_controller.push_selection(side, unit_id)
        self.map_scene.set_selected_unit(side, unit_id)
        if select_row:
            self._scroll_units_list_to_unit(unit_id, side=side)
        if self._viewer_units_model is not None:
            self._viewer_units_model.update_selection(
                self._selected_unit_side, self._selected_unit_id
            )
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
        self._set_selected_unit(side, unit_id, source="map", select_row=False)
        self._scroll_units_list_to_unit(unit_id, side=side)
        self._on_target_selected(unit_id)

    def _sync_selection_from_table(self):
        pass

    def add_log_line(self, line: str):
        raw_text = str(line)
        self._capture_rolloff_sides_from_log(raw_text)
        self._update_turn_context(raw_text)
        categories = self._classify_line(raw_text)
        if self._should_assign_shooting_side(raw_text, categories):
            categories.add(self._current_turn_side)
        channel = self._detect_log_channel(raw_text, categories)
        display_text = self._decorate_log_line(raw_text, categories)
        entry = {
            "raw": raw_text,
            "display": display_text,
            "compact": self._compact_gameplay_line(raw_text, categories),
            "turn": self._current_turn_number,
            "categories": categories,
            "channel": channel,
        }
        self._log_entries.append(entry)
        self._append_log_to_file(raw_text)
        self._fx_parser.consume_line(raw_text)
        self._drain_fx_queue()
        if len(self._log_entries) > self._max_log_lines:
            self._log_entries = self._log_entries[-self._max_log_lines :]
        self._refresh_log_views()

    def _append_to_view(self, view: QtWidgets.QPlainTextEdit, text: str):
        scrollbar = view.verticalScrollBar()
        at_bottom = scrollbar.value() >= scrollbar.maximum()
        view.appendPlainText(text)
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    def _classify_line(self, line: str):
        lowered = line.lower()
        is_target_shoot_trace = self._is_target_shoot_trace(line)
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
        if (not is_target_shoot_trace) and self._matches_any(
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
            categories.add("combat_basic")
            categories.add("key")
        if "shooting" not in categories and self._is_shooting_report_line(line):
            categories.add("shooting")
            categories.add("combat_basic")
            categories.add("key")
        if is_target_shoot_trace:
            categories.add("debug")
        if self._matches_any(
            lowered,
            [
                "движение",
                "movement",
                "move:",
                "позиция до",
                "позиция после",
                "no move",
                "ходьб",
            ],
        ):
            categories.add("movement")
            categories.add("combat_basic")
        if self._matches_any(
            lowered,
            [
                "чардж",
                "charge",
            ],
        ):
            categories.add("charge")
            categories.add("combat_basic")

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
            categories.add("combat_basic")
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
                "reward (",
                "fx:",
                "los_debug",
                "req:",
            ],
        ):
            categories.add("debug")
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
            categories.add("result")
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
        if self._matches_any(
            lowered,
            [
                "побед",
                "winner",
                "конец боевого раунда",
                "game over",
                "итерация",
            ],
        ):
            categories.add("result")
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

    def _is_target_shoot_trace(self, text: str) -> bool:
        lowered = str(text or "").lower()
        return "[target][shoot]" in lowered

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

    def _is_combat_event(self, event: dict) -> bool:
        phase = str((event or {}).get("phase") or "").lower()
        return phase in {"movement", "shooting", "charge", "fight"}

    def _detect_log_channel(self, text: str, categories: set) -> str:
        lowered = str(text or "").lower()
        if self._is_target_shoot_trace(text):
            return "fx"
        if "los_debug" in lowered:
            return "los"
        if "fx:" in lowered:
            return "fx"
        if "reward (" in lowered:
            return "reward"
        if "req:" in lowered:
            return "req"
        if "errors" in categories:
            return "error"
        if "result" in categories:
            return "result"
        if "turn" in categories or "key" in categories:
            return "phase"
        if "combat_basic" in categories:
            return "combat"
        return "system"

    def _compact_gameplay_line(self, text: str, categories: set) -> str:
        raw = str(text or "").strip()
        if not raw:
            return ""
        reason_tag = self._reason_tag(raw)
        if "movement" in categories:
            if "позиция до" in raw.lower() or "позиция после" in raw.lower():
                return f"👣 {raw}{reason_tag}"
        if "shooting" in categories:
            return f"🎯 {raw}{reason_tag}"
        if "charge" in categories:
            return f"⚡ {raw}{reason_tag}"
        if "fight" in categories:
            return f"⚔️ {raw}{reason_tag}"
        if "result" in categories:
            return f"🏁 {raw}{reason_tag}"
        if "errors" in categories:
            return f"⚠️ {raw}{reason_tag}"
        if "turn" in categories or "key" in categories:
            return f"⭐ {raw}{reason_tag}"
        return f"{raw}{reason_tag}"

    def _reason_tag(self, raw: str) -> str:
        lowered = str(raw or "").lower()
        if "цель вне дальности" in lowered:
            return " [reason:out_of_range]"
        if "нет доступных целей" in lowered:
            return " [reason:no_targets]"
        if "advance без assault" in lowered:
            return " [reason:advance_no_assault]"
        if "advance — чардж невозможен" in lowered or "чардж невозможен" in lowered:
            return " [reason:advance_no_charge]"
        if "overwatch невозможен" in lowered and "нет доступных стреляющих юнитов" in lowered:
            return " [reason:no_overwatch_units]"
        return ""

    def _entry_matches_filter(self, entry: dict) -> bool:
        categories = entry.get("categories", set())
        channel = entry.get("channel")
        if channel in {"fx", "los", "reward", "req", "system"}:
            debug_btn = self._log_filter_buttons.get("debug")
            return bool(debug_btn is not None and debug_btn.isChecked())
        if "combat_basic" in categories or "turn" in categories or "result" in categories or "errors" in categories:
            return True
        return False

    def _is_filter_enabled_for_entry(self, entry: dict) -> bool:
        categories = entry.get("categories", set())
        channel = entry.get("channel")
        mapping = {
            "movement": "movement" in categories,
            "shooting": "shooting" in categories,
            "charge": "charge" in categories,
            "fight": "fight" in categories,
            "result": "result" in categories or channel in {"phase", "result"},
            "errors": "errors" in categories or channel == "error",
            "debug": channel in {"fx", "los", "reward", "req", "system"} or "debug" in categories,
        }
        filters = self.viewer_controller._log_filters
        for key, match in mapping.items():
            if filters.get(key, True) and match:
                return True
        return False

    def _should_show_entry(self, entry):
        if not self._entry_matches_filter(entry):
            return False
        return self._is_filter_enabled_for_entry(entry)

    def _collect_alert_lines(self) -> list[str]:
        out_of_range_count = 0
        overwatch_block_count = 0
        for entry in self._log_entries[-300:]:
            text = str(entry.get("raw") or "").lower()
            if "цель вне дальности" in text:
                out_of_range_count += 1
            if "overwatch невозможен" in text and "нет доступных стреляющих юнитов" in text:
                overwatch_block_count += 1
        alerts = []
        if out_of_range_count >= 3:
            alerts.append(f"⚠️ Алерт: много out_of_range за окно журнала ({out_of_range_count}).")
        if overwatch_block_count >= 3:
            alerts.append(f"⚠️ Алерт: часто блокируется Overwatch ({overwatch_block_count}).")
        return alerts

    def _build_round_summary_card(self) -> list[str]:
        result_lines = [str(e.get("raw") or "") for e in self._log_entries[-200:] if "result" in (e.get("categories") or set())]
        if not result_lines:
            return []
        last_round = next((line for line in reversed(result_lines) if "конец боевого раунда" in line.lower()), None)
        last_iter = next((line for line in reversed(result_lines) if "итерация" in line.lower() and "здоровье" in line.lower()), None)
        hp_line = next((line for line in reversed(result_lines) if "здоровье model" in line.lower()), None)
        if not any((last_round, last_iter, hp_line)):
            return []
        card = ["🏁 === КАРТОЧКА РАУНДА ==="]
        if last_round:
            card.append(last_round)
        if last_iter:
            card.append(last_iter)
        if hp_line:
            card.append(hp_line)
        return card

    def _timeline_label_text(self) -> str:
        try:
            vc = self.viewer_controller
            return f"{vc.roundText} • {vc.activeLabelText} • {vc.phaseText}"
        except RuntimeError:
            if self._controller_v1:
                vc = self.viewer_controller
                return f"{vc.roundText} • {vc.activeLabelText} • {vc.phaseText}"
            return "Раунд: — • Активен: — • Фаза: —"

    def _collect_visible_entries(self):
        visible = []
        for idx, entry in enumerate(self._log_entries):
            if not self._should_show_entry(entry):
                continue
            text = entry["display"] if entry.get("channel") in {"fx", "los", "reward", "req", "system"} else (entry.get("compact") or entry["display"])
            color = self._line_color(entry)
            visible.append({"text": text, "color": color, "entry_idx": idx, "is_aux": False})
        return visible

    def _line_color(self, entry: dict) -> str:
        categories = entry.get("categories", set())
        channel = entry.get("channel")
        if "errors" in categories or channel == "error":
            return "#ff6b6b"
        if "shooting" in categories:
            return "#ffd166"
        if "fight" in categories:
            return "#f4978e"
        if "charge" in categories:
            return "#b388eb"
        if "movement" in categories:
            return "#7bd389"
        if "result" in categories:
            return "#7aa2f7"
        if channel in {"fx", "los", "reward", "req", "system"}:
            return Theme.muted.name()
        return Theme.text.name()

    def _refresh_log_views(self):
        visible_entries = self._collect_visible_entries()
        lines = [v["text"] for v in visible_entries]

        alert_lines = self._collect_alert_lines()
        filters = self.viewer_controller._log_filters
        round_card = self._build_round_summary_card() if filters.get("result", True) else []
        show_alerts = bool(alert_lines and filters.get("errors", True))
        if show_alerts:
            lines.extend(["", "=== АЛЕРТЫ ===", *alert_lines])
        if round_card:
            lines.extend(["", *round_card])

        self._visible_log_entries = list(visible_entries)
        if show_alerts:
            self._visible_log_entries.append({"text": "=== АЛЕРТЫ ===", "color": "#ff9f43", "entry_idx": -1, "is_aux": True})
            for alert in alert_lines:
                self._visible_log_entries.append({"text": alert, "color": "#ff9f43", "entry_idx": -1, "is_aux": True})
        if round_card:
            self._visible_log_entries.append({"text": "🏁 === КАРТОЧКА РАУНДА ===", "color": "#7aa2f7", "entry_idx": -1, "is_aux": True})
            for line in round_card[1:]:
                self._visible_log_entries.append({"text": line, "color": "#7aa2f7", "entry_idx": -1, "is_aux": True})

        if self._qml_log_model is not None:
            self._qml_log_model.set_filters(self.viewer_controller._log_filters)
            self._qml_log_model.set_search(self.viewer_controller.logSearchText)
            turn_key = f"{self._current_turn_number}:{self._current_turn_side}"
            self._qml_log_model.set_current_turn_key(turn_key)
            enriched = []
            for item_data in self._visible_log_entries:
                raw = str(item_data.get("text") or "")
                kind = classify_log_kind(raw)
                enriched.append(
                    {
                        **item_data,
                        "kind": kind,
                        "timestamp": extract_log_timestamp(raw),
                        "is_header": False,
                        "header_text": "",
                        "unit_id": -1,
                        "is_current_turn": True,
                    }
                )
            def _row_color(kind: str) -> str:
                if kind == "header":
                    return Theme.muted.name()
                return Theme.text.name()

            qml_rows = self._qml_log_model.build_rows_from_entries(
                enriched,
                color_resolver=_row_color,
            )
            if not qml_rows:
                qml_rows = []
            self._qml_log_model.set_rows(qml_rows)
            self.viewer_controller.bump_log_refresh()
        self._update_log_filter_hidden_counts()

        if self.log_view is not None:
            self.log_view.clear()
            for item_data in self._visible_log_entries:
                item = QtWidgets.QListWidgetItem(str(item_data.get("text") or ""))
                item.setForeground(QtGui.QBrush(QtGui.QColor(str(item_data.get("color") or Theme.text.name()))))
                item.setData(QtCore.Qt.UserRole, item_data)
                self.log_view.addItem(item)
            if self.log_view.count() > 0:
                self.log_view.scrollToBottom()

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
                channel = self._detect_log_channel(raw_text, categories)
                self._log_entries.append(
                    {
                        "raw": raw_text,
                        "display": self._decorate_log_line(raw_text, categories),
                        "compact": self._compact_gameplay_line(raw_text, categories),
                        "turn": self._current_turn_number,
                        "categories": categories,
                        "channel": channel,
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
        if self.log_view is not None:
            self.log_view.clear()
        if self._qml_log_model is not None:
            self._qml_log_model.set_rows([])
            self.viewer_controller.bump_log_refresh()
        self._visible_log_entries = []
        self.map_scene.set_log_movement_overlay(None, persistent=True)
        self.map_scene.clear_log_movement_hover_overlay()

    def _collect_current_turn_logs(self):
        return "\n".join(str(v.get("text") or "") for v in self._visible_log_entries)

    def _on_log_item_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        payload = self._movement_payload_from_log_item(item)
        if payload is None:
            return
        self.map_scene.clear_log_movement_hover_overlay()
        self._focus_camera_for_movement_payload(payload)

    def _on_log_item_hovered(self, item: QtWidgets.QListWidgetItem) -> None:
        payload = self._movement_payload_from_log_item(item)
        if payload is None:
            self.map_scene.clear_log_movement_hover_overlay()
            return
        self.map_scene.set_log_movement_overlay(payload, persistent=False)

    def _on_log_item_hover_left(self) -> None:
        self.map_scene.clear_log_movement_hover_overlay()
        self.map_scene.set_log_movement_overlay(None, persistent=True)

    def _focus_camera_for_movement_payload(self, payload: dict) -> None:
        to_pos = payload.get("to")
        from_pos = payload.get("from")
        target = to_pos if isinstance(to_pos, tuple) else from_pos
        if not (isinstance(target, tuple) and len(target) >= 2):
            return
        ok = self.map_scene.center_on_state_cell(int(target[0]), int(target[1]))
        if not ok:
            self.add_log_line(
                "[VIEWER] Не удалось центрировать камеру: координаты вне карты. Где: viewer/app.py (_focus_camera_for_movement_payload). Что дальше: проверьте событие движения."
            )

    def _movement_payload_from_entry_data(self, data: Optional[dict]) -> Optional[dict]:
        if not isinstance(data, dict) or data.get("is_aux"):
            return None
        entry_idx = data.get("entry_idx")
        if not isinstance(entry_idx, int) or entry_idx < 0 or entry_idx >= len(self._log_entries):
            return None
        entry = self._log_entries[entry_idx] if 0 <= entry_idx < len(self._log_entries) else {}
        categories = entry.get("categories") if isinstance(entry, dict) else set()
        raw_text = str(entry.get("raw") or "") if isinstance(entry, dict) else ""
        if "movement" not in (categories or set()):
            return None
        lowered = raw_text.lower()
        if "позиция до:" not in lowered and "позиция после:" not in lowered:
            return None
        return self._extract_movement_payload(entry_idx)

    def _movement_payload_from_log_item(self, item: Optional[QtWidgets.QListWidgetItem]) -> Optional[dict]:
        if item is None:
            return None
        data = item.data(QtCore.Qt.UserRole)
        return self._movement_payload_from_entry_data(data if isinstance(data, dict) else None)

    def _on_qml_log_row_clicked(self, row: int) -> None:
        if row < 0 or row >= len(self._visible_log_entries):
            return
        payload = self._movement_payload_from_entry_data(self._visible_log_entries[row])
        if payload is None:
            return
        self.map_scene.clear_log_movement_hover_overlay()
        self._focus_camera_for_movement_payload(payload)

    def _on_qml_log_row_hovered(self, row: int) -> None:
        if row < 0 or row >= len(self._visible_log_entries):
            return
        payload = self._movement_payload_from_entry_data(self._visible_log_entries[row])
        if payload is None:
            self.map_scene.clear_log_movement_hover_overlay()
            return
        self.map_scene.set_log_movement_overlay(payload, persistent=False)

    def _on_qml_log_hover_exited(self) -> None:
        self._on_log_item_hover_left()

    def _extract_movement_payload(self, entry_idx: int) -> Optional[dict]:
        move_before_re = re.compile(
            r"Unit\s+(?P<id>\d+).*?Позиция до:\s*\((?P<x>-?\d+),\s*(?P<y>-?\d+)\).*?distance=(?P<dist>\d+)",
            re.IGNORECASE,
        )
        move_after_re = re.compile(r"Unit\s+(?P<id>\d+).*?Позиция после:\s*\((?P<x>-?\d+),\s*(?P<y>-?\d+)\)", re.IGNORECASE)
        unit_id_re = re.compile(r"Unit\s+(?P<id>\d+)", re.IGNORECASE)

        anchor_text = str((self._log_entries[entry_idx] or {}).get("raw") or "") if 0 <= entry_idx < len(self._log_entries) else ""
        hinted_unit_id = None
        hinted_match = unit_id_re.search(anchor_text)
        if hinted_match:
            hinted_unit_id = int(hinted_match.group("id"))

        unit_id = hinted_unit_id
        from_pos = None
        to_pos = None
        unit_name = ""
        distance = None
        no_move = False
        start = max(0, entry_idx - 12)
        end = min(len(self._log_entries), entry_idx + 12)

        def _log_pos_to_state_xy(raw_a: str, raw_b: str) -> tuple[int, int]:
            # В movement-логах координаты исторически пишутся как (y, x),
            # а рендер использует state-space (x, y).
            row_y = int(raw_a)
            col_x = int(raw_b)
            return col_x, row_y

        for idx in range(start, end):
            text = str((self._log_entries[idx] or {}).get("raw") or "")
            before = move_before_re.search(text)
            if before:
                current_id = int(before.group("id"))
                if unit_id is None:
                    unit_id = current_id
                if current_id == unit_id:
                    from_pos = _log_pos_to_state_xy(before.group("x"), before.group("y"))
                    distance = int(before.group("dist"))
                    name_match = re.search(r"Unit\s+\d+\s+—\s+([^:]+):", text)
                    if name_match:
                        unit_name = str(name_match.group(1)).strip()
            after = move_after_re.search(text)
            if after:
                current_id = int(after.group("id"))
                if unit_id is None:
                    unit_id = current_id
                if current_id == unit_id:
                    to_pos = _log_pos_to_state_xy(after.group("x"), after.group("y"))
                    if "no move" in text.lower() or "движение пропущено" in text.lower():
                        no_move = True
            if "no move" in text.lower() and unit_id is not None and f"Unit {unit_id}" in text:
                no_move = True

        if unit_id is None or from_pos is None:
            return None
        if to_pos is None:
            to_pos = from_pos
            no_move = True
        if distance == 0:
            no_move = True
        return {
            "unit_id": int(unit_id),
            "from": from_pos,
            "to": to_pos,
            "unit_name": unit_name,
            "distance": int(distance) if isinstance(distance, int) else None,
            "no_move": bool(no_move or from_pos == to_pos),
        }

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
        rotated = str(AGENT_PLAY_LOG_PATH.parent / "LOGS_FOR_AGENTS_PLAY.old.md")
        try:
            if os.path.exists(rotated):
                os.remove(rotated)
            os.replace(self._log_file_path, rotated)
        except OSError:
            pass

    def _count_dice_entries(self, text: str, min_value: int = 1, max_value: int = 6) -> int:
        try:
            return len(dice_values_from_user_text(text, min_value=min_value, max_value=max_value))
        except ValueError:
            stripped = str(text or "").strip()
            if not stripped:
                return 0
            if max_value <= 9 and not re.search(r"[\s,]", stripped) and stripped.isdigit():
                return len(stripped)
            return len([p for p in re.split(r"[,\s]+", stripped) if p])

    def _rebuild_unit_row_mapping(self):
        self._unit_row_by_key = {}
        if self._viewer_units_model is None:
            return
        for row in range(self._viewer_units_model.rowCount()):
            side = self._viewer_units_model.data(self._viewer_units_model.index(row, 0), ViewerUnitsListModel.SideRole)
            uid = self._viewer_units_model.data(self._viewer_units_model.index(row, 0), ViewerUnitsListModel.IdRole)
            if side and uid is not None:
                self._unit_row_by_key[(side, int(uid))] = row

    def _find_row_for_unit(self, unit_key):
        return self._unit_row_by_key.get(unit_key)

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

    @staticmethod
    def _state_active_is_model(state: Optional[dict]) -> bool:
        if not isinstance(state, dict):
            return False
        return str(state.get("active") or state.get("active_side") or "").strip().lower() == "model"

    @staticmethod
    def _viewer_activation_model_unit(state: Optional[dict]) -> Tuple[Optional[int], Optional[str]]:
        """Активный юнит ИИ из state.viewer.activation (после экспорта движка)."""
        if not isinstance(state, dict):
            return None, None
        vinfo = state.get("viewer")
        if not isinstance(vinfo, dict):
            return None, None
        act = vinfo.get("activation")
        if not isinstance(act, dict):
            return None, None
        if str(act.get("side") or "").strip().lower() != "model":
            return None, None
        uid = act.get("unit_id")
        if uid is None:
            return None, None
        try:
            return int(uid), "model"
        except (TypeError, ValueError):
            return None, None

    def _clear_stale_target_marker_during_model_turn(self, state: dict) -> None:
        """Сбрасываем маркер цели с хода игрока до обработки FX (иначе «залипает» на отряде игрока)."""
        if not self._state_active_is_model(state):
            return
        if self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(
            self._pending_request
        ):
            return
        if self._is_target_request(self._pending_request):
            return
        self.map_scene.clear_target_selection()

    def _flash_model_shot_target_overlay(self, target_id: int) -> None:
        """Коротко показывает кольцо «цель» на отряде игрока при выстреле ИИ."""
        self._model_shot_target_flash_gen += 1
        gen = self._model_shot_target_flash_gen
        self.map_scene.set_target_unit(int(target_id))

        def _clear() -> None:
            if gen != self._model_shot_target_flash_gen:
                return
            if self._is_shooting_target_request(self._pending_request) or self._is_shooting_dice_request(
                self._pending_request
            ):
                return
            if self._is_target_request(self._pending_request):
                return
            self.map_scene.clear_target_selection()

        QtCore.QTimer.singleShot(1500, _clear)

    def _scroll_units_list_to_unit(self, unit_id, side=None) -> None:
        if side is None:
            for (s, uid) in self._unit_row_by_key:
                if uid == unit_id:
                    side = s
                    break
        if side is None:
            return
        if self._controller_v1 and self.viewer_controller is not None:
            self.viewer_controller.scrollUnitsListToUnit(int(unit_id))

    def _select_row_for_unit_id(self, unit_id, side=None):
        self._scroll_units_list_to_unit(unit_id, side=side)

    
    def _refresh_active_context(self):
        state = self.state_watcher.state if self.state_watcher else None
        model_turn = self._state_active_is_model(state)

        unit_id, side = self._resolve_active_unit()
        if model_turn:
            # Ход ИИ: подсветка «активного отряда» только из viewer.activation, не из выбора игрока в таблице.
            a_uid, a_side = self._viewer_activation_model_unit(state)
            if a_uid is not None:
                unit_id, side = a_uid, a_side
            elif unit_id is None:
                unit_id, side = None, None
        else:
            if unit_id is None:
                unit_id = self._shoot_resolver_attacker_id or self._last_shooter_id or self._selected_unit_id
                if unit_id is not None:
                    side = self._side_from_unit_id(int(unit_id)) or self._selected_unit_side

        self._active_unit_id = unit_id
        self._active_unit_side = side
        if not model_turn and self._selected_unit_id is None and unit_id is not None:
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
        if self._controller_v1:
            self.viewer_controller.set_map_overlay_legend(
                self._build_map_overlay_legend(phase_for_overlay, move_range, shoot_range)
            )

    def _update_log_filter_hidden_counts(self) -> None:
        from collections import Counter

        filters = self.viewer_controller._log_filters
        hidden: Counter = Counter()
        for entry in self._log_entries:
            raw = str(entry.get("raw") or entry.get("display") or "")
            kind = classify_log_kind(raw)
            if kind in filters and not filters.get(kind, True):
                hidden[kind] += 1
        self.viewer_controller.set_log_filter_hidden_counts(dict(hidden))

    def _enqueue_fx_event(self, event: FxShotEvent) -> None:
        self._fx_shot_queue.append(event)

    def _drain_fx_queue(self) -> None:
        while self._fx_shot_queue:
            event = self._fx_shot_queue.popleft()
            self._spawn_fx_for_event(event)

    def _spawn_fx_for_event(self, event: FxShotEvent) -> None:
        self._emit_damage_popup(event)
        if event.report_type == "heal" or event.outcome_type == "heal":
            return
        attacker_side = self._side_from_unit_id(event.attacker_id)
        target_side = self._side_from_unit_id(event.target_id)
        if attacker_side == "model" and target_side == "player":
            self._flash_model_shot_target_overlay(int(event.target_id))
        profile = resolve_fx_profile(event.weapon_name)
        if profile is None:
            self._fx_debug(
                f"FX: для оружия '{event.weapon_name}' нет профиля, эффект пропущен."
            )
            return
        fx_key, config = profile
        start = self.map_scene.unit_shoot_anchor_world(attacker_side, event.attacker_id)
        if start is None:
            start = self._unit_world_center_by_key(attacker_side, event.attacker_id)
        end = self.map_scene.unit_shoot_anchor_world(target_side, event.target_id)
        if end is None:
            end = self._unit_world_center_by_key(target_side, event.target_id)
        if start is None or end is None:
            self._fx_debug(
                "FX: не удалось получить координаты для эффекта "
                f"(attacker={event.attacker_id}, target={event.target_id})."
            )
            return
        self._spawn_gauss_effect(start, end, event, config=config, fx_key=fx_key)

    def _spawn_gauss_effect(
        self,
        start: QtCore.QPointF,
        end: QtCore.QPointF,
        event: FxShotEvent,
        *,
        config: Optional[Dict] = None,
        fx_key: Optional[str] = None,
    ) -> None:
        t0 = time.monotonic()
        seed = hash((event.attacker_id, event.target_id, int(t0 * 1000))) & 0xFFFFFFFF
        if config is None:
            config = get_gun_fx_config(fx_key or "Gauss flayer")
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

    def _coerce_float(self, value: object) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    def _refresh_hp_snapshot(self) -> None:
        snap: Dict[Tuple[str, int], Tuple[Optional[float], Optional[float]]] = {}
        for (side, unit_id), unit in self._units_by_key.items():
            if side is None or unit_id is None or not isinstance(unit, dict):
                continue
            hp = self._coerce_float(unit.get("wounds", unit.get("hp")))
            hp_max = self._coerce_float(
                unit.get("max_wounds", unit.get("wounds_max", unit.get("max_hp", unit.get("hp"))))
            )
            snap[(str(side), int(unit_id))] = (hp, hp_max)
        self._hp_snapshot_by_unit = snap

    def _make_popup_key(self, event: FxShotEvent) -> str:
        if event.report_type == "heal" or event.outcome_type == "heal":
            return (
                f"heal|{event.ts}|{event.target_id}|{event.weapon_name}|{event.damage:.4f}"
            )
        return (
            f"{event.ts}|{event.report_type}|{event.attacker_id}|{event.target_id}|"
            f"{event.weapon_name}|{event.damage:.3f}|{event.outcome_type}|{event.failed_saves}"
        )

    def _popup_seen_recently(self, key: str, now_ts: float) -> bool:
        stale = []
        for known_key, ts in self._popup_seen.items():
            if (now_ts - ts) > self._popup_seen_ttl_s:
                stale.append(known_key)
        for stale_key in stale:
            self._popup_seen.pop(stale_key, None)
        if key in self._popup_seen:
            return True
        self._popup_seen[key] = now_ts
        if len(self._popup_seen) > self._popup_seen_max:
            self._popup_seen.popitem(last=False)
        return False

    def _emit_damage_popup(self, event: FxShotEvent) -> None:
        target_side = self._side_from_unit_id(event.target_id)
        if target_side is None:
            return
        popup_key = self._make_popup_key(event)
        now_ts = time.monotonic()
        if self._popup_seen_recently(popup_key, now_ts):
            return
        target_key = (target_side, int(event.target_id))
        hp_after = None
        hp_max = None
        unit = self._units_by_key.get(target_key)
        if isinstance(unit, dict):
            hp_after = self._coerce_float(unit.get("wounds", unit.get("hp")))
            hp_max = self._coerce_float(
                unit.get("max_wounds", unit.get("wounds_max", unit.get("max_hp", unit.get("hp"))))
            )
        prev_hp, prev_hp_max = self._hp_snapshot_by_unit.get(target_key, (None, None))
        if hp_max is None:
            hp_max = prev_hp_max

        hp_before = None
        is_heal = event.report_type == "heal" or event.outcome_type == "heal"
        if is_heal:
            if hp_after is not None and event.damage > 0:
                hp_before = hp_after - float(event.damage)
                if hp_max is not None:
                    hp_before = max(hp_before, 0.0)
            elif prev_hp is not None and hp_after is not None and hp_after > prev_hp:
                hp_before = prev_hp
            elif hp_after is not None:
                hp_before = max(0.0, hp_after - float(event.damage))
        elif hp_after is not None and event.damage > 0:
            hp_before = hp_after + float(event.damage)
            if hp_max is not None:
                hp_before = min(hp_before, hp_max)
        elif prev_hp is not None and hp_after is not None and prev_hp >= hp_after:
            hp_before = prev_hp
        elif hp_after is not None:
            hp_before = hp_after

        event.hp_before = hp_before
        event.hp_after = hp_after
        event.hp_max = hp_max
        event.popup_key = popup_key
        self.map_scene.add_damage_popup(
            kind=event.outcome_type,
            target_side=target_side,
            target_id=int(event.target_id),
            damage_value=float(event.damage),
            hp_before=hp_before,
            hp_after=hp_after,
            hp_max=hp_max,
            dedup_key=popup_key,
            created_ts=now_ts,
        )

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
                    self._cancel_shoot_sequence()
                    return True
                if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter) and self.viewer_controller.shootPopoverOpen:
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
                    self._last_command_text = ""
                    return True
            elif kind == "int":
                if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                    self._submit_answer(self._int_spin_value)
                    return True
            elif kind == "choice":
                if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                    self._submit_choice()
                    return True
            elif kind == "pace":
                if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter, QtCore.Qt.Key_Space):
                    self._submit_answer(True)
                    return True
        return super().eventFilter(obj, event)


def launch(state_path, model_path=None):
    # QQuickWidget + QOpenGLWidget: общий контекст OpenGL и десктопный GL на Windows.
    try:
        QtCore.QCoreApplication.setAttribute(
            QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts,
            True,
        )
        QtCore.QCoreApplication.setAttribute(
            QtCore.Qt.ApplicationAttribute.AA_UseDesktopOpenGL,
            True,
        )
    except Exception:
        pass

    def _viewer_qt_message_handler(mode, context, message):
        # Иначе Qt спамит это на каждый кадр при неверном композитинге.
        if "not compatible with QOpenGLWidget" in message:
            return
        print(message, file=sys.stderr, flush=True)

    try:
        QtCore.qInstallMessageHandler(_viewer_qt_message_handler)
    except Exception:
        pass

    app = QtWidgets.QApplication([])
    try:
        QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
    except Exception:
        pass
    window = ViewerWindow(state_path, model_path=model_path)
    window.setGeometry(0, 0, 2560, 1440)
    window.showMaximized()
    app.exec()
