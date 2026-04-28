from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from PySide6 import QtCore, QtGui


@dataclass(frozen=True)
class CellsZoneStyle:
    """Стиль зоны клеток (full/rapid)."""

    rgb: Tuple[int, int, int]
    fill_alpha: int
    border_alpha: int
    border_width: float


@dataclass(frozen=True)
class RapidHatchStyle:
    """Параметры hatch-паттерна rapid-зоны."""

    tile_size: int
    line_width: float
    line_rgba: Tuple[int, int, int, int]
    lines: Tuple[Tuple[int, int, int, int], ...]


# Full-zone (вся дальность стрельбы): средняя заметность.
# Чтобы сделать full заметнее: увеличьте fill_alpha и/или border_alpha/border_width.
SHOOTING_FULL_ZONE_STYLE = CellsZoneStyle(
    rgb=(230, 174, 82),
    fill_alpha=16,
    border_alpha=64,
    border_width=0.65,
)

# Rapid-zone (половина дальности): визуально приоритетнее full.
# Чтобы сделать rapid менее шумным: снижайте border_alpha и hatch line_rgba alpha.
SHOOTING_RAPID_ZONE_STYLE = CellsZoneStyle(
    rgb=(230, 174, 82),
    fill_alpha=0,
    border_alpha=165,
    border_width=1.35,
)

# Hatch rapid: редкие диагонали. Для большей плотности уменьшайте tile_size
# или добавляйте линии в набор lines. Для меньшего шума делайте наоборот.
SHOOTING_RAPID_HATCH_STYLE = RapidHatchStyle(
    tile_size=14,
    line_width=1.8,
    line_rgba=(230, 174, 82, 82),
    lines=(
        (-2, 13, 4, 7),
        (3, 13, 13, 3),
        (10, 13, 16, 7),
    ),
)


def zone_fill_color(style: CellsZoneStyle) -> QtGui.QColor:
    color = QtGui.QColor(*style.rgb)
    color.setAlpha(style.fill_alpha)
    return color


def zone_border_pen(style: CellsZoneStyle) -> QtGui.QPen:
    pen = QtGui.QPen(QtGui.QColor(style.rgb[0], style.rgb[1], style.rgb[2], style.border_alpha), style.border_width)
    pen.setCosmetic(True)
    return pen


def rapid_hatch_pen(style: RapidHatchStyle) -> QtGui.QPen:
    pen = QtGui.QPen(QtGui.QColor(*style.line_rgba), style.line_width)
    pen.setCapStyle(QtCore.Qt.RoundCap)
    return pen
