from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any, Callable, Optional, Protocol

import numpy as np
import torch

from core.engine.phases.replay_meta import (
    capture_replay_phase_meta,
    replay_phase_meta_enabled,
    snapshot_cp_before,
)
from core.engine.phases.windowed_selfplay import merge_command_meta_into
from core.models.action_contract import action_tensor_to_dict, ordered_action_keys
from core.models.gumbel_muzero_replay import GMZTransition
from core.models.utils import unwrap_env


@dataclass
class GumbelSelfPlayConfig:
    temperature_opening_moves: int = 12
    temperature_opening_value: float = 1.0
    temperature_late_value: float = 0.25
    outcome_only: bool = True
    outcome_value_win: float = 1.0
    outcome_value_loss: float = -1.0
    outcome_value_draw: float = -0.25


class GMZInferenceFn(Protocol):
    """(obs, masks, *, is_new_episode, step, episode_id) -> pi, beh, actions, value, policy_version."""

    def __call__(
        self,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        *,
        is_new_episode: bool,
        step_in_episode: int,
        episode_id: int,
    ) -> tuple[list[np.ndarray], list[np.ndarray], list[int], float, int]:
        ...


def _state_to_np(state: Any) -> np.ndarray:
    if isinstance(state, dict):
        return np.asarray(list(state.values()), dtype=np.float32)
    return np.asarray(state, dtype=np.float32)


def play_episode_with_gumbel_muzero(
    *,
    env,
    search=None,
    inference_fn: Optional[GMZInferenceFn] = None,
    len_model: int,
    config: Optional[GumbelSelfPlayConfig] = None,
    enemy_policy_fn: Optional[Callable[[Any], dict]] = None,
    policy_version: int = 0,
    episode_id: int = 0,
    deterministic: bool = False,
) -> tuple[list[GMZTransition], dict]:
    cfg = config or GumbelSelfPlayConfig()
    env_u = unwrap_env(env)
    full_trace_enabled = (
        str(os.getenv("ACTION_TRACE_ENABLED", "0")).strip() == "1"
        or str(os.getenv("VERBOSE_LOGS", "0")).strip() == "1"
    )
    trunc_mode = not full_trace_enabled

    state, _ = env.reset(options={"m": env_u.model, "e": env_u.enemy, "trunc": trunc_mode})
    done = False
    last_info: dict = {}
    steps = 0
    records: list[dict] = []
    final_value = 0.0

    if inference_fn is None and search is None:
        raise ValueError("play_episode_with_gumbel_muzero: нужен search или inference_fn")

    while not done:
        obs_np = _state_to_np(state)
        legal_dict = env_u.get_legal_action_masks_by_head(side="model")
        ordered_keys = ordered_action_keys(int(len_model))
        legal_masks = [legal_dict[k] for k in ordered_keys]
        _temp = cfg.temperature_opening_value if steps < int(cfg.temperature_opening_moves) else cfg.temperature_late_value

        step_policy_version = int(policy_version)
        if inference_fn is not None:
            pi_targets, behavior_logits, action_list, value_est, step_policy_version = inference_fn(
                obs_np,
                legal_masks,
                is_new_episode=(steps == 0),
                step_in_episode=steps,
                episode_id=int(episode_id),
            )
        else:
            pi_targets, behavior_logits, action_list, value_est = search.run(
                obs=obs_np,
                legal_masks_by_head=legal_masks,
                deterministic=bool(deterministic),
            )

        action_dict = action_tensor_to_dict(torch.tensor([action_list], dtype=torch.long), len_model=int(len_model))
        cp_before = snapshot_cp_before(env_u) if replay_phase_meta_enabled() else None
        phase_at_move = str(getattr(env_u, "phase", "") or "")
        next_state, reward, done, trunc, info = env.step(action_dict)
        phase_meta = capture_replay_phase_meta(
            env_u,
            action_dict=action_dict,
            cp_before=cp_before,
            phase=phase_at_move,
        )
        phase_meta = merge_command_meta_into(
            phase_meta,
            env_u,
            action_dict,
            cp_before=cp_before,
        )
        if isinstance(info, dict):
            last_info = dict(info)
        try:
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
        records.append(
            {
                "state": obs_np,
                "action": np.asarray(action_list, dtype=np.int64),
                "reward": float(reward),
                "done": bool(done),
                "policy_targets": [np.asarray(x, dtype=np.float32) for x in pi_targets],
                "behavior_logits": [np.asarray(x, dtype=np.float32) for x in behavior_logits],
                "value_est": float(value_est),
                "legal_masks_by_head": [np.asarray(x, dtype=np.float32) for x in legal_masks],  # B2: for reanalysis
                "phase_meta": phase_meta,
            }
        )
        final_value = float(np.tanh(float(value_est)))
        state = next_state
        steps += 1

    if bool(cfg.outcome_only):
        outcome_value_win = float(np.clip(float(cfg.outcome_value_win), -1.0, 1.0))
        outcome_value_loss = float(np.clip(float(cfg.outcome_value_loss), -1.0, 1.0))
        outcome_value_draw = float(np.clip(float(cfg.outcome_value_draw), -1.0, 1.0))
        winner = str(last_info.get("winner", "") or "").strip().lower()
        end_reason = str(last_info.get("end reason", "") or "").strip().lower()
        if winner in {"model", "learner", "ai"} or end_reason == "wipeout_enemy":
            final_value = outcome_value_win
        elif winner in {"enemy", "player", "opponent"} or end_reason == "wipeout_model":
            final_value = outcome_value_loss
        else:
            final_value = outcome_value_draw
    else:
        # When outcome_only=False, still clip via atom range so value_target stays in distribution support
        from core.models.gumbel_muzero_model import VALUE_ATOM_MIN, VALUE_ATOM_MAX
        final_value = float(np.clip(final_value, VALUE_ATOM_MIN, VALUE_ATOM_MAX))

    out: list[GMZTransition] = []
    for rec in records:
        out.append(
            GMZTransition(
                state=np.asarray(rec["state"], dtype=np.float32),
                action=np.asarray(rec["action"], dtype=np.int64),
                reward=float(rec["reward"]),
                done=bool(rec["done"]),
                policy_targets=[np.asarray(x, dtype=np.float32) for x in rec["policy_targets"]],
                behavior_logits=[np.asarray(x, dtype=np.float32) for x in rec["behavior_logits"]],
                value_target=float(final_value),
                legal_masks_by_head=rec.get("legal_masks_by_head", []),  # B2: for real-search reanalysis
                policy_version=int(step_policy_version),
                phase_meta=rec.get("phase_meta"),
            )
        )

    if not last_info:
        try:
            gi = env_u.get_info()
            if isinstance(gi, dict):
                last_info = dict(gi)
        except Exception:
            last_info = {}
    return out, last_info
