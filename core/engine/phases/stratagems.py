from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from core.engine.phases.types import Phase, Timing


class Trigger(StrEnum):
    BATTLE_SHOCK_FAILED = "battle_shock_failed"
    TARGETED_BY_SHOOTING = "targeted_by_shooting"
    ENEMY_ENDED_MOVE = "enemy_ended_move"
    ENEMY_CHARGED_IN = "enemy_charged_in"


class UsageLimit(StrEnum):
    PER_PHASE = "per_phase"
    PER_TURN = "per_turn"
    PER_BATTLE = "per_battle"
    UNLIMITED = "unlimited"


@dataclass(frozen=True)
class StratagemDef:
    """Описание стратагемы (data-only). usage_limit пока НЕ enforced (Stage 6)."""

    id: str
    name_ru: str
    cp_cost: int
    phases: tuple[Phase, ...]
    timing: Timing
    trigger: Trigger
    scope: str  # "self_unit" | "reacting_unit" | "enemy_unit" (описательное)
    keyword_req: tuple[str, ...]
    usage_limit: UsageLimit
    effect_id: str


REGISTRY: tuple[StratagemDef, ...] = (
    StratagemDef(
        id="insane_bravery",
        name_ru="Insane Bravery",
        cp_cost=1,
        phases=(Phase.COMMAND,),
        timing=Timing.MAIN,
        trigger=Trigger.BATTLE_SHOCK_FAILED,
        scope="self_unit",
        keyword_req=(),
        usage_limit=UsageLimit.PER_BATTLE,
        effect_id="auto_pass_battle_shock",
    ),
    StratagemDef(
        id="overwatch",
        name_ru="Fire Overwatch",
        cp_cost=1,
        phases=(Phase.MOVEMENT, Phase.CHARGE),
        timing=Timing.REACTION,
        trigger=Trigger.ENEMY_ENDED_MOVE,
        scope="reacting_unit",
        keyword_req=(),
        usage_limit=UsageLimit.PER_PHASE,
        effect_id="shoot_hits_on_6",
    ),
    StratagemDef(
        id="smokescreen",
        name_ru="Smokescreen",
        cp_cost=1,
        phases=(Phase.SHOOTING,),
        timing=Timing.REACTION,
        trigger=Trigger.TARGETED_BY_SHOOTING,
        scope="reacting_unit",
        keyword_req=("smoke",),
        usage_limit=UsageLimit.UNLIMITED,
        effect_id="benefit_of_cover",
    ),
    StratagemDef(
        id="heroic_intervention",
        name_ru="Heroic Intervention",
        cp_cost=1,
        phases=(Phase.CHARGE,),
        timing=Timing.REACTION,
        trigger=Trigger.ENEMY_CHARGED_IN,
        scope="reacting_unit",
        keyword_req=(),
        usage_limit=UsageLimit.PER_PHASE,
        effect_id="counter_charge",
    ),
)


_BY_ID: dict[str, StratagemDef] = {d.id: d for d in REGISTRY}


def by_id(stratagem_id: str) -> StratagemDef:
    try:
        return _BY_ID[stratagem_id]
    except KeyError:
        raise KeyError(
            f"нет стратагемы id={stratagem_id!r}; где: stratagems.by_id; "
            "что делать: проверить REGISTRY/опечатку id."
        ) from None


def for_phase(phase: Phase) -> list[StratagemDef]:
    return [d for d in REGISTRY if phase in d.phases]


def for_trigger(trigger: Trigger) -> list[StratagemDef]:
    return [d for d in REGISTRY if d.trigger == trigger]
