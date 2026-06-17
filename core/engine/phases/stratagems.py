from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from core.engine.phases.types import ActionKind, ActionOption, Phase, Timing


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
        cp_cost=2,
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


def _unwrap(env):
    """Снять gym-обёртку до Warhammer40kEnv (локально, без цикла на option_generator)."""
    return getattr(env, "unwrapped", env)


def legal_stratagem_options(
    env,
    side: str,
    *,
    phase: Phase,
    trigger: Trigger,
    candidate_unit_idxs: list[int] | None = None,
) -> list[ActionOption]:
    """Какие стратагемы доступны сейчас (read-only).

    Фильтры: фаза, триггер, хватает ли CP, юнит жив, есть ли нужный keyword.
    legacy_patch есть только у insane_bravery (выразима в плоском action_dict);
    реакции пока несут пустой patch (исполняются движком авто до Stage 6/7).
    """
    e = _unwrap(env)
    is_model = side == "model"
    cp = int(e.modelCP if is_model else e.enemyCP)
    health = e.unit_health if is_model else e.enemy_health
    unit_data_list = e.unit_data if is_model else e.enemy_data

    defs = [d for d in for_trigger(trigger) if phase in d.phases]
    options: list[ActionOption] = []
    for d in defs:
        if cp < d.cp_cost:
            continue
        if candidate_unit_idxs is None:
            continue
        for raw in candidate_unit_idxs:
            i = int(raw)
            if not (0 <= i < len(health)) or health[i] <= 0:
                continue
            if d.keyword_req and not all(
                e._unit_has_keyword(unit_data_list[i], kw) for kw in d.keyword_req
            ):
                continue
            legacy_patch = {"use_cp": 1, "cp_on": i} if d.id == "insane_bravery" else {}
            options.append(
                ActionOption(
                    kind=ActionKind.USE_STRATAGEM,
                    unit_idx=i,
                    param={"stratagem_id": d.id},
                    legacy_patch=dict(legacy_patch),
                    meta={
                        "stratagem_id": d.id,
                        "cp_cost": d.cp_cost,
                        "timing": d.timing,
                        "scope": d.scope,
                    },
                )
            )
    return options
