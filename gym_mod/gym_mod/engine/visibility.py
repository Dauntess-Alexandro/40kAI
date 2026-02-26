from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

Cell = Tuple[int, int]


def supercover_line_cells(a_cell: Sequence[int], b_cell: Sequence[int]) -> List[Cell]:
    """Return supercover cells between A and B, excluding endpoints."""
    x0, y0 = int(a_cell[0]), int(a_cell[1])
    x1, y1 = int(b_cell[0]), int(b_cell[1])

    cells: List[Cell] = []
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    if steps <= 1:
        return []

    for i in range(1, steps):
        t = i / steps
        fx = x0 + dx * t
        fy = y0 + dy * t
        candidates = {
            (int(fx), int(fy)),
            (int(round(fx)), int(round(fy))),
            (int(fx + 0.5), int(fy + 0.5)),
        }
        for cell in sorted(candidates):
            if cell == (x0, y0) or cell == (x1, y1):
                continue
            if cell not in cells:
                cells.append(cell)
    return cells


def has_line_of_sight(att_cell: Sequence[int], tgt_cell: Sequence[int], opaque_cells: Iterable[Cell]) -> bool:
    opaque = {(int(r), int(c)) for r, c in opaque_cells}
    for cell in supercover_line_cells(att_cell, tgt_cell):
        if cell in opaque:
            return False
    return True


def is_obscured_by_barricade(att_cell: Sequence[int], tgt_cell: Sequence[int], barricade_cells: Iterable[Cell]) -> bool:
    barr = {(int(r), int(c)) for r, c in barricade_cells}
    if not barr:
        return False
    for cell in supercover_line_cells(att_cell, tgt_cell):
        if cell in barr:
            return True
    return False
