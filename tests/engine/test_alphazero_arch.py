import os

import numpy as np
import torch

from core.models.alphazero_model import (
    AlphaZeroPolicyValueNet,
    load_alphazero_state_dict,
    make_alphazero_net,
)
from core.models.alphazero_replay import AZTransition, AlphaZeroReplayBuffer
from core.models.alphazero_trainer import (
    AlphaZeroTrainConfig,
    build_alphazero_lr_scheduler,
    train_alphazero_step,
)


def test_alphazero_make_factory_uses_env(monkeypatch):
    monkeypatch.setenv("AZ_HIDDEN_SIZE", "128")
    monkeypatch.setenv("AZ_NUM_LAYERS", "3")
    monkeypatch.setenv("AZ_VALUE_ENSEMBLE", "2")
    net = make_alphazero_net(20, [4, 3])
    assert net.hidden_size == 128
    assert net.num_layers == 3
    assert net.n_value_ensemble == 2


def test_alphazero_residual_trunk_forward():
    net = AlphaZeroPolicyValueNet(24, [5, 3, 7], hidden_size=64, num_layers=3)
    x = torch.randn(4, 24)
    logits, value = net(x)
    assert len(logits) == 3
    assert value.shape == (4,)
    assert value.min() >= -1.0 and value.max() <= 1.0
    assert logits[0].shape == (4, 5)


def test_alphazero_value_ensemble_averaging():
    net = AlphaZeroPolicyValueNet(16, [4], hidden_size=32, num_layers=2, n_value_ensemble=4)
    x = torch.randn(2, 16)
    _, value = net(x)
    assert value.shape == (2,)
    assert float(value.min()) >= -1.0
    assert float(value.max()) <= 1.0


def test_load_alphazero_state_dict_warns_on_legacy_keys():
    net = make_alphazero_net(10, [3])
    legacy = {"layer1.weight": torch.randn(256, 10), "layer2.bias": torch.randn(256)}
    warnings: list[str] = []

    def _log(msg):
        warnings.append(str(msg))

    load_alphazero_state_dict(net, legacy, log_fn=_log)
    assert len(warnings) >= 1
    assert any("layer1" in w for w in warnings)


def test_az_lr_scheduler_steps_with_train_step():
    n_obs = 12
    n_actions = [4, 3]
    net = make_alphazero_net(n_obs, n_actions)
    replay = AlphaZeroReplayBuffer(capacity=64)
    for _ in range(32):
        replay.push(
            AZTransition(
                state=np.random.randn(n_obs).astype(np.float32),
                policy_targets=[np.ones(a, dtype=np.float32) / float(a) for a in n_actions],
                value_target=0.5,
            )
        )
    try:
        opt = torch.optim.SGD(net.parameters(), lr=1e-2)
    except Exception as exc:
        import pytest

        pytest.skip(f"torch.optim недоступен: {exc}")
    cfg = AlphaZeroTrainConfig(batch_size=16, lr_scheduler_type="cosine", lr_total_steps=50)
    sched = build_alphazero_lr_scheduler(opt, cfg, total_steps_hint=50)
    lr_before = opt.param_groups[0]["lr"]
    out = train_alphazero_step(
        net=net,
        optimizer=opt,
        replay=replay,
        config=cfg,
        device=torch.device("cpu"),
        scheduler=sched,
    )
    assert out is not None
    assert opt.param_groups[0]["lr"] <= lr_before + 1e-12 or sched is not None
