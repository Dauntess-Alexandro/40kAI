import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet


def test_gumbel_muzero_model_forward_shapes():
    n_obs = 32
    n_actions = [5, 2, 8, 8, 5, 4, 24, 24]
    net = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions, latent_dim=128, hidden_dim=128, action_embed_dim=32)
    x = torch.randn(3, n_obs)
    logits, value = net(x)
    assert len(logits) == len(n_actions)
    assert value.shape == (3,)
    for idx, head in enumerate(logits):
        assert head.shape == (3, n_actions[idx])


def test_gumbel_muzero_initial_and_recurrent_inference_shapes():
    n_obs = 16
    n_actions = [4, 3, 6]
    net = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions, latent_dim=64, hidden_dim=64, action_embed_dim=16)
    obs = torch.randn(2, n_obs)
    logits, value, reward, latent = net.initial_inference(obs)
    assert len(logits) == len(n_actions)
    assert value.shape == (2,)
    assert reward.shape == (2,)
    assert latent.shape == (2, 64)

    actions = torch.tensor([[1, 0, 2], [3, 2, 1]], dtype=torch.long)
    logits2, value2, reward2, latent2 = net.recurrent_inference(latent, actions)
    assert len(logits2) == len(n_actions)
    assert value2.shape == (2,)
    assert reward2.shape == (2,)
    assert latent2.shape == (2, 64)
