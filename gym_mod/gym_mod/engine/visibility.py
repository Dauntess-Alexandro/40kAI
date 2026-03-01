import math
import os
from typing import Iterable

Cell = tuple[int, int]
Point = tuple[float, float]


def _as_cell_set(cells: Iterable[Cell] | None) -> set[Cell]:
    if not cells:
        return set()
    return { (int(x), int(y)) for x, y in cells }


def _is_debug_enabled() -> bool:
    los_raw = os.getenv("LOS_DEBUG")
    los_effective = "1" if los_raw is None else str(los_raw).strip()
    terrain_effective = str(os.getenv("TERRAIN_DEBUG", "0")).strip()
    return los_effective != "0" or terrain_effective != "0"


def _short_cells(cells: list[Cell], edge: int = 5) -> str:
    if len(cells) <= edge * 2:
        return str(cells)
    head = cells[:edge]
    tail = cells[-edge:]
    return f"{head} ... {tail} (len={len(cells)})"


def _debug_log(msg: str) -> None:
    if _is_debug_enabled():
        print(f"[LOS] {msg}")


def supercover_line_cells(a_cell: Cell, b_cell: Cell) -> list[Cell]:
    """Детерминированная supercover-линия между центрами клеток."""
    x0, y0 = int(a_cell[0]), int(a_cell[1])
    x1, y1 = int(b_cell[0]), int(b_cell[1])

    dx = x1 - x0
    dy = y1 - y0
    nx = abs(dx)
    ny = abs(dy)
    sign_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    sign_y = 0 if dy == 0 else (1 if dy > 0 else -1)

    x, y = x0, y0
    ix, iy = 0, 0
    cells = [(x, y)]

    while ix < nx or iy < ny:
        lhs = (1 + 2 * ix) * ny
        rhs = (1 + 2 * iy) * nx
        if lhs == rhs:
            x += sign_x
            y += sign_y
            ix += 1
            iy += 1
        elif lhs < rhs:
            x += sign_x
            ix += 1
        else:
            y += sign_y
            iy += 1
        cells.append((x, y))

    return cells


def get_cell_sample_points(cell: Cell, mode: str = "single_ray") -> list[Point]:
    x, y = int(cell[0]), int(cell[1])
    cx, cy = x + 0.5, y + 0.5
    if mode == "single_ray":
        return [(cx, cy)]
    if mode == "multi_ray_5":
        return [(cx, cy), (x, y), (x + 1.0, y), (x, y + 1.0), (x + 1.0, y + 1.0)]
    if mode == "multi_ray_9":
        return [
            (x + 0.25, y + 0.25), (cx, y + 0.25), (x + 0.75, y + 0.25),
            (x + 0.25, cy), (cx, cy), (x + 0.75, cy),
            (x + 0.25, y + 0.75), (cx, y + 0.75), (x + 0.75, y + 0.75),
        ]
    raise ValueError(f"Неизвестный visibility mode: {mode}")


def raytrace(a_point: Point, b_point: Point) -> list[Cell]:
    """Базовый трассировщик точки-точки для будущих multi-ray режимов."""
    ax, ay = float(a_point[0]), float(a_point[1])
    bx, by = float(b_point[0]), float(b_point[1])
    dx = bx - ax
    dy = by - ay
    steps = max(1, int(max(abs(dx), abs(dy)) * 2))

    cells: list[Cell] = []
    for i in range(steps + 1):
        t = i / steps
        x = ax + dx * t
        y = ay + dy * t
        cell = (math.floor(x), math.floor(y))
        if not cells or cells[-1] != cell:
            cells.append(cell)
    return cells


def visibility_report(
    a_cell: Cell,
    b_cell: Cell,
    opaque_set: Iterable[Cell] | None = None,
    obscuring_set: Iterable[Cell] | None = None,
) -> dict:
    opaque_cells = _as_cell_set(opaque_set)
    obscuring_cells = _as_cell_set(obscuring_set)
    crossed_cells = supercover_line_cells(a_cell, b_cell)

    _debug_log(f"visibility_report: a_cell={a_cell}, b_cell={b_cell}")

    middle_cells = crossed_cells[1:-1] if len(crossed_cells) > 2 else []
    blocked_by = next((cell for cell in middle_cells if cell in opaque_cells), None)
    los = blocked_by is None
    obscured = any(cell in obscuring_cells for cell in middle_cells)

    _debug_log(
        "result: "
        f"crossed_cells={_short_cells(crossed_cells)}, "
        f"los={los}, obscured={obscured}, blocked_by={blocked_by}"
    )

    return {
        "los": los,
        "obscured": obscured,
        "crossed_cells": crossed_cells,
        "blocked_by": blocked_by,
    }


def has_line_of_sight(a_cell: Cell, b_cell: Cell, opaque_cells_set: Iterable[Cell] | None = None) -> bool:
    return bool(visibility_report(a_cell, b_cell, opaque_set=opaque_cells_set)["los"])


def is_obscured(a_cell: Cell, b_cell: Cell, obscuring_cells_set: Iterable[Cell] | None = None) -> bool:
    return bool(visibility_report(a_cell, b_cell, obscuring_set=obscuring_cells_set)["obscured"])
