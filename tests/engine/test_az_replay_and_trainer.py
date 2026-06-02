"""Tests for AZ replay balanced sampling (no full-buffer scan) + trainer tensor build."""

from __future__ import annotations

import numpy as np
import torch

from core.models.alphazero_replay import AlphaZeroReplayBuffer, AZTransition
from core.models.alphazero_model import make_alphazero_net
from core.models.alphazero_trainer import AlphaZeroTrainConfig, train_alphazero_step


HEADS = [5, 2, 4]
N_OBS = 16


def _mk(value: float) -> AZTransition:
    return AZTransition(
        state=np.zeros(N_OBS, dtype=np.float32),
        policy_targets=[np.full(h, 1.0 / h, dtype=np.float32) for h in HEADS],
        value_target=float(value),
        policy_version=0,
        faction="X",
    )


def _fill(n_win: int, n_loss: int, n_draw: int) -> AlphaZeroReplayBuffer:
    rb = AlphaZeroReplayBuffer(capacity=10000)
    for _ in range(n_win):
        rb.push(_mk(1.0))
    for _ in range(n_loss):
        rb.push(_mk(-1.0))
    for _ in range(n_draw):
        rb.push(_mk(-0.25))
    return rb


class TestBalancedOutcomeSampling:
    def test_returns_batch_size(self):
        rb = _fill(500, 500, 500)
        out = rb.sample_balanced_outcome(128)
        assert len(out) == 128
        assert all(isinstance(t, AZTransition) for t in out)

    def test_small_buffer_returns_all(self):
        rb = _fill(10, 10, 10)
        out = rb.sample_balanced_outcome(128)
        assert len(out) == 30  # буфер <= bs → весь буфер

    def test_balances_dominant_outcome(self):
        # 95% wins, 5% losses/draws — balanced должен поднять долю не-win
        rb = _fill(950, 25, 25)
        # усредним по нескольким запускам (сэмплинг рандомный)
        non_win = 0
        trials = 20
        for _ in range(trials):
            out = rb.sample_balanced_outcome(60)
            non_win += sum(1 for t in out if t.value_target <= 0.20)
        frac_non_win = non_win / (trials * 60)
        # при чистом uniform было бы ~5%; balanced должен дать заметно больше
        assert frac_non_win > 0.15, f"balanced не поднял долю редких исходов: {frac_non_win:.2f}"

    def test_only_one_outcome(self):
        rb = _fill(500, 0, 0)
        out = rb.sample_balanced_outcome(64)
        assert len(out) == 64
        assert all(t.value_target == 1.0 for t in out)

    def test_does_not_scan_whole_buffer(self, monkeypatch):
        # Проверяем O(подвыборка), а не O(N): random.sample вызывается на буфере
        # с oversample = bs * BALANCED_OVERSAMPLE, а не итерируется весь буфер.
        rb = _fill(4000, 4000, 4000)
        calls = {}
        import core.models.alphazero_replay as mod
        real_sample = mod.random.sample

        def spy(pop, k):
            calls["first_k"] = calls.get("first_k", k)
            return real_sample(pop, k)

        monkeypatch.setattr(mod.random, "sample", spy)
        rb.sample_balanced_outcome(128)
        # первый sample — кандидаты: 128 * 4 = 512, не 12000
        assert calls["first_k"] == 128 * rb.BALANCED_OVERSAMPLE


class TestTrainerTensorBuild:
    def test_step_runs_and_trains_value(self):
        rb = _fill(200, 200, 200)
        net = make_alphazero_net(N_OBS, HEADS, hidden_size=32, num_layers=1)
        opt = torch.optim.AdamW(net.parameters(), lr=1e-3)
        cfg = AlphaZeroTrainConfig(batch_size=64, balanced_outcome_sampling=True)
        info = train_alphazero_step(
            net=net, optimizer=opt, replay=rb, config=cfg, device=torch.device("cpu")
        )
        assert info is not None
        assert np.isfinite(info["loss"]) and np.isfinite(info["value_loss"])

    def test_value_head_receives_gradient(self):
        rb = _fill(100, 100, 100)
        net = make_alphazero_net(N_OBS, HEADS, hidden_size=32, num_layers=1)
        opt = torch.optim.SGD(net.parameters(), lr=0.0)  # lr=0: веса не двинутся, но grad посчитается
        cfg = AlphaZeroTrainConfig(batch_size=64, balanced_outcome_sampling=False)

        # хук: после backward проверим, что у value-головы есть градиент
        train_alphazero_step(net=net, optimizer=opt, replay=rb, config=cfg, device=torch.device("cpu"))
        vh = net.value_heads[0]
        assert vh.weight.grad is not None
        assert float(vh.weight.grad.abs().sum()) > 0.0, "value head не получил градиент"
