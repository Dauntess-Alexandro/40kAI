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
    mtime_ns: int = 0
    size: int = -1
    state: Dict[str, Any] = field(default_factory=_default_state)

    def load_if_changed(self) -> bool:
        if not os.path.exists(self.path):
            return False
        stat = os.stat(self.path)
        new_mtime_ns = int(getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000)))
        new_size = int(stat.st_size)
        if new_mtime_ns == self.mtime_ns and new_size == self.size:
            return False
        self.mtime_ns = new_mtime_ns
        self.size = new_size
        self.state = load_state(self.path)
        return True
