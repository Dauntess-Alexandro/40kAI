import math
from typing import Callable, List, Sequence

from gym_mod.engine.logging_utils import format_unit

ABILITY_REANIMATION = "Reanimation Protocols"


DiceFn = Callable[..., int]
LogFn = Callable[[str], None]


def roll_d3(dice_fn: DiceFn) -> int:
    roll = dice_fn(max=3)
    if isinstance(roll, Sequence) and not isinstance(roll, (str, bytes)):
        return int(roll[0])
    return int(roll)


def _normalize_faction(value: str) -> str:
    return value.strip().lower()


def is_necrons(unit_data: dict) -> bool:
    for key in ("Faction", "Army Faction", "Army"):
        value = unit_data.get(key)
        if isinstance(value, str) and _normalize_faction(value) == "necrons":
            return True
    return False


def has_ability(unit_data: dict, ability_name: str) -> bool:
    abilities = unit_data.get("Abilities")
    if abilities is None:
        return False
    if isinstance(abilities, str):
        return abilities == ability_name
    if isinstance(abilities, Sequence):
        return ability_name in abilities
    return False


def _build_wounds_per_model(unit_health: float, unit_data: dict) -> List[int]:
    max_wounds = int(unit_data["W"])
    starting_models = int(unit_data["#OfModels"])
    current_total = int(round(unit_health))
    if current_total <= 0:
        return []

    alive_models = min(starting_models, int(math.ceil(current_total / max_wounds)))
    if alive_models <= 0:
        return []

    wounds = [max_wounds] * max(0, alive_models - 1)
    last_wounds = current_total - max_wounds * (alive_models - 1)
    if last_wounds <= 0:
        last_wounds = max_wounds
    wounds.append(min(last_wounds, max_wounds))
    return wounds


def _can_reanimate(wounds: List[int], unit_data: dict) -> bool:
    if not wounds:
        return False
    max_wounds = int(unit_data["W"])
    starting_models = int(unit_data["#OfModels"])
    if any(w < max_wounds for w in wounds):
        return True
    return len(wounds) < starting_models


def _log_reanimation(log_fn: LogFn, message: str) -> None:
    if log_fn is None:
        return
    log_fn(message)


def reanimation_protocols_one_unit(
    unit_health: float,
    unit_data: dict,
    dice_fn: DiceFn,
    log_fn: LogFn,
    unit_label: str,
) -> float:
    max_wounds = int(unit_data["W"])
    starting_models = int(unit_data["#OfModels"])
    wounds = _build_wounds_per_model(unit_health, unit_data)
    if not _can_reanimate(wounds, unit_data):
        return float(unit_health)
    _log_reanimation(log_fn, f"{unit_label}Используется способность: {ABILITY_REANIMATION}")
    roll = roll_d3(dice_fn)

    _log_reanimation(log_fn, f"{unit_label}Reanimation Protocols: бросок D3 = {roll}")
    _log_reanimation(
        log_fn,
        f"{unit_label}До: моделей={len(wounds)}, раны={wounds} всего={sum(wounds)}",
    )

    for _ in range(roll):
        wounded_indices = [idx for idx, w in enumerate(wounds) if w < max_wounds]
        if wounded_indices:
            idx = min(wounded_indices, key=lambda i: wounds[i])
            wounds[idx] += 1
            _log_reanimation(log_fn, f"{unit_label}Лечение раненой модели idx={idx}")
            continue

        if len(wounds) < starting_models:
            wounds.append(1)
            _log_reanimation(log_fn, f"{unit_label}Возвращена уничтоженная модель с 1 раной")
            continue

        break

    new_total = min(sum(wounds), starting_models * max_wounds)
    _log_reanimation(
        log_fn,
        f"{unit_label}После:  моделей={len(wounds)}, раны={wounds} всего={new_total}",
    )
    return float(new_total)


def apply_end_of_command_phase(env, side: str, dice_fn: DiceFn, log_fn: LogFn) -> None:
    if side == "model":
        health = env.unit_health
        data = env.unit_data
        side_label = env._display_side(side) if hasattr(env, "_display_side") else "MODEL"
        unit_id_offset = 21
    else:
        health = env.enemy_health
        data = env.enemy_data
        side_label = env._display_side(side) if hasattr(env, "_display_side") else "ENEMY"
        unit_id_offset = 11

    for i in range(len(health)):
        if health[i] <= 0:
            continue
        unit_data = data[i]
        if not is_necrons(unit_data):
            continue
        if not has_ability(unit_data, ABILITY_REANIMATION):
            continue
        unit_id = unit_id_offset + i
        unit_label = f"[{side_label}] {format_unit(unit_id, unit_data)} "
        health[i] = reanimation_protocols_one_unit(
            health[i],
            unit_data,
            dice_fn,
            log_fn,
            unit_label,
        )

    if hasattr(env, "_sync_after_command_phase_reanimation"):
        env._sync_after_command_phase_reanimation(side)


def _self_check_fixed_roll(roll: int) -> DiceFn:
    def _dice(max: int = 6, num: int = 1) -> int:
        _ = max
        _ = num
        return roll

    return _dice


def run_self_checks() -> None:
    data = {"W": 3, "#OfModels": 3}
    result = reanimation_protocols_one_unit(5, data, _self_check_fixed_roll(3), None, "[TEST] ")
    if result != 8:
        raise AssertionError(f"Expected 8, got {result}")

    data = {"W": 1, "#OfModels": 10}
    result = reanimation_protocols_one_unit(7, data, _self_check_fixed_roll(3), None, "[TEST] ")
    if result != 10:
        raise AssertionError(f"Expected 10, got {result}")


if __name__ == "__main__":
    run_self_checks()
    print("skills.py self-checks passed")
