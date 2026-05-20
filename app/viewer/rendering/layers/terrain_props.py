"""Terrain props sprites (barrels, terrain pieces); invoked via ``draw_terrain_features``."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_terrain_props_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._props:
        return
    painter.save()
    painter.setClipRect(w._board_rect)
    for prop in w._props:
        prop_pixmap = w._terrain_texture_by_name(prop.sprite_name) if prop.sprite_name else None
        if prop_pixmap is None:
            prop_pixmap = w._prop_textures.get(prop.kind) if prop.kind else None
        if prop_pixmap is None:
            if prop.debug_rect is not None:
                painter.save()
                pen = QtGui.QPen(QtGui.QColor(220, 80, 80, 220), 1.5)
                pen.setCosmetic(True)
                painter.setPen(pen)
                painter.setBrush(QtGui.QColor(220, 80, 80, 90))
                painter.drawRect(prop.debug_rect)
                painter.setPen(QtGui.QColor(240, 235, 235, 235))
                painter.setFont(Theme.font(size=8, bold=True))
                painter.drawText(
                    prop.debug_rect.adjusted(2.0, 2.0, -2.0, -2.0),
                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                    str(prop.kind or "terrain"),
                )
                painter.restore()
            continue
        if w.render_prop_shadows:
            shadow_pixmap = w._shadow_textures.get(prop.kind)
            if shadow_pixmap is not None:
                shadow_center = prop.center + QtCore.QPointF(8.0, 12.0)
                w._draw_sprite(
                    painter,
                    shadow_pixmap,
                    shadow_center,
                    rotation_deg=prop.rotation_deg,
                    scale=prop.scale,
                    alpha=0.7,
                )
        if prop.draw_rect is not None:
            source_rect = w._terrain_content_rect(prop.sprite_name, prop_pixmap)
            draw_rect = w._fit_pixmap_in_rect(
                prop_pixmap,
                prop.draw_rect,
                inset_ratio=w._terrain_barrel_cell_scale,
                source_rect=source_rect,
            )
            if prop.rotation_deg:
                painter.save()
                painter.translate(draw_rect.center())
                painter.rotate(prop.rotation_deg)
                rotated_rect = QtCore.QRectF(
                    -draw_rect.width() * 0.5,
                    -draw_rect.height() * 0.5,
                    draw_rect.width(),
                    draw_rect.height(),
                )
                painter.drawPixmap(rotated_rect, prop_pixmap, source_rect)
                painter.restore()
            else:
                painter.drawPixmap(draw_rect, prop_pixmap, source_rect)
            continue

        w._draw_sprite(
            painter,
            prop_pixmap,
            prop.center,
            rotation_deg=prop.rotation_deg,
            scale=prop.scale,
            alpha=1.0,
        )
    painter.restore()
