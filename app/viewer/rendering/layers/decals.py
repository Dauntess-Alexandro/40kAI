"""Ground decals (blood marks, scratch textures)."""

from __future__ import annotations

from PySide6 import QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_decals_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._decals or not w._decal_textures:
        return
    painter.save()
    painter.setClipRect(w._board_rect)
    for decal in w._decals:
        pixmap = w._decal_textures.get(decal.texture_key)
        if pixmap is None:
            continue
        w._draw_sprite(
            painter,
            pixmap,
            decal.center,
            rotation_deg=decal.rotation_deg,
            scale=decal.scale,
            alpha=0.9,
        )
    painter.restore()
