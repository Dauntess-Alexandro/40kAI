import os

import torch

from core.models.PPO import ActorCriticMultiHead, ResidualBlock, make_actor_critic


def test_forward_shape_with_residual():
    n_obs = 20
    n_actions = [4, 3, 5]
    net = make_actor_critic(n_obs, n_actions, hidden_size=64, num_layers=2)
    x = torch.randn(8, n_obs)
    logits, value = net(x)
    assert len(logits) == len(n_actions)
    assert logits[0].shape == (8, 4)
    assert logits[1].shape == (8, 3)
    assert logits[2].shape == (8, 5)
    assert value.shape == (8,)


def test_num_layers_param():
    net = ActorCriticMultiHead(10, [3], hidden_size=32, num_layers=3)
    assert len(net.blocks) == 3
    assert all(isinstance(b, ResidualBlock) for b in net.blocks)


def test_has_input_layernorm():
    net = make_actor_critic(10, [3], hidden_size=32, num_layers=1)
    assert hasattr(net, "input_norm")
    assert isinstance(net.input_norm, torch.nn.LayerNorm)


def test_configurable_hidden_size_env(monkeypatch):
    monkeypatch.setenv("PPO_HIDDEN_SIZE", "128")
    monkeypatch.setenv("PPO_NUM_LAYERS", "3")
    net = make_actor_critic(10, [2])
    assert net.hidden_size == 128
    assert net.num_layers == 3
