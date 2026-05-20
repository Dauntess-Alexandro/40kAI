"""Hover unit footprint + threat / weapon-range ellipses."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_unit_tooltip_overlays_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if w._hover_unit_key is None:
        return
    unit = w._state_unit(w._hover_unit_key)
    if not unit:
        return
    painter.save()
    base_pen = QtGui.QPen(QtGui.QColor(112, 192, 131, 210), 1.8)
    base_pen.setCosmetic(True)
    painter.setPen(base_pen)
    painter.setBrush(QtGui.QColor(112, 192, 131, 38))
    unit_cells = w._unit_model_view_cells(unit) or (
        [w._unit_anchor_view_cell(unit)] if w._unit_anchor_view_cell(unit) else []
    )
    for cell in unit_cells:
        if cell is None:
            continue
        rect = QtCore.QRectF(cell[0] * w.cell_size, cell[1] * w.cell_size, w.cell_size, w.cell_size)
        painter.drawRect(rect)

    threat = w._hover_tooltip_text.get("threat") if isinstance(w._hover_tooltip_text, dict) else {}
    los_keys = (threat or {}).get("enemies_in_los_keys") or []
    los_pen = QtGui.QPen(QtGui.QColor(242, 188, 76, 190), 1.5)
    los_pen.setCosmetic(True)
    painter.setPen(los_pen)
    painter.setBrush(QtGui.QColor(242, 188, 76, 20))
    for key in los_keys:
        target = w._unit_by_key.get(key)
        if target is None:
            continue
        painter.drawEllipse(target.center, target.radius + 3, target.radius + 3)

    if w._hover_weapon_range is not None:
        weapon_keys = w._enemy_keys_in_range_of(unit, forced_range=w._hover_weapon_range)
        w_pen = QtGui.QPen(QtGui.QColor(169, 123, 245, 210), 1.8)
        w_pen.setCosmetic(True)
        painter.setPen(w_pen)
        painter.setBrush(QtGui.QColor(169, 123, 245, 28))
        for key in weapon_keys:
            target = w._unit_by_key.get(key)
            if target is None:
                continue
            painter.drawEllipse(target.center, target.radius + 5, target.radius + 5)

    if w._hover_status_enemy_ids:
        s_pen = QtGui.QPen(QtGui.QColor(255, 245, 120, 230), 1.6)
        s_pen.setCosmetic(True)
        painter.setPen(s_pen)
        painter.setBrush(QtGui.QColor(255, 245, 120, 24))
        for key, target in w._unit_by_key.items():
            if target is None:
                continue
            if key[0] == unit.get("side"):
                continue
            if int(key[1]) not in w._hover_status_enemy_ids:
                continue
            painter.drawEllipse(target.center, target.radius + 7, target.radius + 7)
    painter.restore()
