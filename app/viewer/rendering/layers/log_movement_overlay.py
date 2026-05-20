"""Hover/persistent overlay for movement lines from battle log."""

from __future__ import annotations

import math
from time import monotonic

from PySide6 import QtCore, QtGui

from app.viewer.rendering.hit_test import safe_int
from app.viewer.rendering.layer_context import LayerContext


def paint_log_movement_overlay_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    payload = w._log_move_overlay_hover or w._log_move_overlay_persistent
    if not isinstance(payload, dict):
        return

    from_pos = payload.get("from")
    to_pos = payload.get("to")
    if not isinstance(from_pos, (tuple, list)) or len(from_pos) < 2:
        return
    if not isinstance(to_pos, (tuple, list)) or len(to_pos) < 2:
        return

    from_cell = w._state_xy_to_view_xy(int(from_pos[0]), int(from_pos[1]))
    to_cell = w._state_xy_to_view_xy(int(to_pos[0]), int(to_pos[1]))
    if from_cell is None or to_cell is None:
        return

    from_center = w._cell_center(from_cell[0], from_cell[1])
    to_center = w._cell_center(to_cell[0], to_cell[1])
    no_move = bool(payload.get("no_move")) or (from_cell == to_cell)

    painter.save()
    if payload is w._log_move_overlay_hover:
        line_alpha = 150
        marker_alpha = 170
    else:
        line_alpha = 220
        marker_alpha = 235

    if not no_move:
        trail_icon = w._icon_for_unit_name(str(payload.get("unit_name") or ""))
        if trail_icon is not None and not trail_icon.isNull():
            ghost_alpha = 0.30 if payload is w._log_move_overlay_hover else 0.38
            painter.setOpacity(ghost_alpha)
            unit_id = safe_int(payload.get("unit_id"))
            matched_render = None
            if unit_id is not None:
                for render in w._units:
                    if int(render.key[1]) == int(unit_id):
                        matched_render = render
                        break

            if matched_render is not None and matched_render.model_centers:
                icon_size = max(6.0, w.cell_size * w._model_icon_scale)
                for model_center in matched_render.model_centers:
                    offset = model_center - matched_render.center
                    ghost_center = from_center + offset
                    ghost_rect = QtCore.QRectF(
                        ghost_center.x() - icon_size / 2,
                        ghost_center.y() - icon_size / 2,
                        icon_size,
                        icon_size,
                    )
                    painter.drawPixmap(ghost_rect, trail_icon, QtCore.QRectF(trail_icon.rect()))
            else:
                icon_size = max(6.0, w.cell_size * w._unit_icon_scale)
                ghost_rect = QtCore.QRectF(
                    from_center.x() - icon_size / 2,
                    from_center.y() - icon_size / 2,
                    icon_size,
                    icon_size,
                )
                painter.drawPixmap(ghost_rect, trail_icon, QtCore.QRectF(trail_icon.rect()))
        painter.setOpacity(1.0)
        path_pen = QtGui.QPen(QtGui.QColor(95, 192, 255, line_alpha), 2.6)
        path_pen.setCosmetic(True)
        path_pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(path_pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawLine(from_center, to_center)

        angle = math.atan2(to_center.y() - from_center.y(), to_center.x() - from_center.x())
        head_len = max(8.0, w.cell_size * 0.35)
        left = QtCore.QPointF(
            to_center.x() - head_len * math.cos(angle - math.pi / 6.0),
            to_center.y() - head_len * math.sin(angle - math.pi / 6.0),
        )
        right = QtCore.QPointF(
            to_center.x() - head_len * math.cos(angle + math.pi / 6.0),
            to_center.y() - head_len * math.sin(angle + math.pi / 6.0),
        )
        painter.setBrush(QtGui.QColor(95, 192, 255, line_alpha))
        painter.drawPolygon(QtGui.QPolygonF([to_center, left, right]))

        move_cells = payload.get("distance")
        try:
            move_cells = int(move_cells)
        except (TypeError, ValueError):
            move_cells = 0
        if move_cells > 0:
            badge_center = QtCore.QPointF(
                (from_center.x() + to_center.x()) * 0.5,
                (from_center.y() + to_center.y()) * 0.5,
            )
            badge_text = f"{move_cells} кл."
            font = QtGui.QFont(painter.font())
            font.setPointSizeF(max(8.0, float(font.pointSizeF() if font.pointSizeF() > 0 else 10.0)))
            font.setBold(True)
            painter.setFont(font)
            fm = QtGui.QFontMetricsF(font)
            text_rect = fm.boundingRect(badge_text)
            pad_x = 8.0
            pad_y = 4.0
            badge_rect = QtCore.QRectF(
                badge_center.x() - text_rect.width() * 0.5 - pad_x,
                badge_center.y() - text_rect.height() * 0.5 - pad_y,
                text_rect.width() + pad_x * 2.0,
                text_rect.height() + pad_y * 2.0,
            )
            badge_bg = QtGui.QColor(95, 192, 255, max(120, line_alpha - 25))
            badge_border = QtGui.QPen(QtGui.QColor(135, 214, 255, max(170, line_alpha)), 1.2)
            badge_border.setCosmetic(True)
            painter.setPen(badge_border)
            painter.setBrush(QtGui.QBrush(badge_bg))
            painter.drawRoundedRect(badge_rect, 6.0, 6.0)
            painter.setPen(QtGui.QPen(QtGui.QColor(12, 20, 32, 245)))
            painter.drawText(badge_rect, QtCore.Qt.AlignCenter, badge_text)
    else:
        radius = max(6.0, w.cell_size * 0.34)
        pulse = 0.5 + 0.5 * math.sin(monotonic() * 6.0)
        ring_color = QtGui.QColor(255, 210, 92, int(130 + 80 * pulse))
        ring_pen = QtGui.QPen(ring_color, 2.2)
        ring_pen.setCosmetic(True)
        painter.setPen(ring_pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawEllipse(from_center, radius, radius)
        painter.drawEllipse(from_center, radius * 1.35, radius * 1.35)

    start_pen = QtGui.QPen(QtGui.QColor(68, 214, 118, marker_alpha), 2.0)
    start_pen.setCosmetic(True)
    painter.setPen(start_pen)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(68, 214, 118, 85)))
    painter.drawEllipse(from_center, max(4.0, w.cell_size * 0.22), max(4.0, w.cell_size * 0.22))

    end_pen = QtGui.QPen(QtGui.QColor(255, 109, 109, marker_alpha), 2.0)
    end_pen.setCosmetic(True)
    painter.setPen(end_pen)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 109, 109, 95)))
    painter.drawEllipse(to_center, max(4.0, w.cell_size * 0.24), max(4.0, w.cell_size * 0.24))
    painter.restore()
