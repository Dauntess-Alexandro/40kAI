from __future__ import annotations

from dataclasses import dataclass
import json
import re
from collections import deque
from typing import Deque, Dict, Iterable, List, Optional, Set, Tuple

from PySide6 import QtCore

from viewer.model_log_tree import (
    MOVE_AFTER_RE,
    MOVE_BEFORE_RE,
    PHASE_LABELS,
    _is_action_msg,
    _is_skip_msg,
)

PHASE_KEYWORDS = {
    "command": ("команд", "command"),
    "movement": ("движ", "movement"),
    "shooting": ("стрел", "shoot"),
    "charge": ("чардж", "charge"),
    "fight": ("бой", "fight"),
}

UNIT_ID_RE = re.compile(r"\bUnit\s+(\d+)")
PHASE_LINE_RE = re.compile(r"ФАЗА\s+([А-ЯA-Z\s]+)", re.IGNORECASE)
ROUND_END_RE = re.compile(r"конец боевого раунда\s*(\d+)", re.IGNORECASE)


@dataclass(frozen=True)
class TimelineEvent:
    kind: str
    phase: Optional[str] = None
    round_id: Optional[int] = None
    unit_id: Optional[int] = None
    unit_name: Optional[str] = None
    message: Optional[str] = None
    from_cell: Optional[Tuple[int, int]] = None
    to_cell: Optional[Tuple[int, int]] = None
    duration_ms: Optional[int] = None

    def key(self) -> Tuple:
        return (
            self.kind,
            self.phase,
            self.round_id,
            self.unit_id,
            self.message,
            self.from_cell,
            self.to_cell,
        )


class TimelineBuilder:
    def __init__(self) -> None:
        self._seen_model_events: Set[str] = set()
        self._seen_log_lines: Set[str] = set()
        self._last_phase_key: Optional[Tuple[int, str]] = None
        self._phase_units: Set[int] = set()
        self._action_seen: Set[Tuple[int, str, int, str]] = set()
        self._move_cache: Dict[Tuple[int, str, int], Dict[str, Tuple[int, int]]] = {}
        self._log_phase: Optional[str] = None
        self._log_round_id: Optional[int] = None
        self._log_move_cache: Dict[int, Dict[str, Tuple[int, int]]] = {}

    def reset_log_cache(self) -> None:
        self._seen_log_lines.clear()
        self._log_phase = None
        self._log_round_id = None
        self._log_move_cache.clear()

    def ingest_model_events(self, events: Iterable[dict]) -> List[TimelineEvent]:
        new_events: List[TimelineEvent] = []
        for event in events:
            if not isinstance(event, dict):
                continue
            signature = self._event_signature(event)
            if signature in self._seen_model_events:
                continue
            self._seen_model_events.add(signature)
            round_id = event.get("battle_round")
            if round_id is None:
                continue
            try:
                round_id = int(round_id)
            except (TypeError, ValueError):
                continue
            phase = str(event.get("phase") or "unknown").lower()
            phase_key = (round_id, phase)
            if self._last_phase_key != phase_key:
                self._last_phase_key = phase_key
                self._phase_units = set()
                self._action_seen = set()
                new_events.append(
                    TimelineEvent(
                        kind="phase_start",
                        phase=phase,
                        round_id=round_id,
                        message=_phase_label(phase, round_id),
                        duration_ms=900,
                    )
                )
            unit_id = event.get("unit_id")
            unit_name = event.get("unit_name")
            unit_id = _safe_unit_id(unit_id)
            if unit_id is not None and unit_id not in self._phase_units:
                self._phase_units.add(unit_id)
                new_events.append(
                    TimelineEvent(
                        kind="unit_start",
                        phase=phase,
                        round_id=round_id,
                        unit_id=unit_id,
                        unit_name=unit_name,
                        duration_ms=450,
                    )
                )
            msg = str(event.get("msg") or "")
            if phase == "movement" and unit_id is not None:
                self._capture_move(new_events, round_id, phase, unit_id, msg)
            if unit_id is not None and ("shooting" == phase or "charge" == phase or "fight" == phase):
                if _is_action_msg(phase, msg) or _is_skip_msg(msg):
                    action_key = (round_id, phase, unit_id, msg)
                    if action_key not in self._action_seen:
                        self._action_seen.add(action_key)
                        new_events.append(
                            TimelineEvent(
                                kind="action",
                                phase=phase,
                                round_id=round_id,
                                unit_id=unit_id,
                                unit_name=unit_name,
                                message=msg,
                                duration_ms=1200 if phase == "shooting" else 800,
                            )
                        )
            if str(event.get("type") or "") == "phase_end":
                new_events.append(
                    TimelineEvent(
                        kind="phase_end",
                        phase=phase,
                        round_id=round_id,
                        message=_phase_label(phase, round_id),
                        duration_ms=400,
                    )
                )
            if ROUND_END_RE.search(msg):
                new_events.append(
                    TimelineEvent(
                        kind="round_end",
                        round_id=round_id,
                        message=msg,
                        duration_ms=800,
                    )
                )
        return new_events

    def ingest_log_lines(self, lines: Iterable[str], round_id: Optional[int]) -> List[TimelineEvent]:
        new_events: List[TimelineEvent] = []
        if round_id is not None:
            self._log_round_id = round_id
        for line in lines:
            raw = str(line)
            signature = raw.strip()
            if signature in self._seen_log_lines:
                continue
            self._seen_log_lines.add(signature)
            phase = _parse_phase_line(raw)
            if phase:
                self._log_phase = phase
                new_events.append(
                    TimelineEvent(
                        kind="phase_start",
                        phase=phase,
                        round_id=self._log_round_id,
                        message=_phase_label(phase, self._log_round_id),
                        duration_ms=900,
                    )
                )
                continue
            if ROUND_END_RE.search(raw):
                new_events.append(
                    TimelineEvent(
                        kind="round_end",
                        round_id=self._log_round_id,
                        message=raw,
                        duration_ms=800,
                    )
                )
                continue
            unit_id = _safe_unit_id(_extract_unit_id(raw))
            if unit_id is None:
                continue
            if self._log_phase == "movement":
                self._capture_log_move(new_events, unit_id, raw)
            if self._log_phase in ("shooting", "charge", "fight"):
                if _is_action_msg(self._log_phase, raw) or _is_skip_msg(raw):
                    new_events.append(
                        TimelineEvent(
                            kind="action",
                            phase=self._log_phase,
                            round_id=self._log_round_id,
                            unit_id=unit_id,
                            message=raw,
                            duration_ms=1200 if self._log_phase == "shooting" else 800,
                        )
                    )
        return new_events

    def _capture_move(
        self,
        new_events: List[TimelineEvent],
        round_id: int,
        phase: str,
        unit_id: int,
        msg: str,
    ) -> None:
        key = (round_id, phase, unit_id)
        data = self._move_cache.setdefault(key, {})
        before = MOVE_BEFORE_RE.search(msg)
        if before:
            data["from"] = (int(before.group("x")), int(before.group("y")))
        after = MOVE_AFTER_RE.search(msg)
        if after:
            data["to"] = (int(after.group("x")), int(after.group("y")))
        if "from" in data and "to" in data:
            distance = _manhattan(data["from"], data["to"])
            new_events.append(
                TimelineEvent(
                    kind="move",
                    phase=phase,
                    round_id=round_id,
                    unit_id=unit_id,
                    from_cell=data["from"],
                    to_cell=data["to"],
                    duration_ms=_move_duration(distance),
                )
            )
            self._move_cache.pop(key, None)

    def _capture_log_move(self, new_events: List[TimelineEvent], unit_id: int, msg: str) -> None:
        data = self._log_move_cache.setdefault(unit_id, {})
        before = MOVE_BEFORE_RE.search(msg)
        if before:
            data["from"] = (int(before.group("x")), int(before.group("y")))
        after = MOVE_AFTER_RE.search(msg)
        if after:
            data["to"] = (int(after.group("x")), int(after.group("y")))
        if "from" in data and "to" in data:
            distance = _manhattan(data["from"], data["to"])
            new_events.append(
                TimelineEvent(
                    kind="move",
                    phase=self._log_phase,
                    round_id=self._log_round_id,
                    unit_id=unit_id,
                    from_cell=data["from"],
                    to_cell=data["to"],
                    duration_ms=_move_duration(distance),
                )
            )
            self._log_move_cache.pop(unit_id, None)

    def _event_signature(self, event: dict) -> str:
        try:
            return json.dumps(event, sort_keys=True, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(event)


class TimelinePlayer(QtCore.QObject):
    event_started = QtCore.Signal(object)
    event_finished = QtCore.Signal(object)
    queue_changed = QtCore.Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self._queue: Deque[TimelineEvent] = deque()
        self._seen_keys: Set[Tuple] = set()
        self._enabled = False
        self._auto_play = True
        self._step_mode = False
        self._speed = 1.0
        self._current: Optional[TimelineEvent] = None
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._finish_timer_event)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def step_mode(self) -> bool:
        return self._step_mode

    @property
    def current_event(self) -> Optional[TimelineEvent]:
        return self._current

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)
        if not self._enabled:
            self._timer.stop()
            self._current = None
        elif self._auto_play and self._current is None:
            self._advance()

    def set_auto_play(self, enabled: bool) -> None:
        self._auto_play = bool(enabled)
        if self._auto_play and self._enabled and self._current is None:
            self._advance()

    def set_step_mode(self, enabled: bool) -> None:
        self._step_mode = bool(enabled)
        if self._step_mode:
            self._auto_play = False
            self._timer.stop()
        elif self._auto_play and self._enabled and self._current is None:
            self._advance()

    def set_speed(self, speed: float) -> None:
        if speed <= 0:
            return
        self._speed = speed

    def enqueue(self, events: Iterable[TimelineEvent]) -> None:
        added = 0
        for event in events:
            key = event.key()
            if key in self._seen_keys:
                continue
            self._seen_keys.add(key)
            self._queue.append(event)
            added += 1
        if added:
            self.queue_changed.emit(len(self._queue))
        if self._enabled and self._auto_play and self._current is None:
            self._advance()

    def clear(self) -> None:
        self._queue.clear()
        self._seen_keys.clear()
        self._current = None
        self._timer.stop()
        self.queue_changed.emit(0)

    def next_event(self) -> None:
        if not self._enabled:
            return
        if self._current is None:
            self._advance()

    def complete_current(self) -> None:
        if self._current is None:
            return
        finished = self._current
        self._current = None
        self.event_finished.emit(finished)
        if self._enabled and self._auto_play and not self._step_mode:
            self._advance()

    def _advance(self) -> None:
        if not self._enabled:
            return
        if not self._queue:
            return
        self._current = self._queue.popleft()
        self.queue_changed.emit(len(self._queue))
        self.event_started.emit(self._current)
        if self._current.kind == "move":
            return
        delay = int((self._current.duration_ms or 0) / max(self._speed, 0.1))
        if delay <= 0:
            self.complete_current()
            return
        self._timer.start(delay)

    def _finish_timer_event(self) -> None:
        self.complete_current()


def _extract_unit_id(text: str) -> Optional[int]:
    match = UNIT_ID_RE.search(text)
    if not match:
        return None
    return _safe_unit_id(match.group(1))


def _safe_unit_id(value: Optional[object]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_phase_line(line: str) -> Optional[str]:
    match = PHASE_LINE_RE.search(line)
    if not match:
        return None
    label = match.group(1).lower()
    for phase, tokens in PHASE_KEYWORDS.items():
        if any(token in label for token in tokens):
            return phase
    return None


def _phase_label(phase: Optional[str], round_id: Optional[int]) -> str:
    if not phase:
        return "ФАЗА НЕИЗВЕСТНА"
    label = PHASE_LABELS.get(phase, f"ФАЗА {phase.upper()}")
    if round_id is None:
        return label
    return f"{label} (Раунд {round_id})"


def _manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _move_duration(distance: int) -> int:
    base = 350
    per_cell = 140
    return min(2000, base + per_cell * max(distance, 0))
