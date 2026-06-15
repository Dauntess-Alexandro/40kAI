import numpy as np
import torch
from core.models.smz_inference_server import SMZInferenceServer

from core.models.sampled_muzero_model import make_sampled_muzero_net
from core.models.sampled_muzero_search import (
    BatchedSampledMuZeroSearch,
    SampledMuZeroSearchConfig,
)


def _make_net(n_obs, n_actions):
    torch.manual_seed(0)
    return make_sampled_muzero_net(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=32, hidden_dim=32, num_layers=1, action_embed_dim=8,
    )


def _make_batch(n_obs, n_actions, n_envs, seed=7):
    rng = np.random.default_rng(seed)
    batch = []
    for env_id in range(n_envs):
        obs = rng.standard_normal(n_obs).astype(np.float32)
        masks = []
        for size in n_actions:
            m = rng.integers(0, 2, size=size).astype(bool)
            if not m.any():
                m[0] = True
            masks.append(m)
        batch.append({"env_id": env_id, "obs": obs,
                      "legal_masks_by_head": masks, "is_new_episode": True})
    return batch


def _server(net, cfg):
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    return SMZInferenceServer(
        net=net, search_config=cfg, device=torch.device("cpu"),
        request_queue=ctx.Queue(), reply_queues=[ctx.Queue() for _ in range(8)],
        sync_path="", sync_check_interval=999.0,
        inference_batch_size=8, inference_batch_interval_s=0.02,
        compile_mode=False,
    )


def test_server_build_batch_responses_contract():
    n_obs, n_actions, n_envs = 10, [4, 3], 5
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=16, prior_weight=0.0)
    srv = _server(net, cfg)
    batch = _make_batch(n_obs, n_actions, n_envs)
    np.random.seed(1)
    responses = srv.build_batch_responses(batch)
    assert len(responses) == n_envs
    for resp in responses:
        assert resp["kind"] == "infer_response"
        assert len(resp["selected_actions"]) == len(n_actions)
        assert len(resp["policy_targets"]) == len(n_actions)
        for h, size in enumerate(n_actions):
            p = resp["policy_targets"][h]
            assert p.shape[0] == size and abs(float(p.sum()) - 1.0) < 1e-5
            eid = int(resp["env_id"])
            assert batch[eid]["legal_masks_by_head"][h][resp["selected_actions"][h]]
        assert len(resp["behavior_logits"]) == len(n_actions)
        assert isinstance(resp["value_est"], float)
    srv.stop()


def test_server_matches_direct_sampled_search():
    n_obs, n_actions, n_envs = 10, [4, 3], 4
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=16, prior_weight=0.0)
    batch = _make_batch(n_obs, n_actions, n_envs, seed=3)
    requests = [{"env_id": b["env_id"], "obs": b["obs"],
                 "legal_masks_by_head": b["legal_masks_by_head"]} for b in batch]

    np.random.seed(99)
    direct = BatchedSampledMuZeroSearch(
        net=net, config=cfg, device=torch.device("cpu")
    ).run_batched_stateful(requests, deterministic=False)

    srv = _server(net, cfg)
    np.random.seed(99)
    served = srv.build_batch_responses(batch)
    srv.stop()

    served_by_env = {int(r["env_id"]): r for r in served}
    for d in direct:
        s = served_by_env[int(d["env_id"])]
        assert s["selected_actions"] == list(d["selected_actions"])
        for h in range(len(n_actions)):
            np.testing.assert_allclose(s["policy_targets"][h], d["policy_targets"][h], atol=1e-5)


def test_server_uses_sampled_search_not_gmz():
    net = _make_net(8, [3])
    cfg = SampledMuZeroSearchConfig(num_samples=8)
    srv = _server(net, cfg)
    assert isinstance(srv._batched_search, BatchedSampledMuZeroSearch)
    srv.stop()
