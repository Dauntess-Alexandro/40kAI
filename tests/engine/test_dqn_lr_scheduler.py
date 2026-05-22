import os
import tempfile

import pytest
import torch
import torch.optim as optim

from core.models.DQN import DQN, dqn_kwargs_from_env


def _build_scheduler(optimizer, kind="cosine", t_max=100):
    if kind == "cosine":
        return optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=t_max)
    if kind == "plateau":
        return optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=5)
    return None


def test_lr_scheduler_save_load_in_checkpoint():
    kwargs = dqn_kwargs_from_env()
    n_obs, n_actions = 8, [3, 2]
    policy = DQN(n_obs, n_actions, dueling=True, distributional="iqn", **kwargs)
    target = DQN(n_obs, n_actions, dueling=True, distributional="iqn", **kwargs)
    try:
        optimizer = optim.SGD(policy.parameters(), lr=1e-3)
    except Exception as exc:
        pytest.skip(f"torch.optim недоступен: {exc}")
    scheduler = _build_scheduler(optimizer, kind="cosine", t_max=50)
    assert scheduler is not None
    scheduler.step()
    lr_before = optimizer.param_groups[0]["lr"]

    extra = {
        "target_net": target.state_dict(),
        "target_model_state_dict": target.state_dict(),
        "lr_scheduler": scheduler.state_dict(),
    }

    with tempfile.NamedTemporaryFile(suffix=".pth", delete=False) as tmp:
        path = tmp.name
    try:
        torch.save({"policy_net": policy.state_dict(), **extra}, path)
        data = torch.load(path, weights_only=False)

        policy2 = DQN(n_obs, n_actions, dueling=True, distributional="iqn", **kwargs)
        opt2 = optim.SGD(policy2.parameters(), lr=1e-3)
        sched2 = _build_scheduler(opt2, kind="cosine", t_max=50)
        sched2.load_state_dict(data["lr_scheduler"])
        assert abs(opt2.param_groups[0]["lr"] - lr_before) < 1e-9
    finally:
        os.unlink(path)
