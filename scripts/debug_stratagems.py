"""
Минимальный debug-сценарий для проверки логов стратагем 10e.

Запуск (нужен сохранённый pickle с env/model/enemy, как в play.py):
  VERBOSE_LOGS=1 python scripts/debug_stratagems.py path/to/save.pickle

Скрипт искусственно сближает первые юниты, чтобы гарантировать:
  - Smokescreen (в момент выбора цели стрельбы)
  - Overwatch (после завершения перемещения врага)
  - Heroic Intervention (после успешного charge move)
"""

import sys
import pickle


def _build_action(env):
    action = {
        "move": 4,
        "attack": 1,
        "charge": 0,
        "shoot": 0,
        "use_cp": 0,
        "cp_on": 0,
    }
    for i in range(len(env.unit_health)):
        action[f"move_num_{i}"] = 0
    return action


def main(path):
    with open(path, "rb") as f:
        env, model, enemy = pickle.load(f)

    env.reset(options={"m": model, "e": enemy, "trunc": False})
    env.modelCP = 2
    env.enemyCP = 2

    # Сближаем первые юниты, чтобы были в дальности стрельбы/чарджа.
    if env.unit_coords and env.enemy_coords:
        env.unit_coords[0] = [5, 5]
        env.enemy_coords[0] = [7, 5]

    action = _build_action(env)

    # Movement (enemy) -> должен триггернуть Overwatch защитника.
    env.movement_phase("enemy", battle_shock=[False] * len(env.enemy_health))

    # Shooting (model) -> должен вызвать Smokescreen при выборе цели.
    env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=action)

    # Charge (model) -> должен вызвать Heroic Intervention после успешного чарджа.
    env.charge_phase("model", advanced_flags=[False] * len(env.unit_health), action=action)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/debug_stratagems.py path/to/save.pickle")
        raise SystemExit(1)
    main(sys.argv[1])
