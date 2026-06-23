from __future__ import annotations

from core.engine.phases.stratagems import STRATAGEM_PHASES
from core.engine.phases.types import ActionOption


def default_action_dict(len_model: int) -> dict[str, int]:
    """Нейтральный ход в плоском контракте.

    move=4 → нет направления (stay-fallback); attack=1 → пытаться вступить в бой/чардж;
    остальные головы — индекс 0. move_num_{i}/shoot_num_{i}/charge_num_{i} на каждого юнита.
    Пофазные головы strat_<phase>/<phase>_unit — аддитивно, применение под-проект 3.
    """
    n = int(len_model)
    action: dict[str, int] = {"move": 4, "attack": 1}
    for i in range(n):
        action[f"move_num_{i}"] = 0
        action[f"shoot_num_{i}"] = 0
        action[f"charge_num_{i}"] = 0
    for ph in STRATAGEM_PHASES:
        action[f"strat_{ph.value}"] = 0
        action[f"strat_{ph.value}_unit"] = 0
    return action


def compile_options_to_action_dict(options: list[ActionOption], len_model: int) -> dict[str, int]:
    """Сложить legacy_patch выбранных опций в один плоский action_dict.

    Per-unit shoot_num_{i}/charge_num_{i} — без lossy-override между юнитами.
    """
    action = default_action_dict(int(len_model))
    for opt in options:
        for key, value in opt.legacy_patch.items():
            action[str(key)] = int(value)
    return action
