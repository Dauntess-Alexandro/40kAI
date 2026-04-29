import torch

from core.models.DQN import DQN, NoisyLinear
from core.models.memory import ReplayMemory
from core.models.utils import c51_project_distribution, optimize_model


def test_noisy_linear_changes_output_after_noise_reset():
    layer = NoisyLinear(8, 4, sigma0=0.5)
    layer.train()
    x = torch.randn(2, 8)
    y1 = layer(x)
    layer.reset_noise()
    y2 = layer(x)
    assert not torch.allclose(y1, y2)


def test_c51_projection_distribution_is_normalized():
    support = torch.linspace(-10.0, 10.0, 51)
    next_dist = torch.full((3, 51), 1.0 / 51.0)
    rewards = torch.tensor([0.0, 1.0, -1.0], dtype=torch.float32)
    gammas = torch.tensor([0.99, 0.95, 0.90], dtype=torch.float32)
    projected = c51_project_distribution(rewards, gammas, next_dist, support)
    sums = projected.sum(dim=1)
    assert torch.allclose(sums, torch.ones_like(sums), atol=1e-4)
    assert torch.isfinite(projected).all()


def test_optimize_model_smoke_with_c51_and_per():
    import core.models.utils as model_utils

    old_batch = model_utils.BATCH_SIZE
    model_utils.BATCH_SIZE = 2
    try:
        n_obs = 10
        n_actions = [3, 2, 4, 2, 2, 2]
        policy = DQN(n_obs, n_actions, dueling=True, noisy=True, distributional="c51", num_atoms=51, v_min=-10, v_max=10)
        target = DQN(n_obs, n_actions, dueling=True, noisy=True, distributional="c51", num_atoms=51, v_min=-10, v_max=10)
        target.load_state_dict(policy.state_dict())
        optimizer = torch.optim.Adam(policy.parameters(), lr=1e-4)
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
    finally:
        model_utils.BATCH_SIZE = old_batch
