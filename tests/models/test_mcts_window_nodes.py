import numpy as np
import torch

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.option_candidates import root_joint_candidates
from core.models.windowed_mcts import mcts_window_nodes_enabled, resolve_active_window_index
from tests.engine.phases._helpers import build_env


def _obs_np(env):
    s = env._get_observation()
    if isinstance(s, dict):
        return np.asarray(list(s.values()), dtype=np.float32)
    return np.asarray(s, dtype=np.float32)


def test_window_nodes_disabled_by_default(monkeypatch):
    monkeypatch.delenv("MCTS_WINDOW_NODES", raising=False)
    assert mcts_window_nodes_enabled() is False


def test_resolve_active_window_index_command_on_move_zero():
    assert resolve_active_window_index(move_count=0, num_windows=12) == 0
    assert resolve_active_window_index(move_count=3, num_windows=12) == 3


def test_window_nodes_changes_root_candidates(monkeypatch):
    monkeypatch.setenv("MCTS_WINDOW_NODES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    n_actions = [int(env.action_space.spaces[k].n) for k in ordered_action_keys(len_model)]
    obs = env._get_observation()
    obs_np = _obs_np(env)
    net = AlphaZeroPolicyValueNet(int(obs_np.size), n_actions)
    priors = [np.ones(n, dtype=np.float32) / n for n in n_actions]
    legal = [np.ones(n, dtype=bool) for n in n_actions]

    full = root_joint_candidates(
        mode="option",
        priors=priors,
        legal_masks=legal,
        env=env,
        len_model=len_model,
        window_nodes=False,
    )
    layered = root_joint_candidates(
        mode="option",
        priors=priors,
        legal_masks=legal,
        env=env,
        len_model=len_model,
        window_nodes=True,
        move_count=0,
    )
    assert len(layered) >= 1
    assert set(layered.tuples).issubset(set(full.tuples) | set(layered.tuples))


def test_mcts_runs_with_window_nodes(monkeypatch):
    monkeypatch.setenv("MCTS_WINDOW_NODES", "1")
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    n_actions = [int(env.action_space.spaces[k].n) for k in ordered_action_keys(len_model)]
    obs = env._get_observation()
    obs_np = _obs_np(env)
    net = AlphaZeroPolicyValueNet(int(obs_np.size), n_actions)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]
    mcts = AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(
            simulations=4,
            mode="tree",
            max_depth=1,
            candidate_mode="option",
            window_nodes=True,
            simulate_enemy_in_tree=False,
        ),
        device=torch.device("cpu"),
    )
    pi, act, val = mcts.run(
        obs=obs_np,
        legal_masks_by_head=legal,
        temperature=0.0,
        env=env,
        len_model=len_model,
        move_count=0,
        reset_options={"m": env.model, "e": env.enemy, "trunc": True},
    )
    assert pi
    assert act
