import numpy as np

from core.models.ppo_buffer import PPORolloutBuffer


def _fill_buffer(buf: PPORolloutBuffer, seed: int = 0):
    rng = np.random.default_rng(seed)
    for i in range(24):
        buf.add(
            obs=rng.random(4, dtype=np.float32),
            action=rng.integers(0, 3, size=2, dtype=np.int64),
            logprob=float(rng.random()),
            reward=float(rng.random()),
            done=bool(i % 7 == 6),
            value=float(rng.random()),
            masks_by_head=[np.ones(3, dtype=np.bool_), np.ones(2, dtype=np.bool_)],
            env_id=int(i % 3),
        )


def test_gae_torch_matches_numpy():
    buf_legacy = PPORolloutBuffer()
    buf_torch = PPORolloutBuffer()
    _fill_buffer(buf_legacy, seed=42)
    _fill_buffer(buf_torch, seed=42)

    ret_n, adv_n = buf_legacy.compute_returns_and_advantages(gamma=0.99, gae_lambda=0.95)
    ret_t, adv_t = buf_torch.compute_returns_and_advantages_torch(gamma=0.99, gae_lambda=0.95)

    np.testing.assert_allclose(ret_n, ret_t, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(adv_n, adv_t, rtol=1e-5, atol=1e-5)
