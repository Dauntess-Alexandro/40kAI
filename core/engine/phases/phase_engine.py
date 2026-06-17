from __future__ import annotations

from core.engine.phases.legacy_compiler import default_action_dict
from core.engine.phases.option_generator import command_window, movement_options_for_unit
from core.engine.phases.types import ActionKind, DecisionWindow, Phase, SubStep, Timing


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


def run_movement(env, side, decide):
    """Исполнить фазу движения через окна решений (по юниту).

    decide(window) -> ActionOption: выбирает опцию движения (STAY/MOVE/ADVANCE).
    Индекс reachable из выбранной опции прокидывается в movement_phase (decide_move),
    исполнение делегируется ей (без дублирования логики).
    """
    e = _unwrap(env)
    health = e.unit_health if side == "model" else e.enemy_health
    alive = [i for i, hp in enumerate(health) if hp > 0]
    chosen_idx: dict[int, int] = {}
    for u in alive:
        opts = movement_options_for_unit(e, side, u)
        win = DecisionWindow(
            window_id=f"movement:{side}:{u}",
            owner_side=side,
            phase=Phase.MOVEMENT,
            sub_step=SubStep.MOVE_UNIT,
            timing=Timing.MAIN,
            cursor_unit_idx=int(u),
            options=opts,
        )
        opt = decide(win)
        if opt is not None and opt.param.get("reachable_index") is not None:
            chosen_idx[int(u)] = int(opt.param["reachable_index"])
    action = default_action_dict(len(health))
    return e.movement_phase(
        side,
        action=action,
        battle_shock=[False] * len(health),
        decide_move=lambda i: chosen_idx.get(i, 0),
    )
