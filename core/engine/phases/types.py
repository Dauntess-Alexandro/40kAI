from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Phase(StrEnum):
    COMMAND = "command"
    MOVEMENT = "movement"
    SHOOTING = "shooting"
    CHARGE = "charge"
    FIGHT = "fight"
    SCORING = "scoring"


class SubStep(StrEnum):
    BATTLE_SHOCK = "battle_shock"
    MOVE_UNIT = "move_unit"
    PICK_SHOOT_TARGET = "pick_shoot_target"
    PICK_CHARGE_TARGET = "pick_charge_target"
    FIGHT_UNIT = "fight_unit"
    SCORE = "score"


class Timing(StrEnum):
    MAIN = "main"
    REACTION = "reaction"


class ActionKind(StrEnum):
    STAY = "stay"
    MOVE = "move"
    ADVANCE = "advance"
    FALL_BACK = "fall_back"
    SHOOT = "shoot"
    CHARGE = "charge"
    FIGHT = "fight"
    USE_STRATAGEM = "use_stratagem"
    PASS = "pass"
    END_PHASE = "end_phase"


@dataclass
class ActionOption:
    """Атомарный выбор в окне решения.

    legacy_patch — частичный плоский action_dict, который реализует эту опцию
    в текущем env.step (источник истины по маппингу — сам генератор).
    """

    kind: ActionKind
    unit_idx: int | None = None
    target_idx: int | None = None  # глобальный индекс врага для SHOOT/CHARGE
    param: dict[str, Any] = field(default_factory=dict)
    legacy_patch: dict[str, int] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionWindow:
    """Точка, где одна сторона выбирает одну из options."""

    window_id: str
    owner_side: str  # "model" | "enemy"
    phase: Phase
    sub_step: SubStep
    timing: Timing
    cursor_unit_idx: int | None
    options: list[ActionOption]
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class PhaseState:
    """Нормализованное «где мы сейчас» в иерархии фаз."""

    battle_round: int
    active_side: str
    phase: Phase
    sub_step: SubStep
    timing: Timing
    cursor_unit_idx: int | None = None


@dataclass
class PhaseResult:
    """Результат применения ActionOption движком фаз (для будущих стадий)."""

    reward_delta: float = 0.0
    events: list[Any] = field(default_factory=list)
    next_window: DecisionWindow | None = None
    done: bool = False
    info_patch: dict[str, Any] = field(default_factory=dict)
