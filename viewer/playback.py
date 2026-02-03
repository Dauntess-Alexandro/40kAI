from __future__ import annotations

from typing import Callable, List, Optional

from PySide6 import QtCore


class PlaybackController(QtCore.QObject):
    def __init__(
        self,
        board,
        log_fn: Callable[[str], None],
        *,
        debug: bool = False,
        parent: Optional[QtCore.QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._board = board
        self._log = log_fn
        self._debug = debug
        self._queue: List[dict] = []
        self._waiting_for_enter = False
        self._current_phase: Optional[str] = None
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._process_next_event)

    def add_events(self, events: List[dict]) -> None:
        if not events:
            return
        for event in events:
            if not isinstance(event, dict):
                continue
            self._queue.append(event)
            if self._debug:
                self._log(f"[PRESENT][DEBUG] Получено событие: {event}")
        if not self._waiting_for_enter and not self._timer.isActive():
            self._process_next_event()

    def handle_enter(self) -> bool:
        if self._board.is_animating():
            self._board.finish_animation()
            if self._debug:
                self._log("[PRESENT][DEBUG] Enter: завершили текущую анимацию.")
            return True
        if self._waiting_for_enter:
            self._waiting_for_enter = False
            if self._debug:
                self._log("[PRESENT][DEBUG] Enter: продолжаем следующую фазу.")
            self._process_next_event()
            return True
        return False

    def _process_next_event(self) -> None:
        if self._waiting_for_enter:
            return
        if not self._queue:
            return
        event = self._queue.pop(0)
        event_type = str(event.get("type") or "")
        duration_ms = int(event.get("duration_ms") or 0)
        if event_type == "phase_start":
            self._current_phase = event.get("phase")
            self._board.set_active_phase(self._current_phase)
            self._schedule_next(duration_ms or 100)
            return
        if event_type == "phase_end":
            self._waiting_for_enter = True
            if self._debug:
                phase = event.get("phase") or self._current_phase
                self._log(f"[PRESENT][DEBUG] Ожидание Enter для фазы: {phase}.")
            return
        if event_type == "unit_focus":
            self._apply_unit_focus(event)
            self._schedule_next(duration_ms or 200)
            return
        if event_type == "unit_move":
            self._apply_unit_focus(event)
            self._apply_move(event, duration_ms or 600)
            self._schedule_next(duration_ms or 600)
            return
        if event_type in {"unit_shoot", "unit_charge", "unit_fight"}:
            self._apply_unit_focus(event)
            self._schedule_next(duration_ms or 300)
            return
        if event_type == "turn_end":
            self._board.set_active_unit(None, None)
            self._board.set_active_phase(None)
            self._schedule_next(duration_ms or 0)
            return
        self._schedule_next(duration_ms or 0)

    def _apply_unit_focus(self, event: dict) -> None:
        side = event.get("side") or "model"
        unit_id = event.get("unit_id")
        phase = event.get("phase") or self._current_phase
        self._board.set_active_phase(phase)
        if unit_id is not None:
            self._board.set_active_unit(side, unit_id)

    def _apply_move(self, event: dict, duration_ms: int) -> None:
        side = event.get("side") or "model"
        unit_id = event.get("unit_id")
        if unit_id is None:
            return
        from_pos = event.get("from")
        to_pos = event.get("to")
        self._board.play_move(side, unit_id, from_pos, to_pos, duration_ms)

    def _schedule_next(self, duration_ms: int) -> None:
        if duration_ms <= 0:
            self._process_next_event()
            return
        self._timer.start(duration_ms)
