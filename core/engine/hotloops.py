import os
from typing import Tuple

import numpy as np


def _as_bool_env(name: str, default: bool = True) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() not in {"0", "false", "off", "no"}


_NUMBA_ENABLED = False
_numba_scan_targets = None

if _as_bool_env("ENABLE_NUMBA_HOTLOOPS", default=True):
    try:
        from numba import njit  # type: ignore

        @njit(cache=True)
        def _numba_scan_targets(src_x: float, src_y: float, coords: np.ndarray, health: np.ndarray, in_attack: np.ndarray, range_sq: float) -> np.ndarray:
            n = coords.shape[0]
            out = np.empty(n, dtype=np.int64)
            count = 0
            for i in range(n):
                if health[i] <= 0:
                    continue
                if in_attack[i] != 0:
                    continue
                dx = coords[i, 0] - src_x
                dy = coords[i, 1] - src_y
                if (dx * dx + dy * dy) <= range_sq:
                    out[count] = i
                    count += 1
            return out[:count]

        _NUMBA_ENABLED = True
    except Exception:
        _numba_scan_targets = None


def scan_targets_in_range(
    src_xy: np.ndarray,
    target_coords: np.ndarray,
    target_health: np.ndarray,
    target_in_attack: np.ndarray,
    range_limit: float,
) -> Tuple[np.ndarray, bool]:
    """
    Возвращает tuple: (индексы целей в радиусе, использован_numba).
    Все входы ожидаются как numpy-массивы.
    """
    if target_coords.size == 0:
        return np.empty(0, dtype=np.int64), _NUMBA_ENABLED

    src = np.asarray(src_xy, dtype=np.float64)
    coords = np.asarray(target_coords, dtype=np.float64)
    health = np.asarray(target_health, dtype=np.float64)
    in_attack = np.asarray(target_in_attack, dtype=np.int8)

    range_sq = float(range_limit) * float(range_limit)

    if _NUMBA_ENABLED and _numba_scan_targets is not None:
        return _numba_scan_targets(float(src[0]), float(src[1]), coords, health, in_attack, range_sq), True

    dx = coords[:, 0] - float(src[0])
    dy = coords[:, 1] - float(src[1])
    mask = (health > 0) & (in_attack == 0) & ((dx * dx + dy * dy) <= range_sq)
    return np.flatnonzero(mask).astype(np.int64), False
