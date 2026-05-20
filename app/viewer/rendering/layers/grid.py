"""Board grid lines (screen space, cosmetic pen)."""

from __future__ import annotations

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_grid_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if w._board_rect.isEmpty() or w._scale <= 0:
        return
    painter.save()
    painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
    pen = Theme.pen(Theme.grid, 1.0)
    pen.setCosmetic(True)
    painter.setPen(pen)

    pan_x, pan_y = w._snap_pan_to_pixels(w._pan)
    scale = w._scale
    cell = float(w.cell_size)
    width = w.width()
    height = w.height()
    board_screen_rect = QtCore.QRectF(
        pan_x,
        pan_y,
        w._board_width * cell * scale,
        w._board_height * cell * scale,
    )
    painter.setClipRect(board_screen_rect)
    left_world = (-pan_x) / scale
    right_world = (width - pan_x) / scale
    top_world = (-pan_y) / scale
    bottom_world = (height - pan_y) / scale

    min_col = max(0, int(left_world // cell))
    max_col = min(w._board_width, int(right_world // cell) + 1)
    min_row = max(0, int(top_world // cell))
    max_row = min(w._board_height, int(bottom_world // cell) + 1)

    ratio = w.devicePixelRatioF() or 1.0
    pixel = 1.0 / ratio

    for col in range(min_col, max_col + 1):
        world_x = col * cell
        screen_x = pan_x + world_x * scale
        screen_x = round(screen_x / pixel) * pixel
        painter.drawLine(
            QtCore.QPointF(screen_x, board_screen_rect.top()),
            QtCore.QPointF(screen_x, board_screen_rect.bottom()),
        )

    for row in range(min_row, max_row + 1):
        world_y = row * cell
        screen_y = pan_y + world_y * scale
        screen_y = round(screen_y / pixel) * pixel
        painter.drawLine(
            QtCore.QPointF(board_screen_rect.left(), screen_y),
            QtCore.QPointF(board_screen_rect.right(), screen_y),
        )

    painter.restore()
