"""IPC helpers for GMZ inference server (no GPU required)."""

from __future__ import annotations

import multiprocessing as mp

import numpy as np
import pytest


def test_mp_queue_dict_roundtrip():
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    req = {
        "env_id": 0,
        "obs": np.zeros(4, dtype=np.float32),
        "legal_masks_by_head": [np.ones(3, dtype=bool)],
        "is_new_episode": True,
    }
    q.put(req)
    out = q.get(timeout=1.0)
    assert int(out["env_id"]) == 0
    assert np.asarray(out["obs"]).shape == (4,)


def test_gmz_inference_client_put_get():
    from core.models.gmz_inference_client import GMZInferenceClient

    ctx = mp.get_context("spawn")
    request_q = ctx.Queue()
    reply_q = ctx.Queue()
    client = GMZInferenceClient(0, request_q, reply_q, timeout=1.0, max_retries=1)

    def _fake_server():
        req = request_q.get(timeout=2.0)
        reply_q.put(
            {
                "env_id": int(req["env_id"]),
                "selected_actions": [0, 0, 0],
                "policy_targets": [np.ones(3, dtype=np.float32) / 3.0],
                "behavior_logits": [np.zeros(3, dtype=np.float32)],
                "value_est": 0.1,
                "policy_version": 1,
            }
        )

    import threading

    t = threading.Thread(target=_fake_server, daemon=True)
    t.start()
    resp = client.infer(
        obs=np.zeros(4, dtype=np.float32),
        legal_masks_by_head=[np.ones(3, dtype=bool)],
        step_in_episode=0,
        episode_id=0,
        is_new_episode=True,
    )
    assert resp["policy_version"] == 1
    assert len(resp["selected_actions"]) == 3
