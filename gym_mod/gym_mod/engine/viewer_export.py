import json
import os


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUTPUT_DIR = os.path.join(ROOT_DIR, "viewer_out")
SNAPSHOT_PATH = os.path.join(OUTPUT_DIR, "snapshot.json")
EVENTS_PATH = os.path.join(OUTPUT_DIR, "events.jsonl")


def _debug(message: str) -> None:
    if os.getenv("VIEWER_DEBUG", "0") == "1":
        print(f"[viewer_export] {message}")


def _ensure_output_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _safe_int(value, fallback=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _safe_float(value, fallback=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_snapshot_from_env(env) -> dict:
    units = []
    for idx, coords in enumerate(getattr(env, "enemy_coords", [])):
        unit_id = env._unit_id("enemy", idx)
        unit_data = env._get_unit_data("enemy", idx)
        hp = env.enemy_health[idx] if idx < len(env.enemy_health) else None
        units.append(
            {
                "id": unit_id,
                "side": "player",
                "x": _safe_int(coords[1], None) if coords is not None else None,
                "y": _safe_int(coords[0], None) if coords is not None else None,
                "hp": _safe_float(hp, None),
                "name": unit_data.get("Name") if isinstance(unit_data, dict) else None,
            }
        )

    for idx, coords in enumerate(getattr(env, "unit_coords", [])):
        unit_id = env._unit_id("model", idx)
        unit_data = env._get_unit_data("model", idx)
        hp = env.unit_health[idx] if idx < len(env.unit_health) else None
        units.append(
            {
                "id": unit_id,
                "side": "model",
                "x": _safe_int(coords[1], None) if coords is not None else None,
                "y": _safe_int(coords[0], None) if coords is not None else None,
                "hp": _safe_float(hp, None),
                "name": unit_data.get("Name") if isinstance(unit_data, dict) else None,
            }
        )

    active_side = getattr(env, "active_side", None)
    if active_side == "enemy":
        active_side = "player"
    elif active_side == "model":
        active_side = "model"

    tick = _safe_int(getattr(env, "numTurns", None), 0)
    if not tick:
        tick = _safe_int(getattr(env, "battle_round", None), 0)

    return {
        "tick": tick,
        "active_side": active_side,
        "phase": getattr(env, "phase", None),
        "units": units,
        "fx": [],
    }


def write_snapshot(state_dict: dict) -> None:
    _ensure_output_dir()
    tmp_path = SNAPSHOT_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(state_dict, handle, ensure_ascii=False)
    os.replace(tmp_path, SNAPSHOT_PATH)
    _debug(f"snapshot written: {SNAPSHOT_PATH}")


def append_event(event_dict: dict) -> None:
    _ensure_output_dir()
    with open(EVENTS_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(event_dict, ensure_ascii=False) + "\n")
    _debug(f"event appended: {event_dict.get('type')}")
