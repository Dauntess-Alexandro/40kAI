"""OpenGL board renderer for the 40kAI viewer.

Viewer tech findings ("Играть в GUI"):
- gui_qt launches scripts/viewer.* which executes `python -m viewer`.
- The viewer is PySide6-based and previously used QGraphicsView/QGraphicsScene
  (viewer/app.py + viewer/scene.py). This file upgrades the board renderer to
  QOpenGLWidget while keeping the same state.json contract.
"""

from __future__ import annotations

from dataclasses import dataclass
import copy
import json
import math
import os
from pathlib import Path
from project_paths import AGENT_PLAY_LOG_PATH, CORE_DIR
import random
from time import monotonic, perf_counter
from typing import Any, Dict, Iterable, List, Optional, Tuple

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from app.viewer.styles import Theme
from app.viewer.config import load_viewer_config, viewer_flag
from app.viewer.cells_fx import (
    SHOOTING_RAPID_HATCH_STYLE,
    rapid_hatch_pen,
)
from app.viewer.tooltip import TerrainTooltipWidget, UnitTooltipWidget

GL_BLEND = 0x0BE2
GL_SRC_ALPHA = 0x0302
GL_ONE_MINUS_SRC_ALPHA = 0x0303
ENV_BOARD_WIDTH = 60
ENV_BOARD_HEIGHT = 40


def resolve_asset_path(rel_path: str) -> Path:
    return Path(__file__).resolve().parent / "assets" / rel_path


@dataclass
class UnitRender:
    key: Tuple[str, int]
    center: QtCore.QPointF
    radius: float
    color: QtGui.QColor
    label: str
    icon: Optional[QtGui.QPixmap] = None
    model_centers: Optional[List[QtCore.QPointF]] = None
    facing: str = "right"


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


@dataclass
class ScorchDecalFx:
    center: QtCore.QPointF
    created_t: float
    ttl_s: float
    size_cells: float
    rotation_deg: float
    alpha: float


@dataclass
class DecalInstance:
    texture_key: str
    center: QtCore.QPointF
    rotation_deg: float
    scale: float


@dataclass
class DeployPlacementFlash:
    cells: List[Tuple[int, int]]
    t0: float
    duration: float


@dataclass
class PropInstance:
    kind: str
    center: QtCore.QPointF
    rotation_deg: float
    scale: float
    debug_rect: Optional[QtCore.QRectF] = None
    sprite_name: str = ""
    draw_rect: Optional[QtCore.QRectF] = None


@dataclass
class ParticleInstance:
    texture_key: str
    position: QtCore.QPointF
    velocity: QtCore.QPointF
    life: float
    age: float
    size_px: float
    alpha: float
    mode: str


@dataclass
class SquadStatusSnapshot:
    hp: Optional[float]
    hp_max: Optional[float]
    alive_models: Optional[int]
    total_models: Optional[int]


@dataclass
class DamagePopup:
    kind: str
    target_key: Tuple[str, int]
    text_main: str
    created_t: float
    ttl_s: float
    rise_px: float
    dedup_key: str
    stack_index: int = 0
    amount: float = 0.0
    damage_hits: int = 1
    hp_before: Optional[float] = None
    hp_after: Optional[float] = None
    hp_max: Optional[float] = None
    seed: int = 0


@dataclass
class _StatusLayout:
    center_x: float
    top_y: float
    bar_w: float
    bar_h: float
    pips_y: float


class TextureManager:
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._pixmaps: Dict[str, QtGui.QPixmap] = {}

    def load_png(self, rel_path: str) -> Optional[QtGui.QPixmap]:
        if rel_path in self._pixmaps:
            return self._pixmaps[rel_path]
        path = self._base_dir / rel_path
        if not path.exists():
            return None
        image = QtGui.QImage(str(path))
        if image.isNull():
            return None
        pixmap = QtGui.QPixmap.fromImage(image)
        self._pixmaps[rel_path] = pixmap
        return pixmap

class OpenGLBoardWidget(QOpenGLWidget):
    unit_selected = QtCore.Signal(str, int)
    unit_right_clicked = QtCore.Signal(str, int, object)
    cell_clicked = QtCore.Signal(int, int)
    cell_right_clicked = QtCore.Signal(int, int)
    cell_hovered = QtCore.Signal(object)
    shoot_overlay_mode_changed = QtCore.Signal(str)

    def __init__(
        self,
        cell_size: int = 24,
        unit_icon_scale: float = 2.75,
        model_icon_scale: float = 0.75,
        terrain_barrel_cell_scale: float = 0.92,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent)
        self.cell_size = cell_size
        _vw_cfg = load_viewer_config()
        self._layers_v2 = viewer_flag("viewer.render.layers_v2", _vw_cfg)
        self._viewer_debug_overlay_flag = viewer_flag("viewer.debug.overlay", _vw_cfg)
        self._fx_v2 = viewer_flag("viewer.fx.v2", _vw_cfg)
        self._viewer_cfg_snapshot: Dict[str, Any] = dict(_vw_cfg)
        self._fx_tune_base: Optional[Dict[str, float]] = None
        q0 = str(os.environ.get("VIEWER_FX_QUALITY", "") or _vw_cfg.get("fx_quality") or "medium").strip().lower()
        self._fx_quality_resolved = q0 if q0 in {"low", "medium", "high"} else "medium"
        self._fx_gauss_alpha_scale = 1.0
        self._paint_serial = 0
        self._last_click_screen: Optional[QtCore.QPointF] = None
        self._perf_last_mono: Optional[float] = None
        self._perf_frame_ms: List[float] = []
        self._perf_frames_since_report = 0
        self._state: Dict = {}
        self._board_width = 0
        self._board_height = 0
        self._state_board_width: Optional[int] = None
        self._state_board_height: Optional[int] = None
        self._swap_axes = False
        self._rotate90 = False
        self._board_debug_logged = False
        self._board_rect = QtCore.QRectF()
        self._grid_picture: Optional[QtGui.QPicture] = None
        self._grid_size: Tuple[int, int] = (0, 0)

        self._units: List[UnitRender] = []
        self._unit_by_key: Dict[Tuple[str, int], UnitRender] = {}
        self._objectives: List[ObjectiveRender] = []
        self._unit_labels: List[Tuple[str, QtCore.QPointF]] = []
        self._unit_hitboxes_screen: Dict[Tuple[str, int], QtCore.QRectF] = {}
        self._last_hover_hitbox_debug_sig: Optional[Tuple[object, int, int, int, int]] = None
        self._objective_labels: List[Tuple[str, QtCore.QPointF]] = []
        self._units_state: List[dict] = []
        self._unit_state_by_key: Dict[Tuple[str, int], dict] = {}
        self._prev_unit_positions: Dict[Tuple[str, int], QtCore.QPointF] = {}
        self._curr_unit_positions: Dict[Tuple[str, int], QtCore.QPointF] = {}
        self._prev_model_cells_by_key: Dict[Tuple[str, int], List[Tuple[float, float]]] = {}
        self._curr_model_cells_by_key: Dict[Tuple[str, int], List[Tuple[float, float]]] = {}
        self._unit_anim_timer = QtCore.QTimer(self)
        self._unit_anim_timer.setInterval(16)
        self._unit_anim_timer.timeout.connect(self._animate_unit_step)
        self._unit_anim_clock = QtCore.QElapsedTimer()
        self._unit_anim_duration_ms = 180
        self._move_base_ms = 155.0
        self._move_per_cell_ms = 88.0
        self._move_cap_ms = 920.0
        self._move_seq_floor_new_step_ms = 260.0
        self._move_seq_floor_default_ms = 180.0
        self._move_ease = "smoothstep"
        self._status_prev: Dict[Tuple[str, int], SquadStatusSnapshot] = {}
        self._status_curr: Dict[Tuple[str, int], SquadStatusSnapshot] = {}
        self._status_anim_t0: float = monotonic()
        self._status_anim_duration_s: float = 0.28
        self._status_hp_fast_duration_s: float = 0.14
        self._status_hp_lag_duration_s: float = 0.26
        self._status_hp_loss_min_px: float = 2.0
        self._status_hp_coalesce_window_s: float = 0.11
        self._status_hp_hit_flash_s: float = 0.09
        self._status_pip_step_s: float = 0.055
        self._status_offset_y_cells: float = 0.34

        self._status_hp_crit_threshold: float = 0.30
        self._status_crit_pulse_period_s: float = 0.95

        self._status_hp_bg_color = QtGui.QColor(24, 28, 24, 214)
        self._status_hp_backplate_color = QtGui.QColor(10, 12, 13, 180)
        self._status_hp_lag_color = QtGui.QColor(226, 214, 186, 124)
        self._status_hp_overheal_color = QtGui.QColor(114, 154, 186, 208)
        self._status_hp_border_color = QtGui.QColor(18, 22, 22, 235)
        self._status_hp_border_crit_color = QtGui.QColor(177, 90, 82, 220)
        self._status_hp_text_bg = QtGui.QColor(8, 10, 12, 166)
        self._status_hp_text_color = QtGui.QColor(220, 226, 220, 242)

        self._status_pip_alive_color = QtGui.QColor(154, 177, 139, 222)
        self._status_pip_lost_color = QtGui.QColor(93, 106, 123, 176)
        self._status_pip_flash_color = QtGui.QColor(220, 205, 166, 235)

        self._status_hp_lag_from_ratio: Dict[Tuple[str, int], float] = {}
        self._status_hp_lag_to_ratio: Dict[Tuple[str, int], float] = {}
        self._status_hp_lag_t0: Dict[Tuple[str, int], float] = {}
        self._status_hp_last_drop_t: Dict[Tuple[str, int], float] = {}
        self._status_hp_hit_mag: Dict[Tuple[str, int], float] = {}

        self._move_highlights: List[QtCore.QRectF] = []
        self._reachable_highlights: List[QtCore.QRectF] = []
        self._reachable_cells_set: set[tuple[int, int]] = set()
        self._move_reachable_highlights: List[QtCore.QRectF] = []
        self._advance_reachable_highlights: List[QtCore.QRectF] = []
        self._move_cells_set: set[tuple[int, int]] = set()
        self._advance_cells_set: set[tuple[int, int]] = set()
        self._reachable_overlay_sig: Optional[Tuple[object, int, int]] = None
        self._target_highlights: List[Tuple[QtCore.QPointF, float]] = []
        self._shoot_range_highlights: List[QtCore.QRectF] = []
        self._shoot_rapid_range_highlights: List[QtCore.QRectF] = []
        self._shoot_target_infos: List[Dict[str, object]] = []
        self._shoot_hovered_target_key: Optional[Tuple[str, int]] = None
        self._last_shoot_hover_debug_sig: Optional[Tuple[int, str]] = None
        self._last_shoot_overlay_debug_sig: Optional[Tuple[object, ...]] = None
        self._last_shoot_overlay_cells_debug_sig: Optional[Tuple[object, ...]] = None
        self._show_shoot_range_cells = False
        self._show_objective_radius = True

        self._active_unit_id = None
        self._active_unit_side = None
        self._selected_unit_id = None
        self._selected_unit_side = None
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
        self._ai_activation_key: Optional[Tuple[str, int]] = None
        self._ai_activation_meta: Dict[str, Any] = {}
        self._last_viewer_step_seq: Optional[int] = None
        self._last_ai_follow_sig: Optional[Tuple[Optional[Tuple[str, int]], int]] = None
        self._last_user_camera_ts: float = 0.0
        self._view_pulse_timer = QtCore.QTimer(self)
        self._view_pulse_timer.setSingleShot(True)
        self._view_pulse_timer.timeout.connect(self._finish_ai_zoom_pulse)
        self._ai_pulse_base_scale: Optional[float] = None
        self._ai_ring_anim_timer = QtCore.QTimer(self)
        self._ai_ring_anim_timer.setInterval(33)
        self._ai_ring_anim_timer.timeout.connect(self.update)
        self._fx_active: List[GaussTracerEffect] = []
        self._fx_scorch_decals: List[ScorchDecalFx] = []
        self._fx_scorch_max_active = 96
        self._damage_popups_active: List[DamagePopup] = []
        self._damage_popup_dedup_seen: Dict[str, float] = {}
        self._damage_popup_ttl_s = 0.95
        self._damage_popup_rise_min_px = 14.0
        self._damage_popup_rise_max_px = 36.0
        # Зазор над верхним краем спрайта (якорь уже на «линии макушки»: центр модели минус половина иконки).
        self._damage_popup_anchor_lift_cells = 0.34
        self._damage_popup_font_size = 11
        self._damage_popup_outline_px = 2.2
        self._damage_popup_coalesce_window_s = 0.16
        self._damage_popup_max_active = 96
        self._damage_popup_hit_stop_s = 0.032
        self._damage_popup_hit_stop_until: float = 0.0
        self._damage_popup_lod_font_shrink_scale = 0.55
        self._damage_popup_sfx_warned = False
        self._damage_popup_sfx_cache: Dict[str, Any] = {}
        self._damage_grad_damage_a = QtGui.QColor(255, 210, 130, 255)
        self._damage_grad_damage_b = QtGui.QColor(220, 72, 68, 255)
        self._damage_grad_save_a = QtGui.QColor(120, 235, 220, 255)
        self._damage_grad_save_b = QtGui.QColor(38, 88, 190, 255)
        self._damage_grad_heal_a = QtGui.QColor(186, 255, 205, 255)
        self._damage_grad_heal_b = QtGui.QColor(58, 200, 118, 255)
        self._damage_grad_miss_a = QtGui.QColor(188, 192, 206, 255)
        self._damage_grad_miss_b = QtGui.QColor(168, 150, 198, 255)
        self._damage_popup_badge_border = QtGui.QColor(255, 255, 255, 55)
        self._damage_popup_text_shadow = QtGui.QColor(6, 8, 10, 230)
        # Оттенок многослойного свечения вокруг глифов (не чистый чёрный — меньше «жирного» контура).
        self._damage_popup_glow_damage = QtGui.QColor(52, 16, 12)
        self._damage_popup_glow_save = QtGui.QColor(10, 28, 40)
        self._damage_popup_glow_heal = QtGui.QColor(14, 48, 26)
        self._damage_popup_glow_miss = QtGui.QColor(28, 22, 38)

        self._scale = 1.0
        self._min_scale = 0.2
        self._max_scale = 6.0
        self._fit_padding = 0.96
        self._unit_icon_scale = max(0.25, float(unit_icon_scale))
        self._model_icon_scale = max(0.2, float(model_icon_scale))
        self._terrain_barrel_cell_scale = max(0.1, min(1.0, float(terrain_barrel_cell_scale)))
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
        self._deploy_ghost_cells: List[Tuple[int, int]] = []
        self._deploy_ghost_valid: Optional[bool] = None
        self._deploy_ghost_unit_name: str = ""
        self._deploy_ghost_alpha_valid = 0.55
        self._deploy_ghost_alpha_invalid = 0.40
        self._deploy_preview_units: List[UnitRender] = []
        self._deploy_preview_unit_keys: set[Tuple[str, int]] = set()
        self._deploy_placement_fx: List[DeployPlacementFlash] = []
        self._deploy_snap_duration_s = 0.22
        self._hover_unit_key: Optional[Tuple[str, int]] = None
        self._hover_tooltip_text: Optional[Dict] = None
        self._hover_tooltip_ts: float = 0.0
        self._hover_tooltip_interval_s = 1.0 / 30.0
        self._hover_candidate_key: Optional[Tuple[str, int]] = None
        self._hover_candidate_pos = QtCore.QPoint()
        self._hover_candidate_mods = QtCore.Qt.KeyboardModifiers()
        self._tooltip_target_pos = QtCore.QPoint()
        self._tooltip_follow_timer = QtCore.QTimer(self)
        self._tooltip_follow_timer.setInterval(25)
        self._tooltip_follow_timer.timeout.connect(self._tick_tooltip_follow)
        self._tooltip_pinned = False
        self._tooltip_widget = UnitTooltipWidget(self)
        self._tooltip_widget.weapon_hovered.connect(self._on_tooltip_weapon_hovered)
        self._tooltip_widget.weapon_hover_left.connect(self._on_tooltip_weapon_hover_left)
        self._tooltip_widget.copy_stats_requested.connect(self._on_tooltip_copy_stats_requested)
        self._tooltip_widget.status_chip_hovered.connect(self._on_status_chip_hovered)
        self._tooltip_widget.status_chip_left.connect(self._on_status_chip_left)
        self._terrain_tooltip_widget = TerrainTooltipWidget(self)
        self._viewer_debug_enabled = str(os.getenv("VIEWER_DEBUG", "0")).strip() == "1"
        self._hover_terrain_feature: Optional[dict] = None
        self._hover_weapon_range: Optional[int] = None
        self._hover_status_enemy_ids: List[int] = []
        self._visibility_lists_cache: Dict[Tuple[object, object, object], Dict[str, List[int]]] = {}
        self._last_terrain_hover_debug_sig: Optional[Tuple[int, int, str]] = None
        self._unit_data = self._load_unit_data()
        self._unit_data_by_name = self._index_unit_data(self._unit_data)
        self._weapon_data = self._load_weapon_data()
        self._weapon_data_by_name = self._index_weapon_data(self._weapon_data)
        self._t0: Optional[float] = None
        self._fx_timer = QtCore.QTimer(self)
        self._fx_timer.setInterval(16)
        self._fx_timer.timeout.connect(self._tick_fx)
        self._fx_pixmaps: Dict[str, QtGui.QPixmap] = {}
        self._fx_tinted_cache: Dict[Tuple[str, int], QtGui.QPixmap] = {}
        self._fx_initialized = False

        assets_root = resolve_asset_path("")
        self._texture_manager = TextureManager(assets_root)
        self._unit_icon_by_name = self._build_unit_icon_map()
        self._faction_icon_by_keyword = self._build_faction_icon_map()
        self._ground_textures: List[QtGui.QPixmap] = []
        self._prop_textures: Dict[str, QtGui.QPixmap] = {}
        self._shadow_textures: Dict[str, QtGui.QPixmap] = {}
        self._decal_textures: Dict[str, QtGui.QPixmap] = {}
        self._fx_particle_textures: Dict[str, QtGui.QPixmap] = {}
        self._target_overlay_pixmaps: Dict[str, Optional[QtGui.QPixmap]] = {}
        self._log_move_overlay_persistent: Optional[Dict[str, object]] = None
        self._log_move_overlay_hover: Optional[Dict[str, object]] = None
        self._rapid_hatch_brush_cache: Optional[QtGui.QBrush] = None
        self._decals: List[DecalInstance] = []
        self._props: List[PropInstance] = []
        self._terrain_features_state: List[dict] = []
        self._terrain_cell_index: Dict[Tuple[int, int], dict] = {}
        self._terrain_log_signature: Optional[tuple] = None
        self._terrain_props_signature: Optional[tuple] = None
        self._terrain_sprite_log_cache: set[str] = set()
        self._terrain_texture_cache: Dict[str, QtGui.QPixmap] = {}
        self._terrain_source_rect_cache: Dict[str, QtCore.QRectF] = {}
        self._particles: List[ParticleInstance] = []
        self._particles_last_ts: Optional[float] = None
        self._props_initialized = False
        self._props_seed = 613
        self._props_board_size: Tuple[int, int] = (0, 0)
        self.render_terrain = True
        self.render_decals = False
        self.render_prop_shadows = False
        self.render_fx = True
        self._cursor_world_raw: Optional[QtCore.QPointF] = None

        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def initializeGL(self) -> None:
        super().initializeGL()
        self._t0 = perf_counter()
        self._setup_gl_blend()
        self._load_environment_assets()
        self._load_fx_assets()
        if not self._fx_timer.isActive():
            self._fx_timer.start()

    def _setup_gl_blend(self) -> None:
        context = self.context()
        if context is None:
            return
        functions = context.functions()
        if functions is None:
            return
        functions.glEnable(GL_BLEND)
        functions.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _load_environment_assets(self) -> None:
        self._ground_textures = []
        for name in ("ground/ground_01.png", "ground/ground_02.png"):
            pixmap = self._texture_manager.load_png(name)
            if pixmap is not None:
                self._ground_textures.append(pixmap)

        self._prop_textures.clear()
        self._shadow_textures.clear()
        self._decal_textures.clear()

        terrain_dir = self._texture_manager._base_dir / "props" / "terrain"
        if terrain_dir.exists():
            for path in sorted(terrain_dir.glob("*.png")):
                pixmap = self._texture_manager.load_png(f"props/terrain/{path.name}")
                if pixmap is not None:
                    self._prop_textures[path.name] = pixmap

        self._fx_particle_textures.clear()
        fx_dir = self._texture_manager._base_dir / "fx"
        if fx_dir.exists():
            for path in fx_dir.glob("*.png"):
                pixmap = self._texture_manager.load_png(f"fx/{path.name}")
                if pixmap is not None:
                    self._fx_particle_textures[path.stem] = pixmap

    def set_error_message(self, message: Optional[str]) -> None:
        self._error_message = message
        self.update()

    def reset_runtime_visuals(self, *, clear_units: bool = True, clear_state: bool = False) -> None:
        """Clear transient render/session caches without touching camera pan/zoom."""
        if clear_state:
            self._state = {}
        if clear_units:
            self._units_state = []
            self._units = []
            self._unit_by_key = {}
            self._unit_state_by_key = {}
            self._unit_labels = []
            self._unit_hitboxes_screen = {}
            self._prev_unit_positions = {}
            self._curr_unit_positions = {}
            self._prev_model_cells_by_key = {}
            self._curr_model_cells_by_key = {}
            self._status_prev = {}
            self._status_curr = {}
            self._selected_unit_key = None
            self._active_unit_id = None
            self._active_unit_side = None
            self._selected_unit_id = None
            self._selected_unit_side = None
            self._ai_activation_key = None
            self._ai_activation_meta = {}
            self._last_ai_follow_sig = None
            self._last_viewer_step_seq = None
            self._ai_ring_anim_timer.stop()
        self._target_unit_id = None
        self._target_cell = None
        self._hover_cell = None
        self._deploy_ghost_cells = []
        self._deploy_ghost_valid = None
        self._deploy_ghost_unit_name = ""
        self._deploy_preview_units = []
        self._deploy_preview_unit_keys = set()
        self._deploy_placement_fx = []
        self._move_highlights = []
        self._target_highlights = []
        self._objectives = []
        self._objective_labels = []
        self._fx_active = []
        self._damage_popups_active = []
        self._damage_popup_dedup_seen = {}
        self._damage_popup_hit_stop_until = 0.0
        self._particles = []
        self._particles_last_ts = None
        self._unit_anim_timer.stop()
        self._view_anim_timer.stop()
        self._clear_hover_tooltip(force=True)
        self.update()

    def update_state(self, state: Optional[Dict]) -> None:
        self._state = state or {}
        self._visibility_lists_cache = {}
        if not state:
            self.set_error_message(
                "Состояние игры недоступно. Где: viewer/state.json. "
                "Что делать дальше: запустите игру и дождитесь генерации state.json."
            )
            return
        self.set_error_message(None)
        board = self._state.get("board", {})
        raw_units = list(self._state.get("units", []) or [])

        filtered_units = []
        for unit in raw_units:
            if not isinstance(unit, dict):
                continue
            hp_value = self._safe_int(unit.get("hp"))
            alive_models_value = self._safe_int(unit.get("alive_models"))
            if hp_value is not None and hp_value <= 0:
                continue
            if alive_models_value is not None and alive_models_value <= 0:
                continue
            filtered_units.append(unit)

        width, height = self._resolve_board_dims(board, raw_units)
        self._board_width = width
        self._board_height = height
        self._board_rect = QtCore.QRectF(0, 0, width * self.cell_size, height * self.cell_size)
        self._ensure_grid_cache(width, height)
        self._terrain_features_state = self._parse_terrain_features(self._state.get("terrain_features", []) or [])
        self._terrain_cell_index = self._build_terrain_cell_index(self._terrain_features_state)
        self._log_terrain_features_once()
        if self.render_terrain:
            terrain_sig = tuple(
                (
                    feature["kind"],
                    feature["sprite"],
                    tuple(feature["cells"]),
                    tuple(feature.get("cell_rotations") or []),
                )
                for feature in self._terrain_features_state
            )
            if terrain_sig != self._terrain_props_signature:
                self._terrain_props_signature = terrain_sig
                self._props_initialized = False
            if (width, height) != self._props_board_size:
                self._props_board_size = (width, height)
                self._props_initialized = False
            self._ensure_props()

        self._units_state = filtered_units
        self._unit_state_by_key = {}
        for unit in self._units_state:
            key_side = unit.get("side")
            key_id = unit.get("id")
            if key_side is None or key_id is None:
                continue
            self._unit_state_by_key[(str(key_side), int(key_id))] = unit

        prev_status = dict(self._status_curr)
        self._status_prev = prev_status
        self._status_curr = {}
        for key, unit in self._unit_state_by_key.items():
            snapshot = self._extract_squad_status(unit)
            self._status_curr[key] = snapshot
            if key not in self._status_prev:
                self._status_prev[key] = snapshot
        self._status_prev = {
            key: value
            for key, value in self._status_prev.items()
            if key in self._status_curr
        }
        now = monotonic()
        self._refresh_hp_loss_anim(now)
        self._status_anim_t0 = now

        live_keys = set()
        for u in self._units_state:
            nk = self._norm_unit_key(u.get("side"), u.get("id"))
            if nk is not None:
                live_keys.add(nk)
        if self._deploy_preview_units:
            self._deploy_preview_units = [
                render for render in self._deploy_preview_units
                if render.key not in live_keys
            ]
            self._deploy_preview_unit_keys = {render.key for render in self._deploy_preview_units}

        self._curr_unit_positions = self._normalize_unit_key_dict(self._curr_unit_positions)
        self._prev_unit_positions = self._normalize_unit_key_dict(self._prev_unit_positions)
        self._curr_model_cells_by_key = self._normalize_unit_key_dict(self._curr_model_cells_by_key)
        self._prev_model_cells_by_key = self._normalize_unit_key_dict(self._prev_model_cells_by_key)

        next_curr_positions: Dict[Tuple[str, int], QtCore.QPointF] = {}
        for unit in self._units_state:
            key = self._norm_unit_key(unit.get("side"), unit.get("id"))
            if key is None:
                continue
            view_cell = self._unit_anchor_view_cell(unit)
            if view_cell is None:
                continue
            view_x, view_y = view_cell
            next_curr_positions[key] = QtCore.QPointF(float(view_x), float(view_y))

        next_model_cells: Dict[Tuple[str, int], List[Tuple[float, float]]] = {}
        for unit in self._units_state:
            key = self._norm_unit_key(unit.get("side"), unit.get("id"))
            if key is None:
                continue
            raw_cells = self._unit_model_view_cells(unit)
            if raw_cells:
                next_model_cells[key] = [(float(x), float(y)) for x, y in raw_cells]
            else:
                anchor = self._unit_anchor_view_cell(unit)
                if anchor is not None:
                    next_model_cells[key] = [(float(anchor[0]), float(anchor[1]))]

        prior_curr_positions = dict(self._curr_unit_positions)
        movement_requires_anim = self._movement_requires_walk_anim(next_curr_positions, prior_curr_positions)

        vinfo = state.get("viewer") if isinstance(state.get("viewer"), dict) else {}
        self._parse_viewer_activation_vinfo(vinfo)
        if self._ai_activation_key or self._ai_activation_meta:
            if not self._ai_ring_anim_timer.isActive():
                self._ai_ring_anim_timer.start()
        else:
            self._ai_ring_anim_timer.stop()
        seq = vinfo.get("step_seq")
        prev_seq = getattr(self, "_last_viewer_step_seq", None)
        if isinstance(seq, int):
            self._last_viewer_step_seq = seq

        if movement_requires_anim:
            self._prev_unit_positions = dict(prior_curr_positions)
            self._curr_unit_positions = dict(next_curr_positions)
            for key, point in self._curr_unit_positions.items():
                if key not in prior_curr_positions:
                    sx, sy = float(point.x()), float(point.y())
                    if sx >= 0.75:
                        self._prev_unit_positions[key] = QtCore.QPointF(sx - 1.0, sy)
                    elif sy >= 0.75:
                        self._prev_unit_positions[key] = QtCore.QPointF(sx, sy - 1.0)
                    else:
                        self._prev_unit_positions[key] = QtCore.QPointF(
                            min(sx + 1.0, float(max(0, self._board_width - 1))), sy
                        )
                else:
                    self._prev_unit_positions.setdefault(key, QtCore.QPointF(point))

            self._prev_model_cells_by_key = copy.deepcopy(self._curr_model_cells_by_key)
            self._curr_model_cells_by_key = {}
            for key, cells in next_model_cells.items():
                self._curr_model_cells_by_key[key] = list(cells)
            for key in list(self._curr_model_cells_by_key.keys()):
                self._prev_model_cells_by_key.setdefault(key, list(self._curr_model_cells_by_key[key]))

            max_m = 0
            for key, curr_pt in self._curr_unit_positions.items():
                prev_pt = self._prev_unit_positions.get(key)
                if prev_pt is None:
                    continue
                dm = abs(curr_pt.x() - prev_pt.x()) + abs(curr_pt.y() - prev_pt.y())
                max_m = max(max_m, int(round(dm)))
            base_ms = float(self._move_base_ms)
            per_cell_ms = float(self._move_per_cell_ms)
            cap_ms = float(self._move_cap_ms)
            dist_ms = min(cap_ms, base_ms + per_cell_ms * max(0, max_m - 1)) if max_m > 0 else 0
            seq_floor = (
                float(self._move_seq_floor_new_step_ms)
                if (isinstance(seq, int) and (prev_seq is None or seq > prev_seq))
                else float(self._move_seq_floor_default_ms)
            )
            if max_m <= 0:
                self._unit_anim_duration_ms = 0
            else:
                self._unit_anim_duration_ms = max(dist_ms, seq_floor)
            self._start_unit_animation()
        else:
            self._curr_unit_positions = dict(next_curr_positions)
            self._curr_model_cells_by_key = {k: list(v) for k, v in next_model_cells.items()}
            if not self._unit_anim_timer.isActive():
                self._rebuild_units(1.0)

        self._objectives = []
        self._objective_labels = []
        for objective in (self._state.get("objectives", []) or [])[:1]:
            view_cell = self._state_to_view_cell(objective.get("x"), objective.get("y"))
            if view_cell is None:
                continue
            view_x, view_y = view_cell
            radius = self.cell_size * 0.2
            center = QtCore.QPointF(
                view_x * self.cell_size + self.cell_size / 2,
                view_y * self.cell_size + self.cell_size / 2,
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
        self._maybe_follow_ai_camera(vinfo, seq)

        if self._hover_unit_key is not None:
            if self._state_unit(self._hover_unit_key) is not None:
                self._refresh_tooltip_anchor()
            else:
                self._clear_hover_tooltip(force=True)

        self.update()

    @staticmethod
    def _safe_int(value: object) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _norm_unit_key(side: object, uid: object) -> Optional[Tuple[str, int]]:
        if side is None or uid is None:
            return None
        try:
            iid = int(uid)
        except (TypeError, ValueError):
            return None
        return (str(side), iid)

    def _normalize_unit_key_dict(self, data: Optional[Dict[Tuple, Any]]) -> Dict[Tuple[str, int], Any]:
        out: Dict[Tuple[str, int], Any] = {}
        for k, v in (data or {}).items():
            if not isinstance(k, tuple) or len(k) != 2:
                continue
            nk = self._norm_unit_key(k[0], k[1])
            if nk is not None:
                out[nk] = v
        return out

    def _movement_requires_walk_anim(
        self,
        next_pos: Dict[Tuple[str, int], QtCore.QPointF],
        prior_curr: Dict[Tuple[str, int], QtCore.QPointF],
    ) -> bool:
        """Новый кадр перемещения по полю: сменилась клетка якоря или впервые появился юнит. Без эвристик овервотча."""
        for k, p in next_pos.items():
            old = prior_curr.get(k)
            if old is None:
                return True
            ox, oy = int(round(old.x())), int(round(old.y()))
            nx, ny = int(round(p.x())), int(round(p.y()))
            if ox != nx or oy != ny:
                return True
        return False

    def state_pos_to_xy(self, pos: object) -> Optional[Tuple[int, int]]:
        """Map env/grid position (row, col) to view (x, y)."""
        if not isinstance(pos, (tuple, list)) or len(pos) < 2:
            return None
        row = self._safe_int(pos[0])
        col = self._safe_int(pos[1])
        if row is None or col is None:
            return None
        return col, row

    def xy_to_state_pos(self, x: object, y: object) -> Optional[Tuple[int, int]]:
        """Map view (x, y) to env/grid position (row, col)."""
        col = self._safe_int(x)
        row = self._safe_int(y)
        if col is None or row is None:
            return None
        return row, col

    def _state_xy_to_view_xy(self, x: object, y: object) -> Optional[Tuple[int, int]]:
        """state.json stores coordinates as x=col, y=row (already in view axes)."""
        state_x = self._safe_int(x)
        state_y = self._safe_int(y)
        if state_x is None or state_y is None:
            return None
        return state_x, state_y

    def _state_to_view_cell(self, x: object, y: object) -> Optional[Tuple[int, int]]:
        return self._state_xy_to_view_xy(x, y)

    def _unit_anchor_state_xy(self, unit: dict) -> Tuple[object, object]:
        if not isinstance(unit, dict):
            return None, None
        anchor_x = unit.get("anchor_x")
        anchor_y = unit.get("anchor_y")
        if self._safe_int(anchor_x) is not None and self._safe_int(anchor_y) is not None:
            return anchor_x, anchor_y
        return unit.get("x"), unit.get("y")

    def _unit_anchor_view_cell(self, unit: dict) -> Optional[Tuple[int, int]]:
        anchor_x, anchor_y = self._unit_anchor_state_xy(unit)
        return self._state_to_view_cell(anchor_x, anchor_y)

    def _unit_model_view_cells(self, unit: dict) -> List[Tuple[int, int]]:
        if not isinstance(unit, dict):
            return []
        model_positions = unit.get("model_positions")
        if not isinstance(model_positions, list):
            return []
        cells: List[Tuple[int, int]] = []
        for pos in model_positions:
            if not isinstance(pos, dict):
                continue
            view_cell = self._state_to_view_cell(pos.get("x"), pos.get("y"))
            if view_cell is not None:
                cells.append(view_cell)
        return cells

    def _resolve_board_dims(self, board: dict, units: List[dict]) -> Tuple[int, int]:
        """Viewer contract: env coordinates are x in [0..W-1], y in [0..H-1]."""
        board = board or {}
        width = self._safe_int(board.get("width"))
        height = self._safe_int(board.get("height"))

        if width is None:
            width = self._safe_int(board.get("board_w"))
        if height is None:
            height = self._safe_int(board.get("board_h"))

        cols = self._safe_int(board.get("cols"))
        rows = self._safe_int(board.get("rows"))
        if width is None and cols is not None:
            width = cols
        if height is None and rows is not None:
            height = rows

        width = width or ENV_BOARD_WIDTH
        height = height or ENV_BOARD_HEIGHT
        self._state_board_width = width
        self._state_board_height = height
        self._swap_axes = False
        self._rotate90 = False

        if (width, height) == (ENV_BOARD_HEIGHT, ENV_BOARD_WIDTH):
            self._swap_axes = True

        x_values = [self._safe_int(unit.get("x")) for unit in units if isinstance(unit, dict)]
        y_values = [self._safe_int(unit.get("y")) for unit in units if isinstance(unit, dict)]
        max_x = max((x for x in x_values if x is not None), default=-1)
        max_y = max((y for y in y_values if y is not None), default=-1)
        if max_x >= 0 and max_y >= 0:
            clearly_out_of_bounds = max_x >= width or max_y >= height
            fits_if_swapped = max_x < height and max_y < width
            if clearly_out_of_bounds and fits_if_swapped:
                self._swap_axes = True

        if self._swap_axes:
            width, height = height, width
        return width, height

    def board_debug_info(self) -> Dict[str, object]:
        return {
            "state_board_width": self._state_board_width,
            "state_board_height": self._state_board_height,
            "renderer_board_width": self._board_width,
            "renderer_board_height": self._board_height,
            "swap_axes": self._swap_axes,
            "rotate90": self._rotate90,
        }

    def set_active_context(
        self,
        active_unit_id=None,
        active_unit_side=None,
        selected_unit_id=None,
        selected_unit_side=None,
        phase=None,
        move_range=None,
        shoot_range=None,
        show_objective_radius=True,
        targets=None,
    ) -> None:
        self._active_unit_id = active_unit_id
        self._active_unit_side = active_unit_side
        self._selected_unit_id = selected_unit_id
        self._selected_unit_side = selected_unit_side
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
        self._spawn_scorch_for_fx(effect)
        self.update()

    def add_damage_popup(
        self,
        *,
        kind: str,
        target_side: str,
        target_id: int,
        damage_value: float = 0.0,
        hp_before: Optional[float] = None,
        hp_after: Optional[float] = None,
        hp_max: Optional[float] = None,
        dedup_key: str = "",
        created_ts: Optional[float] = None,
    ) -> None:
        key = self._norm_unit_key(target_side, target_id)
        if key is None:
            return
        now_ts = monotonic() if created_ts is None else float(created_ts)
        dedup_key = str(dedup_key or f"{kind}:{key[0]}:{key[1]}:{int(now_ts * 1000)}")
        dedup_seen_ts = self._damage_popup_dedup_seen.get(dedup_key)
        if dedup_seen_ts is not None and (now_ts - dedup_seen_ts) <= max(0.2, self._damage_popup_ttl_s):
            return
        self._damage_popup_dedup_seen[dedup_key] = now_ts

        kind_norm = str(kind or "damage").strip().lower()
        damage = max(0.0, float(damage_value or 0.0))
        if kind_norm == "damage":
            n = int(round(damage)) if damage > 0 else 0
            main_text = f"-{n} ХП"
        elif kind_norm == "heal":
            n = int(round(damage)) if damage > 0 else 0
            main_text = f"+{n} ХП"
        elif kind_norm == "save":
            main_text = "СЕЙВ"
        else:
            main_text = "ПРОМАХ"
        seed = (hash(dedup_key) ^ int(now_ts * 1000)) & 0xFFFFFFFF

        reused = False
        for popup in reversed(self._damage_popups_active):
            if popup.target_key != key:
                continue
            if popup.kind != kind_norm:
                continue
            if (now_ts - popup.created_t) > self._damage_popup_coalesce_window_s:
                continue
            if kind_norm == "damage":
                popup.amount += damage
                popup.damage_hits += 1
                popup.created_t = now_ts
                popup.ttl_s = max(popup.ttl_s, self._damage_popup_ttl_s)
                popup.text_main = f"-{int(round(popup.amount))} ХП"
                if hp_after is not None:
                    popup.hp_after = hp_after
                if hp_max is not None:
                    popup.hp_max = hp_max
                if hp_before is not None and popup.hp_before is None:
                    popup.hp_before = hp_before
                popup.dedup_key = dedup_key
                popup.seed = seed
                reused = True
                anchor = self._popup_world_anchor_for_key(key)
                if anchor is not None:
                    self._spawn_popup_burst(anchor, kind_norm, seed + 17)
                self._maybe_trigger_popup_hit_stop(popup.amount, hp_max, now_ts)
                break
            if kind_norm == "heal":
                popup.amount += damage
                popup.damage_hits += 1
                popup.created_t = now_ts
                popup.ttl_s = max(popup.ttl_s, self._damage_popup_ttl_s)
                popup.text_main = f"+{int(round(popup.amount))} ХП"
                if hp_after is not None:
                    popup.hp_after = hp_after
                if hp_max is not None:
                    popup.hp_max = hp_max
                if hp_before is not None and popup.hp_before is None:
                    popup.hp_before = hp_before
                popup.dedup_key = dedup_key
                popup.seed = seed
                reused = True
                anchor = self._popup_world_anchor_for_key(key)
                if anchor is not None:
                    self._spawn_popup_burst(anchor, kind_norm, seed + 19)
                break
        if reused:
            self.update()
            return

        same_target = [p for p in self._damage_popups_active if p.target_key == key]
        stack_index = min(3, len(same_target))
        rise_px = max(
            self._damage_popup_rise_min_px,
            min(self._damage_popup_rise_max_px, float(self.cell_size) * (0.55 + 0.15 * stack_index)),
        )
        popup = DamagePopup(
            kind=kind_norm,
            target_key=key,
            text_main=main_text,
            created_t=now_ts,
            ttl_s=self._damage_popup_ttl_s,
            rise_px=rise_px,
            dedup_key=dedup_key,
            stack_index=stack_index,
            amount=damage,
            damage_hits=1,
            hp_before=hp_before,
            hp_after=hp_after,
            hp_max=hp_max,
            seed=seed,
        )
        self._damage_popups_active.append(popup)
        if len(self._damage_popups_active) > self._damage_popup_max_active:
            self._damage_popups_active = self._damage_popups_active[-self._damage_popup_max_active :]
        anchor = self._popup_world_anchor_for_key(key)
        if anchor is not None:
            self._spawn_popup_burst(anchor, kind_norm, seed)
        if kind_norm == "damage":
            self._maybe_trigger_popup_hit_stop(damage, hp_max, now_ts)
        self._play_popup_sfx("save" if kind_norm == "heal" else kind_norm)
        self.update()

    def _model_icon_world_size(self) -> float:
        """Сторона квадрата спрайта модели в координатах доски (как в _draw_units_layer)."""
        return max(6.0, float(self.cell_size) * float(self._model_icon_scale))

    def _popup_world_anchor_for_key(self, key: Tuple[str, int]) -> Optional[QtCore.QPointF]:
        render = self._unit_by_key.get(key)
        if render is None:
            return None
        raw_mc = render.model_centers
        centers: List[QtCore.QPointF] = list(raw_mc) if raw_mc else [render.center]
        half = self._model_icon_world_size() * 0.5
        unit = self._state_unit(key)
        n_models = 1
        if isinstance(unit, dict):
            am = self._safe_int(unit.get("alive_models"))
            tm = self._safe_int(unit.get("models"))
            n_models = max(1, am or tm or 1)
        # Нет model_positions в стейте → model_centers пустой, в рендере только render.center (середина отряда).
        squad_center_only = not bool(raw_mc)

        if len(centers) == 1:
            c = centers[0]
            y = float(c.y()) - half
            if squad_center_only and n_models > 1:
                spread = math.sqrt(float(min(n_models, 20)))
                y -= float(self.cell_size) * (0.26 + 0.085 * spread)
            return QtCore.QPointF(float(c.x()), y)

        # Иконка центрирована на model_center; «линия макушек» верхнего ряда: min(Y) − half (как опора для HUD сверху).
        top = min(centers, key=lambda p: p.y())
        cx = sum(float(p.x()) for p in centers) / float(len(centers))
        return QtCore.QPointF(cx, float(top.y()) - half)

    def _spawn_popup_burst(self, center: QtCore.QPointF, kind: str, seed: int) -> None:
        if not self._fx_particle_textures:
            return
        rng = random.Random(int(seed) & 0xFFFFFFFF)
        kind_l = str(kind or "damage").lower()

        def _emit(texture_hint: str, count: int, speed_lo: float, speed_hi: float, life_lo: float, life_hi: float, spread: float, bias_up: float) -> None:
            tex = self._resolve_fx_key(texture_hint)
            if tex is None:
                return
            for _ in range(count):
                ang = rng.uniform(-spread, spread) - math.pi / 2.0 + bias_up
                spd = rng.uniform(speed_lo, speed_hi)
                vx = math.cos(ang) * spd
                vy = math.sin(ang) * spd
                life = rng.uniform(life_lo, life_hi)
                size = rng.uniform(8.0, 22.0) if kind_l != "miss" else rng.uniform(14.0, 28.0)
                alpha = rng.uniform(0.45, 0.85)
                mode = (
                    "additive"
                    if kind_l == "damage" or kind_l == "save" or kind_l == "heal"
                    else "normal"
                )
                self._particles.append(
                    ParticleInstance(
                        texture_key=tex,
                        position=QtCore.QPointF(center),
                        velocity=QtCore.QPointF(vx, vy),
                        life=life,
                        age=0.0,
                        size_px=size,
                        alpha=alpha,
                        mode=mode,
                    )
                )

        if kind_l == "damage":
            _emit("spark", rng.randint(8, 12), 55.0, 140.0, 0.18, 0.42, 0.55, 0.0)
        elif kind_l == "save":
            _emit("spark", rng.randint(3, 5), 35.0, 85.0, 0.28, 0.55, 0.9, 0.25)
        elif kind_l == "heal":
            _emit("spark", rng.randint(5, 9), 42.0, 105.0, 0.20, 0.46, 0.62, -0.12)
        else:
            _emit("smoke", rng.randint(6, 9), 12.0, 48.0, 0.35, 0.65, math.pi * 0.85, 0.0)

    def _maybe_trigger_popup_hit_stop(self, damage_amount: float, hp_max: Optional[float], now_ts: float) -> None:
        big = damage_amount >= 3.0
        if hp_max is not None and float(hp_max) > 1e-6:
            big = big or (float(damage_amount) / float(hp_max)) >= 0.30
        if big:
            self._damage_popup_hit_stop_until = max(
                self._damage_popup_hit_stop_until,
                now_ts + float(self._damage_popup_hit_stop_s),
            )

    def _play_popup_sfx(self, kind: str) -> None:
        raw = str(os.getenv("VIEWER_POPUP_SFX", "0")).strip().lower()
        if raw not in {"1", "true", "yes", "on"}:
            return
        try:
            from PySide6.QtMultimedia import QSoundEffect
            from PySide6.QtCore import QUrl
        except Exception:
            if not self._damage_popup_sfx_warned:
                self._damage_popup_sfx_warned = True
                print(
                    "Звук pop-up недоступен (QtMultimedia). Где: viewer/opengl_view.py (_play_popup_sfx). "
                    "Что делать дальше: установите PySide6 с QtMultimedia или отключите VIEWER_POPUP_SFX."
                )
            return
        name_map = {
            "damage": "popup_damage.wav",
            "save": "popup_save.wav",
            "heal": "popup_save.wav",
            "miss": "popup_miss.wav",
        }
        fname = name_map.get(str(kind).lower(), "popup_damage.wav")
        path = Path(__file__).resolve().parent / "assets" / "sfx" / fname
        if not path.is_file():
            if not self._damage_popup_sfx_warned:
                self._damage_popup_sfx_warned = True
                print(
                    f"Файл SFX не найден: {path}. Где: viewer/opengl_view.py (_play_popup_sfx). "
                    "Что делать дальше: добавьте .wav в viewer/assets/sfx/ или выключите VIEWER_POPUP_SFX."
                )
            return
        cache_key = str(path)
        effect = self._damage_popup_sfx_cache.get(cache_key)
        if effect is None:
            effect = QSoundEffect(self)
            effect.setSource(QUrl.fromLocalFile(str(path)))
            effect.setVolume(0.35)
            self._damage_popup_sfx_cache[cache_key] = effect
        try:
            effect.play()
        except Exception:
            pass

    @staticmethod
    def _popup_motion_rise(life_t: float, rise_px: float) -> Tuple[float, float, float]:
        """Возвращает (rise_text_px, rise_badge_px, anticipation_px)."""
        t = max(0.0, min(1.0, float(life_t)))
        anticip = 0.0
        if t < 0.10:
            anticip = 5.0 * (1.0 - t / 0.10)
        u = max(0.0, min(1.0, (t - 0.02) / 0.58))
        rise = rise_px * (1.0 - math.exp(-5.0 * u))
        overshoot = 0.12 * rise_px * math.sin(math.pi * u * 1.85) * math.exp(-4.2 * u)
        rise_text = max(0.0, rise + overshoot - anticip)
        rise_badge = max(0.0, rise * 0.88 + overshoot * 0.65 - anticip * 0.9)
        return rise_text, rise_badge, anticip

    @staticmethod
    def _popup_spiral_offset(stack_index: int) -> Tuple[float, float]:
        if stack_index <= 0:
            return 0.0, 0.0
        ang = stack_index * 0.92
        r = 10.0 + stack_index * 7.5
        return math.cos(ang) * r, math.sin(ang) * r * 0.65

    def _popup_gradient_for_kind(self, kind: str) -> Tuple[QtGui.QColor, QtGui.QColor]:
        k = str(kind or "").lower()
        if k == "save":
            return self._damage_grad_save_a, self._damage_grad_save_b
        if k == "heal":
            return self._damage_grad_heal_a, self._damage_grad_heal_b
        if k == "miss":
            return self._damage_grad_miss_a, self._damage_grad_miss_b
        return self._damage_grad_damage_a, self._damage_grad_damage_b

    def _popup_text_outline_for_kind(self, kind: str) -> Tuple[QtGui.QColor, QtGui.QColor]:
        """База для многослойного свечения и финальный «ободок» глифа по типу pop-up."""
        k = str(kind or "").lower()
        if k == "save":
            return self._damage_popup_glow_save, QtGui.QColor(18, 52, 72)
        if k == "heal":
            return self._damage_popup_glow_heal, QtGui.QColor(26, 92, 52)
        if k == "miss":
            return self._damage_popup_glow_miss, QtGui.QColor(48, 44, 62)
        return self._damage_popup_glow_damage, QtGui.QColor(72, 28, 24)

    def _build_damage_popup_badge_path(self, kind: str, rect: QtCore.QRectF) -> QtGui.QPainterPath:
        k = str(kind or "").lower()
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        path = QtGui.QPainterPath()
        if k == "heal":
            ry = min(h * 0.45, w * 0.38)
            path.addRoundedRect(rect, ry, ry)
            return path
        if k == "miss":
            ry = min(h * 0.5, w * 0.5)
            path.addRoundedRect(rect, ry, ry)
            return path
        if k == "save":
            pad = max(2.0, min(6.0, w * 0.04))
            path.moveTo(x + w * 0.5, y + pad)
            path.arcTo(x + pad, y + pad, w - 2 * pad, h * 0.62, 180.0, -180.0)
            path.lineTo(x + w - pad * 0.5, y + h - pad * 1.2)
            path.quadTo(x + w * 0.5, y + h + pad * 0.35, x + pad * 0.5, y + h - pad * 1.2)
            path.closeSubpath()
            return path
        skew = w * 0.07
        notch = h * 0.22
        path.moveTo(x + skew * 0.35, y + notch)
        path.lineTo(x + w * 0.12, y + h * 0.08)
        path.lineTo(x + w - skew, y)
        path.lineTo(x + w - skew * 0.2, y + h - notch * 0.4)
        path.lineTo(x + w * 0.55, y + h)
        path.lineTo(x + skew * 0.15, y + h - h * 0.12)
        path.closeSubpath()
        return path

    def _draw_popup_gradient_label(
        self,
        painter: QtGui.QPainter,
        center: QtCore.QPointF,
        text: str,
        font: QtGui.QFont,
        grad_a: QtGui.QColor,
        grad_b: QtGui.QColor,
        fade: float,
        outer_glow_base: QtGui.QColor,
        rim_color: QtGui.QColor,
    ) -> None:
        path = QtGui.QPainterPath()
        path.addText(0.0, 0.0, font, text)
        tb = path.boundingRect()
        if tb.width() <= 0.0 or tb.height() <= 0.0:
            return
        path.translate(-tb.center().x(), -tb.center().y())
        painter.save()
        painter.translate(center)
        grad = QtGui.QLinearGradient(-tb.width() * 0.5, -tb.height() * 0.5, tb.width() * 0.5, tb.height() * 0.5)
        ga = QtGui.QColor(grad_a)
        gb = QtGui.QColor(grad_b)
        ga.setAlpha(int(ga.alpha() * fade))
        gb.setAlpha(int(gb.alpha() * fade))
        grad.setColorAt(0.0, ga)
        grad.setColorAt(1.0, gb)
        for i in range(7, 0, -1):
            glow = QtGui.QColor(outer_glow_base)
            glow.setAlpha(int(22 * i * fade))
            pen = QtGui.QPen(glow, float(i) * 0.85)
            pen.setJoinStyle(QtCore.Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawPath(path)
        inner = QtGui.QColor(255, 255, 255)
        inner.setAlpha(int(55 * fade))
        painter.setPen(QtGui.QPen(inner, 1.1))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(path)
        painter.fillPath(path, QtGui.QBrush(grad))
        edge = QtGui.QColor(rim_color)
        edge.setAlpha(int(200 * fade))
        painter.setPen(QtGui.QPen(edge, 0.85))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(path)
        painter.restore()

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
        self._target_cell = self._state_xy_to_view_xy(cell[0], cell[1]) if cell is not None else None
        self._target_unit_id = None
        self.update()

    def clear_target_selection(self) -> None:
        self._target_unit_id = None
        self._target_cell = None
        self.update()

    def set_hover_cell(self, cell: Optional[Tuple[int, int]]) -> None:
        self._hover_cell = self._state_xy_to_view_xy(cell[0], cell[1]) if cell is not None else None
        self.update()

    def set_deploy_ghost(self, cells: List[Tuple[int, int]], is_valid: Optional[bool], unit_name: str = "") -> None:
        self._deploy_ghost_cells = list(cells or [])
        self._deploy_ghost_valid = is_valid
        self._deploy_ghost_unit_name = str(unit_name or "")
        self.update()

    def add_temporary_deploy_unit(
        self,
        *,
        unit_side: str,
        unit_id: int,
        unit_name: str,
        model_cells: List[Tuple[int, int]],
        facing: Optional[str] = None,
    ) -> None:
        if not model_cells:
            return
        key = (str(unit_side), int(unit_id))
        self._deploy_preview_units = [render for render in self._deploy_preview_units if render.key != key]
        color = Theme.player if key[0] == "player" else Theme.model
        model_centers: List[QtCore.QPointF] = []
        for state_x, state_y in model_cells:
            view_cell = self._state_xy_to_view_xy(state_x, state_y)
            if view_cell is None:
                continue
            model_centers.append(
                QtCore.QPointF(
                    view_cell[0] * self.cell_size + self.cell_size / 2,
                    view_cell[1] * self.cell_size + self.cell_size / 2,
                )
            )
        if not model_centers:
            return
        center = model_centers[0]
        render = UnitRender(
            key=key,
            center=QtCore.QPointF(center),
            radius=self.cell_size * 0.35,
            color=color,
            label=f"{key[1]}",
            icon=self._icon_for_unit_name(str(unit_name or "")),
            model_centers=model_centers,
            facing=("left" if str(facing).lower() == "left" else "right"),
        )
        self._deploy_preview_units.append(render)
        self._deploy_preview_unit_keys = {r.key for r in self._deploy_preview_units}
        self.update()

    def trigger_deploy_snap_flash(self, model_cells: List[Tuple[int, int]], duration_s: Optional[float] = None) -> None:
        cells = [tuple(cell) for cell in (model_cells or []) if isinstance(cell, (list, tuple)) and len(cell) >= 2]
        if not cells:
            return
        self._deploy_placement_fx.append(
            DeployPlacementFlash(
                cells=[(int(x), int(y)) for x, y in cells],
                t0=monotonic(),
                duration=max(0.05, float(duration_s or self._deploy_snap_duration_s)),
            )
        )
        self.update()

    def clear_temporary_deploy_units(self) -> None:
        if not self._deploy_preview_units:
            return
        self._deploy_preview_units = []
        self._deploy_preview_unit_keys = set()
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
        self._reachable_highlights = []
        self._reachable_cells_set = set()
        self._move_reachable_highlights = []
        self._advance_reachable_highlights = []
        self._move_cells_set = set()
        self._advance_cells_set = set()
        self._target_highlights = []
        self._shoot_range_highlights = []
        self._shoot_rapid_range_highlights = []
        self._shoot_target_infos = []
        self._shoot_hovered_target_key = None

        active_key = (self._active_unit_side, self._active_unit_id)
        if active_key[0] is None or active_key[1] is None:
            return
        unit = self._state_unit(active_key)
        if not isinstance(unit, dict):
            return

        if self._should_show_movement():
            if not self._viewer_human_turn_active():
                return
            move_cells, advance_cells = self._active_unit_movement_cells_statexy(unit)
            cells = list(move_cells) + list(advance_cells)
            if cells:
                all_highlights: List[QtCore.QRectF] = []
                move_highlights: List[QtCore.QRectF] = []
                advance_highlights: List[QtCore.QRectF] = []
                cell_set: set[tuple[int, int]] = set()
                move_set: set[tuple[int, int]] = set()
                advance_set: set[tuple[int, int]] = set()

                for x, y in move_cells:
                    view_cell = self._state_to_view_cell(x, y)
                    if view_cell is None:
                        continue
                    move_set.add((int(x), int(y)))
                    cell_set.add((int(x), int(y)))
                    vx, vy = view_cell
                    rect = QtCore.QRectF(vx * self.cell_size, vy * self.cell_size, self.cell_size, self.cell_size)
                    move_highlights.append(rect)
                    all_highlights.append(rect)

                for x, y in advance_cells:
                    view_cell = self._state_to_view_cell(x, y)
                    if view_cell is None:
                        continue
                    advance_set.add((int(x), int(y)))
                    cell_set.add((int(x), int(y)))
                    vx, vy = view_cell
                    rect = QtCore.QRectF(vx * self.cell_size, vy * self.cell_size, self.cell_size, self.cell_size)
                    advance_highlights.append(rect)
                    all_highlights.append(rect)

                self._reachable_cells_set = cell_set
                self._reachable_highlights = all_highlights
                self._move_cells_set = move_set
                self._advance_cells_set = advance_set
                self._move_reachable_highlights = move_highlights
                self._advance_reachable_highlights = advance_highlights

                if self._viewer_debug_enabled:
                    sig = (
                        active_key[1],
                        len(move_set),
                        len(advance_set),
                        hash(tuple(sorted(cell_set))) if cell_set else 0,
                    )
                    if sig != self._reachable_overlay_sig:
                        self._reachable_overlay_sig = sig
                        self._append_agent_log(
                            f"[VIEWER] reachable_overlay unit={active_key[1]} move={len(move_set)} advance={len(advance_set)}"
                        )
            return

        if self._should_show_shooting():
            if self._viewer_human_turn_active():
                self._build_shooting_overlay(unit)

    def select_unit(self, side, unit_id) -> None:
        self.set_selected_unit(side, unit_id)

    def set_selected_unit(self, side, unit_id) -> None:
        if unit_id is None:
            self._selected_unit_key = None
            self._selected_unit_id = None
            self._selected_unit_side = None
            self.update()
            return
        key = (side, unit_id)
        if key in self._unit_by_key:
            self._selected_unit_key = key
            self._selected_unit_id = unit_id
            self._selected_unit_side = side
            self.update()

    def fit_to_view(self) -> None:
        if self._board_rect.isEmpty():
            return
        viewport_w = float(self.width())
        viewport_h = float(self.height())
        if viewport_w <= 0 or viewport_h <= 0:
            return

        board_px_w = float(self._board_width * self.cell_size)
        board_px_h = float(self._board_height * self.cell_size)
        if board_px_w <= 0 or board_px_h <= 0:
            return

        fit_scale = self._fit_padding * min(viewport_w / board_px_w, viewport_h / board_px_h)
        fit_scale = max(self._min_scale, min(self._max_scale, fit_scale))

        center_x = board_px_w * 0.5
        center_y = board_px_h * 0.5
        pan = QtCore.QPointF(
            viewport_w * 0.5 - center_x * fit_scale,
            viewport_h * 0.5 - center_y * fit_scale,
        )

        self._scale = fit_scale
        self._pan = pan
        self._set_target_view(self._scale, self._pan, immediate=True)

        if os.getenv("GUI_DEBUG") == "1":
            print(
                "[VIEWER FIT] "
                f"viewport={int(viewport_w)}x{int(viewport_h)}, "
                f"board_px={int(board_px_w)}x{int(board_px_h)}, "
                f"cell_px={self.cell_size}, zoom={self._scale:.4f}"
            )

        self.update()

    def center_view(self) -> None:
        self._center_board()
        self._set_target_view(self._scale, self._pan, immediate=True)
        self.update()

    def center_on_state_cell(self, state_x: int, state_y: int) -> bool:
        """Center camera on state-space coordinates (x, y)."""
        view_cell = self._state_xy_to_view_xy(int(state_x), int(state_y))
        if view_cell is None:
            return False
        center = self._cell_center(view_cell[0], view_cell[1])
        viewport_center = QtCore.QPointF(self.width() / 2.0, self.height() / 2.0)
        self._pan = viewport_center - center * self._scale
        self._set_target_view(self._scale, self._pan, immediate=False)
        self.update()
        return True

    def _parse_viewer_activation_vinfo(self, vinfo: Dict) -> None:
        self._ai_activation_key = None
        self._ai_activation_meta = {}
        act = vinfo.get("activation")
        if not isinstance(act, dict) or not act:
            return
        if act.get("side") != "model":
            return
        uid = act.get("unit_id")
        if uid is not None:
            try:
                uid_int = int(uid)
            except (TypeError, ValueError):
                uid_int = None
            if uid_int is not None:
                self._ai_activation_key = ("model", uid_int)
        self._ai_activation_meta = {
            "phase": act.get("phase"),
            "step_kind": act.get("step_kind"),
            "unit_index": act.get("unit_index"),
            "unit_id": act.get("unit_id"),
        }

    @staticmethod
    def _format_ai_phase_badge_text(meta: Dict[str, Any]) -> str:
        phase = meta.get("phase")
        step_kind = meta.get("step_kind")
        phase_map = {
            "command": "Командование",
            "movement": "Движение",
            "shooting": "Стрельба",
            "charge": "Заряд",
            "fight": "Бой",
        }
        raw_phase = str(phase or "").strip()
        phase_ru = phase_map.get(raw_phase, raw_phase or "—")
        # Завершение фазы командования (внутренний шаг command_resolve) — как у «Действие: движение · юнит N».
        if step_kind == "command_resolve":
            return "Действие: командование · завершение фазы"
        if step_kind == "phase_end":
            return f"{phase_ru} · конец фазы"
        if step_kind == "before_unit":
            # «Действие: тип фазы · юнит N» — согласовано с кнопкой «Далее: фаза · юнит N».
            phase_lc = phase_ru.lower() if phase_ru and phase_ru != "—" else str(raw_phase or "шаг")
            uid = meta.get("unit_id")
            unit_tail = ""
            if uid is not None:
                try:
                    unit_tail = f" · юнит {int(uid)}"
                except (TypeError, ValueError):
                    unit_tail = ""
            return f"Действие: {phase_lc}{unit_tail}"
        if step_kind == "unit":
            return f"{phase_ru} · ход"
        sk = str(step_kind or "").strip()
        if not sk:
            return phase_ru
        # Не выводим внутренние snake_case-идентификаторы в оверлей.
        if "_" in sk and sk.isascii():
            return f"{phase_ru} · шаг"
        return f"{phase_ru} · {sk}"

    def _note_user_camera_interaction(self) -> None:
        self._last_user_camera_ts = monotonic()

    def _finish_ai_zoom_pulse(self) -> None:
        if self._ai_pulse_base_scale is not None:
            self._set_target_view(self._ai_pulse_base_scale, None, immediate=False)
            self._ai_pulse_base_scale = None
        self.update()

    def _start_ai_zoom_pulse(self) -> None:
        if str(os.getenv("VIEWER_FOLLOW_AI_PULSE", "1")).strip() != "1":
            return
        base = float(self._target_scale)
        self._ai_pulse_base_scale = base
        boosted = min(self._max_scale, max(self._min_scale, base * 1.08))
        if abs(boosted - base) < 1e-6:
            self._ai_pulse_base_scale = None
            return
        self._set_target_view(boosted, None, immediate=False)
        self._view_pulse_timer.stop()
        self._view_pulse_timer.start(420)

    def _maybe_follow_ai_camera(self, _vinfo: Dict, seq: object) -> None:
        if str(os.getenv("VIEWER_FOLLOW_AI", "0")).strip() != "1":
            return
        if monotonic() - self._last_user_camera_ts < 2.5:
            return
        key = self._ai_activation_key
        seq_int: int
        try:
            seq_int = int(seq) if seq is not None else -1
        except (TypeError, ValueError):
            seq_int = -1
        sig: Tuple[Optional[Tuple[str, int]], int] = (key, seq_int)
        if sig == self._last_ai_follow_sig:
            return
        if key is None:
            self._last_ai_follow_sig = sig
            return
        unit = self._unit_state_by_key.get(key)
        if unit is None:
            return
        ax, ay = self._unit_anchor_state_xy(unit)
        sx = self._safe_int(ax)
        sy = self._safe_int(ay)
        if sx is None or sy is None:
            return
        ok = bool(self.center_on_state_cell(sx, sy))
        if ok:
            self._start_ai_zoom_pulse()
        self._last_ai_follow_sig = sig

    def set_log_movement_overlay(self, payload: Optional[Dict[str, object]], *, persistent: bool) -> None:
        """Set overlay from log interaction: persistent=click, transient=hover."""
        if persistent:
            self._log_move_overlay_persistent = dict(payload) if payload else None
        else:
            self._log_move_overlay_hover = dict(payload) if payload else None
        self.update()

    def clear_log_movement_hover_overlay(self) -> None:
        if self._log_move_overlay_hover is None:
            return
        self._log_move_overlay_hover = None
        self.update()

    def _center_board(self) -> None:
        if self._board_rect.isEmpty():
            return
        view_center = QtCore.QPointF(self.width() / 2, self.height() / 2)
        board_center = self._board_rect.center()
        self._pan = view_center - board_center * self._scale
        self._target_pan = QtCore.QPointF(self._pan)

    def _append_agent_log(self, msg: str) -> None:
        if not msg:
            return
        try:
            import datetime
            log_path = AGENT_PLAY_LOG_PATH
            log_path.parent.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_path, "a", encoding="utf-8") as handle:
                handle.write(f"{timestamp} | {msg}\n")
        except Exception:
            return

    def _parse_terrain_features(self, features_raw: List[dict]) -> List[dict]:
        parsed: List[dict] = []
        for feature in features_raw:
            if not isinstance(feature, dict):
                continue
            kind = str(feature.get("kind") or "terrain_feature").strip() or "terrain_feature"
            sprite = str(feature.get("sprite") or "").strip()
            cells: List[Tuple[int, int]] = []
            for cell in (feature.get("cells") or []):
                if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                    continue
                cells.append((int(cell[0]), int(cell[1])))
            cell_rot = [int(v) for v in list(feature.get("cell_rotations") or [])]
            if kind.lower() == "barricade":
                cell_rot = [0] * len(cells)
            parsed.append({
                "id": str(feature.get("id") or ""),
                "kind": kind,
                "name": str(feature.get("name") or kind),
                "keywords": [str(v) for v in list(feature.get("keywords") or feature.get("tags") or [])],
                "sprite": sprite,
                "cells": cells,
                "cell_rotations": cell_rot,
                "covering_unit_ids": [int(v) for v in list(feature.get("covering_unit_ids") or []) if str(v).strip().isdigit()],
            })
        return parsed

    def _build_terrain_cell_index(self, features: List[dict]) -> Dict[Tuple[int, int], dict]:
        index: Dict[Tuple[int, int], dict] = {}
        for feature in features:
            if not isinstance(feature, dict):
                continue
            for cell in (feature.get("cells") or []):
                if not isinstance(cell, tuple) or len(cell) < 2:
                    continue
                index[(int(cell[0]), int(cell[1]))] = feature
        return index

    def _terrain_feature_at_world(self, world: QtCore.QPointF) -> Optional[dict]:
        state_pos = self._world_to_state_pos(world)
        if state_pos is None:
            return None
        return self._terrain_cell_index.get((int(state_pos[0]), int(state_pos[1])))

    def _log_terrain_features_once(self) -> None:
        sig = tuple(
            (
                str(feature.get("kind") or ""),
                tuple(feature.get("cells") or []),
                str(feature.get("sprite") or ""),
            )
            for feature in self._terrain_features_state
            if isinstance(feature, dict)
        )
        if sig == self._terrain_log_signature:
            return
        self._terrain_log_signature = sig
        if sig:
            first_kind = str(sig[0][0] or "")
            first_sprite = str(sig[0][2] or "")
            first_cells_count = len(sig[0][1])
            self._append_agent_log(
                f"[VIEWER][TERRAIN] features={len(sig)} first=<{first_kind},{first_sprite},{first_cells_count}>"
            )
            return
        self._append_agent_log("[VIEWER][TERRAIN] features=0")

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

    def _ensure_props(self) -> None:
        if not self.render_terrain:
            return
        if self._props_initialized:
            return
        if self._board_rect.isEmpty():
            return

        self._props = []
        for feature in self._terrain_features_state:
            if not isinstance(feature, dict):
                continue
            feature_kind = str(feature.get("kind") or "terrain_feature").strip() or "terrain_feature"
            cells = list(feature.get("cells") or [])
            if not cells:
                continue
            sprite_name = str(feature.get("sprite") or "")
            sprite_path = self._texture_manager._base_dir / "props" / "terrain" / sprite_name
            exists = bool(sprite_name) and sprite_path.exists()
            sprite_log_key = f"{sprite_name}|{sprite_path}"
            if sprite_log_key not in self._terrain_sprite_log_cache:
                self._terrain_sprite_log_cache.add(sprite_log_key)
                self._append_agent_log(
                    f"[VIEWER][TERRAIN] load sprite={sprite_name or '(empty)'} path={sprite_path} exists={exists}"
                )

            texture_key = sprite_name if sprite_name in self._prop_textures else feature_kind
            cell_rot = list(feature.get("cell_rotations") or [])
            if feature_kind.lower() == "barricade":
                cell_rot = [0] * len(cells)
            for idx, (row, col) in enumerate(cells):
                rot = float(cell_rot[idx]) if idx < len(cell_rot) else 0.0
                cell_rect = QtCore.QRectF(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                self._props.append(
                    PropInstance(
                        kind=texture_key,
                        center=cell_rect.center(),
                        rotation_deg=rot,
                        scale=1.0,
                        debug_rect=cell_rect,
                        sprite_name=sprite_name,
                        draw_rect=cell_rect,
                    )
                )

        self._props_initialized = True

    def _view_world_rect(self) -> QtCore.QRectF:
        pan_x, pan_y = self._snap_pan_to_pixels(self._pan)
        scale = self._scale if self._scale > 0 else 1.0
        width = self.width()
        height = self.height()
        left_world = (-pan_x) / scale
        right_world = (width - pan_x) / scale
        top_world = (-pan_y) / scale
        bottom_world = (height - pan_y) / scale
        return QtCore.QRectF(
            left_world,
            top_world,
            right_world - left_world,
            bottom_world - top_world,
        )

    def _draw_sprite(
        self,
        painter: QtGui.QPainter,
        pixmap: QtGui.QPixmap,
        center: QtCore.QPointF,
        *,
        rotation_deg: float = 0.0,
        scale: float = 1.0,
        alpha: float = 1.0,
    ) -> None:
        if pixmap.isNull():
            return
        painter.save()
        painter.setOpacity(max(0.0, min(1.0, alpha)))
        painter.translate(center)
        if rotation_deg:
            painter.rotate(rotation_deg)
        painter.scale(scale, scale)
        half_w = pixmap.width() / 2
        half_h = pixmap.height() / 2
        painter.drawPixmap(QtCore.QPointF(-half_w, -half_h), pixmap)
        painter.restore()

    def _draw_grid(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.grid import paint_grid_layer

        self._paint_board_layer(painter, paint_grid_layer, layer_name="grid")

    def _add_decal(self, kind: str, center: QtCore.QPointF) -> None:
        if not self.render_decals:
            return
        texture_key = self._resolve_decal_key(kind)
        if texture_key is None:
            return
        rotation = random.uniform(0.0, 360.0)
        scale = random.uniform(0.7, 1.1)
        self._decals.append(
            DecalInstance(
                texture_key=texture_key,
                center=center,
                rotation_deg=rotation,
                scale=scale,
            )
        )
        if len(self._decals) > 500:
            self._decals = self._decals[-500:]

    def _spawn_scorch_for_fx(self, effect: GaussTracerEffect) -> None:
        if effect is None:
            return
        scorch_sprite = self._fx_pixmaps.get("gauss_scorch_decal")
        if scorch_sprite is None or scorch_sprite.isNull():
            return
        cfg = effect.config or {}
        ttl_s = max(0.4, float(cfg.get("scorch_ttl_s", 1.8)))
        size_cells = max(
            0.12,
            float(cfg.get("scorch_base", 0.42)) * float(cfg.get("scorch_scale", 1.2)),
        )
        alpha = max(0.25, min(1.0, float(cfg.get("scorch_alpha", 0.95))))
        direction = effect.end - effect.start
        length = math.hypot(direction.x(), direction.y())
        center = QtCore.QPointF(effect.end)
        if length > 1e-3:
            dir_unit = QtCore.QPointF(direction.x() / length, direction.y() / length)
            normal = QtCore.QPointF(-dir_unit.y(), dir_unit.x())
            rng = random.Random((effect.seed + 101) & 0xFFFFFFFF)
            off_min = float(cfg.get("scorch_offset_px_min", 2.0))
            off_max = float(cfg.get("scorch_offset_px_max", 4.0))
            off_px = rng.uniform(off_min, off_max) * rng.choice((-1.0, 1.0))
            center = QtCore.QPointF(
                effect.end.x() + normal.x() * self._px_to_world(off_px),
                effect.end.y() + normal.y() * self._px_to_world(off_px),
            )
        self._fx_scorch_decals.append(
            ScorchDecalFx(
                center=center,
                created_t=monotonic(),
                ttl_s=ttl_s,
                size_cells=size_cells,
                rotation_deg=random.uniform(0.0, 360.0),
                alpha=alpha,
            )
        )
        if len(self._fx_scorch_decals) > self._fx_scorch_max_active:
            self._fx_scorch_decals = self._fx_scorch_decals[-self._fx_scorch_max_active :]

    def _draw_scorch_decals(self, painter: QtGui.QPainter) -> None:
        if not self._fx_scorch_decals:
            return
        scorch_sprite = self._fx_pixmaps.get("gauss_scorch_decal")
        if scorch_sprite is None or scorch_sprite.isNull():
            return
        now = monotonic()
        kept: List[ScorchDecalFx] = []
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setClipRect(self._board_rect)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        for decal in self._fx_scorch_decals:
            age = now - decal.created_t
            if age >= decal.ttl_s:
                continue
            kept.append(decal)
            fade = 1.0
            fade_tail = min(0.35, decal.ttl_s * 0.4)
            if age > (decal.ttl_s - fade_tail):
                fade = max(0.0, (decal.ttl_s - age) / max(1e-4, fade_tail))
            # Keep original texture colors (charred ring + green core). Size in board cells
            # like impact rings, not raw pixmap pixels.
            size = max(0.001, self.cell_size * decal.size_cells)
            painter.save()
            painter.setOpacity(max(0.0, min(1.0, decal.alpha * fade)))
            painter.translate(decal.center)
            if decal.rotation_deg:
                painter.rotate(decal.rotation_deg)
            rect = QtCore.QRectF(-size / 2.0, -size / 2.0, size, size)
            painter.drawPixmap(rect, scorch_sprite, QtCore.QRectF(scorch_sprite.rect()))
            painter.restore()
        painter.restore()
        self._fx_scorch_decals = kept

    def _resolve_decal_key(self, kind: str) -> Optional[str]:
        if not self._decal_textures:
            return None
        kind_lower = kind.lower()
        for name in self._decal_textures:
            if kind_lower in name.lower():
                return name
        return next(iter(self._decal_textures.keys()), None)

    def _spawn_particles(self, center: QtCore.QPointF, kind: str, count: int) -> None:
        if not self._fx_particle_textures:
            return
        texture_key = self._resolve_fx_key(kind)
        if texture_key is None:
            return
        rng = random.Random()
        for _ in range(count):
            speed = rng.uniform(8.0, 28.0)
            angle = rng.uniform(0.0, math.tau)
            velocity = QtCore.QPointF(math.cos(angle) * speed, math.sin(angle) * speed)
            life = rng.uniform(0.45, 1.2) if kind != "spark" else rng.uniform(0.2, 0.5)
            size = rng.uniform(18.0, 36.0) if kind == "smoke" else rng.uniform(10.0, 20.0)
            alpha = 0.75 if kind == "spark" else 0.6
            mode = "additive" if kind == "spark" else "normal"
            self._particles.append(
                ParticleInstance(
                    texture_key=texture_key,
                    position=QtCore.QPointF(center),
                    velocity=velocity,
                    life=life,
                    age=0.0,
                    size_px=size,
                    alpha=alpha,
                    mode=mode,
                )
            )

    def _resolve_fx_key(self, kind: str) -> Optional[str]:
        kind_lower = kind.lower()
        for name in self._fx_particle_textures:
            if kind_lower in name.lower():
                return name
        return next(iter(self._fx_particle_textures.keys()), None)

    def set_move_animation_config(self, cfg: Optional[Dict[str, Any]] = None) -> None:
        """Параметры из viewer_config.json: move_base_ms, move_per_cell_ms, move_cap_ms, …"""
        if not isinstance(cfg, dict):
            return

        def _clamp_f(key: str, current: float, lo: float, hi: float) -> float:
            if key not in cfg:
                return current
            try:
                v = float(cfg[key])
            except (TypeError, ValueError):
                return current
            return max(lo, min(hi, v))

        self._move_base_ms = _clamp_f("move_base_ms", self._move_base_ms, 0.0, 8000.0)
        self._move_per_cell_ms = _clamp_f("move_per_cell_ms", self._move_per_cell_ms, 0.0, 2000.0)
        self._move_cap_ms = _clamp_f("move_cap_ms", self._move_cap_ms, 1.0, 20000.0)
        self._move_seq_floor_new_step_ms = _clamp_f(
            "move_seq_floor_new_step_ms", self._move_seq_floor_new_step_ms, 0.0, 8000.0
        )
        self._move_seq_floor_default_ms = _clamp_f(
            "move_seq_floor_default_ms", self._move_seq_floor_default_ms, 0.0, 8000.0
        )
        raw_ease = cfg.get("move_ease", self._move_ease)
        if isinstance(raw_ease, str):
            e = raw_ease.strip().lower()
            if e in {"linear", "smoothstep", "cubic_out"}:
                self._move_ease = e

        self._viewer_cfg_snapshot = dict(cfg)
        self._fx_v2 = viewer_flag("viewer.fx.v2", cfg)
        self._maybe_apply_motion_tokens_for_fx_v2(cfg)
        self._fx_tune_base = {
            "move_cap_ms": float(self._move_cap_ms),
            "popup_ttl_s": float(self._damage_popup_ttl_s),
            "hit_stop_s": float(self._damage_popup_hit_stop_s),
            "outline_px": float(self._damage_popup_outline_px),
            "status_anim_duration_s": float(self._status_anim_duration_s),
            "rise_min_px": float(self._damage_popup_rise_min_px),
            "rise_max_px": float(self._damage_popup_rise_max_px),
        }
        self._apply_fx_quality_tuning()

    def set_fx_quality(self, level: Optional[str]) -> None:
        """Runtime FX tier (``low`` / ``medium`` / ``high``); used with ``viewer.fx.v2``."""
        lvl = str(level or "").strip().lower()
        if lvl not in {"low", "medium", "high"}:
            lvl = "medium"
        if lvl != self._fx_quality_resolved:
            self._fx_quality_resolved = lvl
            self._apply_fx_quality_tuning()

    def _maybe_apply_motion_tokens_for_fx_v2(self, cfg: Dict[str, Any]) -> None:
        if not self._fx_v2 or not viewer_flag("viewer.theme.v2", cfg):
            return
        try:
            from theme.loader import load_tokens

            data = load_tokens()
            motion = data.get("motion") if isinstance(data.get("motion"), dict) else {}
        except Exception:
            return
        ease = motion.get("moveEaseFxV2") or motion.get("moveEase")
        if isinstance(ease, str):
            e = ease.strip().lower()
            if e in {"linear", "smoothstep", "cubic_out"}:
                self._move_ease = e

    def _default_fx_v2_scales(self, level: str) -> Dict[str, float]:
        if level == "low":
            return {"moveCapScale": 0.82, "popupTtlScale": 0.72, "hitStopMs": 0.0, "gaussAlphaScale": 0.55}
        if level == "high":
            return {"moveCapScale": 1.08, "popupTtlScale": 1.18, "hitStopMs": 48.0, "gaussAlphaScale": 1.12}
        return {"moveCapScale": 1.0, "popupTtlScale": 1.0, "hitStopMs": 32.0, "gaussAlphaScale": 1.0}

    def _merge_token_fx_v2_scales(self, scales: Dict[str, Dict[str, float]]) -> None:
        cfg = getattr(self, "_viewer_cfg_snapshot", None) or {}
        if not self._fx_v2 or not viewer_flag("viewer.theme.v2", cfg):
            return
        try:
            from theme.loader import load_tokens

            motion = load_tokens().get("motion") if isinstance(load_tokens().get("motion"), dict) else {}
            fxv2 = motion.get("fxV2") if isinstance(motion.get("fxV2"), dict) else {}
        except Exception:
            return
        for tier in ("low", "medium", "high"):
            raw = fxv2.get(tier)
            if not isinstance(raw, dict):
                continue
            tgt = scales.setdefault(tier, {})
            for key in ("moveCapScale", "popupTtlScale", "hitStopMs", "gaussAlphaScale"):
                if key not in raw:
                    continue
                try:
                    tgt[key] = float(raw[key])
                except (TypeError, ValueError):
                    continue

    def _apply_fx_quality_tuning(self) -> None:
        base = self._fx_tune_base
        if base is None:
            return
        cfg = getattr(self, "_viewer_cfg_snapshot", None) or {}
        env_q = str(os.environ.get("VIEWER_FX_QUALITY", "") or "").strip().lower()
        lvl = env_q if env_q in {"low", "medium", "high"} else str(cfg.get("fx_quality", "medium")).strip().lower()
        if lvl not in {"low", "medium", "high"}:
            lvl = "medium"
        self._fx_quality_resolved = lvl

        scales = {
            "low": dict(self._default_fx_v2_scales("low")),
            "medium": dict(self._default_fx_v2_scales("medium")),
            "high": dict(self._default_fx_v2_scales("high")),
        }
        self._merge_token_fx_v2_scales(scales)
        s = scales.get(lvl, scales["medium"])

        # Restore baseline from last set_move_animation_config, then optionally apply FX v2 tiering.
        self._move_cap_ms = base["move_cap_ms"]
        self._damage_popup_ttl_s = base["popup_ttl_s"]
        self._damage_popup_hit_stop_s = base["hit_stop_s"]
        self._damage_popup_outline_px = base["outline_px"]
        self._status_anim_duration_s = base["status_anim_duration_s"]
        self._damage_popup_rise_min_px = base["rise_min_px"]
        self._damage_popup_rise_max_px = base["rise_max_px"]
        self._fx_gauss_alpha_scale = 1.0

        if not self._fx_v2:
            return

        cap_scale = float(s.get("moveCapScale", 1.0))
        ttl_scale = float(s.get("popupTtlScale", 1.0))
        gauss_scale = float(s.get("gaussAlphaScale", 1.0))
        hit_stop_ms = float(s.get("hitStopMs", 32.0))

        self._move_cap_ms = max(1.0, float(base["move_cap_ms"]) * max(0.25, cap_scale))
        self._damage_popup_ttl_s = max(0.25, float(base["popup_ttl_s"]) * max(0.35, ttl_scale))
        self._damage_popup_hit_stop_s = max(0.0, hit_stop_ms / 1000.0)
        self._damage_popup_outline_px = max(1.0, float(base["outline_px"]) * (1.05 if lvl == "high" else 1.0))
        self._status_anim_duration_s = max(
            0.08,
            float(base["status_anim_duration_s"]) * (0.88 if lvl == "low" else 1.12 if lvl == "high" else 1.0),
        )
        self._damage_popup_rise_min_px = max(
            8.0, float(base["rise_min_px"]) * (0.85 if lvl == "low" else 1.15 if lvl == "high" else 1.0)
        )
        self._damage_popup_rise_max_px = max(
            self._damage_popup_rise_min_px + 2.0,
            float(base["rise_max_px"]) * (0.85 if lvl == "low" else 1.15 if lvl == "high" else 1.0),
        )
        self._fx_gauss_alpha_scale = max(0.15, min(1.6, gauss_scale))

    def _apply_move_ease(self, t: float) -> float:
        t = max(0.0, min(1.0, float(t)))
        kind = str(self._move_ease or "smoothstep").strip().lower()
        if kind == "linear":
            return t
        if kind == "cubic_out":
            return 1.0 - (1.0 - t) ** 3
        return t * t * (3.0 - 2.0 * t)

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
        raw_f = max(0.0, min(1.0, float(factor)))
        f = self._apply_move_ease(raw_f)
        self._units = []
        self._unit_by_key = {}
        self._unit_labels = []
        self._unit_hitboxes_screen = {}

        occupied: Dict[Tuple[int, int], List[dict]] = {}
        for unit in self._units_state:
            key = self._norm_unit_key(unit.get("side"), unit.get("id"))
            if key is None:
                continue
            curr_pos = self._curr_unit_positions.get(key)
            if curr_pos is None:
                continue
            cell_key = (int(curr_pos.x()), int(curr_pos.y()))
            occupied.setdefault(cell_key, []).append(unit)

        for unit in self._units_state:
            key = self._norm_unit_key(unit.get("side"), unit.get("id"))
            if key is None:
                continue
            curr_pos = self._curr_unit_positions.get(key)
            if curr_pos is None:
                continue
            prev_pos = self._prev_unit_positions.get(key, curr_pos)
            interp_x = prev_pos.x() + (curr_pos.x() - prev_pos.x()) * f
            interp_y = prev_pos.y() + (curr_pos.y() - prev_pos.y()) * f

            stack = occupied.get((int(curr_pos.x()), int(curr_pos.y())), [])
            offset = 0.0
            if len(stack) > 1:
                offset = (stack.index(unit) - (len(stack) - 1) / 2) * (self.cell_size * 0.15)
            center_x = interp_x * self.cell_size + self.cell_size / 2 + offset
            center_y = interp_y * self.cell_size + self.cell_size / 2 - offset
            color = Theme.player if unit.get("side") == "player" else Theme.model
            radius = self.cell_size * 0.35
            prev_m = self._prev_model_cells_by_key.get(key)
            curr_m = self._curr_model_cells_by_key.get(key)
            model_centers: List[QtCore.QPointF] = []
            if prev_m and curr_m and len(prev_m) == len(curr_m):
                n = len(prev_m)
                use_stagger = bool(getattr(self, "_fx_v2", False)) and n > 1
                stagger_span = 0.34
                for i, ((px, py), (cx, cy)) in enumerate(zip(prev_m, curr_m)):
                    if use_stagger:
                        start = stagger_span * (i / max(1, n - 1))
                        denom = max(1e-4, 1.0 - stagger_span)
                        sub = max(0.0, min(1.0, (raw_f - start) / denom))
                        lf = self._apply_move_ease(sub)
                    else:
                        lf = f
                    mx = px + (cx - px) * lf
                    my = py + (cy - py) * lf
                    model_centers.append(
                        QtCore.QPointF(
                            mx * self.cell_size + self.cell_size / 2,
                            my * self.cell_size + self.cell_size / 2,
                        )
                    )
            elif prev_m and curr_m and len(prev_m) != len(curr_m) and len(prev_m) > 0 and len(curr_m) > 0:
                pcx = sum(p[0] for p in prev_m) / float(len(prev_m))
                pcy = sum(p[1] for p in prev_m) / float(len(prev_m))
                ccx = sum(c[0] for c in curr_m) / float(len(curr_m))
                ccy = sum(c[1] for c in curr_m) / float(len(curr_m))
                ox = (pcx - ccx) * (1.0 - f)
                oy = (pcy - ccy) * (1.0 - f)
                for cx, cy in curr_m:
                    mx = cx + ox
                    my = cy + oy
                    model_centers.append(
                        QtCore.QPointF(
                            mx * self.cell_size + self.cell_size / 2,
                            my * self.cell_size + self.cell_size / 2,
                        )
                    )
            else:
                model_cells = self._unit_model_view_cells(unit)
                model_centers = [
                    QtCore.QPointF(
                        model_x * self.cell_size + self.cell_size / 2,
                        model_y * self.cell_size + self.cell_size / 2,
                    )
                    for model_x, model_y in model_cells
                ]
            unit_name = str(unit.get("name") or "")
            alive_models = self._safe_int(unit.get("alive_models"))
            total_models = self._safe_int(unit.get("models"))
            model_label = ""
            if alive_models is not None and total_models is not None:
                model_label = f" {alive_models}/{total_models}"
            elif total_models is not None:
                model_label = f" {total_models}"
            render = UnitRender(
                key=key,
                center=QtCore.QPointF(center_x, center_y),
                radius=radius,
                color=color,
                label=f"{unit.get('id', '')}{model_label}",
                icon=self._icon_for_unit_name(unit_name),
                model_centers=model_centers,
                facing=self._resolve_render_facing(unit),
            )
            self._units.append(render)
            self._unit_by_key[key] = render
            self._unit_labels.append(
                (render.label, QtCore.QPointF(center_x - radius, center_y - radius - 8))
            )

    def _state_unit(self, unit_key: Tuple[str, int]) -> Optional[dict]:
        units = self._state.get("units", []) or []
        for unit in units:
            nk = self._norm_unit_key(unit.get("side"), unit.get("id"))
            if nk == unit_key:
                return unit
        return None

    def _cells_from_raw(self, raw_cells: object) -> List[Tuple[int, int]]:
        result: List[Tuple[int, int]] = []
        for cell in list(raw_cells or []):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            x = self._safe_int(cell[0])
            y = self._safe_int(cell[1])
            if x is None or y is None:
                continue
            result.append((x, y))
        return result

    def _active_unit_movement_cells_statexy(self, unit: dict) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        unit_status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
        raw_move_cells = unit_status.get("move_cells")
        raw_advance_cells = unit_status.get("advance_cells")
        overlay = self._state.get("movement_overlay") if isinstance(self._state.get("movement_overlay"), dict) else {}
        if raw_move_cells is None:
            raw_move_cells = overlay.get("move_cells")
        if raw_advance_cells is None:
            raw_advance_cells = overlay.get("advance_cells")

        move_cells = self._cells_from_raw(raw_move_cells)
        advance_cells = self._cells_from_raw(raw_advance_cells)
        if move_cells or advance_cells:
            return move_cells, advance_cells

        raw_cells = unit_status.get("reachable_cells")
        if raw_cells is None:
            raw_cells = self._state.get("active_unit_reachable_cells")
        return self._cells_from_raw(raw_cells), []

    def is_reachable_cell(self, x: int, y: int) -> bool:
        return (int(x), int(y)) in self._reachable_cells_set

    def is_move_cell(self, x: int, y: int) -> bool:
        return (int(x), int(y)) in self._move_cells_set

    def is_advance_cell(self, x: int, y: int) -> bool:
        return (int(x), int(y)) in self._advance_cells_set

    def _should_show_movement(self) -> bool:
        phase = str(self._phase or "").lower()
        return "move" in phase or "движ" in phase or "movement" in phase

    def _should_show_shooting(self) -> bool:
        phase = str(self._phase or "").lower()
        return "shoot" in phase or "стрел" in phase or "shooting" in phase

    def _viewer_human_turn_active(self) -> bool:
        """state_export: active player = ход человека, model = ход ИИ. Оверлей клеток — только для человека."""
        active = str(self._state.get("active") or self._state.get("active_side") or "").strip().lower()
        if active == "model":
            return False
        return True

    def shooting_overlay_mode_label(self) -> str:
        if self._show_shoot_range_cells:
            return "Cells+Targets"
        return "Targets"

    def _draw_movement_overlay(self, unit: dict) -> None:
        move_range = self._move_range
        if move_range is None:
            return
        view_cell = self._unit_anchor_view_cell(unit)
        if view_cell is None:
            return
        x, y = view_cell
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

    def _build_shooting_overlay(self, unit: dict) -> None:
        shoot_range = self._safe_int(self._shoot_range)
        source = self._unit_anchor_view_cell(unit)
        sx, sy = source if source is not None else (None, None)

        target_filter = set(self._resolve_targets(unit, shoot_range or 0))

        inferred_range = shoot_range
        inferred_from_targets = False
        max_dist = 0
        if source is not None and target_filter:
            max_dist = 0
            for side, target_id in target_filter:
                target = None
                for candidate in self._state.get("units", []) or []:
                    if candidate.get("side") == side and self._safe_int(candidate.get("id")) == int(target_id):
                        target = candidate
                        break
                if target is None:
                    continue
                tx_ty = self._unit_anchor_view_cell(target)
                if tx_ty is None:
                    continue
                tx, ty = tx_ty
                max_dist = max(max_dist, max(abs(tx - sx), abs(ty - sy)))
            # ВАЖНО: не сужаем range до набора текущих валидных целей.
            # target_filter зависит от фазы/запроса и может содержать только ближайшие цели.
            # Сужение ломает геометрию Cells-overlay (радиус визуально меньше реального оружейного range).
            if max_dist > 0 and (inferred_range is None or inferred_range <= 0):
                inferred_range = int(max_dist)
                inferred_from_targets = True

        rapid_range = self._resolve_rapid_fire_cells_range(unit, inferred_range)

        self._log_shoot_overlay_range_debug(
            unit=unit,
            full_range_raw=shoot_range,
            full_range_cells=inferred_range,
            rapid_range_cells=rapid_range,
            source=source,
            target_filter=target_filter,
            inferred_from_targets=inferred_from_targets,
            max_target_dist=max_dist,
        )

        if inferred_range is not None and inferred_range > 0 and source is not None:
            max_x = max(0, int(self._board_width) - 1)
            max_y = max(0, int(self._board_height) - 1)
            total_cells = 0
            inside_cells = 0
            outside_cells = 0
            rapid_cells = 0
            for y in range(0, max_y + 1):
                for x in range(0, max_x + 1):
                    total_cells += 1
                    distance = max(abs(x - sx), abs(y - sy))
                    if distance > inferred_range:
                        outside_cells += 1
                        continue
                    inside_cells += 1
                    self._shoot_range_highlights.append(
                        QtCore.QRectF(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    )
                    if rapid_range is not None and distance <= rapid_range:
                        rapid_cells += 1
                        self._shoot_rapid_range_highlights.append(
                            QtCore.QRectF(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        )
            self._log_shoot_overlay_cells_debug(
                unit=unit,
                source=source,
                full_range_cells=inferred_range,
                rapid_range_cells=rapid_range,
                total_cells=total_cells,
                inside_cells=inside_cells,
                rapid_cells=rapid_cells,
                outside_cells=outside_cells,
            )

        shooter_id = self._safe_int(unit.get("id"))
        for target in self._state.get("units", []) or []:
            if not isinstance(target, dict):
                continue
            if target.get("side") == unit.get("side"):
                continue

            target_id = self._safe_int(target.get("id"))
            target_key = (target.get("side"), int(target_id)) if target_id is not None else None
            if target_filter and target_key not in target_filter:
                continue
            if target_id is None:
                continue

            tx_ty = self._unit_anchor_view_cell(target)
            if tx_ty is None:
                continue
            tx, ty = tx_ty
            if inferred_range is not None and inferred_range > 0 and source is not None:
                distance = max(abs(tx - sx), abs(ty - sy))
                if distance > inferred_range:
                    continue

            status = target.get("unit_status") if isinstance(target.get("unit_status"), dict) else {}
            seen_by = {self._safe_int(v) for v in list(status.get("seen_by_ids") or [])}
            obscured_vs = {self._safe_int(v) for v in list(status.get("obscured_vs") or [])}
            has_los = shooter_id is not None and shooter_id in seen_by
            obscured = has_los and shooter_id is not None and shooter_id in obscured_vs

            classification = "NO_LOS"
            if has_los and obscured:
                classification = "OBSCURED"
            elif has_los:
                classification = "VALID"

            key = (str(target.get("side")), int(target_id))
            self._shoot_target_infos.append(
                {
                    "unit_id": int(target_id),
                    "unit_key": key,
                    "classification": classification,
                }
            )

    def _resolve_targets(self, unit: dict, shoot_range: int) -> Iterable[Tuple[str, int]]:
        targets = set()
        if isinstance(self._targets, list):
            for entry in self._targets:
                if isinstance(entry, dict):
                    side = entry.get("side")
                    target_id = self._safe_int(entry.get("id"))
                    if side and target_id is not None:
                        targets.add((side, int(target_id)))
                elif isinstance(entry, (list, tuple)) and len(entry) >= 2:
                    side = entry[0]
                    target_id = self._safe_int(entry[1])
                    if side and target_id is not None:
                        targets.add((side, int(target_id)))
                elif isinstance(entry, int):
                    for candidate in self._state.get("units", []) or []:
                        if self._safe_int(candidate.get("id")) == int(entry):
                            c_side = candidate.get("side")
                            if c_side:
                                targets.add((c_side, int(entry)))
            if targets:
                return targets

        # Fallback: только данные движка из state export (in_range_ids / in_range_targets).
        # Не используем чистую геометрию по anchor-клетке, чтобы не рисовать "ложно валидные" цели.
        unit_status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
        in_range_ids = unit_status.get("in_range_ids") or unit_status.get("in_range_targets") or []
        visible_ids = unit_status.get("can_see_ids") or []
        try:
            in_range_set = {
                int(v) for v in in_range_ids if isinstance(v, (int, float, str)) and str(v).strip().isdigit()
            }
            visible_set = {
                int(v) for v in visible_ids if isinstance(v, (int, float, str)) and str(v).strip().isdigit()
            }
        except (TypeError, ValueError):
            in_range_set = set()
            visible_set = set()

        if in_range_set:
            for target in self._state.get("units", []) or []:
                if not isinstance(target, dict):
                    continue
                if target.get("side") == unit.get("side"):
                    continue
                target_id = self._safe_int(target.get("id"))
                if target_id is None:
                    continue
                if int(target_id) not in in_range_set:
                    continue
                if visible_set and int(target_id) not in visible_set:
                    continue
                target_side = target.get("side")
                if target_side:
                    targets.add((str(target_side), int(target_id)))
            if targets:
                return targets

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
        self._note_user_camera_interaction()
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
            state_pos = self._world_to_state_pos(world)
            if state_pos is not None:
                state_xy = (int(state_pos[1]), int(state_pos[0]))
                if self.is_reachable_cell(state_xy[0], state_xy[1]):
                    self.cell_right_clicked.emit(state_xy[0], state_xy[1])
                    return

            self._rebuild_unit_hitboxes_screen()
            unit_key = self._unit_key_at_screen_pos(QtCore.QPointF(event.position()))
            terrain_feature = self._terrain_feature_at_world(world) if unit_key is None else None
            if unit_key:
                self.unit_right_clicked.emit(unit_key[0], int(unit_key[1]), event.globalPosition().toPoint())
                return
            elif terrain_feature is not None:
                self._tooltip_pinned = not self._tooltip_pinned
                self._terrain_tooltip_widget.set_pinned(self._tooltip_pinned)
                if self._tooltip_pinned:
                    self._show_terrain_tooltip(terrain_feature, event.globalPosition().toPoint())
                else:
                    self._clear_hover_tooltip(force=True)
            else:
                self._spawn_particles(world, "spark", 14)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        pos = QtCore.QPointF(event.position())
        if self._dragging:
            delta = pos - self._drag_start
            self._drag_distance = max(self._drag_distance, abs(delta.x()) + abs(delta.y()))
            self._note_user_camera_interaction()
            self._set_target_view(pan=self._target_pan + delta)
            self._drag_start = pos
            self.update()
        world = self._map_to_world(pos)
        self._cursor_world_raw = QtCore.QPointF(world)
        self._cursor_world = self._snap_world_to_cell(world)
        self._update_hover_cell(world)
        state_pos = self._world_to_state_pos(world)
        if state_pos is None:
            self.cell_hovered.emit(None)
        else:
            # _world_to_state_pos returns (row, col), while viewer deployment API expects (x=col, y=row).
            self.cell_hovered.emit((int(state_pos[1]), int(state_pos[0])))
        self._update_hover_tooltip(event, world, pos)
        self._update_shooting_hover_target(pos)
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            if self._drag_distance < 4:
                self._last_click_screen = QtCore.QPointF(event.position())
                self._select_unit_at(event.position())
                world = self._map_to_world(QtCore.QPointF(event.position()))
                state_pos = self._world_to_state_pos(world)
                if state_pos is not None:
                    # _world_to_state_pos returns (row, col), while click contract is (x=col, y=row).
                    self.cell_clicked.emit(int(state_pos[1]), int(state_pos[0]))
                self._spawn_particles(world, "smoke", 16)
            self._dragging = False
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self._hover_cell = None
        self.cell_hovered.emit(None)
        self._clear_hover_tooltip()
        self._shoot_hovered_target_key = None
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
        if key == QtCore.Qt.Key_R and self._should_show_shooting():
            self._show_shoot_range_cells = not self._show_shoot_range_cells
            self.shoot_overlay_mode_changed.emit(self.shooting_overlay_mode_label())
            self.refresh_overlays()
            self.update()
            return
        super().keyPressEvent(event)

    def _select_unit_at(self, pos: QtCore.QPointF) -> None:
        world = self._map_to_world(pos)
        from app.viewer.rendering.hit_test import pick_unit_world

        closest_key = pick_unit_world(world, self._units)
        if closest_key:
            was_key = self._selected_unit_key
            self.set_selected_unit(closest_key[0], closest_key[1])
            if closest_key != was_key:
                self.unit_selected.emit(closest_key[0], closest_key[1])
        self.update()

    def _clear_hover_tooltip(self, force: bool = False) -> None:
        if self._tooltip_pinned and not force:
            return
        if self._hover_unit_key is None and self._hover_terrain_feature is None and not self._hover_tooltip_text:
            return
        self._hover_unit_key = None
        self._hover_terrain_feature = None
        self._hover_tooltip_text = None
        self._hover_candidate_key = None
        self._hover_weapon_range = None
        self._hover_status_enemy_ids = []
        self._tooltip_widget.hide_animated()
        self._terrain_tooltip_widget.hide_animated()
        if self._tooltip_follow_timer.isActive():
            self._tooltip_follow_timer.stop()

    def _draw_ground_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.ground import paint_ground_layer

        self._paint_board_layer(painter, paint_ground_layer, layer_name="ground")

    def _draw_decals_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.decals import paint_decals_layer

        self._paint_board_layer(painter, paint_decals_layer, layer_name="decals")

    def _draw_props_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.terrain_props import paint_terrain_props_layer

        self._paint_board_layer(painter, paint_terrain_props_layer, layer_name="terrain_props")

    def _terrain_texture_by_name(self, sprite_name: str) -> Optional[QtGui.QPixmap]:
        key = str(sprite_name or "").strip()
        if not key:
            return None
        cached = self._terrain_texture_cache.get(key)
        if cached is not None:
            return cached
        rel_path = f"props/terrain/{key}"
        pixmap = self._texture_manager.load_png(rel_path)
        if pixmap is None:
            return None
        self._terrain_texture_cache[key] = pixmap
        return pixmap

    def _terrain_content_rect(self, sprite_name: str, pixmap: QtGui.QPixmap) -> QtCore.QRectF:
        key = str(sprite_name or "").strip()
        cached = self._terrain_source_rect_cache.get(key)
        if cached is not None:
            return cached
        if pixmap.isNull():
            fallback = QtCore.QRectF(0, 0, 1, 1)
            if key:
                self._terrain_source_rect_cache[key] = fallback
            return fallback

        image = pixmap.toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        width = image.width()
        height = image.height()
        alpha_threshold = 10
        min_x, min_y = width, height
        max_x, max_y = -1, -1

        for y in range(height):
            for x in range(width):
                if QtGui.qAlpha(image.pixel(x, y)) <= alpha_threshold:
                    continue
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

        if max_x < min_x or max_y < min_y:
            rect = QtCore.QRectF(0, 0, width, height)
        else:
            rect = QtCore.QRectF(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

        if key:
            self._terrain_source_rect_cache[key] = rect
        return rect

    @staticmethod
    def _fit_pixmap_in_rect(
        pixmap: QtGui.QPixmap,
        target_rect: QtCore.QRectF,
        *,
        inset_ratio: float = 1.0,
        source_rect: Optional[QtCore.QRectF] = None,
    ) -> QtCore.QRectF:
        if pixmap.isNull() or target_rect.width() <= 0 or target_rect.height() <= 0:
            return target_rect
        source = source_rect or QtCore.QRectF(0, 0, pixmap.width(), pixmap.height())
        tex_w = max(1.0, float(source.width()))
        tex_h = max(1.0, float(source.height()))
        s = min(target_rect.width() / tex_w, target_rect.height() / tex_h)
        s *= max(0.01, float(inset_ratio))
        draw_w = tex_w * s
        draw_h = tex_h * s
        draw_x = target_rect.x() + (target_rect.width() - draw_w) * 0.5
        draw_y = target_rect.y() + (target_rect.height() - draw_h) * 0.5
        return QtCore.QRectF(draw_x, draw_y, draw_w, draw_h)

    def _draw_particles_layer(self, painter: QtGui.QPainter) -> None:
        if not self._particles or not self._fx_particle_textures:
            return
        painter.save()
        painter.setClipRect(self._board_rect)
        for particle in self._particles:
            pixmap = self._fx_particle_textures.get(particle.texture_key)
            if pixmap is None:
                continue
            painter.setCompositionMode(
                QtGui.QPainter.CompositionMode_Plus
                if particle.mode == "additive"
                else QtGui.QPainter.CompositionMode_SourceOver
            )
            alpha = max(0.0, min(1.0, particle.alpha * (1.0 - particle.age / particle.life)))
            size_scale = particle.size_px * (1.0 + 0.35 * (particle.age / particle.life))
            max_dim = max(1.0, float(max(pixmap.width(), pixmap.height())))
            self._draw_sprite(
                painter,
                pixmap,
                particle.position,
                rotation_deg=0.0,
                scale=size_scale / max_dim,
                alpha=alpha,
            )
        painter.restore()

    def _viewer_perf_tick(self) -> None:
        if not os.environ.get("VIEWER_PERF_INSTRUMENT"):
            return
        now = perf_counter()
        if self._perf_last_mono is not None:
            self._perf_frame_ms.append((now - self._perf_last_mono) * 1000.0)
        self._perf_last_mono = now
        self._perf_frames_since_report += 1
        try:
            interval = max(30, int(os.environ.get("VIEWER_PERF_REPORT_FRAMES", "300")))
        except ValueError:
            interval = 300
        max_samples = 12000
        extra = len(self._perf_frame_ms) - max_samples
        if extra > 0:
            del self._perf_frame_ms[:extra]
        if self._perf_frames_since_report >= interval:
            self._perf_frames_since_report = 0
            self._viewer_perf_emit_report()

    def _viewer_perf_emit_report(self) -> None:
        arr = self._perf_frame_ms
        if len(arr) < 5:
            return
        sorted_ms = sorted(arr)

        def pct(p: float) -> float:
            idx = min(len(sorted_ms) - 1, max(0, int(round(p * (len(sorted_ms) - 1)))))
            return sorted_ms[idx]

        p50 = pct(0.50)
        p95 = pct(0.95)
        print(
            f"[VIEWER_PERF] samples={len(arr)} p50_ms={p50:.3f} p95_ms={p95:.3f}",
            flush=True,
        )

    def _paint_board_layer(self, painter: QtGui.QPainter, paint_fn, *, layer_name: str = "") -> None:
        """Dispatch modular paint passes (Sprint 4)."""
        from app.viewer.rendering.layer_context import LayerContext

        ctx = LayerContext(self, painter)
        if self._layers_v2 and os.environ.get("VIEWER_LAYER_MS"):
            t0 = perf_counter()
            paint_fn(ctx)
            dt_ms = (perf_counter() - t0) * 1000.0
            label = layer_name or getattr(paint_fn, "__name__", "layer")
            print(f"[VIEWER_LAYER] {label} {dt_ms:.3f} ms", flush=True)
            return
        paint_fn(ctx)

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
            self._viewer_perf_tick()
            painter.end()
            return

        self._paint_serial += 1

        painter.setTransform(self._view_transform())
        self._draw_ground_layer(painter)
        painter.setTransform(QtGui.QTransform())
        self._draw_grid(painter)
        painter.setTransform(self._view_transform())
        self._draw_movement_layer(painter)
        self._draw_log_movement_overlay_layer(painter)
        self._draw_objective_layer(painter)
        self._draw_deploy_ghost_layer(painter)
        self._draw_platform_fx_layer(painter)
        if self.render_terrain:
            self.draw_terrain_features(painter)
        if self.render_decals or self._fx_scorch_decals:
            self._draw_decals_layer(painter)
        self._draw_hovered_terrain_cells_layer(painter)
        self._draw_unit_tooltip_overlays_layer(painter)
        self._draw_shooting_layer(painter, target_pass="under")
        # Подсветка хода ИИ — на земле, до спрайтов (иначе «полоса» режет модели по поясу)
        self._draw_selection_layer(painter)
        self._draw_units_layer(painter)
        self._draw_deploy_snap_fx_layer(painter)
        self._draw_shooting_layer(painter, target_pass="over")
        if self.render_fx:
            self._draw_fx_layer(painter)
        self._draw_squad_status_layer(painter)
        self._draw_damage_popups_layer(painter)
        self._draw_ai_phase_badge_layer(painter)
        self._draw_labels_layer(painter)

        painter.setTransform(QtGui.QTransform())
        from app.viewer.rendering.layers.debug_overlay import paint_debug_overlay_layer

        self._paint_board_layer(painter, paint_debug_overlay_layer, layer_name="debug_overlay")

        self._viewer_perf_tick()
        painter.end()

    def _draw_movement_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.movement import paint_movement_layer

        self._paint_board_layer(painter, paint_movement_layer, layer_name="movement")

    def _draw_damage_popups_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.damage_popups import paint_damage_popups_layer

        self._paint_board_layer(painter, paint_damage_popups_layer, layer_name="damage_popups")

    def _draw_objective_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.objectives import paint_objectives_layer

        self._paint_board_layer(painter, paint_objectives_layer, layer_name="objectives")

    def _resolve_render_facing(self, unit: Optional[dict]) -> str:
        if not isinstance(unit, dict):
            return "right"
        raw = str(unit.get("facing") or "").strip().lower()
        if raw in {"left", "right"}:
            return raw
        x_val = unit.get("x")
        board_w = self._board_width or ENV_BOARD_WIDTH
        try:
            x = float(x_val)
        except (TypeError, ValueError):
            return "right"
        return "right" if x < (float(board_w) / 2.0) else "left"

    def _draw_pixmap_with_facing(self, painter: QtGui.QPainter, rect: QtCore.QRectF, pixmap: QtGui.QPixmap, facing: str) -> None:
        if facing == "left":
            painter.save()
            painter.translate(rect.x() + rect.width(), 0.0)
            painter.scale(-1.0, 1.0)
            mirrored_rect = QtCore.QRectF(0.0, rect.y(), rect.width(), rect.height())
            painter.drawPixmap(mirrored_rect, pixmap, QtCore.QRectF(pixmap.rect()))
            painter.restore()
            return
        painter.drawPixmap(rect, pixmap, QtCore.QRectF(pixmap.rect()))

    def _viewer_dim_non_active_enabled(self) -> bool:
        # По умолчанию без приглушения; включить: VIEWER_DIM_NON_ACTIVE=1
        return str(os.getenv("VIEWER_DIM_NON_ACTIVE", "0")).strip() == "1"

    def _opacity_for_unit_render(self, render: UnitRender) -> float:
        if not self._viewer_dim_non_active_enabled():
            return 1.0
        if not self._ai_activation_key and not self._ai_activation_meta:
            return 1.0
        side = render.key[0]
        if side == "player":
            return 0.42
        if side == "model" and render.key != self._ai_activation_key:
            return 0.88
        return 1.0

    def _draw_units_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.units import paint_units_layer

        self._paint_board_layer(painter, paint_units_layer, layer_name="units")

    def _draw_deploy_ghost_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.deploy_ghost import paint_deploy_ghost_layer

        self._paint_board_layer(painter, paint_deploy_ghost_layer, layer_name="deploy_ghost")

    def _draw_selection_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.selection import paint_selection_layer

        self._paint_board_layer(painter, paint_selection_layer, layer_name="selection")

    def _ai_phase_badge_anchor_world(self, render: UnitRender) -> Tuple[float, float]:
        """Центр X и нижняя грань плашки (мир): сразу над блоком HP отряда."""
        compact_mode = self._scale < 0.55
        unit = self._unit_state_by_key.get(render.key)
        if isinstance(unit, dict):
            status = self._interpolate_status(render.key)
            if status is not None:
                layout = self._build_status_layout(render, status, compact_mode)
                hp_text_font = Theme.font(size=7 if compact_mode else 8, bold=True)
                fm = QtGui.QFontMetrics(hp_text_font)
                text_block_h = 0.0 if compact_mode else float(fm.height() + 2)
                hud_top = layout.top_y - 2.0 - text_block_h
                gap = 6.0
                return float(layout.center_x), float(hud_top - gap)
        centers = list(render.model_centers or [render.center])
        min_y = min(c.y() for c in centers)
        cx = sum(c.x() for c in centers) / len(centers)
        zoom_safe = self.cell_size * max(0.28, 0.44 / max(0.65, self._scale))
        return float(cx), float(min_y - zoom_safe - self.cell_size * 0.55)

    def _draw_ai_phase_badge_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.ai_phase_badge import paint_ai_phase_badge_layer

        self._paint_board_layer(painter, paint_ai_phase_badge_layer, layer_name="ai_phase_badge")

    def _draw_log_movement_overlay_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.log_movement_overlay import paint_log_movement_overlay_layer

        self._paint_board_layer(painter, paint_log_movement_overlay_layer, layer_name="log_movement")

    def _target_hitbox_for_info(self, info: Dict[str, object]) -> Optional[QtCore.QRectF]:
        from app.viewer.rendering.hit_test import target_hitbox_for_shoot_info

        return target_hitbox_for_shoot_info(info, self._unit_hitboxes_screen)

    def _draw_shooting_targets_overlay(
        self,
        painter: QtGui.QPainter,
        target_infos: List[Dict[str, object]],
        hovered_target_key: Optional[Tuple[str, int]],
        *,
        render_under_units: bool,
    ) -> None:
        from app.viewer.rendering.layer_context import LayerContext
        from app.viewer.rendering.layers.shooting_targets_overlay import paint_shooting_targets_overlay

        paint_shooting_targets_overlay(
            LayerContext(self, painter),
            target_infos,
            hovered_target_key,
            render_under_units=render_under_units,
        )

    def _target_overlay_assets(self) -> Dict[str, Optional[QtGui.QPixmap]]:
        if self._target_overlay_pixmaps:
            return self._target_overlay_pixmaps
        assets = {
            "target_valid_base": "fx/target_valid_base.png",
            "target_obscured_base": "fx/target_obscured_base.png",
            "target_nolos_base": "fx/target_nolos_base.png",
            "target_marker_valid": "fx/target_marker_valid.png",
            "target_marker_obscured": "fx/target_marker_obscured.png",
            "target_marker_nolos": "fx/target_marker_nolos.png",
            "target_hover_ring": "fx/target_hover_ring.png",
        }
        for key, rel_path in assets.items():
            self._target_overlay_pixmaps[key] = self._texture_manager.load_png(rel_path)
        return self._target_overlay_pixmaps

    def _draw_shooting_layer(self, painter: QtGui.QPainter, *, target_pass: str = "over") -> None:
        from app.viewer.rendering.layers.shooting import paint_shooting_layer

        def _paint(ctx):
            paint_shooting_layer(ctx, target_pass=target_pass)

        label = "shooting_under" if str(target_pass).lower() == "under" else "shooting_over"
        self._paint_board_layer(painter, _paint, layer_name=label)

    def _draw_labels_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.labels import paint_labels_layer

        self._paint_board_layer(painter, paint_labels_layer, layer_name="labels")

    def _draw_squad_status_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.squad_status import paint_squad_status_layer

        self._paint_board_layer(painter, paint_squad_status_layer, layer_name="squad_status")

    def _build_status_layout(self, render: UnitRender, status: SquadStatusSnapshot, compact_mode: bool) -> "_StatusLayout":
        bar_w = max(24.0, self.cell_size * (1.55 if compact_mode else 1.9))
        bar_h = 5.0 if compact_mode else 6.0
        pips_h = 0.0 if compact_mode else 3.0
        text_h = 0.0 if compact_mode else 11.0
        spacing_hp_to_pips = 2.0 if compact_mode else 2.4
        spacing_text_to_hp = 2.0 if compact_mode else 2.4
        card_h = text_h + spacing_text_to_hp + bar_h + spacing_hp_to_pips + pips_h
        center_x, top_y = self._status_anchor(render, card_h)
        return _StatusLayout(
            center_x=center_x,
            top_y=top_y,
            bar_w=bar_w,
            bar_h=bar_h,
            pips_y=top_y + bar_h + spacing_hp_to_pips,
        )

    def _draw_squad_hp_bar(
        self,
        painter: QtGui.QPainter,
        key: Tuple[str, int],
        layout: "_StatusLayout",
        status: SquadStatusSnapshot,
        compact_mode: bool,
    ) -> None:
        hp = status.hp
        hp_max = status.hp_max
        if hp is None or hp_max is None or hp_max <= 0:
            return

        rect = QtCore.QRectF(layout.center_x - layout.bar_w / 2.0, layout.top_y, layout.bar_w, layout.bar_h)
        ratio = max(0.0, min(1.0, float(hp) / float(hp_max)))

        bg_rect = rect.adjusted(-1.1, -1.1, 1.1, 1.1)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._status_hp_backplate_color)
        painter.drawRoundedRect(bg_rect, 3.2, 3.2)

        painter.setBrush(self._status_hp_bg_color)
        painter.drawRoundedRect(rect, 2.6, 2.6)

        fill_w = rect.width() * ratio
        if fill_w > 0.7:
            fill_rect = QtCore.QRectF(rect.x(), rect.y(), fill_w, rect.height())
            painter.setBrush(self._hp_color(ratio))
            painter.drawRoundedRect(fill_rect, 2.4, 2.4)

        over_ratio = max(0.0, float(hp) / float(hp_max) - 1.0)
        if over_ratio > 0.0:
            over_w = rect.width() * min(0.3, over_ratio)
            over_rect = QtCore.QRectF(rect.right() - over_w, rect.y(), over_w, rect.height())
            painter.setBrush(self._status_hp_overheal_color)
            painter.drawRoundedRect(over_rect, 2.0, 2.0)

        lag_ratio = self._hp_lag_ratio(key)
        loss_w = rect.width() * max(0.0, lag_ratio - ratio)
        if loss_w >= self._status_hp_loss_min_px:
            lag_rect = QtCore.QRectF(
                rect.x() + rect.width() * ratio,
                rect.y(),
                loss_w,
                rect.height(),
            )
            loss_strength = max(0.0, min(1.0, (lag_ratio - ratio) * 2.2))
            lag_color = self._mix_colors(self._status_hp_lag_color, QtGui.QColor(230, 206, 158, 170), loss_strength)
            painter.setBrush(lag_color)
            painter.drawRoundedRect(lag_rect, 2.0, 2.0)

        hit_flash = self._hp_hit_flash_alpha(key)
        if hit_flash > 0.02:
            edge_x = rect.x() + rect.width() * ratio
            flash_color = QtGui.QColor(240, 220, 170, int(170 * hit_flash))
            flash_pen = QtGui.QPen(flash_color, 1.0 + 1.2 * hit_flash)
            flash_pen.setCosmetic(True)
            painter.setPen(flash_pen)
            painter.drawLine(QtCore.QPointF(edge_x, rect.y() - 0.6), QtCore.QPointF(edge_x, rect.bottom() + 0.6))

        pulse = self._status_crit_pulse(ratio)
        border_w = 1.0 + (0.5 * pulse)
        border_color = self._status_hp_border_color if pulse <= 0.0 else self._mix_colors(
            self._status_hp_border_color,
            self._status_hp_border_crit_color,
            pulse,
        )
        border_pen = QtGui.QPen(border_color, border_w)
        border_pen.setCosmetic(True)
        painter.setPen(border_pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(rect, 2.6, 2.6)

        if pulse > 0.01 and not compact_mode:
            glow = QtCore.QRectF(rect.adjusted(-1.7, -1.2, 1.7, 1.2))
            glow_color = QtGui.QColor(self._status_hp_border_crit_color)
            glow_color.setAlpha(int(56 + 66 * pulse))
            glow_pen = QtGui.QPen(glow_color, 1.2 + 0.8 * pulse)
            glow_pen.setCosmetic(True)
            painter.setPen(glow_pen)
            painter.drawRoundedRect(glow, 3.0, 3.0)

    def _draw_squad_model_pips(
        self,
        painter: QtGui.QPainter,
        key: Tuple[str, int],
        layout: "_StatusLayout",
        status: SquadStatusSnapshot,
    ) -> None:
        total = status.total_models
        alive = status.alive_models
        if total is None or total <= 0:
            return

        alive = max(0, min(total, int(alive if alive is not None else total)))
        max_visible = 14
        draw_total = min(total, max_visible)
        seg_w = 4.8
        seg_h = 2.6
        gap = 1.9
        line_w = draw_total * seg_w + (draw_total - 1) * gap
        x0 = layout.center_x - line_w / 2.0

        progress = self._status_anim_progress()
        prev = self._status_prev.get(key)
        prev_alive = alive if prev is None or prev.alive_models is None else int(prev.alive_models)
        prev_alive = max(0, min(total, prev_alive))

        for idx in range(draw_total):
            is_alive_now = idx < alive
            was_alive = idx < prev_alive
            color = QtGui.QColor(self._status_pip_alive_color if is_alive_now else self._status_pip_lost_color)
            alpha = color.alpha()
            flash_mix = 0.0
            if was_alive and not is_alive_now:
                step = idx - alive
                flash_mix = self._status_pip_loss_flash(progress, step)
                alpha = int(216 - (216 - 142) * min(1.0, max(0.0, progress)))
            color.setAlpha(alpha)
            if flash_mix > 0.0:
                color = self._mix_colors(color, self._status_pip_flash_color, flash_mix)
                color.setAlpha(min(255, int(alpha + 38 * flash_mix)))

            rect = QtCore.QRectF(x0 + idx * (seg_w + gap), layout.pips_y, seg_w, seg_h)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(color)
            painter.drawRoundedRect(rect, 0.95, 0.95)

    def _draw_squad_hp_text(
        self,
        painter: QtGui.QPainter,
        center_x: float,
        y: float,
        status: SquadStatusSnapshot,
        font: QtGui.QFont,
    ) -> None:
        hp = status.hp
        hp_max = status.hp_max
        if hp is None:
            return
        if hp_max is not None and hp_max > 0:
            label = f"{int(round(hp))}/{int(round(hp_max))}"
        else:
            label = f"{int(round(hp))}"
        painter.save()
        painter.setFont(font)
        metrics = QtGui.QFontMetrics(font)
        text_w = metrics.horizontalAdvance(label) + 6
        text_h = metrics.height() + 2
        rect = QtCore.QRectF(center_x - text_w / 2.0, y - text_h, text_w, text_h)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._status_hp_text_bg)
        painter.drawRoundedRect(rect, 3.0, 3.0)
        painter.setPen(self._status_hp_text_color)
        painter.drawText(rect, QtCore.Qt.AlignCenter, label)
        painter.restore()

    def _status_anchor(self, render: UnitRender, card_height_px: float) -> Tuple[float, float]:
        centers = render.model_centers or [render.center]
        min_x = min(point.x() for point in centers)
        max_x = max(point.x() for point in centers)
        min_y = min(point.y() for point in centers)
        max_y = max(point.y() for point in centers)
        span_x = max(1.0, max_x - min_x)
        span_y = max(1.0, max_y - min_y)
        center_x = (min_x + max_x) * 0.5

        density = span_x / max(1.0, float(self.cell_size))
        x_shift = 0.0
        if density < 1.0 and len(centers) >= 5:
            x_shift = min(self.cell_size * 0.16, (1.0 - density) * self.cell_size * 0.24)
            x_shift *= -1.0 if int(render.key[1]) % 2 else 1.0

        zoom_safe_offset = self.cell_size * max(0.28, 0.44 / max(0.65, self._scale))
        formation_headroom = span_y * 0.5
        card_pad = card_height_px + (self.cell_size * 0.12)
        top_y = min_y - (zoom_safe_offset + formation_headroom + card_pad)
        center_x += x_shift

        margin = self.cell_size * 0.25
        board_left = self._board_rect.left() + margin
        board_right = self._board_rect.right() - margin
        board_top = self._board_rect.top() + margin
        board_bottom = self._board_rect.bottom() - margin
        center_x = max(board_left, min(board_right, center_x))
        top_y = max(board_top, min(board_bottom - card_height_px, top_y))
        return center_x, top_y

    def _extract_squad_status(self, unit: dict) -> SquadStatusSnapshot:
        hp = self._coerce_number(unit.get("wounds", unit.get("hp")))
        hp_max = self._coerce_number(
            unit.get("max_wounds", unit.get("wounds_max", unit.get("max_hp", unit.get("wounds", unit.get("hp")))))
        )
        alive = self._safe_int(unit.get("alive_models"))
        total = self._safe_int(unit.get("models", unit.get("max_models")))
        if alive is None and total is not None:
            alive = total
        if alive is not None:
            alive = max(0, alive)
        if total is not None:
            total = max(0, total)
        return SquadStatusSnapshot(hp=hp, hp_max=hp_max, alive_models=alive, total_models=total)

    def _interpolate_status(self, key: Tuple[str, int]) -> Optional[SquadStatusSnapshot]:
        current = self._status_curr.get(key)
        if current is None:
            return None
        previous = self._status_prev.get(key, current)
        hp_t = self._status_anim_progress(duration_s=self._status_hp_fast_duration_s)
        hp = self._lerp_optional(previous.hp, current.hp, hp_t)
        hp_max = self._lerp_optional(previous.hp_max, current.hp_max, hp_t)
        alive_models = self._step_models(previous.alive_models, current.alive_models, self._status_anim_progress())
        return SquadStatusSnapshot(
            hp=hp,
            hp_max=hp_max,
            alive_models=alive_models,
            total_models=current.total_models,
        )

    def _status_anim_progress(self, *, duration_s: Optional[float] = None) -> float:
        elapsed = max(0.0, monotonic() - self._status_anim_t0)
        duration = self._status_anim_duration_s if duration_s is None else float(duration_s)
        if duration <= 0.0:
            return 1.0
        return max(0.0, min(1.0, elapsed / duration))

    def _lerp_optional(self, start: Optional[float], end: Optional[float], t: float) -> Optional[float]:
        if end is None:
            return start
        if start is None:
            return end
        eased = self._ease_out_cubic(t)
        return start + (end - start) * eased

    def _step_models(self, start: Optional[int], end: Optional[int], t: float) -> Optional[int]:
        if end is None:
            return start
        if start is None:
            return end
        if start <= end:
            return end
        drop = start - end
        max_steps = max(1, drop)
        step_interval = self._status_pip_step_s / max(0.001, self._status_anim_duration_s)
        completed = min(drop, max(0, int((t + 1e-6) / max(step_interval, 1e-4))))
        value = start - min(max_steps, completed)
        return max(end, value)

    def _hp_color(self, ratio: float) -> QtGui.QColor:
        if ratio < self._status_hp_crit_threshold:
            return QtGui.QColor(166, 74, 66, 236)
        if ratio < 0.6:
            return QtGui.QColor(184, 162, 88, 236)
        return QtGui.QColor(98, 146, 94, 236)

    def _hp_lag_ratio(self, key: Tuple[str, int]) -> float:
        lag_from = self._status_hp_lag_from_ratio.get(key)
        lag_to = self._status_hp_lag_to_ratio.get(key)
        lag_t0 = self._status_hp_lag_t0.get(key)
        if lag_from is not None and lag_to is not None and lag_t0 is not None:
            t = max(0.0, min(1.0, (monotonic() - lag_t0) / max(0.001, self._status_hp_lag_duration_s)))
            eased = self._ease_in_out_cubic(t)
            value = lag_from + (lag_to - lag_from) * eased
            if t >= 1.0:
                self._status_hp_lag_from_ratio.pop(key, None)
                self._status_hp_lag_to_ratio.pop(key, None)
                self._status_hp_lag_t0.pop(key, None)
            return max(0.0, min(1.4, value))

        current = self._status_curr.get(key)
        prev = self._status_prev.get(key)
        if current is None or prev is None:
            return 0.0
        if current.hp is None or prev.hp is None or current.hp_max is None or current.hp_max <= 0:
            return 0.0
        cur_ratio = max(0.0, min(1.4, float(current.hp) / float(current.hp_max)))
        prev_ratio = max(0.0, min(1.4, float(prev.hp) / float(current.hp_max)))
        lag_t = self._status_anim_progress(duration_s=self._status_hp_lag_duration_s)
        return prev_ratio - (prev_ratio - cur_ratio) * self._ease_in_out_cubic(lag_t)

    def _status_crit_pulse(self, ratio: float) -> float:
        if ratio >= self._status_hp_crit_threshold:
            return 0.0
        phase = (max(0.0, monotonic() - self._status_anim_t0) / max(0.2, self._status_crit_pulse_period_s)) * math.tau
        wave = 0.5 + 0.5 * math.sin(phase)
        severity = 1.0 - max(0.0, min(1.0, ratio / max(0.001, self._status_hp_crit_threshold)))
        return wave * (0.35 + 0.65 * severity)

    def _refresh_hp_loss_anim(self, now_ts: float) -> None:
        active_keys = set(self._status_curr.keys())
        for key in list(self._status_hp_lag_from_ratio.keys()):
            if key not in active_keys:
                self._status_hp_lag_from_ratio.pop(key, None)
                self._status_hp_lag_to_ratio.pop(key, None)
                self._status_hp_lag_t0.pop(key, None)
                self._status_hp_last_drop_t.pop(key, None)
                self._status_hp_hit_mag.pop(key, None)

        for key, current in self._status_curr.items():
            previous = self._status_prev.get(key)
            cur_ratio = self._hp_ratio_from_snapshot(current)
            prev_ratio = self._hp_ratio_from_snapshot(previous)
            if cur_ratio is None or prev_ratio is None:
                continue
            if prev_ratio <= cur_ratio + 1e-4:
                continue

            last_drop = self._status_hp_last_drop_t.get(key)
            existing_from = self._status_hp_lag_from_ratio.get(key)
            existing_to = self._status_hp_lag_to_ratio.get(key)
            existing_t0 = self._status_hp_lag_t0.get(key)
            coalesce = (
                last_drop is not None
                and existing_from is not None
                and existing_to is not None
                and existing_t0 is not None
                and (now_ts - last_drop) <= self._status_hp_coalesce_window_s
            )

            if coalesce:
                self._status_hp_lag_to_ratio[key] = min(existing_to, cur_ratio)
                self._status_hp_hit_mag[key] = max(
                    self._status_hp_hit_mag.get(key, 0.0),
                    max(0.0, existing_from - self._status_hp_lag_to_ratio[key]),
                )
            else:
                lag_start = max(prev_ratio, self._hp_lag_ratio(key))
                self._status_hp_lag_from_ratio[key] = lag_start
                self._status_hp_lag_to_ratio[key] = cur_ratio
                self._status_hp_lag_t0[key] = now_ts
                self._status_hp_hit_mag[key] = max(0.0, lag_start - cur_ratio)
            self._status_hp_last_drop_t[key] = now_ts

    @staticmethod
    def _hp_ratio_from_snapshot(snapshot: Optional[SquadStatusSnapshot]) -> Optional[float]:
        if snapshot is None or snapshot.hp is None or snapshot.hp_max is None or snapshot.hp_max <= 0:
            return None
        return max(0.0, min(1.4, float(snapshot.hp) / float(snapshot.hp_max)))

    def _hp_hit_flash_alpha(self, key: Tuple[str, int]) -> float:
        t0 = self._status_hp_last_drop_t.get(key)
        mag = self._status_hp_hit_mag.get(key, 0.0)
        if t0 is None or mag <= 0.0:
            return 0.0
        dt = monotonic() - t0
        if dt <= 0.0 or dt >= self._status_hp_hit_flash_s:
            return 0.0
        local = dt / max(0.001, self._status_hp_hit_flash_s)
        tri = 1.0 - abs(2.0 * local - 1.0)
        return max(0.0, min(1.0, tri * min(1.0, mag * 4.0)))

    @staticmethod
    def _ease_out_cubic(t: float) -> float:
        t = max(0.0, min(1.0, float(t)))
        return 1.0 - pow(1.0 - t, 3)

    @staticmethod
    def _ease_in_out_cubic(t: float) -> float:
        t = max(0.0, min(1.0, float(t)))
        if t < 0.5:
            return 4.0 * t * t * t
        return 1.0 - pow(-2.0 * t + 2.0, 3) / 2.0

    def _status_pip_loss_flash(self, progress: float, step: int) -> float:
        step_delay = self._status_pip_step_s / max(0.001, self._status_anim_duration_s)
        local_t = progress - step * step_delay
        if local_t <= 0.0:
            return 0.0
        if local_t < 0.32:
            return min(1.0, local_t / 0.32)
        if local_t < 0.9:
            return max(0.0, 1.0 - (local_t - 0.32) / 0.58)
        return 0.0

    @staticmethod
    def _mix_colors(a: QtGui.QColor, b: QtGui.QColor, t: float) -> QtGui.QColor:
        t = max(0.0, min(1.0, float(t)))
        return QtGui.QColor(
            int(a.red() + (b.red() - a.red()) * t),
            int(a.green() + (b.green() - a.green()) * t),
            int(a.blue() + (b.blue() - a.blue()) * t),
            int(a.alpha() + (b.alpha() - a.alpha()) * t),
        )


    def _tick_fx(self) -> None:
        now = monotonic()
        if now < float(getattr(self, "_damage_popup_hit_stop_until", 0.0) or 0.0):
            self._particles_last_ts = now
            if self.isVisible():
                self.update()
            return
        if self._particles_last_ts is None:
            self._particles_last_ts = now
        dt = now - self._particles_last_ts
        self._particles_last_ts = now
        if self._particles:
            remaining: List[ParticleInstance] = []
            for particle in self._particles:
                particle.age += dt
                if particle.age >= particle.life:
                    continue
                particle.position = QtCore.QPointF(
                    particle.position.x() + particle.velocity.x() * dt,
                    particle.position.y() + particle.velocity.y() * dt,
                )
                remaining.append(particle)
            self._particles = remaining
        if self._deploy_placement_fx:
            self._deploy_placement_fx = [
                fx for fx in self._deploy_placement_fx
                if (now - fx.t0) < fx.duration
            ]
        if self._damage_popups_active:
            self._damage_popups_active = [
                popup for popup in self._damage_popups_active
                if (now - popup.created_t) < popup.ttl_s
            ]
        if self._damage_popup_dedup_seen:
            self._damage_popup_dedup_seen = {
                key: ts for key, ts in self._damage_popup_dedup_seen.items()
                if (now - ts) <= max(self._damage_popup_ttl_s * 2.0, 2.0)
            }
        if self._fx_scorch_decals:
            self._fx_scorch_decals = [
                decal for decal in self._fx_scorch_decals
                if (now - decal.created_t) < decal.ttl_s
            ]
        if self.isVisible():
            self.update()

    def _load_fx_assets(self) -> None:
        if self._fx_initialized:
            return
        assets_dir = resolve_asset_path("fx")
        for name in (
            "glow_soft",
            "ring_soft",
            "tesseract_segments",
            "gauss_muzzle_atlas",
            "gauss_glow_radial",
            "gauss_noise_stripe",
            "gauss_scorch_decal",
            "necron_glyphs_atlas",
            "gauss_impact_ring",
        ):
            path = assets_dir / f"{name}.png"
            if not path.exists():
                continue
            image = QtGui.QImage(str(path))
            if image.isNull():
                continue
            pixmap = QtGui.QPixmap.fromImage(image)
            self._fx_pixmaps[name] = pixmap
        platform_assets = {
            "highlight_platform/base": "highlight_platform/platform_base_512.png",
            "highlight_platform/glow": "highlight_platform/platform_glow_512.png",
            "highlight_platform/noise": "highlight_platform/platform_noise_tile_256.png",
            "highlight_platform/scanlines": "highlight_platform/scanlines_tile_256.png",
            "highlight_platform/sparkle": "highlight_platform/sparkle_particle_64.png",
        }
        for key, rel_path in platform_assets.items():
            path = assets_dir / rel_path
            if not path.exists():
                continue
            image = QtGui.QImage(str(path))
            if image.isNull():
                continue
            self._fx_pixmaps[key] = QtGui.QPixmap.fromImage(image)
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
        key = self._norm_unit_key(unit.get("side"), unit.get("id"))
        if key is None:
            return None
        return self._unit_by_key.get(key)

    def unit_shoot_anchor_world(
        self, side: Optional[str], unit_id: int
    ) -> Optional[QtCore.QPointF]:
        """Screen-space anchor for weapon FX: centroid of model icons, else squad center."""
        key = self._norm_unit_key(side, unit_id)
        if key is None:
            return None
        render = self._unit_by_key.get(key)
        if render is None:
            return None
        centers = render.model_centers
        if centers:
            n = len(centers)
            return QtCore.QPointF(
                sum(p.x() for p in centers) / n,
                sum(p.y() for p in centers) / n,
            )
        return QtCore.QPointF(render.center)

    def _is_necron(self, unit: Optional[dict]) -> bool:
        if not unit:
            return False
        faction = str(unit.get("faction") or "")
        name = str(unit.get("name") or "")
        return faction.lower() == "necrons" or "necron" in name.lower()

    def _normalize_unit_name(self, unit_name: str) -> str:
        normalized = unit_name.strip().lower().replace("-", " ")
        return " ".join(normalized.split())

    def _build_unit_icon_map(self) -> Dict[str, QtGui.QPixmap]:
        icon_links = {
            "Necron Warriors": "icons/necron_warriors_icon.png",
            "Royal Warden": "icons/royal_warden_icon.png",
            "Canoptek Scarab Swarms": "icons/canoptek_scarab_swarms_icon.png",
        }
        name_aliases = {
            "warriors": "Necron Warriors",
            "necron warrior": "Necron Warriors",
            "royal warden": "Royal Warden",
            "canoptek scarab swarm": "Canoptek Scarab Swarms",
            "scarab swarms": "Canoptek Scarab Swarms",
        }

        icon_map: Dict[str, QtGui.QPixmap] = {}
        for raw_name, rel_path in icon_links.items():
            pixmap = self._texture_manager.load_png(rel_path)
            if pixmap is None or pixmap.isNull():
                continue
            normalized = self._normalize_unit_name(raw_name)
            icon_map[normalized] = pixmap

        for alias, canonical in name_aliases.items():
            canonical_key = self._normalize_unit_name(canonical)
            if canonical_key not in icon_map:
                continue
            icon_map[self._normalize_unit_name(alias)] = icon_map[canonical_key]

        return icon_map

    def _icon_for_unit_name(self, unit_name: str) -> Optional[QtGui.QPixmap]:
        key = self._normalize_unit_name(unit_name)
        if key in self._unit_icon_by_name:
            return self._unit_icon_by_name[key]

        # Fallback: иконка подтягивается даже при небольшом расхождении имени из ростера.
        for known_key, pixmap in self._unit_icon_by_name.items():
            if known_key and (known_key in key or key in known_key):
                return pixmap
        return None

    def _build_faction_icon_map(self) -> Dict[str, QtGui.QPixmap]:
        icon_links = {
            "NECRONS": "../gui_qt/assets/necrons.png",
        }
        icon_map: Dict[str, QtGui.QPixmap] = {}
        for keyword, rel_path in icon_links.items():
            pixmap = self._texture_manager.load_png(rel_path)
            if pixmap is None or pixmap.isNull():
                continue
            icon_map[keyword.upper()] = pixmap
        return icon_map

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

    def _draw_deploy_snap_fx_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.deploy_snap_fx import paint_deploy_snap_fx_layer

        self._paint_board_layer(painter, paint_deploy_snap_fx_layer, layer_name="deploy_snap_fx")

    def _draw_fx_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.fx import paint_fx_layer

        self._paint_board_layer(painter, paint_fx_layer, layer_name="fx")

    def _draw_platform_fx_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.platform_fx import paint_platform_fx_layer

        self._paint_board_layer(painter, paint_platform_fx_layer, layer_name="platform_fx")

    def _resolve_unit_by_key_or_id(
        self,
        unit_side: Optional[str],
        unit_id: Optional[int],
    ) -> Tuple[Optional[dict], Optional[UnitRender]]:
        if unit_id is None:
            return None, None
        unit = None
        render = None
        if unit_side is not None:
            key = (unit_side, unit_id)
            render = self._unit_by_key.get(key)
            unit = self._state_unit(key)
        if render is None:
            unit = self._find_unit_by_id(unit_id)
            render = self._unit_render_for_unit(unit)
            if render is not None and unit is None:
                unit = self._state_unit(render.key)
        return unit, render

    def _platform_rect_for_render(self, render: UnitRender, unit: Optional[dict]) -> QtCore.QRectF:
        # Если есть явные позиции моделей в state, считаем platform от них.
        model_centers: List[QtCore.QPointF] = []
        model_positions = unit.get("model_positions") if isinstance(unit, dict) else None
        if isinstance(model_positions, list):
            for pos in model_positions:
                if not isinstance(pos, dict):
                    continue
                view_cell = self._state_to_view_cell(pos.get("x"), pos.get("y"))
                if view_cell is None:
                    continue
                model_centers.append(
                    QtCore.QPointF(
                        view_cell[0] * self.cell_size + self.cell_size / 2,
                        view_cell[1] * self.cell_size + self.cell_size / 2,
                    )
                )
        if not model_centers and render.model_centers:
            model_centers = list(render.model_centers)

        if model_centers:
            min_x = min(center.x() for center in model_centers)
            max_x = max(center.x() for center in model_centers)
            min_y = min(center.y() for center in model_centers)
            max_y = max(center.y() for center in model_centers)
            bbox_width_cells = (max_x - min_x) / self.cell_size
            bbox_height_cells = (max_y - min_y) / self.cell_size
            rx_cells = (bbox_width_cells * 0.5) + 0.6
            ry_cells = (bbox_height_cells * 0.5) + 0.6
            rx_cells = max(1.4, min(rx_cells, 4.8))
            ry_cells = max(0.9, min(ry_cells, 3.2))

            centroid_x = sum(center.x() for center in model_centers) / len(model_centers)
            centroid_y = sum(center.y() for center in model_centers) / len(model_centers)
            center = QtCore.QPointF(
                centroid_x,
                centroid_y + self.cell_size * 0.32,
            )
            width = rx_cells * 2.0 * self.cell_size
            height = ry_cells * 2.0 * self.cell_size
            return QtCore.QRectF(
                center.x() - width * 0.5,
                center.y() - height * 0.5,
                width,
                height,
            )

        # Fallback: старый якорный размер, если позиции моделей недоступны.
        width = self.cell_size * 2.8
        height = self.cell_size * 1.2
        center = QtCore.QPointF(render.center.x(), render.center.y() + self.cell_size * 0.2)
        return QtCore.QRectF(
            center.x() - width * 0.5,
            center.y() - height * 0.5,
            width,
            height,
        )

    def _draw_soft_radial_glow_ellipse(
        self,
        painter: QtGui.QPainter,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        color: QtGui.QColor,
        strength: float,
        *,
        composition: QtGui.QPainter.CompositionMode,
        peak_alpha: int,
        mid_stop: float = 0.55,
    ) -> None:
        """Плавный ореол без прямоугольных краёв спрайта (градиент в нормализованном эллипсе)."""
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setCompositionMode(composition)
        painter.setPen(QtCore.Qt.NoPen)
        painter.translate(cx, cy)
        painter.scale(max(rx, 1e-6), max(ry, 1e-6))
        grad = QtGui.QRadialGradient(0.0, 0.0, 1.0)
        a0 = int(max(0, min(255, int(peak_alpha * strength))))
        grad.setColorAt(0.0, QtGui.QColor(color.red(), color.green(), color.blue(), a0))
        grad.setColorAt(mid_stop, QtGui.QColor(color.red(), color.green(), color.blue(), int(a0 * 0.38)))
        grad.setColorAt(0.78, QtGui.QColor(color.red(), color.green(), color.blue(), int(a0 * 0.14)))
        grad.setColorAt(0.92, QtGui.QColor(color.red(), color.green(), color.blue(), int(a0 * 0.04)))
        grad.setColorAt(1.0, QtGui.QColor(color.red(), color.green(), color.blue(), 0))
        painter.setBrush(QtGui.QBrush(grad))
        painter.drawEllipse(QtCore.QRectF(-1.0, -1.0, 2.0, 2.0))
        painter.restore()

    def _draw_platform_highlight(
        self,
        painter: QtGui.QPainter,
        render: UnitRender,
        color: QtGui.QColor,
        strength: float,
        pulse: float,
        t: float,
        *,
        pulse_strength: float = 1.0,
        glow_scale: float = 1.0,
        noise_scale: float = 1.0,
        scan_scale: float = 1.0,
        sparkle_scale: float = 1.0,
    ) -> None:
        rect = self._platform_rect_for_render(render, self._state_unit(render.key))
        if rect.isEmpty():
            return

        base_pixmap = self._tinted_pixmap("highlight_platform/base", color)
        glow_pixmap = self._tinted_pixmap("highlight_platform/glow", color)
        noise_pixmap = self._tinted_pixmap("highlight_platform/noise", color)
        scan_pixmap = self._tinted_pixmap("highlight_platform/scanlines", color)
        sparkle_pixmap = self._tinted_pixmap("highlight_platform/sparkle", color)

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        fx_pulse = 1.0 + (pulse - 0.5) * pulse_strength
        glow_margin = rect.height() * (0.34 + 0.06 * pulse * pulse_strength)
        glow_rect = rect.adjusted(-glow_margin, -glow_margin, glow_margin, glow_margin)
        pcx = float(rect.center().x())
        pcy = float(rect.center().y())
        feather_rx = max(glow_rect.width() * 0.51, self.cell_size * 0.35)
        feather_ry = max(glow_rect.height() * 0.48, self.cell_size * 0.30)
        self._draw_soft_radial_glow_ellipse(
            painter,
            pcx,
            pcy,
            feather_rx * 1.08 * glow_scale,
            feather_ry * 1.06 * glow_scale,
            color,
            strength,
            composition=QtGui.QPainter.CompositionMode_SourceOver,
            peak_alpha=48,
        )
        self._draw_soft_radial_glow_ellipse(
            painter,
            pcx,
            pcy,
            feather_rx * 0.78 * glow_scale,
            feather_ry * 0.74 * glow_scale,
            color,
            strength,
            composition=QtGui.QPainter.CompositionMode_Plus,
            peak_alpha=26,
            mid_stop=0.5,
        )
        self._draw_fx_sprite_rect(
            painter,
            glow_pixmap,
            glow_rect,
            opacity=0.20 * strength * (0.82 + 0.18 * pulse * pulse_strength) * glow_scale,
        )
        inner_rect = QtCore.QRectF(rect)
        inner_rect.setWidth(rect.width() * 0.85)
        inner_rect.setHeight(rect.height() * 0.85)
        inner_rect.moveCenter(rect.center())
        self._draw_fx_sprite_rect(
            painter,
            base_pixmap,
            rect,
            opacity=0.35 * strength,
        )
        self._draw_fx_sprite_rect(
            painter,
            base_pixmap,
            inner_rect,
            opacity=0.24 * strength * (0.9 + 0.1 * pulse * pulse_strength),
        )

        clip = QtGui.QPainterPath()
        clip.addEllipse(rect)
        inner_clip = QtGui.QPainterPath()
        ring_core_rect = rect.adjusted(rect.width() * 0.24, rect.height() * 0.24, -rect.width() * 0.24, -rect.height() * 0.24)
        inner_clip.addEllipse(ring_core_rect)
        ring_mask = clip.subtracted(inner_clip)
        painter.save()
        painter.setClipPath(clip)
        if noise_pixmap is not None:
            noise_brush = QtGui.QBrush(noise_pixmap)
            noise_transform = QtGui.QTransform()
            noise_transform.translate((t * 5.12) % 256.0, (t * 2.56) % 256.0)
            noise_brush.setTransform(noise_transform)
            painter.setOpacity(0.07 * strength * noise_scale)
            painter.fillPath(clip, noise_brush)
            painter.setOpacity(0.22 * strength * noise_scale)
            painter.fillPath(ring_mask, noise_brush)
        if scan_pixmap is not None:
            scan_brush = QtGui.QBrush(scan_pixmap)
            scan_transform = QtGui.QTransform()
            scan_transform.translate(0.0, (t * 26.0) % 256.0)
            scan_brush.setTransform(scan_transform)
            painter.setOpacity(0.19 * strength * scan_scale)
            painter.fillPath(clip, scan_brush)
        painter.restore()

        if sparkle_pixmap is not None and sparkle_scale > 0:
            center = rect.center()
            sparkle_count = 6
            base_rx = rect.width() * 0.38
            base_ry = rect.height() * 0.28
            for idx in range(sparkle_count):
                phase = t * (0.65 + idx * 0.11) + idx * 1.37
                sparkle_center = QtCore.QPointF(
                    center.x() + math.cos(phase) * base_rx,
                    center.y() + math.sin(phase * 1.7) * base_ry,
                )
                size = self.cell_size * (0.24 + 0.04 * math.sin(phase * 1.8)) * max(0.4, sparkle_scale)
                sparkle_rect = QtCore.QRectF(
                    sparkle_center.x() - size * 0.5,
                    sparkle_center.y() - size * 0.5,
                    size,
                    size,
                )
                sparkle_alpha = (0.13 + 0.07 * math.sin(phase * 2.1)) * strength * sparkle_scale * fx_pulse
                self._draw_fx_sprite_rect(
                    painter,
                    sparkle_pixmap,
                    sparkle_rect,
                    opacity=max(0.0, sparkle_alpha),
                )
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
        glyph_count_scale = float(config.get("glyph_count_scale", 1.0))
        raw_count = rng.randint(count_min, count_max)
        glyph_count = max(1, int(round(raw_count * glyph_count_scale)))
        glyphs: List[GlyphBlueprint] = []
        glyph_atlas = self._fx_pixmaps.get("necron_glyphs_atlas")
        if glyph_atlas is not None and not glyph_atlas.isNull():
            shape_count = 16
        else:
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

            glow_alpha = 0.55 * ease_out(glow_p) * float(getattr(self, "_fx_gauss_alpha_scale", 1.0) or 1.0)
            core_alpha = 0.85 * ease_out(core_p) * float(getattr(self, "_fx_gauss_alpha_scale", 1.0) or 1.0)
            flash_alpha = 0.9 * ease_out(flash_p) * float(getattr(self, "_fx_gauss_alpha_scale", 1.0) or 1.0)
            ring_alpha = 0.7 * ease_out(ring_p) * float(getattr(self, "_fx_gauss_alpha_scale", 1.0) or 1.0)

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

            # Порядок: tube line -> noise stripe -> radial stamps -> core -> pulse -> ...
            tube_alpha = glow_alpha * float(config.get("beam_tube_alpha_scale", 0.72))
            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            glow_pen = QtGui.QPen(glow_color)
            glow_pen.setWidthF(glow_width * 1.15)
            glow_pen.setCapStyle(QtCore.Qt.RoundCap)
            glow_pen.setJoinStyle(QtCore.Qt.RoundJoin)
            glow_pen.setColor(self._with_alpha(glow_color, tube_alpha))
            painter.setPen(glow_pen)
            painter.drawLine(fx.start, fx.end)
            painter.restore()

            noise_sprite = self._fx_pixmaps.get("gauss_noise_stripe")
            if noise_sprite is not None and not noise_sprite.isNull():
                noise_alpha = glow_alpha * float(config.get("beam_noise_alpha_scale", 0.5))
                tinted_noise = self._tinted_pixmap(
                    "gauss_noise_stripe",
                    self._with_alpha(glow_color, noise_alpha),
                )
                beam_h = self._px_to_world(glow_width_px * 1.35)
                angle_deg = math.degrees(math.atan2(direction.y(), direction.x()))
                painter.save()
                painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
                painter.translate(fx.start)
                painter.rotate(angle_deg)
                painter.setOpacity(min(1.0, noise_alpha * 1.1))
                dst = QtCore.QRectF(0.0, -beam_h / 2.0, length, beam_h)
                scroll_px_s = float(config.get("beam_noise_scroll_px_s", 110.0))
                scroll_px = -((age * scroll_px_s) % max(1.0, float(tinted_noise.width())))
                painter.drawTiledPixmap(dst, tinted_noise, QtCore.QPointF(scroll_px, 0.0))
                painter.setOpacity(1.0)
                painter.restore()

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            glow_sprite = self._fx_pixmaps.get("gauss_glow_radial")
            if glow_sprite is not None and not glow_sprite.isNull():
                glow_sprite_color = self._with_alpha(glow_color, glow_alpha)
                tinted = self._tinted_pixmap("gauss_glow_radial", glow_sprite_color)
                step_px = float(config.get("beam_glow_step_px", 6.5))
                step_world = self._px_to_world(max(5.0, step_px))
                steps = max(2, int(length / max(step_world, 0.001)) + 1)
                beam_scale = float(config.get("beam_glow_sprite_scale", 1.48))
                sprite_size = max(
                    glow_width * beam_scale,
                    self._px_to_world(glow_width_px * 1.05),
                )
                painter.setOpacity(min(1.0, glow_alpha * 1.0))
                for idx in range(steps):
                    t = idx / max(1, steps - 1)
                    cx = fx.start.x() + direction.x() * t
                    cy = fx.start.y() + direction.y() * t
                    rect = QtCore.QRectF(
                        cx - sprite_size / 2,
                        cy - sprite_size / 2,
                        sprite_size,
                        sprite_size,
                    )
                    painter.drawPixmap(rect, tinted, QtCore.QRectF(tinted.rect()))
                painter.setOpacity(1.0)
            painter.restore()

            muzzle_sprite = self._fx_pixmaps.get("gauss_muzzle_atlas")
            muzzle_life_s = max(0.06, float(config.get("muzzle_life_s", 0.14)))
            if muzzle_sprite is not None and not muzzle_sprite.isNull() and age < muzzle_life_s:
                frame = min(3, int((age / muzzle_life_s) * 4.0))
                src_w = muzzle_sprite.width() // 4
                src_h = muzzle_sprite.height()
                src = QtCore.QRect(frame * src_w, 0, src_w, src_h)
                muzzle_scale = float(config.get("muzzle_scale", 1.0))
                muzzle_stretch_x = float(config.get("muzzle_stretch_x", 1.0))
                muzzle_size = self.cell_size * 0.52 * max(0.7, muzzle_scale)
                barrel_offset = self.cell_size * 0.17 * max(0.7, muzzle_scale)
                muzzle_center = QtCore.QPointF(
                    fx.start.x() + dir_unit.x() * barrel_offset,
                    fx.start.y() + dir_unit.y() * barrel_offset,
                )
                rect = QtCore.QRectF(
                    muzzle_center.x() - (muzzle_size * muzzle_stretch_x) / 2,
                    muzzle_center.y() - muzzle_size / 2,
                    muzzle_size * muzzle_stretch_x,
                    muzzle_size,
                )
                muzzle_fade = max(0.0, 1.0 - age / muzzle_life_s)
                tinted_muzzle = self._tinted_pixmap(
                    "gauss_muzzle_atlas",
                    self._with_alpha(glow_color, min(1.0, 0.95 * muzzle_fade)),
                )
                painter.save()
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
                painter.drawPixmap(rect, tinted_muzzle, src)
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
            glyph_atlas = self._fx_pixmaps.get("necron_glyphs_atlas")
            if glyph_atlas is not None and not glyph_atlas.isNull():
                glyph_sprite_scale = float(config.get("glyph_sprite_scale", 1.0))
                glyph_pulse_speed = float(config.get("glyph_pulse_speed", 1.0))
                cols = 4
                rows = 4
                cell_w = glyph_atlas.width() // cols
                cell_h = glyph_atlas.height() // rows
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
                    scale = self._px_to_world(glyph.scale_px * glyph_sprite_scale)
                    alpha = glyph.alpha * fade * (
                        0.85
                        + 0.15
                        * math.sin((age + glyph.phase) * math.tau * glyph_pulse_speed)
                    )
                    tinted_glyph = self._tinted_pixmap(
                        "necron_glyphs_atlas", self._with_alpha(glyph_dim, alpha)
                    )
                    gid = int(glyph.glyph_id) % (cols * rows)
                    src_col = gid % cols
                    src_row = gid // cols
                    src = QtCore.QRect(
                        src_col * cell_w,
                        src_row * cell_h,
                        cell_w,
                        cell_h,
                    )
                    center = QtCore.QPointF(base.x() + offset.x(), base.y() + offset.y())
                    rect = QtCore.QRectF(
                        center.x() - scale * 0.5,
                        center.y() - scale * 0.5,
                        scale,
                        scale,
                    )
                    painter.drawPixmap(rect, tinted_glyph, src)
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
            flash_sprite = self._fx_pixmaps.get("gauss_glow_radial")
            if flash_sprite is None or flash_sprite.isNull():
                pass
            else:
                tinted_flash = self._tinted_pixmap("gauss_glow_radial", self._with_alpha(impact_color, flash_alpha))
                flash_scale = float(config.get("impact_flash_sprite_scale", 1.28))
                size = flash_radius * flash_scale
                rect = QtCore.QRectF(
                    fx.end.x() - size / 2,
                    fx.end.y() - size / 2,
                    size,
                    size,
                )
                painter.save()
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
                painter.setOpacity(min(1.0, flash_alpha * 1.2))
                painter.drawPixmap(rect, tinted_flash, QtCore.QRectF(tinted_flash.rect()))
                painter.restore()
            painter.restore()

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            ring_sprite = self._fx_pixmaps.get("gauss_impact_ring")
            if ring_sprite is None or ring_sprite.isNull():
                pass
            else:
                tinted_ring = self._tinted_pixmap("gauss_impact_ring", self._with_alpha(impact_color, ring_alpha))
                ring_scale = float(config.get("impact_ring_sprite_scale", 1.45))
                size = ring_radius * ring_scale
                rect = QtCore.QRectF(
                    fx.end.x() - size / 2,
                    fx.end.y() - size / 2,
                    size,
                    size,
                )
                painter.save()
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
                painter.setOpacity(min(1.0, ring_alpha * 1.1))
                painter.drawPixmap(rect, tinted_ring, QtCore.QRectF(tinted_ring.rect()))
                painter.restore()
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

    def _tinted_pixmap(self, name: str, color: QtGui.QColor) -> QtGui.QPixmap:
        """Return a colorized + alpha-applied copy of an FX sprite, cached.

        Uses CompositionMode_SourceIn to multiply RGB by `color` while keeping
        the source alpha shape. The cache key quantizes color to 5-bit per
        channel + alpha, so dynamic alpha across frames stays bounded.
        """
        base = self._fx_pixmaps.get(name)
        if base is None or base.isNull():
            return base if base is not None else QtGui.QPixmap()
        key = (
            name,
            (color.red() >> 3) << 19
            | (color.green() >> 3) << 14
            | (color.blue() >> 3) << 9
            | (color.alpha() >> 3) << 4,
        )
        cached = self._fx_tinted_cache.get(key)
        if cached is not None:
            return cached
        tinted = QtGui.QPixmap(base.size())
        tinted.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(tinted)
        p.drawPixmap(0, 0, base)
        p.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        p.fillRect(tinted.rect(), color)
        p.end()
        if len(self._fx_tinted_cache) > 256:
            self._fx_tinted_cache.pop(next(iter(self._fx_tinted_cache)))
        self._fx_tinted_cache[key] = tinted
        return tinted

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

    def _draw_fx_sprite_rect(
        self,
        painter: QtGui.QPainter,
        pixmap: Optional[QtGui.QPixmap],
        rect: QtCore.QRectF,
        opacity: float,
    ) -> None:
        if pixmap is None or rect.isEmpty() or opacity <= 0:
            return
        painter.save()
        painter.setOpacity(opacity)
        painter.drawPixmap(rect, pixmap, QtCore.QRectF(pixmap.rect()))
        painter.restore()

    def _cell_center(self, col: int, row: int) -> QtCore.QPointF:
        return QtCore.QPointF(
            col * self.cell_size + self.cell_size / 2,
            row * self.cell_size + self.cell_size / 2,
        )

    def _world_to_view_cell(self, world: QtCore.QPointF) -> Optional[Tuple[int, int]]:
        if self._board_rect.isEmpty():
            return None
        col = int(world.x() // self.cell_size)
        row = int(world.y() // self.cell_size)
        if col < 0 or row < 0 or col >= self._board_width or row >= self._board_height:
            return None
        return col, row

    def _world_to_state_pos(self, world: QtCore.QPointF) -> Optional[Tuple[int, int]]:
        view_cell = self._world_to_view_cell(world)
        if view_cell is None:
            return None
        return self.xy_to_state_pos(*view_cell)

    def _update_hover_cell(self, world: QtCore.QPointF) -> None:
        self._hover_cell = self._world_to_view_cell(world)

    def _rebuild_unit_hitboxes_screen(self) -> None:
        transform = self._view_transform()
        hitboxes: Dict[Tuple[str, int], QtCore.QRectF] = {}
        for render in self._units:
            key = render.key
            if key[0] is None or key[1] is None:
                continue
            centers = list(render.model_centers or [render.center])
            if not centers:
                continue
            if render.model_centers:
                icon_size_world = max(6.0, self.cell_size * self._model_icon_scale)
            else:
                icon_size_world = max(6.0, render.radius * self._unit_icon_scale)
            half_size_screen = max(2.0, (icon_size_world * self._scale) / 2.0)
            min_x = min_y = None
            max_x = max_y = None
            for center in centers:
                screen_center = transform.map(center)
                left = float(screen_center.x() - half_size_screen)
                right = float(screen_center.x() + half_size_screen)
                top = float(screen_center.y() - half_size_screen)
                bottom = float(screen_center.y() + half_size_screen)
                min_x = left if min_x is None else min(min_x, left)
                max_x = right if max_x is None else max(max_x, right)
                min_y = top if min_y is None else min(min_y, top)
                max_y = bottom if max_y is None else max(max_y, bottom)
            if min_x is None or min_y is None or max_x is None or max_y is None:
                continue
            hitboxes[key] = QtCore.QRectF(min_x, min_y, max_x - min_x, max_y - min_y)
        self._unit_hitboxes_screen = hitboxes

    def hit_test_screen(self, screen_pos: QtCore.QPointF):
        """Screen-space pick using icon hitboxes (for QML / ``ViewerController.hitTestBoard``)."""
        from app.viewer.rendering.hit_test import HitResult, pick_unit_screen

        self._rebuild_unit_hitboxes_screen()
        key = pick_unit_screen(screen_pos, self._unit_hitboxes_screen, self._units)
        if key is None:
            return HitResult.none()
        return HitResult(kind="unit", side=str(key[0]), unit_id=int(key[1]))

    def _unit_key_at_screen_pos(self, screen_pos: QtCore.QPointF) -> Optional[Tuple[str, int]]:
        from app.viewer.rendering.hit_test import pick_unit_screen

        return pick_unit_screen(screen_pos, self._unit_hitboxes_screen, self._units)

    def _update_shooting_hover_target(self, screen_pos: QtCore.QPointF) -> None:
        if not self._should_show_shooting() or not self._shoot_target_infos:
            self._shoot_hovered_target_key = None
            return
        self._rebuild_unit_hitboxes_screen()
        hovered: Optional[Tuple[str, int]] = None
        hovered_classification = ""
        for info in reversed(self._shoot_target_infos):
            key = info.get("unit_key")
            if not isinstance(key, tuple) or len(key) < 2:
                continue
            norm_key = (str(key[0]), int(key[1]))
            rect = self._target_hitbox_for_info(info)
            if rect is None or not rect.contains(screen_pos):
                continue
            hovered = norm_key
            hovered_classification = str(info.get("classification") or "")
            break
        self._shoot_hovered_target_key = hovered
        if self._viewer_debug_enabled and hovered is not None:
            sig = (int(hovered[1]), hovered_classification)
            if sig != self._last_shoot_hover_debug_sig:
                self._last_shoot_hover_debug_sig = sig
                self._append_agent_log(
                    f"[VIEWER][SHOOT_HOVER] target_id={hovered[1]} classification={hovered_classification}"
                )

    def _show_unit_tooltip_immediate(
        self,
        unit_key: Tuple[str, int],
        global_pos: QtCore.QPoint,
        modifiers: QtCore.Qt.KeyboardModifiers,
    ) -> None:
        unit = self._state_unit(unit_key)
        if not unit:
            self._clear_hover_tooltip()
            return
        if modifiers & (QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier):
            self._tooltip_pinned = True
        self._terrain_tooltip_widget.hide_animated()
        self._hover_candidate_key = unit_key
        self._hover_candidate_pos = global_pos
        self._hover_candidate_mods = modifiers
        self._tooltip_widget.set_pinned(self._tooltip_pinned)
        self._tooltip_widget.set_debug_mode(self._debug_overlay)
        tooltip_payload = self._build_unit_tooltip_payload(unit)
        self._hover_tooltip_text = tooltip_payload
        self._hover_unit_key = unit_key
        self._hover_terrain_feature = None
        self._hover_tooltip_ts = monotonic()
        accent = self._unit_accent_color(unit)
        self._tooltip_widget.update_content(tooltip_payload, accent)
        anchor = self._tooltip_anchor_for_unit(unit_key, global_pos) if self._tooltip_pinned else self._tooltip_anchor_for_cursor(global_pos)
        self._position_tooltip(anchor, animate=False)

    def _on_tooltip_weapon_hovered(self, payload: object) -> None:
        if not isinstance(payload, dict):
            self._hover_weapon_range = None
            self.update()
            return
        range_num = payload.get("range_num")
        if isinstance(range_num, (int, float)):
            self._hover_weapon_range = int(range_num)
        else:
            self._hover_weapon_range = None
        self._refresh_tooltip_anchor()
        self.update()

    def _on_tooltip_weapon_hover_left(self) -> None:
        if self._hover_weapon_range is None:
            return
        self._hover_weapon_range = None
        self._refresh_tooltip_anchor()
        self.update()

    def _on_tooltip_copy_stats_requested(self, text: str) -> None:
        clipboard = QtWidgets.QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(str(text or ""))

    def _on_status_chip_hovered(self, ids: object) -> None:
        if isinstance(ids, list):
            self._hover_status_enemy_ids = [int(v) for v in ids if isinstance(v, (int, float, str)) and str(v).strip().isdigit()]
        else:
            self._hover_status_enemy_ids = []
        self.update()

    def _on_status_chip_left(self) -> None:
        if not self._hover_status_enemy_ids:
            return
        self._hover_status_enemy_ids = []
        self.update()

    def _update_hover_tooltip(self, event: QtGui.QMouseEvent, world: QtCore.QPointF, screen_pos: QtCore.QPointF) -> None:
        if self._board_rect.isEmpty():
            self._clear_hover_tooltip()
            return
        if self._tooltip_pinned and (self._hover_unit_key is not None or self._hover_terrain_feature is not None):
            return

        self._rebuild_unit_hitboxes_screen()
        unit_key = self._unit_key_at_screen_pos(screen_pos)
        if unit_key is not None:
            if unit_key != self._hover_unit_key:
                self._show_unit_tooltip_immediate(
                    unit_key,
                    event.globalPosition().toPoint(),
                    event.modifiers(),
                )
                if self._viewer_debug_enabled:
                    rect = self._unit_hitboxes_screen.get(unit_key)
                    if rect is not None:
                        sig = (unit_key[1], int(rect.x()), int(rect.y()), int(rect.width()), int(rect.height()))
                        if sig != self._last_hover_hitbox_debug_sig:
                            self._last_hover_hitbox_debug_sig = sig
                            self._append_agent_log(
                                f"[VIEWER][HOVER] unit={unit_key[1]} hitbox=({int(rect.x())},{int(rect.y())},{int(rect.width())},{int(rect.height())})"
                            )
            else:
                anchor = self._tooltip_anchor_for_cursor(event.globalPosition().toPoint())
                self._set_tooltip_target(anchor)
            return

        terrain_feature = self._terrain_feature_at_world(world)
        if terrain_feature is not None:
            self._show_terrain_tooltip(terrain_feature, event.globalPosition().toPoint())
            return

        self._clear_hover_tooltip()

    def _unit_key_at_world(self, world: QtCore.QPointF) -> Optional[Tuple[str, int]]:
        view_cell = self._world_to_view_cell(world)
        if view_cell is None:
            return None
        col, row = view_cell
        candidates = []
        for unit in self._units_state:
            view_cell = self._unit_anchor_view_cell(unit)
            if view_cell == (col, row):
                candidates.append(unit)
        closest_key = None
        closest_dist = None
        for unit in candidates:
            key = self._norm_unit_key(unit.get("side"), unit.get("id"))
            if key is None:
                continue
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

    def _load_weapon_data(self) -> List[dict]:
        base_dir = Path(__file__).resolve().parents[1]
        data_path = CORE_DIR / "engine" / "unitData.json"
        if not data_path.exists():
            return []
        try:
            with data_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return []
        weapon_data = data.get("WeaponData", [])
        if isinstance(weapon_data, list):
            return weapon_data
        return []

    def _load_unit_data(self) -> List[dict]:
        base_dir = Path(__file__).resolve().parents[1]
        data_path = CORE_DIR / "engine" / "unitData.json"
        if not data_path.exists():
            return []
        try:
            with data_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return []
        unit_data = data.get("UnitData", [])
        if isinstance(unit_data, list):
            return unit_data
        return []

    def _index_unit_data(self, unit_data: List[dict]) -> Dict[str, List[dict]]:
        index: Dict[str, List[dict]] = {}
        for entry in unit_data:
            name = str(entry.get("Name") or "").strip().lower()
            if not name:
                continue
            index.setdefault(name, []).append(entry)
        return index

    def _index_weapon_data(self, weapon_data: List[dict]) -> Dict[str, List[dict]]:
        index: Dict[str, List[dict]] = {}
        for entry in weapon_data:
            name = str(entry.get("Name") or "").strip().lower()
            if not name:
                continue
            index.setdefault(name, []).append(entry)
        return index

    def _unit_profile(self, unit: dict) -> Optional[dict]:
        name_candidates = [
            unit.get("name"),
            unit.get("unit_name"),
            unit.get("type"),
            unit.get("unit_type"),
        ]
        for name in name_candidates:
            label = str(name or "").strip()
            if not label:
                continue
            matches = self._unit_data_by_name.get(label.lower())
            if matches:
                return matches[0]
        return None

    def _unit_weapon_names(self, unit: dict) -> List[str]:
        names: List[str] = []
        for key in ("weapon_name", "weapon", "weapons", "weapon_names", "ranged_weapon", "melee_weapon"):
            value = unit.get(key)
            if not value:
                continue
            if isinstance(value, list):
                names.extend(value)
            elif isinstance(value, dict):
                maybe_name = value.get("Name") or value.get("name")
                if maybe_name:
                    names.append(maybe_name)
            else:
                names.append(value)
        cleaned = []
        seen = set()
        for name in names:
            label = str(name).strip()
            if not label or label in seen:
                continue
            seen.add(label)
            cleaned.append(label)
        if not cleaned:
            profile = self._unit_profile(unit)
            if profile:
                weapons = profile.get("Weapons")
                if isinstance(weapons, list):
                    for name in weapons:
                        label = str(name).strip()
                        if label and label not in seen:
                            seen.add(label)
                            cleaned.append(label)
        return cleaned

    def _get_weapon_by_type(self, unit: dict, weapon_type: str) -> Optional[dict]:
        names = self._unit_weapon_names(unit)
        if not names:
            return None
        army = str(unit.get("army") or unit.get("faction") or "").lower()
        weapon_type = weapon_type.lower()
        for name in names:
            matches = [
                entry
                for entry in self._weapon_data_by_name.get(name.lower(), [])
                if str(entry.get("Type") or "").lower() == weapon_type
            ]
            if not matches:
                continue
            if army:
                for entry in matches:
                    if str(entry.get("Army") or "").lower() == army:
                        return entry
            return matches[0]
        return None

    def _get_primary_ranged_weapon(self, unit: dict) -> Optional[dict]:
        return self._get_weapon_by_type(unit, "ranged")

    def _get_primary_melee_weapon(self, unit: dict) -> Optional[dict]:
        return self._get_weapon_by_type(unit, "melee")

    def _format_skill_value(self, value: object) -> str:
        if value is None:
            return "—"
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return "—"
            if text.endswith("+"):
                return text
            try:
                return f"{int(float(text))}+"
            except ValueError:
                return text
        if isinstance(value, (int, float)):
            return f"{int(value)}+"
        return str(value)

    def _format_stat_value(self, value: object) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            text = value.strip()
            return text if text else None
        return str(value)

    def _build_unit_tooltip_payload(self, unit: dict) -> Dict:
        title = self._unit_display_name(unit)
        total_models = self._safe_int(unit.get("models"))
        alive_models = self._safe_int(unit.get("alive_models"))
        if alive_models is not None and total_models is not None:
            models = f"{alive_models}/{total_models}"
        elif total_models is not None:
            models = str(total_models)
        else:
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
        weapon_profiles = self._collect_weapon_profiles(unit)
        ranged_profile = next((w for w in weapon_profiles if w.get("group") == "ranged"), None)
        melee_profile = next((w for w in weapon_profiles if w.get("group") == "melee"), None)
        ranged_name = (
            ranged_profile.get("name")
            if ranged_profile
            else self._tooltip_weapon_name(unit)
        ) or "—"
        melee_name = melee_profile.get("name") if melee_profile else "—"
        unit_id = unit.get("id", "—")
        los = self._tooltip_los_status(unit)
        mods = self._tooltip_mods_status(unit)
        weapon_range = (
            ranged_profile.get("range")
            if ranged_profile and ranged_profile.get("range") is not None
            else self._resolve_weapon_range(unit)
        )
        bs_value = (
            unit.get("bs") or unit.get("BS") or unit.get("ballistic_skill")
        )
        ws_value = (
            unit.get("ws") or unit.get("WS") or unit.get("weapon_skill")
        )
        ranged_attacks = self._format_stat_value(
            ranged_profile.get("attacks") if ranged_profile else None
        )
        ranged_strength = self._format_stat_value(
            ranged_profile.get("strength") if ranged_profile else None
        )
        ranged_ap = self._format_stat_value(
            ranged_profile.get("ap") if ranged_profile else None
        )
        ranged_damage = self._format_stat_value(
            ranged_profile.get("damage") if ranged_profile else None
        )
        melee_attacks = self._format_stat_value(
            melee_profile.get("attacks") if melee_profile else None
        )
        melee_strength = self._format_stat_value(
            melee_profile.get("strength") if melee_profile else None
        )
        melee_ap = self._format_stat_value(
            melee_profile.get("ap") if melee_profile else None
        )
        melee_damage = self._format_stat_value(
            melee_profile.get("damage") if melee_profile else None
        )
        threat = self._unit_threat_summary(unit)
        keyword_chips = self._unit_keyword_chips(unit)
        status_chips = self._unit_status_chips(threat)
        copy_stats = self._unit_copy_stats_text(unit, weapon_profiles)
        return {
            "title": title,
            "unit_id": unit_id,
            "side": unit.get("side") or "—",
            "portrait": self._unit_portrait_glyph(unit),
            "portrait_icon": self._icon_for_unit_name(str(unit.get("name") or "")),
            "faction_icon": self._unit_faction_icon(unit),
            "models": models,
            "wounds": wounds_label,
            "wounds_value": wounds_value,
            "wounds_max": wounds_max,
            "ranged_name": ranged_name,
            "ranged_range": weapon_range if weapon_range is not None else "—",
            "ranged_bs": self._format_skill_value(bs_value),
            "ranged_attacks": ranged_attacks,
            "ranged_strength": ranged_strength,
            "ranged_ap": ranged_ap,
            "ranged_damage": ranged_damage,
            "melee_name": melee_name,
            "melee_ws": self._format_skill_value(ws_value),
            "melee_attacks": melee_attacks,
            "melee_strength": melee_strength,
            "melee_ap": melee_ap,
            "melee_damage": melee_damage,
            "cover": cover,
            "los": los,
            "mods": mods,
            "keyword_chips": keyword_chips,
            "status_chips": status_chips,
            "threat": threat,
            "weapon_profiles": weapon_profiles,
            "copy_stats": copy_stats,
        }

    def _collect_weapon_profiles(self, unit: dict) -> List[Dict]:
        profiles: List[Dict] = []
        for name in self._unit_weapon_names(unit):
            for entry in self._weapon_data_by_name.get(str(name).lower(), []):
                profiles.append(
                    {
                        "name": str(entry.get("Name") or name),
                        "group": "melee" if str(entry.get("Type") or "").lower() == "melee" else "ranged",
                        "range": self._format_stat_value(entry.get("Range")) or "—",
                        "range_num": self._coerce_number(entry.get("Range")),
                        "attacks": self._format_stat_value(entry.get("A")) or "—",
                        "strength": self._format_stat_value(entry.get("S")) or "—",
                        "ap": self._format_stat_value(entry.get("AP")) or "—",
                        "damage": self._format_stat_value(entry.get("Damage")) or "—",
                    }
                )
        if not profiles:
            fallback = self._tooltip_weapon_name(unit)
            profiles.append({"name": fallback, "group": "ranged", "range": "—", "range_num": None, "attacks": "—", "strength": "—", "ap": "—", "damage": "—"})
        return profiles

    def _unit_copy_stats_text(self, unit: dict, weapon_profiles: List[Dict]) -> str:
        tags = ",".join(self._unit_tags(unit)[:5])
        weapon_names = ", ".join([str(w.get("name") or "—") for w in weapon_profiles[:3]])
        return (
            f"Unit {self._unit_display_name(unit)} id={unit.get('id')} "
            f"models={unit.get('models', '—')} hp={unit.get('wounds', unit.get('hp', '—'))} "
            f"tags={tags or '—'} weapons={weapon_names or '—'}"
        )

    def _unit_portrait_glyph(self, unit: dict) -> str:
        army = str(unit.get("army") or unit.get("faction") or "").lower()
        if "necron" in army:
            return "☥"
        return "⚔"

    def _unit_faction_icon(self, unit: dict) -> Optional[QtGui.QPixmap]:
        for keyword in self._unit_keywords(unit):
            icon = self._faction_icon_by_keyword.get(keyword.upper())
            if icon is not None and not icon.isNull():
                return icon
        return None

    def _unit_keywords(self, unit: dict) -> List[str]:
        profile = self._unit_profile(unit) or {}
        keywords: List[str] = []
        raw = profile.get("KEYWORDS") or profile.get("keywords")
        if isinstance(raw, list):
            keywords.extend([str(v) for v in raw])
        elif isinstance(raw, str):
            keywords.extend([v.strip() for v in raw.split(",")])
        return [k.strip().upper() for k in keywords if str(k).strip()]

    def _unit_tags(self, unit: dict) -> List[str]:
        tags: List[str] = self._unit_keywords(unit)
        for key in ("keywords", "tags"):
            value = unit.get(key)
            if isinstance(value, list):
                tags.extend([str(v) for v in value])
            elif isinstance(value, str):
                tags.extend([v.strip() for v in value.split(",")])
        for key in ("type", "unit_type", "army", "faction"):
            value = str(unit.get(key) or "").strip()
            if value:
                tags.append(value)
        seen = set()
        clean: List[str] = []
        for tag in tags:
            t = str(tag).strip().upper().replace(" ", "_")
            if not t or t in seen:
                continue
            seen.add(t)
            clean.append(t)
        return clean

    def _unit_threat_summary(self, unit: dict) -> Dict[str, object]:
        enemies = [u for u in (self._state.get("units", []) or []) if u.get("side") != unit.get("side")]
        unit_cell = self._unit_anchor_view_cell(unit)
        unit_status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
        obscured_vs = [int(v) for v in list(unit_status.get("obscured_vs") or []) if str(v).strip().isdigit()]
        exposed_to = [int(v) for v in list(unit_status.get("exposed_to") or []) if str(v).strip().isdigit()]
        vis_lists = self._unit_visibility_lists(unit)
        can_see_ids = vis_lists.get("can_see_ids", [])
        seen_by_ids = vis_lists.get("seen_by_ids", [])
        in_range_ids = vis_lists.get("in_range_ids", [])
        enemies_seeing = len(seen_by_ids)
        targets_in_range = len(in_range_ids)
        obscured = self._read_first_bool(unit_status, ("obscured",))
        fully_visible = self._read_first_bool(unit_status, ("fully_visible",))
        los_bool = enemies_seeing > 0
        if fully_visible is None:
            fully_visible = los_bool and not bool(obscured)
        return {
            "los": "✔" if los_bool else "✖",
            "obscured": "✔" if obscured else ("✖" if obscured is not None else "—"),
            "enemies_seeing": enemies_seeing if unit_cell is not None else "—",
            "targets_in_range": targets_in_range if unit_cell is not None else "—",
            "fully_visible": bool(fully_visible),
            "in_cover": self._read_first_bool(unit_status, ("in_cover",)),
            "objective_status": self._unit_objective_status(unit),
            "enemies_in_los_keys": self._enemy_keys_in_range_of(unit),
            "obscured_vs": obscured_vs,
            "exposed_to": exposed_to,
            "engagement_with": [int(v) for v in list(unit_status.get("engagement_with") or []) if str(v).strip().isdigit()],
            "can_see_ids": can_see_ids,
            "seen_by_ids": seen_by_ids,
            "in_range_ids": in_range_ids,
        }

    def _unit_visibility_lists(self, unit: dict) -> Dict[str, List[int]]:
        unit_status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
        state_sig = self._state.get("generated_at") or f"{self._state.get('turn')}-{self._state.get('round')}-{self._state.get('phase')}"
        unit_key = (unit.get("side"), unit.get("id"), state_sig, self._hover_weapon_range)
        cached = self._visibility_lists_cache.get(unit_key)
        if cached is not None:
            return cached

        def _ids(raw: object) -> List[int]:
            if not isinstance(raw, list):
                return []
            vals = [int(v) for v in raw if isinstance(v, (int, float, str)) and str(v).strip().isdigit()]
            return sorted(set(vals))

        can_see_ids = _ids(unit_status.get("can_see_ids"))
        seen_by_ids = _ids(unit_status.get("seen_by_ids"))
        if self._hover_weapon_range is None:
            in_range_ids = _ids(unit_status.get("in_range_ids") or unit_status.get("in_range_targets"))
        else:
            in_range_ids = []

        # fallback если движок не прислал поля
        if not can_see_ids or not seen_by_ids:
            unit_cell = self._unit_anchor_view_cell(unit)
            if unit_cell is not None:
                ux, uy = unit_cell
                if not can_see_ids:
                    for enemy in (self._state.get("units", []) or []):
                        if enemy.get("side") == unit.get("side"):
                            continue
                        e_cell = self._unit_anchor_view_cell(enemy)
                        if e_cell is None:
                            continue
                        # fallback: без движка считаем как потенциально видимую цель по геометрии
                        can_see_ids.append(int(enemy.get("id")))
                if not seen_by_ids:
                    for enemy in (self._state.get("units", []) or []):
                        if enemy.get("side") == unit.get("side"):
                            continue
                        e_cell = self._unit_anchor_view_cell(enemy)
                        if e_cell is None:
                            continue
                        dist = abs(e_cell[0] - ux) + abs(e_cell[1] - uy)
                        e_range = self._primary_ranged_range(enemy)
                        if e_range is not None and dist <= e_range:
                            seen_by_ids.append(int(enemy.get("id")))
                if not in_range_ids or self._hover_weapon_range is not None:
                    own_range = self._hover_weapon_range if self._hover_weapon_range is not None else self._primary_ranged_range(unit)
                    if own_range is not None:
                        can_see_set = set(can_see_ids)
                        for enemy in (self._state.get("units", []) or []):
                            if enemy.get("side") == unit.get("side"):
                                continue
                            enemy_id = int(enemy.get("id")) if str(enemy.get("id")).strip().isdigit() else None
                            if enemy_id is None or enemy_id not in can_see_set:
                                continue
                            e_cell = self._unit_anchor_view_cell(enemy)
                            if e_cell is None:
                                continue
                            dist = abs(e_cell[0] - ux) + abs(e_cell[1] - uy)
                            if dist <= own_range:
                                in_range_ids.append(enemy_id)

        result = {
            "can_see_ids": sorted(set(can_see_ids)),
            "seen_by_ids": sorted(set(seen_by_ids)),
            "in_range_ids": sorted(set(in_range_ids)),
        }
        self._visibility_lists_cache[unit_key] = result
        return result

    def _primary_ranged_range(self, unit: dict) -> Optional[int]:
        ranged = self._get_primary_ranged_weapon(unit)
        if ranged is not None:
            r = self._coerce_number(ranged.get("Range"))
            if r is not None:
                return int(r)
        r = self._resolve_weapon_range(unit)
        return int(r) if isinstance(r, (int, float)) else None

    def _read_first_bool(self, data: dict, keys: Tuple[str, ...]) -> Optional[bool]:
        for key in keys:
            if key not in data:
                continue
            value = data.get(key)
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return bool(value)
            if isinstance(value, str):
                val = value.strip().lower()
                if val in {"1", "true", "yes", "y"}:
                    return True
                if val in {"0", "false", "no", "n"}:
                    return False
        return None

    def _unit_objective_status(self, unit: dict) -> Optional[str]:
        unit_status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
        direct = str(unit_status.get("objective_state") or "").strip().lower()
        if direct in {"holding", "contesting"}:
            return direct.upper()
        unit_cell = self._unit_anchor_view_cell(unit)
        if unit_cell is None:
            return None
        ux, uy = unit_cell
        for objective in (self._state.get("objectives", []) or []):
            obj_cell = self._state_to_view_cell(objective.get("x"), objective.get("y"))
            if obj_cell is None:
                continue
            radius = self._safe_int(objective.get("control_radius")) or 3
            if abs(obj_cell[0] - ux) + abs(obj_cell[1] - uy) > radius:
                continue
            owner = str(objective.get("owner") or "").lower()
            side = str(unit.get("side") or "").lower()
            return "HOLDING" if owner and owner == side else "CONTESTING"
        return None

    def _unit_keyword_chips(self, unit: dict) -> List[Dict[str, str]]:
        static_tags = self._unit_tags(unit)
        limit = 5
        chips = [{"label": tag, "tone": "neutral"} for tag in static_tags[:limit]]
        rest = len(static_tags) - limit
        if rest > 0:
            chips.append({"label": f"+{rest}", "tone": "neutral"})
        return chips

    def _unit_status_chips(self, threat: Dict[str, object]) -> List[Dict[str, str]]:
        chips: List[Dict[str, str]] = []
        if threat.get("in_cover") is True:
            chips.append({"label": "🛡 IN COVER", "tone": "good", "ids": []})
        obscured_vs = [int(v) for v in list(threat.get("obscured_vs") or [])]
        exposed_to = [int(v) for v in list(threat.get("exposed_to") or [])]
        if obscured_vs:
            chips.append({
                "label": f"👁 OBSCURED vs {self._format_id_list(obscured_vs)}",
                "tone": "status_obscured",
                "ids": obscured_vs,
            })
        if exposed_to:
            chips.append({
                "label": f"⚠ EXPOSED to {self._format_id_list(exposed_to)}",
                "tone": "status_exposed",
                "ids": exposed_to,
            })
        objective_status = threat.get("objective_status")
        if objective_status:
            if str(objective_status).upper() == "HOLDING":
                chips.append({"label": "🏁 HOLDING", "tone": "status_holding", "ids": []})
            else:
                chips.append({"label": "⚔ CONTESTING", "tone": "status_contesting", "ids": []})
        engagement = [int(v) for v in list(threat.get("engagement_with") or [])]
        if engagement:
            chips.append({
                "label": f"⚔ IN ENGAGEMENT vs {self._format_id_list(engagement)}",
                "tone": "status_contesting",
                "ids": engagement,
            })
        return chips

    def _format_id_list(self, ids: List[int]) -> str:
        values = sorted({int(v) for v in ids})
        if not values:
            return "—"
        if len(values) <= 3:
            return ",".join(str(v) for v in values)
        head = ",".join(str(v) for v in values[:2])
        return f"{head} +{len(values) - 2}"

    def _enemy_keys_in_range_of(self, unit: dict, forced_range: Optional[int] = None) -> List[Tuple[str, int]]:
        unit_cell = self._unit_anchor_view_cell(unit)
        if unit_cell is None:
            return []
        ux, uy = unit_cell
        rng = forced_range if forced_range is not None else self._primary_ranged_range(unit)
        if rng is None:
            return []
        range_eps = 0.1
        keys: List[Tuple[str, int]] = []
        for enemy in (self._state.get("units", []) or []):
            if enemy.get("side") == unit.get("side"):
                continue
            e_cell = self._unit_anchor_view_cell(enemy)
            if e_cell is None:
                continue
            dist = max(abs(e_cell[0] - ux), abs(e_cell[1] - uy))
            if float(dist) <= float(rng) + float(range_eps):
                keys.append((enemy.get("side"), enemy.get("id")))
        return keys

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
        elif self._tooltip_pinned and self._hover_terrain_feature is not None:
            anchor = self._tooltip_anchor_for_cursor(self.mapToGlobal(self.rect().center()))
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

    def _show_terrain_tooltip(self, terrain_feature: dict, anchor_pos: QtCore.QPoint) -> None:
        self._hover_candidate_key = None
        self._hover_unit_key = None
        self._tooltip_widget.hide_animated()
        payload = self._build_terrain_tooltip_payload(terrain_feature)
        self._hover_terrain_feature = terrain_feature
        self._hover_tooltip_text = payload
        self._hover_tooltip_ts = monotonic()
        self._terrain_tooltip_widget.set_pinned(self._tooltip_pinned)
        self._terrain_tooltip_widget.update_content(payload, Theme.objective)
        self._tooltip_target_pos = self._clamp_tooltip_pos(anchor_pos, self._terrain_tooltip_widget.sizeHint())
        self._terrain_tooltip_widget.show_at(self._tooltip_target_pos, animate=True)
        if self._viewer_debug_enabled:
            state_pos = None
            cells = terrain_feature.get("cells") or []
            if cells:
                state_pos = cells[0]
            if state_pos is not None:
                sig = (int(state_pos[0]), int(state_pos[1]), str(terrain_feature.get("id") or ""))
                if sig != self._last_terrain_hover_debug_sig:
                    self._last_terrain_hover_debug_sig = sig
                    self._append_agent_log(
                        f"[VIEWER][TERRAIN] hover cell=({int(state_pos[0])},{int(state_pos[1])}) "
                        f"id={terrain_feature.get('id') or '-'} kind={terrain_feature.get('kind') or '-'} "
                        f"keywords={','.join(terrain_feature.get('keywords') or [])}"
                    )

    def _build_terrain_tooltip_payload(self, feature: dict) -> Dict:
        kind = str(feature.get("kind") or "terrain")
        name = str(feature.get("name") or "").strip()
        title = name if name else f"Terrain: {kind}"
        keywords = [str(v).strip() for v in list(feature.get("keywords") or []) if str(v).strip()]

        coords: List[Tuple[int, int]] = []
        for cell in list(feature.get("cells") or []):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            # terrain_feature.cells хранит (row, col) -> для отображения даём (x=col, y=row)
            row = int(cell[0])
            col = int(cell[1])
            coords.append((col, row))
        coords.sort(key=lambda pos: (pos[0], pos[1]))
        coords_text = " ".join(f"({x},{y})" for x, y in coords) if coords else "—"

        kind_lower = kind.lower()
        rules_lines = [
            "Rules: No deploy • No end move on top",
            "Cover: INFANTRY within 3\" if obscured",
        ]
        covering_ids = [int(v) for v in list(feature.get("covering_unit_ids") or []) if str(v).strip().isdigit()]
        covering_chip = None
        if covering_ids:
            covering_ids = sorted(set(covering_ids))
            if len(covering_ids) <= 2:
                cover_text = ", ".join(str(v) for v in covering_ids)
            else:
                cover_text = f"{covering_ids[0]}, {covering_ids[1]} +{len(covering_ids) - 2}"
            covering_chip = f"СКРЫВАЕТ {cover_text}"
        kind_badge = "B" if "barricade" in kind_lower else "T"
        return {
            "title": title,
            "id": feature.get("id") or "—",
            "terrain_type": kind,
            "keywords": keywords,
            "covering_chip": covering_chip,
            "coords": coords_text,
            "rules": rules_lines,
            "kind_badge": kind_badge,
        }

    def _draw_hovered_terrain_cells_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.hovered_terrain_cells import paint_hovered_terrain_cells_layer

        self._paint_board_layer(painter, paint_hovered_terrain_cells_layer, layer_name="hovered_terrain_cells")

    def _draw_unit_tooltip_overlays_layer(self, painter: QtGui.QPainter) -> None:
        from app.viewer.rendering.layers.unit_tooltip_overlays import paint_unit_tooltip_overlays_layer

        self._paint_board_layer(painter, paint_unit_tooltip_overlays_layer, layer_name="unit_tooltip_overlays")

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
        status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else unit
        cover = self._read_first_bool(status, ("in_cover", "cover", "has_cover"))
        if cover is None:
            return "—"
        return "Да" if cover else "Нет"

    def _tooltip_weapon_name(self, unit: dict) -> str:
        weapon_name = unit.get("weapon_name") or unit.get("weapon") or unit.get("weapons")
        if isinstance(weapon_name, list):
            if weapon_name:
                weapon_name = weapon_name[0]
            else:
                weapon_name = None
        return weapon_name or "—"

    def _resolve_weapon_range(self, unit: dict) -> Optional[int]:
        for key in ("range", "weapon_range", "shoot_range", "shooting_range"):
            value = unit.get(key)
            if value is not None:
                return value
        return None

    def _resolve_rapid_fire_cells_range(self, unit: dict, full_range: Optional[int]) -> Optional[int]:
        if full_range is None:
            return None
        full = self._safe_int(full_range)
        if full is None or full <= 1:
            return None
        weapon = self._get_primary_ranged_weapon(unit)
        if not isinstance(weapon, dict):
            return None
        if not self._weapon_is_rapid_fire(weapon):
            return None
        return max(1, full // 2)

    def _log_shoot_overlay_range_debug(
        self,
        *,
        unit: dict,
        full_range_raw: Optional[int],
        full_range_cells: Optional[int],
        rapid_range_cells: Optional[int],
        source: Optional[Tuple[int, int]],
        target_filter: set[Tuple[str, int]],
        inferred_from_targets: bool,
        max_target_dist: int,
    ) -> None:
        shooter_id = self._safe_int(unit.get("id"))
        shooter_name = self._unit_display_name(unit)
        weapon = self._get_primary_ranged_weapon(unit) if isinstance(unit, dict) else None
        weapon_name = str((weapon or {}).get("Name") or unit.get("weapon_name") or "—")
        weapon_range_src = self._safe_int((weapon or {}).get("Range")) if isinstance(weapon, dict) else None
        rapid_enabled = self._weapon_is_rapid_fire(weapon) if isinstance(weapon, dict) else False
        sig = (
            shooter_id,
            source,
            weapon_name,
            weapon_range_src,
            full_range_raw,
            full_range_cells,
            rapid_range_cells,
            rapid_enabled,
            tuple(sorted(target_filter)),
            inferred_from_targets,
            max_target_dist,
        )
        if sig == self._last_shoot_overlay_debug_sig:
            return
        self._last_shoot_overlay_debug_sig = sig
        self._append_agent_log(
            "[VIEWER][SHOOT_RANGE] "
            f"Что случилось: рассчитан shooting-overlay для Unit {shooter_id} ({shooter_name}); "
            f"weapon={weapon_name}, source_range={weapon_range_src}, request_range={full_range_raw}, "
            f"cells_full={full_range_cells}, cells_rapid={rapid_range_cells}, rapid_fire={1 if rapid_enabled else 0}, "
            f"source_cell={source}, target_filter_size={len(target_filter)}, max_target_dist={max_target_dist}, "
            f"inferred_from_targets={1 if inferred_from_targets else 0}. "
            "Где: viewer/opengl_view.py (_build_shooting_overlay). "
            "Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — "
            "проверить UI state -> active weapon и экспорт weapon_range из engine."
        )

    def _log_shoot_overlay_cells_debug(
        self,
        *,
        unit: dict,
        source: Optional[Tuple[int, int]],
        full_range_cells: Optional[int],
        rapid_range_cells: Optional[int],
        total_cells: int,
        inside_cells: int,
        rapid_cells: int,
        outside_cells: int,
    ) -> None:
        shooter_id = self._safe_int(unit.get("id"))
        sig = (shooter_id, source, full_range_cells, rapid_range_cells, total_cells, inside_cells, rapid_cells, outside_cells)
        if sig == self._last_shoot_overlay_cells_debug_sig:
            return
        self._last_shoot_overlay_cells_debug_sig = sig
        self._append_agent_log(
            "[VIEWER][SHOOT_RANGE][CELLS] "
            f"Что случилось: по клеткам рассчитан overlay для Unit {shooter_id}; "
            f"source={source}, full_cells={full_range_cells}, rapid_cells={rapid_range_cells}, "
            f"вошло={inside_cells}, rapid={rapid_cells}, не вошло={outside_cells}, всего={total_cells}. "
            "Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). "
            "Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), "
            "проверить метрику distance=max(|dx|,|dy|) и корректность full_cells."
        )

    def _rapid_fire_hatch_brush(self) -> QtGui.QBrush:
        if self._rapid_hatch_brush_cache is not None:
            return QtGui.QBrush(self._rapid_hatch_brush_cache)
        tile = QtGui.QPixmap(SHOOTING_RAPID_HATCH_STYLE.tile_size, SHOOTING_RAPID_HATCH_STYLE.tile_size)
        tile.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(tile)
        painter.setPen(rapid_hatch_pen(SHOOTING_RAPID_HATCH_STYLE))
        for x1, y1, x2, y2 in SHOOTING_RAPID_HATCH_STYLE.lines:
            painter.drawLine(x1, y1, x2, y2)
        painter.end()
        self._rapid_hatch_brush_cache = QtGui.QBrush(tile)
        return QtGui.QBrush(self._rapid_hatch_brush_cache)

    def _weapon_is_rapid_fire(self, weapon: dict) -> bool:
        for key in ("Type", "type", "Abilities", "abilities", "Special", "special", "Notes", "notes"):
            value = weapon.get(key)
            if value is None:
                continue
            text = str(value).strip().lower().replace("_", " ").replace("-", "")
            compact = " ".join(text.split())
            if "rapid fire" in compact or "rapidfire" in compact:
                return True
        return False

    def _tooltip_los_status(self, unit: dict) -> str:
        summary = self._unit_threat_summary(unit)
        return str(summary.get("los") or "—")

    def _tooltip_mods_status(self, unit: dict) -> str:
        return "—"
    def draw_terrain_features(self, painter: QtGui.QPainter) -> None:
        self._draw_props_layer(painter)
