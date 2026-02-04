from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from PySide6 import QtCore

from viewer.opengl_view import OpenGLBoardWidget


@dataclass
class PhaseStep:
    phase: str
    unit_id: int
    action: str
    from_xy: Optional[Tuple[float, float]] = None
    to_xy: Optional[Tuple[float, float]] = None


class PhasePlaybackController(QtCore.QObject):
    PHASES = ["command", "move", "shoot", "charge", "fight"]

    def __init__(
        self,
        board: OpenGLBoardWidget,
        *,
        on_hint: Optional[Callable[[str], None]] = None,
        logger: Optional[Callable[[str], None]] = None,
        focus_ms: int = 250,
        move_ms: int = 600,
    ) -> None:
        super().__init__(board)
        self._board = board
        self._on_hint = on_hint
        self._logger = logger
        self._focus_ms = focus_ms
        self._move_ms = move_ms
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._advance_step)

        self._state = "IDLE"
        self._phase_index = 0
        self._step_index = 0
        self._steps_by_phase: Dict[str, List[PhaseStep]] = {}
        self._prev_enemy_state: Optional[dict] = None
        self._next_enemy_state: Optional[dict] = None
        self._diff_moves: Dict[int, Tuple[Tuple[float, float], Tuple[float, float]]] = {}
        self._last_active: Optional[str] = None
        self._debug = bool(os.getenv("VIEW_PHASEPLAY_DEBUG"))

    def should_suppress_auto_animation(self, state: dict) -> bool:
        if self._state in ("PLAYING_PHASE", "WAIT_ENTER"):
            return True
        active = state.get("active")
        return self._is_enemy(self._last_active) and not self._is_enemy(active)

    def on_state_applied(self, state: dict) -> None:
        active = state.get("active")
        if self._is_enemy(active) and not self._is_enemy(self._last_active):
            self._on_enemy_start(state)
        elif self._is_enemy(self._last_active) and not self._is_enemy(active):
            self._on_enemy_end(state)
        self._last_active = active

    def is_overriding_context(self) -> bool:
        return self._state in ("PLAYING_PHASE", "WAIT_ENTER")

    def on_enter(self) -> None:
        if self._board.is_animating():
            self._log("Enter: принудительное завершение анимации.")
            self._board.finish_animation()
            return
        self._log("Enter: обработка.")
        if self._state != "WAIT_ENTER":
            return
        self._set_hint("")
        self._phase_index += 1
        if self._phase_index >= len(self.PHASES):
            self._finish()
            return
        self._state = "PLAYING_PHASE"
        self._start_phase(self.PHASES[self._phase_index])

    def _on_enemy_start(self, state: dict) -> None:
        self._reset()
        self._prev_enemy_state = self._snapshot_enemy_state(state)
        self._log("Начало хода модели: сохранено предыдущее состояние.")

    def _on_enemy_end(self, state: dict) -> None:
        if not self._prev_enemy_state:
            self._prev_enemy_state = self._snapshot_enemy_state(state)
        self._next_enemy_state = self._snapshot_enemy_state(state)
        self._diff_moves = self._build_diff_moves(self._prev_enemy_state, self._next_enemy_state)
        self._log(f"Конец хода модели: diff_moves={len(self._diff_moves)}.")
        self._steps_by_phase = self._build_steps(self._next_enemy_state, self._diff_moves)
        self._phase_index = 0
        self._step_index = 0
        self._state = "PLAYING_PHASE"
        self._board.set_phase_playback_enabled(True)
        self._start_phase(self.PHASES[self._phase_index])

    def _start_phase(self, phase: str) -> None:
        self._log(f"Старт фазы: {phase}.")
        self._board.set_active_phase(phase)
        self._step_index = 0
        self._set_hint("")
        self._advance_step()

    def _advance_step(self) -> None:
        if self._state != "PLAYING_PHASE":
            return
        phase = self.PHASES[self._phase_index]
        steps = self._steps_by_phase.get(phase, [])
        if self._step_index >= len(steps):
            self._enter_wait()
            return
        step = steps[self._step_index]
        self._step_index += 1
        if step.action == "focus":
            self._log(f"Шаг: focus unit_id={step.unit_id}.")
            self._board.set_active_phase(step.phase)
            self._board.set_active_unit(step.unit_id)
            self._schedule(self._focus_ms)
        elif step.action == "move":
            self._log(
                f"Шаг: move unit_id={step.unit_id} from={step.from_xy} to={step.to_xy}."
            )
            if step.from_xy and step.to_xy:
                self._board.play_move(step.unit_id, step.from_xy, step.to_xy, self._move_ms)
            self._schedule(self._move_ms)
        else:
            self._schedule(self._focus_ms)

    def _enter_wait(self) -> None:
        self._state = "WAIT_ENTER"
        self._set_hint("Нажми Enter для следующей фазы.")
        self._log("Переход в WAIT_ENTER.")

    def _finish(self) -> None:
        self._state = "DONE"
        self._set_hint("")
        self._board.set_active_unit(None)
        self._board.set_active_phase(None)
        self._board.set_phase_playback_enabled(False)
        self._log("Демонстрация фаз завершена.")

    def _reset(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
        self._state = "IDLE"
        self._phase_index = 0
        self._step_index = 0
        self._steps_by_phase = {}
        self._diff_moves = {}
        self._prev_enemy_state = None
        self._next_enemy_state = None
        self._set_hint("")
        self._board.set_active_unit(None)
        self._board.set_active_phase(None)
        self._board.set_phase_playback_enabled(False)

    def _schedule(self, delay_ms: int) -> None:
        if delay_ms <= 0:
            self._advance_step()
            return
        if self._timer.isActive():
            self._timer.stop()
        self._timer.start(delay_ms)

    def _set_hint(self, text: str) -> None:
        if self._on_hint:
            self._on_hint(text)

    def _log(self, message: str) -> None:
        if self._debug and self._logger:
            self._logger(f"[PHASEPLAY] {message}")

    @staticmethod
    def _is_enemy(side: Optional[str]) -> bool:
        return side in ("enemy", "model")

    @classmethod
    def _snapshot_enemy_state(cls, state: dict) -> dict:
        units = []
        for unit in state.get("units", []) or []:
            if not cls._is_enemy(unit.get("side")):
                continue
            units.append(
                {
                    "id": unit.get("id"),
                    "x": unit.get("x"),
                    "y": unit.get("y"),
                    "side": unit.get("side"),
                }
            )
        return {
            "round": state.get("round"),
            "turn": state.get("turn"),
            "units": units,
        }

    @staticmethod
    def _build_diff_moves(
        prev_state: dict, next_state: dict
    ) -> Dict[int, Tuple[Tuple[float, float], Tuple[float, float]]]:
        prev_units = {
            unit.get("id"): (unit.get("x"), unit.get("y"))
            for unit in prev_state.get("units", []) or []
            if unit.get("id") is not None
        }
        next_units = {
            unit.get("id"): (unit.get("x"), unit.get("y"))
            for unit in next_state.get("units", []) or []
            if unit.get("id") is not None
        }
        diff_moves: Dict[int, Tuple[Tuple[float, float], Tuple[float, float]]] = {}
        for unit_id, to_pos in next_units.items():
            from_pos = prev_units.get(unit_id)
            if from_pos is None or to_pos is None:
                continue
            if from_pos != to_pos:
                diff_moves[unit_id] = (from_pos, to_pos)
        return diff_moves

    @classmethod
    def _build_steps(
        cls,
        next_state: dict,
        diff_moves: Dict[int, Tuple[Tuple[float, float], Tuple[float, float]]],
    ) -> Dict[str, List[PhaseStep]]:
        unit_ids = sorted(
            {
                unit.get("id")
                for unit in next_state.get("units", []) or []
                if unit.get("id") is not None
            }
        )
        steps_by_phase: Dict[str, List[PhaseStep]] = {phase: [] for phase in cls.PHASES}
        for phase in cls.PHASES:
            for unit_id in unit_ids:
                steps_by_phase[phase].append(
                    PhaseStep(phase=phase, unit_id=unit_id, action="focus")
                )
                if phase == "move" and unit_id in diff_moves:
                    from_xy, to_xy = diff_moves[unit_id]
                    steps_by_phase[phase].append(
                        PhaseStep(
                            phase=phase,
                            unit_id=unit_id,
                            action="move",
                            from_xy=from_xy,
                            to_xy=to_xy,
                        )
                    )
        return steps_by_phase
