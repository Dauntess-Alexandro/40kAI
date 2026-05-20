"""AI step phase pill near active squad."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_ai_phase_badge_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    meta = w._ai_activation_meta
    key = w._ai_activation_key
    if not meta or not (meta.get("phase") is not None or meta.get("step_kind") is not None):
        return
    badge_text = w._format_ai_phase_badge_text(meta)
    if not badge_text:
        return

    render = w._unit_by_key.get(key) if key else None
    if render is not None:
        cx, badge_bottom = w._ai_phase_badge_anchor_world(render)
    else:
        cx = (w._board_width * w.cell_size) * 0.5
        badge_bottom = 24.0

    font = Theme.font(10, bold=True)
    painter.setFont(font)
    fm = QtGui.QFontMetrics(font)
    pad_x, pad_y = 11.0, 6.0
    text_w = fm.horizontalAdvance(badge_text)
    text_h = fm.height()
    bg_w = text_w + pad_x * 2
    bg_h = text_h + pad_y * 2
    radius = min(bg_h * 0.5, 14.0)
    bg_rect = QtCore.QRectF(cx - bg_w * 0.5, badge_bottom - bg_h, bg_w, bg_h)
    margin = 4.0
    bg_rect.moveLeft(max(w._board_rect.left() + margin, min(bg_rect.left(), w._board_rect.right() - bg_w - margin)))

    path = QtGui.QPainterPath()
    path.addRoundedRect(bg_rect, radius, radius)

    painter.save()
    sh = QtGui.QPainterPath()
    sh.addRoundedRect(bg_rect.translated(1.5, 2.0), radius, radius)
    painter.fillPath(sh, QtGui.QColor(0, 0, 0, 76))

    grad = QtGui.QLinearGradient(bg_rect.topLeft(), bg_rect.bottomLeft())
    grad.setColorAt(0.0, QtGui.QColor(48, 58, 78, 246))
    grad.setColorAt(1.0, QtGui.QColor(24, 28, 38, 238))
    painter.fillPath(path, grad)

    bcol = QtGui.QColor(Theme.accent)
    bcol.setAlpha(210)
    pen = QtGui.QPen(bcol)
    pen.setWidthF(1.25)
    pen.setCosmetic(True)
    painter.setPen(pen)
    painter.setBrush(QtCore.Qt.NoBrush)
    painter.drawPath(path)

    align = int(QtCore.Qt.AlignCenter)
    shadow = QtGui.QPen(QtGui.QColor(0, 0, 0, 165))
    painter.setPen(shadow)
    painter.drawText(bg_rect.translated(0.6, 1.0), align, badge_text)
    painter.setPen(QtGui.QPen(QtGui.QColor(244, 240, 232, 252)))
    painter.drawText(bg_rect, align, badge_text)
    painter.restore()
