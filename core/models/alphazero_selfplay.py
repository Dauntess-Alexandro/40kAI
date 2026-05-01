from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any, Callable, Optional

import numpy as np
import torch

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_replay import AZTransition
from core.models.utils import convertToDict


@dataclass
class SelfPlayConfig:
    temperature_opening_moves: int = 12
    temperature_opening_value: float = 1.0
    temperature_late_value: float = 0.2


def _state_to_np(state: Any) -> np.ndarray:
    if isinstance(state, dict):
        return np.asarray(list(state.values()), dtype=np.float32)
    return np.asarray(state, dtype=np.float32)


def play_episode_with_mcts(
    *,
    env,
    mcts,
    len_model: int,
    config: SelfPlayConfig | None = None,
    enemy_policy_fn: Optional[Callable[[Any], dict]] = None,
    outcome_only: bool = True,
    outcome_value_win: float = 1.0,
    outcome_value_loss: float = -1.0,
    outcome_value_draw: float = -0.25,
) -> tuple[list[AZTransition], dict]:
    cfg = config or SelfPlayConfig()
    env_u = getattr(env, "unwrapped", env)
    full_trace_enabled = (
        str(os.getenv("ACTION_TRACE_ENABLED", "0")).strip() == "1"
        or str(os.getenv("VERBOSE_LOGS", "0")).strip() == "1"
    )
    trunc_mode = not full_trace_enabled
    state, _ = env.reset(options={"m": env_u.model, "e": env_u.enemy, "trunc": trunc_mode})
    done = False
    steps = 0
    records: list[tuple[np.ndarray, list[np.ndarray]]] = []
    final_value = 0.0
    last_info: dict = {}

    while not done:
        obs_np = _state_to_np(state)
        legal_dict = env_u.get_legal_action_masks_by_head(side="model")
        ordered_keys = ordered_action_keys(int(len_model))
        legal_masks = [legal_dict[k] for k in ordered_keys]
        temp = cfg.temperature_opening_value if steps < int(cfg.temperature_opening_moves) else cfg.temperature_late_value
        pi_targets, action_list, _v = mcts.run(
            obs=obs_np,
            legal_masks_by_head=legal_masks,
            temperature=temp,
            env=env,
            len_model=int(len_model),
            enemy_policy_fn=enemy_policy_fn,
        )

        action_dict = convertToDict(torch.tensor([action_list], dtype=torch.long))
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
        records.append((obs_np, pi_targets))
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

    out: list[AZTransition] = []
    for s, pi in records:
        out.append(AZTransition(state=s, policy_targets=pi, value_target=final_value))
    if not last_info:
        try:
            gi = env_u.get_info()
            if isinstance(gi, dict):
                last_info = dict(gi)
        except Exception:
            last_info = {}
    return out, last_info
