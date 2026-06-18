"""Stage 8.3: windowed self-play — command через PhaseEngine + плоский action_dict."""

from __future__ import annotations

import json
import os
from collections.abc import Callable

from core.engine.phases import phase_engine
from core.engine.phases.option_generator import command_window
from core.engine.phases.replay_meta import ReplayPhaseMeta
from core.engine.phases.types import ActionKind, ActionOption, DecisionWindow, SubStep


def windowed_selfplay_enabled(explicit: bool | None = None) -> bool:
    if explicit is not None:
        return bool(explicit)
    raw = str(os.getenv("WINDOWED_SELFPLAY", "0")).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def make_command_decide_from_action_dict(
    action_dict: dict | None,
) -> Callable[[DecisionWindow], ActionOption]:
    """Маппинг плоских голов use_cp/cp_on → выбор опции command_window."""
    use_cp = 0
    cp_on = 0
    if isinstance(action_dict, dict):
        use_cp = int(action_dict.get("use_cp", 0) or 0)
        cp_on = int(action_dict.get("cp_on", 0) or 0)

    def decide(window: DecisionWindow) -> ActionOption:
        if use_cp == 1:
            for opt in window.options:
                if (
                    opt.kind is ActionKind.USE_STRATAGEM
                    and opt.unit_idx is not None
                    and int(opt.unit_idx) == cp_on
                ):
                    return opt
        for opt in window.options:
            if opt.kind is ActionKind.PASS:
                return opt
        return window.options[0]

    return decide


def run_model_command_from_action(env, action_dict: dict | None):
    """Командная фаза model через command_window (эквивалент use_cp/cp_on в action)."""
    decide = make_command_decide_from_action_dict(action_dict)
    return phase_engine.run_command(env, "model", decide)


def command_replay_meta_from_action(
    env,
    action_dict: dict | None,
    *,
    cp_before: int | None = None,
) -> ReplayPhaseMeta | None:
    """Метаданные replay для command-окна (8.2 + 8.3)."""
    e = getattr(env, "unwrapped", env)
    win = command_window(e, "model")
    opt = make_command_decide_from_action_dict(action_dict)(win)
    cp_after = int(getattr(e, "modelCP", 0) or 0)
    if cp_before is None:
        cp_before = cp_after
    stratagem_id = None
    if opt.kind is ActionKind.USE_STRATAGEM:
        stratagem_id = str(opt.meta.get("stratagem_id", "") or "") or None
    chosen = json.dumps(
        {
            "kind": str(opt.kind.value),
            "unit_idx": opt.unit_idx,
            "stratagem_id": stratagem_id,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return ReplayPhaseMeta(
        phase="command",
        sub_step=str(SubStep.BATTLE_SHOCK.value),
        window_id=str(win.window_id),
        chosen_option=chosen,
        stratagem_id=stratagem_id,
        cp_before=int(cp_before),
        cp_after=int(cp_after),
    )


def merge_command_meta_into(
    meta: ReplayPhaseMeta | None,
    env,
    action_dict: dict | None,
    *,
    cp_before: int | None,
) -> ReplayPhaseMeta | None:
    if not windowed_selfplay_enabled():
        return meta
    cmd = command_replay_meta_from_action(env, action_dict, cp_before=cp_before)
    if cmd is None:
        return meta
    if meta is None:
        return cmd
    return ReplayPhaseMeta(
        phase=cmd.phase or meta.phase,
        sub_step=cmd.sub_step or meta.sub_step,
        window_id=cmd.window_id or meta.window_id,
        chosen_option=cmd.chosen_option or meta.chosen_option,
        stratagem_id=cmd.stratagem_id or meta.stratagem_id,
        cp_before=cmd.cp_before if cmd.cp_before is not None else meta.cp_before,
        cp_after=cmd.cp_after if cmd.cp_after is not None else meta.cp_after,
    )
