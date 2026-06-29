import torch

from core.models.phoenix_config import PhoenixConfig
from core.models.phoenix_model import (
    PhoenixActionEmbed,
    PhoenixDynamics,
    PhoenixNet,
    infer_phoenix_arch_from_state_dict,
)


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


# --- Task 4: PhoenixNet tests ---


def _net():
    cfg = PhoenixConfig(hidden_size=32, num_layers=1, emb_dim=8, noisy=False)
    return PhoenixNet(n_observations=12, action_sizes=[3, 4], cfg=cfg), cfg


def test_phoenixnet_forward_shapes():
    net, cfg = _net()
    obs = torch.randn(5, 12)
    z = net.encode(obs)
    assert z.shape == (5, cfg.hidden_size)
    q = net.iqn_q(obs)
    assert len(q) == 2 and q[0].shape == (5, 3) and q[1].shape == (5, 4)
    p = net.project(z)
    assert net.predict(p).shape == p.shape


def test_update_targets_moves_toward_online():
    net, _ = _net()
    # сместим online encoder, target должен подтянуться при ema=1.0 (полная копия)
    with torch.no_grad():
        for p in net.online.parameters():
            p.add_(1.0)
    net.update_targets(ema_rl=1.0, ema_spr=1.0)
    for po, pt in zip(net.online.parameters(), net.target.parameters()):
        assert torch.allclose(po, pt, atol=1e-6)


def test_reset_changes_heads_and_shrinks_encoder():
    net, cfg = _net()
    enc_before = [p.detach().clone() for p in net._encoder_parameters()]
    head_before = next(net.online.head_bundles.parameters()).detach().clone()
    net.reset_heads_and_shrink_encoder(alpha=0.5)
    head_after = next(net.online.head_bundles.parameters()).detach()
    assert not torch.allclose(head_before, head_after)  # голова сброшена
    # encoder сдвинут (shrink-perturb), но не обнулён
    enc_after = list(net._encoder_parameters())
    moved = any(not torch.allclose(b, a) for b, a in zip(enc_before, enc_after))
    assert moved


def test_arch_restore_roundtrip():
    net, cfg = _net()
    arch = infer_phoenix_arch_from_state_dict(net.state_dict())
    assert arch["hidden_size"] == cfg.hidden_size
    assert arch["num_layers"] == cfg.num_layers
    assert arch["emb_dim"] == cfg.emb_dim
