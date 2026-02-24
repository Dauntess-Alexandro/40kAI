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
) -> Tuple[bool, str]:
    if not _in_bounds(coord, b_len, b_hei):
        return False, "out_of_bounds"
    if not is_in_deploy_zone(side, coord, b_len, b_hei):
        return False, "outside_deploy_zone"
    key = (int(coord[0]), int(coord[1]))
    occupied_set = set((int(r), int(c)) for r, c in occupied)
    if key in occupied_set:
        return False, "occupied"

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
    mode = mode_raw if mode_raw in {"auto", "manual_player"} else "auto"
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
    side_counts = {
        "model": len(model_units),
        "enemy": len(enemy_units),
    }
    manual_total = side_counts.get("enemy", 0)
    manual_done = 0

    def _place_unit(unit, side: str, unit_idx: int):
        nonlocal manual_done
        zone_side = side_to_zone[side]
        unit_model_offsets = _collect_model_offsets(unit)
        coord = None
        use_manual = mode == "manual_player" and side == "enemy"
        if use_manual:
            io = get_active_io()
            unit_id = 11 + unit_idx
            unit_label = format_unit(unit_id, getattr(unit, "unit_data", None), include_instance_id=False)
            unit_name = ""
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
                        "model_offsets": [[int(dr), int(dc)] for dr, dc in unit_model_offsets],
                    },
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
        )
        if not ok:
            raise RuntimeError(
                f"Deployment validation failed: side={side}, zone_side={zone_side}, coord={coord}, reason={reason}"
            )
        if hasattr(unit, "set_anchor"):
            unit.set_anchor(coord[0], coord[1])
        else:
            unit.unit_coords = [coord[0], coord[1]]
        occupied.add(coord)
        _add_unit_model_cells(occupied_model_cells, coord, unit_model_offsets)
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
        deploy_only_war(
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
        return
    deploy_only_war(
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
