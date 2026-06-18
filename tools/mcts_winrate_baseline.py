#!/usr/bin/env python
"""Winrate-baseline harness: сравнение MCTS candidate_mode на одной frozen-сети.

Пример:
  python tools/mcts_winrate_baseline.py --episodes 50 --seed 1000 --modes joint,filter,option
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import AlphaZeroPolicyValueNet
from tests.engine.phases._helpers import build_env


def _obs_from_env(env) -> np.ndarray:
    state = env._get_observation()
    if isinstance(state, dict):
        return np.asarray(list(state.values()), dtype=np.float32)
    return np.asarray(state, dtype=np.float32)


def _episode_outcome(env, *, mcts, len_model: int, seed: int) -> str:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    done = False
    steps = 0
    last_info: dict = {}
    while not done and steps < 200:
        obs = _obs_from_env(env)
        legal_dict = env.get_legal_action_masks_by_head("model")
        legal = [legal_dict[k] for k in ordered_action_keys(len_model)]
        _pi, action_list, _v = mcts.run(
            obs=obs,
            legal_masks_by_head=legal,
            temperature=0.1,
            env=env,
            len_model=len_model,
            move_count=steps,
            reset_options={"m": env.model, "e": env.enemy, "trunc": True},
        )
        from core.models.utils import convertToDict

        action_dict = convertToDict(torch.tensor([action_list], dtype=torch.long))
        _obs, _r, done, trunc, info = env.step(action_dict)
        if isinstance(info, dict):
            last_info = dict(info)
        if not done:
            env.enemyTurn(trunc=True)
            done = bool(getattr(env, "game_over", False))
        done = bool(done or trunc)
        steps += 1

    winner = str(last_info.get("winner", "") or "").strip().lower()
    end_reason = str(last_info.get("end reason", "") or "").strip().lower()
    if winner in {"model", "learner", "ai"} or end_reason == "wipeout_enemy":
        return "win"
    if winner in {"enemy", "player", "opponent"} or end_reason == "wipeout_model":
        return "loss"
    return "draw"


def run_baseline(*, episodes: int, seed: int, modes: list[str]) -> dict:
    env = build_env()
    len_model = len(env.unit_health)
    n_actions = [int(env.action_space.spaces[k].n) for k in ordered_action_keys(len_model)]
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = int(_obs_from_env(env).size)
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)

    results: dict[str, dict[str, float]] = {}
    for mode in modes:
        mcts = AlphaZeroFactorizedMCTS(
            net,
            config=MCTSConfig(
                simulations=16,
                mode="tree",
                max_depth=1,
                dirichlet_eps=0.0,
                top_k_per_head=6,
                candidate_mode=str(mode),
            ),
            device=torch.device("cpu"),
        )
        wins = losses = draws = 0
        for ep in range(int(episodes)):
            outcome = _episode_outcome(env, mcts=mcts, len_model=len_model, seed=int(seed) + ep)
            if outcome == "win":
                wins += 1
            elif outcome == "loss":
                losses += 1
            else:
                draws += 1
        n = max(1, int(episodes))
        results[mode] = {
            "wins": float(wins),
            "losses": float(losses),
            "draws": float(draws),
            "winrate": float(wins) / float(n),
        }
    return {"episodes": int(episodes), "seed": int(seed), "modes": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="MCTS candidate_mode winrate baseline")
    parser.add_argument("--episodes", type=int, default=int(os.getenv("MCTS_BASELINE_EPISODES", "30")))
    parser.add_argument("--seed", type=int, default=int(os.getenv("MCTS_BASELINE_SEED", "1000")))
    parser.add_argument("--modes", type=str, default=os.getenv("MCTS_BASELINE_MODES", "joint,filter,option"))
    parser.add_argument("--out", type=str, default="artifacts/results/mcts_candidate_baseline.json")
    args = parser.parse_args()
    modes = [m.strip() for m in str(args.modes).split(",") if m.strip()]
    report = run_baseline(episodes=int(args.episodes), seed=int(args.seed), modes=modes)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
