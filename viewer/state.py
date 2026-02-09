import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict


def _default_state() -> Dict[str, Any]:
    return {
        "board": {"width": 60, "height": 40},
        "turn": None,
        "round": None,
        "phase": None,
        "phase_id": None,
        "active": None,
        "vp": {"player": None, "model": None},
        "cp": {"player": None, "model": None},
        "units": [],
        "objectives": [],
        "log_tail": [],
        "model_events": [],
        "phase_timeline": [],
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
    mtime: float = 0.0
    state: Dict[str, Any] = field(default_factory=_default_state)

    def load_if_changed(self) -> bool:
        if not os.path.exists(self.path):
            return False
        new_mtime = os.path.getmtime(self.path)
        if new_mtime <= self.mtime:
            return False
        self.mtime = new_mtime
        self.state = load_state(self.path)
        return True
