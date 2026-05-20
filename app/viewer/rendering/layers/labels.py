"""Objective name labels (world space)."""

from __future__ import annotations

from PySide6 import QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_labels_layer(ctx: LayerContext) -> None:
    painter = ctx.painter
    text_font = Theme.font(size=8, bold=True)
    painter.setFont(text_font)
    painter.setPen(Theme.text)
    for label, pos in ctx.widget._objective_labels:
        painter.drawText(pos, label)
