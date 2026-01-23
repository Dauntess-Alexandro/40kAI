from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple
import csv


@dataclass(frozen=True)
class UnitInfo:
    unit_id: int
    side: str
    coord: Tuple[int, int]


@dataclass(frozen=True)
class ObjectiveInfo:
    coord: Tuple[int, int]


@dataclass(frozen=True)
class BoardState:
    grid: List[List[int]]
    width: int
    height: int
    units: List[UnitInfo]
    objectives: List[ObjectiveInfo]


def _safe_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_board(path: str | Path = "board.txt") -> Optional[BoardState]:
    board_path = Path(path)
    if not board_path.exists():
        return None

    grid: List[List[int]] = []
    try:
        with board_path.open(newline="") as handle:
            reader = csv.reader(handle)
            for row in reader:
                if not row:
                    continue
                values: List[int] = []
                for cell in row:
                    value = _safe_int(cell.strip())
                    if value is None:
                        continue
                    values.append(value)
                if values:
                    grid.append(values)
    except OSError:
        return None

    if not grid:
        return None

    height = len(grid)
    width = max(len(row) for row in grid)

    units: List[UnitInfo] = []
    objectives: List[ObjectiveInfo] = []

    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == 3:
                objectives.append(ObjectiveInfo(coord=(row_idx, col_idx)))
            elif value >= 20:
                units.append(UnitInfo(unit_id=value, side="model", coord=(row_idx, col_idx)))
            elif 10 < value < 20:
                units.append(UnitInfo(unit_id=value, side="enemy", coord=(row_idx, col_idx)))

    return BoardState(
        grid=grid,
        width=width,
        height=height,
        units=units,
        objectives=objectives,
    )


def clamp_viewport(
    center: Tuple[int, int],
    size: Tuple[int, int],
    bounds: Tuple[int, int],
) -> Tuple[int, int]:
    center_x, center_y = center
    view_w, view_h = size
    max_x, max_y = bounds
    half_w = max(0, view_w // 2)
    half_h = max(0, view_h // 2)
    min_x = max(0, center_x - half_w)
    min_y = max(0, center_y - half_h)
    max_start_x = max(0, max_x - view_w)
    max_start_y = max(0, max_y - view_h)
    return min(min_x, max_start_x), min(min_y, max_start_y)


def slice_grid(
    grid: Sequence[Sequence[int]],
    start: Tuple[int, int],
    size: Tuple[int, int],
) -> List[List[int]]:
    start_x, start_y = start
    view_w, view_h = size
    sliced: List[List[int]] = []
    for x in range(start_x, min(start_x + view_h, len(grid))):
        row = grid[x]
        sliced.append(list(row[start_y:start_y + view_w]))
    return sliced
