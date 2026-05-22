import torch

from core.models.DQN import DQN, ResidualBlock


def test_forward_shape_with_residual():
    n_obs = 20
    n_actions = [4, 3, 5]
    net = DQN(n_obs, n_actions, dueling=True, noisy=False, distributional="iqn", hidden_size=64, num_layers=2)
    x = torch.randn(8, n_obs)
    outputs = net(x)
    assert len(outputs) == len(n_actions)
    assert outputs[0].shape == (8, 4)
    assert outputs[1].shape == (8, 3)
    assert outputs[2].shape == (8, 5)


def test_num_layers_param():
    net = DQN(10, [3], hidden_size=32, num_layers=3, noisy=False, distributional=None, dueling=False)
    assert len(net.blocks) == 3
    assert all(isinstance(b, ResidualBlock) for b in net.blocks)


def test_iqn_tau_embedding_uses_layernorm():
    net = DQN(10, [3], distributional="iqn", hidden_size=32, num_layers=1)
    assert hasattr(net, "iqn_tau_norm")
    assert isinstance(net.iqn_tau_norm, torch.nn.LayerNorm)


def test_configurable_hidden_size():
    net = DQN(10, [2], hidden_size=128, num_layers=1, noisy=False, distributional=None, dueling=False)
    assert net.hidden_size == 128
    x = torch.randn(4, 10)
    out = net(x)
    assert out[0].shape == (4, 2)
