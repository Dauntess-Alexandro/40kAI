"""Shooting range cells + target overlay passes."""

from __future__ import annotations

from PySide6 import QtGui

from app.viewer.cells_fx import (
    SHOOTING_FULL_ZONE_STYLE,
    SHOOTING_RAPID_ZONE_STYLE,
    zone_border_pen,
    zone_fill_color,
)
from app.viewer.rendering.layer_context import LayerContext


def paint_shooting_layer(ctx: LayerContext, *, target_pass: str = "over") -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._should_show_shooting():
        return
    if not (w._shoot_target_infos or (w._show_shoot_range_cells and w._shoot_range_highlights)):
        return

    draw_under_units = str(target_pass).lower() == "under"

    if (not draw_under_units) and w._show_shoot_range_cells and w._shoot_range_highlights:
        painter.save()
        painter.setBrush(QtGui.QBrush(zone_fill_color(SHOOTING_FULL_ZONE_STYLE)))
        painter.setPen(zone_border_pen(SHOOTING_FULL_ZONE_STYLE))
        for rect in w._shoot_range_highlights:
            painter.drawRect(rect)

        if w._shoot_rapid_range_highlights:
            painter.setPen(zone_border_pen(SHOOTING_RAPID_ZONE_STYLE))
            painter.setBrush(w._rapid_fire_hatch_brush())
            for rect in w._shoot_rapid_range_highlights:
                painter.drawRect(rect)
        painter.restore()

    w._draw_shooting_targets_overlay(
        painter,
        w._shoot_target_infos,
        w._shoot_hovered_target_key,
        render_under_units=draw_under_units,
    )
