import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.utils import normalize_state_dict


def test_gumbel_muzero_checkpoint_contract_contains_algo_and_state():
    n_obs = 14
    n_actions = [4, 2, 6]
    net = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions, latent_dim=32, hidden_dim=32, action_embed_dim=8)
    payload = {
        "algo": "gumbel_muzero",
        "gumbel_muzero_net": normalize_state_dict(net.state_dict()),
        "policy_net": normalize_state_dict(net.state_dict()),
    }
    assert payload["algo"] == "gumbel_muzero"
    assert isinstance(payload["gumbel_muzero_net"], dict)
    clone = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions, latent_dim=32, hidden_dim=32, action_embed_dim=8)
    clone.load_state_dict(payload["gumbel_muzero_net"])

    x = torch.randn(1, n_obs)
    probs, value = clone.infer(x, masks_by_head=None)
    assert len(probs) == len(n_actions)
    assert value.shape == (1,)
