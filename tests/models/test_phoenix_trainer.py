# tests/models/test_phoenix_trainer.py
import torch
from core.models.phoenix_config import PhoenixConfig
from core.models.phoenix_model import PhoenixNet
from core.models.phoenix_replay import SequenceReplayBuffer
from core.models.phoenix_trainer import PhoenixTrainer, anneal_value


def test_anneal_endpoints():
    assert abs(anneal_value(0.97, 0.99, 0, 100) - 0.97) < 1e-9
    assert abs(anneal_value(0.97, 0.99, 100, 100) - 0.99) < 1e-9
    mid = anneal_value(0.97, 0.99, 50, 100)
    assert 0.97 < mid < 0.99


def test_nstep_anneal_decreases():
    cfg = PhoenixConfig(nstep_start=10, nstep_end=3, anneal_steps=100)
    net = PhoenixNet(8, [3, 4], cfg)
    tr = PhoenixTrainer(net, cfg)
    assert tr.current_nstep(0) == 10
    assert tr.current_nstep(100) == 3
    assert tr.current_nstep(50) <= 10 and tr.current_nstep(50) >= 3


def test_learn_step_runs_and_returns_losses():
    torch.manual_seed(0)
    cfg = PhoenixConfig(hidden_size=32, num_layers=1, emb_dim=8, spr_horizon_K=3, ve_horizon=2)
    net = PhoenixNet(6, [3, 4], cfg)
    tr = PhoenixTrainer(net, cfg)
    buf = SequenceReplayBuffer(capacity=64, window=cfg.window_horizon)
    for ep in range(4):
        for t in range(8):
            buf.push([0.1 * t] * 6, [0, 0], [True, True], reward=float(t % 2), done=(t == 7))
    windows, _, _ = buf.sample(8)
    out = tr.learn_step(windows)
    assert "loss" in out and out["loss"] == out["loss"]  # not NaN
    assert out["loss_spr"] >= 0.0
    assert out["td_errors"].shape[0] == len(windows)


def test_learn_step_accepts_is_weights_and_latent_bootstrap():
    torch.manual_seed(1)
    cfg = PhoenixConfig(
        hidden_size=24,
        num_layers=1,
        emb_dim=8,
        spr_horizon_K=2,
        ve_horizon=2,
        ve_latent_bootstrap=True,
        iqn_num_quantiles=8,
        iqn_num_target_quantiles=8,
        iqn_num_tau_samples=8,
    )
    net = PhoenixNet(6, [3, 4], cfg)
    tr = PhoenixTrainer(net, cfg)
    buf = SequenceReplayBuffer(capacity=64, window=cfg.window_horizon)
    for ep in range(3):
        for t in range(5):
            buf.push([0.05 * (t + ep)] * 6, [0, 1], [True, True], reward=float(t), done=(t == 4))
    windows, _, weights = buf.sample(4)
    out = tr.learn_step(windows, is_weights=weights)
    assert out["loss"] == out["loss"]
    assert out["loss_iqn"] >= 0.0


def test_maybe_reset_triggers_on_interval():
    cfg = PhoenixConfig(hidden_size=16, num_layers=1, reset_interval=5)
    net = PhoenixNet(6, [3, 4], cfg)
    tr = PhoenixTrainer(net, cfg)
    head_before = next(net.online.head_bundles.parameters()).detach().clone()
    fired = [tr.maybe_reset(s) for s in range(1, 7)]
    assert any(fired)
    head_after = next(net.online.head_bundles.parameters()).detach()
    assert not torch.allclose(head_before, head_after)
