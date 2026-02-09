import json
import os
from collections import OrderedDict
from datetime import datetime

from gym_mod.engine.event_bus import get_event_recorder


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


def _sort_events(events):
    indexed = []
    for idx, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        seq = _safe_int(event.get("seq"), None)
        ts = _safe_float(event.get("ts"), None)
        if seq is not None:
            key = (0, seq, ts or 0, idx)
        else:
            key = (1, ts or 0, idx)
        indexed.append((key, event))
    indexed.sort(key=lambda item: item[0])
    return [event for _, event in indexed]


def _build_phase_timeline(events):
    phases: "OrderedDict[str, dict]" = OrderedDict()
    for event in events:
        if not isinstance(event, dict):
            continue
        phase_id = event.get("phase_id")
        if not phase_id:
            phase_id = (
                f"{event.get('battle_round', '—')}:"
                f"{event.get('turn', '—')}:"
                f"{event.get('side', '—')}:"
                f"{event.get('phase', 'unknown')}"
            )
        if phase_id not in phases:
            phases[phase_id] = {
                "phase_id": phase_id,
                "phase": event.get("phase"),
                "turn": event.get("turn"),
                "battle_round": event.get("battle_round"),
                "side": event.get("side"),
                "events": [],
                "start_seq": None,
                "end_seq": None,
            }
        phase_entry = phases[phase_id]
        seq = _safe_int(event.get("seq"), None)
        phase_entry["events"].append(
            {
                "seq": seq,
                "type": event.get("type"),
                "msg": event.get("msg"),
                "unit_id": event.get("unit_id"),
                "unit_name": event.get("unit_name"),
                "verbosity": event.get("verbosity"),
            }
        )
        if seq is not None:
            if phase_entry["start_seq"] is None or seq < phase_entry["start_seq"]:
                phase_entry["start_seq"] = seq
            if phase_entry["end_seq"] is None or seq > phase_entry["end_seq"]:
                phase_entry["end_seq"] = seq
    return list(phases.values())


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


def write_state_json(env, path=None):
    state_path = path or os.getenv("STATE_JSON_PATH", DEFAULT_STATE_PATH)
    os.makedirs(os.path.dirname(state_path), exist_ok=True)

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

    objectives = []
    for idx, coords in enumerate(getattr(env, "coordsOfOM", [])):
        objectives.append({
            "id": idx + 1,
            "x": _safe_int(coords[1], None),
            "y": _safe_int(coords[0], None),
        })

    active_side = getattr(env, "active_side", None)
    if active_side == "enemy":
        active_side = "player"
    elif active_side == "model":
        active_side = "model"

    event_tail = _read_event_tail()
    sorted_events = _sort_events(event_tail)
    payload = {
        "board": {"width": _safe_int(getattr(env, "b_hei", None), None),
                  "height": _safe_int(getattr(env, "b_len", None), None)},
        "turn": _safe_int(getattr(env, "numTurns", None), None),
        "round": _safe_int(getattr(env, "battle_round", None), None),
        "phase": getattr(env, "phase", None),
        "phase_id": getattr(env, "_phase_id", None),
        "active": active_side,
        "vp": {"player": _safe_int(getattr(env, "enemyVP", None), None),
               "model": _safe_int(getattr(env, "modelVP", None), None)},
        "cp": {"player": _safe_int(getattr(env, "enemyCP", None), None),
               "model": _safe_int(getattr(env, "modelCP", None), None)},
        "units": units,
        "objectives": objectives,
        "log_tail": _read_log_tail(),
        "model_events": sorted_events,
        "phase_timeline": _build_phase_timeline(sorted_events),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

    with open(state_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    return payload
