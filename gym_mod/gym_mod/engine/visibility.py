import math
from typing import Iterable


Cell = tuple[int, int]
Point = tuple[float, float]


def supercover_line_cells(a_cell: Cell, b_cell: Cell) -> list[Cell]:
    """
    Deterministic supercover between two grid cells.
    Returns every crossed cell (including start/end).
    """
    x0, y0 = int(a_cell[0]), int(a_cell[1])
    x1, y1 = int(b_cell[0]), int(b_cell[1])

    dx = x1 - x0
    dy = y1 - y0
    nx = abs(dx)
    ny = abs(dy)
    sign_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    sign_y = 0 if dy == 0 else (1 if dy > 0 else -1)

    x, y = x0, y0
    result: list[Cell] = [(x, y)]
    ix = 0
    iy = 0

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
        result.append((x, y))

    return result


def get_cell_sample_points(cell: Cell, mode: str = "single_ray") -> list[Point]:
    """
    Future-ready sampling API. For now single-ray is enough.
    """
    cx = float(int(cell[0])) + 0.5
    cy = float(int(cell[1])) + 0.5
    if mode == "single_ray":
        return [(cx, cy)]

    corners = [
        (float(int(cell[0])) + 0.05, float(int(cell[1])) + 0.05),
        (float(int(cell[0])) + 0.95, float(int(cell[1])) + 0.05),
        (float(int(cell[0])) + 0.05, float(int(cell[1])) + 0.95),
        (float(int(cell[0])) + 0.95, float(int(cell[1])) + 0.95),
    ]
    if mode == "multi_ray_5":
        return [(cx, cy), *corners]

    if mode == "multi_ray_9":
        edges = [
            (cx, float(int(cell[1])) + 0.05),
            (cx, float(int(cell[1])) + 0.95),
            (float(int(cell[0])) + 0.05, cy),
            (float(int(cell[0])) + 0.95, cy),
        ]
        return [(cx, cy), *corners, *edges]

    return [(cx, cy)]


def raytrace(a_point: Point, b_point: Point) -> list[Cell]:
    """
    Generic point raytrace. Current implementation is deterministic and
    compatible with single-ray center-to-center mode.
    """
    a_cell = (int(math.floor(a_point[0])), int(math.floor(a_point[1])))
    b_cell = (int(math.floor(b_point[0])), int(math.floor(b_point[1])))
    return supercover_line_cells(a_cell, b_cell)


def has_line_of_sight(a_cell: Cell, b_cell: Cell, opaque_cells_set: Iterable[Cell]) -> bool:
    report = visibility_report(a_cell, b_cell, opaque_cells_set=opaque_cells_set)
    return bool(report["los"])


def is_obscured(a_cell: Cell, b_cell: Cell, obscuring_cells_set: Iterable[Cell]) -> bool:
    report = visibility_report(a_cell, b_cell, obscuring_cells_set=obscuring_cells_set)
    return bool(report["obscured"])


def visibility_report(
    a_cell: Cell,
    b_cell: Cell,
    opaque_cells_set: Iterable[Cell] | None = None,
    obscuring_cells_set: Iterable[Cell] | None = None,
    visibility_mode: str = "single_ray",
) -> dict:
    opaque = set((int(x), int(y)) for x, y in (opaque_cells_set or []))
    obscuring = set((int(x), int(y)) for x, y in (obscuring_cells_set or []))

    a_samples = get_cell_sample_points(a_cell, mode=visibility_mode)
    b_samples = get_cell_sample_points(b_cell, mode=visibility_mode)

    # Single-ray for now (first sample pair), API is ready for future multi-ray.
    crossed = raytrace(a_samples[0], b_samples[0])

    middle_cells = crossed[1:-1] if len(crossed) >= 2 else []
    blocked_by = next((cell for cell in middle_cells if cell in opaque), None)
    obscured = any(cell in obscuring for cell in middle_cells)

    return {
        "los": blocked_by is None,
        "obscured": bool(obscured),
        "crossed_cells": crossed,
        "blocked_by": blocked_by,
        "visibility_mode": visibility_mode,
    }

