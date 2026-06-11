import numpy as np
import pytest
import torch

import core.models.utils as U
import train
from core.models.DQN import DQN
from core.models.memory import ReplayMemory


def test_push_dqn_batch_steps_to_memory_batches_cpu_tensor_creation(monkeypatch):
    orig_tensor = train.torch.tensor
    tensor_calls = []

    def counting_tensor(data, *args, **kwargs):
        tensor_calls.append((np.asarray(data).shape, kwargs.get("device"), kwargs.get("dtype")))
        return orig_tensor(data, *args, **kwargs)

    monkeypatch.setattr(train.torch, "tensor", counting_tensor)

    memory = ReplayMemory(16)
    batch_steps = [
        (np.array([1.0, 2.0, 3.0, 4.0]), [1, 0, 2], 0.5, np.array([5.0, 6.0, 7.0, 8.0]), False, 3),
        (np.array([2.0, 3.0, 4.0, 5.0]), [0, 1, 1], -1.25, None, True, 1),
        (np.array([3.0, 4.0, 5.0, 6.0]), [2, 1, 0], 2.0, np.array([9.0, 8.0, 7.0, 6.0]), False, 2),
    ]

    pushed = train._push_dqn_batch_steps_to_memory(memory, batch_steps)

    assert pushed == 3
    assert len(memory) == 3
    assert [shape for shape, _device, _dtype in tensor_calls] == [
        (3, 4),
        (3, 3),
        (3,),
        (2, 4),
    ]

    transitions = memory.state_dict()["items"]
    assert transitions[0].state.shape == (1, 4)
    assert transitions[0].action.shape == (1, 3)
    assert transitions[0].reward.shape == (1,)
    assert transitions[0].next_state.shape == (1, 4)
    assert transitions[0].state.device.type == "cpu"
    assert transitions[0].reward.device.type == "cpu"
    assert transitions[0].next_state.device.type == "cpu"
    assert transitions[1].next_state is None
    assert transitions[2].n_step == 2
    assert transitions[0].state.untyped_storage().nbytes() == transitions[0].state.numel() * transitions[0].state.element_size()
    assert transitions[0].next_state.untyped_storage().nbytes() == transitions[0].next_state.numel() * transitions[0].next_state.element_size()

    torch.testing.assert_close(transitions[0].state, orig_tensor([[1.0, 2.0, 3.0, 4.0]]))
    torch.testing.assert_close(transitions[2].next_state, orig_tensor([[9.0, 8.0, 7.0, 6.0]]))


def test_resolve_dqn_updates_per_batch_scales_for_distributed_actors():
    assert train._resolve_dqn_updates_per_batch(
        8,
        num_local_actors=8,
        num_remote_actors=8,
        distributed_enabled=True,
    ) == 4
    assert train._resolve_dqn_updates_per_batch(
        8,
        num_local_actors=8,
        num_remote_actors=8,
        distributed_enabled=False,
    ) == 8
    assert train._resolve_dqn_updates_per_batch(
        1,
        num_local_actors=1,
        num_remote_actors=99,
        distributed_enabled=True,
    ) == 1


def test_format_dqn_queue_metrics_includes_perf_fields():
    line = train._format_dqn_queue_metrics(
        qsize=17,
        dropped_batches=3,
        push_batch_ms=1.234,
        optimize_ms=45.678,
        updates_per_sec=2.5,
        batches=4,
        transitions=128,
        updates=16,
        interval_s=6.0,
    )

    assert line.startswith("[DQN][PERF] ")
    assert "qsize=17" in line
    assert "dropped_batches=3" in line
    assert "push_batch_ms=1.23" in line
    assert "optimize_ms=45.68" in line
    assert "updates/sec=2.50" in line


def test_cpu_replay_batch_can_optimize_on_cuda_when_available():
    if not torch.cuda.is_available():
        pytest.skip("CUDA unavailable")

    old_batch_size = U.BATCH_SIZE
    U.BATCH_SIZE = 2
    try:
        n_obs = 4
        n_actions = [3, 2, 4]
        device = torch.device("cuda")
        policy = DQN(
            n_obs,
            n_actions,
            dueling=False,
            noisy=False,
            distributional=None,
            hidden_size=32,
            num_layers=1,
        ).to(device)
        target = DQN(
            n_obs,
            n_actions,
            dueling=False,
            noisy=False,
            distributional=None,
            hidden_size=32,
            num_layers=1,
        ).to(device)
        target.load_state_dict(policy.state_dict())
        optimizer = torch.optim.SGD(policy.parameters(), lr=1e-3)
        memory = ReplayMemory(8)
        batch_steps = [
            (np.full(n_obs, 0.0, dtype=np.float32), [0, 1, 2], 0.0, np.full(n_obs, 1.0, dtype=np.float32), False, 1),
            (np.full(n_obs, 1.0, dtype=np.float32), [1, 0, 3], 0.5, np.full(n_obs, 2.0, dtype=np.float32), False, 1),
            (np.full(n_obs, 2.0, dtype=np.float32), [2, 1, 0], -0.25, None, True, 1),
        ]

        train._push_dqn_batch_steps_to_memory(memory, batch_steps)
        assert memory.state_dict()["items"][0].state.device.type == "cpu"

        result = U.optimize_model(
            policy,
            target,
            optimizer,
            memory,
            n_obs,
            double_dqn_enabled=True,
            per_enabled=False,
            use_amp=False,
        )

        assert result is not None
        assert result["loss"] >= 0.0
    finally:
        U.BATCH_SIZE = old_batch_size
