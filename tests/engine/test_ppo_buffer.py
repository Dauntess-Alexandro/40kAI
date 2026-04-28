import numpy as np
import torch

from core.models.ppo_buffer import PPORolloutBuffer


def test_ppo_buffer_returns_and_shapes():
    buf = PPORolloutBuffer()
    for i in range(8):
        masks = [np.array([True, True]), np.array([True, False, True])]
        buf.add(
            obs=np.array([i, i + 1, i + 2], dtype=np.float32),
            action=np.array([0, 2], dtype=np.int64),
            logprob=-0.1,
            reward=1.0,
            done=(i == 7),
            value=0.2,
            masks_by_head=masks,
        )
    batch = buf.to_tensors(device=torch.device("cpu"), gamma=0.99, gae_lambda=0.95, normalize_adv=True)
    assert batch.obs.shape == (8, 3)
    assert batch.actions.shape == (8, 2)
    assert batch.logprobs.shape == (8,)
    assert batch.returns.shape == (8,)
    assert batch.advantages.shape == (8,)
    assert len(batch.masks_by_head) == 2
    assert batch.masks_by_head[0].shape == (8, 2)
    assert batch.masks_by_head[1].shape == (8, 3)


