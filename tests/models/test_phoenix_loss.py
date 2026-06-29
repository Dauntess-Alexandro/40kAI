import torch

from core.models.phoenix_loss import (
    spr_consistency_loss,
    value_expansion_target,
    value_expansion_target_masked,
)


def test_spr_zero_when_pred_equals_target():
    pred = torch.randn(4, 3, 8)
    target = pred.clone()
    done = torch.zeros(4, 3)
    loss = spr_consistency_loss(pred, target, done)
    assert float(loss) < 1e-5


def test_spr_positive_when_mismatch():
    torch.manual_seed(0)
    pred = torch.randn(4, 3, 8)
    target = torch.randn(4, 3, 8)
    done = torch.zeros(4, 3)
    assert float(spr_consistency_loss(pred, target, done)) > 0.0


def test_spr_ignores_done_steps():
    torch.manual_seed(0)
    pred = torch.randn(2, 2, 8)
    target = pred.clone()
    # испортим второй шаг, но пометим его как done → должен игнорироваться
    target[:, 1] = torch.randn(2, 8)
    done = torch.tensor([[0.0, 1.0], [0.0, 1.0]])
    assert float(spr_consistency_loss(pred, target, done)) < 1e-5


def test_spr_no_grad_to_target():
    pred = torch.randn(2, 2, 8, requires_grad=True)
    target = torch.randn(2, 2, 8, requires_grad=True)
    done = torch.zeros(2, 2)
    loss = spr_consistency_loss(pred, target, done)
    loss.backward()
    assert target.grad is None or torch.allclose(target.grad, torch.zeros_like(target))


def test_ve_target_h0_returns_bootstrap():
    rewards = torch.zeros(3, 4)
    gammas = torch.full((3, 4), 0.99)
    boot = torch.tensor([1.0, 2.0, 3.0])
    out = value_expansion_target(rewards, gammas, boot, h=0)
    assert torch.allclose(out, boot)


def test_ve_target_nstep_accumulation():
    # h=2: r0 + γ r1 + γ^2 boot, при γ=0.5
    rewards = torch.tensor([[1.0, 1.0, 0.0]])
    gammas = torch.full((1, 3), 0.5)
    boot = torch.tensor([4.0])
    out = value_expansion_target(rewards, gammas, boot, h=2)
    expected = 1.0 + 0.5 * 1.0 + (0.5 ** 2) * 4.0
    assert abs(float(out) - expected) < 1e-6


def test_ve_masked_equals_unmasked_without_done():
    # Без терминала маскированный VE совпадает с обычным
    rewards = torch.tensor([[1.0, 1.0, 0.0]])
    gammas = torch.full((1, 3), 0.5)
    boot = torch.tensor([4.0])
    done = torch.zeros(1, 3)
    out = value_expansion_target_masked(rewards, gammas, boot, done, h=2)
    expected = value_expansion_target(rewards, gammas, boot, h=2)
    assert torch.allclose(out, expected)


def test_ve_masked_zeroes_bootstrap_past_terminal():
    # Терминал на шаге 1 → шаг 2 невалиден (done[2]=1): bootstrap на obs[h=2] зануляется,
    # но реальные награды r0, r1 (шаг терминала валиден) остаются.
    rewards = torch.tensor([[1.0, 1.0, 9.0]])  # 9.0 — награда из чужого эпизода
    gammas = torch.full((1, 3), 0.5)
    boot = torch.tensor([4.0])
    done = torch.tensor([[0.0, 0.0, 1.0]])
    out = value_expansion_target_masked(rewards, gammas, boot, done, h=2)
    # r0 + γ r1 + γ^2 * 0  = 1 + 0.5 = 1.5 (boot обрезан, r2 за горизонтом)
    assert abs(float(out) - 1.5) < 1e-6


def test_ve_masked_truncates_reward_leak():
    # Терминал на шаге 0 → шаги 1,2 невалидны: ни награды, ни bootstrap из следующего эпизода.
    rewards = torch.tensor([[1.0, 9.0, 9.0]])  # 9.0 — утечка из чужого эпизода
    gammas = torch.full((1, 3), 0.5)
    boot = torch.tensor([4.0])
    done = torch.tensor([[0.0, 1.0, 1.0]])
    out = value_expansion_target_masked(rewards, gammas, boot, done, h=2)
    # только r0; r1 занулён маской, boot занулён (done[2]=1)
    assert abs(float(out) - 1.0) < 1e-6
