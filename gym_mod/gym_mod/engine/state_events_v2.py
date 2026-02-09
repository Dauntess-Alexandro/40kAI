import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

EVENT_VERSION = 2

PHASE_START = "phase_start"
PHASE_END = "phase_end"
UNIT_SELECTED = "unit_selected"
UNIT_MOVE = "unit_move"
SHOT = "shot"
UNIT_HP = "unit_hp"
UNIT_KILLED = "unit_killed"
CAMERA_FOCUS = "camera_focus"
FX_SPAWN = "fx_spawn"

REQUIRED_FIELDS = ("version", "event_id", "turn", "phase", "type")


def ensure_fields(evt: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in defaults.items():
        evt.setdefault(key, value)
    return evt


def _coerce_int(value: Any, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Поле {field} должно быть int, получили {value!r}.")


def validate_event(evt: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(evt, dict):
        raise ValueError(f"EventV2 должен быть dict, получили {type(evt).__name__}.")

    evt = dict(evt)
    evt["version"] = EVENT_VERSION
    for key in REQUIRED_FIELDS:
        if key not in evt:
            raise ValueError(f"EventV2 без поля {key}.")

    evt["event_id"] = _coerce_int(evt.get("event_id"), "event_id")
    evt["turn"] = _coerce_int(evt.get("turn"), "turn")
    evt["phase"] = str(evt.get("phase") or "")
    evt["type"] = str(evt.get("type") or "")

    if "t_ms" in evt and evt["t_ms"] is not None:
        evt["t_ms"] = _coerce_int(evt.get("t_ms"), "t_ms")

    if "unit_id" in evt and evt["unit_id"] is not None:
        evt["unit_id"] = _coerce_int(evt.get("unit_id"), "unit_id")

    return evt


def _read_last_event_id(path: str) -> int:
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "rb") as handle:
            handle.seek(0, os.SEEK_END)
            end = handle.tell()
            if end == 0:
                return 0
            size = min(end, 8192)
            handle.seek(end - size)
            chunk = handle.read(size)
        lines = chunk.splitlines()
        for raw in reversed(lines):
            if not raw.strip():
                continue
            try:
                data = json.loads(raw.decode("utf-8"))
                return int(data.get("event_id", 0))
            except Exception:
                continue
    except Exception:
        return 0
    return 0


@dataclass
class EventWriterV2:
    path: str
    event_id: int = 0

    def __init__(self, path: Optional[str] = None) -> None:
        default_path = os.path.join(os.getcwd(), "gui", "state_events.jsonl")
        self.path = path or os.getenv("STATE_EVENTS_PATH", default_path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.event_id = _read_last_event_id(self.path)

    def emit(
        self,
        event_type: str,
        *,
        turn: int,
        phase: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self.event_id += 1
        evt = {
            "version": EVENT_VERSION,
            "event_id": self.event_id,
            "turn": turn,
            "phase": phase,
            "type": event_type,
            "t_ms": int(time.time() * 1000),
        }
        if payload:
            evt.update(payload)
        evt = validate_event(evt)
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(evt, ensure_ascii=False) + "\n")
        return evt


def iter_json_lines(lines: Iterable[str]) -> Iterable[Dict[str, Any]]:
    for line in lines:
        text = line.strip()
        if not text:
            continue
        yield json.loads(text)
