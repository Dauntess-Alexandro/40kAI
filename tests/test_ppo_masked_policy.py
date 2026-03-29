import torch

from model.PPO import ActorCriticMultiHead


def test_ppo_masked_action_respects_invalid_entries():
    net = ActorCriticMultiHead(n_observations=6, n_actions=[3, 4])
    obs = torch.zeros((1, 6), dtype=torch.float32)
    masks = [
        torch.tensor([[False, True, False]], dtype=torch.bool),
        torch.tensor([[True, False, False, False]], dtype=torch.bool),
    ]
    actions, logp, values = net.act(obs, masks_by_head=masks, deterministic=True)
    assert actions.shape == (1, 2)
    assert int(actions[0, 0].item()) == 1
    assert int(actions[0, 1].item()) == 0
    assert logp.shape == (1,)
    assert values.shape == (1,)

