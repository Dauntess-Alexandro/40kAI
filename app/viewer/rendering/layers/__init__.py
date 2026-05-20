"""Composable paint passes for ``OpenGLBoardWidget``."""

from app.viewer.rendering.layers.ai_phase_badge import paint_ai_phase_badge_layer
from app.viewer.rendering.layers.damage_popups import paint_damage_popups_layer
from app.viewer.rendering.layers.debug_overlay import paint_debug_overlay_layer
from app.viewer.rendering.layers.decals import paint_decals_layer
from app.viewer.rendering.layers.deploy_ghost import paint_deploy_ghost_layer
from app.viewer.rendering.layers.deploy_snap_fx import paint_deploy_snap_fx_layer
from app.viewer.rendering.layers.fx import paint_fx_layer
from app.viewer.rendering.layers.grid import paint_grid_layer
from app.viewer.rendering.layers.ground import paint_ground_layer
from app.viewer.rendering.layers.hovered_terrain_cells import paint_hovered_terrain_cells_layer
from app.viewer.rendering.layers.labels import paint_labels_layer
from app.viewer.rendering.layers.log_movement_overlay import paint_log_movement_overlay_layer
from app.viewer.rendering.layers.movement import paint_movement_layer
from app.viewer.rendering.layers.objectives import paint_objectives_layer
from app.viewer.rendering.layers.platform_fx import paint_platform_fx_layer
from app.viewer.rendering.layers.selection import paint_selection_layer
from app.viewer.rendering.layers.shooting import paint_shooting_layer
from app.viewer.rendering.layers.shooting_targets_overlay import paint_shooting_targets_overlay
from app.viewer.rendering.layers.squad_status import paint_squad_status_layer
from app.viewer.rendering.layers.terrain_props import paint_terrain_props_layer
from app.viewer.rendering.layers.unit_tooltip_overlays import paint_unit_tooltip_overlays_layer
from app.viewer.rendering.layers.units import paint_units_layer

__all__ = [
    "paint_ai_phase_badge_layer",
    "paint_damage_popups_layer",
    "paint_debug_overlay_layer",
    "paint_decals_layer",
    "paint_deploy_ghost_layer",
    "paint_deploy_snap_fx_layer",
    "paint_fx_layer",
    "paint_grid_layer",
    "paint_ground_layer",
    "paint_hovered_terrain_cells_layer",
    "paint_labels_layer",
    "paint_log_movement_overlay_layer",
    "paint_movement_layer",
    "paint_objectives_layer",
    "paint_platform_fx_layer",
    "paint_selection_layer",
    "paint_shooting_layer",
    "paint_shooting_targets_overlay",
    "paint_squad_status_layer",
    "paint_terrain_props_layer",
    "paint_unit_tooltip_overlays_layer",
    "paint_units_layer",
]
