from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from core.engine.phases.types import ActionKind, ActionOption, Phase, Timing


class Trigger(StrEnum):
    BATTLE_SHOCK_FAILED = "battle_shock_failed"
    TARGETED_BY_SHOOTING = "targeted_by_shooting"
    ENEMY_ENDED_MOVE = "enemy_ended_move"
    ENEMY_CHARGED_IN = "enemy_charged_in"
    FIGHT_PHASE = "fight_phase"


class UsageLimit(StrEnum):
    PER_PHASE = "per_phase"
    PER_TURN = "per_turn"
    PER_BATTLE = "per_battle"
    UNLIMITED = "unlimited"


@dataclass(frozen=True)
class StratagemDef:
    """Описание стратагемы (data-only). usage_limit enforced через stratagems.usage_limit_reached (B1c)."""

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
    # Insane Bravery — Core Stratagem 10ed (Wahapedia):
    #   https://wahapedia.ru/wh40k10ed/the-rules/core-stratagems/#Insane-Bravery
    #   WHEN: Battle-shock step of your Command phase, just after a unit fails a Battle-shock test.
    #   COST: 1 CP. EFFECT: that unit is not Battle-shocked.
    #   RESTRICTION (usage_limit): once per battle (PER_BATTLE).
    # Реализация: command_phase() при провале теста зовёт _apply_stratagem(insane_bravery) →
    # списывает 1 CP, снимает battle_shock с юнита. Правила берём из Wahapedia, не выдумываем.
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
    # Fire Overwatch — Core Stratagem 10ed (Wahapedia):
    #   https://wahapedia.ru/wh40k10ed/the-rules/core-stratagems/#Fire-Overwatch
    #   WHEN: ход оппонента, когда вражеский юнит начинает/заканчивает Normal/Advance/Fall Back/Charge
    #   move в пределах 24" и видимости. COST: 1 CP. EFFECT: ваш юнит немедленно стреляет по нему,
    #   но попадания только на немодифицированную 6. RESTRICTION: once per turn (на ваш ход).
    # Реализация (песочница): effect_id=shoot_hits_on_6 на ENEMY_ENDED_MOVE в movement/charge,
    # usage_limit PER_PHASE (упрощение «once per turn»). Условия 24"/видимости — на стороне движка.
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
    # Smokescreen — Core Stratagem 10ed (Wahapedia):
    #   https://wahapedia.ru/wh40k10ed/the-rules/core-stratagems/#Smokescreen
    #   WHEN: Shooting phase оппонента, когда выбрана цель — ваш SMOKE-юнит. COST: 1 CP.
    #   EFFECT: до конца фазы юнит получает Benefit of Cover и Stealth.
    # Реализация (песочница): моделируем Benefit of Cover + Stealth (hit_penalty=1).
    # keyword_req=("smoke",); usage_limit UNLIMITED (как в правилах нет «1 раз»).
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
    # Heroic Intervention — Core Stratagem 10ed (Wahapedia):
    #   https://wahapedia.ru/wh40k10ed/the-rules/core-stratagems/#Heroic-Intervention
    #   WHEN: Charge phase оппонента, после того как вражеский юнит закончил charge move. COST: 2 CP.
    #   EFFECT: ваш eligible-юнит в пределах дистанции может объявить и совершить charge по тому юниту.
    # Реализация (песочница): effect_id=counter_charge на ENEMY_CHARGED_IN; usage_limit PER_PHASE.
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
    # Protocol of the Hungry Void — Necrons Awakened Dynasty Battle Tactic Stratagem 10ed (Wahapedia):
    #   https://wahapedia.ru/wh40k10ed/factions/necrons/Stratagems
    #   WHEN: Fight phase. TARGET: одна NECRONS-юнит, ещё не выбранная драться в этой фазе.
    #   COST: 1 CP. EFFECT: до конца фазы +1 к Strength melee-оружия юнита; дополнительно, если
    #   юнит ведёт NECRONS CHARACTER — улучшить AP melee на 1 (не суммируется с другими AP-модификаторами).
    # Реализация (песочница): моделируем +1 Strength (effect_id=hungry_void_strength_mod,
    # strength_mod=1) + AP+1 при CHARACTER-лидере (в _fight_effects_for_attacker).
    # keyword_req=("necrons",) — только NECRONS-юниты могут использовать стратагему (A7).
    # usage_limit PER_PHASE enforced (B1c).
    StratagemDef(
        id="hungry_void",
        name_ru="Hungry Void",
        cp_cost=1,
        phases=(Phase.FIGHT,),
        timing=Timing.MAIN,
        trigger=Trigger.FIGHT_PHASE,
        scope="self_unit",
        keyword_req=("necrons",),
        usage_limit=UsageLimit.PER_PHASE,
        effect_id="hungry_void_strength_mod",
    ),
    # Command Re-roll — Core Stratagem 10ed (Wahapedia):
    #   https://wahapedia.ru/wh40k10ed/the-rules/core-stratagems/#Command-Re-roll
    #   WHEN: любой момент игры, перед/после броска. COST: 1 CP. EFFECT: ре-ролл ОДНОГО броска
    #   (hit/wound/save/charge/D6 и т.п.). RESTRICTION: 1 раз на бросок.
    # Реализация (песочница): упрощено до fight-phase — ре-ролл ОДНОГО проваленного wound-броска
    # атаки юнита (fight-only упрощение реального per-roll правила).
    StratagemDef(
        id="command_reroll",
        name_ru="Command Re-roll (упрощённо)",
        cp_cost=1,
        phases=(Phase.FIGHT,),
        timing=Timing.MAIN,
        trigger=Trigger.FIGHT_PHASE,
        scope="self_unit",
        keyword_req=(),
        usage_limit=UsageLimit.PER_PHASE,
        effect_id="command_reroll_wounds",
    ),
    # Go to Ground — Core Stratagem 10ed (Wahapedia):
    #   https://wahapedia.ru/wh40k10ed/the-rules/core-stratagems/#Go-to-Ground
    #   WHEN: Shooting phase оппонента, когда выбрана цель — ваш INFANTRY-юнит. COST: 1 CP.
    #   EFFECT: до конца фазы юнит получает Benefit of Cover и +1 к save throws.
    # Реализация (песочница): реальный эффект — Benefit of Cover + 6+ invulnerable save; моделируем оба.
    # effect_id=benefit_of_cover; _maybe_use_go_to_ground возвращает {"cover": True, "invuln_grant": 6}.
    # keyword_req=("infantry",); usage_limit UNLIMITED.
    StratagemDef(
        id="go_to_ground",
        name_ru="Go to Ground",
        cp_cost=1,
        phases=(Phase.SHOOTING,),
        timing=Timing.REACTION,
        trigger=Trigger.TARGETED_BY_SHOOTING,
        scope="reacting_unit",
        keyword_req=("infantry",),
        usage_limit=UsageLimit.UNLIMITED,
        effect_id="benefit_of_cover",
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


def usage_limit_reached(env, side: str, d: StratagemDef, *, phase: str | None = None) -> bool:
    """B1c: исчерпан ли usage_limit стратагемы для стороны по журналу stratagem_used.

    Окно подсчёта по типу лимита (каждый ограниченный тип = максимум 1 раз в окне):
      PER_PHASE  — в текущем (battle_round, phase);
      PER_TURN   — в текущем battle_round (ход стороны = раунд);
      PER_BATTLE — за всю партию;
      UNLIMITED  — без ограничения.
    `phase` — строка фазы окна/применения; если None, берём env.phase.
    """
    if d.usage_limit is UsageLimit.UNLIMITED:
        return False
    e = _unwrap(env)
    phase_str = str(phase if phase is not None else getattr(e, "phase", "") or "")
    battle_round = int(getattr(e, "battle_round", 1) or 1)
    used = getattr(e, "stratagem_used", None) or []
    for rec in used:
        if len(rec) < 4:
            continue
        r_side, r_id, r_round, r_phase = rec[0], rec[1], rec[2], rec[3]
        if str(r_side) != side or str(r_id) != d.id:
            continue
        if d.usage_limit is UsageLimit.PER_BATTLE:
            return True
        if d.usage_limit is UsageLimit.PER_TURN and int(r_round) == battle_round:
            return True
        if d.usage_limit is UsageLimit.PER_PHASE and int(r_round) == battle_round and str(r_phase) == phase_str:
            return True
    return False


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
        # B1c: исчерпанные по usage_limit стратагемы не предлагаем как опцию.
        if usage_limit_reached(e, side, d, phase=phase.value):
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
