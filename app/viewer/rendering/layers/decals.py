"""Ground decals (blood marks, scratch textures)."""

from __future__ import annotations

from PySide6 import QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_decals_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    has_world_decals = bool(w._decals and w._decal_textures)
    has_scorch = bool(getattr(w, "_fx_scorch_decals", None))
    if not has_world_decals and not has_scorch:
        return
    painter.save()
    painter.setClipRect(w._board_rect)
    if has_scorch:
        w._draw_scorch_decals(painter)
    if not has_world_decals:
        painter.restore()
        return
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
