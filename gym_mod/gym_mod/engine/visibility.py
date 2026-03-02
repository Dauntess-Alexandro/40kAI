import math
from typing import Iterable


Cell = tuple[int, int]
Point = tuple[float, float]

_VALID_VISIBILITY_MODES = {"single_ray", "multi_ray_5", "multi_ray_9"}


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


def _normalize_mode(mode: str) -> str:
    mode_raw = str(mode or "single_ray").strip().lower()
    if mode_raw in _VALID_VISIBILITY_MODES:
        return mode_raw
    return "single_ray"


def get_cell_sample_points(cell: Cell, mode: str = "single_ray") -> list[Point]:
    """
    Future-ready sampling API. Supports single/multi-ray modes.
    """
    mode = _normalize_mode(mode)

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

    edges = [
        (cx, float(int(cell[1])) + 0.05),
        (cx, float(int(cell[1])) + 0.95),
        (float(int(cell[0])) + 0.05, cy),
        (float(int(cell[0])) + 0.95, cy),
    ]
    return [(cx, cy), *corners, *edges]


def raytrace(a_point: Point, b_point: Point) -> list[Cell]:
    """
    Point-to-point deterministic grid traversal (supercover-style).
    Unlike cell-center fallback, this keeps corner/edge sample differences,
    so multi-ray modes produce distinct rays.
    """
    x0, y0 = float(a_point[0]), float(a_point[1])
    x1, y1 = float(b_point[0]), float(b_point[1])

    x = int(math.floor(x0))
    y = int(math.floor(y0))
    x_end = int(math.floor(x1))
    y_end = int(math.floor(y1))

    cells: list[Cell] = [(x, y)]
    if (x, y) == (x_end, y_end):
        return cells

    dx = x1 - x0
    dy = y1 - y0

    step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

    if step_x != 0:
        t_delta_x = abs(1.0 / dx)
        next_x_boundary = (x + 1.0) if step_x > 0 else float(x)
        t_max_x = ((next_x_boundary - x0) / dx) if step_x > 0 else ((x0 - next_x_boundary) / (-dx))
    else:
        t_delta_x = float("inf")
        t_max_x = float("inf")

    if step_y != 0:
        t_delta_y = abs(1.0 / dy)
        next_y_boundary = (y + 1.0) if step_y > 0 else float(y)
        t_max_y = ((next_y_boundary - y0) / dy) if step_y > 0 else ((y0 - next_y_boundary) / (-dy))
    else:
        t_delta_y = float("inf")
        t_max_y = float("inf")

    while (x, y) != (x_end, y_end):
        if t_max_x < t_max_y:
            x += step_x
            t_max_x += t_delta_x
            cells.append((x, y))
            continue
        if t_max_y < t_max_x:
            y += step_y
            t_max_y += t_delta_y
            cells.append((x, y))
            continue

        # Corner hit: include both adjacent cells deterministically.
        x += step_x
        cells.append((x, y))
        y += step_y
        cells.append((x, y))
        t_max_x += t_delta_x
        t_max_y += t_delta_y

    dedup: list[Cell] = []
    for cell in cells:
        if not dedup or dedup[-1] != cell:
            dedup.append(cell)
    return dedup


def has_line_of_sight(a_cell: Cell, b_cell: Cell, opaque_cells_set: Iterable[Cell], visibility_mode: str = "single_ray") -> bool:
    report = visibility_report(a_cell, b_cell, opaque_cells_set=opaque_cells_set, visibility_mode=visibility_mode)
    return bool(report["los"])


def is_obscured(a_cell: Cell, b_cell: Cell, obscuring_cells_set: Iterable[Cell], visibility_mode: str = "single_ray") -> bool:
    report = visibility_report(a_cell, b_cell, obscuring_cells_set=obscuring_cells_set, visibility_mode=visibility_mode)
    return bool(report["obscured"])


def _build_ray_report(crossed: list[Cell], opaque: set[Cell], obscuring: set[Cell]) -> dict:
    middle_cells = crossed[1:-1] if len(crossed) >= 2 else []
    blocked_by = next((cell for cell in middle_cells if cell in opaque), None)
    obscured = any(cell in obscuring for cell in middle_cells)
    return {
        "crossed_cells": crossed,
        "blocked_by": blocked_by,
        "los": blocked_by is None,
        "obscured": bool(obscured),
    }


def visibility_report(
    a_cell: Cell,
    b_cell: Cell,
    opaque_cells_set: Iterable[Cell] | None = None,
    obscuring_cells_set: Iterable[Cell] | None = None,
    visibility_mode: str = "single_ray",
) -> dict:
    mode = _normalize_mode(visibility_mode)
    opaque = set((int(x), int(y)) for x, y in (opaque_cells_set or []))
    obscuring = set((int(x), int(y)) for x, y in (obscuring_cells_set or []))

    a_samples = get_cell_sample_points(a_cell, mode=mode)
    b_samples = get_cell_sample_points(b_cell, mode=mode)

    rays: list[dict] = []
    for i in range(min(len(a_samples), len(b_samples))):
        crossed = raytrace(a_samples[i], b_samples[i])
        ray_report = _build_ray_report(crossed, opaque, obscuring)
        ray_report["ray_index"] = i
        rays.append(ray_report)

    if not rays:
        rays = [{"ray_index": 0, "crossed_cells": [a_cell, b_cell], "blocked_by": None, "los": True, "obscured": False}]

    los_any = any(ray["los"] for ray in rays)
    unblocked_rays = [ray for ray in rays if ray["los"]]
    obscured_any = any(ray["obscured"] for ray in unblocked_rays)
    fully_visible = los_any and all((not ray["obscured"]) for ray in unblocked_rays) and len(unblocked_rays) == len(rays)
    partially_visible = los_any and (not fully_visible)

    primary_ray = next((ray for ray in rays if ray["los"]), rays[0])
    blocked_by = None if los_any else next((ray["blocked_by"] for ray in rays if ray["blocked_by"] is not None), None)

    return {
        "los": bool(los_any),
        "obscured": bool(obscured_any),
        "fully_visible": bool(fully_visible),
        "partially_visible": bool(partially_visible),
        "crossed_cells": list(primary_ray["crossed_cells"]),
        "blocked_by": blocked_by,
        "visibility_mode": mode,
        "rays_total": len(rays),
        "rays_clear": len(unblocked_rays),
        "ray_reports": rays,
    }
