"""Debug drawing: hitboxes, optional paint/frame HUD (config ``viewer.debug.overlay``)."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_debug_overlay_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    painter.setTransform(QtGui.QTransform())

    draw_hitboxes = bool(w._viewer_debug_enabled or getattr(w, "_viewer_debug_overlay_flag", False))
    if draw_hitboxes:
        w._rebuild_unit_hitboxes_screen()
        if w._unit_hitboxes_screen:
            painter.save()
            pen = QtGui.QPen(QtGui.QColor(120, 220, 120, 180), 1.0)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            for rect in w._unit_hitboxes_screen.values():
                painter.drawRect(rect)
            painter.restore()

    cfg_overlay = getattr(w, "_viewer_debug_overlay_flag", False)
    if cfg_overlay:
        painter.save()
        painter.setPen(QtGui.QColor(255, 205, 120))
        painter.setFont(Theme.font(size=9, bold=True))
        serial = int(getattr(w, "_paint_serial", 0))
        painter.drawText(
            QtCore.QRectF(8, max(8.0, float(w.height()) - 52), 280, 22),
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            f"paint#{serial}",
        )
        last = getattr(w, "_last_click_screen", None)
        if last is not None:
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 120, 120, 200), 1.0))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 120, 120, 55)))
            r = 7.0
            painter.drawEllipse(last, r, r)
            painter.drawLine(QtCore.QPointF(last.x() - 14, last.y()), QtCore.QPointF(last.x() + 14, last.y()))
            painter.drawLine(QtCore.QPointF(last.x(), last.y() - 14), QtCore.QPointF(last.x(), last.y() + 14))
        painter.restore()

    if w._debug_overlay:
        debug_lines = [
            "DEBUG: (0,0) вверху слева",
            (
                f"Слои: terrain={'on' if w.render_terrain else 'off'}, "
                f"decals={'on' if w.render_decals else 'off'}, "
                f"fx={'on' if w.render_fx else 'off'}"
            ),
        ]
        if w._cursor_world is not None:
            state_pos = w._world_to_state_pos(w._cursor_world)
            if state_pos is not None:
                debug_lines.append(f"Курсор: x={state_pos[1]}, y={state_pos[0]}")
        painter.setPen(Theme.text)
        painter.setFont(Theme.font(size=9, bold=False))
        painter.drawText(
            QtCore.QRectF(8, 8, w.width() - 16, 60),
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
            "\n".join(debug_lines),
        )
