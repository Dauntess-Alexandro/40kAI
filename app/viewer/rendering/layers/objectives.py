"""Objective markers + control radius (world space)."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_objectives_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    for objective in w._objectives:
        painter.setBrush(Theme.brush(objective.color))
        painter.setPen(Theme.pen(Theme.outline, 0.8))
        painter.drawEllipse(objective.center, objective.radius, objective.radius)
        if w._show_objective_radius:
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
