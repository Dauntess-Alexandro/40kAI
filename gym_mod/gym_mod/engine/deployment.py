"""Deployment helpers for the Only War mission."""
from __future__ import annotations

import random
from typing import Iterable, List, Optional, Sequence, Tuple

from gym_mod.engine.logging_utils import format_unit

DEPLOY_DEPTH_RATIO = 0.25


def deploy_depth(board_width: int) -> int:
    return max(1, int(board_width * DEPLOY_DEPTH_RATIO))


def _in_bounds(coord: Sequence[int], b_len: int, b_hei: int) -> bool:
    x, y = int(coord[0]), int(coord[1])
    return 0 <= x < b_len and 0 <= y < b_hei


def is_in_deploy_zone(side: str, coord: Sequence[int], b_len: int, b_hei: int) -> bool:
    """
    Check if coord is wholly within the deployment zone for the given side.
    Coordinates are treated as [row, col].
    Only War deployment is left/right, so we check X=col axis (0..b_hei-1).
    """
    if side not in ("model", "enemy"):
        raise ValueError(f"Unknown side: {side}")
    if not _in_bounds(coord, b_len, b_hei):
        return False
    x = int(coord[1])
    depth = deploy_depth(b_hei)
    if side == "enemy":
        return x >= b_hei - depth
    return x <= depth - 1


def _zone_coords(side: str, b_len: int, b_hei: int) -> List[Tuple[int, int]]:
    depth = deploy_depth(b_hei)
    coords: List[Tuple[int, int]] = []
    if side == "enemy":
        x_min = max(0, b_hei - depth)
        x_max = b_hei - 1
    else:
        x_min = 0
        x_max = max(0, depth - 1)
    for row in range(b_len):
        for col in range(x_min, x_max + 1):
            coords.append((row, col))
    return coords


def _zone_bounds_for_side(side: str, b_hei: int) -> Tuple[int, int]:
    depth = deploy_depth(b_hei)
    if side == "enemy":
        return max(0, b_hei - depth), b_hei - 1
    return 0, max(0, depth - 1)


def get_random_free_deploy_coord(
    side: str,
    b_len: int,
    b_hei: int,
    occupied: Iterable[Tuple[int, int]],
) -> Tuple[int, int]:
    occupied_set = set((int(x), int(y)) for x, y in occupied)
    choices = [c for c in _zone_coords(side, b_len, b_hei) if c not in occupied_set]
    if not choices:
        raise RuntimeError(f"No free deployment space for side={side}")
    return random.choice(choices)


def _log_deploy(log_fn: Optional[callable], side: str, unit_idx: int, coord: Tuple[int, int], unit=None):
    if log_fn is None:
        return
    unit_id = (11 + unit_idx) if side == "enemy" else (21 + unit_idx)
    unit_data = getattr(unit, "unit_data", None)
    instance_id = getattr(unit, "instance_id", None)
    unit_label = format_unit(
        unit_id,
        unit_data,
        instance_id=instance_id,
        include_instance_id=False,
    )
    log_fn(f"[DEPLOY][{side.upper()}] {unit_label} -> ({coord[0]},{coord[1]})")


def deploy_only_war(
    model_units: Sequence,
    enemy_units: Sequence,
    b_len: int,
    b_hei: int,
    attacker_side: str,
    log_fn: Optional[callable] = None,
) -> None:
    """
    Alternating deployment starting with attacker.
    Units are placed wholly within their deployment zones and on free cells.
    """
    if attacker_side not in ("model", "enemy"):
        raise ValueError(f"Unknown attacker side: {attacker_side}")

    defender_side = "enemy" if attacker_side == "model" else "model"
    attacker_zone_side = "model"
    defender_zone_side = "enemy"
    side_to_zone = {
        attacker_side: attacker_zone_side,
        defender_side: defender_zone_side,
    }
    if log_fn is not None:
        left_min_x, left_max_x = _zone_bounds_for_side(attacker_zone_side, b_hei)
        right_min_x, right_max_x = _zone_bounds_for_side(defender_zone_side, b_hei)
        log_fn(
            f"[DEPLOY][Only War] attacker={attacker_side} -> LEFT x={left_min_x}..{left_max_x}; "
            f"defender={defender_side} -> RIGHT x={right_min_x}..{right_max_x}"
        )
        log_fn(f"[DEPLOY] Order: {attacker_side} first, alternating")

    occupied: set[Tuple[int, int]] = set()

    def _place_unit(unit, side: str, unit_idx: int):
        zone_side = side_to_zone[side]
        coord = get_random_free_deploy_coord(zone_side, b_len, b_hei, occupied)
        unit.unit_coords = [coord[0], coord[1]]
        occupied.add(coord)
        _log_deploy(log_fn, side, unit_idx, coord, unit=unit)

    attacker_units = model_units if attacker_side == "model" else enemy_units
    defender_units = model_units if defender_side == "model" else enemy_units

    a_idx = 0
    d_idx = 0
    while a_idx < len(attacker_units) or d_idx < len(defender_units):
        if a_idx < len(attacker_units):
            _place_unit(attacker_units[a_idx], attacker_side, a_idx)
            a_idx += 1
        if d_idx < len(defender_units):
            _place_unit(defender_units[d_idx], defender_side, d_idx)
            d_idx += 1


def post_deploy_setup(log_fn: Optional[callable] = None) -> None:
    """Placeholder for future post-deployment units (infiltrators, etc.)."""
    # TODO: add support for "set up after both armies deployed" units.
    if log_fn is not None:
        log_fn("[MISSION Only War] Post-deploy: currently no post-deploy units supported")
