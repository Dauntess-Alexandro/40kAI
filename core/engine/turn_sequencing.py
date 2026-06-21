"""Порядок двух половин боевого раунда из env.turn_order (Determine First Turn).

Единая точка решения «кто ходит первым» для всех драйверов (eval/train/play/self-play),
чтобы не дублировать порядок и держать счёт раундов согласованным (см.
docs/superpowers/specs/2026-06-21-first-turn-rolloff-design.md).
"""
from __future__ import annotations

from collections.abc import Callable


def run_battle_round(env, *, run_model_half: Callable[[], None], run_enemy_half: Callable[[], None]) -> None:
    """Прогнать обе половины раунда в порядке env.turn_order, short-circuit по game_over."""
    env_u = getattr(env, "unwrapped", env)
    order = list(getattr(env_u, "turn_order", ["enemy", "model"]))
    halves = {"model": run_model_half, "enemy": run_enemy_half}
    for side in order:
        half = halves.get(side)
        if half is None:
            continue
        half()
        if bool(getattr(env_u, "game_over", False)):
            return
