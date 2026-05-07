import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig


def test_gumbel_muzero_search_policy_targets_sum_to_one():
    n_obs = 12
    n_actions = [4, 3, 5]
    net = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions, latent_dim=64, hidden_dim=64, action_embed_dim=16)
    search = GumbelMuZeroSearch(
        net=net,
        config=GumbelMuZeroSearchConfig(num_simulations=24, root_top_k=3, temperature=0.2),
        device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [
        np.array([1, 1, 0, 1], dtype=bool),
        np.array([1, 0, 1], dtype=bool),
        np.array([1, 1, 1, 0, 0], dtype=bool),
    ]
    pi, actions, value = search.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert len(pi) == len(n_actions)
    assert len(actions) == len(n_actions)
    for head_idx, p in enumerate(pi):
        assert p.shape[0] == n_actions[head_idx]
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
    assert -5.0 <= float(value) <= 5.0
