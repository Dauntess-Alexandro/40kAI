"""Регрессия режимов кандидатов MCTS (Stage 4)."""

import numpy as np
import torch

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import AlphaZeroPolicyValueNet
from tests.engine.phases._helpers import build_env


def _run_mcts_once(*, candidate_mode: str, seed: int) -> tuple[list[list[float]], list[int], float]:
    torch.manual_seed(seed)
    np.random.seed(seed)
    env = build_env()
    state, _ = env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    n_actions = [int(env.action_space.spaces[k].n) for k in ordered_action_keys(len_model)]
    obs = np.asarray(list(state.values()) if isinstance(state, dict) else state, dtype=np.float32)
    n_obs = int(obs.size)
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]

    mcts = AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(
            simulations=12,
            c_puct=1.3,
            top_k_per_head=4,
            mode="tree",
            max_depth=1,
            dirichlet_eps=0.0,
            root_dirichlet_only=False,
            candidate_mode=candidate_mode,
        ),
        device=torch.device("cpu"),
    )
    pi, act, value = mcts.run(
        obs=obs,
        legal_masks_by_head=legal,
        temperature=0.5,
        env=env,
        len_model=len_model,
        reset_options={"m": env.model, "e": env.enemy, "trunc": True},
    )
    pi_serial = [[float(x) for x in p.tolist()] for p in pi]
    return pi_serial, [int(a) for a in act], float(value)


def test_joint_mode_deterministic_on_fixed_seed():
    a = _run_mcts_once(candidate_mode="joint", seed=42)
    b = _run_mcts_once(candidate_mode="joint", seed=42)
    assert a == b


def test_filter_mode_runs_and_differs_or_subset():
    joint = _run_mcts_once(candidate_mode="joint", seed=7)
    filt = _run_mcts_once(candidate_mode="filter", seed=7)
    assert len(filt[0]) == len(joint[0])
    assert len(filt[1]) == len(joint[1])


def test_option_mode_runs():
    out = _run_mcts_once(candidate_mode="option", seed=11)
    assert out[0]
    assert out[1]


def test_option_plus_mode_runs():
    out = _run_mcts_once(candidate_mode="option_plus", seed=13)
    assert out[0]
    assert out[1]
