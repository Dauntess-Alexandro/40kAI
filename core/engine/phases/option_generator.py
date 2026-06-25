from __future__ import annotations

from core.engine.phases.stratagems import (
    Trigger,
    by_id,
    legal_stratagem_options,
    stratagem_choice_index,
)
from core.engine.phases.types import (
    ActionKind,
    ActionOption,
    DecisionWindow,
    Phase,
    SubStep,
    Timing,
)


def _unwrap(env):
    """Снять gym-обёртку до Warhammer40kEnv (без зависимости от core.models)."""
    return getattr(env, "unwrapped", env)


def shooting_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]:
    """PASS + по одной SHOOT-опции на валидную цель юнита.

    shoot в плоском контракте — локальный ранг в списке целей юнита
    (см. warhamEnv.shooting_phase: idOfE = valid_target_ids[raw]).
    """
    e = _unwrap(env)
    valid = list(e.get_shoot_targets_for_unit(side, int(unit_idx)))
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=int(unit_idx))]
    for rank, target_global in enumerate(valid):
        options.append(
            ActionOption(
                kind=ActionKind.SHOOT,
                unit_idx=int(unit_idx),
                target_idx=int(target_global),
                param={"local_rank": int(rank)},
                legacy_patch={f"shoot_num_{int(unit_idx)}": int(rank)},
            )
        )
    return options


def _legacy_move_dir_for_destination(row: int, col: int, x: int, y: int) -> int:
    dr = int(y) - int(row)
    dc = int(x) - int(col)
    if dr == 0 and dc == 0:
        return 4
    if abs(dr) >= abs(dc):
        return 0 if dr > 0 else 1
    return 3 if dc > 0 else 2


def movement_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]:
    """STAY/MOVE/ADVANCE-опции, индекс-в-индекс с _pick_destination_by_reachable_index.

    candidates = [stay] + move_cells(normal) + advance_cells(advance);
    reachable_index — это значение move_num_{unit_idx}.
    """
    e = _unwrap(env)
    overlay = e.get_unit_movement_overlay(side, int(unit_idx))
    move_cells = list(overlay.get("move_cells") or [])
    advance_cells = list(overlay.get("advance_cells") or [])

    coords = e.unit_coords if side == "model" else e.enemy_coords
    row = int(coords[int(unit_idx)][0])
    col = int(coords[int(unit_idx)][1])

    # Тот же порядок, что у warhamEnv._pick_destination_by_reachable_index.
    candidates: list[tuple[int, int, ActionKind]] = [(int(col), int(row), ActionKind.STAY)]
    candidates.extend((int(x), int(y), ActionKind.MOVE) for x, y in move_cells)
    candidates.extend((int(x), int(y), ActionKind.ADVANCE) for x, y in advance_cells)

    options: list[ActionOption] = []
    for k, (x, y, kind) in enumerate(candidates):
        legacy_patch = {f"move_num_{int(unit_idx)}": int(k)}
        move_dir = _legacy_move_dir_for_destination(row, col, int(x), int(y))
        if kind is not ActionKind.STAY and move_dir != 4:
            legacy_patch["move"] = int(move_dir)
        options.append(
            ActionOption(
                kind=kind,
                unit_idx=int(unit_idx),
                param={"reachable_index": int(k), "dest": (int(x), int(y))},
                legacy_patch=legacy_patch,
            )
        )
    return options


def charge_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]:
    """PASS + по одной CHARGE-опции на валидную цель юнита.

    charge в плоском контракте — глобальный индекс врага; для попытки нужен attack=1.
    """
    e = _unwrap(env)
    valid = list(e.get_charge_targets_for_unit(side, int(unit_idx)))
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=int(unit_idx))]
    for target_global in valid:
        options.append(
            ActionOption(
                kind=ActionKind.CHARGE,
                unit_idx=int(unit_idx),
                target_idx=int(target_global),
                legacy_patch={f"charge_num_{int(unit_idx)}": int(target_global), "attack": 1},
            )
        )
    return options


def fight_stratagem_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]:
    """PASS + active fight-phase stratagems for one alive unit."""
    e = _unwrap(env)
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=int(unit_idx))]
    options.extend(
        legal_stratagem_options(
            e,
            side,
            phase=Phase.FIGHT,
            trigger=Trigger.FIGHT_PHASE,
            candidate_unit_idxs=[int(unit_idx)],
        )
    )
    return options


def command_reroll_options_for_unit(
    env, side: str, unit_idx: int, *, phase: Phase, rolls: tuple[str, ...]
) -> list[ActionOption]:
    """Опции Command Re-roll для живого юнита в данной фазе (по одной на под-тип roll).

    Phase-агностично: вызывается из окон movement/shooting/charge (fight идёт через
    legal_stratagem_options). Не зависит от trigger — Command Re-roll многофазный.
    Гейт «один бросок = один реролл» — на стороне исполнения (consumed); лимит UNLIMITED,
    естественный лимит — CP. Возвращает [] если стратагемы нет в фазе, мало CP или юнит мёртв.
    """
    e = _unwrap(env)
    d = by_id("command_reroll")
    if phase not in d.phases:
        return []
    is_model = side == "model"
    cp = int(e.modelCP if is_model else e.enemyCP)
    if cp < d.cp_cost:
        return []
    health = e.unit_health if is_model else e.enemy_health
    i = int(unit_idx)
    if not (0 <= i < len(health)) or health[i] <= 0:
        return []
    # Подзадача 3.3: advance reroll нелегален в movement-окне.
    # Advance не имеет pass/fail-критерия, поэтому не предлагаем его как legal option,
    # сохраняя при этом подтип в action-contract/choices.
    if phase is Phase.MOVEMENT:
        rolls = tuple(roll for roll in rolls if str(roll) != "advance")
        if not rolls:
            return []
    # Гейт «нет цели — нет реролла»: не предлагаем command_reroll, если у юнита нет предстоящего
    # броска в этой фазе (нет валидной цели стрельбы/чарджа) — иначе CP тратится впустую (wasted).
    if phase is Phase.SHOOTING and not e.get_shoot_targets_for_unit(side, i):
        return []
    if phase is Phase.CHARGE and not e.get_charge_targets_for_unit(side, i):
        return []
    options: list[ActionOption] = []
    for roll in rolls:
        options.append(
            ActionOption(
                kind=ActionKind.USE_STRATAGEM,
                unit_idx=i,
                param={"stratagem_id": d.id, "reroll_roll": roll},
                legacy_patch={
                    f"strat_{phase.value}": stratagem_choice_index(phase, f"command_reroll:{roll}"),
                    f"strat_{phase.value}_unit": i,
                },
                meta={
                    "stratagem_id": d.id,
                    "cp_cost": d.cp_cost,
                    "timing": d.timing,
                    "scope": d.scope,
                    "reroll_roll": roll,
                },
            )
        )
    return options


def _alive_indices(health) -> list[int]:
    return [i for i, hp in enumerate(health) if hp > 0]


def command_window(env, side: str) -> DecisionWindow:
    """Окно командной фазы: Insane Bravery на провал Battle-shock.

    Опции Bravery берутся из реестра стратагем (legal_stratagem_options),
    а не инлайнятся: единый источник истины по легальности CP.
    """
    e = _unwrap(env)
    health = e.unit_health if side == "model" else e.enemy_health
    cp = int(e.modelCP if side == "model" else e.enemyCP)
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=None)]
    options.extend(
        legal_stratagem_options(
            e,
            side,
            phase=Phase.COMMAND,
            trigger=Trigger.BATTLE_SHOCK_FAILED,
            candidate_unit_idxs=_alive_indices(health),
        )
    )
    return DecisionWindow(
        window_id=f"command:{side}",
        owner_side=side,
        phase=Phase.COMMAND,
        sub_step=SubStep.BATTLE_SHOCK,
        timing=Timing.MAIN,
        cursor_unit_idx=None,
        options=options,
        context={"cp": cp},
    )


def generate_windows(env, side: str = "model") -> list[DecisionWindow]:
    """Упорядоченные окна хода: command → movement → shooting → charge → fight.

    Fight-окна: стратагемы боя (Hungry Void, Command Re-roll) на живого юнита;
    исполнение в env.step — через голову strat_fight (AZ MCTS) или PhaseEngine.run_fight.
    """
    e = _unwrap(env)
    health = e.unit_health if side == "model" else e.enemy_health
    alive = _alive_indices(health)
    windows: list[DecisionWindow] = [command_window(e, side)]

    for u in alive:
        windows.append(
            DecisionWindow(
                window_id=f"movement:{side}:{u}",
                owner_side=side,
                phase=Phase.MOVEMENT,
                sub_step=SubStep.MOVE_UNIT,
                timing=Timing.MAIN,
                cursor_unit_idx=int(u),
                options=movement_options_for_unit(e, side, u),
            )
        )
    for u in alive:
        windows.append(
            DecisionWindow(
                window_id=f"shooting:{side}:{u}",
                owner_side=side,
                phase=Phase.SHOOTING,
                sub_step=SubStep.PICK_SHOOT_TARGET,
                timing=Timing.MAIN,
                cursor_unit_idx=int(u),
                options=shooting_options_for_unit(e, side, u),
            )
        )
    # Окна стратагем shooting (per-unit command reroll: hit/wound)
    for u in alive:
        _sopts = command_reroll_options_for_unit(e, side, u, phase=Phase.SHOOTING, rolls=("hit", "wound"))
        if _sopts:
            windows.append(
                DecisionWindow(
                    window_id=f"shooting_stratagem:{side}:{u}",
                    owner_side=side,
                    phase=Phase.SHOOTING,
                    sub_step=SubStep.PICK_SHOOT_TARGET,
                    timing=Timing.MAIN,
                    cursor_unit_idx=int(u),
                    options=[ActionOption(kind=ActionKind.PASS, unit_idx=int(u)), *_sopts],
                )
            )
    for u in alive:
        windows.append(
            DecisionWindow(
                window_id=f"charge:{side}:{u}",
                owner_side=side,
                phase=Phase.CHARGE,
                sub_step=SubStep.PICK_CHARGE_TARGET,
                timing=Timing.MAIN,
                cursor_unit_idx=int(u),
                options=charge_options_for_unit(e, side, u),
            )
        )
    # Окна стратагем charge (per-unit command reroll: charge)
    for u in alive:
        _sopts = command_reroll_options_for_unit(e, side, u, phase=Phase.CHARGE, rolls=("charge",))
        if _sopts:
            windows.append(
                DecisionWindow(
                    window_id=f"charge_stratagem:{side}:{u}",
                    owner_side=side,
                    phase=Phase.CHARGE,
                    sub_step=SubStep.PICK_CHARGE_TARGET,
                    timing=Timing.MAIN,
                    cursor_unit_idx=int(u),
                    options=[ActionOption(kind=ActionKind.PASS, unit_idx=int(u)), *_sopts],
                )
            )
    for u in alive:
        windows.append(
            DecisionWindow(
                window_id=f"fight:{side}:{u}",
                owner_side=side,
                phase=Phase.FIGHT,
                sub_step=SubStep.FIGHT_UNIT,
                timing=Timing.MAIN,
                cursor_unit_idx=int(u),
                options=fight_stratagem_options_for_unit(e, side, u),
            )
        )
    return windows
