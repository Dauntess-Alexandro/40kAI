from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional


STATE_V2_VERSION = 2


def _safe_int(value: Any, fallback: Optional[int] = None) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _safe_float(value: Any, fallback: Optional[float] = None) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


@dataclass(frozen=True)
class BoardState:
    width: int
    height: int

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "BoardState":
        return cls(
            width=_safe_int(payload.get("width"), 60) or 60,
            height=_safe_int(payload.get("height"), 40) or 40,
        )

    def to_dict(self) -> Dict[str, int]:
        return {"width": int(self.width), "height": int(self.height)}


@dataclass(frozen=True)
class PhaseState:
    phase: Optional[str]
    active_side: Optional[str]
    turn: Optional[int]
    battle_round: Optional[int]

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "PhaseState":
        return cls(
            phase=payload.get("phase"),
            active_side=payload.get("active"),
            turn=_safe_int(payload.get("turn")),
            battle_round=_safe_int(payload.get("round")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase,
            "active": self.active_side,
            "turn": self.turn,
            "round": self.battle_round,
        }


@dataclass(frozen=True)
class UnitState:
    side: str
    unit_id: int
    name: str
    models: Optional[int]
    hp: Optional[float]
    x: Optional[int]
    y: Optional[int]
    alive: bool = True
    status: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "UnitState":
        hp_value = _safe_float(payload.get("hp"), None)
        return cls(
            side=str(payload.get("side") or ""),
            unit_id=_safe_int(payload.get("id"), -1) or -1,
            name=str(payload.get("name") or "—"),
            models=_safe_int(payload.get("models"), None),
            hp=hp_value,
            x=_safe_int(payload.get("x"), None),
            y=_safe_int(payload.get("y"), None),
            alive=payload.get("alive", hp_value is None or hp_value > 0),
            status=dict(payload.get("status") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "side": self.side,
            "id": self.unit_id,
            "name": self.name,
            "models": self.models,
            "hp": self.hp,
            "x": self.x,
            "y": self.y,
            "alive": self.alive,
            "status": dict(self.status),
        }


@dataclass(frozen=True)
class ObjectiveState:
    objective_id: int
    x: Optional[int]
    y: Optional[int]
    owner: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ObjectiveState":
        return cls(
            objective_id=_safe_int(payload.get("id"), 0) or 0,
            x=_safe_int(payload.get("x"), None),
            y=_safe_int(payload.get("y"), None),
            owner=payload.get("owner"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.objective_id,
            "x": self.x,
            "y": self.y,
            "owner": self.owner,
        }


@dataclass(frozen=True)
class ResourceState:
    player: Optional[int]
    model: Optional[int]

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ResourceState":
        return cls(
            player=_safe_int(payload.get("player"), None),
            model=_safe_int(payload.get("model"), None),
        )

    def to_dict(self) -> Dict[str, Optional[int]]:
        return {"player": self.player, "model": self.model}


@dataclass(frozen=True)
class GameStateV2:
    board: BoardState
    phase: PhaseState
    units: List[UnitState]
    objectives: List[ObjectiveState]
    vp: ResourceState
    cp: ResourceState
    log_tail: List[str] = field(default_factory=list)
    model_events: List[Dict[str, Any]] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: int = STATE_V2_VERSION

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "GameStateV2":
        board = BoardState.from_dict(payload.get("board", {}))
        phase = PhaseState.from_dict(payload)
        units = [
            UnitState.from_dict(item)
            for item in payload.get("units", [])
            if isinstance(item, dict)
        ]
        objectives = [
            ObjectiveState.from_dict(item)
            for item in payload.get("objectives", [])
            if isinstance(item, dict)
        ]
        vp = ResourceState.from_dict(payload.get("vp", {}))
        cp = ResourceState.from_dict(payload.get("cp", {}))
        return cls(
            board=board,
            phase=phase,
            units=units,
            objectives=objectives,
            vp=vp,
            cp=cp,
            log_tail=[str(line) for line in payload.get("log_tail", [])],
            model_events=list(payload.get("model_events", []) or []),
            generated_at=str(payload.get("generated_at") or datetime.utcnow().isoformat() + "Z"),
            version=_safe_int(payload.get("version"), STATE_V2_VERSION) or STATE_V2_VERSION,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "board": self.board.to_dict(),
            "turn": self.phase.turn,
            "round": self.phase.battle_round,
            "phase": self.phase.phase,
            "active": self.phase.active_side,
            "vp": self.vp.to_dict(),
            "cp": self.cp.to_dict(),
            "units": [unit.to_dict() for unit in self.units],
            "objectives": [objective.to_dict() for objective in self.objectives],
            "log_tail": list(self.log_tail),
            "model_events": list(self.model_events),
            "generated_at": self.generated_at,
        }


def units_from_payload(payload: Iterable[Dict[str, Any]]) -> List[UnitState]:
    return [UnitState.from_dict(item) for item in payload if isinstance(item, dict)]


def objectives_from_payload(payload: Iterable[Dict[str, Any]]) -> List[ObjectiveState]:
    return [ObjectiveState.from_dict(item) for item in payload if isinstance(item, dict)]
