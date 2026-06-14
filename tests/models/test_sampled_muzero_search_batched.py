import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.sampled_muzero_search import (
    SampledMuZeroSearch,
    SampledMuZeroSearchConfig,
    run_batched,
)


def _make_net(n_obs, n_actions):
    torch.manual_seed(0)
    return GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions,
                           latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16)


def _make_requests(n_obs, n_actions, n_envs, seed=7):
    rng = np.random.default_rng(seed)
    reqs = []
    for env_id in range(n_envs):
        obs = rng.standard_normal(n_obs).astype(np.float32)
        masks = []
        for size in n_actions:
            m = rng.integers(0, 2, size=size).astype(bool)
            if not m.any():
                m[0] = True
            masks.append(m)
        reqs.append({"env_id": env_id, "obs": obs, "legal_masks_by_head": masks})
    return reqs


def test_run_batched_matches_sequential_deterministic():
    n_obs, n_actions, n_envs = 12, [4, 3, 5], 6
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=20, temperature=0.15, prior_weight=0.0)
    device = torch.device("cpu")
    reqs = _make_requests(n_obs, n_actions, n_envs)

    np.random.seed(123)
    seq = []
    for r in reqs:
        s = SampledMuZeroSearch(net=net, config=cfg, device=device)
        seq.append(s.run(obs=r["obs"], legal_masks_by_head=r["legal_masks_by_head"], deterministic=True))

    np.random.seed(123)
    bat = run_batched(net=net, cfg=cfg, device=device, requests=reqs, deterministic=True)

    assert len(bat) == n_envs
    for n, (pi, beh, act, val) in enumerate(seq):
        b = bat[n]
        assert b["env_id"] == reqs[n]["env_id"]
        assert b["selected_actions"] == list(act), f"env {n} actions mismatch"
        assert abs(b["value_est"] - val) < 1e-4, f"env {n} value mismatch"
        for h in range(len(n_actions)):
            np.testing.assert_allclose(b["policy_targets"][h], pi[h], atol=1e-5)
            np.testing.assert_allclose(b["behavior_logits"][h], beh[h], atol=1e-5)


def test_run_batched_shapes_and_legality_stochastic():
    n_obs, n_actions, n_envs = 10, [4, 3], 5
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=16)
    reqs = _make_requests(n_obs, n_actions, n_envs, seed=42)
    np.random.seed(1)
    out = run_batched(net=net, cfg=cfg, device=torch.device("cpu"), requests=reqs, deterministic=False)
    assert len(out) == n_envs
    for n, r in enumerate(out):
        for h, size in enumerate(n_actions):
            p = r["policy_targets"][h]
            assert p.shape[0] == size and abs(float(p.sum()) - 1.0) < 1e-5
            assert reqs[n]["legal_masks_by_head"][h][r["selected_actions"][h]]
