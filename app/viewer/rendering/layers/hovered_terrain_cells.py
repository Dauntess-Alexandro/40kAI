"""Highlight terrain feature cells under hover."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_hovered_terrain_cells_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    feature = w._hover_terrain_feature
    if not isinstance(feature, dict):
        return
    cells = list(feature.get("cells") or [])
    if not cells:
        return
    painter.save()
    pen = QtGui.QPen(QtGui.QColor(247, 186, 78, 215), 1.8)
    pen.setCosmetic(True)
    painter.setPen(pen)
    painter.setBrush(QtGui.QColor(247, 186, 78, 45))
    for cell in cells:
        if not isinstance(cell, (list, tuple)) or len(cell) < 2:
            continue
        row = int(cell[0])
        col = int(cell[1])
        rect = QtCore.QRectF(
            col * w.cell_size,
            row * w.cell_size,
            w.cell_size,
            w.cell_size,
        )
        painter.drawRect(rect)
    painter.restore()
