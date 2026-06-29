import torch
from core.models.phoenix_model import PhoenixActionEmbed


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
