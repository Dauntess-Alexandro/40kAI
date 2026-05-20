"""Particles / Gauss traces / hover & target glow sprites."""

from __future__ import annotations

import math
from time import perf_counter

from PySide6 import QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_fx_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    w._draw_particles_layer(painter)
    w._draw_gauss_effects(painter)
    if not w._fx_pixmaps:
        return
    t = (perf_counter() - w._t0) if w._t0 is not None else 0.0
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t * 1.2)

    target_unit = w._find_unit_by_id(w._target_unit_id)
    target_render = w._unit_render_for_unit(target_unit)
    target_center = None
    target_radius = None
    if target_render:
        target_center = target_render.center
        target_radius = target_render.radius
    elif w._target_cell is not None:
        target_center = w._cell_center(*w._target_cell)
        target_radius = w.cell_size * 0.4
    if target_center is not None and target_radius is not None:
        if target_render is not None and target_render.key == w._selected_unit_key:
            target_center = None
        else:
            color = QtGui.QColor(Theme.objective)
            strength = 1.0
            ring_pixmap = w._tinted_pixmap("ring_soft", color)
            seg_pixmap = w._tinted_pixmap("tesseract_segments", color)
            ring_alpha = 0.5 * (0.7 + 0.3 * pulse) * strength
            seg_alpha = 0.55 * (0.8 + 0.2 * pulse) * strength
            ring_size = target_radius * 4.4 * (0.95 + 0.08 * pulse)
            seg_size = target_radius * 5.0 * (0.98 + 0.05 * pulse)
            tr_base = max(target_radius * 2.75, w.cell_size * 1.05)
            w._draw_soft_radial_glow_ellipse(
                painter,
                float(target_center.x()),
                float(target_center.y()),
                tr_base * 1.12,
                tr_base * 0.92,
                color,
                strength,
                composition=QtGui.QPainter.CompositionMode_SourceOver,
                peak_alpha=40,
            )
            painter.save()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
            w._draw_fx_sprite(painter, ring_pixmap, target_center, ring_size, ring_alpha)
            angle = math.degrees(t * 0.6)
            w._draw_fx_sprite(
                painter,
                seg_pixmap,
                target_center,
                seg_size,
                seg_alpha,
                rotation_deg=angle,
            )
            painter.restore()

    if w._hover_cell is not None:
        hover_center = w._cell_center(*w._hover_cell)
        h = QtGui.QColor(Theme.highlight)
        s = QtGui.QColor(Theme.selection)
        blend = 0.55
        hover_color = QtGui.QColor(
            int(h.red() * blend + s.red() * (1.0 - blend)),
            int(h.green() * blend + s.green() * (1.0 - blend)),
            int(h.blue() * blend + s.blue() * (1.0 - blend)),
        )
        hover_pixmap = w._tinted_pixmap("glow_soft", hover_color)
        hover_alpha = 0.25 * (0.8 + 0.2 * pulse)
        hover_size = w.cell_size * 2.2
        painter.save()
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        w._draw_fx_sprite(painter, hover_pixmap, hover_center, hover_size, hover_alpha)
        painter.restore()
