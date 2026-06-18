"""Safety-harness под Track 2 (пошаговое исполнение хода).

Фиксирует ПОВЕДЕНИЕ движка на детерминированном эпизоде (фикс. seed + скриптованное
действие). Пока env.step переписывают (Track 2), этот тест ловит любое изменение
траектории. Движок проверен на детерминизм под seed (см. test_trace_is_deterministic).

Как перегенерировать GOLDEN (после ОСОЗНАННОГО изменения поведения):
  - запустить _build_trace(12345) и вставить результат в GOLDEN_SEED_12345.
Поля per-step: [sum_unit_hp, sum_enemy_hp, modelCP, enemyCP, modelVP, enemyVP, battle_round, game_over].
"""
from __future__ import annotations

import random

import numpy as np

from core.engine.phases import compile_options_to_action_dict
from core.engine.unit import Unit
from core.envs.warhamEnv import Warhammer40kEnv


def _mk(name: str) -> Unit:
    data = {"Name": name, "Movement": 6, "M": 6, "W": 2, "#OfModels": 3, "OC": 1, "Ld": 7, "T": 4, "Sv": 3}
    weapon = {"Name": "Stub gun", "Type": "Ranged", "Range": 24, "A": 1, "BS": 4, "S": 4, "AP": 0, "Damage": 1}
    melee = {"Name": "Stub blade", "Type": "Melee", "Range": 2, "A": 1, "WS": 4, "S": 4, "AP": 0, "Damage": 1}
    return Unit(data=data, weapon=weapon, melee=melee, b_len=30, b_hei=30, GUI=False)


def _build_trace(seed: int, steps: int = 8) -> list[list]:
    random.seed(seed)
    np.random.seed(seed)
    model = [_mk("ModelA"), _mk("ModelB")]
    enemy = [_mk("EnemyA"), _mk("EnemyB")]
    env = Warhammer40kEnv(enemy=enemy, model=model, b_len=30, b_hei=30)
    env.reset(options={"m": model, "e": enemy, "trunc": True})
    n = len(env.unit_health)
    action = compile_options_to_action_dict([], n)
    trace: list[list] = []
    with env.simulation_mode():
        for _ in range(steps):
            env.step(dict(action))
            if not env.game_over:
                env.enemyTurn(trunc=True)
            trace.append([
                round(float(sum(env.unit_health)), 2),
                round(float(sum(env.enemy_health)), 2),
                int(env.modelCP),
                int(env.enemyCP),
                int(env.modelVP),
                int(env.enemyVP),
                int(env.battle_round),
                bool(env.game_over),
            ])
            if env.game_over:
                break
    return trace


GOLDEN_SEED_12345 = [
    [11.0, 10.0, 1, 2, 0, 0, 2, False],
    [11.0, 9.0, 3, 4, 0, 0, 3, False],
    [11.0, 7.0, 5, 6, 0, 0, 4, False],
    [11.0, 7.0, 7, 8, 0, 0, 5, False],
    [11.0, 7.0, 9, 10, 0, 0, 6, False],
    [11.0, 6.0, 11, 12, 0, 0, 7, False],
    [10.0, 5.0, 10, 14, 0, 0, 8, False],
    [10.0, 5.0, 9, 16, 0, 0, 9, False],
]


def test_trace_is_deterministic():
    """Под фикс. seed траектория воспроизводима (необходимо для сравнения до/после Track 2)."""
    assert _build_trace(12345) == _build_trace(12345)


def test_trace_matches_golden():
    """Поведение движка совпадает с замороженным эталоном (регресс-гард Track 2)."""
    assert _build_trace(12345) == GOLDEN_SEED_12345


def test_other_seed_differs():
    """Санити: другой seed даёт другую траекторию (эталон не вырожден)."""
    assert _build_trace(999) != GOLDEN_SEED_12345
