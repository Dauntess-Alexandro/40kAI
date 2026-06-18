from __future__ import annotations

from core.engine.phases import stratagem_engine
from core.engine.phases.legacy_compiler import default_action_dict
from core.engine.phases.option_generator import (
    charge_options_for_unit,
    command_window,
    fight_stratagem_options_for_unit,
    movement_options_for_unit,
    shooting_options_for_unit,
)
from core.engine.phases.types import ActionKind, DecisionWindow, Phase, PhaseTurnState, SubStep, Timing


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def _health_for_side(env, side):
    e = _unwrap(env)
    return e.unit_health if side == "model" else e.enemy_health


def _ensure_state(env, side, state: PhaseTurnState | None = None) -> PhaseTurnState:
    if state is not None:
        return state
    health = _health_for_side(env, side)
    return PhaseTurnState(
        side=str(side),
        battle_shock=[False] * len(health),
        advanced_flags=[False] * len(health),
    )


def _invalidate(env, reason: str) -> None:
    e = _unwrap(env)
    fn = getattr(e, "_invalidate_target_cache", None)
    if callable(fn):
        fn(reason)


def _sync_positions(env) -> None:
    e = _unwrap(env)
    fn = getattr(e, "_sync_model_positions_to_anchors", None)
    if callable(fn):
        fn()


def run_command(env, side, decide, state: PhaseTurnState | None = None) -> PhaseTurnState:
    """Исполнить командную фазу через окно решений.

    decide(window) -> ActionOption: выбирает одну опцию окна (PASS или USE_STRATAGEM).
    Исполнение делегируется command_phase (decide_bravery), без дублирования логики.
    """
    e = _unwrap(env)
    state = _ensure_state(e, side, state)
    win = command_window(e, side)
    chosen = decide(win)
    chosen_units: set[int] = set()
    if chosen is not None and chosen.kind is ActionKind.USE_STRATAGEM and chosen.unit_idx is not None:
        chosen_units.add(int(chosen.unit_idx))
    result = e.command_phase(side, decide_bravery=lambda i: i in chosen_units)
    if isinstance(result, tuple):
        battle_shock = result[0] if len(result) > 0 else []
        reward_delta = float(result[1] or 0.0) if len(result) > 1 else 0.0
    else:
        battle_shock = result if result is not None else state.battle_shock
        reward_delta = 0.0
    state.battle_shock = list(battle_shock or [])
    state.reward_delta += reward_delta
    state.info["command_reward_delta"] = reward_delta
    return state


def run_movement(
    env,
    side,
    decide,
    state: PhaseTurnState | None = None,
    *,
    base_action: dict | None = None,
) -> PhaseTurnState:
    """Исполнить фазу движения через окна решений (по юниту).

    decide(window) -> ActionOption: выбирает опцию движения (STAY/MOVE/ADVANCE).
    Индекс reachable из выбранной опции прокидывается в movement_phase (decide_move),
    исполнение делегируется ей (без дублирования логики).
    """
    e = _unwrap(env)
    state = _ensure_state(e, side, state)
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
    action = dict(base_action) if base_action is not None else default_action_dict(len(health))
    if base_action is not None:
        decide_move = lambda i: int(action.get(f"move_num_{i}", 0))  # noqa: E731
    else:
        decide_move = lambda i: chosen_idx.get(i, 0)  # noqa: E731
    result = e.movement_phase(
        side,
        action=action,
        battle_shock=list(state.battle_shock or [False] * len(health)),
        decide_move=decide_move,
    )
    if isinstance(result, tuple):
        advanced_flags = result[0] if len(result) > 0 else []
        reward_delta = float(result[1] or 0.0) if len(result) > 1 else 0.0
        if len(result) > 2:
            state.info["movement_meta"] = result[2]
    else:
        advanced_flags = result if result is not None else state.advanced_flags
        reward_delta = 0.0
    state.advanced_flags = list(advanced_flags or [False] * len(health))
    state.reward_delta += reward_delta
    state.info["movement_reward_delta"] = reward_delta
    _sync_positions(e)
    _invalidate(e, f"phase_engine_after_movement:{side}")
    return state


def run_shooting(
    env,
    side,
    decide,
    state: PhaseTurnState | None = None,
    *,
    base_action: dict | None = None,
) -> PhaseTurnState:
    """Исполнить фазу стрельбы через окна решений (по юниту).

    decide(window) -> ActionOption: SHOOT (с param local_rank) или PASS.
    Для PASS-юнитов decide_shoot возвращает -1 (ранг вне диапазона → стрельба пропускается).
    """
    e = _unwrap(env)
    state = _ensure_state(e, side, state)
    health = e.unit_health if side == "model" else e.enemy_health
    alive = [i for i, hp in enumerate(health) if hp > 0]
    chosen_rank: dict[int, int] = {}
    for u in alive:
        opts = shooting_options_for_unit(e, side, u)
        win = DecisionWindow(
            window_id=f"shooting:{side}:{u}",
            owner_side=side,
            phase=Phase.SHOOTING,
            sub_step=SubStep.PICK_SHOOT_TARGET,
            timing=Timing.MAIN,
            cursor_unit_idx=int(u),
            options=opts,
        )
        opt = decide(win)
        if opt is not None and opt.kind is ActionKind.SHOOT and opt.param.get("local_rank") is not None:
            chosen_rank[int(u)] = int(opt.param["local_rank"])
    action = dict(base_action) if base_action is not None else default_action_dict(len(health))
    decide_shoot = None if base_action is not None else (lambda i: chosen_rank.get(i, -1))
    result = e.shooting_phase(
        side,
        advanced_flags=list(state.advanced_flags or [False] * len(health)),
        action=action,
        decide_shoot=decide_shoot,
    )
    reward_delta = float(result or 0.0) if result is not None else 0.0
    state.reward_delta += reward_delta
    state.info["shooting_reward_delta"] = reward_delta
    return state


def run_charge(
    env,
    side,
    decide,
    state: PhaseTurnState | None = None,
    *,
    base_action: dict | None = None,
) -> PhaseTurnState:
    """Исполнить фазу чарджа через окна решений (по юниту).

    decide(window) -> ActionOption: CHARGE (target_idx — глобальный id врага) или PASS.
    Для PASS-юнитов decide_charge возвращает None (чардж не объявляется).
    """
    e = _unwrap(env)
    state = _ensure_state(e, side, state)
    health = e.unit_health if side == "model" else e.enemy_health
    alive = [i for i, hp in enumerate(health) if hp > 0]
    chosen_target: dict[int, int] = {}
    for u in alive:
        opts = charge_options_for_unit(e, side, u)
        win = DecisionWindow(
            window_id=f"charge:{side}:{u}",
            owner_side=side,
            phase=Phase.CHARGE,
            sub_step=SubStep.PICK_CHARGE_TARGET,
            timing=Timing.MAIN,
            cursor_unit_idx=int(u),
            options=opts,
        )
        opt = decide(win)
        if opt is not None and opt.kind is ActionKind.CHARGE and opt.target_idx is not None:
            chosen_target[int(u)] = int(opt.target_idx)
    action = dict(base_action) if base_action is not None else default_action_dict(len(health))
    decide_charge = None if base_action is not None else (lambda i: chosen_target.get(i))
    result = e.charge_phase(
        side,
        advanced_flags=list(state.advanced_flags or [False] * len(health)),
        action=action,
        decide_charge=decide_charge,
    )
    reward_delta = float(result or 0.0) if result is not None else 0.0
    state.reward_delta += reward_delta
    state.info["charge_reward_delta"] = reward_delta
    return state


def run_fight(env, side, decide, state: PhaseTurnState | None = None) -> PhaseTurnState:
    """Исполнить фазу боя через окна решений (по eligible-бойцу).

    decide(window) -> ActionOption: USE_STRATAGEM (fight-phase, напр. hungry_void) или PASS.
    Выбранные стратагемы применяются через stratagem_engine.apply ДО боя — fight_phase
    читает их из active_stratagem_effects (_fight_effects_for_attacker).
    """
    e = _unwrap(env)
    state = _ensure_state(e, side, state)
    health = e.unit_health if side == "model" else e.enemy_health
    in_attack = e.unitInAttack if side == "model" else e.enemyInAttack
    eligible = [i for i in range(len(health)) if health[i] > 0 and in_attack[i][0] == 1]
    chosen: dict[int, str] = {}
    for u in eligible:
        opts = fight_stratagem_options_for_unit(e, side, u)
        win = DecisionWindow(
            window_id=f"fight:{side}:{u}",
            owner_side=side,
            phase=Phase.FIGHT,
            sub_step=SubStep.FIGHT_UNIT,
            timing=Timing.MAIN,
            cursor_unit_idx=int(u),
            options=opts,
        )
        opt = decide(win)
        if opt is not None and opt.kind is ActionKind.USE_STRATAGEM and opt.meta.get("stratagem_id"):
            chosen[int(u)] = str(opt.meta["stratagem_id"])
    for u, sid in chosen.items():
        stratagem_engine.apply(e, side, sid, u, phase="fight")
    result = e.fight_phase(side)
    reward_delta = float(result or 0.0) if result is not None else 0.0
    state.reward_delta += reward_delta
    state.info["fight_reward_delta"] = reward_delta
    return state
