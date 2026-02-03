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
        "active_unit": None,
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


def _stat_mtime_ns(path: str) -> int:
    stat_result = os.stat(path)
    if hasattr(stat_result, "st_mtime_ns"):
        return int(stat_result.st_mtime_ns)
    return int(stat_result.st_mtime * 1_000_000_000)


@dataclass
class StateWatcher:
    path: str
    mtime_ns: int = 0
    state: Dict[str, Any] = field(default_factory=_default_state)

    def load_if_changed(self) -> bool:
        if not os.path.exists(self.path):
            return False
        new_mtime = _stat_mtime_ns(self.path)
        if new_mtime <= self.mtime_ns:
            return False
        self.mtime_ns = new_mtime
        self.state = load_state(self.path)
        return True
