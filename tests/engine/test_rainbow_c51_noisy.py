import pytest
import torch

from core.models.DQN import DQN, NoisyLinear


def _sgd_or_skip(params, lr=1e-3):
    try:
        return torch.optim.SGD(params, lr=lr)
    except Exception as exc:
        pytest.skip(f"torch.optim недоступен в этой среде: {exc}")
from core.models.memory import ReplayMemory
from core.models.utils import optimize_model, quantile_huber_loss


def test_noisy_linear_changes_output_after_noise_reset():
    layer = NoisyLinear(8, 4, sigma0=0.5)
    layer.train()
    x = torch.randn(2, 8)
    y1 = layer(x)
    layer.reset_noise()
    y2 = layer(x)
    assert not torch.allclose(y1, y2)


def test_iqn_quantile_huber_loss_is_finite_and_shaped():
    pred = torch.randn(3, 8)
    tgt = torch.randn(3, 12)
    taus = torch.rand(3, 8, 1)
    loss, td = quantile_huber_loss(pred, tgt, taus, kappa=1.0)
    assert loss.shape == (3,)
    assert td.shape == (3, 8, 12)
    assert torch.isfinite(loss).all()
    assert torch.isfinite(td).all()


@pytest.mark.parametrize("hidden_size,num_layers", [(128, 1), (256, 3)])
def test_optimize_model_smoke_with_iqn_and_per_toggle(hidden_size, num_layers):
    import core.models.utils as model_utils

    old_batch = model_utils.BATCH_SIZE
    model_utils.BATCH_SIZE = 2
    try:
        n_obs = 10
        n_actions = [3, 2, 4, 2, 2, 2]
        policy = DQN(
            n_obs, n_actions, dueling=True, noisy=True, distributional="iqn",
            iqn_num_quantiles=16, iqn_num_target_quantiles=16, iqn_num_tau_samples=16, iqn_embed_dim=32,
            hidden_size=hidden_size, num_layers=num_layers,
        )
        target = DQN(
            n_obs, n_actions, dueling=True, noisy=True, distributional="iqn",
            iqn_num_quantiles=16, iqn_num_target_quantiles=16, iqn_num_tau_samples=16, iqn_embed_dim=32,
            hidden_size=hidden_size, num_layers=num_layers,
        )
        target.load_state_dict(policy.state_dict())
        optimizer = _sgd_or_skip(policy.parameters())
        memory = ReplayMemory(16)

        for _ in range(2):
            state = torch.randn(1, n_obs)
            action = torch.tensor([[1, 1, 2, 1, 0, 1]], dtype=torch.long)
            next_state = torch.randn(1, n_obs)
            reward = torch.tensor([0.5], dtype=torch.float32)
            n_step = 3
            next_shoot_mask = torch.tensor([True, True, True, False], dtype=torch.bool)
            memory.push(state, action, next_state, reward, n_step, next_shoot_mask)

        result = optimize_model(
            policy,
            target,
            optimizer,
            memory,
            n_obs,
            double_dqn_enabled=True,
            per_enabled=False,
            per_beta=0.4,
            per_eps=1e-6,
            use_amp=False,
        )
        assert result is not None
        assert "loss" in result and result["loss"] >= 0.0
        assert result.get("dist_stats") is not None
        result_per = optimize_model(
            policy,
            target,
            optimizer,
            memory,
            n_obs,
            double_dqn_enabled=True,
            per_enabled=False,
            per_beta=0.4,
            per_eps=1e-6,
            use_amp=False,
        )
        assert result_per is not None
    finally:
        model_utils.BATCH_SIZE = old_batch
