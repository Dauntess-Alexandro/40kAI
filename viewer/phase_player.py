from __future__ import annotations

import copy
from collections import deque
from dataclasses import dataclass
import time
from typing import Callable, Deque, Dict, Optional, Tuple

from PySide6 import QtCore


@dataclass(frozen=True)
class StateFingerprint:
    round_id: Optional[int]
    turn_id: Optional[int]
    phase: Optional[str]
    active: Optional[str]
    units: Tuple[Tuple, ...]


class PhasePlayer(QtCore.QObject):
    def __init__(
        self,
        apply_state: Callable[[Dict], None],
        *,
        is_animating: Callable[[], bool],
        min_delay_ms: int = 120,
        phase_delay_ms: int = 260,
        poll_ms: int = 30,
    ) -> None:
        super().__init__()
        self._apply_state = apply_state
        self._is_animating = is_animating
        self._min_delay_ms = max(0, int(min_delay_ms))
        self._phase_delay_ms = max(0, int(phase_delay_ms))
        self._poll_ms = max(10, int(poll_ms))
        self._queue: Deque[Dict] = deque()
        self._active = False
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._tick)
        self._last_fingerprint: Optional[StateFingerprint] = None
        self._last_context: Optional[Tuple[Optional[int], Optional[int], Optional[str], Optional[str]]] = None
        self._apply_started_at: Optional[float] = None
        self._pending_delay_ms: int = self._min_delay_ms

    def enqueue(self, state: Dict) -> None:
        snapshot = copy.deepcopy(state)
        fingerprint = self._fingerprint(snapshot)
        if fingerprint == self._last_fingerprint:
            return
        self._queue.append(snapshot)
        if not self._active:
            self._active = True
            self._tick()

    def _tick(self) -> None:
        if self._apply_started_at is not None:
            if self._is_animating():
                self._timer.start(self._poll_ms)
                return
            elapsed_ms = (time.monotonic() - self._apply_started_at) * 1000
            if elapsed_ms < self._pending_delay_ms:
                self._timer.start(self._poll_ms)
                return
            self._apply_started_at = None

        if not self._queue:
            self._active = False
            return

        state = self._queue.popleft()
        self._apply_state(state)
        self._last_fingerprint = self._fingerprint(state)
        self._pending_delay_ms = self._compute_delay_ms(state)
        self._apply_started_at = time.monotonic()
        self._timer.start(self._poll_ms)

    def _compute_delay_ms(self, state: Dict) -> int:
        phase = state.get("phase")
        active = state.get("active") or state.get("active_side")
        round_id = state.get("round")
        turn_id = state.get("turn")
        context = (round_id, turn_id, str(phase) if phase is not None else None, active)
        delay = self._min_delay_ms
        if self._last_context is not None and context != self._last_context:
            delay = max(delay, self._phase_delay_ms)
        self._last_context = context
        return delay

    def _fingerprint(self, state: Dict) -> StateFingerprint:
        round_id = state.get("round")
        turn_id = state.get("turn")
        phase = state.get("phase")
        active = state.get("active") or state.get("active_side")
        units = []
        for unit in state.get("units", []) or []:
            units.append(
                (
                    unit.get("side"),
                    unit.get("id"),
                    unit.get("x"),
                    unit.get("y"),
                    unit.get("hp"),
                    unit.get("models"),
                )
            )
        return StateFingerprint(
            round_id=round_id,
            turn_id=turn_id,
            phase=str(phase) if phase is not None else None,
            active=active,
            units=tuple(units),
        )
