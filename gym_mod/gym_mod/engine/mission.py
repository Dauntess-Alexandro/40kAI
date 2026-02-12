"""Only War mission logic."""
from __future__ import annotations

from typing import Callable, List, Tuple

import reward_config as reward_cfg

MISSION_NAME = "Only War"
ONLY_WAR_BOARD_WIDTH_INCH = 60
ONLY_WAR_BOARD_HEIGHT_INCH = 40
ONLY_WAR_CENTER_OBJECTIVE_ID = 1
# TODO(Only War): support post-deploy units ("set up after both armies deployed").
# Currently no post-deploy units supported.
MAX_BATTLE_ROUNDS = 10
START_SCORING_ROUND = reward_cfg.VP_START_SCORING_ROUND
VP_CAP_PER_COMMAND = reward_cfg.VP_CAP_PER_COMMAND


def controlled_objectives(env, side: str) -> Tuple[int, List[int]]:
    """
    Returns (count, indices) of objectives controlled by the given side.
    Uses current OC totals on each objective.
    """
    if side not in ("model", "enemy"):
        raise ValueError(f"Unknown side: {side}")

    model_totals = getattr(env, "model_obj_oc", None)
    enemy_totals = getattr(env, "enemy_obj_oc", None)
    if model_totals is None or enemy_totals is None:
        raise AttributeError("Objective OC totals not available on env")

    controlled = []
    for idx in range(len(model_totals)):
        model_oc = int(model_totals[idx])
        enemy_oc = int(enemy_totals[idx])
        if side == "model" and model_oc > enemy_oc:
            controlled.append(idx)
        elif side == "enemy" and enemy_oc > model_oc:
            controlled.append(idx)

    return len(controlled), controlled


def score_end_of_command_phase(env, side: str, log_fn: Callable[[str], None] | None = None) -> int:
    """
    Only War scoring:
    - if env.battle_round < START_SCORING_ROUND -> 0
    - otherwise gained = min(VP_CAP_PER_COMMAND, count_controlled)
    - adds gained to env.modelVP/env.enemyVP
    - returns gained
    """
    if hasattr(env, "refresh_objective_control"):
        env.refresh_objective_control()

    count_controlled, indices = controlled_objectives(env, side)

    if env.battle_round < START_SCORING_ROUND:
        gained = 0
    else:
        gained = min(VP_CAP_PER_COMMAND, count_controlled)

    if side == "model":
        vp_before = env.modelVP
        env.modelVP += gained
        vp_after = env.modelVP
    else:
        vp_before = env.enemyVP
        env.enemyVP += gained
        vp_after = env.enemyVP

    if log_fn is not None:
        side_label = side.upper()
        cap_note = " (cap)" if gained == VP_CAP_PER_COMMAND and count_controlled > VP_CAP_PER_COMMAND else ""
        display_indices = [idx + 1 for idx in indices]
        indices_note = f", objectives={display_indices}" if display_indices else ""
        objective_id = ONLY_WAR_CENTER_OBJECTIVE_ID
        center = None
        if getattr(env, "coordsOfOM", None):
            center = env.coordsOfOM[0]

        model_oc = int(env.model_obj_oc[0]) if len(getattr(env, "model_obj_oc", [])) > 0 else 0
        enemy_oc = int(env.enemy_obj_oc[0]) if len(getattr(env, "enemy_obj_oc", [])) > 0 else 0
        controlled_side = "none"
        if model_oc > enemy_oc:
            controlled_side = "model"
        elif enemy_oc > model_oc:
            controlled_side = "enemy"

        attacker_side = getattr(env, "attacker_side", None)
        defender_side = getattr(env, "defender_side", None)
        controlled_role = controlled_side
        if controlled_side == attacker_side:
            controlled_role = "attacker"
        elif controlled_side == defender_side:
            controlled_role = "defender"

        center_note = "center=(n/a,n/a)"
        if center is not None and len(center) >= 2:
            # env coords are stored as [row, col] -> x=col, y=row
            center_note = f"center=({int(center[1])},{int(center[0])})"

        log_fn(
            f"[{side_label}] {MISSION_NAME}: end of Command phase -> "
            f"controlled={count_controlled}, gained={gained}{cap_note}, VP: {vp_before} -> {vp_after}{indices_note}; "
            f"objectives=[{objective_id}], {center_note}, controlled_by={controlled_role}"
        )

    return gained


def check_end_of_battle(env) -> Tuple[bool, str, str | None]:
    """
    Returns (game_over, reason, winner).
    reason: "wipeout_model" / "wipeout_enemy" / "turn_limit"
    winner: "model" / "enemy" / None (draw)
    """
    model_wiped = sum(env.unit_health) <= 0
    enemy_wiped = sum(env.enemy_health) <= 0

    if model_wiped and enemy_wiped:
        return True, "wipeout_model", None
    if model_wiped:
        return True, "wipeout_model", "enemy"
    if enemy_wiped:
        return True, "wipeout_enemy", "model"

    if env.battle_round > MAX_BATTLE_ROUNDS:
        if env.modelVP > env.enemyVP:
            winner = "model"
        elif env.enemyVP > env.modelVP:
            winner = "enemy"
        else:
            winner = None
        return True, "turn_limit", winner

    return False, "", None


def apply_end_of_battle(env, log_fn: Callable[[str], None] | None = None) -> Tuple[bool, str, str | None]:
    """
    Wrapper: calls check_end_of_battle(), sets env.game_over if needed,
    logs winner/draw, returns the same tuple.
    """
    game_over, reason, winner = check_end_of_battle(env)
    if game_over and not env.game_over:
        env.game_over = True
        if log_fn is not None:
            if reason == "turn_limit":
                if winner is None:
                    log_fn(f"Game over: turn_limit -> draw (VP {env.modelVP}-{env.enemyVP})")
                else:
                    log_fn(
                        f"Game over: turn_limit (after BR{MAX_BATTLE_ROUNDS}) -> winner={winner} "
                        f"(VP {env.modelVP}-{env.enemyVP})"
                    )
            else:
                if winner is None:
                    log_fn(f"Game over: {reason} -> draw")
                else:
                    log_fn(f"Game over: {reason} -> winner={winner}")
    return game_over, reason, winner
