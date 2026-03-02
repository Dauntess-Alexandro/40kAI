"""Mission rules and adapters.

Only War-specific logic is centralized here:
- board dimensions
- objective layout
- deployment zones and deployment helper
- mission scoring logs
"""
from __future__ import annotations

import random
import os
from typing import Callable, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import reward_config as reward_cfg

from gym_mod.engine.logging_utils import format_unit
from gym_mod.engine.game_io import get_active_io

MISSION_ONLY_WAR = "only_war"
MISSION_NAME = "Only War"
ONLY_WAR_BOARD_WIDTH_INCH = 60
ONLY_WAR_BOARD_HEIGHT_INCH = 40
ONLY_WAR_CENTER_OBJECTIVE_ID = 1
ONLY_WAR_DEPLOY_DEPTH_RATIO = 0.25

# TODO(Only War): support post-deploy units ("set up after both armies deployed").
# Currently no post-deploy units supported.
MAX_BATTLE_ROUNDS = 10
START_SCORING_ROUND = reward_cfg.VP_START_SCORING_ROUND
VP_CAP_PER_COMMAND = reward_cfg.VP_CAP_PER_COMMAND

TerrainFeature = dict

_TERRAIN_SPRITE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "viewer", "assets", "props", "terrain")
)
_BARRICADE_SPRITE_NAME = "barrels_red_warning_3x1.png"


def _terrain_sprite_candidates() -> list[str]:
    try:
        names = sorted(
            file_name
            for file_name in os.listdir(_TERRAIN_SPRITE_DIR)
            if file_name.lower().endswith(".png")
        )
        return names
    except Exception:
        return []


def _terrain_seed() -> int:
    raw = str(os.getenv("TERRAIN_SEED", "1040") or "1040").strip()
    try:
        return int(raw)
    except ValueError:
        return 1040


def _make_barricade_cells(anchor_row: int, anchor_col: int, orientation: str) -> list[tuple[int, int]]:
    if orientation == "vertical":
        return [(anchor_row + i, anchor_col) for i in range(3)]
    return [(anchor_row, anchor_col + i) for i in range(3)]


def _make_terrain_feature(cells: list[tuple[int, int]], sprite_name: str) -> TerrainFeature:
    return {
        "kind": "barricade",
        "cells": [[int(r), int(c)] for r, c in cells],
        "tags": ["OBSTACLE", "BARRICADE"],
        "opacity": "obscuring",
        "sprite": str(sprite_name or ""),
    }


def _generate_only_war_terrain_features(b_len: int, b_hei: int, *, rng: random.Random) -> list[TerrainFeature]:
    count = 4 if rng.random() < 0.5 else 2
    pair_count = max(1, count // 2)
    center_col = int(b_hei // 2)
    depth = deploy_depth(b_hei)

    objective_cells = {(int(b_len // 2), int(b_hei // 2))}
    used_cells: set[tuple[int, int]] = set()
    features: list[TerrainFeature] = []

    candidate_rows = [max(1, b_len // 4), max(1, b_len // 2 - 2), min(b_len - 4, (3 * b_len) // 4)]
    rng.shuffle(candidate_rows)

    safe_left_min = max(depth + 1, 6)
    safe_left_max = max(safe_left_min, center_col - 5)

    rows_iter = candidate_rows[:]
    while len(rows_iter) < pair_count:
        rows_iter.append(rng.randint(1, max(1, b_len - 4)))

    for pair_idx in range(pair_count):
        row = int(max(1, min(b_len - 4, rows_iter[pair_idx])))
        orientation = "horizontal" if rng.random() < 0.5 else "vertical"

        attempt_ok = False
        for _ in range(20):
            left_col = int(rng.randint(safe_left_min, safe_left_max))
            mirror_col = int((b_hei - 1) - left_col)

            left_cells = _make_barricade_cells(row, left_col, orientation)
            right_cells = _make_barricade_cells(row, mirror_col - (2 if orientation == "horizontal" else 0), orientation)

            pair_cells = left_cells + right_cells
            if any(not _in_bounds(cell, b_len, b_hei) for cell in pair_cells):
                continue
            if any(cell in objective_cells for cell in pair_cells):
                continue
            if any(cell in used_cells for cell in pair_cells):
                continue
            if any(is_in_deploy_zone("model", cell, b_len, b_hei) or is_in_deploy_zone("enemy", cell, b_len, b_hei) for cell in pair_cells):
                continue

            features.append(_make_terrain_feature(left_cells, _BARRICADE_SPRITE_NAME))
            features.append(_make_terrain_feature(right_cells, _BARRICADE_SPRITE_NAME))
            used_cells.update(pair_cells)
            attempt_ok = True
            break

        if not attempt_ok:
            continue

    return features


def only_war_terrain_features(b_len: int, b_hei: int) -> list[TerrainFeature]:
    rng = random.Random(_terrain_seed() + int(b_len) * 1000 + int(b_hei))
    return _generate_only_war_terrain_features(int(b_len), int(b_hei), rng=rng)


def terrain_cells_from_features(terrain_features: Iterable[dict] | None) -> set[tuple[int, int]]:
    cells: set[tuple[int, int]] = set()
    for feature in (terrain_features or []):
        if not isinstance(feature, dict):
            continue
        for cell in (feature.get("cells") or []):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            cells.add((int(cell[0]), int(cell[1])))
    return cells


def normalize_mission_name(value: str | None) -> str:
    raw = (value or MISSION_ONLY_WAR).strip().lower().replace("-", "_").replace(" ", "_")
    if raw in {"only_war", "onlywar", "only"}:
        return MISSION_ONLY_WAR
    return MISSION_ONLY_WAR


def mission_display_name(value: str | None) -> str:
    mission = normalize_mission_name(value)
    if mission == MISSION_ONLY_WAR:
        return MISSION_NAME
    return MISSION_NAME


def board_dims_for_mission(value: str | None) -> Tuple[int, int]:
    """Returns env grid dims as (rows=b_len, cols=b_hei)."""
    mission = normalize_mission_name(value)
    if mission == MISSION_ONLY_WAR:
        return int(ONLY_WAR_BOARD_HEIGHT_INCH), int(ONLY_WAR_BOARD_WIDTH_INCH)
    return int(ONLY_WAR_BOARD_HEIGHT_INCH), int(ONLY_WAR_BOARD_WIDTH_INCH)


def objective_coords_for_mission(value: str | None, b_len: int, b_hei: int) -> np.ndarray:
    mission = normalize_mission_name(value)
    if mission == MISSION_ONLY_WAR:
        center_row = int(b_len // 2)
        center_col = int(b_hei // 2)
        return np.array([[center_row, center_col]])
    center_row = int(b_len // 2)
    center_col = int(b_hei // 2)
    return np.array([[center_row, center_col]])


def apply_mission_layout(env, mission_name: str | None = None) -> None:
    """Apply selected mission board/objectives on env (backward-compatible)."""
    mission = normalize_mission_name(mission_name)
    b_len, b_hei = board_dims_for_mission(mission)
    env.b_len = b_len
    env.b_hei = b_hei
    env.board = np.zeros((env.b_len, env.b_hei))
    env.coordsOfOM = objective_coords_for_mission(mission, env.b_len, env.b_hei)
    env.model_obj_oc = np.zeros(len(env.coordsOfOM), dtype=int)
    env.enemy_obj_oc = np.zeros(len(env.coordsOfOM), dtype=int)
    env._objective_hold_streaks = [0] * len(env.coordsOfOM)
    env.mission_name = mission_display_name(mission)
    env.terrain_features = only_war_terrain_features(env.b_len, env.b_hei)
    io = get_active_io()
    sprite_exists = (_TERRAIN_SPRITE_DIR and os.path.exists(os.path.join(_TERRAIN_SPRITE_DIR, _BARRICADE_SPRITE_NAME)))
    io.log(
        f"[MISSION][TERRAIN] kind=barricade sprite={_BARRICADE_SPRITE_NAME} "
        f"count={len(env.terrain_features)} exists={sprite_exists}"
    )


def deploy_depth(board_width: int) -> int:
    return max(1, int(board_width * ONLY_WAR_DEPLOY_DEPTH_RATIO))


def _in_bounds(coord: Sequence[int], b_len: int, b_hei: int) -> bool:
    row, col = int(coord[0]), int(coord[1])
    return 0 <= row < b_len and 0 <= col < b_hei


def is_in_deploy_zone(side: str, coord: Sequence[int], b_len: int, b_hei: int) -> bool:
    """Coordinates are [row, col], deployment checks X=col (left/right)."""
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


def _coord_to_flat(coord: Sequence[int], b_hei: int) -> int:
    return int(coord[0]) * int(b_hei) + int(coord[1])


def _flat_to_coord(flat_idx: int, b_len: int, b_hei: int) -> Tuple[int, int]:
    total = max(1, int(b_len) * int(b_hei))
    idx = int(flat_idx) % total
    row = idx // int(b_hei)
    col = idx % int(b_hei)
    return row, col


def _valid_deploy_cells(
    side: str,
    b_len: int,
    b_hei: int,
    occupied: Iterable[Tuple[int, int]],
    *,
    model_offsets: Iterable[Tuple[int, int]] | None = None,
    occupied_model_cells: Iterable[Tuple[int, int]] | None = None,
    terrain_cells: Iterable[Tuple[int, int]] | None = None,
) -> List[Tuple[int, int]]:
    valid: List[Tuple[int, int]] = []
    for row, col in _zone_coords(side, b_len, b_hei):
        ok, _ = validate_deploy_coord(
            side,
            (row, col),
            b_len,
            b_hei,
            occupied,
            model_offsets=model_offsets,
            occupied_model_cells=occupied_model_cells,
            terrain_cells=terrain_cells,
        )
        if ok:
            valid.append((row, col))
    return valid


def _unit_cells_from_anchor(anchor: Sequence[int], offsets: Iterable[Tuple[int, int]] | None) -> List[Tuple[int, int]]:
    row = int(anchor[0])
    col = int(anchor[1])
    data = list(offsets or [(0, 0)])
    return [(row + int(dr), col + int(dc)) for dr, dc in data]


def _deployment_global_score(
    side: str,
    b_len: int,
    b_hei: int,
    placed_side_units: Sequence[dict],
    *,
    cfg: dict,
) -> Tuple[float, dict]:
    if not placed_side_units:
        return 0.0, {"forward": 0.0, "spread": 0.0, "edge": 0.0, "cover": 0.0}

    units_cells: List[List[Tuple[int, int]]] = []
    centroids: List[Tuple[float, float]] = []
    for item in placed_side_units:
        anchor = item.get("anchor", (0, 0))
        offsets = item.get("offsets", [(0, 0)])
        cells = _unit_cells_from_anchor(anchor, offsets)
        if not cells:
            continue
        units_cells.append(cells)
        avg_row = sum(r for r, _ in cells) / len(cells)
        avg_col = sum(c for _, c in cells) / len(cells)
        centroids.append((avg_row, avg_col))

    if not units_cells:
        return 0.0, {"forward": 0.0, "spread": 0.0, "edge": 0.0, "cover": 0.0}

    denom_col = max(1.0, float(b_hei - 1))
    if side == "enemy":
        forward_vals = [max(0.0, min(1.0, (denom_col - c) / denom_col)) for _, c in centroids]
    else:
        forward_vals = [max(0.0, min(1.0, c / denom_col)) for _, c in centroids]
    forward_score = float(sum(forward_vals) / max(1, len(forward_vals)))

    spread_target = max(1.0, float(os.getenv("DEPLOYMENT_RL_SPREAD_TARGET", str(getattr(reward_cfg, "DEPLOYMENT_RL_SPREAD_TARGET", 6.0))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_SPREAD_TARGET", 6.0))))
    if len(centroids) <= 1:
        spread_score = 1.0
    else:
        deficits: List[float] = []
        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                dist = abs(float(centroids[i][0]) - float(centroids[j][0]))
                deficits.append(max(0.0, 1.0 - min(1.0, dist / spread_target)))
        spread_score = max(0.0, 1.0 - (sum(deficits) / max(1, len(deficits))))

    edge_margin_thr = max(0.5, float(os.getenv("DEPLOYMENT_RL_EDGE_MARGIN_TARGET", str(getattr(reward_cfg, "DEPLOYMENT_RL_EDGE_MARGIN_TARGET", 2.0))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_EDGE_MARGIN_TARGET", 2.0))))
    edge_vals: List[float] = []
    for cells in units_cells:
        min_margin = min(
            min(r, c, max(0, b_len - 1 - r), max(0, b_hei - 1 - c))
            for r, c in cells
        )
        edge_vals.append(max(0.0, min(1.0, float(min_margin) / edge_margin_thr)))
    edge_score = float(sum(edge_vals) / max(1, len(edge_vals)))

    # Placeholder for terrain-aware cover readiness. TODO: use actual terrain/LOS data when available.
    cover_score = 0.0
    # TODO: formation_flexibility component (space for first move / congestion) can be added here.

    fw = float(cfg.get("forward_w", 1.0))
    sw = float(cfg.get("spread_w", 0.6))
    ew = float(cfg.get("edge_w", 0.2))
    cw = float(cfg.get("cover_w", 0.0))
    weight_sum = max(1e-9, fw + sw + ew + cw)
    score = (fw * forward_score + sw * spread_score + ew * edge_score + cw * cover_score) / weight_sum
    return float(score), {
        "forward": float(forward_score),
        "spread": float(spread_score),
        "edge": float(edge_score),
        "cover": float(cover_score),
    }


def _choose_rl_deploy_coord(
    side: str,
    b_len: int,
    b_hei: int,
    occupied: Iterable[Tuple[int, int]],
    *,
    model_offsets: Iterable[Tuple[int, int]] | None = None,
    occupied_model_cells: Iterable[Tuple[int, int]] | None = None,
    placed_side_units: Sequence[dict] | None = None,
    terrain_cells: Iterable[Tuple[int, int]] | None = None,
    rng: random.Random | None = None,
    log_fn: Optional[callable] = None,
    unit_label: str = "",
) -> Tuple[Tuple[int, int], dict]:
    valid_cells = _valid_deploy_cells(
        side,
        b_len,
        b_hei,
        occupied,
        model_offsets=model_offsets,
        occupied_model_cells=occupied_model_cells,
        terrain_cells=terrain_cells,
    )
    if not valid_cells:
        raise RuntimeError(f"No valid deployment cells for rl_phase side={side}")

    policy_rng = rng if rng is not None else random
    max_attempts = max(1, int(os.getenv("DEPLOYMENT_RL_MAX_ATTEMPTS", "20") or "20"))
    invalid_penalty = float(os.getenv("DEPLOYMENT_RL_INVALID_PENALTY", str(getattr(reward_cfg, "DEPLOYMENT_RL_INVALID_PENALTY", 0.0))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_INVALID_PENALTY", 0.0)))
    valid_reward = float(os.getenv("DEPLOYMENT_RL_VALID_REWARD", str(getattr(reward_cfg, "DEPLOYMENT_RL_VALID_REWARD", 0.0))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_VALID_REWARD", 0.0)))
    score_scale = float(os.getenv("DEPLOYMENT_RL_SCORE_SCALE", str(getattr(reward_cfg, "DEPLOYMENT_RL_SCORE_SCALE", 0.05))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_SCORE_SCALE", 0.05)))
    forward_w = float(os.getenv("DEPLOYMENT_RL_FORWARD_W", str(getattr(reward_cfg, "DEPLOYMENT_RL_FORWARD_W", 1.0))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_FORWARD_W", 1.0)))
    spread_w = float(os.getenv("DEPLOYMENT_RL_SPREAD_W", str(getattr(reward_cfg, "DEPLOYMENT_RL_SPREAD_W", 0.6))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_SPREAD_W", 0.6)))
    edge_w = float(os.getenv("DEPLOYMENT_RL_EDGE_W", str(getattr(reward_cfg, "DEPLOYMENT_RL_EDGE_W", 0.2))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_EDGE_W", 0.2)))
    cover_w = float(os.getenv("DEPLOYMENT_RL_COVER_W", str(getattr(reward_cfg, "DEPLOYMENT_RL_COVER_W", 0.0))) or str(getattr(reward_cfg, "DEPLOYMENT_RL_COVER_W", 0.0)))
    # Stage-1 safety: RL deploy samples only from currently valid cells.
    # Это убирает массовые invalid-попытки и даёт стабильный деплой без смены правил миссии.
    total_cells = max(1, len(valid_cells))

    stats = {
        "mode": "rl_phase",
        "attempts": 0,
        "invalid": 0,
        "fallback": 0,
        "reward": 0.0,
        "selected_flat": None,
        "selected_coord": None,
        "selected_reason": "",
        "deploy_reward_delta": 0.0,
        "score_before": 0.0,
        "score_after": 0.0,
        "forward_score": 0.0,
        "spread_score": 0.0,
        "edge_score": 0.0,
        "cover_score": 0.0,
    }

    score_cfg = {
        "scale": score_scale,
        "forward_w": forward_w,
        "spread_w": spread_w,
        "edge_w": edge_w,
        "cover_w": cover_w,
    }
    if log_fn is not None:
        log_fn(
            "[DEPLOY][RL] score_config "
            f"scale={score_scale:.3f} w_forward={forward_w:.3f} w_spread={spread_w:.3f} "
            f"w_edge={edge_w:.3f} w_cover={cover_w:.3f}"
        )

    for _ in range(max_attempts):
        valid_idx = int(policy_rng.randrange(total_cells))
        coord = valid_cells[valid_idx]
        flat = _coord_to_flat(coord, b_hei)
        stats["attempts"] += 1
        ok, reason = validate_deploy_coord(
            side,
            coord,
            b_len,
            b_hei,
            occupied,
            model_offsets=model_offsets,
            occupied_model_cells=occupied_model_cells,
            terrain_cells=terrain_cells,
        )
        if ok:
            score_before, before_parts = _deployment_global_score(
                side,
                b_len,
                b_hei,
                placed_side_units or [],
                cfg=score_cfg,
            )
            score_after, after_parts = _deployment_global_score(
                side,
                b_len,
                b_hei,
                list(placed_side_units or []) + [{"anchor": coord, "offsets": list(model_offsets or [(0, 0)])}],
                cfg=score_cfg,
            )
            deploy_reward_delta = score_scale * (score_after - score_before)
            stats["reward"] += valid_reward + deploy_reward_delta
            stats["selected_flat"] = flat
            stats["selected_coord"] = coord
            stats["selected_reason"] = "policy"
            stats["deploy_reward_delta"] = float(deploy_reward_delta)
            stats["score_before"] = float(score_before)
            stats["score_after"] = float(score_after)
            stats["forward_score"] = float(after_parts.get("forward", 0.0))
            stats["spread_score"] = float(after_parts.get("spread", 0.0))
            stats["edge_score"] = float(after_parts.get("edge", 0.0))
            stats["cover_score"] = float(after_parts.get("cover", 0.0))
            if log_fn is not None:
                log_fn(
                    f"[DEPLOY][RL] accepted {unit_label or side}: flat={flat}, coord=({coord[0]},{coord[1]}), "
                    f"attempt={stats['attempts']}, reward={stats['reward']:+.3f}, "
                    f"score_before={score_before:.3f}, score_after={score_after:.3f}, "
                    f"reward_delta={deploy_reward_delta:+.3f}, "
                    f"forward={after_parts.get('forward', 0.0):.3f}, spread={after_parts.get('spread', 0.0):.3f}, "
                    f"edge={after_parts.get('edge', 0.0):.3f}, cover={after_parts.get('cover', 0.0):.3f}"
                )
            return coord, stats
        stats["invalid"] += 1
        stats["reward"] -= invalid_penalty
        if log_fn is not None:
            log_fn(
                f"[DEPLOY][RL] invalid {unit_label or side}: flat={flat}, coord=({coord[0]},{coord[1]}), "
                f"reason={reason}, penalty=-{invalid_penalty:.3f}"
            )

    fallback = (policy_rng.choice(valid_cells) if hasattr(policy_rng, "choice") else random.choice(valid_cells))
    stats["fallback"] = 1
    stats["reward"] += valid_reward
    stats["selected_flat"] = _coord_to_flat(fallback, b_hei)
    stats["selected_coord"] = fallback
    stats["selected_reason"] = "fallback_valid"
    if log_fn is not None:
        log_fn(
            f"[DEPLOY][RL] fallback {unit_label or side}: coord=({fallback[0]},{fallback[1]}), "
            f"attempts={stats['attempts']}, invalid={stats['invalid']}, reward={stats['reward']:+.3f}"
        )
    return fallback, stats


def get_random_free_deploy_coord(
    side: str,
    b_len: int,
    b_hei: int,
    occupied: Iterable[Tuple[int, int]],
    *,
    rng: random.Random | None = None,
    strategy: str = "random",
    unit_idx: int | None = None,
    total_units: int | None = None,
    log_fn: Optional[callable] = None,
) -> Tuple[int, int]:
    occupied_set = set((int(row), int(col)) for row, col in occupied)
    choices = [c for c in _zone_coords(side, b_len, b_hei) if c not in occupied_set]
    if not choices:
        raise RuntimeError(f"No free deployment space for side={side}")

    picker = rng.choice if rng is not None else random.choice
    if strategy != "template_jitter":
        return picker(choices)

    x_min, x_max = _zone_bounds_for_side(side, b_hei)
    x_center = int((x_min + x_max) // 2)

    if total_units is None or total_units <= 0:
        target_row = b_len // 2
    else:
        idx = 0 if unit_idx is None else max(0, int(unit_idx))
        span = max(1, b_len - 1)
        target_row = int(round((idx + 1) * span / (int(total_units) + 1)))

    jitter_rows = [0, -1, 1, -2, 2, -3, 3]
    jitter_cols = [0, -1, 1, -2, 2]
    template_candidates: list[Tuple[int, int]] = []
    for dr in jitter_rows:
        for dc in jitter_cols:
            cand = (int(target_row + dr), int(x_center + dc))
            if cand in template_candidates:
                continue
            if cand in occupied_set:
                continue
            if not _in_bounds(cand, b_len, b_hei):
                continue
            if not is_in_deploy_zone(side, cand, b_len, b_hei):
                continue
            template_candidates.append(cand)

    if template_candidates:
        return picker(template_candidates)

    if log_fn is not None:
        log_fn(
            f"[DEPLOY][AUTO] strategy=template_jitter fallback=random; "
            f"reason=no_valid_template_candidates side={side} unit_idx={unit_idx}"
        )
    return picker(choices)


def validate_deploy_coord(
    side: str,
    coord: Sequence[int],
    b_len: int,
    b_hei: int,
    occupied: Iterable[Tuple[int, int]],
    *,
    model_offsets: Iterable[Tuple[int, int]] | None = None,
    occupied_model_cells: Iterable[Tuple[int, int]] | None = None,
    terrain_cells: Iterable[Tuple[int, int]] | None = None,
) -> Tuple[bool, str]:
    if not _in_bounds(coord, b_len, b_hei):
        return False, "out_of_bounds"
    if not is_in_deploy_zone(side, coord, b_len, b_hei):
        return False, "outside_deploy_zone"
    key = (int(coord[0]), int(coord[1]))
    occupied_set = set((int(r), int(c)) for r, c in occupied)
    terrain_set = set((int(r), int(c)) for r, c in (terrain_cells or []))
    if key in occupied_set:
        return False, "occupied"
    if key in terrain_set:
        return False, "terrain_no_deploy"

    offsets = list(model_offsets or [(0, 0)])
    model_occupied_set = set((int(r), int(c)) for r, c in (occupied_model_cells or []))
    for dr, dc in offsets:
        m_row = int(coord[0]) + int(dr)
        m_col = int(coord[1]) + int(dc)
        m_coord = (m_row, m_col)
        if not _in_bounds(m_coord, b_len, b_hei):
            return False, "out_of_bounds"
        if not is_in_deploy_zone(side, m_coord, b_len, b_hei):
            return False, "outside_deploy_zone"
        if m_coord in model_occupied_set:
            return False, "occupied"
        if m_coord in terrain_set:
            return False, "terrain_no_deploy"

    return True, "ok"


def _resolve_deploy_rng(seed: int | None) -> random.Random | None:
    if seed is None:
        return None
    return random.Random(int(seed))


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


def _collect_model_offsets(unit) -> List[Tuple[int, int]]:
    def _fallback_offsets_from_unit_size() -> List[Tuple[int, int]]:
        count = 1
        unit_data = getattr(unit, "unit_data", None)
        if isinstance(unit_data, dict):
            try:
                count = max(1, int(unit_data.get("#OfModels", 1)))
            except (TypeError, ValueError):
                count = 1
        # Keep formation offsets in sync with warhamEnv._formation_offsets,
        # so deploy preview matches final formation after env.reset().
        formation_offsets: List[Tuple[int, int]] = [
            (0, 0),
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
            (0, 2), (0, -2), (2, 0), (-2, 0),
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1),
        ]
        return formation_offsets[:count]

    if not hasattr(unit, "models"):
        return _fallback_offsets_from_unit_size()
    try:
        models = unit.models()
    except Exception:
        return _fallback_offsets_from_unit_size()
    if not isinstance(models, list) or not models:
        return _fallback_offsets_from_unit_size()
    anchor = getattr(unit, "unit_coords", [0, 0])
    base_row = int(anchor[0])
    base_col = int(anchor[1])
    result: List[Tuple[int, int]] = []
    for model in models:
        if not isinstance(model, dict) or not model.get("alive", True):
            continue
        coords = model.get("coords", [base_row, base_col, 0])
        if len(coords) < 2:
            continue
        dr = int(coords[0]) - base_row
        dc = int(coords[1]) - base_col
        candidate = (dr, dc)
        if candidate not in result:
            result.append(candidate)
    # If unit internals still keep all models at anchor (PR1-style),
    # use battle formation offsets by model count instead of a single dot.
    if not result or len(result) == 1:
        return _fallback_offsets_from_unit_size()
    return result


def _add_unit_model_cells(occupied_model_cells: set[Tuple[int, int]], anchor: Tuple[int, int], offsets: Iterable[Tuple[int, int]]) -> None:
    for dr, dc in offsets:
        occupied_model_cells.add((int(anchor[0]) + int(dr), int(anchor[1]) + int(dc)))


def _facing_for_deploy_zone(zone_side: str) -> str:
    return "right" if str(zone_side) == "model" else "left"


def deploy_only_war(
    model_units: Sequence,
    enemy_units: Sequence,
    b_len: int,
    b_hei: int,
    attacker_side: str,
    log_fn: Optional[callable] = None,
    deployment_seed: int | None = None,
    deployment_strategy: str | None = None,
    deployment_mode: str | None = None,
) -> None:
    if attacker_side not in ("model", "enemy"):
        raise ValueError(f"Unknown attacker side: {attacker_side}")

    defender_side = "enemy" if attacker_side == "model" else "model"
    if deployment_seed is None:
        raw_seed = os.getenv("DEPLOYMENT_SEED", "").strip()
        if raw_seed != "":
            try:
                deployment_seed = int(raw_seed)
            except ValueError:
                if log_fn is not None:
                    log_fn(
                        f"[DEPLOY][AUTO] invalid DEPLOYMENT_SEED='{raw_seed}'; "
                        "Где: mission.deploy_only_war. Что делать дальше: укажите целое число."
                    )
                deployment_seed = None

    strategy_raw = (deployment_strategy or os.getenv("DEPLOYMENT_STRATEGY", "template_jitter")).strip().lower()
    strategy = strategy_raw if strategy_raw in {"random", "template_jitter"} else "template_jitter"
    mode_raw = (deployment_mode or os.getenv("DEPLOYMENT_MODE", "auto")).strip().lower()
    mode = mode_raw if mode_raw in {"auto", "manual_player", "rl_phase"} else "auto"
    rng = _resolve_deploy_rng(deployment_seed)
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
        log_fn(
            f"[DEPLOY][AUTO] mode={mode} strategy={strategy} seed={deployment_seed if deployment_seed is not None else 'none'}"
        )
        log_fn(f"[DEPLOY] Order: {attacker_side} first, alternating")

    occupied: set[Tuple[int, int]] = set()
    occupied_model_cells: set[Tuple[int, int]] = set()
    terrain_cells = terrain_cells_from_features(only_war_terrain_features(b_len, b_hei))
    side_counts = {
        "model": len(model_units),
        "enemy": len(enemy_units),
    }
    manual_total = side_counts.get("enemy", 0)
    manual_done = 0
    rl_summary = {
        "attempts": 0,
        "invalid": 0,
        "fallback": 0,
        "reward": 0.0,
        "units": 0,
        "total_deploy_reward": 0.0,
        "forward_sum": 0.0,
        "spread_sum": 0.0,
        "edge_sum": 0.0,
        "cover_sum": 0.0,
    }
    placed_by_side: dict[str, list[dict]] = {"model": [], "enemy": []}

    def _place_unit(unit, side: str, unit_idx: int):
        nonlocal manual_done
        zone_side = side_to_zone[side]
        unit_model_offsets = _collect_model_offsets(unit)
        coord = None
        unit_id = (11 + unit_idx) if side == "enemy" else (21 + unit_idx)
        unit_label = format_unit(unit_id, getattr(unit, "unit_data", None), include_instance_id=False)
        unit_name = ""
        if isinstance(getattr(unit, "unit_data", None), dict):
            unit_name = str(getattr(unit, "unit_data", {}).get("Name") or "")
        use_manual = (mode == "manual_player" and side == "enemy") or (
            mode == "rl_phase"
            and side == "enemy"
            and os.getenv("DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE", "1").strip().lower() not in {"0", "false", "no"}
        )
        use_rl_model = mode == "rl_phase" and side == "model"
        if use_manual:
            io = get_active_io()
            if isinstance(getattr(unit, "unit_data", None), dict):
                unit_name = str(getattr(unit, "unit_data", {}).get("Name") or "")
            x_min, x_max = _zone_bounds_for_side(zone_side, b_hei)
            y_min, y_max = 0, b_len - 1
            next_label = None
            if unit_idx + 1 < len(enemy_units):
                next_unit = enemy_units[unit_idx + 1]
                next_label = format_unit(11 + unit_idx + 1, getattr(next_unit, "unit_data", None), include_instance_id=False)
            while True:
                current_index = manual_done + 1
                prompt = (
                    f"[DEPLOY][MANUAL] Расставьте юнита: {unit_label} [{current_index}/{manual_total}]. "
                    f"Осталось расставить: {max(0, manual_total - manual_done)}. "
                    f"Зона: X={x_min}..{x_max}, Y={y_min}..{y_max}."
                )
                if next_label is not None:
                    prompt += f" Следом: {next_label} [{current_index + 1}/{manual_total}]"
                try:
                    response = io.request_deploy_coord(
                        prompt,
                        x_min=x_min,
                        x_max=x_max,
                        y_min=y_min,
                        y_max=y_max,
                        meta={
                            "deployment_mode": mode,
                            "deploy_side": side,
                            "deploy_unit_id": unit_id,
                            "deploy_unit_label": unit_label,
                            "deploy_unit_name": unit_name,
                            "deploy_index": current_index,
                            "deploy_total": manual_total,
                            "deploy_remaining": max(0, manual_total - manual_done),
                            "deploy_next_label": next_label,
                            "deploy_zone_side": zone_side,
                            "deploy_b_len": b_len,
                            "deploy_b_hei": b_hei,
                            "occupied": [[int(r), int(c)] for r, c in sorted(occupied)],
                            "occupied_model_cells": [[int(r), int(c)] for r, c in sorted(occupied_model_cells)],
                            "terrain_cells": [[int(r), int(c)] for r, c in sorted(terrain_cells)],
                            "model_offsets": [[int(dr), int(dc)] for dr, dc in unit_model_offsets],
                        },
                    )
                except EOFError:
                    response = None
                    if log_fn is not None:
                        log_fn(
                            f"[DEPLOY][MANUAL] {unit_label}: stdin EOF при ручном деплое. "
                            "Где: mission.deploy_only_war. Что делать дальше: auto-placement для этого юнита "
                            "или переключите DEPLOYMENT_MODE на auto/rl_phase для неинтерактивного запуска."
                        )
                if response is None:
                    if log_fn is not None:
                        log_fn(
                            f"[DEPLOY][MANUAL] {unit_label}: ручной ввод отменён. "
                            "Где: mission.deploy_only_war. Что делать дальше: auto-placement для этого юнита."
                        )
                    break
                x = int(response.get("x", -99999))
                y = int(response.get("y", -99999))
                coord_candidate = (y, x)
                ok, reason = validate_deploy_coord(
                    zone_side,
                    coord_candidate,
                    b_len,
                    b_hei,
                    occupied,
                    model_offsets=unit_model_offsets,
                    occupied_model_cells=occupied_model_cells,
                    terrain_cells=terrain_cells,
                )
                if ok:
                    coord = coord_candidate
                    if log_fn is not None:
                        log_fn(f"[DEPLOY][MANUAL] accepted {unit_label} -> ({coord[0]},{coord[1]})")
                    break
                if log_fn is not None:
                    log_fn(
                        f"[DEPLOY][MANUAL] invalid {unit_label}: reason={reason}, x={x}, y={y}. "
                        "Где: mission.deploy_only_war. Что делать дальше: выберите другую клетку в зоне деплоя."
                    )

        if coord is None and use_rl_model:
            coord, rl_stats = _choose_rl_deploy_coord(
                zone_side,
                b_len,
                b_hei,
                occupied,
                model_offsets=unit_model_offsets,
                occupied_model_cells=occupied_model_cells,
                terrain_cells=terrain_cells,
                placed_side_units=placed_by_side.get(side, []),
                rng=rng,
                log_fn=log_fn,
                unit_label=unit_label,
            )
            rl_summary["attempts"] += int(rl_stats.get("attempts", 0))
            rl_summary["invalid"] += int(rl_stats.get("invalid", 0))
            rl_summary["fallback"] += int(rl_stats.get("fallback", 0))
            rl_summary["reward"] += float(rl_stats.get("reward", 0.0))
            rl_summary["units"] += 1
            rl_summary["total_deploy_reward"] += float(rl_stats.get("deploy_reward_delta", 0.0))
            rl_summary["forward_sum"] += float(rl_stats.get("forward_score", 0.0))
            rl_summary["spread_sum"] += float(rl_stats.get("spread_score", 0.0))
            rl_summary["edge_sum"] += float(rl_stats.get("edge_score", 0.0))
            rl_summary["cover_sum"] += float(rl_stats.get("cover_score", 0.0))

        if coord is None:
            coord = get_random_free_deploy_coord(
                zone_side,
                b_len,
                b_hei,
                occupied,
                rng=rng,
                strategy=strategy,
                unit_idx=unit_idx,
                total_units=side_counts.get(side, 0),
                log_fn=log_fn,
            )
        ok, reason = validate_deploy_coord(
            zone_side,
            coord,
            b_len,
            b_hei,
            occupied,
            model_offsets=unit_model_offsets,
            occupied_model_cells=occupied_model_cells,
            terrain_cells=terrain_cells,
        )
        if not ok:
            raise RuntimeError(
                f"Deployment validation failed: side={side}, zone_side={zone_side}, coord={coord}, reason={reason}"
            )
        if hasattr(unit, "set_anchor"):
            unit.set_anchor(coord[0], coord[1])
        else:
            unit.unit_coords = [coord[0], coord[1]]
        facing = _facing_for_deploy_zone(zone_side)
        try:
            setattr(unit, "facing", facing)
        except Exception:
            pass
        if isinstance(getattr(unit, "unit_data", None), dict):
            unit.unit_data["Facing"] = facing
        occupied.add(coord)
        _add_unit_model_cells(occupied_model_cells, coord, unit_model_offsets)
        placed_by_side.setdefault(side, []).append({"anchor": coord, "offsets": list(unit_model_offsets)})
        if side == "enemy":
            manual_done += 1
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

    if mode == "rl_phase" and log_fn is not None:
        rl_units = max(1, int(rl_summary["units"]))
        avg_forward = float(rl_summary["forward_sum"]) / rl_units
        avg_spread = float(rl_summary["spread_sum"]) / rl_units
        avg_edge = float(rl_summary["edge_sum"]) / rl_units
        avg_cover = float(rl_summary["cover_sum"]) / rl_units
        rl_summary["avg_forward"] = avg_forward
        rl_summary["avg_spread"] = avg_spread
        rl_summary["avg_edge"] = avg_edge
        rl_summary["avg_cover"] = avg_cover
        log_fn(
            "[DEPLOY][RL][SUMMARY] "
            f"units={rl_summary['units']} attempts={rl_summary['attempts']} invalid={rl_summary['invalid']} "
            f"fallback={rl_summary['fallback']} reward={rl_summary['reward']:+.3f} "
            f"total_deploy_reward={rl_summary['total_deploy_reward']:+.3f} "
            f"avg_forward={avg_forward:.3f} avg_spread={avg_spread:.3f} avg_edge={avg_edge:.3f} avg_cover={avg_cover:.3f}"
        )
    return rl_summary if mode == "rl_phase" else None


def post_deploy_setup(log_fn: Optional[callable] = None) -> None:
    if log_fn is not None:
        log_fn("[MISSION Only War] Post-deploy: currently no post-deploy units supported")


def deploy_for_mission(
    mission_name: str | None,
    model_units: Sequence,
    enemy_units: Sequence,
    b_len: int,
    b_hei: int,
    attacker_side: str,
    log_fn: Optional[callable] = None,
    deployment_seed: int | None = None,
    deployment_strategy: str | None = None,
    deployment_mode: str | None = None,
) -> None:
    mission = normalize_mission_name(mission_name)
    if mission == MISSION_ONLY_WAR:
        return deploy_only_war(
            model_units,
            enemy_units,
            b_len,
            b_hei,
            attacker_side,
            log_fn=log_fn,
            deployment_seed=deployment_seed,
            deployment_strategy=deployment_strategy,
            deployment_mode=deployment_mode,
        )
    return deploy_only_war(
        model_units,
        enemy_units,
        b_len,
        b_hei,
        attacker_side,
        log_fn=log_fn,
        deployment_seed=deployment_seed,
        deployment_strategy=deployment_strategy,
        deployment_mode=deployment_mode,
    )


def controlled_objectives(env, side: str) -> Tuple[int, List[int]]:
    if side not in ("model", "enemy"):
        raise ValueError(f"Unknown side: {side}")

    model_totals = getattr(env, "model_obj_oc", None)
    enemy_totals = getattr(env, "enemy_obj_oc", None)
    if model_totals is None or enemy_totals is None:
        raise AttributeError("Objective OC totals not available on env")

    controlled = []
    for idx in range(len(model_totals)):
        model_oc = int(model_totals[idx])
        enemy_oc = int(enemy_totals[idx])
        if side == "model" and model_oc > enemy_oc:
            controlled.append(idx)
        elif side == "enemy" and enemy_oc > model_oc:
            controlled.append(idx)

    return len(controlled), controlled


def score_end_of_command_phase(env, side: str, log_fn: Callable[[str], None] | None = None) -> int:
    if hasattr(env, "refresh_objective_control"):
        env.refresh_objective_control()

    count_controlled, indices = controlled_objectives(env, side)

    if env.battle_round < START_SCORING_ROUND:
        gained = 0
    else:
        gained = min(VP_CAP_PER_COMMAND, count_controlled)

    if side == "model":
        vp_before = env.modelVP
        env.modelVP += gained
        vp_after = env.modelVP
    else:
        vp_before = env.enemyVP
        env.enemyVP += gained
        vp_after = env.enemyVP

    if log_fn is not None:
        side_label = side.upper()
        cap_note = " (cap)" if gained == VP_CAP_PER_COMMAND and count_controlled > VP_CAP_PER_COMMAND else ""
        display_indices = [idx + 1 for idx in indices]
        indices_note = f", objectives={display_indices}" if display_indices else ""
        objective_id = ONLY_WAR_CENTER_OBJECTIVE_ID
        center = env.coordsOfOM[0] if getattr(env, "coordsOfOM", None) is not None and len(env.coordsOfOM) > 0 else None

        model_oc = int(env.model_obj_oc[0]) if len(getattr(env, "model_obj_oc", [])) > 0 else 0
        enemy_oc = int(env.enemy_obj_oc[0]) if len(getattr(env, "enemy_obj_oc", [])) > 0 else 0
        controlled_side = "none"
        if model_oc > enemy_oc:
            controlled_side = "model"
        elif enemy_oc > model_oc:
            controlled_side = "enemy"

        attacker_side = getattr(env, "attacker_side", None)
        defender_side = getattr(env, "defender_side", None)
        controlled_role = controlled_side
        if controlled_side == attacker_side:
            controlled_role = "attacker"
        elif controlled_side == defender_side:
            controlled_role = "defender"

        center_note = "center=(n/a,n/a)"
        if center is not None and len(center) >= 2:
            center_note = f"center=({int(center[1])},{int(center[0])})"

        log_fn(
            f"[{side_label}] {MISSION_NAME}: end of Command phase -> "
            f"controlled={count_controlled}, gained={gained}{cap_note}, VP: {vp_before} -> {vp_after}{indices_note}; "
            f"objectives=[{objective_id}], {center_note}, controlled_by={controlled_role}"
        )

    return gained


def check_end_of_battle(env) -> Tuple[bool, str, str | None]:
    model_wiped = sum(env.unit_health) <= 0
    enemy_wiped = sum(env.enemy_health) <= 0

    if model_wiped and enemy_wiped:
        return True, "wipeout_model", None
    if model_wiped:
        return True, "wipeout_model", "enemy"
    if enemy_wiped:
        return True, "wipeout_enemy", "model"

    if env.battle_round > MAX_BATTLE_ROUNDS:
        if env.modelVP > env.enemyVP:
            winner = "model"
        elif env.enemyVP > env.modelVP:
            winner = "enemy"
        else:
            winner = None
        return True, "turn_limit", winner

    return False, "", None


def apply_end_of_battle(env, log_fn: Callable[[str], None] | None = None) -> Tuple[bool, str, str | None]:
    game_over, reason, winner = check_end_of_battle(env)
    if game_over and not env.game_over:
        env.game_over = True
        if log_fn is not None:
            if reason == "turn_limit":
                if winner is None:
                    log_fn(f"Game over: turn_limit -> draw (VP {env.modelVP}-{env.enemyVP})")
                else:
                    log_fn(
                        f"Game over: turn_limit (after BR{MAX_BATTLE_ROUNDS}) -> winner={winner} "
                        f"(VP {env.modelVP}-{env.enemyVP})"
                    )
            else:
                if winner is None:
                    log_fn(f"Game over: {reason} -> draw")
                else:
                    log_fn(f"Game over: {reason} -> winner={winner}")
    return game_over, reason, winner
