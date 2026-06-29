import torch

from core.models.phoenix_model import PhoenixActionEmbed, PhoenixDynamics


def test_action_embed_masks_inactive_heads():
    torch.manual_seed(0)
    emb = PhoenixActionEmbed(action_sizes=[3, 4], emb_dim=8)
    actions = torch.tensor([[1, 2], [0, 3]], dtype=torch.long)
    mask_all = torch.ones(2, 2, dtype=torch.bool)
    out_all = emb(actions, mask_all)
    assert out_all.shape == (2, 8)

    # Вторая голова неактивна → результат == вклад только первой головы
    mask_first = torch.tensor([[True, False], [True, False]])
    out_first = emb(actions, mask_first)
    only_first = emb.embeddings[0](actions[:, 0])
    assert torch.allclose(out_first, only_first, atol=1e-6)

    # Полностью неактивные головы → нулевой вектор
    mask_none = torch.zeros(2, 2, dtype=torch.bool)
    out_none = emb(actions, mask_none)
    assert torch.allclose(out_none, torch.zeros(2, 8), atol=1e-6)


def test_dynamics_rollout_shapes_and_recurrence():
    torch.manual_seed(0)
    dyn = PhoenixDynamics(hidden_size=16, emb_dim=8, dynamics_type="mlp")
    z0 = torch.randn(4, 16)
    a_seq = torch.randn(4, 3, 8)
    out = dyn.rollout(z0, a_seq)
    assert out.shape == (4, 3, 16)
    # рекуррентность: первый шаг == step(z0, a_seq[:,0])
    first = dyn.step(z0, a_seq[:, 0])
    assert torch.allclose(out[:, 0], first, atol=1e-6)
    # второй шаг == step(out[:,0], a_seq[:,1])
    second = dyn.step(out[:, 0], a_seq[:, 1])
    assert torch.allclose(out[:, 1], second, atol=1e-6)
