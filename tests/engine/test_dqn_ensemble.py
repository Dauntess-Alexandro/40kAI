import os

import numpy as np
import torch

import core.models.utils as U
from core.models.DQN import DQN
from core.models.memory import PrioritizedReplayMemory


def test_q_ensemble_stats_shape():
    n_obs = 12
    n_actions = [3, 2]
    net = DQN(
        n_obs, n_actions, dueling=True, noisy=False, distributional="iqn",
        hidden_size=32, num_layers=1, n_ensemble=3,
    )
    x = torch.randn(5, n_obs)
    means, stds = net.q_ensemble_stats(x)
    assert len(means) == len(n_actions)
    assert len(stds) == len(n_actions)
    assert means[0].shape == (5, 3)
    assert stds[0].shape == (5, 3)
    assert (stds[0] >= 0).all()


def test_iqn_ensemble_members_count():
    net = DQN(10, [4], distributional="iqn", n_ensemble=2, hidden_size=32, num_layers=1)
    x = torch.randn(3, 10)
    members = net.iqn_ensemble_members(x, num_quantiles=8)
    assert len(members) == 2
    assert members[0][0].shape[0] == 3


def test_optimize_model_ensemble_heads_different_widths():
    """Регресс: ensemble>1 с разноширинными головами не должен падать на агрегации std.

    Реальный экшен-спейс 40k имеет головы разной ширины (move/attack/shoot/...),
    поэтому torch.stack(stds, dim=1) недопустим — проверяем PER-путь целиком.
    """
    os.environ["PER_ENSEMBLE_PRIORITY_LAMBDA"] = "0.1"
    torch.manual_seed(0)
    np.random.seed(0)
    n_obs, n_actions = 12, [3, 2, 4]

    def make_net():
        return DQN(
            n_obs, n_actions, dueling=True, noisy=True, distributional="iqn",
            hidden_size=64, num_layers=2, n_ensemble=3,
            iqn_num_quantiles=16, iqn_num_target_quantiles=16, iqn_num_tau_samples=16,
        )

    policy, target = make_net(), make_net()
    target.load_state_dict(policy.state_dict())
    opt = torch.optim.Adam(policy.parameters(), lr=1e-4)
    mem = PrioritizedReplayMemory(1024)
    for _ in range(U.BATCH_SIZE + 50):
        s = torch.randn(1, n_obs)
        a = torch.tensor([[np.random.randint(x) for x in n_actions]], dtype=torch.long)
        ns = None if np.random.rand() < 0.1 else torch.randn(1, n_obs)
        r = torch.tensor([np.random.randn()], dtype=torch.float32)
        mask = np.random.rand(n_actions[2]) > 0.3
        mem.push(s, a, ns, r, np.random.randint(1, 4), mask)

    res = U.optimize_model(
        policy, target, opt, mem, n_obs,
        double_dqn_enabled=True, per_enabled=True, per_beta=0.4,
    )
    assert res is not None
    ds = res["dist_stats"]
    assert ds["n_ensemble"] == 3
    assert ds["ensemble_std_mean"] >= 0.0


def test_infer_dqn_arch_roundtrip_ensemble_and_single():
    """Арх из state_dict восстанавливается так, что load_state_dict проходит (ens=3 и ens=1)."""
    from core.models.DQN import infer_dqn_arch_from_state_dict, make_dqn

    for n_ens in (1, 3):
        src = make_dqn(
            12, [3, 2, 4], dueling=True, noisy=True, distributional="iqn",
            hidden_size=64, num_layers=2, n_ensemble=n_ens,
        )
        sd = src.state_dict()
        arch = infer_dqn_arch_from_state_dict(sd)
        assert arch["n_ensemble"] == n_ens
        assert arch["dueling"] is True
        assert arch["noisy"] is True
        assert arch["distributional"] == "iqn"
        assert arch["num_layers"] == 2
        assert arch["hidden_size"] == 64
        # Пересобранная по восстановленному арх сеть грузит веса без mismatch.
        rebuilt = make_dqn(12, [3, 2, 4], **arch)
        rebuilt.load_state_dict(sd)
