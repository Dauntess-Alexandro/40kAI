"""Stage 8.3–8.4: windowed self-play — PhaseEngine + плоский action_dict."""

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
    raw = str(os.getenv("WINDOWED_SELFPLAY", "1")).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def _pick_pass(window: DecisionWindow) -> ActionOption:
    for opt in window.options:
        if opt.kind is ActionKind.PASS:
            return opt
    return window.options[0]


def _action_int(action_dict: dict | None, key: str, default: int = 0) -> int:
    if not isinstance(action_dict, dict):
        return int(default)
    return int(action_dict.get(key, default) or default)


def make_command_decide_from_action_dict(
    action_dict: dict | None,
) -> Callable[[DecisionWindow], ActionOption]:
    """Маппинг strat_command/strat_command_unit → выбор опции command_window."""
    from core.engine.phases.stratagems import stratagem_choice_str
    from core.engine.phases.types import Phase as _Ph

    strat_cmd = _action_int(action_dict, "strat_command", 0)
    strat_unit = _action_int(action_dict, "strat_command_unit", 0)
    choice = stratagem_choice_str(_Ph.COMMAND, strat_cmd)

    def decide(window: DecisionWindow) -> ActionOption:
        if choice and choice != "none":
            for opt in window.options:
                if (
                    opt.kind is ActionKind.USE_STRATAGEM
                    and opt.meta.get("stratagem_id") == choice
                    and opt.unit_idx is not None
                    and int(opt.unit_idx) == strat_unit
                ):
                    return opt
        return _pick_pass(window)

    return decide


def make_movement_decide_from_action_dict(
    action_dict: dict | None,
) -> Callable[[DecisionWindow], ActionOption]:
    """Маппинг move_num_{unit} → reachable_index в окне движения."""

    def decide(window: DecisionWindow) -> ActionOption:
        u = window.cursor_unit_idx
        if u is None:
            return window.options[0]
        want = _action_int(action_dict, f"move_num_{int(u)}", 0)
        for opt in window.options:
            if int(opt.param.get("reachable_index", -1)) == want:
                return opt
        for opt in window.options:
            if opt.kind is ActionKind.STAY:
                return opt
        return window.options[0]

    return decide


def make_shooting_decide_from_action_dict(
    action_dict: dict | None,
) -> Callable[[DecisionWindow], ActionOption]:
    """Маппинг shoot_num_{unit} → local_rank в окне стрельбы юнита."""

    def decide(window: DecisionWindow) -> ActionOption:
        u = window.cursor_unit_idx
        if u is None:
            return _pick_pass(window)
        shoot_rank = _action_int(action_dict, f"shoot_num_{int(u)}", 0)
        for opt in window.options:
            if opt.kind is ActionKind.SHOOT and int(opt.param.get("local_rank", -1)) == shoot_rank:
                return opt
        return _pick_pass(window)

    return decide


def make_charge_decide_from_action_dict(
    action_dict: dict | None,
) -> Callable[[DecisionWindow], ActionOption]:
    """Маппинг attack/charge_num_{unit} → CHARGE-опция (глобальный индекс врага)."""
    attack = _action_int(action_dict, "attack", 0)

    def decide(window: DecisionWindow) -> ActionOption:
        if attack != 1:
            return _pick_pass(window)
        u = window.cursor_unit_idx
        if u is None:
            return _pick_pass(window)
        charge_target = _action_int(action_dict, f"charge_num_{int(u)}", 0)
        for opt in window.options:
            if opt.kind is ActionKind.CHARGE and opt.target_idx is not None:
                if int(opt.target_idx) == charge_target:
                    return opt
        return _pick_pass(window)

    return decide


def make_fight_decide_from_action_dict(
    env,
    action_dict: dict | None,
) -> Callable[[DecisionWindow], ActionOption]:
    """Маппинг _pending_fight_stratagem_plan → fight-окна (option/MCTS)."""
    e = _unwrap(env)
    plan = dict(getattr(e, "_pending_fight_stratagem_plan", None) or {})

    def decide(window: DecisionWindow) -> ActionOption:
        u = window.cursor_unit_idx
        sid = plan.get(u) if u is not None else None
        if sid:
            sid_s = str(sid)
            for opt in window.options:
                if opt.kind is ActionKind.USE_STRATAGEM and str(opt.meta.get("stratagem_id", "")) == sid_s:
                    return opt
        return _pick_pass(window)

    return decide


def run_model_command_from_action(env, action_dict: dict | None):
    """Командная фаза model через command_window (эквивалент use_cp/cp_on в action)."""
    decide = make_command_decide_from_action_dict(action_dict)
    return phase_engine.run_command(env, "model", decide)


def run_model_movement_from_action(env, action_dict: dict | None, state=None):
    decide = make_movement_decide_from_action_dict(action_dict)
    return phase_engine.run_movement(env, "model", decide, state, base_action=action_dict)


def run_model_shooting_from_action(env, action_dict: dict | None, state=None):
    decide = make_shooting_decide_from_action_dict(action_dict)
    return phase_engine.run_shooting(env, "model", decide, state, base_action=action_dict)


def run_model_charge_from_action(env, action_dict: dict | None, state=None):
    decide = make_charge_decide_from_action_dict(action_dict)
    return phase_engine.run_charge(env, "model", decide, state, base_action=action_dict)


def run_model_fight_from_action(env, action_dict: dict | None, state=None):
    e = _unwrap(env)
    decide = make_fight_decide_from_action_dict(e, action_dict)
    e._pending_fight_stratagem_plan = None
    return phase_engine.run_fight(env, "model", decide, state)


def run_model_turn_from_action(env, action_dict: dict | None):
    """Полный ход model: command → movement → shooting → charge → fight."""
    state = run_model_command_from_action(env, action_dict)
    state = run_model_movement_from_action(env, action_dict, state)
    state = run_model_shooting_from_action(env, action_dict, state)
    state = run_model_charge_from_action(env, action_dict, state)
    return run_model_fight_from_action(env, action_dict, state)


def _option_summary(opt: ActionOption) -> dict:
    sid = None
    if opt.kind is ActionKind.USE_STRATAGEM:
        sid = str(opt.meta.get("stratagem_id", "") or "") or None
    return {
        "kind": str(opt.kind.value),
        "unit_idx": opt.unit_idx,
        "stratagem_id": sid,
    }


def command_replay_meta_from_action(
    env,
    action_dict: dict | None,
    *,
    cp_before: int | None = None,
) -> ReplayPhaseMeta | None:
    """Метаданные replay для command-окна (8.2 + 8.3)."""
    e = _unwrap(env)
    win = command_window(e, "model")
    opt = make_command_decide_from_action_dict(action_dict)(win)
    cp_after = int(getattr(e, "modelCP", 0) or 0)
    if cp_before is None:
        cp_before = cp_after
    stratagem_id = None
    if opt.kind is ActionKind.USE_STRATAGEM:
        stratagem_id = str(opt.meta.get("stratagem_id", "") or "") or None
    chosen = json.dumps(_option_summary(opt), ensure_ascii=False, sort_keys=True)
    return ReplayPhaseMeta(
        phase="command",
        sub_step=str(SubStep.BATTLE_SHOCK.value),
        window_id=str(win.window_id),
        chosen_option=chosen,
        stratagem_id=stratagem_id,
        cp_before=int(cp_before),
        cp_after=int(cp_after),
    )


def turn_replay_meta_from_action(
    env,
    action_dict: dict | None,
    *,
    cp_before: int | None = None,
) -> ReplayPhaseMeta | None:
    """Метаданные replay для полного windowed-хода model."""
    cmd = command_replay_meta_from_action(env, action_dict, cp_before=cp_before)
    if cmd is None:
        return None
    e = _unwrap(env)
    alive = [i for i, hp in enumerate(e.unit_health) if hp > 0]
    summary = {
        "command": cmd.window_id,
        "movement": [f"movement:model:{i}" for i in alive],
        "shooting": [f"shooting:model:{i}" for i in alive],
        "charge": [f"charge:model:{i}" for i in alive],
        "fight": [f"fight:model:{i}" for i in alive if e.unitInAttack[i][0] == 1],
    }
    return ReplayPhaseMeta(
        phase="windowed_turn",
        sub_step=cmd.sub_step,
        window_id="windowed_turn:model",
        chosen_option=json.dumps(summary, ensure_ascii=False, sort_keys=True),
        stratagem_id=cmd.stratagem_id,
        cp_before=cmd.cp_before,
        cp_after=cmd.cp_after,
    )


def merge_command_meta_into(
    meta: ReplayPhaseMeta | None,
    env,
    action_dict: dict | None,
    *,
    cp_before: int | None,
) -> ReplayPhaseMeta | None:
    return merge_windowed_meta_into(meta, env, action_dict, cp_before=cp_before)


def merge_windowed_meta_into(
    meta: ReplayPhaseMeta | None,
    env,
    action_dict: dict | None,
    *,
    cp_before: int | None,
) -> ReplayPhaseMeta | None:
    if not windowed_selfplay_enabled():
        return meta
    turn = turn_replay_meta_from_action(env, action_dict, cp_before=cp_before)
    if turn is None:
        return meta
    if meta is None:
        return turn
    return ReplayPhaseMeta(
        phase=turn.phase or meta.phase,
        sub_step=turn.sub_step or meta.sub_step,
        window_id=turn.window_id or meta.window_id,
        chosen_option=turn.chosen_option or meta.chosen_option,
        stratagem_id=turn.stratagem_id or meta.stratagem_id,
        cp_before=turn.cp_before if turn.cp_before is not None else meta.cp_before,
        cp_after=turn.cp_after if turn.cp_after is not None else meta.cp_after,
    )
