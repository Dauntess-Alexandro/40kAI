import pytest
import torch

from core.models.DQN import DQN
from core.models.distill import distill_step, policy_kl_loss


class _FakeTeacher(torch.nn.Module):
    def forward(self, x):
        return [torch.softmax(torch.randn(x.shape[0], 4), dim=-1), torch.softmax(torch.randn(x.shape[0], 2), dim=-1)]


def test_distill_step_reduces_kl_vs_random_init():
    n_obs = 10
    n_actions = [4, 2]
    student = DQN(n_obs, n_actions, dueling=True, noisy=False, distributional=None, hidden_size=32, num_layers=1)
    teacher = _FakeTeacher()
    x = torch.randn(16, n_obs)

    with torch.no_grad():
        before = policy_kl_loss(
            teacher(x),
            student.q_values(x),
        ).item()

    try:
        opt = torch.optim.SGD(student.parameters(), lr=1e-2)
    except Exception as exc:
        pytest.skip(f"torch.optim недоступен: {exc}")

    for _ in range(20):
        out = distill_step(teacher, student, x, alpha_kl=1.0)
        opt.zero_grad()
        out["loss"].backward()
        opt.step()

    with torch.no_grad():
        after = policy_kl_loss(teacher(x), student.q_values(x)).item()
    assert after <= before + 1e-3
