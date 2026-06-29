import torch
from core.models.phoenix_loss import spr_consistency_loss


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
