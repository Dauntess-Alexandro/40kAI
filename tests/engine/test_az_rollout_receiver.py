"""Integration: ZMQ PUSH → PULL → mp.Queue via RolloutReceiver."""

from __future__ import annotations

import multiprocessing as mp
import time

import pytest

from core.models.az_rollout_protocol import build_wire_message, encode_rollout_message
from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import RemoteRolloutSink


def test_push_pull_to_data_q():
    ctx = mp.get_context("spawn")
    data_q: mp.Queue = ctx.Queue(maxsize=32)
    receiver = RolloutReceiver(
        data_q,
        bind_host="127.0.0.1",
        bind_port=15557,
        expected_contract_hash="hash1",
        auth_token="tok",
    )
    receiver.start()
    time.sleep(0.3)
    try:
        sink = RemoteRolloutSink(
            host="127.0.0.1",
            port=15557,
            auth_token="tok",
            worker_id=7,
            env_contract_hash="hash1",
        )
        import numpy as np

        time.sleep(0.2)
        sink.put(
            "rollout",
            {
                "actor_idx": 7,
                "policy_version": 1,
                "env_contract_hash": "hash1",
                "transitions": [
                    {
                        "state": np.asarray([0.1, 0.2], dtype=np.float32),
                        "policy_targets": [np.asarray([1.0, 0.0], dtype=np.float32)],
                        "value_target": 0.0,
                        "policy_version": 1,
                    }
                ],
            },
        )
        time.sleep(0.3)
        sink.close()
        deadline = time.time() + 5.0
        got_rollout = False
        while time.time() < deadline:
            try:
                kind, payload = data_q.get(timeout=0.5)
            except Exception:
                continue
            if kind == "rollout":
                assert payload.get("source") == "remote"
                assert len(payload.get("transitions", [])) == 1
                got_rollout = True
                break
        assert got_rollout
    finally:
        receiver.stop()


def test_active_remote_workers_counts_recent_heartbeats():
    import multiprocessing as mp

    ctx = mp.get_context("spawn")
    data_q: mp.Queue = ctx.Queue(maxsize=8)
    receiver = RolloutReceiver(data_q, bind_host="127.0.0.1", bind_port=15561)
    now = time.time()
    # 3 свежих воркера + 1 устаревший (> stale_sec назад)
    receiver._remote_workers = {100, 101, 102, 103}
    receiver._last_heartbeat = {100: now, 101: now - 5, 102: now - 1, 103: now - 120}
    assert receiver.active_remote_workers(stale_sec=30.0) == 3
    # без heartbeat'ов — fallback на число виденных воркеров
    receiver._last_heartbeat = {}
    assert receiver.active_remote_workers() == 4
