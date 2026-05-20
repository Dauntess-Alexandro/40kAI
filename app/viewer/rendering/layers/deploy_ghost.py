"""Deploy preview ghost icons / fallback ellipses."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_deploy_ghost_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._deploy_ghost_cells:
        return

    ghost_icon = w._icon_for_unit_name(w._deploy_ghost_unit_name) if w._deploy_ghost_unit_name else None
    alpha = w._deploy_ghost_alpha_valid if w._deploy_ghost_valid else w._deploy_ghost_alpha_invalid

    painter.save()
    painter.setOpacity(max(0.0, min(1.0, alpha)))

    if ghost_icon is not None and not ghost_icon.isNull():
        icon_size = max(6.0, w.cell_size * w._model_icon_scale)
        for state_x, state_y in w._deploy_ghost_cells:
            view_cell = w._state_xy_to_view_xy(state_x, state_y)
            if view_cell is None:
                continue
            center = w._cell_center(view_cell[0], view_cell[1])
            rect = QtCore.QRectF(
                center.x() - icon_size / 2,
                center.y() - icon_size / 2,
                icon_size,
                icon_size,
            )
            painter.drawPixmap(rect, ghost_icon, QtCore.QRectF(ghost_icon.rect()))
    else:
        color = QtGui.QColor(70, 220, 120, 110) if w._deploy_ghost_valid else QtGui.QColor(220, 70, 70, 120)
        border = QtGui.QColor(70, 220, 120, 190) if w._deploy_ghost_valid else QtGui.QColor(220, 70, 70, 210)
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtGui.QPen(border, 1.3))
        size = w.cell_size * 0.62
        for state_x, state_y in w._deploy_ghost_cells:
            view_cell = w._state_xy_to_view_xy(state_x, state_y)
            if view_cell is None:
                continue
            center = w._cell_center(view_cell[0], view_cell[1])
            rect = QtCore.QRectF(center.x() - size / 2, center.y() - size / 2, size, size)
            painter.drawEllipse(rect)

    painter.setOpacity(1.0)
    if w._deploy_ghost_valid is False:
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor(220, 70, 70, 180), 1.4))
        ring_size = w.cell_size * 0.68
        for state_x, state_y in w._deploy_ghost_cells:
            view_cell = w._state_xy_to_view_xy(state_x, state_y)
            if view_cell is None:
                continue
            center = w._cell_center(view_cell[0], view_cell[1])
            rect = QtCore.QRectF(center.x() - ring_size / 2, center.y() - ring_size / 2, ring_size, ring_size)
            painter.drawEllipse(rect)
    painter.restore()
