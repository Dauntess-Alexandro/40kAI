"""OpenGL board renderer for the 40kAI viewer.

Viewer tech findings ("Играть в GUI"):
- gui_qt launches scripts/viewer.* which executes `python -m viewer`.
- The viewer is PySide6-based and previously used QGraphicsView/QGraphicsScene
  (viewer/app.py + viewer/scene.py). This file upgrades the board renderer to
  QOpenGLWidget while keeping the same state.json contract.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import random
from time import monotonic, perf_counter
from typing import Dict, Iterable, List, Optional, Tuple

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from viewer.styles import Theme


@dataclass
class UnitRender:
    key: Tuple[str, int]
    center: QtCore.QPointF
    radius: float
    color: QtGui.QColor
    label: str


@dataclass
class ObjectiveRender:
    center: QtCore.QPointF
    radius: float
    color: QtGui.QColor
    label: str
    owner_color: QtGui.QColor
    control_radius: float


@dataclass
class DisintegrationParticle:
    offset: QtCore.QPointF
    velocity: QtCore.QPointF
    size_px: float
    life: float


@dataclass
class BranchBlueprint:
    u: float
    side_sign: float
    length_px: float
    bend_px: float
    phase: float
    width_px: float
    alpha: float
    period: float
    life: float
    fork: bool


@dataclass
class GlyphBlueprint:
    u: float
    offset_n_px: float
    glyph_id: int
    scale_px: float
    phase: float
    alpha: float
    drift_speed: float
    period: float
    life: float


@dataclass
class EdgeSpeckBlueprint:
    u0: float
    side_sign: float
    offset_px: float
    size_px: float
    alpha: float
    phase: float
    period: float
    life: float
    speed: float
    wobble_px: float


@dataclass
class GaussTracerEffect:
    start: QtCore.QPointF
    end: QtCore.QPointF
    t0: float
    duration: float
    seed: int
    particles: List[DisintegrationParticle]
    config: Dict
    branches: List[BranchBlueprint]
    glyphs: List[GlyphBlueprint]
    edge_specks: List[EdgeSpeckBlueprint]


class UnitTooltipWidget(QtWidgets.QFrame):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self._accent_color = Theme.accent
        self._pinned = False
        self._debug_mode = False
        self._target_pos = QtCore.QPoint()

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.setObjectName("unitTooltip")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.ToolTip, True)

        self._opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_anim = QtCore.QPropertyAnimation(self._opacity_effect, b"opacity", self)
        self._fade_anim.setDuration(160)
        self._fade_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        self._move_anim = QtCore.QPropertyAnimation(self, b"pos", self)
        self._move_anim.setDuration(160)
        self._move_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self._anim_group = QtCore.QParallelAnimationGroup(self)
        self._anim_group.addAnimation(self._fade_anim)
        self._anim_group.addAnimation(self._move_anim)

        self._icon_map = {
            "models": "👥",
            "wounds": "❤️",
            "weapon": "🔫",
            "range": "📏",
            "bs": "🎯",
            "cover": "🛡",
            "los": "👁",
            "mods": "✨",
            "pin": "📌",
            "debug": "🔧",
        }

        self._build_layout()
        self.hide()

    def _build_layout(self) -> None:
        self._marker = QtWidgets.QFrame(self)
        self._marker.setFixedSize(6, 22)
        self._marker.setObjectName("unitTooltipMarker")

        self._title_label = QtWidgets.QLabel(self)
        self._title_label.setFont(Theme.font(size=10, bold=True))
        self._title_label.setObjectName("unitTooltipTitle")

        self._meta_label = QtWidgets.QLabel(self)
        self._meta_label.setFont(Theme.font(size=8, bold=False))
        self._meta_label.setObjectName("unitTooltipMeta")

        self._status_label = QtWidgets.QLabel(self)
        self._status_label.setFont(Theme.font(size=8, bold=True))
        self._status_label.setObjectName("unitTooltipStatus")

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        header_layout.addWidget(self._marker)
        header_layout.addWidget(self._title_label, 1)
        header_layout.addWidget(self._status_label, 0, QtCore.Qt.AlignRight)
        header_layout.addWidget(self._meta_label, 0, QtCore.Qt.AlignRight)

        self._divider = QtWidgets.QFrame(self)
        self._divider.setFrameShape(QtWidgets.QFrame.HLine)
        self._divider.setFrameShadow(QtWidgets.QFrame.Plain)
        self._divider.setFixedHeight(1)
        self._divider.setObjectName("unitTooltipDivider")

        self._stats_grid = QtWidgets.QGridLayout()
        self._stats_grid.setContentsMargins(0, 0, 0, 0)
        self._stats_grid.setHorizontalSpacing(12)
        self._stats_grid.setVerticalSpacing(4)

        self._stat_widgets: Dict[str, QtWidgets.QWidget] = {}
        for key in ("models", "wounds", "weapon", "range", "bs", "cover", "los", "mods"):
            widget = self._build_stat_widget(key)
            self._stat_widgets[key] = widget

        self._stats_grid.addWidget(self._stat_widgets["models"], 0, 0)
        self._stats_grid.addWidget(self._stat_widgets["wounds"], 0, 1)
        self._stats_grid.addWidget(self._stat_widgets["weapon"], 1, 0)
        self._stats_grid.addWidget(self._stat_widgets["range"], 1, 1)
        self._stats_grid.addWidget(self._stat_widgets["bs"], 2, 0)
        self._stats_grid.addWidget(self._stat_widgets["cover"], 2, 1)
        self._stats_grid.addWidget(self._stat_widgets["los"], 3, 0)
        self._stats_grid.addWidget(self._stat_widgets["mods"], 3, 1)
        self._stats_grid.setColumnStretch(0, 1)
        self._stats_grid.setColumnStretch(1, 1)

        self._hp_bar = QtWidgets.QProgressBar(self)
        self._hp_bar.setRange(0, 1)
        self._hp_bar.setValue(0)
        self._hp_bar.setTextVisible(False)
        self._hp_bar.setFixedHeight(7)
        self._hp_bar.setObjectName("unitTooltipHpBar")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)
        layout.addLayout(header_layout)
        layout.addWidget(self._divider)
        layout.addLayout(self._stats_grid)
        layout.addWidget(self._hp_bar)
        self.setLayout(layout)

    def _build_stat_widget(self, key: str) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        icon = QtWidgets.QLabel(self._icon_map.get(key, ""), widget)
        icon.setFont(Theme.font(size=9, bold=False))
        icon.setObjectName("unitTooltipIcon")
        value = QtWidgets.QLabel("—", widget)
        value.setFont(Theme.font(size=9, bold=False))
        value.setObjectName("unitTooltipValue")
        layout.addWidget(icon)
        layout.addWidget(value, 1)
        widget.setLayout(layout)
        widget._icon_label = icon
        widget._value_label = value
        return widget

    def set_debug_mode(self, enabled: bool) -> None:
        self._debug_mode = enabled

    def set_pinned(self, pinned: bool) -> None:
        self._pinned = pinned

    def update_content(self, payload: Dict, accent: QtGui.QColor) -> None:
        self._accent_color = accent
        self._title_label.setText(payload.get("title", "Юнит"))
        unit_id = payload.get("unit_id", "—")
        self._meta_label.setText(f"Unit {unit_id}")

        status_bits: List[str] = []
        if self._pinned:
            status_bits.append(f"{self._icon_map['pin']} PIN")
        if self._debug_mode:
            status_bits.append(f"{self._icon_map['debug']} DBG")
        self._status_label.setText("  ".join(status_bits))

        self._set_stat_value("models", payload.get("models", "—"))
        self._set_stat_value("wounds", payload.get("wounds", "—"))
        self._set_stat_value("weapon", payload.get("weapon", "—"))
        self._set_stat_value("range", payload.get("range", "—"))
        self._set_stat_value("bs", payload.get("bs", "—"))
        self._set_stat_value("cover", payload.get("cover", "—"))
        self._set_stat_value("los", payload.get("los", "—"))
        self._set_stat_value("mods", payload.get("mods", "—"))

        wounds_value = payload.get("wounds_value")
        wounds_max = payload.get("wounds_max")
        if isinstance(wounds_value, (int, float)) and isinstance(wounds_max, (int, float)):
            self._hp_bar.setRange(0, max(1, int(wounds_max)))
            self._hp_bar.setValue(max(0, int(wounds_value)))
            self._hp_bar.show()
        else:
            self._hp_bar.hide()

        self._apply_styles()

    def _set_stat_value(self, key: str, value: object) -> None:
        widget = self._stat_widgets.get(key)
        if not widget:
            return
        text = "—" if value is None else str(value)
        widget._value_label.setText(text)

    def _apply_styles(self) -> None:
        accent = self._accent_color
        accent_rgba = f"rgba({accent.red()}, {accent.green()}, {accent.blue()}, 0.7)"
        bg_rgba = "rgba(20, 22, 20, 0.86)"
        self.setStyleSheet(
            """
            QFrame#unitTooltip {{
                background-color: {bg};
                border: 1px solid {accent};
                border-radius: 8px;
            }}
            QFrame#unitTooltipMarker {{
                background-color: {accent};
                border-radius: 3px;
            }}
            QLabel#unitTooltipTitle {{
                color: {text};
            }}
            QLabel#unitTooltipMeta {{
                color: {muted};
            }}
            QLabel#unitTooltipStatus {{
                color: {accent};
            }}
            QFrame#unitTooltipDivider {{
                background-color: {accent};
            }}
            QLabel#unitTooltipIcon {{
                color: {accent};
            }}
            QLabel#unitTooltipValue {{
                color: {text};
            }}
            QProgressBar#unitTooltipHpBar {{
                background: rgba(10, 12, 10, 0.6);
                border: 1px solid rgba(0, 0, 0, 0.3);
                border-radius: 4px;
            }}
            QProgressBar#unitTooltipHpBar::chunk {{
                background-color: {accent};
                border-radius: 4px;
            }}
            """.format(
                bg=bg_rgba,
                accent=accent_rgba,
                text=Theme.text.name(),
                muted=Theme.muted.name(),
            )
        )

    def show_at(self, target_pos: QtCore.QPoint, animate: bool = True) -> None:
        self._target_pos = target_pos
        if not animate:
            self.move(target_pos)
            self._opacity_effect.setOpacity(1.0)
            self.show()
            return
        start_pos = target_pos + QtCore.QPoint(0, 6)
        self._move_anim.stop()
        self._fade_anim.stop()
        self._anim_group.stop()
        try:
            self._anim_group.finished.disconnect(self.hide)
        except TypeError:
            pass
        self.move(start_pos)
        self.show()
        self._fade_anim.setStartValue(self._opacity_effect.opacity())
        self._fade_anim.setEndValue(1.0)
        self._move_anim.setStartValue(start_pos)
        self._move_anim.setEndValue(target_pos)
        self._anim_group.start()

    def hide_animated(self) -> None:
        if not self.isVisible():
            return
        self._fade_anim.stop()
        self._move_anim.stop()
        self._anim_group.stop()
        self._fade_anim.setStartValue(self._opacity_effect.opacity())
        self._fade_anim.setEndValue(0.0)
        self._move_anim.setStartValue(self.pos())
        self._move_anim.setEndValue(self.pos())
        try:
            self._anim_group.finished.disconnect(self.hide)
        except TypeError:
            pass
        self._anim_group.start()
        self._anim_group.finished.connect(self.hide)


class OpenGLBoardWidget(QOpenGLWidget):
    unit_selected = QtCore.Signal(str, int)

    def __init__(self, cell_size: int = 18, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.cell_size = cell_size
        self._state: Dict = {}
        self._board_width = 0
        self._board_height = 0
        self._board_rect = QtCore.QRectF()
        self._grid_picture: Optional[QtGui.QPicture] = None
        self._grid_size: Tuple[int, int] = (0, 0)

        self._units: List[UnitRender] = []
        self._unit_by_key: Dict[Tuple[str, int], UnitRender] = {}
        self._objectives: List[ObjectiveRender] = []
        self._unit_labels: List[Tuple[str, QtCore.QPointF]] = []
        self._objective_labels: List[Tuple[str, QtCore.QPointF]] = []
        self._units_state: List[dict] = []
        self._prev_unit_positions: Dict[Tuple[str, int], QtCore.QPointF] = {}
        self._curr_unit_positions: Dict[Tuple[str, int], QtCore.QPointF] = {}
        self._unit_anim_timer = QtCore.QTimer(self)
        self._unit_anim_timer.setInterval(16)
        self._unit_anim_timer.timeout.connect(self._animate_unit_step)
        self._unit_anim_clock = QtCore.QElapsedTimer()
        self._unit_anim_duration_ms = 180

        self._move_highlights: List[QtCore.QRectF] = []
        self._target_highlights: List[Tuple[QtCore.QPointF, float]] = []
        self._show_objective_radius = True

        self._active_unit_id = None
        self._active_unit_side = None
        self._phase = None
        self._move_range = None
        self._shoot_range = None
        self._targets = None
        self._layer_order = [
            "objectives",
            "units",
            "selection",
            "fx",
            "labels",
        ]

        self._selected_unit_key: Optional[Tuple[str, int]] = None
        self._fx_active: List[GaussTracerEffect] = []

        self._scale = 1.0
        self._min_scale = 0.2
        self._max_scale = 6.0
        self._pan = QtCore.QPointF(0, 0)
        self._target_scale = self._scale
        self._target_pan = QtCore.QPointF(0, 0)
        self._view_anim_timer = QtCore.QTimer(self)
        self._view_anim_timer.setInterval(16)
        self._view_anim_timer.timeout.connect(self._animate_view_step)
        self._dragging = False
        self._drag_start = QtCore.QPointF(0, 0)
        self._drag_distance = 0.0

        self._debug_overlay = False
        self._cursor_world: Optional[QtCore.QPointF] = None
        self._error_message: Optional[str] = None

        self._target_unit_id: Optional[int] = None
        self._target_cell: Optional[Tuple[int, int]] = None
        self._hover_cell: Optional[Tuple[int, int]] = None
        self._hover_unit_key: Optional[Tuple[str, int]] = None
        self._hover_tooltip_text: Optional[Dict] = None
        self._hover_tooltip_ts: float = 0.0
        self._hover_tooltip_interval_s = 1.0 / 30.0
        self._hover_candidate_key: Optional[Tuple[str, int]] = None
        self._hover_candidate_pos = QtCore.QPoint()
        self._hover_candidate_mods = QtCore.Qt.KeyboardModifiers()
        self._hover_timer = QtCore.QTimer(self)
        self._hover_timer.setSingleShot(True)
        self._hover_timer.setInterval(150)
        self._hover_timer.timeout.connect(self._show_hover_tooltip)
        self._tooltip_target_pos = QtCore.QPoint()
        self._tooltip_follow_timer = QtCore.QTimer(self)
        self._tooltip_follow_timer.setInterval(25)
        self._tooltip_follow_timer.timeout.connect(self._tick_tooltip_follow)
        self._tooltip_pinned = False
        self._tooltip_widget = UnitTooltipWidget(self)
        self._t0: Optional[float] = None
        self._fx_timer = QtCore.QTimer(self)
        self._fx_timer.setInterval(16)
        self._fx_timer.timeout.connect(self._tick_fx)
        self._fx_pixmaps: Dict[str, QtGui.QPixmap] = {}
        self._fx_tinted_cache: Dict[Tuple[str, int], QtGui.QPixmap] = {}
        self._fx_initialized = False

        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def initializeGL(self) -> None:
        super().initializeGL()
        self._t0 = perf_counter()
        self._load_fx_assets()
        if not self._fx_timer.isActive():
            self._fx_timer.start()

    def set_error_message(self, message: Optional[str]) -> None:
        self._error_message = message
        self.update()

    def update_state(self, state: Optional[Dict]) -> None:
        self._state = state or {}
        if not state:
            self.set_error_message(
                "Состояние игры недоступно. Где: viewer/state.json. "
                "Что делать дальше: запустите игру и дождитесь генерации state.json."
            )
            return
        self.set_error_message(None)
        self._clear_hover_tooltip(force=True)
        board = self._state.get("board", {})
        width = int(board.get("width") or 60)
        height = int(board.get("height") or 40)
        self._board_width = width
        self._board_height = height
        self._board_rect = QtCore.QRectF(0, 0, width * self.cell_size, height * self.cell_size)
        self._ensure_grid_cache(width, height)

        self._units_state = list(self._state.get("units", []) or [])
        self._prev_unit_positions = dict(self._curr_unit_positions)
        self._curr_unit_positions = {}
        for unit in self._units_state:
            key = (unit.get("side"), unit.get("id"))
            x = unit.get("x")
            y = unit.get("y")
            if key[0] is None or key[1] is None or x is None or y is None:
                continue
            self._curr_unit_positions[key] = QtCore.QPointF(float(x), float(y))

        for key, point in self._curr_unit_positions.items():
            self._prev_unit_positions.setdefault(key, QtCore.QPointF(point))

        self._start_unit_animation()

        self._objectives = []
        self._objective_labels = []
        for objective in self._state.get("objectives", []) or []:
            x = objective.get("x")
            y = objective.get("y")
            if x is None or y is None:
                continue
            radius = self.cell_size * 0.2
            center = QtCore.QPointF(
                x * self.cell_size + self.cell_size / 2,
                y * self.cell_size + self.cell_size / 2,
            )
            owner = objective.get("owner")
            owner_color = Theme.objective
            if owner == "player":
                owner_color = Theme.player
            elif owner == "model":
                owner_color = Theme.model
            render = ObjectiveRender(
                center=center,
                radius=radius,
                color=Theme.objective,
                label=str(objective.get("id", "")),
                owner_color=owner_color,
                control_radius=3 * self.cell_size,
            )
            self._objectives.append(render)
            self._objective_labels.append(
                (
                    render.label,
                    QtCore.QPointF(
                        center.x() + radius,
                        center.y() + radius,
                    ),
                )
            )

        self.refresh_overlays()
        self.update()

    def set_active_context(
        self,
        active_unit_id=None,
        active_unit_side=None,
        phase=None,
        move_range=None,
        shoot_range=None,
        show_objective_radius=True,
        targets=None,
    ) -> None:
        self._active_unit_id = active_unit_id
        self._active_unit_side = active_unit_side
        self._phase = phase or ""
        self._move_range = move_range
        self._shoot_range = shoot_range
        self._show_objective_radius = bool(show_objective_radius)
        self._targets = targets
        self.refresh_overlays()
        self.update()

    def build_gauss_effect(
        self,
        start: QtCore.QPointF,
        end: QtCore.QPointF,
        *,
        t0: float,
        duration: float,
        seed: int,
        config: Optional[Dict] = None,
    ) -> GaussTracerEffect:
        config = config or {}
        direction = end - start
        length_world = math.hypot(direction.x(), direction.y())
        particles = self._generate_gauss_particles(seed)
        branches = self._generate_gauss_branches(seed, length_world, config)
        glyphs = self._generate_gauss_glyphs(seed, config)
        edge_specks = self._generate_gauss_edge_specks(seed, config)
        return GaussTracerEffect(
            start=start,
            end=end,
            t0=t0,
            duration=duration,
            seed=seed,
            particles=particles,
            config=config,
            branches=branches,
            glyphs=glyphs,
            edge_specks=edge_specks,
        )

    def add_effect(self, effect: GaussTracerEffect) -> None:
        if effect is None:
            return
        self._fx_active.append(effect)
        self.update()

    def set_active_unit(self, unit_id: Optional[int]) -> None:
        self._active_unit_id = unit_id
        self._active_unit_side = None
        unit = self._find_unit_by_id(unit_id) if unit_id is not None else None
        if unit is not None:
            self._active_unit_side = unit.get("side")
        self.refresh_overlays()
        self.update()

    def set_target_unit(self, unit_id: Optional[int]) -> None:
        self._target_unit_id = unit_id
        self._target_cell = None
        self.update()

    def set_target_cell(self, cell: Optional[Tuple[int, int]]) -> None:
        self._target_cell = cell
        self._target_unit_id = None
        self.update()

    def set_hover_cell(self, cell: Optional[Tuple[int, int]]) -> None:
        self._hover_cell = cell
        self.update()

    def set_active_phase(self, phase: Optional[str]) -> None:
        self._phase = phase or ""
        self.refresh_overlays()
        self.update()

    def set_objective_radius_visible(self, visible: bool) -> None:
        self._show_objective_radius = bool(visible)
        self.update()

    def refresh_overlays(self) -> None:
        self._move_highlights = []
        self._target_highlights = []
        return

    def select_unit(self, side, unit_id) -> None:
        key = (side, unit_id)
        if key in self._unit_by_key:
            self._selected_unit_key = key
            self.update()

    def fit_to_view(self) -> None:
        if self._board_rect.isEmpty():
            return
        view_size = self.size()
        if view_size.width() <= 0 or view_size.height() <= 0:
            return
        scale_x = view_size.width() / self._board_rect.width()
        scale_y = view_size.height() / self._board_rect.height()
        self._scale = max(self._min_scale, min(self._max_scale, min(scale_x, scale_y) * 0.95))
        self._center_board()
        self._set_target_view(self._scale, self._pan, immediate=True)
        self.update()

    def center_view(self) -> None:
        self._center_board()
        self._set_target_view(self._scale, self._pan, immediate=True)
        self.update()

    def _center_board(self) -> None:
        if self._board_rect.isEmpty():
            return
        view_center = QtCore.QPointF(self.width() / 2, self.height() / 2)
        board_center = self._board_rect.center()
        self._pan = view_center - board_center * self._scale
        self._target_pan = QtCore.QPointF(self._pan)

    def _ensure_grid_cache(self, width: int, height: int) -> None:
        if self._grid_picture and self._grid_size == (width, height):
            return
        picture = QtGui.QPicture()
        painter = QtGui.QPainter(picture)
        pen = Theme.pen(Theme.grid, 0.5)
        pen.setCosmetic(True)
        painter.setPen(pen)
        for x in range(width + 1):
            x_pos = x * self.cell_size
            painter.drawLine(x_pos, 0, x_pos, height * self.cell_size)
        for y in range(height + 1):
            y_pos = y * self.cell_size
            painter.drawLine(0, y_pos, width * self.cell_size, y_pos)
        painter.end()
        self._grid_picture = picture
        self._grid_size = (width, height)

    def _draw_grid(self, painter: QtGui.QPainter) -> None:
        if self._board_rect.isEmpty() or self._scale <= 0:
            return
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
        pen = Theme.pen(Theme.grid, 1.0)
        pen.setCosmetic(True)
        painter.setPen(pen)

        pan_x, pan_y = self._snap_pan_to_pixels(self._pan)
        scale = self._scale
        cell = float(self.cell_size)
        width = self.width()
        height = self.height()
        board_screen_rect = QtCore.QRectF(
            pan_x,
            pan_y,
            self._board_width * cell * scale,
            self._board_height * cell * scale,
        )
        painter.setClipRect(board_screen_rect)
        left_world = (-pan_x) / scale
        right_world = (width - pan_x) / scale
        top_world = (-pan_y) / scale
        bottom_world = (height - pan_y) / scale

        min_col = max(0, int(left_world // cell))
        max_col = min(self._board_width, int(right_world // cell) + 1)
        min_row = max(0, int(top_world // cell))
        max_row = min(self._board_height, int(bottom_world // cell) + 1)

        ratio = self.devicePixelRatioF() or 1.0
        pixel = 1.0 / ratio

        for col in range(min_col, max_col + 1):
            world_x = col * cell
            screen_x = pan_x + world_x * scale
            screen_x = round(screen_x / pixel) * pixel
            painter.drawLine(
                QtCore.QPointF(screen_x, board_screen_rect.top()),
                QtCore.QPointF(screen_x, board_screen_rect.bottom()),
            )

        for row in range(min_row, max_row + 1):
            world_y = row * cell
            screen_y = pan_y + world_y * scale
            screen_y = round(screen_y / pixel) * pixel
            painter.drawLine(
                QtCore.QPointF(board_screen_rect.left(), screen_y),
                QtCore.QPointF(board_screen_rect.right(), screen_y),
            )

        painter.restore()

    def _start_unit_animation(self) -> None:
        self._unit_anim_clock.restart()
        if self._unit_anim_duration_ms <= 0:
            self._rebuild_units(1.0)
            if self._unit_anim_timer.isActive():
                self._unit_anim_timer.stop()
            self.refresh_overlays()
            self.update()
            return
        if not self._unit_anim_timer.isActive():
            self._unit_anim_timer.start()
        self._rebuild_units(0.0)
        self.refresh_overlays()
        self.update()

    def _animate_unit_step(self) -> None:
        if not self._unit_anim_clock.isValid():
            self._unit_anim_clock.start()
        elapsed = self._unit_anim_clock.elapsed()
        factor = min(1.0, elapsed / float(self._unit_anim_duration_ms))
        self._rebuild_units(factor)
        self.refresh_overlays()
        self.update()
        if factor >= 1.0 and self._unit_anim_timer.isActive():
            self._unit_anim_timer.stop()

    def _rebuild_units(self, factor: float) -> None:
        self._units = []
        self._unit_by_key = {}
        self._unit_labels = []

        occupied: Dict[Tuple[int, int], List[dict]] = {}
        for unit in self._units_state:
            key = (unit.get("side"), unit.get("id"))
            curr_pos = self._curr_unit_positions.get(key)
            if curr_pos is None:
                continue
            cell_key = (int(curr_pos.x()), int(curr_pos.y()))
            occupied.setdefault(cell_key, []).append(unit)

        for unit in self._units_state:
            key = (unit.get("side"), unit.get("id"))
            curr_pos = self._curr_unit_positions.get(key)
            if curr_pos is None:
                continue
            prev_pos = self._prev_unit_positions.get(key, curr_pos)
            interp_x = prev_pos.x() + (curr_pos.x() - prev_pos.x()) * factor
            interp_y = prev_pos.y() + (curr_pos.y() - prev_pos.y()) * factor

            stack = occupied.get((int(curr_pos.x()), int(curr_pos.y())), [])
            offset = 0.0
            if len(stack) > 1:
                offset = (stack.index(unit) - (len(stack) - 1) / 2) * (self.cell_size * 0.15)
            center_x = interp_x * self.cell_size + self.cell_size / 2 + offset
            center_y = interp_y * self.cell_size + self.cell_size / 2 - offset
            color = Theme.player if unit.get("side") == "player" else Theme.model
            radius = self.cell_size * 0.35
            render = UnitRender(
                key=key,
                center=QtCore.QPointF(center_x, center_y),
                radius=radius,
                color=color,
                label=str(unit.get("id", "")),
            )
            self._units.append(render)
            if key[0] is not None and key[1] is not None:
                self._unit_by_key[key] = render
            self._unit_labels.append(
                (render.label, QtCore.QPointF(center_x - radius, center_y - radius - 8))
            )

    def _state_unit(self, unit_key: Tuple[str, int]) -> Optional[dict]:
        units = self._state.get("units", []) or []
        for unit in units:
            if (unit.get("side"), unit.get("id")) == unit_key:
                return unit
        return None

    def _should_show_movement(self) -> bool:
        phase = str(self._phase or "").lower()
        return "move" in phase or "движ" in phase or "movement" in phase or self._move_range is not None

    def _should_show_shooting(self) -> bool:
        phase = str(self._phase or "").lower()
        return "shoot" in phase or "стрел" in phase or "shooting" in phase

    def _draw_movement_overlay(self, unit: dict) -> None:
        move_range = self._move_range
        if move_range is None:
            return
        x = unit.get("x")
        y = unit.get("y")
        if x is None or y is None:
            return
        for dx in range(-move_range, move_range + 1):
            for dy in range(-move_range, move_range + 1):
                if abs(dx) + abs(dy) > move_range:
                    continue
                cell_x = x + dx
                cell_y = y + dy
                if (
                    cell_x < 0
                    or cell_y < 0
                    or cell_x >= self._board_width
                    or cell_y >= self._board_height
                ):
                    continue
                rect = QtCore.QRectF(
                    cell_x * self.cell_size,
                    cell_y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                self._move_highlights.append(rect)

    def _draw_target_overlay(self, unit: dict) -> None:
        shoot_range = self._shoot_range
        if shoot_range is None:
            return
        source_x = unit.get("x")
        source_y = unit.get("y")
        if source_x is None or source_y is None:
            return
        target_keys = self._resolve_targets(unit, shoot_range)
        for key in target_keys:
            target = self._unit_by_key.get(key)
            if not target:
                continue
            radius = target.radius + self.cell_size * 0.1
            self._target_highlights.append((target.center, radius))

    def _resolve_targets(self, unit: dict, shoot_range: int) -> Iterable[Tuple[str, int]]:
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

    def _view_transform(self) -> QtGui.QTransform:
        transform = QtGui.QTransform()
        pan_x, pan_y = self._snap_pan_to_pixels(self._pan)
        transform.translate(pan_x, pan_y)
        transform.scale(self._scale, self._scale)
        return transform

    def _snap_pan_to_pixels(self, pan: QtCore.QPointF) -> Tuple[float, float]:
        ratio = self.devicePixelRatioF() or 1.0
        pixel = 1.0 / ratio
        snapped_x = round(pan.x() / pixel) * pixel
        snapped_y = round(pan.y() / pixel) * pixel
        return snapped_x, snapped_y

    def _set_target_view(
        self,
        scale: Optional[float] = None,
        pan: Optional[QtCore.QPointF] = None,
        *,
        immediate: bool = False,
    ) -> None:
        if scale is not None:
            self._target_scale = scale
        if pan is not None:
            self._target_pan = QtCore.QPointF(pan)
        if immediate:
            self._scale = self._target_scale
            self._pan = QtCore.QPointF(self._target_pan)
            if self._view_anim_timer.isActive():
                self._view_anim_timer.stop()
            return
        if not self._view_anim_timer.isActive():
            self._view_anim_timer.start()

    def _animate_view_step(self) -> None:
        smoothing = 0.2
        scale_delta = self._target_scale - self._scale
        pan_delta = self._target_pan - self._pan
        self._scale += scale_delta * smoothing
        self._pan += pan_delta * smoothing
        if (
            abs(scale_delta) < 0.001
            and abs(pan_delta.x()) < 0.1
            and abs(pan_delta.y()) < 0.1
        ):
            self._scale = self._target_scale
            self._pan = QtCore.QPointF(self._target_pan)
            self._view_anim_timer.stop()
        self.update()

    def _map_to_world(self, pos: QtCore.QPointF) -> QtCore.QPointF:
        transform = self._view_transform()
        inverted, ok = transform.inverted()
        if not ok:
            return QtCore.QPointF()
        return inverted.map(pos)

    def _snap_world_to_cell(self, world: QtCore.QPointF) -> QtCore.QPointF:
        if self._board_rect.isEmpty():
            return world
        col = int(world.x() // self.cell_size)
        row = int(world.y() // self.cell_size)
        col = max(0, min(self._board_width - 1, col))
        row = max(0, min(self._board_height - 1, row))
        return QtCore.QPointF(
            col * self.cell_size + self.cell_size / 2,
            row * self.cell_size + self.cell_size / 2,
        )

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self._board_rect.isEmpty():
            return
        delta = event.angleDelta().y()
        if delta == 0:
            return
        cursor = event.position()
        world_before = self._map_to_world(cursor)
        factor = 1.15 if delta > 0 else 1 / 1.15
        new_scale = self._scale * factor
        new_scale = max(self._min_scale, min(self._max_scale, new_scale))
        if new_scale == self._scale:
            return
        target_pan = cursor - world_before * new_scale
        self._set_target_view(new_scale, target_pan)
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self._dragging = True
            self._drag_start = QtCore.QPointF(event.position())
            self._drag_distance = 0.0
        if event.button() == QtCore.Qt.RightButton:
            world = self._map_to_world(QtCore.QPointF(event.position()))
            unit_key = self._unit_key_at_world(world)
            if unit_key:
                self._tooltip_pinned = not self._tooltip_pinned
                self._tooltip_widget.set_pinned(self._tooltip_pinned)
                if self._tooltip_pinned:
                    self._hover_candidate_key = unit_key
                    self._hover_candidate_pos = event.globalPosition().toPoint()
                    self._show_hover_tooltip()
                else:
                    self._clear_hover_tooltip(force=True)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        pos = QtCore.QPointF(event.position())
        if self._dragging:
            delta = pos - self._drag_start
            self._drag_distance = max(self._drag_distance, abs(delta.x()) + abs(delta.y()))
            self._set_target_view(pan=self._target_pan + delta)
            self._drag_start = pos
            self.update()
        world = self._map_to_world(pos)
        self._cursor_world = self._snap_world_to_cell(world)
        self._update_hover_cell(world)
        self._update_hover_tooltip(event, world)
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            if self._drag_distance < 4:
                self._select_unit_at(event.position())
            self._dragging = False
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self._hover_cell = None
        self._clear_hover_tooltip()
        self.update()
        super().leaveEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.key()
        if key == QtCore.Qt.Key_C:
            self.center_view()
            return
        if key == QtCore.Qt.Key_D:
            self._debug_overlay = not self._debug_overlay
            self._tooltip_widget.set_debug_mode(self._debug_overlay)
            self.update()
            return
        super().keyPressEvent(event)

    def _select_unit_at(self, pos: QtCore.QPointF) -> None:
        world = self._map_to_world(pos)
        closest_key = None
        closest_dist = None
        for render in self._units:
            dx = world.x() - render.center.x()
            dy = world.y() - render.center.y()
            distance = (dx * dx + dy * dy) ** 0.5
            if distance <= render.radius:
                if closest_dist is None or distance < closest_dist:
                    closest_dist = distance
                    closest_key = render.key
        if closest_key and closest_key != self._selected_unit_key:
            self._selected_unit_key = closest_key
            self.unit_selected.emit(closest_key[0], closest_key[1])
        self.update()

    def _clear_hover_tooltip(self, force: bool = False) -> None:
        if self._hover_timer.isActive():
            self._hover_timer.stop()
        if self._tooltip_pinned and not force:
            return
        if self._hover_unit_key is None and not self._hover_tooltip_text:
            return
        self._hover_unit_key = None
        self._hover_tooltip_text = None
        self._hover_candidate_key = None
        self._tooltip_widget.hide_animated()
        if self._tooltip_follow_timer.isActive():
            self._tooltip_follow_timer.stop()

    def paintGL(self) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHints(
            QtGui.QPainter.Antialiasing
            | QtGui.QPainter.TextAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
        )
        painter.fillRect(self.rect(), Theme.background)

        if self._error_message:
            painter.setPen(Theme.text)
            painter.drawText(
                self.rect(),
                QtCore.Qt.AlignCenter | QtCore.Qt.TextWordWrap,
                self._error_message,
            )
            painter.end()
            return

        self._draw_grid(painter)

        painter.setTransform(self._view_transform())
        for layer_name in self._layer_order:
            if layer_name == "movement":
                self._draw_movement_layer(painter)
            elif layer_name == "objectives":
                self._draw_objective_layer(painter)
            elif layer_name == "units":
                self._draw_units_layer(painter)
            elif layer_name == "selection":
                self._draw_selection_layer(painter)
            elif layer_name == "shooting":
                self._draw_shooting_layer(painter)
            elif layer_name == "fx":
                self._draw_fx_layer(painter)
            elif layer_name == "labels":
                self._draw_labels_layer(painter)

        painter.setTransform(QtGui.QTransform())
        if self._debug_overlay:
            debug_lines = ["DEBUG: (0,0) вверху слева"]
            if self._cursor_world is not None:
                col = int(self._cursor_world.x() // self.cell_size)
                row = int(self._cursor_world.y() // self.cell_size)
                debug_lines.append(f"Курсор: row={row}, col={col}")
            painter.setPen(Theme.text)
            painter.setFont(Theme.font(size=9, bold=False))
            painter.drawText(
                QtCore.QRectF(8, 8, self.width() - 16, 60),
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                "\n".join(debug_lines),
            )

        painter.end()

    def _draw_movement_layer(self, painter: QtGui.QPainter) -> None:
        if not self._move_highlights:
            return
        highlight = QtGui.QColor(Theme.selection)
        highlight.setAlpha(80)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(highlight))
        for rect in self._move_highlights:
            painter.drawRect(rect)

    def _draw_objective_layer(self, painter: QtGui.QPainter) -> None:
        for objective in self._objectives:
            painter.setBrush(Theme.brush(objective.color))
            painter.setPen(Theme.pen(Theme.outline, 0.8))
            painter.drawEllipse(objective.center, objective.radius, objective.radius)
            if self._show_objective_radius:
                control_pen = QtGui.QPen(objective.owner_color)
                control_pen.setWidthF(1.2)
                control_pen.setStyle(QtCore.Qt.DashLine)
                painter.setPen(control_pen)
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.drawEllipse(
                    objective.center,
                    objective.control_radius,
                    objective.control_radius,
                )

    def _draw_units_layer(self, painter: QtGui.QPainter) -> None:
        for render in self._units:
            painter.setBrush(Theme.brush(render.color))
            painter.setPen(Theme.pen(Theme.outline, 0.8))
            painter.drawEllipse(render.center, render.radius, render.radius)

    def _draw_selection_layer(self, painter: QtGui.QPainter) -> None:
        if self._selected_unit_key in self._unit_by_key:
            render = self._unit_by_key[self._selected_unit_key]
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(Theme.pen(Theme.selection, 2))
            painter.drawEllipse(render.center, render.radius + 2, render.radius + 2)

    def _draw_shooting_layer(self, painter: QtGui.QPainter) -> None:
        if not self._target_highlights:
            return
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(Theme.pen(Theme.accent, 2))
        for center, radius in self._target_highlights:
            painter.drawEllipse(center, radius, radius)

    def _draw_labels_layer(self, painter: QtGui.QPainter) -> None:
        text_font = Theme.font(size=8, bold=True)
        painter.setFont(text_font)
        painter.setPen(Theme.text)
        for label, pos in self._unit_labels:
            painter.drawText(pos, label)
        for label, pos in self._objective_labels:
            painter.drawText(pos, label)

    def _tick_fx(self) -> None:
        if self.isVisible():
            self.update()

    def _load_fx_assets(self) -> None:
        if self._fx_initialized:
            return
        assets_dir = Path(__file__).resolve().parent / "assets" / "fx"
        for name in ("glow_soft", "ring_soft", "tesseract_segments"):
            path = assets_dir / f"{name}.png"
            if not path.exists():
                continue
            image = QtGui.QImage(str(path))
            if image.isNull():
                continue
            pixmap = QtGui.QPixmap.fromImage(image)
            self._fx_pixmaps[name] = pixmap
        self._fx_initialized = True

    def _find_unit_by_id(self, unit_id: Optional[int]) -> Optional[dict]:
        if unit_id is None:
            return None
        for unit in self._state.get("units", []) or []:
            if unit.get("id") == unit_id:
                return unit
        return None

    def _unit_render_for_unit(self, unit: Optional[dict]) -> Optional[UnitRender]:
        if not unit:
            return None
        key = (unit.get("side"), unit.get("id"))
        return self._unit_by_key.get(key)

    def _is_necron(self, unit: Optional[dict]) -> bool:
        if not unit:
            return False
        faction = str(unit.get("faction") or "")
        name = str(unit.get("name") or "")
        return faction.lower() == "necrons" or "necron" in name.lower()

    def _fx_color_for_unit(self, unit: Optional[dict]) -> Tuple[QtGui.QColor, float]:
        if self._is_necron(unit):
            return QtGui.QColor(100, 255, 140), 1.0
        return QtGui.QColor(180, 220, 255), 0.35

    def _tinted_pixmap(self, name: str, color: QtGui.QColor) -> Optional[QtGui.QPixmap]:
        base = self._fx_pixmaps.get(name)
        if base is None:
            return None
        key = (name, color.rgba())
        cached = self._fx_tinted_cache.get(key)
        if cached is not None:
            return cached
        tinted = QtGui.QPixmap(base.size())
        tinted.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(tinted)
        painter.drawPixmap(0, 0, base)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(tinted.rect(), color)
        painter.end()
        self._fx_tinted_cache[key] = tinted
        return tinted

    def _draw_fx_layer(self, painter: QtGui.QPainter) -> None:
        self._draw_gauss_effects(painter)
        if not self._fx_pixmaps:
            return
        t = (perf_counter() - self._t0) if self._t0 is not None else 0.0
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t * 1.2)

        active_unit = self._find_unit_by_id(self._active_unit_id)
        active_render = self._unit_render_for_unit(active_unit)
        if active_render is None and self._selected_unit_key in self._unit_by_key:
            active_render = self._unit_by_key[self._selected_unit_key]
            active_unit = self._state_unit(self._selected_unit_key)
        if active_render:
            color, strength = self._fx_color_for_unit(active_unit)
            glow_pixmap = self._tinted_pixmap("glow_soft", color)
            ring_pixmap = self._tinted_pixmap("ring_soft", color)
            glow_alpha = 0.45 * (0.7 + 0.3 * pulse) * strength
            ring_alpha = 0.55 * (0.7 + 0.3 * pulse) * strength
            glow_size = active_render.radius * 4.2 * (0.95 + 0.08 * pulse)
            ring_size = active_render.radius * 3.6 * (0.95 + 0.08 * pulse)
            painter.save()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
            self._draw_fx_sprite(painter, glow_pixmap, active_render.center, glow_size, glow_alpha)
            painter.restore()
            painter.save()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            self._draw_fx_sprite(painter, ring_pixmap, active_render.center, ring_size, ring_alpha)
            painter.restore()

        target_unit = self._find_unit_by_id(self._target_unit_id)
        target_render = self._unit_render_for_unit(target_unit)
        target_center = None
        target_radius = None
        if target_render:
            target_center = target_render.center
            target_radius = target_render.radius
        elif self._target_cell is not None:
            target_center = self._cell_center(*self._target_cell)
            target_radius = self.cell_size * 0.4
        if target_center is not None and target_radius is not None:
            color, strength = self._fx_color_for_unit(target_unit)
            ring_pixmap = self._tinted_pixmap("ring_soft", color)
            seg_pixmap = self._tinted_pixmap("tesseract_segments", color)
            ring_alpha = 0.5 * (0.7 + 0.3 * pulse) * strength
            seg_alpha = 0.55 * (0.8 + 0.2 * pulse) * strength
            ring_size = target_radius * 4.4 * (0.95 + 0.08 * pulse)
            seg_size = target_radius * 5.0 * (0.98 + 0.05 * pulse)
            painter.save()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            self._draw_fx_sprite(painter, ring_pixmap, target_center, ring_size, ring_alpha)
            angle = math.degrees(t * 0.6)
            self._draw_fx_sprite(
                painter,
                seg_pixmap,
                target_center,
                seg_size,
                seg_alpha,
                rotation_deg=angle,
            )
            painter.restore()

        if self._hover_cell is not None:
            hover_center = self._cell_center(*self._hover_cell)
            hover_color = QtGui.QColor(200, 230, 255)
            hover_pixmap = self._tinted_pixmap("glow_soft", hover_color)
            hover_alpha = 0.25 * (0.8 + 0.2 * pulse)
            hover_size = self.cell_size * 2.2
            painter.save()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
            self._draw_fx_sprite(painter, hover_pixmap, hover_center, hover_size, hover_alpha)
            painter.restore()

    def _generate_gauss_particles(self, seed: int) -> List[DisintegrationParticle]:
        rng = random.Random(seed)
        particles: List[DisintegrationParticle] = []
        count = rng.randint(10, 25)
        for _ in range(count):
            angle = rng.uniform(0.0, math.tau)
            radius = self.cell_size * rng.uniform(0.05, 0.2)
            offset = QtCore.QPointF(math.cos(angle) * radius, math.sin(angle) * radius)
            vel_mag = self.cell_size * rng.uniform(0.6, 1.5)
            velocity = QtCore.QPointF(math.cos(angle) * vel_mag, math.sin(angle) * vel_mag)
            size_px = rng.uniform(2.0, 4.0)
            life = rng.uniform(0.25, 0.35)
            particles.append(
                DisintegrationParticle(
                    offset=offset,
                    velocity=velocity,
                    size_px=size_px,
                    life=life,
                )
            )
        return particles

    def _generate_gauss_branches(
        self,
        seed: int,
        length_world: float,
        config: Dict,
    ) -> List[BranchBlueprint]:
        rng = random.Random(seed + 11)
        branches_config = config.get("branches", {})
        count_min = int(branches_config.get("count_min", 10))
        count_max = int(branches_config.get("count_max", 18))
        length_cells = length_world / max(self.cell_size, 0.001)
        length_scale = max(0.75, min(1.35, length_cells / 7.0))
        base_count = rng.uniform(count_min, count_max)
        count = max(6, int(round(base_count * length_scale)))
        life_min = float(branches_config.get("life_min", 0.10))
        life_max = float(branches_config.get("life_max", 0.18))
        width_px = float(branches_config.get("width_px", 1.0))
        wide_width_px = float(branches_config.get("wide_width_px", 2.0))
        wide_chance = float(branches_config.get("wide_chance", 0.12))
        len_min_px = float(branches_config.get("len_min_px", 6.0))
        len_max_px = float(branches_config.get("len_max_px", 18.0))
        alpha_min = float(branches_config.get("alpha_min", 0.10))
        alpha_max = float(branches_config.get("alpha_max", 0.22))
        spawn_rate_min = float(branches_config.get("spawn_rate_min", 2.0))
        spawn_rate_max = float(branches_config.get("spawn_rate_max", 4.0))
        fork_chance = float(branches_config.get("fork_chance", 0.25))
        branches: List[BranchBlueprint] = []
        for _ in range(count):
            period = 1.0 / max(0.05, rng.uniform(spawn_rate_min, spawn_rate_max))
            branches.append(
                BranchBlueprint(
                    u=rng.uniform(0.06, 0.94),
                    side_sign=rng.choice((-1.0, 1.0)),
                    length_px=rng.uniform(len_min_px, len_max_px),
                    bend_px=rng.uniform(-1.5, 3.5),
                    phase=rng.uniform(0.0, 1.0),
                    width_px=wide_width_px if rng.random() < wide_chance else width_px,
                    alpha=rng.uniform(alpha_min, alpha_max),
                    period=period,
                    life=rng.uniform(life_min, life_max),
                    fork=rng.random() < fork_chance,
                )
            )
        return branches

    def _generate_gauss_glyphs(self, seed: int, config: Dict) -> List[GlyphBlueprint]:
        rng = random.Random(seed + 37)
        glyph_config = config.get("glyphs", {})
        count_min = int(glyph_config.get("count_min", 8))
        count_max = int(glyph_config.get("count_max", 14))
        alpha_min = float(glyph_config.get("alpha_min", 0.06))
        alpha_max = float(glyph_config.get("alpha_max", 0.14))
        scale_min_px = float(glyph_config.get("scale_min_px", 1.6))
        scale_max_px = float(glyph_config.get("scale_max_px", 3.0))
        offset_min_px = float(glyph_config.get("offset_n_min_px", -4.0))
        offset_max_px = float(glyph_config.get("offset_n_max_px", 4.0))
        drift_min = float(glyph_config.get("drift_speed_min", 0.10))
        drift_max = float(glyph_config.get("drift_speed_max", 0.25))
        life_min = float(glyph_config.get("life_min", 0.25))
        life_max = float(glyph_config.get("life_max", 0.45))
        period_min = float(glyph_config.get("period_min", 0.7))
        period_max = float(glyph_config.get("period_max", 1.4))
        glyph_count = rng.randint(count_min, count_max)
        glyphs: List[GlyphBlueprint] = []
        shape_count = len(self._gauss_glyph_shapes())
        for _ in range(glyph_count):
            glyphs.append(
                GlyphBlueprint(
                    u=rng.uniform(0.08, 0.92),
                    offset_n_px=rng.uniform(offset_min_px, offset_max_px),
                    glyph_id=rng.randrange(shape_count),
                    scale_px=rng.uniform(scale_min_px, scale_max_px),
                    phase=rng.uniform(0.0, 1.0),
                    alpha=rng.uniform(alpha_min, alpha_max),
                    drift_speed=rng.uniform(drift_min, drift_max),
                    period=rng.uniform(period_min, period_max),
                    life=rng.uniform(life_min, life_max),
                )
            )
        return glyphs

    def _generate_gauss_edge_specks(self, seed: int, config: Dict) -> List[EdgeSpeckBlueprint]:
        rng = random.Random(seed + 91)
        speck_config = config.get("edge_specks", {})
        count_min = int(speck_config.get("count_min", 60))
        count_max = int(speck_config.get("count_max", 120))
        life_min = float(speck_config.get("life_min", 0.16))
        life_max = float(speck_config.get("life_max", 0.26))
        size_min_px = float(speck_config.get("size_min_px", 1.0))
        size_max_px = float(speck_config.get("size_max_px", 3.0))
        alpha_min = float(speck_config.get("alpha_min", 0.08))
        alpha_max = float(speck_config.get("alpha_max", 0.18))
        offset_min_px = float(speck_config.get("offset_min_px", 2.0))
        offset_max_px = float(speck_config.get("offset_max_px", 6.0))
        speed_min = float(speck_config.get("speed_min", 0.6))
        speed_max = float(speck_config.get("speed_max", 1.8))
        wobble_min_px = float(speck_config.get("wobble_min_px", 0.5))
        wobble_max_px = float(speck_config.get("wobble_max_px", 1.5))
        period_min = float(speck_config.get("period_min", 0.35))
        period_max = float(speck_config.get("period_max", 0.6))
        count = rng.randint(count_min, count_max)
        specks: List[EdgeSpeckBlueprint] = []
        for _ in range(count):
            specks.append(
                EdgeSpeckBlueprint(
                    u0=rng.uniform(0.0, 1.0),
                    side_sign=rng.choice((-1.0, 1.0)),
                    offset_px=rng.uniform(offset_min_px, offset_max_px),
                    size_px=rng.uniform(size_min_px, size_max_px),
                    alpha=rng.uniform(alpha_min, alpha_max),
                    phase=rng.uniform(0.0, 1.0),
                    period=rng.uniform(period_min, period_max),
                    life=rng.uniform(life_min, life_max),
                    speed=rng.uniform(speed_min, speed_max),
                    wobble_px=rng.uniform(wobble_min_px, wobble_max_px),
                )
            )
        return specks

    def _window_fade(self, time_value: float, period: float, life: float) -> float:
        if period <= 0.0 or life <= 0.0:
            return 0.0
        t_mod = time_value % period
        if t_mod > life:
            return 0.0
        edge = min(life * 0.25, life * 0.5)
        if edge <= 0.0:
            return 1.0
        if t_mod < edge:
            return t_mod / edge
        if t_mod > life - edge:
            return max(0.0, (life - t_mod) / edge)
        return 1.0

    def _dim_color(self, color: QtGui.QColor, factor: float) -> QtGui.QColor:
        factor = max(0.0, min(1.0, factor))
        return QtGui.QColor(
            int(color.red() * factor),
            int(color.green() * factor),
            int(color.blue() * factor),
        )

    def _gauss_glyph_shapes(
        self,
    ) -> List[List[Tuple[QtCore.QPointF, QtCore.QPointF]]]:
        return [
            [
                (QtCore.QPointF(-0.6, -0.4), QtCore.QPointF(-0.6, 0.4)),
                (QtCore.QPointF(-0.6, -0.4), QtCore.QPointF(0.6, -0.4)),
                (QtCore.QPointF(-0.6, 0.4), QtCore.QPointF(0.3, 0.4)),
            ],
            [
                (QtCore.QPointF(-0.5, -0.5), QtCore.QPointF(0.5, -0.5)),
                (QtCore.QPointF(-0.5, -0.5), QtCore.QPointF(-0.5, 0.5)),
                (QtCore.QPointF(-0.2, 0.1), QtCore.QPointF(0.5, 0.1)),
            ],
            [
                (QtCore.QPointF(-0.5, -0.2), QtCore.QPointF(0.5, -0.2)),
                (QtCore.QPointF(0.0, -0.6), QtCore.QPointF(0.0, 0.6)),
                (QtCore.QPointF(-0.5, 0.2), QtCore.QPointF(0.5, 0.2)),
            ],
            [
                (QtCore.QPointF(-0.6, -0.3), QtCore.QPointF(-0.2, -0.3)),
                (QtCore.QPointF(0.2, 0.3), QtCore.QPointF(0.6, 0.3)),
                (QtCore.QPointF(-0.2, -0.3), QtCore.QPointF(0.2, 0.3)),
            ],
            [
                (QtCore.QPointF(-0.4, -0.4), QtCore.QPointF(0.4, -0.4)),
                (QtCore.QPointF(-0.4, 0.4), QtCore.QPointF(0.4, 0.4)),
                (QtCore.QPointF(-0.4, -0.4), QtCore.QPointF(-0.4, 0.4)),
                (QtCore.QPointF(0.4, -0.4), QtCore.QPointF(0.4, 0.4)),
            ],
            [
                (QtCore.QPointF(-0.5, 0.0), QtCore.QPointF(0.5, 0.0)),
                (QtCore.QPointF(0.0, -0.5), QtCore.QPointF(0.0, 0.5)),
                (QtCore.QPointF(-0.2, -0.2), QtCore.QPointF(0.2, 0.2)),
            ],
            [
                (QtCore.QPointF(-0.5, -0.1), QtCore.QPointF(-0.1, -0.5)),
                (QtCore.QPointF(-0.1, -0.5), QtCore.QPointF(0.5, -0.5)),
                (QtCore.QPointF(-0.1, -0.1), QtCore.QPointF(0.4, 0.4)),
            ],
            [
                (QtCore.QPointF(-0.4, -0.4), QtCore.QPointF(0.4, 0.0)),
                (QtCore.QPointF(-0.4, 0.4), QtCore.QPointF(0.4, 0.0)),
                (QtCore.QPointF(-0.1, -0.2), QtCore.QPointF(0.1, 0.2)),
            ],
        ]

    def _draw_gauss_effects(self, painter: QtGui.QPainter) -> None:
        if not self._fx_active:
            return
        now = monotonic()
        remaining: List[GaussTracerEffect] = []
        for fx in self._fx_active:
            age = now - fx.t0
            duration = max(0.001, fx.duration)
            progress = max(0.0, min(1.0, age / duration))
            if progress >= 1.0:
                continue
            remaining.append(fx)

            config = fx.config or {}

            def _resolve_life(value: Optional[float], default_fraction: float) -> float:
                if value is None:
                    value = default_fraction
                value = float(value)
                if value <= 1.0:
                    return max(0.001, duration * value)
                return value

            core_life = _resolve_life(config.get("core_life"), 0.22)
            glow_life = _resolve_life(config.get("glow_life"), 0.34)
            flash_life = _resolve_life(config.get("flash_life"), 0.14)
            ring_life = _resolve_life(config.get("ring_life"), 0.38)

            core_p = min(1.0, age / core_life)
            glow_p = min(1.0, age / glow_life)
            flash_p = min(1.0, age / flash_life)
            ring_p = min(1.0, age / ring_life)

            def ease_out(value: float) -> float:
                return (1.0 - value) ** 2

            glow_alpha = 0.55 * ease_out(glow_p)
            core_alpha = 0.85 * ease_out(core_p)
            flash_alpha = 0.9 * ease_out(flash_p)
            ring_alpha = 0.7 * ease_out(ring_p)

            glow_color = QtGui.QColor(*config.get("glow_color", (90, 255, 140)))
            core_color = QtGui.QColor(*config.get("core_color", (140, 255, 190)))
            impact_color = QtGui.QColor(*config.get("impact_color", (160, 255, 200)))

            glow_jitter_speed = float(config.get("glow_jitter_speed", 18.0))
            glow_jitter_px = float(config.get("glow_jitter_px", 2.0))
            glow_width_px = float(config.get("glow_width_px", 10.0))
            core_width_px = float(config.get("core_width_px", 2.0))
            core_gap_px = float(config.get("core_gap_px", 2.2))
            jitter = 0.6 + 0.4 * math.sin((age + fx.seed * 0.0001) * glow_jitter_speed)
            glow_width = self._px_to_world(glow_width_px + glow_jitter_px * jitter)
            core_width = self._px_to_world(core_width_px)
            core_gap = self._px_to_world(core_gap_px)
            direction = fx.end - fx.start
            length = math.hypot(direction.x(), direction.y())
            length = max(length, 0.001)
            dir_unit = QtCore.QPointF(direction.x() / length, direction.y() / length)
            normal_unit = QtCore.QPointF(-dir_unit.y(), dir_unit.x())

            # Порядок слоёв: glow tube -> core beam -> pulse -> edge specks/branches/glyphs
            # -> impact flash/ring -> disintegration pixels.
            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            glow_pen = QtGui.QPen(glow_color)
            glow_pen.setWidthF(glow_width)
            glow_pen.setCapStyle(QtCore.Qt.RoundCap)
            glow_pen.setJoinStyle(QtCore.Qt.RoundJoin)
            glow_pen.setColor(self._with_alpha(glow_color, glow_alpha))
            painter.setPen(glow_pen)
            painter.drawLine(fx.start, fx.end)
            painter.restore()

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            core_pen = QtGui.QPen(core_color)
            core_pen.setWidthF(core_width)
            core_pen.setCapStyle(QtCore.Qt.RoundCap)
            core_pen.setJoinStyle(QtCore.Qt.RoundJoin)
            core_pen.setColor(self._with_alpha(core_color, core_alpha))
            painter.setPen(core_pen)
            offset = QtCore.QPointF(normal_unit.x() * core_gap, normal_unit.y() * core_gap)
            painter.drawLine(fx.start + offset, fx.end + offset)
            painter.drawLine(fx.start - offset, fx.end - offset)
            painter.restore()

            pulse_color = QtGui.QColor(*config.get("pulse_color", (120, 255, 170)))
            pulse_len = self._px_to_world(float(config.get("pulse_len_px", 12.0)))
            pulse_gap = self._px_to_world(float(config.get("pulse_gap_px", 18.0)))
            pulse_count = max(1, int(length / pulse_gap))
            pulse_speed = float(config.get("pulse_speed", 0.9))
            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            pulse_alpha = float(config.get("pulse_alpha", 0.5))
            pulse_width_px = float(config.get("pulse_width_px", 3.0))
            pulse_pen = QtGui.QPen(self._with_alpha(pulse_color, pulse_alpha * glow_alpha))
            pulse_pen.setWidthF(self._px_to_world(pulse_width_px))
            pulse_pen.setCapStyle(QtCore.Qt.RoundCap)
            painter.setPen(pulse_pen)
            for idx in range(pulse_count):
                base = (idx / pulse_count + age * pulse_speed) % 1.0
                start_pos = fx.start + QtCore.QPointF(direction.x() * base, direction.y() * base)
                end_pos = fx.start + QtCore.QPointF(
                    direction.x() * min(1.0, base + pulse_len / max(length, 0.001)),
                    direction.y() * min(1.0, base + pulse_len / max(length, 0.001)),
                )
                painter.drawLine(start_pos, end_pos)
            painter.restore()

            glow_dim = self._dim_color(glow_color, 0.75)
            branch_dim = self._dim_color(core_color, 0.7)
            glyph_dim = self._dim_color(glow_color, 0.6)
            glow_half_px = glow_width_px * 0.5

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            painter.setPen(QtCore.Qt.NoPen)
            for speck in fx.edge_specks:
                fade = self._window_fade(age + speck.phase, speck.period, speck.life)
                if fade <= 0.0:
                    continue
                u = (speck.u0 + (age * speck.speed) / length) % 1.0
                base = QtCore.QPointF(
                    fx.start.x() + direction.x() * u,
                    fx.start.y() + direction.y() * u,
                )
                wobble = speck.wobble_px * math.sin((age + speck.phase) * math.tau * 1.1)
                offset_px = glow_half_px + speck.offset_px + wobble
                offset = QtCore.QPointF(
                    normal_unit.x() * self._px_to_world(offset_px) * speck.side_sign,
                    normal_unit.y() * self._px_to_world(offset_px) * speck.side_sign,
                )
                size_world = self._px_to_world(speck.size_px)
                intensity = 0.75 + 0.25 * math.sin((age + speck.phase) * math.tau * 1.7)
                alpha = speck.alpha * fade * intensity
                color = self._with_alpha(glow_dim, alpha)
                painter.setBrush(QtGui.QBrush(color))
                rect = QtCore.QRectF(
                    base.x() + offset.x() - size_world / 2,
                    base.y() + offset.y() - size_world / 2,
                    size_world,
                    size_world,
                )
                painter.drawRect(rect)
            painter.restore()

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            for branch in fx.branches:
                fade = self._window_fade(age + branch.phase, branch.period, branch.life)
                if fade <= 0.0:
                    continue
                anchor = QtCore.QPointF(
                    fx.start.x() + direction.x() * branch.u,
                    fx.start.y() + direction.y() * branch.u,
                )
                end_offset = QtCore.QPointF(
                    normal_unit.x() * self._px_to_world(branch.length_px) * branch.side_sign,
                    normal_unit.y() * self._px_to_world(branch.length_px) * branch.side_sign,
                )
                bend = QtCore.QPointF(
                    dir_unit.x() * self._px_to_world(branch.bend_px),
                    dir_unit.y() * self._px_to_world(branch.bend_px),
                )
                end_point = anchor + end_offset + bend
                alpha = branch.alpha * fade
                branch_pen = QtGui.QPen(self._with_alpha(branch_dim, alpha))
                branch_pen.setWidthF(self._px_to_world(branch.width_px))
                branch_pen.setCapStyle(QtCore.Qt.RoundCap)
                painter.setPen(branch_pen)
                painter.drawLine(anchor, end_point)
                if branch.fork:
                    fork_len = self._px_to_world(branch.length_px * 0.6)
                    fork_offset = QtCore.QPointF(
                        normal_unit.x() * fork_len * branch.side_sign * 0.6,
                        normal_unit.y() * fork_len * branch.side_sign * 0.6,
                    )
                    fork_point = anchor + fork_offset + bend
                    painter.drawLine(anchor, fork_point)
            painter.restore()

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            glyph_shapes = self._gauss_glyph_shapes()
            glyph_pen = QtGui.QPen()
            glyph_pen.setWidthF(self._px_to_world(1.0))
            glyph_pen.setCapStyle(QtCore.Qt.RoundCap)
            for glyph in fx.glyphs:
                fade = self._window_fade(age + glyph.phase, glyph.period, glyph.life)
                if fade <= 0.0:
                    continue
                u = (glyph.u + age * glyph.drift_speed) % 1.0
                base = QtCore.QPointF(
                    fx.start.x() + direction.x() * u,
                    fx.start.y() + direction.y() * u,
                )
                offset = QtCore.QPointF(
                    normal_unit.x() * self._px_to_world(glyph.offset_n_px),
                    normal_unit.y() * self._px_to_world(glyph.offset_n_px),
                )
                scale = self._px_to_world(glyph.scale_px)
                alpha = glyph.alpha * fade * (0.85 + 0.15 * math.sin((age + glyph.phase) * math.tau))
                glyph_pen.setColor(self._with_alpha(glyph_dim, alpha))
                painter.setPen(glyph_pen)
                for start_pt, end_pt in glyph_shapes[glyph.glyph_id]:
                    start_world = QtCore.QPointF(
                        base.x()
                        + offset.x()
                        + dir_unit.x() * start_pt.x() * scale
                        + normal_unit.x() * start_pt.y() * scale,
                        base.y()
                        + offset.y()
                        + dir_unit.y() * start_pt.x() * scale
                        + normal_unit.y() * start_pt.y() * scale,
                    )
                    end_world = QtCore.QPointF(
                        base.x()
                        + offset.x()
                        + dir_unit.x() * end_pt.x() * scale
                        + normal_unit.x() * end_pt.y() * scale,
                        base.y()
                        + offset.y()
                        + dir_unit.y() * end_pt.x() * scale
                        + normal_unit.y() * end_pt.y() * scale,
                    )
                    painter.drawLine(start_world, end_world)
            painter.restore()

            flash_radius = self.cell_size * (
                float(config.get("impact_flash_base", 0.08))
                + float(config.get("impact_flash_extra", 0.12)) * flash_p
            )
            ring_radius = self.cell_size * (
                float(config.get("impact_ring_base", 0.05))
                + float(config.get("impact_ring_extra", 0.3)) * ring_p
            )
            ring_width = self._px_to_world(float(config.get("impact_ring_width_px", 2.5)))

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QBrush(self._with_alpha(impact_color, flash_alpha)))
            painter.drawEllipse(fx.end, flash_radius, flash_radius)
            painter.restore()

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            ring_pen = QtGui.QPen(self._with_alpha(impact_color, ring_alpha))
            ring_pen.setWidthF(ring_width)
            painter.setPen(ring_pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawEllipse(fx.end, ring_radius, ring_radius)
            painter.restore()

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
            particle_color = QtGui.QColor(*config.get("particle_color", (140, 255, 180)))
            for particle in fx.particles:
                particle_age = age
                if particle_age >= particle.life:
                    continue
                particle_p = min(1.0, particle_age / particle.life)
                alpha = 0.7 * ease_out(particle_p)
                size_world = self._px_to_world(particle.size_px)
                velocity = QtCore.QPointF(
                    particle.velocity.x() * particle_age,
                    particle.velocity.y() * particle_age,
                )
                position = fx.end + particle.offset + velocity
                rect = QtCore.QRectF(
                    position.x() - size_world / 2,
                    position.y() - size_world / 2,
                    size_world,
                    size_world,
                )
                painter.setPen(QtCore.Qt.NoPen)
                painter.setBrush(QtGui.QBrush(self._with_alpha(particle_color, alpha)))
                painter.drawRect(rect)
            painter.restore()

        self._fx_active = remaining

    def _with_alpha(self, color: QtGui.QColor, alpha: float) -> QtGui.QColor:
        out = QtGui.QColor(color)
        out.setAlphaF(max(0.0, min(1.0, alpha)))
        return out

    def _px_to_world(self, px: float) -> float:
        scale = self._scale if self._scale > 0 else 1.0
        return px / scale

    def _draw_fx_sprite(
        self,
        painter: QtGui.QPainter,
        pixmap: Optional[QtGui.QPixmap],
        center: QtCore.QPointF,
        size: float,
        opacity: float,
        rotation_deg: float = 0.0,
    ) -> None:
        if pixmap is None or opacity <= 0 or size <= 0:
            return
        painter.save()
        painter.translate(center)
        if rotation_deg:
            painter.rotate(rotation_deg)
        painter.setOpacity(opacity)
        rect = QtCore.QRectF(-size / 2, -size / 2, size, size)
        source_rect = QtCore.QRectF(pixmap.rect())
        painter.drawPixmap(rect, pixmap, source_rect)
        painter.restore()

    def _cell_center(self, col: int, row: int) -> QtCore.QPointF:
        return QtCore.QPointF(
            col * self.cell_size + self.cell_size / 2,
            row * self.cell_size + self.cell_size / 2,
        )

    def _update_hover_cell(self, world: QtCore.QPointF) -> None:
        if self._board_rect.isEmpty():
            self._hover_cell = None
            return
        col = int(world.x() // self.cell_size)
        row = int(world.y() // self.cell_size)
        if col < 0 or row < 0 or col >= self._board_width or row >= self._board_height:
            self._hover_cell = None
            return
        self._hover_cell = (col, row)

    def _update_hover_tooltip(self, event: QtGui.QMouseEvent, world: QtCore.QPointF) -> None:
        if self._board_rect.isEmpty():
            self._clear_hover_tooltip()
            return
        unit_key = self._unit_key_at_world(world)
        if unit_key is None:
            self._clear_hover_tooltip()
            return
        if self._tooltip_pinned and self._hover_unit_key is not None:
            return
        now = monotonic()
        needs_refresh = unit_key != self._hover_unit_key
        if not needs_refresh and now - self._hover_tooltip_ts < self._hover_tooltip_interval_s:
            anchor = self._tooltip_anchor_for_cursor(event.globalPosition().toPoint())
            self._set_tooltip_target(anchor)
            return
        unit = self._state_unit(unit_key)
        if not unit:
            self._clear_hover_tooltip()
            return
        anchor = self._tooltip_anchor_for_cursor(event.globalPosition().toPoint())
        self._set_tooltip_target(anchor)
        if unit_key != self._hover_candidate_key:
            self._hover_candidate_key = unit_key
            self._hover_candidate_pos = event.globalPosition().toPoint()
            self._hover_candidate_mods = event.modifiers()
            self._hover_timer.start()
        elif self._hover_timer.isActive():
            self._hover_candidate_pos = event.globalPosition().toPoint()
            self._hover_candidate_mods = event.modifiers()
        if needs_refresh:
            tooltip_payload = self._build_unit_tooltip_payload(unit)
            if self._tooltip_widget.isVisible():
                self._hover_tooltip_text = tooltip_payload
                self._hover_unit_key = unit_key
                self._hover_tooltip_ts = now
                accent = self._unit_accent_color(unit)
                self._tooltip_widget.set_pinned(self._tooltip_pinned)
                self._tooltip_widget.set_debug_mode(self._debug_overlay)
                self._tooltip_widget.update_content(tooltip_payload, accent)

    def _unit_key_at_world(self, world: QtCore.QPointF) -> Optional[Tuple[str, int]]:
        if self._board_rect.isEmpty():
            return None
        col = int(world.x() // self.cell_size)
        row = int(world.y() // self.cell_size)
        if col < 0 or row < 0 or col >= self._board_width or row >= self._board_height:
            return None
        candidates = [
            unit
            for unit in self._units_state
            if int(unit.get("x", -1)) == col and int(unit.get("y", -1)) == row
        ]
        closest_key = None
        closest_dist = None
        for unit in candidates:
            key = (unit.get("side"), unit.get("id"))
            render = self._unit_by_key.get(key)
            if render is None:
                continue
            dx = world.x() - render.center.x()
            dy = world.y() - render.center.y()
            distance = (dx * dx + dy * dy) ** 0.5
            if closest_dist is None or distance < closest_dist:
                closest_dist = distance
                closest_key = key
        if closest_key:
            return closest_key
        closest_key = None
        closest_dist = None
        for render in self._units:
            dx = world.x() - render.center.x()
            dy = world.y() - render.center.y()
            distance = (dx * dx + dy * dy) ** 0.5
            if distance <= render.radius:
                if closest_dist is None or distance < closest_dist:
                    closest_dist = distance
                    closest_key = render.key
        return closest_key

    def _tooltip_anchor_for_unit(
        self,
        unit_key: Tuple[str, int],
        fallback_pos: QtCore.QPoint,
    ) -> QtCore.QPoint:
        render = self._unit_by_key.get(unit_key)
        if render is None:
            return fallback_pos
        screen_pos = self._view_transform().map(render.center)
        offset = QtCore.QPoint(12, -12)
        return self.mapToGlobal(QtCore.QPoint(int(screen_pos.x()), int(screen_pos.y()))) + offset

    def _tooltip_anchor_for_cursor(self, cursor_pos: QtCore.QPoint) -> QtCore.QPoint:
        offset = QtCore.QPoint(14, 18)
        return cursor_pos + offset

    def _build_unit_tooltip_payload(self, unit: dict) -> Dict:
        title = self._unit_display_name(unit)
        models = unit.get("models", "—")
        wounds_value = self._coerce_number(unit.get("wounds", unit.get("hp")))
        wounds_max = self._coerce_number(
            unit.get("max_wounds", unit.get("wounds_max", unit.get("wounds", unit.get("hp"))))
        )
        wounds_label = "—"
        if wounds_value is not None and wounds_max is not None:
            wounds_label = f"{int(wounds_value)}/{int(wounds_max)}"
        elif wounds_value is not None:
            wounds_label = str(int(wounds_value))
        cover = self._tooltip_cover_status(unit)
        weapon_name = self._tooltip_weapon_name(unit)
        unit_id = unit.get("id", "—")
        los = self._tooltip_los_status(unit)
        mods = self._tooltip_mods_status(unit)
        weapon_range = self._resolve_weapon_range(unit) or "—"
        bs = unit.get("bs") or unit.get("BS") or unit.get("ballistic_skill") or "—"
        return {
            "title": title,
            "unit_id": unit_id,
            "models": models,
            "wounds": wounds_label,
            "wounds_value": wounds_value,
            "wounds_max": wounds_max,
            "weapon": weapon_name,
            "range": weapon_range,
            "bs": bs,
            "cover": cover,
            "los": los,
            "mods": mods,
        }

    def _coerce_number(self, value: object) -> Optional[float]:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return None
        return None

    def _unit_accent_color(self, unit: dict) -> QtGui.QColor:
        army = str(unit.get("army") or unit.get("faction") or "").lower()
        side = str(unit.get("side") or "").lower()
        if "necron" in army or "некрон" in army:
            return QtGui.QColor("#6fbf7a")
        if side == "player":
            return Theme.player
        if side == "model":
            return Theme.model
        return Theme.accent

    def _position_tooltip(self, anchor: QtCore.QPoint, animate: bool = True) -> None:
        if not self._tooltip_widget:
            return
        widget = self._tooltip_widget
        widget.adjustSize()
        pos = self._clamp_tooltip_pos(anchor, widget.size())
        self._tooltip_target_pos = pos
        widget.show_at(pos, animate=animate)
        if not self._tooltip_follow_timer.isActive():
            self._tooltip_follow_timer.start()

    def _clamp_tooltip_pos(self, anchor: QtCore.QPoint, size: QtCore.QSize) -> QtCore.QPoint:
        padding = 12
        pos = QtCore.QPoint(anchor)
        screen = self.screen() or self.window().screen()
        available = screen.availableGeometry() if screen else self.rect()
        if pos.x() + size.width() + padding > available.right():
            pos.setX(pos.x() - size.width() - padding)
        if pos.y() + size.height() + padding > available.bottom():
            pos.setY(pos.y() - size.height() - padding)
        if pos.x() < padding:
            pos.setX(padding)
        if pos.y() < padding:
            pos.setY(padding)
        return pos

    def _refresh_tooltip_anchor(self) -> None:
        if self._hover_unit_key is None:
            return
        unit = self._state_unit(self._hover_unit_key)
        if not unit:
            self._clear_hover_tooltip(force=True)
            return
        anchor = self._tooltip_anchor_for_unit(self._hover_unit_key, self.mapToGlobal(QtCore.QPoint(0, 0)))
        accent = self._unit_accent_color(unit)
        payload = self._build_unit_tooltip_payload(unit)
        self._tooltip_widget.update_content(payload, accent)
        self._position_tooltip(anchor)

    def _set_tooltip_target(self, anchor: QtCore.QPoint) -> None:
        if not self._tooltip_widget:
            return
        self._tooltip_widget.adjustSize()
        self._tooltip_target_pos = self._clamp_tooltip_pos(anchor, self._tooltip_widget.size())
        if not self._tooltip_follow_timer.isActive() and self._tooltip_widget.isVisible():
            self._tooltip_follow_timer.start()

    def _tick_tooltip_follow(self) -> None:
        widget = self._tooltip_widget
        if not widget.isVisible():
            self._tooltip_follow_timer.stop()
            return
        if self._tooltip_pinned and self._hover_unit_key is not None:
            anchor = self._tooltip_anchor_for_unit(
                self._hover_unit_key,
                self.mapToGlobal(QtCore.QPoint(0, 0)),
            )
            self._set_tooltip_target(anchor)
        current = widget.pos()
        target = self._tooltip_target_pos
        dx = target.x() - current.x()
        dy = target.y() - current.y()
        if abs(dx) < 1 and abs(dy) < 1:
            widget.move(target)
            return
        step = 0.35
        next_pos = QtCore.QPoint(
            int(current.x() + dx * step),
            int(current.y() + dy * step),
        )
        widget.move(next_pos)

    def _show_hover_tooltip(self) -> None:
        if not self._hover_candidate_key:
            return
        unit = self._state_unit(self._hover_candidate_key)
        if not unit:
            self._clear_hover_tooltip()
            return
        if self._hover_candidate_mods & (QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier):
            self._tooltip_pinned = True
        self._tooltip_widget.set_pinned(self._tooltip_pinned)
        self._tooltip_widget.set_debug_mode(self._debug_overlay)
        tooltip_payload = self._build_unit_tooltip_payload(unit)
        self._hover_tooltip_text = tooltip_payload
        self._hover_unit_key = self._hover_candidate_key
        self._hover_tooltip_ts = monotonic()
        accent = self._unit_accent_color(unit)
        self._tooltip_widget.update_content(tooltip_payload, accent)
        if self._tooltip_pinned:
            anchor = self._tooltip_anchor_for_unit(self._hover_unit_key, self._hover_candidate_pos)
        else:
            anchor = self._tooltip_anchor_for_cursor(self._hover_candidate_pos)
        self._position_tooltip(anchor, animate=True)

    def _unit_display_name(self, unit: dict) -> str:
        name = str(unit.get("name") or "").strip()
        unit_type = str(unit.get("type") or unit.get("unit_type") or "").strip()
        if name and unit_type and unit_type.lower() not in name.lower():
            return f"{name} ({unit_type})"
        if name:
            return name
        if unit_type:
            return unit_type
        return "Юнит"

    def _tooltip_cover_status(self, unit: dict) -> str:
        return "—"

    def _tooltip_weapon_name(self, unit: dict) -> str:
        weapon_name = unit.get("weapon_name") or unit.get("weapon") or unit.get("weapons")
        if isinstance(weapon_name, list):
            weapon_name = ", ".join(map(str, weapon_name))
        return weapon_name or "—"

    def _resolve_weapon_range(self, unit: dict) -> Optional[int]:
        for key in ("range", "weapon_range", "shoot_range", "shooting_range"):
            value = unit.get(key)
            if value is not None:
                return value
        return None

    def _tooltip_los_status(self, unit: dict) -> str:
        return "—"

    def _tooltip_mods_status(self, unit: dict) -> str:
        return "—"
