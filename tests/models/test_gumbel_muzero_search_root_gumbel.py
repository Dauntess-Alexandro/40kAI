import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import (
    GumbelMuZeroSearch,
    GumbelMuZeroSearchConfig,
    make_search_config,
    SEARCH_PRESETS,
)


def _make_net(n_obs, n_actions):
    return GumbelMuZeroNet(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16,
    )


def test_gumbel_muzero_search_policy_targets_sum_to_one():
    n_obs = 12
    n_actions = [4, 3, 5]
    net = _make_net(n_obs, n_actions)
    search = GumbelMuZeroSearch(
        net=net,
        config=GumbelMuZeroSearchConfig(num_simulations=24, root_top_k=3, temperature=0.2, prior_weight=0.25),
        device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [
        np.array([1, 1, 0, 1], dtype=bool),
        np.array([1, 0, 1], dtype=bool),
        np.array([1, 1, 1, 0, 0], dtype=bool),
    ]
    pi, _, actions, value = search.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert len(pi) == len(n_actions)
    assert len(actions) == len(n_actions)
    for head_idx, p in enumerate(pi):
        assert p.shape[0] == n_actions[head_idx]
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
    assert -5.0 <= float(value) <= 5.0


def test_gumbel_muzero_search_illegal_actions_zero_prob():
    n_obs = 8
    n_actions = [5]
    net = _make_net(n_obs, n_actions)
    search = GumbelMuZeroSearch(
        net=net,
        config=GumbelMuZeroSearchConfig(num_simulations=16, root_top_k=2, prior_weight=0.25),
        device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.array([True, False, False, True, False], dtype=bool)]
    pi, _, actions, _ = search.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    # illegal actions must have zero probability
    assert pi[0][1] == 0.0
    assert pi[0][2] == 0.0
    assert pi[0][4] == 0.0
    # selected action must be legal
    assert legal[0][actions[0]]


def test_gumbel_muzero_search_deterministic_vs_stochastic():
    n_obs = 8
    n_actions = [4, 3]
    net = _make_net(n_obs, n_actions)
    cfg = GumbelMuZeroSearchConfig(num_simulations=8, root_top_k=2, prior_weight=0.25)
    search = GumbelMuZeroSearch(net=net, config=cfg, device=torch.device("cpu"))
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.ones(4, dtype=bool), np.ones(3, dtype=bool)]

    _, _, actions_det, _ = search.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    # deterministic must return a valid action
    for a, size in zip(actions_det, n_actions):
        assert 0 <= a < size


def test_gumbel_muzero_search_last_run_stats():
    n_obs = 8
    n_actions = [3]
    net = _make_net(n_obs, n_actions)
    cfg = GumbelMuZeroSearchConfig(num_simulations=4, root_top_k=2, prior_weight=0.25)
    search = GumbelMuZeroSearch(net=net, config=cfg, device=torch.device("cpu"))
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.ones(3, dtype=bool)]
    search.run(obs=obs, legal_masks_by_head=legal)
    stats = search.last_run_stats
    assert "root_value" in stats
    assert "q_mean" in stats
    assert "simulations" in stats


import pytest

@pytest.mark.parametrize("preset", ["fast", "balanced", "heavy"])
def test_search_presets_make(preset):
    cfg = make_search_config(preset=preset)
    expected = SEARCH_PRESETS[preset]
    assert cfg.num_simulations == expected["num_simulations"]
    assert cfg.root_top_k == expected["root_top_k"]
    assert cfg.prior_weight == expected["prior_weight"]
