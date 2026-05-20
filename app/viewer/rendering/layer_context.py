"""Shared context passed to modular board render layers (Sprint 4+)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PySide6 import QtGui


@dataclass
class LayerContext:
    """Minimal coupling: layers read state from the board widget."""

    widget: Any
    painter: QtGui.QPainter
