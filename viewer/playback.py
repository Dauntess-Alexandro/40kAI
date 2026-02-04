from __future__ import annotations

import os
import re
from typing import Callable, Dict, List, Optional, Tuple

from PySide6 import QtCore


class PlaybackController(QtCore.QObject):
    STATE_IDLE = "idle"
    STATE_PLAYING_PHASE = "playing_phase"
    STATE_WAIT_ENTER = "wait_enter"
    STATE_DONE = "done"

    def __init__(self, board, status_callback: Optional[Callable[[str], None]] = None):
        super().__init__(board)
        self._board = board
        self._status_callback = status_callback
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._play_next_event_in_phase)
        self._debug = os.getenv("VIEW_PLAYBACK_DEBUG", "").strip() == "1"
        self._move_before_re = re.compile(
            r"Позиция до:\s*\((?P<x>-?\d+),\s*(?P<y>-?\d+)\)"
        )
        self._move_after_re = re.compile(
            r"Позиция после:\s*\((?P<x>-?\d+),\s*(?P<y>-?\d+)\)"
        )

        self.events: List[Dict] = []
        self._events_by_phase: Dict[str, List[Dict]] = {}
        self._phase_index = 0
        self.idx = 0
        self.current_phase = ""
        self.phase_order = ["command", "move", "shoot", "charge", "fight"]
        self.state = self.STATE_IDLE
        self._pending_move_from: Dict[int, Tuple[float, float]] = {}

    def reset(self) -> None:
        self._log_debug("reset")
        self._timer.stop()
        self.events = []
        self._events_by_phase = {}
        self._phase_index = 0
        self.idx = 0
        self.current_phase = ""
        self.state = self.STATE_IDLE
        self._pending_move_from = {}
        self._board.clear_playback_context()
        self._board.set_active_phase(None)
        self._set_status("")

    def start(self, events: List[Dict]) -> None:
        if not events:
            return
        self.events = list(events)
        self._events_by_phase = self._split_events(events)
        self._phase_index = 0
        self._log_debug(f"start playback: events={len(events)}")
        self.start_phase(self.phase_order[0])

    def start_phase(self, phase: str) -> None:
        self.state = self.STATE_PLAYING_PHASE
        self.current_phase = phase
        self.idx = 0
        if phase == "move":
            self._pending_move_from = {}
        self._board.set_active_phase(phase)
        self._set_status(f"Идёт фаза {self._phase_label(phase)}…")
        self._log_debug(f"start_phase: {phase}")
        if not self._events_by_phase.get(phase):
            self._handle_phase_end()
            return
        self._play_next_event_in_phase()

    def _play_next_event_in_phase(self) -> None:
        if self.state != self.STATE_PLAYING_PHASE:
            return
        if self._board.is_animating():
            self._timer.start(50)
            return
        phase_events = self._events_by_phase.get(self.current_phase, [])
        if self.idx >= len(phase_events):
            self._handle_phase_end()
            return
        event = phase_events[self.idx]
        self.idx += 1
        event_type = str(event.get("type", "")).lower()
        self._log_debug(
            f"event: type={event_type}, phase={event.get('phase')}, unit={event.get('unit_id')}"
        )

        if event_type == "phase_start":
            self._timer.start(self._duration_ms(event, 120))
            return
        if event_type == "phase_end":
            self._handle_phase_end()
            return

        unit_id = self._extract_unit_id(event)
        unit_side = self._normalize_side(event.get("side"))
        if unit_id is not None and event_type in (
            "unit_start",
            "move",
            "shoot",
            "charge",
            "fight",
            "skip",
            "summary",
            "scan",
        ):
            self._board.set_active_unit(unit_id, unit_side)

        if event_type in ("unit_move", "move"):
            from_xy, to_xy = self._resolve_move_points(event, unit_id)
            duration_ms = self._duration_ms(event, 300)
            if unit_id is not None and from_xy and to_xy and from_xy != to_xy:
                self._board.play_move(unit_id, from_xy, to_xy, duration_ms, side=unit_side)
                self._timer.start(max(80, duration_ms))
                return
        self._timer.start(self._duration_ms(event, 220))

    def _handle_phase_end(self) -> None:
        self.state = self.STATE_WAIT_ENTER
        self._board.set_active_phase(self.current_phase)
        self._set_status(
            f"Фаза {self._phase_label(self.current_phase)} завершена. Нажмите Enter для продолжения."
        )
        self._log_debug(f"WAIT_ENTER: {self.current_phase}")

    def on_enter(self) -> bool:
        if self.state == self.STATE_PLAYING_PHASE:
            if self._board.is_animating():
                self._board.finish_animation()
                self._log_debug("enter: finish_animation (playing)")
                return True
            return False
        if self.state != self.STATE_WAIT_ENTER:
            return False
        if self._board.is_animating():
            self._board.finish_animation()
            self._log_debug("enter: finish_animation (wait_enter)")
            return True
        next_phase = self._next_phase()
        if next_phase is None:
            self.state = self.STATE_DONE
            self._board.clear_playback_context()
            self._board.set_active_phase(None)
            self._set_status("")
            self._log_debug("playback done")
            return True
        self.start_phase(next_phase)
        return True

    def is_active(self) -> bool:
        return self.state in (self.STATE_PLAYING_PHASE, self.STATE_WAIT_ENTER)

    def _split_events(self, events: List[Dict]) -> Dict[str, List[Dict]]:
        buckets: Dict[str, List[Dict]] = {phase: [] for phase in self.phase_order}
        for event in events:
            if not isinstance(event, dict):
                continue
            side = self._normalize_side(event.get("side"))
            if side not in (None, "model"):
                continue
            phase = self._normalize_phase(event.get("phase"))
            if not phase:
                continue
            if phase in buckets:
                buckets[phase].append(event)
        return buckets

    def _normalize_phase(self, phase: Optional[str]) -> Optional[str]:
        if not phase:
            return None
        lowered = str(phase).lower()
        if "command" in lowered or "ком" in lowered:
            return "command"
        if "move" in lowered or "движ" in lowered or "movement" in lowered:
            return "move"
        if "shoot" in lowered or "стрел" in lowered or "shooting" in lowered:
            return "shoot"
        if "charge" in lowered or "заряд" in lowered:
            return "charge"
        if "fight" in lowered or "бой" in lowered:
            return "fight"
        return None

    def _normalize_side(self, side: Optional[str]) -> Optional[str]:
        if not side:
            return None
        lowered = str(side).lower()
        if lowered == "enemy":
            return "model"
        return lowered

    def _next_phase(self) -> Optional[str]:
        if self.current_phase not in self.phase_order:
            return None
        idx = self.phase_order.index(self.current_phase) + 1
        if idx >= len(self.phase_order):
            return None
        return self.phase_order[idx]

    def _extract_unit_id(self, event: Dict) -> Optional[int]:
        for key in ("unit_id", "unit", "id"):
            value = event.get(key)
            if isinstance(value, int):
                return value
            if isinstance(value, str) and value.isdigit():
                return int(value)
        return None

    def _extract_move_points(
        self, event: Dict
    ) -> Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
        start = event.get("from") or event.get("start")
        end = event.get("to") or event.get("end")
        return self._parse_point(start), self._parse_point(end)

    def _resolve_move_points(
        self, event: Dict, unit_id: Optional[int]
    ) -> Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
        start, end = self._extract_move_points(event)
        if start and end:
            return start, end
        msg = str(event.get("msg") or "")
        before = self._move_before_re.search(msg)
        if before and unit_id is not None:
            self._pending_move_from[unit_id] = (
                float(before.group("x")),
                float(before.group("y")),
            )
        after = self._move_after_re.search(msg)
        if after and unit_id is not None:
            to_xy = (float(after.group("x")), float(after.group("y")))
            from_xy = self._pending_move_from.pop(unit_id, None)
            if from_xy is None:
                from_xy = to_xy
            return from_xy, to_xy
        return None, None

    def _parse_point(self, value) -> Optional[Tuple[float, float]]:
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return float(value[0]), float(value[1])
        if isinstance(value, dict):
            x = value.get("x")
            y = value.get("y")
            if x is not None and y is not None:
                return float(x), float(y)
        return None

    def _duration_ms(self, event: Dict, default: int) -> int:
        for key in ("duration_ms", "duration", "delay_ms"):
            value = event.get(key)
            if isinstance(value, (int, float)):
                return max(50, int(value))
        return default

    def _phase_label(self, phase: str) -> str:
        labels = {
            "command": "КОМАНДА",
            "move": "ДВИЖЕНИЕ",
            "shoot": "СТРЕЛЬБА",
            "charge": "ЗАРЯД",
            "fight": "БОЙ",
        }
        return labels.get(phase, phase)

    def _set_status(self, text: str) -> None:
        if self._status_callback:
            self._status_callback(text)

    def _log_debug(self, message: str) -> None:
        if self._debug:
            print(f"[VIEWER PLAYBACK] {message}")
