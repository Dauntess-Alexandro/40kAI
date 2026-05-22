import torch

from core.models.PPO import ActorCriticMultiHead, make_actor_critic


def test_value_ensemble_averages_heads():
    net = make_actor_critic(12, [4, 3], hidden_size=32, num_layers=1, n_value_ensemble=3)
    assert net.n_value_ensemble == 3
    assert len(net.value_heads) == 3
    assert not hasattr(net, "value_head")

    x = torch.randn(5, 12)
    _, value = net(x)
    assert value.shape == (5,)

    per_head = torch.stack([h(net._encode(x)).squeeze(-1) for h in net.value_heads], dim=0)
    expected = per_head.mean(dim=0)
    assert torch.allclose(value, expected, atol=1e-5)


def test_single_value_head_alias():
    net = ActorCriticMultiHead(8, [5], hidden_size=32, num_layers=1, n_value_ensemble=1)
    assert hasattr(net, "value_head")
    assert net.value_head is net.value_heads[0]
