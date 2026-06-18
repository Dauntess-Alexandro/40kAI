from __future__ import annotations

from core.engine.phases.types import ActionOption


def default_action_dict(len_model: int) -> dict[str, int]:
    """Нейтральный ход в плоском контракте.

    move=4 → нет направления (stay-fallback); attack=1 → пытаться вступить в бой/чардж;
    остальные головы — индекс 0. move_num_{i} на каждого юнита модели.
    """
    action: dict[str, int] = {
        "move": 4,
        "attack": 1,
        "shoot": 0,
        "charge": 0,
        "use_cp": 0,
        "cp_on": 0,
    }
    for i in range(int(len_model)):
        action[f"move_num_{i}"] = 0
    return action


def compile_options_to_action_dict(options: list[ActionOption], len_model: int) -> dict[str, int]:
    """Сложить legacy_patch выбранных опций в один плоский action_dict.

    Ограничение плоского контракта: одна голова shoot/charge/use_cp на весь ход,
    поэтому при нескольких конфликтующих опциях побеждает последняя (lossy).
    Это осознанное ограничение слоя до переноса исполнения в PhaseEngine (Stage 7).
    """
    action = default_action_dict(int(len_model))
    for opt in options:
        for key, value in opt.legacy_patch.items():
            action[str(key)] = int(value)
    return action
