from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


EventDict = Dict[str, Any]


@dataclass
class ReplayRecorder:
    emit_fn: Optional[Callable[[EventDict], None]] = None
    debug_log_fn: Optional[Callable[[str], None]] = None
    side: Optional[str] = None
    battle_round: Optional[int] = None
    turn: Optional[int] = None
    _t: int = 0
    events: List[EventDict] = field(default_factory=list)

    def start_turn(self, side: str, battle_round: int, turn: int) -> None:
        self.side = side
        self.battle_round = battle_round
        self.turn = turn
        self._t = 0
        self.events.clear()

    def emit(self, event: EventDict) -> None:
        if self.side is None:
            return
        event = dict(event)
        event.setdefault("side", self.side)
        event.setdefault("battle_round", self.battle_round)
        event.setdefault("turn", self.turn)
        event.setdefault("t", self._t)
        self._t += 1
        self.events.append(event)
        if self.emit_fn is not None:
            self.emit_fn(event)
        if self.debug_log_fn is not None:
            self.debug_log_fn(
                "[REPLAY] "
                f"type={event.get('type')} phase={event.get('phase')} "
                f"unit_id={event.get('unit_id')} t={event.get('t')}"
            )

    def start_phase(self, phase: str) -> None:
        self.emit({
            "type": "phase_start",
            "phase": phase,
            "unit_id": None,
            "unit_name": None,
            "duration_ms": 0,
        })

    def end_phase(self, phase: str, state_snapshot: Optional[Dict[str, Any]] = None) -> None:
        event = {
            "type": "phase_end",
            "phase": phase,
            "unit_id": None,
            "unit_name": None,
            "duration_ms": 0,
        }
        if state_snapshot is not None:
            event["state_snapshot"] = state_snapshot
        self.emit(event)

    def end_turn(self, state_snapshot: Optional[Dict[str, Any]] = None) -> None:
        event = {
            "type": "turn_end",
            "phase": None,
            "unit_id": None,
            "unit_name": None,
            "duration_ms": 0,
        }
        if state_snapshot is not None:
            event["state_snapshot"] = state_snapshot
        self.emit(event)
