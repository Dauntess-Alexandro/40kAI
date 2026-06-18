"""Stage 8.4g: reaction DecisionWindow (opt-in, не в main generate_windows по умолчанию)."""

from __future__ import annotations

import os

from core.engine.phases.stratagems import Trigger, legal_stratagem_options
from core.engine.phases.types import ActionKind, ActionOption, DecisionWindow, Phase, SubStep, Timing


def windowed_reaction_windows_enabled(explicit: bool | None = None) -> bool:
    if explicit is not None:
        return bool(explicit)
    raw = str(os.getenv("WINDOWED_REACTION_WINDOWS", "0")).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def _sub_step_for_phase(phase: Phase) -> SubStep:
    if phase is Phase.SHOOTING:
        return SubStep.PICK_SHOOT_TARGET
    if phase is Phase.CHARGE:
        return SubStep.PICK_CHARGE_TARGET
    if phase is Phase.FIGHT:
        return SubStep.FIGHT_UNIT
    return SubStep.MOVE_UNIT


def build_reaction_windows(
    env,
    reacting_side: str,
    *,
    phase: Phase,
    trigger: Trigger,
    candidate_unit_idxs: list[int] | None = None,
) -> list[DecisionWindow]:
    """Окна реакционных стратагем (Overwatch/Smokescreen/Heroic/Go to Ground).

    По умолчанию выключено (WINDOWED_REACTION_WINDOWS=0). Не вызывается из env.step —
    точка подключения для self-play/MCTS на реакциях (Stage 8.5+).
    """
    if not windowed_reaction_windows_enabled():
        return []
    e = _unwrap(env)
    health = e.unit_health if reacting_side == "model" else e.enemy_health
    units = candidate_unit_idxs if candidate_unit_idxs is not None else [i for i, hp in enumerate(health) if hp > 0]
    windows: list[DecisionWindow] = []
    for u in units:
        opts: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=int(u))]
        opts.extend(
            legal_stratagem_options(
                e,
                reacting_side,
                phase=phase,
                trigger=trigger,
                candidate_unit_idxs=[int(u)],
            )
        )
        if len(opts) <= 1:
            continue
        windows.append(
            DecisionWindow(
                window_id=f"reaction:{reacting_side}:{phase.value}:{trigger.value}:{u}",
                owner_side=str(reacting_side),
                phase=phase,
                sub_step=_sub_step_for_phase(phase),
                timing=Timing.REACTION,
                cursor_unit_idx=int(u),
                options=opts,
                context={"trigger": str(trigger.value)},
            )
        )
    return windows
