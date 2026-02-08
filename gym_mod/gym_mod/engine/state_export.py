import json
import os
from datetime import datetime

from gym_mod.engine.event_bus import get_event_recorder
from gym_mod.engine.state_v2 import (
    BoardState,
    GameStateV2,
    ObjectiveState,
    PhaseState,
    ResourceState,
    UnitState,
)


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


def _read_log_tail(max_lines=30):
    candidates = [
        os.path.join(os.getcwd(), "gui", "response.txt"),
        os.path.join(os.getcwd(), "response.txt"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                lines = [line.rstrip("\n") for line in handle.readlines()]
                return lines[-max_lines:] if lines else []
    return []


def _read_event_tail(max_events=2000):
    recorder = get_event_recorder()
    return recorder.snapshot(limit=max_events)


def _unit_payload(side, unit_id, unit_data, coords, hp):
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
        "hp": _safe_float(hp, None),
        "x": _safe_int(coords[1], None) if coords is not None else None,
        "y": _safe_int(coords[0], None) if coords is not None else None,
    }


def _normalize_active_side(active_side):
    if active_side == "enemy":
        return "player"
    if active_side == "model":
        return "model"
    return active_side


def _collect_units(env):
    units = []
    for idx, coords in enumerate(getattr(env, "enemy_coords", [])):
        unit_id = env._unit_id("enemy", idx)
        unit_data = env._get_unit_data("enemy", idx)
        hp = env.enemy_health[idx] if idx < len(env.enemy_health) else None
        units.append(_unit_payload("player", unit_id, unit_data, coords, hp))
    for idx, coords in enumerate(getattr(env, "unit_coords", [])):
        unit_id = env._unit_id("model", idx)
        unit_data = env._get_unit_data("model", idx)
        hp = env.unit_health[idx] if idx < len(env.unit_health) else None
        units.append(_unit_payload("model", unit_id, unit_data, coords, hp))
    return units


def _collect_objectives(env):
    objectives = []
    for idx, coords in enumerate(getattr(env, "coordsOfOM", [])):
        objectives.append({
            "id": idx + 1,
            "x": _safe_int(coords[1], None),
            "y": _safe_int(coords[0], None),
        })
    return objectives


def _build_state_payload(env):
    active_side = _normalize_active_side(getattr(env, "active_side", None))
    units = _collect_units(env)
    objectives = _collect_objectives(env)

    return {
        "board": {
            "width": _safe_int(getattr(env, "b_hei", None), None),
            "height": _safe_int(getattr(env, "b_len", None), None),
        },
        "turn": _safe_int(getattr(env, "numTurns", None), None),
        "round": _safe_int(getattr(env, "battle_round", None), None),
        "phase": getattr(env, "phase", None),
        "active": active_side,
        "vp": {
            "player": _safe_int(getattr(env, "enemyVP", None), None),
            "model": _safe_int(getattr(env, "modelVP", None), None),
        },
        "cp": {
            "player": _safe_int(getattr(env, "enemyCP", None), None),
            "model": _safe_int(getattr(env, "modelCP", None), None),
        },
        "units": units,
        "objectives": objectives,
        "log_tail": _read_log_tail(),
        "model_events": _read_event_tail(),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def _build_state_v2(env) -> GameStateV2:
    payload = _build_state_payload(env)
    board = BoardState.from_dict(payload.get("board", {}))
    phase = PhaseState.from_dict(payload)
    units = [UnitState.from_dict(unit) for unit in payload["units"]]
    objectives = [ObjectiveState.from_dict(obj) for obj in payload["objectives"]]
    vp = ResourceState.from_dict(payload.get("vp", {}))
    cp = ResourceState.from_dict(payload.get("cp", {}))
    return GameStateV2(
        board=board,
        phase=phase,
        units=units,
        objectives=objectives,
        vp=vp,
        cp=cp,
        log_tail=payload.get("log_tail", []),
        model_events=payload.get("model_events", []),
        generated_at=payload.get("generated_at") or datetime.utcnow().isoformat() + "Z",
    )


def write_state_json(env, path=None):
    state_path = path or os.getenv("STATE_JSON_PATH", DEFAULT_STATE_PATH)
    os.makedirs(os.path.dirname(state_path), exist_ok=True)

    if os.getenv("STATE_V2", "0") == "1":
        payload = _build_state_v2(env).to_dict()
    else:
        payload = _build_state_payload(env)

    with open(state_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    return payload
