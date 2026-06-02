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
