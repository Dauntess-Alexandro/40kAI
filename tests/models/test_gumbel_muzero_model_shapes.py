import torch
import pytest

from core.models.gumbel_muzero_model import (
    GumbelMuZeroNet,
    make_gumbel_muzero_net,
    make_gumbel_muzero_net_preset,
    GMZ_PRESETS,
)


def test_gumbel_muzero_model_forward_shapes():
    n_obs = 32
    n_actions = [5, 2, 8, 8, 5, 4, 24, 24]
    net = GumbelMuZeroNet(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=128, hidden_dim=128, num_layers=2, action_embed_dim=32,
    )
    x = torch.randn(3, n_obs)
    logits, value = net(x)
    assert len(logits) == len(n_actions)
    assert value.shape == (3,)
    for idx, head in enumerate(logits):
        assert head.shape == (3, n_actions[idx])


def test_gumbel_muzero_initial_and_recurrent_inference_shapes():
    n_obs = 16
    n_actions = [4, 3, 6]
    net = GumbelMuZeroNet(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=64, hidden_dim=64, num_layers=2, action_embed_dim=16,
    )
    obs = torch.randn(2, n_obs)
    logits, value, reward, latent = net.initial_inference(obs)
    assert len(logits) == len(n_actions)
    assert value.shape == (2,)
    assert reward.shape == (2,)
    assert latent.shape == (2, 64)
    # reward at initial state must be zero
    assert reward.abs().max().item() < 1e-6

    actions = torch.tensor([[1, 0, 2], [3, 2, 1]], dtype=torch.long)
    logits2, value2, reward2, latent2 = net.recurrent_inference(latent, actions)
    assert len(logits2) == len(n_actions)
    assert value2.shape == (2,)
    assert reward2.shape == (2,)
    assert latent2.shape == (2, 64)


def test_gumbel_muzero_value_bounded():
    net = GumbelMuZeroNet(obs_dim=8, action_sizes=[3, 3], latent_dim=32, hidden_dim=32, num_layers=1)
    obs = torch.randn(16, 8)
    _, value, _, _ = net.initial_inference(obs)
    assert value.min().item() >= -1.0 - 1e-5
    assert value.max().item() <= 1.0 + 1e-5


def test_gumbel_muzero_latent_normalized():
    net = GumbelMuZeroNet(obs_dim=8, action_sizes=[3], latent_dim=64, hidden_dim=64, num_layers=1)
    obs = torch.randn(32, 8)
    _, _, _, latent = net.initial_inference(obs)
    assert abs(latent.mean().item()) < 0.3
    assert abs(latent.std().item() - 1.0) < 0.3


def test_gumbel_muzero_backward():
    net = GumbelMuZeroNet(obs_dim=8, action_sizes=[4, 3], latent_dim=32, hidden_dim=32, num_layers=1)
    obs = torch.randn(4, 8)
    logits, value, _, latent = net.initial_inference(obs)
    loss = value.mean()
    for lgt in logits:
        loss = loss + lgt.mean()
    loss.backward()
    grads = [p.grad for p in net.parameters() if p.grad is not None]
    assert len(grads) > 0


def test_gumbel_muzero_action_mask_applied():
    net = GumbelMuZeroNet(obs_dim=8, action_sizes=[5], latent_dim=32, hidden_dim=32, num_layers=1)
    obs = torch.randn(1, 8)
    mask = torch.tensor([[True, False, False, False, False]])
    logits, _ = net.predict(net.encode(obs), masks_by_head=[mask])
    probs = torch.softmax(logits[0], dim=1)
    # Only action 0 should have significant probability
    assert probs[0, 0].item() > 0.9


@pytest.mark.parametrize("preset", ["fast", "balanced", "heavy"])
def test_gumbel_muzero_presets_instantiate(preset):
    cfg = GMZ_PRESETS[preset]
    net = make_gumbel_muzero_net_preset(obs_dim=16, action_sizes=[4, 3], preset=preset)
    assert net.hidden_dim == cfg["hidden_dim"]
    assert net.latent_dim == cfg["latent_dim"]
    assert net.num_layers == cfg["num_layers"]
    obs = torch.randn(2, 16)
    logits, value = net(obs)
    assert value.shape == (2,)


def test_make_gumbel_muzero_net_overrides():
    net = make_gumbel_muzero_net(obs_dim=10, action_sizes=[3, 3], hidden_dim=64, latent_dim=64, num_layers=1)
    assert net.hidden_dim == 64
    assert net.latent_dim == 64
