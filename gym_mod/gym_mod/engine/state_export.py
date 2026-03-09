import json
import os
import tempfile
import time
from datetime import datetime

from gym_mod.engine.visibility import visibility_report

from gym_mod.engine.event_bus import get_event_recorder
from gym_mod.engine.io_profiler import get_io_profiler


DEFAULT_STATE_PATH = os.path.join(os.getcwd(), "gui", "state.json")


def _safe_int(value, fallback=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _safe_float(value, fallback=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _iter_values(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    try:
        return list(value)
    except TypeError:
        return [value]


def _normalize_facing(value):
    raw = str(value or "").strip().lower()
    if raw in {"left", "l", "west", "w", "-1"}:
        return "left"
    if raw in {"right", "r", "east", "e", "1"}:
        return "right"
    return None


def _facing_from_x(coords, board_width):
    x = _safe_int(coords[1], None) if coords is not None else None
    width = _safe_int(board_width, None)
    if x is None or width is None or width <= 0:
        return None
    return "right" if x < (width / 2.0) else "left"


def _resolve_unit_facing(unit_data, coords, board_width):
    if isinstance(unit_data, dict):
        explicit = (
            unit_data.get("facing")
            or unit_data.get("Facing")
            or unit_data.get("orientation")
            or unit_data.get("Orientation")
        )
        normalized = _normalize_facing(explicit)
        if normalized is not None:
            return normalized
    return _facing_from_x(coords, board_width)


def _read_log_tail(max_lines=30, max_bytes=65536):
    candidates = [
        os.path.join(os.getcwd(), "gui", "response.txt"),
        os.path.join(os.getcwd(), "response.txt"),
    ]
    for path in candidates:
        if not os.path.exists(path):
            continue
        try:
            with open(path, "rb") as handle:
                handle.seek(0, os.SEEK_END)
                file_size = handle.tell()
                if file_size <= 0:
                    return []

                read_size = max(1, min(int(max_bytes), file_size))
                handle.seek(-read_size, os.SEEK_END)
                chunk = handle.read(read_size)
            text = chunk.decode("utf-8", errors="ignore")
            lines = text.splitlines()
            if read_size < file_size and lines:
                lines = lines[1:]
            lines = [line.rstrip("\n") for line in lines]
            return lines[-max_lines:] if lines else []
        except OSError:
            continue
    return []


def _read_event_tail(default_max_events=500):
    recorder = get_event_recorder()
    raw_limit = os.getenv("STATE_MODEL_EVENTS_LIMIT", str(default_max_events))
    try:
        limit = max(0, int(raw_limit))
    except (TypeError, ValueError):
        limit = default_max_events
    if limit == 0:
        return []
    return recorder.snapshot(limit=limit)


def _unit_payload(
    side,
    unit_id,
    unit_data,
    coords,
    hp,
    alive_models=None,
    anchor=None,
    model_positions=None,
    facing=None,
    weapon_profile=None,
):
    name = "—"
    models = None
    if isinstance(unit_data, dict):
        name = unit_data.get("Name") or name
        models = _safe_int(unit_data.get("#OfModels"), None)

    keywords = []
    if isinstance(unit_data, dict):
        raw_keywords = unit_data.get("KEYWORDS")
        if isinstance(raw_keywords, (list, tuple)):
            keywords = [str(v) for v in raw_keywords]
        elif raw_keywords is not None:
            try:
                keywords = [str(v) for v in list(raw_keywords)]
            except TypeError:
                keywords = [str(raw_keywords)]

    weapon_name = None
    weapon_range = None
    if isinstance(weapon_profile, dict):
        weapon_name = weapon_profile.get("Name")
        weapon_range = _safe_int(weapon_profile.get("Range"), None)

    return {
        "side": side,
        "id": unit_id,
        "name": name,
        "models": models,
        "alive_models": _safe_int(alive_models, None),
        "hp": _safe_float(hp, None),
        "x": _safe_int(coords[1], None) if coords is not None else None,
        "y": _safe_int(coords[0], None) if coords is not None else None,
        "anchor_x": _safe_int(anchor[1], None) if anchor is not None else None,
        "anchor_y": _safe_int(anchor[0], None) if anchor is not None else None,
        "model_positions": _iter_values(model_positions),
        "facing": facing,
        "keywords": keywords,
        "weapon_name": str(weapon_name) if weapon_name else None,
        "weapon_range": weapon_range,
    }


def _nearest_covering_barricade_id(env, unit_cell: tuple[int, int]) -> str | None:
    nearest_feature_id: str | None = None
    nearest_dist: float | None = None
    ux, uy = int(unit_cell[0]), int(unit_cell[1])
    for feature in _iter_values(getattr(env, "terrain_features", None)):
        if not isinstance(feature, dict):
            continue
        kind = str(feature.get("kind") or "").strip().lower()
        tags = " ".join(str(v).lower() for v in _iter_values(feature.get("keywords") or feature.get("tags")))
        if kind != "barricade" and "barricade" not in tags:
            continue
        feature_id = str(feature.get("id") or "").strip()
        if not feature_id:
            continue
        feature_min = None
        for cell in _iter_values(feature.get("cells")):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            dist = max(abs(ux - int(cell[0])), abs(uy - int(cell[1])))
            feature_min = dist if feature_min is None else min(feature_min, dist)
        if feature_min is None:
            continue
        if nearest_dist is None or feature_min < nearest_dist:
            nearest_dist = float(feature_min)
            nearest_feature_id = feature_id
    return nearest_feature_id


def _status_debug_enabled() -> bool:
    raw = str(os.getenv("STATUS_DEBUG", os.getenv("TERRAIN_DEBUG", "0"))).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _objective_state_for_unit(env, side: str, unit_cell: tuple[int, int]) -> str | None:
    objectives = _iter_values(getattr(env, "coordsOfOM", None))
    if not objectives:
        return None
    for idx, coords in enumerate(objectives):
        if not isinstance(coords, (list, tuple)) or len(coords) < 2:
            continue
        oy, ox = int(coords[0]), int(coords[1])
        if max(abs(unit_cell[0] - oy), abs(unit_cell[1] - ox)) > 3:
            continue
        model_oc = int(getattr(env, "model_obj_oc", [0])[idx]) if idx < len(getattr(env, "model_obj_oc", [])) else 0
        enemy_oc = int(getattr(env, "enemy_obj_oc", [0])[idx]) if idx < len(getattr(env, "enemy_obj_oc", [])) else 0
        if model_oc > 0 and enemy_oc > 0:
            return "contesting"
        if side == "model" and model_oc > enemy_oc:
            return "holding"
        if side == "enemy" and enemy_oc > model_oc:
            return "holding"
        if model_oc > 0 or enemy_oc > 0:
            return "contesting"
    return None


def _target_cover_cells(env, target_cell: tuple[int, int], radius: int = 3) -> set[tuple[int, int]]:
    obstacle_cells = set()
    for feature in _iter_values(getattr(env, "terrain_features", None)):
        if not isinstance(feature, dict):
            continue
        kind = str(feature.get("kind") or "").strip().lower()
        tags = " ".join(str(v).lower() for v in _iter_values(feature.get("keywords") or feature.get("tags")))
        if kind not in {"barricade", "obstacle"} and "obstacle" not in tags and "barricade" not in tags:
            continue
        for cell in _iter_values(feature.get("cells")):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            obstacle_cells.add((int(cell[0]), int(cell[1])))
    if not obstacle_cells:
        obstacle_cells = set((int(x), int(y)) for x, y in _iter_values(getattr(env, "terrain_opaque_cells", None)))

    tx, ty = int(target_cell[0]), int(target_cell[1])
    return {
        (ox, oy)
        for ox, oy in obstacle_cells
        if max(abs(ox - tx), abs(oy - ty)) <= int(radius)
    }


def _nearest_barricade_distance(env, unit_cell: tuple[int, int]) -> float | None:
    barricade_cells: set[tuple[int, int]] = set()
    for feature in _iter_values(getattr(env, "terrain_features", None)):
        if not isinstance(feature, dict):
            continue
        kind = str(feature.get("kind") or "").strip().lower()
        tags = " ".join(str(v).lower() for v in _iter_values(feature.get("keywords") or feature.get("tags")))
        if kind != "barricade" and "barricade" not in tags:
            continue
        for cell in _iter_values(feature.get("cells")):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            barricade_cells.add((int(cell[0]), int(cell[1])))
    if not barricade_cells:
        return None
    ux, uy = int(unit_cell[0]), int(unit_cell[1])
    min_dist = min(max(abs(ux - bx), abs(uy - by)) for bx, by in barricade_cells)
    return float(min_dist)


def _unit_status_payload(env, side: str, idx: int) -> dict:
    own_coords = env.unit_coords if side == "model" else env.enemy_coords
    enemy_coords = env.enemy_coords if side == "model" else env.unit_coords
    enemy_weapon = env.enemy_weapon if side == "model" else env.unit_weapon
    own_weapon = env.unit_weapon if side == "model" else env.enemy_weapon
    unit_data = env._get_unit_data(side, idx) if hasattr(env, "_get_unit_data") else {}

    if idx >= len(own_coords):
        return {"in_cover": False, "obscured": False, "fully_visible": False, "objective_state": None}

    unit_cell = (int(own_coords[idx][0]), int(own_coords[idx][1]))
    obscuring_cells = env.get_terrain_obscuring_cells_set() if hasattr(env, "get_terrain_obscuring_cells_set") else set()
    target_cover_cells = _target_cover_cells(env, unit_cell, radius=3)
    opaque_cells = getattr(env, "terrain_opaque_cells", set())
    visibility_mode = getattr(env, "visibility_mode", "single_ray")

    def _distance_between_units_local(attacker_side: str, attacker_idx: int, target_side: str, target_idx: int) -> float:
        if hasattr(env, "_shooting_distance_between_units"):
            try:
                return float(env._shooting_distance_between_units(attacker_side, int(attacker_idx), target_side, int(target_idx)))
            except Exception:
                pass
        if hasattr(env, "_distance_between_units"):
            try:
                return float(env._distance_between_units(attacker_side, int(attacker_idx), target_side, int(target_idx)))
            except Exception:
                pass
        attacker_pool = env.unit_coords if attacker_side == "model" else env.enemy_coords
        target_pool = env.unit_coords if target_side == "model" else env.enemy_coords
        if not (0 <= int(attacker_idx) < len(attacker_pool) and 0 <= int(target_idx) < len(target_pool)):
            return float("inf")
        attacker_cell = (int(attacker_pool[int(attacker_idx)][0]), int(attacker_pool[int(attacker_idx)][1]))
        target_cell = (int(target_pool[int(target_idx)][0]), int(target_pool[int(target_idx)][1]))
        return float(max(abs(attacker_cell[0] - target_cell[0]), abs(attacker_cell[1] - target_cell[1])))

    def _has_los_between_units_local(attacker_side: str, attacker_idx: int, target_side: str, target_idx: int) -> bool:
        if hasattr(env, "_unit_has_los"):
            try:
                return bool(env._unit_has_los(attacker_side, int(attacker_idx), target_side, int(target_idx)))
            except Exception:
                pass
        attacker_pool = env.unit_coords if attacker_side == "model" else env.enemy_coords
        target_pool = env.unit_coords if target_side == "model" else env.enemy_coords
        if not (0 <= int(attacker_idx) < len(attacker_pool) and 0 <= int(target_idx) < len(target_pool)):
            return False
        attacker_cell = (int(attacker_pool[int(attacker_idx)][0]), int(attacker_pool[int(attacker_idx)][1]))
        target_cell = (int(target_pool[int(target_idx)][0]), int(target_pool[int(target_idx)][1]))
        target_cover_local = _target_cover_cells(env, target_cell, radius=3)
        report_local = visibility_report(
            attacker_cell,
            target_cell,
            opaque_cells_set=opaque_cells,
            obscuring_cells_set=obscuring_cells,
            target_cover_cells_set=target_cover_local,
            visibility_mode=visibility_mode,
        )
        return bool(report_local.get("los", False))

    enemies_seeing = 0
    obscured_seen = 0
    fully_visible_seen = 0
    obscured_vs: list[int] = []
    exposed_to: list[int] = []
    seen_by_ids: list[int] = []
    for enemy_idx, enemy in enumerate(enemy_coords):
        if not isinstance(enemy, (list, tuple)) or len(enemy) < 2:
            continue
        enemy_id = env._unit_id("enemy" if side == "model" else "model", enemy_idx) if hasattr(env, "_unit_id") else None
        enemy_side = "enemy" if side == "model" else "model"
        if not _has_los_between_units_local(enemy_side, enemy_idx, side, idx):
            continue
        if enemy_id is not None:
            seen_by_ids.append(int(enemy_id))
        distance = _distance_between_units_local(enemy_side, enemy_idx, side, idx)
        range_limit = 0.0
        if enemy_idx < len(enemy_weapon) and isinstance(enemy_weapon[enemy_idx], dict):
            range_limit = float(enemy_weapon[enemy_idx].get("Range", 0) or 0)
        if distance > range_limit:
            continue
        enemies_seeing += 1
        report = visibility_report(
            (int(enemy[0]), int(enemy[1])),
            unit_cell,
            opaque_cells_set=opaque_cells,
            obscuring_cells_set=obscuring_cells,
            target_cover_cells_set=target_cover_cells,
            visibility_mode=visibility_mode,
        )
        if bool(report.get("fully_visible", False)):
            fully_visible_seen += 1
        if bool(report.get("obscured", False)):
            obscured_seen += 1
            if enemy_id is not None:
                obscured_vs.append(int(enemy_id))
        elif enemy_id is not None:
            exposed_to.append(int(enemy_id))

    obscured = enemies_seeing > 0 and obscured_seen > 0
    fully_visible = enemies_seeing > 0 and fully_visible_seen == enemies_seeing

    in_cover = False
    dist_cover = _nearest_barricade_distance(env, unit_cell)
    cover_source_terrain_id = _nearest_covering_barricade_id(env, unit_cell)
    if hasattr(env, "_unit_has_keyword") and hasattr(env, "_barricade_cells"):
        is_infantry = env._unit_has_keyword(unit_data, "infantry")
        if is_infantry and dist_cover is not None:
            in_cover = float(dist_cover) <= 3.0
    if not in_cover:
        cover_source_terrain_id = None

    objective_state = _objective_state_for_unit(env, side, unit_cell)

    used_advance = False
    advance_roll = None
    used_advance_list = getattr(env, "model_used_advance" if side == "model" else "enemy_used_advance", None)
    advance_roll_list = getattr(env, "model_advance_roll" if side == "model" else "enemy_advance_roll", None)
    if isinstance(used_advance_list, (list, tuple)) and idx < len(used_advance_list):
        used_advance = bool(used_advance_list[idx])
    if isinstance(advance_roll_list, (list, tuple)) and idx < len(advance_roll_list):
        raw_roll = advance_roll_list[idx]
        if raw_roll is not None:
            try:
                advance_roll = int(raw_roll)
            except Exception:
                advance_roll = None

    engagement_with: list[int] = []
    for enemy_idx, enemy in enumerate(enemy_coords):
        if not isinstance(enemy, (list, tuple)) or len(enemy) < 2:
            continue
        enemy_hp = env.enemy_health[enemy_idx] if side == "model" else env.unit_health[enemy_idx]
        if float(enemy_hp or 0.0) <= 0:
            continue
        enemy_cell = (int(enemy[0]), int(enemy[1]))
        if max(abs(enemy_cell[0] - unit_cell[0]), abs(enemy_cell[1] - unit_cell[1])) <= 1:
            enemy_id = env._unit_id("enemy" if side == "model" else "model", enemy_idx) if hasattr(env, "_unit_id") else None
            if enemy_id is not None:
                engagement_with.append(int(enemy_id))

    in_range_targets: list[int] = []
    can_see_ids: list[int] = []
    own_range = 0.0
    if idx < len(own_weapon) and isinstance(own_weapon[idx], dict):
        own_range = float(own_weapon[idx].get("Range", 0) or 0)
    enemy_side = "enemy" if side == "model" else "model"
    for enemy_idx, enemy in enumerate(enemy_coords):
        if not isinstance(enemy, (list, tuple)) or len(enemy) < 2:
            continue
        enemy_hp = env.enemy_health[enemy_idx] if side == "model" else env.unit_health[enemy_idx]
        if float(enemy_hp or 0.0) <= 0:
            continue
        if not _has_los_between_units_local(side, idx, enemy_side, enemy_idx):
            continue
        enemy_id = env._unit_id("enemy" if side == "model" else "model", enemy_idx) if hasattr(env, "_unit_id") else None
        if enemy_id is None:
            continue
        can_see_ids.append(int(enemy_id))
        if own_range > 0:
            distance = _distance_between_units_local(side, idx, enemy_side, enemy_idx)
            if distance <= own_range:
                in_range_targets.append(int(enemy_id))

    reachable_cells: list[list[int]] = []
    move_cells: list[list[int]] = []
    advance_cells: list[list[int]] = []
    phase_raw = str(getattr(env, "phase", "") or "").lower()
    movement_phase = ("move" in phase_raw) or ("движ" in phase_raw) or ("movement" in phase_raw)
    if movement_phase and hasattr(env, "get_unit_movement_overlay"):
        try:
            overlay = env.get_unit_movement_overlay(side, idx)
            for cell in _iter_values(overlay.get("move_cells") if isinstance(overlay, dict) else []):
                if isinstance(cell, (list, tuple)) and len(cell) >= 2:
                    rx = _safe_int(cell[0], None)
                    ry = _safe_int(cell[1], None)
                    if rx is not None and ry is not None:
                        move_cells.append([rx, ry])
                        reachable_cells.append([rx, ry])
            for cell in _iter_values(overlay.get("advance_cells") if isinstance(overlay, dict) else []):
                if isinstance(cell, (list, tuple)) and len(cell) >= 2:
                    rx = _safe_int(cell[0], None)
                    ry = _safe_int(cell[1], None)
                    if rx is not None and ry is not None:
                        advance_cells.append([rx, ry])
                        reachable_cells.append([rx, ry])
        except Exception:
            reachable_cells = []
            move_cells = []
            advance_cells = []
    elif movement_phase and hasattr(env, "get_unit_reachable_cells"):
        try:
            raw_reach = env.get_unit_reachable_cells(side, idx)
            for cell in _iter_values(raw_reach):
                if isinstance(cell, (list, tuple)) and len(cell) >= 2:
                    rx = _safe_int(cell[0], None)
                    ry = _safe_int(cell[1], None)
                    if rx is not None and ry is not None:
                        reachable_cells.append([rx, ry])
                        move_cells.append([rx, ry])
        except Exception:
            reachable_cells = []
            move_cells = []
            advance_cells = []

    return {
        "in_cover": bool(in_cover),
        "obscured": bool(obscured),
        "fully_visible": bool(fully_visible),
        "objective_state": objective_state,
        "used_advance": bool(used_advance),
        "advance_roll": advance_roll,
        "dist_cover": dist_cover,
        "cover_source_terrain_id": cover_source_terrain_id,
        "obscured_vs": sorted(set(obscured_vs)),
        "exposed_to": sorted(set(exposed_to)),
        "engagement_with": sorted(set(engagement_with)),
        "in_range_targets": sorted(set(in_range_targets)),
        "can_see_ids": sorted(set(can_see_ids)),
        "seen_by_ids": sorted(set(seen_by_ids)),
        "in_range_ids": sorted(set(in_range_targets)),
        "reachable_cells": reachable_cells,
        "move_cells": move_cells,
        "advance_cells": advance_cells,
    }


def write_state_json(env, path=None):
    io_profiler = get_io_profiler()
    state_path = path or os.getenv("STATE_JSON_PATH", DEFAULT_STATE_PATH)
    os.makedirs(os.path.dirname(state_path), exist_ok=True)

    board_width = _safe_int(getattr(env, "b_hei", None), None)

    units = []
    for idx, coords in enumerate(getattr(env, "enemy_coords", [])):
        unit_id = env._unit_id("enemy", idx)
        unit_data = env._get_unit_data("enemy", idx)
        hp = env.enemy_health[idx] if idx < len(env.enemy_health) else None
        weapon_profile = env.enemy_weapon[idx] if idx < len(getattr(env, "enemy_weapon", [])) else None
        unit_payload = _unit_payload("player", unit_id, unit_data, coords, hp,
                                   alive_models=env._alive_models_from_pool("enemy", idx) if hasattr(env, "_alive_models_from_pool") else None,
                                   anchor=(env.enemy_anchor_coords[idx] if hasattr(env, "enemy_anchor_coords") and idx < len(env.enemy_anchor_coords) else None),
                                   model_positions=([{"x": _safe_int(pos[1], None), "y": _safe_int(pos[0], None), "z": _safe_int(pos[2], 0)}
                                                     for pos in env.enemy_model_positions[idx]]
                                                    if hasattr(env, "enemy_model_positions") and idx < len(env.enemy_model_positions) else []),
                                   facing=_resolve_unit_facing(unit_data, coords, board_width),
                                   weapon_profile=weapon_profile)
        unit_payload["unit_status"] = _unit_status_payload(env, "enemy", idx)
        units.append(unit_payload)

    for idx, coords in enumerate(getattr(env, "unit_coords", [])):
        unit_id = env._unit_id("model", idx)
        unit_data = env._get_unit_data("model", idx)
        hp = env.unit_health[idx] if idx < len(env.unit_health) else None
        weapon_profile = env.unit_weapon[idx] if idx < len(getattr(env, "unit_weapon", [])) else None
        unit_payload = _unit_payload("model", unit_id, unit_data, coords, hp,
                                   alive_models=env._alive_models_from_pool("model", idx) if hasattr(env, "_alive_models_from_pool") else None,
                                   anchor=(env.unit_anchor_coords[idx] if hasattr(env, "unit_anchor_coords") and idx < len(env.unit_anchor_coords) else None),
                                   model_positions=([{"x": _safe_int(pos[1], None), "y": _safe_int(pos[0], None), "z": _safe_int(pos[2], 0)}
                                                     for pos in env.unit_model_positions[idx]]
                                                    if hasattr(env, "unit_model_positions") and idx < len(env.unit_model_positions) else []),
                                   facing=_resolve_unit_facing(unit_data, coords, board_width),
                                   weapon_profile=weapon_profile)
        unit_payload["unit_status"] = _unit_status_payload(env, "model", idx)
        units.append(unit_payload)

    if _status_debug_enabled() and hasattr(env, "_append_agent_log"):
        for unit in units:
            status = unit.get("unit_status") or {}
            env._append_agent_log(
                f"[STATUS] unit={unit.get('id')} in_cover={1 if bool(status.get('in_cover')) else 0} "
                f"dist_cover={status.get('dist_cover')} "
                f"obscured_vs={status.get('obscured_vs') or []} "
                f"exposed_to={status.get('exposed_to') or []}"
            )

    if (os.getenv("TERRAIN_DEBUG", "0") == "1" or os.getenv("VIEWER_DEBUG", "0") == "1") and hasattr(env, "_append_agent_log"):
        active_side_raw = getattr(env, "active_side", None)
        side = "model" if active_side_raw == "model" else ("enemy" if active_side_raw == "enemy" else None)
        active_idx = None
        try:
            active_idx = int(getattr(env, "current_action_index", 0) or 0)
        except (TypeError, ValueError):
            active_idx = None
        if side is not None and active_idx is not None and 0 <= active_idx:
            unit_id = env._unit_id(side, active_idx) if hasattr(env, "_unit_id") else active_idx
            budget = None
            if hasattr(env, "_movement_budget_for_unit"):
                try:
                    budget = int(env._movement_budget_for_unit(side, active_idx))
                except Exception:
                    budget = None
            count = 0
            for unit in units:
                expected_side = "model" if side == "model" else "player"
                if unit.get("side") == expected_side and int(unit.get("id") or -1) == int(unit_id):
                    st = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
                    count = len(list(st.get("reachable_cells") or []))
                    break
            sig = (side, int(unit_id), int(budget or -1), int(count))
            prev_sig = getattr(env, "_last_reachable_log_sig", None)
            if sig != prev_sig:
                env._last_reachable_log_sig = sig
                env._append_agent_log(
                    f"[MOVE] reachable_cells unit={unit_id} budget={budget if budget is not None else '-'} count={count}"
                )

    objectives = []
    for idx, coords in enumerate(getattr(env, "coordsOfOM", [])):
        objectives.append({
            "id": idx + 1,
            "x": _safe_int(coords[1], None),
            "y": _safe_int(coords[0], None),
        })

    terrain_cover_map: dict[str, set[int]] = {}
    for unit in units:
        if not isinstance(unit, dict):
            continue
        unit_id = _safe_int(unit.get("id"), None)
        status = unit.get("unit_status") if isinstance(unit.get("unit_status"), dict) else {}
        source_id = str(status.get("cover_source_terrain_id") or "").strip()
        if unit_id is None or not source_id or not bool(status.get("in_cover")):
            continue
        terrain_cover_map.setdefault(source_id, set()).add(int(unit_id))

    terrain_features = []
    for feature in _iter_values(getattr(env, "terrain_features", None)):
        if not isinstance(feature, dict):
            continue
        cells = []
        for cell in _iter_values(feature.get("cells")):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            cells.append([_safe_int(cell[0], None), _safe_int(cell[1], None)])
        raw_keywords = feature.get("keywords")
        if raw_keywords is None:
            raw_keywords = feature.get("tags")
        keywords = [str(v) for v in _iter_values(raw_keywords)]
        terrain_features.append({
            "id": str(feature.get("id") or ""),
            "kind": str(feature.get("kind") or "barricade"),
            "name": str(feature.get("name") or feature.get("kind") or "Terrain"),
            "keywords": keywords,
            "cells": cells,
            "cell_rotations": [_safe_int(v, 0) for v in _iter_values(feature.get("cell_rotations"))],
            "tags": keywords,
            "opacity": str(feature.get("opacity") or "obscuring"),
            "sprite": str(feature.get("sprite") or ""),
            "covering_unit_ids": sorted(terrain_cover_map.get(str(feature.get("id") or ""), set())),
        })

    active_side = getattr(env, "active_side", None)
    if active_side == "enemy":
        active_side = "player"
    elif active_side == "model":
        active_side = "model"

    movement_overlay = None
    phase_raw = str(getattr(env, "phase", "") or "").lower()
    if ("move" in phase_raw or "движ" in phase_raw or "movement" in phase_raw) and hasattr(env, "get_unit_movement_overlay"):
        try:
            active_idx = int(getattr(env, "current_action_index", 0) or 0)
        except (TypeError, ValueError):
            active_idx = 0
        if active_side in {"player", "model"}:
            overlay_side = "enemy" if active_side == "player" else "model"
            try:
                unit_id = int(env._unit_id(overlay_side, active_idx)) if hasattr(env, "_unit_id") else None
            except Exception:
                unit_id = None
            try:
                overlay_data = env.get_unit_movement_overlay(overlay_side, active_idx)
            except Exception:
                overlay_data = None
            if isinstance(overlay_data, dict):
                movement_overlay = {
                    "unit_id": unit_id,
                    "move_cells": [],
                    "advance_cells": [],
                }
                for cell in _iter_values(overlay_data.get("move_cells")):
                    if isinstance(cell, (list, tuple)) and len(cell) >= 2:
                        cx = _safe_int(cell[0], None)
                        cy = _safe_int(cell[1], None)
                        if cx is not None and cy is not None:
                            movement_overlay["move_cells"].append([cx, cy])
                for cell in _iter_values(overlay_data.get("advance_cells")):
                    if isinstance(cell, (list, tuple)) and len(cell) >= 2:
                        cx = _safe_int(cell[0], None)
                        cy = _safe_int(cell[1], None)
                        if cx is not None and cy is not None:
                            movement_overlay["advance_cells"].append([cx, cy])

    payload = {
        "board": {
            "width": _safe_int(getattr(env, "b_hei", None), None),
            "height": _safe_int(getattr(env, "b_len", None), None),
            "board_w": _safe_int(getattr(env, "b_hei", None), None),
            "board_h": _safe_int(getattr(env, "b_len", None), None),
            "cols": _safe_int(getattr(env, "b_hei", None), None),
            "rows": _safe_int(getattr(env, "b_len", None), None),
        },
        "turn": _safe_int(getattr(env, "numTurns", None), None),
        "round": _safe_int(getattr(env, "battle_round", None), None),
        "phase": getattr(env, "phase", None),
        "active": active_side,
        "movement_overlay": movement_overlay,
        "vp": {"player": _safe_int(getattr(env, "enemyVP", None), None),
               "model": _safe_int(getattr(env, "modelVP", None), None)},
        "cp": {"player": _safe_int(getattr(env, "enemyCP", None), None),
               "model": _safe_int(getattr(env, "modelCP", None), None)},
        "units": units,
        "objectives": objectives,
        "terrain_features": terrain_features,
        "attacker_side": getattr(env, "attacker_side", None),
        "defender_side": getattr(env, "defender_side", None),
        "deployment": {
            "attacker": getattr(env, "attacker_side", None),
            "defender": getattr(env, "defender_side", None),
            "mode": getattr(env, "deployment_mode", None),
            "rl_stats": getattr(env, "deployment_rl_stats", None),
        },
        "payload_kind": "light",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

    payload_mode = str(os.getenv("STATE_PAYLOAD_MODE", "auto")).strip().lower()
    include_full_payload = payload_mode in {"full", "always"}
    if payload_mode in {"auto", "", "default"}:
        interval_ms = max(0, _safe_int(os.getenv("STATE_FULL_PAYLOAD_INTERVAL_MS", "1000"), 1000) or 1000)
        last_full_ts = float(getattr(env, "_state_payload_last_full_ts", 0.0) or 0.0)
        now_ts = time.monotonic()
        include_full_payload = (now_ts - last_full_ts) >= (interval_ms / 1000.0)
        if include_full_payload:
            env._state_payload_last_full_ts = now_ts

    if include_full_payload:
        payload["payload_kind"] = "full"
        payload["log_tail"] = _read_log_tail()
        payload["model_events"] = _read_event_tail()

    state_dir = os.path.dirname(state_path)
    temp_path = None
    try:
        with io_profiler.timed("state export"):
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=state_dir,
                delete=False,
                prefix="state.",
                suffix=".tmp",
            ) as handle:
                temp_path = handle.name
                json.dump(payload, handle, ensure_ascii=False, indent=2)
                handle.flush()
                os.fsync(handle.fileno())

            os.replace(temp_path, state_path)
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

    return payload
