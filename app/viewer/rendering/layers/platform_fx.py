"""Unit platform glow (active + selected passes)."""

from __future__ import annotations

import math
from time import perf_counter

from PySide6 import QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_platform_fx_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._fx_pixmaps:
        return
    t = (perf_counter() - w._t0) if w._t0 is not None else 0.0
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t * 1.2)

    active_unit, active_render = w._resolve_unit_by_key_or_id(
        w._active_unit_side,
        w._active_unit_id,
    )
    if active_render:
        color, strength = w._fx_color_for_unit(active_unit)
        w._draw_platform_highlight(
            painter,
            active_render,
            color,
            strength,
            pulse,
            t,
        )

    selected_matches_active = (
        w._selected_unit_id == w._active_unit_id and w._selected_unit_side == w._active_unit_side
    )
    if w._selected_unit_id is None or selected_matches_active:
        return
    if not w._viewer_human_turn_active():
        return
    selected_unit, selected_render = w._resolve_unit_by_key_or_id(
        w._selected_unit_side,
        w._selected_unit_id,
    )
    if selected_render:
        base_sel = QtGui.QColor(Theme.selection)
        pl, base_strength = w._fx_color_for_unit(selected_unit)
        blend = 0.55
        selected_color = QtGui.QColor(
            int(base_sel.red() * blend + pl.red() * (1.0 - blend)),
            int(base_sel.green() * blend + pl.green() * (1.0 - blend)),
            int(base_sel.blue() * blend + pl.blue() * (1.0 - blend)),
        )
        selected_strength = max(0.26, base_strength * 0.62)
        w._draw_platform_highlight(
            painter,
            selected_render,
            selected_color,
            selected_strength,
            pulse,
            t,
            pulse_strength=0.16,
            glow_scale=0.42,
            noise_scale=0.30,
            scan_scale=0.36,
            sparkle_scale=0.0,
        )
