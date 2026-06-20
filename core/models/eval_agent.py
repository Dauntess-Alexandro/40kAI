"""EvalAgent: единый путь действия+реакции для обеих сторон eval (P1 ≡ P2).

Резолвер конфига читает общие EVAL-флаги (без *_OPPONENT_*); при наличии
*_OPPONENT_* поднимает opponent_override_active (честный 1:1 нарушен).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from core.models.alphazero_ids import is_alphazero_net_algo, is_gumbel_az_algo

_TRUTHY = frozenset({"1", "true", "yes", "on"})
_OPPONENT_KEYS = (
    "AZ_EVAL_OPPONENT_MODE", "AZ_EVAL_OPPONENT_MCTS_SIMS", "AZ_EVAL_OPPONENT_MCTS_TEMPERATURE",
    "GAZ_EVAL_OPPONENT_MODE", "GMZ_OPPONENT_MODE", "GMZ_EVAL_OPPONENT_SIMS",
    "GMZ_EVAL_OPPONENT_TEMPERATURE", "SMZ_OPPONENT_MODE", "SMZ_EVAL_OPPONENT_NUM_SAMPLES",
    "SMZ_EVAL_OPPONENT_TEMPERATURE",
)


def _bool_env(name: str, default: str) -> bool:
    return str(os.getenv(name, default)).strip().lower() in _TRUTHY


@dataclass
class EvalSearchCfg:
    algo: str
    deterministic: bool
    epsilon: float
    search: dict[str, Any] = field(default_factory=dict)
    opponent_override_active: bool = False


def resolve_eval_search_cfg(algo: str) -> EvalSearchCfg:
    algo = str(algo or "").strip().lower()
    deterministic = _bool_env("EVAL_DETERMINISTIC", "1")
    epsilon = float(os.getenv("EVAL_EPSILON", "0"))
    override = any(os.getenv(k) is not None for k in _OPPONENT_KEYS)
    search: dict[str, Any] = {}

    if is_alphazero_net_algo(algo):
        if is_gumbel_az_algo(algo):
            search.update(
                mode=str(os.getenv("GAZ_EVAL_MODE", "gumbel")).strip().lower(),
                num_simulations=max(1, int(os.getenv("GAZ_EVAL_SIMS", "32"))),
                num_considered_actions=max(2, int(os.getenv("GAZ_EVAL_NUM_CONSIDERED", "8"))),
                joint_action=str(os.getenv("GAZ_JOINT_ACTION", "1")).strip() == "1",
                temperature=float(os.getenv("GAZ_EVAL_TEMPERATURE", "0.05")),
            )
        else:
            search.update(
                mode=str(os.getenv("AZ_EVAL_MODE", "mcts")).strip().lower(),
                simulations=max(1, int(os.getenv("AZ_EVAL_MCTS_SIMS", "32"))),
                c_puct=float(os.getenv("AZ_EVAL_MCTS_C_PUCT", "1.5")),
                dirichlet_alpha=float(os.getenv("AZ_EVAL_MCTS_DIR_ALPHA", "0.3")),
                dirichlet_eps=float(os.getenv("AZ_EVAL_MCTS_DIR_EPS", "0.0")),
                top_k_per_head=max(1, int(os.getenv("AZ_EVAL_MCTS_TOP_K_PER_HEAD", "8"))),
                max_depth=max(1, int(os.getenv("AZ_EVAL_MCTS_MAX_DEPTH", "1"))),
                mcts_mode=str(os.getenv("AZ_EVAL_MCTS_MODE", "tree")).strip().lower(),
                candidate_mode=str(os.getenv("AZ_EVAL_MCTS_CANDIDATE_MODE", os.getenv("MCTS_CANDIDATE_MODE", "option"))).strip().lower(),
                window_nodes=_bool_env("AZ_EVAL_MCTS_WINDOW_NODES", os.getenv("MCTS_WINDOW_NODES", "0")),
                joint_best_child=_bool_env("AZ_EVAL_MCTS_JOINT_BEST_CHILD", os.getenv("AZ_MCTS_JOINT_BEST_CHILD", "0")),
                temperature=float(os.getenv("AZ_EVAL_MCTS_TEMPERATURE", "0.06")),
            )
    elif algo == "gumbel_muzero":
        search.update(
            mode=str(os.getenv("GMZ_EVAL_MODE", "search")).strip().lower(),
            num_simulations=max(1, int(os.getenv("GMZ_EVAL_SIMS", "32"))),
            root_top_k=max(1, int(os.getenv("GMZ_EVAL_ROOT_TOP_K", "8"))),
            temperature=float(os.getenv("GMZ_EVAL_TEMPERATURE", "0.10")),
        )
    elif algo == "sampled_muzero":
        search.update(
            mode=str(os.getenv("SMZ_EVAL_MODE", "search")).strip().lower(),
            num_samples=int(os.getenv("SMZ_EVAL_NUM_SAMPLES", "24")),
            temperature=float(os.getenv("SMZ_EVAL_TEMPERATURE", "0.10")),
            sample_temperature=float(os.getenv("SMZ_EVAL_SAMPLE_TEMPERATURE", "1.0")),
            discount=float(os.getenv("SMZ_DISCOUNT", "0.997")),
        )
    return EvalSearchCfg(algo=algo, deterministic=deterministic, epsilon=epsilon, search=search, opponent_override_active=override)
