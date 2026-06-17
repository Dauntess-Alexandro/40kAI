from __future__ import annotations

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
                legacy_patch={"shoot": int(rank)},
            )
        )
    return options


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
        options.append(
            ActionOption(
                kind=kind,
                unit_idx=int(unit_idx),
                param={"reachable_index": int(k), "dest": (int(x), int(y))},
                legacy_patch={f"move_num_{int(unit_idx)}": int(k)},
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
                legacy_patch={"charge": int(target_global), "attack": 1},
            )
        )
    return options


def _alive_indices(health) -> list[int]:
    return [i for i, hp in enumerate(health) if hp > 0]


def command_window(env, side: str) -> DecisionWindow:
    """Окно командной фазы: Insane Bravery на провал Battle-shock.

    Реальный провал теста определяется броском в рантайме; на уровне слоя мы
    предлагаем агенту опцию заранее (PASS / использовать Bravery на юнита i),
    гейтим только по наличию CP — как делает командная фаза env.
    """
    e = _unwrap(env)
    health = e.unit_health if side == "model" else e.enemy_health
    cp = int(e.modelCP if side == "model" else e.enemyCP)
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=None)]
    if cp >= 1:
        for i in _alive_indices(health):
            options.append(
                ActionOption(
                    kind=ActionKind.USE_STRATAGEM,
                    unit_idx=int(i),
                    param={"stratagem_id": "insane_bravery"},
                    legacy_patch={"use_cp": 1, "cp_on": int(i)},
                    meta={"stratagem_id": "insane_bravery", "cp_cost": 1},
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
    """Упорядоченные окна хода: command → movement → shooting → charge.

    Бой/скоринг в текущей модели не дают выбора агента — окон не порождаем.
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
    return windows
