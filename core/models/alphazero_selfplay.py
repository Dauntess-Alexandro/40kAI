from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch

from core.engine.phases.replay_meta import (
    capture_replay_phase_meta,
    replay_phase_meta_enabled,
    snapshot_cp_before,
)
from core.engine.phases.windowed_selfplay import merge_windowed_meta_into
from core.models.action_contract import ordered_action_keys
from core.models.alphazero_replay import AZTransition
from core.models.utils import convertToDict, unwrap_env
from core.telemetry.stratagem_trace import (
    make_stratagem_tracer_for_train,
    stratagem_trace_actor_ok,
)


@dataclass
class SelfPlayConfig:
    temperature_opening_moves: int = 12
    temperature_opening_value: float = 1.0
    temperature_late_value: float = 0.3


def _state_to_np(state: Any) -> np.ndarray:
    if isinstance(state, dict):
        return np.asarray(list(state.values()), dtype=np.float32)
    return np.asarray(state, dtype=np.float32)


def _mcts_uses_joint_best_child(mcts) -> bool:
    cfg = getattr(mcts, "cfg", None)
    raw = getattr(cfg, "joint_action_from_best_child", False)
    enabled = raw if isinstance(raw, bool) else str(raw).strip().lower() in {"1", "true", "yes", "on"}
    if not enabled:
        return False
    mode = str(getattr(cfg, "candidate_mode", "option") or "option").strip().lower()
    return mode in {"option", "filter", "option_plus"}


def play_episode_with_mcts(
    *,
    env,
    mcts,
    len_model: int,
    config: SelfPlayConfig | None = None,
    enemy_policy_fn: Callable[[Any], dict] | None = None,
    outcome_only: bool = True,
    outcome_value_win: float = 1.0,
    outcome_value_loss: float = -1.0,
    outcome_value_draw: float = -0.25,
    policy_version: int = 0,
    actor_idx: int = -1,
    heartbeat_moves: int = 5,
    fixed_temperature: float | None = None,
    policy_argmax: bool = False,
) -> tuple[list[AZTransition], dict]:
    cfg = config or SelfPlayConfig()
    env_u = unwrap_env(env)
    full_trace_enabled = (
        str(os.getenv("ACTION_TRACE_ENABLED", "0")).strip() == "1"
        or str(os.getenv("VERBOSE_LOGS", "0")).strip() == "1"
    )
    trunc_mode = not full_trace_enabled
    strat_tracer = (
        make_stratagem_tracer_for_train()
        if stratagem_trace_actor_ok(int(actor_idx))
        else None
    )
    from core.engine.turn_sequencing import apply_first_turn_prepend
    from core.envs.warhamEnv import resolve_first_turn_side

    env_u.first_turn_side = resolve_first_turn_side(manual_roll_allowed=False, log_fn=None)
    state, _ = env.reset(options={"m": env_u.model, "e": env_u.enemy, "trunc": trunc_mode})
    done = False
    steps = 0
    records: list[tuple[np.ndarray, list[np.ndarray], Any]] = []
    final_value = 0.0
    last_info: dict = {}

    apply_first_turn_prepend(
        env_u,
        run_enemy_half=lambda: env_u.enemyTurn(trunc=trunc_mode, policy_fn=enemy_policy_fn),
    )
    if bool(getattr(env_u, "game_over", False)):
        done = True
    elif list(getattr(env_u, "turn_order", ["enemy", "model"]))[:1] == ["enemy"]:
        # Враг сходил первым (prepend сдвинул доску) → обновить root-obs, иначе
        # первый MCTS-eval/запись пошёл бы на устаревшем (post-reset) наблюдении.
        state = env_u._get_observation()

    while not done:
        obs_np = _state_to_np(state)
        legal_dict = env_u.get_legal_action_masks_by_head(side="model")
        ordered_keys = ordered_action_keys(int(len_model))
        legal_masks = [legal_dict[k] for k in ordered_keys]
        temp = (
            float(fixed_temperature)
            if fixed_temperature is not None
            else (
                cfg.temperature_opening_value
                if steps < int(cfg.temperature_opening_moves)
                else cfg.temperature_late_value
            )
        )
        if heartbeat_moves > 0 and steps > 0 and (steps % int(heartbeat_moves) == 0):
            print(
                f"[{'GAZ' if str(getattr(mcts.cfg, 'mode', '')).strip().lower() == 'gumbel' else 'AZ'}][ACTOR] "
                f"actor={int(actor_idx)} move={int(steps)} mcts_mode={getattr(mcts.cfg, 'mode', 'proxy')}",
                flush=True,
            )
        pi_targets, action_list, _v = mcts.run(
            obs=obs_np,
            legal_masks_by_head=legal_masks,
            temperature=temp,
            env=env,
            len_model=int(len_model),
            enemy_policy_fn=enemy_policy_fn,
            move_count=int(steps),
            reset_options={"m": env_u.model, "e": env_u.enemy, "trunc": trunc_mode},
        )
        if bool(policy_argmax) and not _mcts_uses_joint_best_child(mcts):
            action_list = [int(np.argmax(pi)) for pi in pi_targets]

        action_dict = convertToDict(torch.tensor([action_list], dtype=torch.long))
        cp_before = snapshot_cp_before(env_u) if replay_phase_meta_enabled() else None
        phase_at_move = str(getattr(env_u, "phase", "") or "")
        step_no = int(steps) + 1
        if strat_tracer is not None:
            next_state, reward, done, trunc, info = strat_tracer.run_model_step(
                env, env_u, step_no, action_dict
            )
        else:
            next_state, reward, done, trunc, info = env.step(action_dict)
        phase_meta = capture_replay_phase_meta(
            env_u,
            action_dict=action_dict,
            cp_before=cp_before,
            phase=phase_at_move,
        )
        phase_meta = merge_windowed_meta_into(
            phase_meta,
            env_u,
            action_dict,
            cp_before=cp_before,
        )
        if isinstance(info, dict):
            last_info = dict(info)
        try:
            if strat_tracer is not None:
                strat_tracer.run_enemy_turn(
                    env_u,
                    step_no,
                    trunc=trunc_mode,
                    policy_fn=enemy_policy_fn,
                )
            else:
                env_u.enemyTurn(trunc=trunc_mode, policy_fn=enemy_policy_fn)
            if bool(getattr(env_u, "game_over", False)):
                done = True
                try:
                    gi = env_u.get_info()
                    if isinstance(gi, dict):
                        last_info = dict(gi)
                except Exception:
                    pass
        except Exception:
            pass
        done = bool(done or trunc)
        records.append((obs_np, pi_targets, phase_meta))
        if not outcome_only:
            final_value = float(np.tanh(float(reward)))
        state = next_state
        steps += 1

    if outcome_only:
        outcome_value_win = float(np.clip(float(outcome_value_win), -1.0, 1.0))
        outcome_value_loss = float(np.clip(float(outcome_value_loss), -1.0, 1.0))
        outcome_value_draw = float(np.clip(float(outcome_value_draw), -1.0, 1.0))
        winner = str(last_info.get("winner", "") or "").strip().lower()
        end_reason = str(last_info.get("end reason", "") or "").strip().lower()
        if winner in {"model", "learner", "ai"} or end_reason == "wipeout_enemy":
            final_value = outcome_value_win
        elif winner in {"enemy", "player", "opponent"} or end_reason == "wipeout_model":
            final_value = outcome_value_loss
        else:
            final_value = outcome_value_draw

    faction = str(getattr(env_u, "model_faction", "") or getattr(env_u, "model", "") or "")
    if hasattr(faction, "__class__") and not isinstance(faction, str):
        faction = str(getattr(env_u, "model_faction", "") or "")
    out: list[AZTransition] = []
    for s, pi, phase_meta in records:
        out.append(
            AZTransition(
                state=s,
                policy_targets=pi,
                value_target=final_value,
                policy_version=int(policy_version),
                faction=str(faction),
                phase_meta=phase_meta,
            )
        )
    if not last_info:
        try:
            gi = env_u.get_info()
            if isinstance(gi, dict):
                last_info = dict(gi)
        except Exception:
            last_info = {}
    if strat_tracer is not None:
        ep_label = (
            f"actor={int(actor_idx)} steps={int(steps)}"
            if int(actor_idx) >= 0
            else f"steps={int(steps)}"
        )
        strat_tracer.log_episode_summary(ep_label, env_unwrapped=env_u)
    return out, last_info
