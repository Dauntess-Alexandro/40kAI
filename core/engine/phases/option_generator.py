from __future__ import annotations

from core.engine.phases.types import ActionKind, ActionOption


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
