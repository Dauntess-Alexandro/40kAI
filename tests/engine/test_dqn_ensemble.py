import torch

from core.models.DQN import DQN


def test_q_ensemble_stats_shape():
    n_obs = 12
    n_actions = [3, 2]
    net = DQN(
        n_obs, n_actions, dueling=True, noisy=False, distributional="iqn",
        hidden_size=32, num_layers=1, n_ensemble=3,
    )
    x = torch.randn(5, n_obs)
    means, stds = net.q_ensemble_stats(x)
    assert len(means) == len(n_actions)
    assert len(stds) == len(n_actions)
    assert means[0].shape == (5, 3)
    assert stds[0].shape == (5, 3)
    assert (stds[0] >= 0).all()


def test_iqn_ensemble_members_count():
    net = DQN(10, [4], distributional="iqn", n_ensemble=2, hidden_size=32, num_layers=1)
    x = torch.randn(3, 10)
    members = net.iqn_ensemble_members(x, num_quantiles=8)
    assert len(members) == 2
    assert members[0][0].shape[0] == 3
