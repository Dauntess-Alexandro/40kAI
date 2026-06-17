from __future__ import annotations

from core.engine.phases.option_generator import command_window
from core.engine.phases.types import ActionKind


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def run_command(env, side, decide):
    """Исполнить командную фазу через окно решений.

    decide(window) -> ActionOption: выбирает одну опцию окна (PASS или USE_STRATAGEM).
    Исполнение делегируется command_phase (decide_bravery), без дублирования логики.
    """
    e = _unwrap(env)
    win = command_window(e, side)
    chosen = decide(win)
    chosen_units: set[int] = set()
    if chosen is not None and chosen.kind is ActionKind.USE_STRATAGEM and chosen.unit_idx is not None:
        chosen_units.add(int(chosen.unit_idx))
    return e.command_phase(side, decide_bravery=lambda i: i in chosen_units)
