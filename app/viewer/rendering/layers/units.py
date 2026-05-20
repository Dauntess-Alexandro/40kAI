"""Unit sprites / fallback markers."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_units_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    renders = list(w._units)
    if w._deploy_preview_units:
        existing_keys = {render.key for render in w._units}
        renders.extend(render for render in w._deploy_preview_units if render.key not in existing_keys)
    for render in renders:
        op = w._opacity_for_unit_render(render)
        painter.save()
        painter.setOpacity(max(0.0, min(1.0, op)))
        marker_radius = render.radius
        model_centers = render.model_centers or []
        icon = render.icon
        if icon is not None and not icon.isNull():
            if model_centers:
                icon_size = max(6.0, w.cell_size * w._model_icon_scale)
                for model_center in model_centers:
                    rect = QtCore.QRectF(
                        model_center.x() - icon_size / 2,
                        model_center.y() - icon_size / 2,
                        icon_size,
                        icon_size,
                    )
                    w._draw_pixmap_with_facing(painter, rect, icon, render.facing)
            else:
                icon_size = marker_radius * w._unit_icon_scale
                rect = QtCore.QRectF(
                    render.center.x() - icon_size / 2,
                    render.center.y() - icon_size / 2,
                    icon_size,
                    icon_size,
                )
                w._draw_pixmap_with_facing(painter, rect, icon, render.facing)
            painter.restore()
            continue

        size = max(6.0, marker_radius * 0.6)
        painter.setBrush(Theme.brush(render.color))
        painter.setPen(Theme.pen(Theme.outline, 0.8))
        centers = model_centers or [render.center]
        for center in centers:
            rect = QtCore.QRectF(center.x() - size / 2, center.y() - size / 2, size, size)
            painter.drawRect(rect)
        painter.restore()
