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


def _unit_payload(side, unit_id, unit_data, coords, hp, alive_models=None, anchor=None, model_positions=None, facing=None):
    name = "—"
    models = None
    if isinstance(unit_data, dict):
        name = unit_data.get("Name") or name
        models = _safe_int(unit_data.get("#OfModels"), None)

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
        "model_positions": model_positions or [],
        "facing": facing,
        "keywords": list(unit_data.get("KEYWORDS") or []) if isinstance(unit_data, dict) else [],
    }


def _status_debug_enabled() -> bool:
    raw = str(os.getenv("STATUS_DEBUG", os.getenv("TERRAIN_DEBUG", "0"))).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _objective_state_for_unit(env, side: str, unit_cell: tuple[int, int]) -> str | None:
    objectives = list(getattr(env, "coordsOfOM", []) or [])
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


def _unit_status_payload(env, side: str, idx: int) -> dict:
    own_coords = env.unit_coords if side == "model" else env.enemy_coords
    enemy_coords = env.enemy_coords if side == "model" else env.unit_coords
    enemy_weapon = env.enemy_weapon if side == "model" else env.unit_weapon
    unit_data = env._get_unit_data(side, idx) if hasattr(env, "_get_unit_data") else {}

    if idx >= len(own_coords):
        return {"in_cover": False, "obscured": False, "fully_visible": False, "objective_state": None}

    unit_cell = (int(own_coords[idx][0]), int(own_coords[idx][1]))
    obscuring_cells = env.get_terrain_obscuring_cells_set() if hasattr(env, "get_terrain_obscuring_cells_set") else set()
    opaque_cells = getattr(env, "terrain_opaque_cells", set())
    visibility_mode = getattr(env, "visibility_mode", "single_ray")

    enemies_seeing = 0
    obscured_seen = 0
    fully_visible_seen = 0
    for enemy_idx, enemy in enumerate(enemy_coords):
        if not isinstance(enemy, (list, tuple)) or len(enemy) < 2:
            continue
        attacker_cell = (int(enemy[0]), int(enemy[1]))
        report = visibility_report(
            attacker_cell,
            unit_cell,
            opaque_cells_set=opaque_cells,
            obscuring_cells_set=obscuring_cells,
            visibility_mode=visibility_mode,
        )
        if not bool(report.get("los", False)):
            continue
        distance = max(abs(attacker_cell[0] - unit_cell[0]), abs(attacker_cell[1] - unit_cell[1]))
        range_limit = 0.0
        if enemy_idx < len(enemy_weapon) and isinstance(enemy_weapon[enemy_idx], dict):
            range_limit = float(enemy_weapon[enemy_idx].get("Range", 0) or 0)
        if distance > range_limit:
            continue
        enemies_seeing += 1
        if bool(report.get("fully_visible", False)):
            fully_visible_seen += 1
        if bool(report.get("obscured", False)):
            obscured_seen += 1

    obscured = enemies_seeing > 0 and obscured_seen > 0
    fully_visible = enemies_seeing > 0 and fully_visible_seen == enemies_seeing

    in_cover = False
    if hasattr(env, "_unit_has_keyword") and hasattr(env, "_barricade_cells"):
        is_infantry = env._unit_has_keyword(unit_data, "infantry")
        if is_infantry:
            barricades = env._barricade_cells()
            if barricades:
                min_dist = min(max(abs(unit_cell[0] - c[0]), abs(unit_cell[1] - c[1])) for c in barricades)
                in_cover = min_dist <= 3 and obscured

    objective_state = _objective_state_for_unit(env, side, unit_cell)
    return {
        "in_cover": bool(in_cover),
        "obscured": bool(obscured),
        "fully_visible": bool(fully_visible),
        "objective_state": objective_state,
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
        unit_payload = _unit_payload("player", unit_id, unit_data, coords, hp,
                                   alive_models=env._alive_models_from_pool("enemy", idx) if hasattr(env, "_alive_models_from_pool") else None,
                                   anchor=(env.enemy_anchor_coords[idx] if hasattr(env, "enemy_anchor_coords") and idx < len(env.enemy_anchor_coords) else None),
                                   model_positions=([{"x": _safe_int(pos[1], None), "y": _safe_int(pos[0], None), "z": _safe_int(pos[2], 0)}
                                                     for pos in env.enemy_model_positions[idx]]
                                                    if hasattr(env, "enemy_model_positions") and idx < len(env.enemy_model_positions) else []),
                                   facing=_resolve_unit_facing(unit_data, coords, board_width))
        unit_payload["unit_status"] = _unit_status_payload(env, "enemy", idx)
        units.append(unit_payload)

    for idx, coords in enumerate(getattr(env, "unit_coords", [])):
        unit_id = env._unit_id("model", idx)
        unit_data = env._get_unit_data("model", idx)
        hp = env.unit_health[idx] if idx < len(env.unit_health) else None
        unit_payload = _unit_payload("model", unit_id, unit_data, coords, hp,
                                   alive_models=env._alive_models_from_pool("model", idx) if hasattr(env, "_alive_models_from_pool") else None,
                                   anchor=(env.unit_anchor_coords[idx] if hasattr(env, "unit_anchor_coords") and idx < len(env.unit_anchor_coords) else None),
                                   model_positions=([{"x": _safe_int(pos[1], None), "y": _safe_int(pos[0], None), "z": _safe_int(pos[2], 0)}
                                                     for pos in env.unit_model_positions[idx]]
                                                    if hasattr(env, "unit_model_positions") and idx < len(env.unit_model_positions) else []),
                                   facing=_resolve_unit_facing(unit_data, coords, board_width))
        unit_payload["unit_status"] = _unit_status_payload(env, "model", idx)
        units.append(unit_payload)

    if _status_debug_enabled() and hasattr(env, "_append_agent_log"):
        for unit in units:
            status = unit.get("unit_status") or {}
            env._append_agent_log(
                f"[STATUS] unit={unit.get('id')} in_cover={bool(status.get('in_cover'))} "
                f"obscured={bool(status.get('obscured'))} fully_visible={bool(status.get('fully_visible'))} "
                f"objective={status.get('objective_state') or '-'}"
            )

    objectives = []
    for idx, coords in enumerate(getattr(env, "coordsOfOM", [])):
        objectives.append({
            "id": idx + 1,
            "x": _safe_int(coords[1], None),
            "y": _safe_int(coords[0], None),
        })

    terrain_features = []
    for feature in (getattr(env, "terrain_features", []) or []):
        if not isinstance(feature, dict):
            continue
        cells = []
        for cell in (feature.get("cells") or []):
            if not isinstance(cell, (list, tuple)) or len(cell) < 2:
                continue
            cells.append([_safe_int(cell[0], None), _safe_int(cell[1], None)])
        keywords = [str(v) for v in list(feature.get("keywords") or feature.get("tags") or [])]
        terrain_features.append({
            "id": str(feature.get("id") or ""),
            "kind": str(feature.get("kind") or "barricade"),
            "name": str(feature.get("name") or feature.get("kind") or "Terrain"),
            "keywords": keywords,
            "cells": cells,
            "cell_rotations": [_safe_int(v, 0) for v in list(feature.get("cell_rotations") or [])],
            "tags": keywords,
            "opacity": str(feature.get("opacity") or "obscuring"),
            "sprite": str(feature.get("sprite") or ""),
        })

    active_side = getattr(env, "active_side", None)
    if active_side == "enemy":
        active_side = "player"
    elif active_side == "model":
        active_side = "model"

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
