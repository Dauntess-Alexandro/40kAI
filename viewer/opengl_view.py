"""OpenGL board renderer for the 40kAI viewer.

Viewer tech findings ("Играть в GUI"):
- gui_qt launches scripts/viewer.* which executes `python -m viewer`.
- The viewer is PySide6-based and previously used QGraphicsView/QGraphicsScene
  (viewer/app.py + viewer/scene.py). This file upgrades the board renderer to
  QOpenGLWidget while keeping the same state.json contract.
"""

from __future__ import annotations

from dataclasses import dataclass
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

        self._selected_unit_key: Optional[Tuple[str, int]] = None

        self._demo_unit_key: Optional[Tuple[str, int]] = None
        self._demo_phase: str = ""
        self._demo_color = Theme.selection
        self._demo_pulse_timer = QtCore.QTimer(self)
        self._demo_pulse_timer.setInterval(32)
        self._demo_pulse_timer.timeout.connect(self._animate_demo_pulse)
        self._demo_pulse_clock = QtCore.QElapsedTimer()
        self._demo_pulse_value = 0.0

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

        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

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

    def set_objective_radius_visible(self, visible: bool) -> None:
        self._show_objective_radius = bool(visible)
        self.update()

    def set_demo_focus(
        self,
        phase: Optional[str],
        side: Optional[str],
        unit_id: Optional[int],
    ) -> None:
        if side is None or unit_id is None:
            self._demo_unit_key = None
            self._demo_phase = ""
            if self._demo_pulse_timer.isActive():
                self._demo_pulse_timer.stop()
            self.update()
            return
        self._demo_unit_key = (side, unit_id)
        self._demo_phase = str(phase or "")
        self._demo_color = self._phase_color(self._demo_phase)
        self._demo_pulse_clock.restart()
        if not self._demo_pulse_timer.isActive():
            self._demo_pulse_timer.start()
        self.update()

    def refresh_overlays(self) -> None:
        self._move_highlights = []
        self._target_highlights = []
        active_key = (self._active_unit_side, self._active_unit_id)
        if not active_key[0] or active_key[1] is None:
            return
        unit = self._state_unit(active_key)
        if unit is None:
            return
        if self._should_show_movement():
            self._draw_movement_overlay(unit)
        if self._should_show_shooting():
            self._draw_target_overlay(unit)

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

    def _phase_color(self, phase: str) -> QtGui.QColor:
        phase_text = phase.lower()
        if "command" in phase_text or "команд" in phase_text:
            return Theme.demo_command
        if "move" in phase_text or "движ" in phase_text or "movement" in phase_text:
            return Theme.demo_move
        if "shoot" in phase_text or "стрел" in phase_text or "shooting" in phase_text:
            return Theme.demo_shoot
        if "charge" in phase_text or "чардж" in phase_text:
            return Theme.demo_charge
        if "fight" in phase_text or "битв" in phase_text or "ближн" in phase_text:
            return Theme.demo_fight
        return Theme.selection

    def _animate_demo_pulse(self) -> None:
        if not self._demo_pulse_clock.isValid():
            self._demo_pulse_clock.start()
        elapsed = self._demo_pulse_clock.elapsed()
        self._demo_pulse_value = (elapsed % 1200) / 1200.0
        self.update()

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
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            if self._drag_distance < 4:
                self._select_unit_at(event.position())
            self._dragging = False
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.key()
        if key == QtCore.Qt.Key_C:
            self.center_view()
            return
        if key == QtCore.Qt.Key_D:
            self._debug_overlay = not self._debug_overlay
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

        if self._move_highlights:
            highlight = QtGui.QColor(Theme.selection)
            highlight.setAlpha(80)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QBrush(highlight))
            for rect in self._move_highlights:
                painter.drawRect(rect)

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

        for render in self._units:
            painter.setBrush(Theme.brush(render.color))
            painter.setPen(Theme.pen(Theme.outline, 0.8))
            painter.drawEllipse(render.center, render.radius, render.radius)

        if self._demo_unit_key in self._unit_by_key:
            render = self._unit_by_key[self._demo_unit_key]
            pulse = 0.5 + 0.5 * QtCore.qSin(self._demo_pulse_value * 2 * 3.1415)
            demo_color = QtGui.QColor(self._demo_color)
            demo_color.setAlphaF(0.35 + 0.45 * pulse)
            pen = QtGui.QPen(demo_color)
            pen.setWidthF(2.0 + 1.2 * pulse)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(pen)
            painter.drawEllipse(render.center, render.radius + 4, render.radius + 4)

        if self._selected_unit_key in self._unit_by_key:
            render = self._unit_by_key[self._selected_unit_key]
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(Theme.pen(Theme.selection, 2))
            painter.drawEllipse(render.center, render.radius + 2, render.radius + 2)

        if self._target_highlights:
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(Theme.pen(Theme.accent, 2))
            for center, radius in self._target_highlights:
                painter.drawEllipse(center, radius, radius)

        text_font = Theme.font(size=8, bold=True)
        painter.setFont(text_font)
        painter.setPen(Theme.text)
        for label, pos in self._unit_labels:
            painter.drawText(pos, label)
        for label, pos in self._objective_labels:
            painter.drawText(pos, label)

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
