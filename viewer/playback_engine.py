from __future__ import annotations

import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

from PySide6 import QtCore


class PlaybackEngine(QtCore.QObject):
    sig_apply_snapshot = QtCore.Signal(dict)
    sig_event = QtCore.Signal(dict)
    sig_phase_changed = QtCore.Signal(str, int)
    sig_cursor_changed = QtCore.Signal(int, int)

    def __init__(self, debug: Optional[callable] = None) -> None:
        super().__init__()
        self.current_snapshot: Optional[Dict[str, Any]] = None
        self._pending_snapshot: Optional[Dict[str, Any]] = None
        self.event_queue: List[Dict[str, Any]] = []
        self.by_phase: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.cursor: int = 0
        self.phase_index: int = 0
        self.phase_list: List[str] = []
        self.playback_mode: str = "paused"
        self._speed: float = 1.0
        self._debug = debug

    def _log(self, message: str) -> None:
        if os.getenv("GUI_DEBUG", "0") == "1" and self._debug:
            self._debug(message)

    def ingest_snapshot(self, snapshot_json: Dict[str, Any]) -> None:
        if self.event_queue and self.cursor < len(self.event_queue):
            self._pending_snapshot = snapshot_json
            self._log("Playback: snapshot отложен до конца очереди.")
            return
        self.current_snapshot = snapshot_json
        self._pending_snapshot = None
        self._log("Playback: snapshot применён.")
        self.sig_apply_snapshot.emit(snapshot_json)

    def ingest_event(self, evt: Dict[str, Any]) -> None:
        self.event_queue.append(evt)
        phase = str(evt.get("phase") or "unknown")
        self.by_phase[phase].append(evt)
        if phase not in self.phase_list:
            self.phase_list.append(phase)
        self.sig_cursor_changed.emit(self.cursor, len(self.event_queue))
        self._log(f"Playback: event {evt.get('event_id')} phase={phase} type={evt.get('type')}.")

    def _apply_pending_snapshot_if_ready(self) -> None:
        if self._pending_snapshot and self.cursor >= len(self.event_queue):
            snapshot = self._pending_snapshot
            self._pending_snapshot = None
            self.current_snapshot = snapshot
            self._log("Playback: отложенный snapshot применён.")
            self.sig_apply_snapshot.emit(snapshot)

    def step_event(self, fast: bool = False) -> bool:
        if self.cursor >= len(self.event_queue):
            self._apply_pending_snapshot_if_ready()
            return False
        evt = dict(self.event_queue[self.cursor])
        if fast:
            evt["_fast"] = True
        self.cursor += 1
        phase = str(evt.get("phase") or "unknown")
        if phase in self.phase_list:
            new_index = self.phase_list.index(phase)
            if new_index != self.phase_index:
                self.phase_index = new_index
                self.sig_phase_changed.emit(phase, new_index)
        self.sig_event.emit(evt)
        self.sig_cursor_changed.emit(self.cursor, len(self.event_queue))
        self._log(f"Playback: step cursor={self.cursor}/{len(self.event_queue)} phase={phase}.")
        self._apply_pending_snapshot_if_ready()
        return True

    def goto_phase(self, phase_idx: int) -> None:
        if phase_idx < 0 or phase_idx >= len(self.phase_list):
            return
        target_phase = self.phase_list[phase_idx]
        if phase_idx < self.phase_index and self.current_snapshot is not None:
            self._log("Playback: ресинк на snapshot перед перемоткой назад.")
            self.cursor = 0
            self.phase_index = 0
            self.sig_apply_snapshot.emit(self.current_snapshot)
        while self.cursor < len(self.event_queue):
            evt = self.event_queue[self.cursor]
            if str(evt.get("phase") or "unknown") == target_phase:
                break
            self.step_event(fast=True)
        self.phase_index = phase_idx
        self.sig_phase_changed.emit(target_phase, phase_idx)
        self.sig_cursor_changed.emit(self.cursor, len(self.event_queue))

    def next_phase(self) -> None:
        self.goto_phase(self.phase_index + 1)

    def prev_phase(self) -> None:
        self.goto_phase(self.phase_index - 1)

    def set_speed(self, mult: float) -> None:
        self._speed = max(0.1, float(mult))
        self._log(f"Playback: скорость {self._speed:.2f}x.")

    @property
    def speed(self) -> float:
        return self._speed
