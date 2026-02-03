from __future__ import annotations

import os
from typing import Callable, Dict, List, Optional

from PySide6 import QtCore


class PlaybackController(QtCore.QObject):
    def __init__(
        self,
        map_scene,
        apply_state_fn: Callable[[Dict], None],
        prompt_label=None,
        log_fn: Optional[Callable[[str], None]] = None,
    ):
        super().__init__()
        self._enabled = os.getenv("PRESENT_AI", "0") == "1"
        self._debug = os.getenv("PRESENT_AI_DEBUG", "0") == "1"
        self._map_scene = map_scene
        self._apply_state_fn = apply_state_fn
        self._prompt_label = prompt_label
        self._log_fn = log_fn
        self._phase_order = ["command", "move", "shoot", "charge", "fight"]
        self._pending_turns: List[List[Dict]] = []
        self._collecting: List[Dict] = []
        self._phase_events: Dict[str, List[Dict]] = {}
        self._current_phase = None
        self._phase_index = 0
        self._event_index = 0
        self._state = "idle"
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._play_next_event)
        self._update_prompt(False)

    def add_events(self, events: List[Dict]) -> None:
        if not self._enabled or not events:
            return
        for event in events:
            self._collecting.append(event)
            if event.get("type") == "turn_end":
                self._pending_turns.append(list(self._collecting))
                self._collecting.clear()
        if self._state in ("idle", "done"):
            self._start_next_turn()

    def is_active(self) -> bool:
        return self._state not in ("idle", "done") and self._enabled

    def block_state_updates(self) -> bool:
        return self.is_active()

    def on_enter(self) -> bool:
        if not self._enabled:
            return False
        if self._map_scene.is_animating():
            if self._debug:
                self._log("[REPLAY] Enter: finish animation")
            self._map_scene.finish_animation()
            return True
        if self._state == "waiting_enter":
            if self._debug:
                self._log("[REPLAY] Enter: next phase")
            self._advance_phase()
            return True
        return False

    def _start_next_turn(self) -> None:
        if not self._pending_turns:
            self._state = "idle"
            self._update_prompt(False)
            return
        events = self._pending_turns.pop(0)
        self._phase_events = {phase: [] for phase in self._phase_order}
        for event in events:
            phase = event.get("phase")
            if phase in self._phase_events:
                self._phase_events[phase].append(event)
        self._phase_index = 0
        self._state = "playing_phase"
        self._advance_phase()

    def _advance_phase(self) -> None:
        if self._phase_index >= len(self._phase_order):
            self._state = "done"
            self._update_prompt(False)
            if self._pending_turns:
                self._start_next_turn()
            return
        phase = self._phase_order[self._phase_index]
        self._current_phase = phase
        self._event_index = 0
        self._map_scene.set_active_phase(phase)
        self._update_prompt(False)
        self._state = "playing_phase"
        self._play_next_event()

    def _play_next_event(self) -> None:
        if self._state != "playing_phase":
            return
        events = self._phase_events.get(self._current_phase, [])
        if self._event_index >= len(events):
            self._state = "waiting_enter"
            self._update_prompt(True)
            if self._debug:
                self._log(f"[REPLAY] waiting_enter phase={self._current_phase}")
            return
        event = events[self._event_index]
        self._event_index += 1
        delay = int(event.get("duration_ms") or 0)
        self._apply_event(event)
        if event.get("type") == "phase_end":
            self._state = "waiting_enter"
            self._update_prompt(True)
            return
        delay = max(0, delay)
        if delay == 0:
            self._play_next_event()
            return
        self._timer.start(delay)

    def _apply_event(self, event: Dict) -> None:
        event_type = event.get("type")
        unit_id = event.get("unit_id")
        side = event.get("side")
        if self._debug:
            self._log(
                "[REPLAY] "
                f"type={event_type} phase={event.get('phase')} unit_id={unit_id} t={event.get('t')}"
            )
        if event_type == "phase_start":
            self._map_scene.set_active_phase(event.get("phase"))
        elif event_type == "unit_focus":
            self._map_scene.set_active_unit(unit_id, side=side)
        elif event_type == "unit_move":
            self._map_scene.set_active_unit(unit_id, side=side)
            from_xy = event.get("from") or []
            to_xy = event.get("to") or []
            self._map_scene.play_move(
                unit_id,
                from_xy,
                to_xy,
                duration_ms=int(event.get("duration_ms") or 600),
                side=side,
            )
        elif event_type in ("unit_shoot", "unit_charge", "unit_fight"):
            self._map_scene.set_active_unit(unit_id, side=side)
            target_id = event.get("target_id")
            self._map_scene.play_effect(
                event_type,
                attacker_id=unit_id,
                target_id=target_id,
                duration_ms=int(event.get("duration_ms") or 450),
            )
        if "state_snapshot" in event:
            snapshot = event.get("state_snapshot")
            if isinstance(snapshot, dict):
                self._apply_state_fn(snapshot)

    def _update_prompt(self, visible: bool) -> None:
        if self._prompt_label is None:
            return
        if visible:
            self._prompt_label.setText("Нажмите Enter для следующей фазы")
        self._prompt_label.setVisible(bool(visible))

    def _log(self, message: str) -> None:
        if self._log_fn is not None:
            self._log_fn(message)
