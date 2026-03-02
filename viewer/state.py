import json
import os
import time
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
        "terrain_features": [],
        "log_tail": [],
    }


def load_state(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return _default_state()
    last_error = None
    for _ in range(3):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            break
        except json.JSONDecodeError as exc:
            last_error = exc
            time.sleep(0.02)
    else:
        if last_error is not None:
            raise last_error
        return _default_state()

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
        try:
            self.state = load_state(self.path)
        except json.JSONDecodeError:
            # Писатель может обновлять файл прямо сейчас; оставляем предыдущее валидное состояние.
            return False
        return True
