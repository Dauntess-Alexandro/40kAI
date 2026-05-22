from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any, Callable, Optional

import numpy as np
import torch

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


def _state_to_np(state: Any) -> np.ndarray:
    if isinstance(state, dict):
        return np.asarray(list(state.values()), dtype=np.float32)
    return np.asarray(state, dtype=np.float32)


def play_episode_with_gumbel_muzero(
    *,
    env,
    search,
    len_model: int,
    config: Optional[GumbelSelfPlayConfig] = None,
    enemy_policy_fn: Optional[Callable[[Any], dict]] = None,
    policy_version: int = 0,
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

    while not done:
        obs_np = _state_to_np(state)
        legal_dict = env_u.get_legal_action_masks_by_head(side="model")
        ordered_keys = ordered_action_keys(int(len_model))
        legal_masks = [legal_dict[k] for k in ordered_keys]
        _temp = cfg.temperature_opening_value if steps < int(cfg.temperature_opening_moves) else cfg.temperature_late_value

        pi_targets, action_list, value_est = search.run(
            obs=obs_np,
            legal_masks_by_head=legal_masks,
            deterministic=False,
        )

        action_dict = action_tensor_to_dict(torch.tensor([action_list], dtype=torch.long), len_model=int(len_model))
        next_state, reward, done, trunc, info = env.step(action_dict)
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
                "value_est": float(value_est),
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

    out: list[GMZTransition] = []
    for rec in records:
        out.append(
            GMZTransition(
                state=np.asarray(rec["state"], dtype=np.float32),
                action=np.asarray(rec["action"], dtype=np.int64),
                reward=float(rec["reward"]),
                done=bool(rec["done"]),
                policy_targets=[np.asarray(x, dtype=np.float32) for x in rec["policy_targets"]],
                value_target=float(final_value),
                policy_version=int(policy_version),
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
