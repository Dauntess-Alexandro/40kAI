import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

from gym_mod.engine.state_events_v2 import iter_json_lines, validate_event


def _default_state() -> Dict[str, Any]:
    return {
        "version": 2,
        "board": {"width": 60, "height": 40},
        "turn": None,
        "round": None,
        "phase": None,
        "active": None,
        "vp": {"player": None, "model": None},
        "cp": {"player": None, "model": None},
        "units": [],
        "objectives": [],
        "log_tail": [],
    }


def load_state(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return _default_state()
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    state = _default_state()
    if isinstance(data, dict):
        state.update(data)
    return state


@dataclass
class StateWatcher:
    path: str
    events_path: str | None = None
    mtime: float = 0.0
    state: Dict[str, Any] = field(default_factory=_default_state)
    events_offset: int = 0

    def load_if_changed(self) -> bool:
        if not os.path.exists(self.path):
            return False
        new_mtime = os.path.getmtime(self.path)
        if new_mtime <= self.mtime:
            return False
        self.mtime = new_mtime
        self.state = load_state(self.path)
        return True

    def drain_events(self) -> List[Dict[str, Any]]:
        events_path = self.events_path or os.path.join(os.path.dirname(self.path), "state_events.jsonl")
        if not os.path.exists(events_path):
            return []
        size = os.path.getsize(events_path)
        if size < self.events_offset:
            self.events_offset = 0
        with open(events_path, "r", encoding="utf-8") as handle:
            handle.seek(self.events_offset)
            lines = handle.read().splitlines()
            self.events_offset = handle.tell()
        events: List[Dict[str, Any]] = []
        for raw in iter_json_lines(lines):
            try:
                events.append(validate_event(raw))
            except ValueError:
                continue
        return events
