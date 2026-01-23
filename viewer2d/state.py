from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import json
import os


@dataclass
class Unit:
    side: str
    unit_id: int
    name: str
    hp: Optional[int]
    models: Optional[int]
    x: int
    y: int


@dataclass
class Objective:
    x: int
    y: int


@dataclass
class GameState:
    width: int
    height: int
    turn: int = 0
    round: int = 0
    phase: str = ""
    active: str = ""
    vp_model: int = 0
    vp_player: int = 0
    cp_model: int = 0
    cp_player: int = 0
    units: List[Unit] = field(default_factory=list)
    objectives: List[Objective] = field(default_factory=list)
    log_tail: List[str] = field(default_factory=list)
    source: str = ""


DEFAULT_WIDTH = 60
DEFAULT_HEIGHT = 40


def load_state(state_path: str, board_path: str, response_path: str) -> GameState:
    if os.path.exists(state_path):
        state = _load_state_json(state_path)
        state.source = "state.json"
        return state
    if os.path.exists(board_path):
        state = _load_board_fallback(board_path, response_path)
        state.source = "board.txt"
        return state
    return GameState(width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, source="нет данных")


def _load_state_json(path: str) -> GameState:
    with open(path, "r", encoding="utf-8") as infile:
        payload = json.load(infile)
    board = payload.get("board", {})
    state = GameState(
        width=int(board.get("width", DEFAULT_WIDTH)),
        height=int(board.get("height", DEFAULT_HEIGHT)),
        turn=int(payload.get("turn", 0)),
        round=int(payload.get("round", 0)),
        phase=str(payload.get("phase", "")),
        active=str(payload.get("active", "")),
        vp_model=int(payload.get("vp", {}).get("model", 0)),
        vp_player=int(payload.get("vp", {}).get("player", 0)),
        cp_model=int(payload.get("cp", {}).get("model", 0)),
        cp_player=int(payload.get("cp", {}).get("player", 0)),
        log_tail=[str(line) for line in payload.get("log_tail", []) if line is not None],
    )
    for unit in payload.get("units", []):
        state.units.append(
            Unit(
                side=str(unit.get("side", "")),
                unit_id=int(unit.get("id", 0)),
                name=str(unit.get("name", "")),
                hp=_to_optional_int(unit.get("hp")),
                models=_to_optional_int(unit.get("models")),
                x=int(unit.get("x", 0)),
                y=int(unit.get("y", 0)),
            )
        )
    for obj in payload.get("objectives", []):
        state.objectives.append(Objective(x=int(obj.get("x", 0)), y=int(obj.get("y", 0))))
    return state


def _load_board_fallback(board_path: str, response_path: str) -> GameState:
    rows: List[List[int]] = []
    with open(board_path, "r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            rows.append([int(val) for val in line.split(",") if val])
    width = len(rows) if rows else DEFAULT_WIDTH
    height = len(rows[0]) if rows else DEFAULT_HEIGHT
    state = GameState(width=width, height=height)

    for r_idx, row in enumerate(rows):
        for c_idx, value in enumerate(row):
            if value == 3:
                state.objectives.append(Objective(x=r_idx, y=c_idx))
            elif value >= 10:
                side = "player" if 10 <= value < 20 else "model"
                state.units.append(
                    Unit(
                        side=side,
                        unit_id=value,
                        name=f"Юнит {value}",
                        hp=None,
                        models=None,
                        x=r_idx,
                        y=c_idx,
                    )
                )

    log_tail = _read_log_tail(response_path)
    if log_tail:
        state.log_tail = log_tail
    return state


def _read_log_tail(path: str, max_lines: int = 20) -> List[str]:
    candidates = [path]
    if not path.endswith("response.txt"):
        candidates.append(os.path.join(os.path.dirname(path), "response.txt"))
    for candidate in candidates:
        if os.path.exists(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as infile:
                    lines = [line.rstrip("\n") for line in infile.readlines()]
                return lines[-max_lines:]
            except OSError:
                return []
    return []


def _to_optional_int(value) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
