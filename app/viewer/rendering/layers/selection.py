"""AI activation glow under the active squad (world space)."""

from __future__ import annotations

import math
from time import monotonic

from PySide6 import QtCore, QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_selection_layer(ctx: LayerContext) -> None:
    """Soft blue ellipse under AI-activated unit formation."""
    w = ctx.widget
    painter = ctx.painter
    key = w._ai_activation_key
    render = w._unit_by_key.get(key) if key else None
    if render is None:
        return

    centers = list(render.model_centers or [render.center])
    cell = float(w.cell_size)
    min_x = min(c.x() for c in centers)
    max_x = max(c.x() for c in centers)
    min_y = min(c.y() for c in centers)
    max_y = max(c.y() for c in centers)
    cx = 0.5 * (min_x + max_x)
    cy = 0.5 * (min_y + max_y) + cell * 0.26

    span_x = max(max_x - min_x, cell * 0.48)
    span_y = max(max_y - min_y, cell * 0.42)
    t = monotonic()
    breath = 0.5 + 0.5 * math.sin(t * 1.65)
    pulse = 1.0 + 0.032 * math.sin(t * 1.9)
    rx = (span_x * 0.58 + cell * 0.62) * pulse
    ry = (span_y * 0.52 + cell * 0.48) * pulse

    unit_disc = QtCore.QRectF(-1.0, -1.0, 2.0, 2.0)
    painter.save()
    clip_pad = max(rx * 1.45, ry * 1.45, cell * 3.0)
    painter.setClipRect(w._board_rect.adjusted(-clip_pad, -clip_pad, clip_pad, clip_pad))
    painter.setPen(QtCore.Qt.NoPen)

    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
    painter.save()
    painter.translate(cx, cy)
    painter.scale(rx * 1.32, ry * 1.18)
    outer = QtGui.QRadialGradient(0.0, 0.0, 1.0)
    outer.setColorAt(0.0, QtGui.QColor(130, 205, 255, int(16 + 7 * breath)))
    outer.setColorAt(0.45, QtGui.QColor(85, 165, 235, int(9 + 4 * breath)))
    outer.setColorAt(0.72, QtGui.QColor(55, 120, 205, int(5 + 2 * breath)))
    outer.setColorAt(0.88, QtGui.QColor(40, 95, 175, int(2 + breath)))
    outer.setColorAt(1.0, QtGui.QColor(30, 85, 160, 0))
    painter.setBrush(QtGui.QBrush(outer))
    painter.drawEllipse(unit_disc)
    painter.restore()

    painter.setCompositionMode(QtGui.QPainter.CompositionMode_Plus)
    painter.save()
    painter.translate(cx, cy)
    painter.scale(rx * 0.92, ry * 0.84)
    core = QtGui.QRadialGradient(0.0, 0.0, 1.0)
    core.setColorAt(0.0, QtGui.QColor(200, 235, 255, int(14 + 9 * breath)))
    core.setColorAt(0.42, QtGui.QColor(120, 195, 255, int(8 + 5 * breath)))
    core.setColorAt(0.68, QtGui.QColor(90, 170, 240, int(4 + 2 * breath)))
    core.setColorAt(0.86, QtGui.QColor(60, 130, 210, int(2 + breath)))
    core.setColorAt(1.0, QtGui.QColor(0, 0, 0, 0))
    painter.setBrush(QtGui.QBrush(core))
    painter.drawEllipse(unit_disc)
    painter.restore()

    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
    painter.restore()
