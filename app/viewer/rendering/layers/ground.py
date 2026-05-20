"""Ground texture tiling (world space)."""

from __future__ import annotations

import math

from PySide6 import QtCore, QtGui

from app.viewer.rendering.layer_context import LayerContext


def paint_ground_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._ground_textures or w._board_rect.isEmpty():
        return
    view_rect = w._view_world_rect()
    tile_size = 256.0
    start_x = int(math.floor(view_rect.left() / tile_size))
    end_x = int(math.ceil(view_rect.right() / tile_size))
    start_y = int(math.floor(view_rect.top() / tile_size))
    end_y = int(math.ceil(view_rect.bottom() / tile_size))
    painter.save()
    painter.setClipRect(w._board_rect)
    for ty in range(start_y, end_y + 1):
        for tx in range(start_x, end_x + 1):
            pixmap = w._ground_textures[(tx + ty) % len(w._ground_textures)]
            world_x = tx * tile_size
            world_y = ty * tile_size
            painter.drawPixmap(
                QtCore.QRectF(world_x, world_y, tile_size, tile_size),
                pixmap,
                QtCore.QRectF(0, 0, pixmap.width(), pixmap.height()),
            )
    painter.restore()
