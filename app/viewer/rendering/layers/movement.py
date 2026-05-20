"""Reachable / advance movement cell highlights."""

from __future__ import annotations

from PySide6 import QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_movement_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._should_show_movement():
        return
    if not w._move_reachable_highlights and not w._advance_reachable_highlights:
        return
    move_fill = QtGui.QColor(72, 130, 255, 54)
    move_border = QtGui.QPen(QtGui.QColor(72, 130, 255, 170), 1.0)
    move_border.setCosmetic(True)
    painter.setPen(move_border)
    painter.setBrush(QtGui.QBrush(move_fill))
    for rect in w._move_reachable_highlights:
        painter.drawRect(rect)

    advance_fill = QtGui.QColor(236, 194, 64, 60)
    advance_border = QtGui.QPen(QtGui.QColor(236, 194, 64, 180), 1.0)
    advance_border.setCosmetic(True)
    painter.setPen(advance_border)
    painter.setBrush(QtGui.QBrush(advance_fill))
    for rect in w._advance_reachable_highlights:
        painter.drawRect(rect)
