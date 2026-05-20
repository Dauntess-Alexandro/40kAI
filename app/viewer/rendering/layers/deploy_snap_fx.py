"""Deploy placement snap ring animation."""

from __future__ import annotations

from time import monotonic

from PySide6 import QtCore, QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_deploy_snap_fx_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._deploy_placement_fx:
        return
    now = monotonic()
    painter.save()
    painter.setBrush(QtCore.Qt.NoBrush)
    for fx in w._deploy_placement_fx:
        elapsed = now - fx.t0
        if elapsed < 0.0 or elapsed > fx.duration:
            continue
        progress = max(0.0, min(1.0, elapsed / fx.duration))
        alpha = int(180 * (1.0 - progress))
        radius = w.cell_size * (0.30 + 0.28 * progress)
        pen = QtGui.QPen(QtGui.QColor(120, 230, 255, alpha), 1.8)
        painter.setPen(pen)
        for state_x, state_y in fx.cells:
            view_cell = w._state_xy_to_view_xy(state_x, state_y)
            if view_cell is None:
                continue
            center = w._cell_center(view_cell[0], view_cell[1])
            painter.drawEllipse(center, radius, radius)
    painter.restore()
