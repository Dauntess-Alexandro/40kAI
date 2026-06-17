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
