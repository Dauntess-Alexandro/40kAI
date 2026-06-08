# tests/models/test_dqn_dist_contract_guard.py
"""DQN dist: receiver кладёт 'batch' в очередь и дропает чужой env_contract_hash."""
import queue
import time

import numpy as np
import pytest

from core.models.az_rollout_protocol import (
    build_wire_message,
    encode_rollout_message,
)
from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import make_rollout_sink
from core.models.dqn_dist import RemoteDataQ


def _batch_wire(hash_val: str):
    payload = {"worker_id": 1, "steps": [], "priority": None, "env_contract_hash": hash_val}
    wire = build_wire_message(kind="batch", payload=payload, auth_token="")
    return encode_rollout_message(wire)


def test_batch_enqueued_when_hash_matches():
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, expected_contract_hash="H1")
    rcv._handle_message(_batch_wire("H1"))
    kind, payload = q.get_nowait()
    assert kind == "batch"
    assert payload["source"] == "remote"


def test_batch_dropped_when_hash_mismatch():
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, expected_contract_hash="H1")
    rcv._handle_message(_batch_wire("H2"))
    assert q.empty()


def _drain_for_batch(q: "queue.Queue", timeout: float = 3.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            kind, payload = q.get(timeout=0.3)
        except queue.Empty:
            continue
        if kind == "batch":
            return payload
    return None


def test_real_sink_stamps_hash_and_receiver_drops_mismatch():
    """Регрессия: RemoteRolloutSink должен проставлять env_contract_hash в каждый batch,
    иначе контракт-гард на ПК1 пропускает чужие переходы в replay."""
    pytest.importorskip("zmq")
    port = 5601
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, bind_host="127.0.0.1", bind_port=port, expected_contract_hash="H1", auth_token="t")
    rcv.start()
    time.sleep(0.6)
    s = np.arange(2, dtype=np.float32)
    batch = [(s, [0, 0, 0], 0.0, s, False, 1)]
    try:
        # Чужой контракт H2 — все batch должны дропаться, не только hello.
        bad = RemoteDataQ(
            make_rollout_sink(
                mode="remote", source="remote", remote_host="127.0.0.1",
                remote_port=port, auth_token="t", worker_id=1, env_contract_hash="H2",
            )
        )
        bad.put(("batch", batch))
        assert _drain_for_batch(q, timeout=2.0) is None, "batch с чужим контрактом просочился в replay"
        bad.close()

        # Свой контракт H1 — batch проходит.
        good = RemoteDataQ(
            make_rollout_sink(
                mode="remote", source="remote", remote_host="127.0.0.1",
                remote_port=port, auth_token="t", worker_id=2, env_contract_hash="H1",
            )
        )
        good.put(("batch", batch))
        payload = _drain_for_batch(q, timeout=3.0)
        assert payload is not None and payload["env_contract_hash"] == "H1"
        good.close()
    finally:
        rcv.stop()
