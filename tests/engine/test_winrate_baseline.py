"""Stage 8 safety-harness: winrate-baseline.

Замораживает исход N детерминированных эпизодов (дефолтный ход model-vs-enemy)
на фикс. сидах. Golden-trace ловит изменение ОДНОГО хода; этот harness ловит
СДВИГ ИТОГОВ партии — критично перед windowed-self-play (8.3+), где меняется
петля принятия решений.

Перегенерация эталона (только после ОСОЗНАННОГО изменения баланса/механик):
запустить _run_baseline() и вставить результат в BASELINE_WINNERS.
"""
from __future__ import annotations

import random

import numpy as np

from core.engine.phases import compile_options_to_action_dict
from core.engine.unit import Unit
from core.envs.warhamEnv import Warhammer40kEnv

N_EPISODES = 20
MAX_STEPS = 40


def _mk(name: str) -> Unit:
    data = {"Name": name, "Movement": 6, "M": 6, "W": 2, "#OfModels": 3, "OC": 1, "Ld": 7, "T": 4, "Sv": 3}
    weapon = {"Name": "g", "Type": "Ranged", "Range": 24, "A": 1, "BS": 4, "S": 4, "AP": 0, "Damage": 1}
    melee = {"Name": "b", "Type": "Melee", "Range": 2, "A": 1, "WS": 4, "S": 4, "AP": 0, "Damage": 1}
    return Unit(data=data, weapon=weapon, melee=melee, b_len=30, b_hei=30, GUI=False)


def _episode_winner(seed: int) -> str:
    random.seed(seed)
    np.random.seed(seed)
    model = [_mk("A"), _mk("B")]
    enemy = [_mk("C"), _mk("D")]
    env = Warhammer40kEnv(enemy=enemy, model=model, b_len=30, b_hei=30)
    env.reset(options={"m": model, "e": enemy, "trunc": True})
    n = len(env.unit_health)
    action = compile_options_to_action_dict([], n)
    with env.simulation_mode():
        for _ in range(MAX_STEPS):
            env.step(dict(action))
            if env.game_over:
                break
            env.enemyTurn(trunc=True)
            if env.game_over:
                break
    return str(getattr(env, "last_winner", None) or "")


def _run_baseline() -> list[str]:
    return [_episode_winner(s) for s in range(N_EPISODES)]


BASELINE_WINNERS = [
    "", "model", "model", "model", "", "model", "model", "model", "", "",
    "", "model", "model", "model", "model", "model", "model", "", "", "model",
]


def test_winrate_baseline_unchanged():
    """Итоги N эпизодов совпадают с замороженным эталоном (гард сдвига обучения/баланса)."""
    assert _run_baseline() == BASELINE_WINNERS


def test_baseline_is_deterministic():
    assert _run_baseline() == _run_baseline()
