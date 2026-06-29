import queue
import time

import numpy as np
import pytest

from core.models.az_rollout_protocol import build_wire_message, encode_rollout_message
from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import make_rollout_sink
from core.models.phoenix_dist import PhoenixRemoteDataQ, PhoenixSequenceAssembler, pack_phoenix_batch


def _phoenix_payload(hash_val: str):
    asm = PhoenixSequenceAssembler(window=2)
    emitted = []
    for t in range(3):
        emitted.extend(asm.append([t, t], [0], [True], reward=float(t), done=(t == 2)))
    windows = [w for w, _m in emitted]
    metas = [m for _w, m in emitted]
    return pack_phoenix_batch(windows, worker_id=1, env_contract_hash=hash_val, metas=metas, source="remote")


def test_phoenix_batch_enqueued_when_hash_matches():
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, expected_contract_hash="H1", log_prefix="[PHOENIX][DIST]")
    wire = build_wire_message(kind="phoenix_batch", payload=_phoenix_payload("H1"), auth_token="")
    rcv._handle_message(encode_rollout_message(wire))
    kind, payload = q.get_nowait()
    assert kind == "phoenix_batch"
    assert payload["source"] == "remote"
    assert np.asarray(payload["obs"]).shape[0] > 0


def test_phoenix_batch_dropped_when_hash_mismatch():
    q: queue.Queue = queue.Queue()
    seen: list[str] = []
    rcv = RolloutReceiver(q, expected_contract_hash="H1", log_fn=seen.append, log_prefix="[PHOENIX][DIST]")
    wire = build_wire_message(kind="phoenix_batch", payload=_phoenix_payload("H2"), auth_token="")
    rcv._handle_message(encode_rollout_message(wire))
    assert q.empty()
    assert any("env_contract_hash" in line and "Что делать" in line for line in seen)


def test_real_sink_sends_phoenix_batch_with_hash():
    pytest.importorskip("zmq")
    port = 5612
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(
        q,
        bind_host="127.0.0.1",
        bind_port=port,
        expected_contract_hash="H1",
        auth_token="t",
        log_prefix="[PHOENIX][DIST]",
    )
    rcv.start()
    time.sleep(0.6)
    try:
        sink = make_rollout_sink(
            mode="remote",
            source="remote",
            remote_host="127.0.0.1",
            remote_port=port,
            auth_token="t",
            worker_id=2,
            env_contract_hash="H1",
        )
        rq = PhoenixRemoteDataQ(sink)
        rq.put(("phoenix_batch", _phoenix_payload("ignored_by_sink")))
        deadline = time.time() + 3.0
        got = None
        while time.time() < deadline:
            try:
                kind, payload = q.get(timeout=0.2)
            except queue.Empty:
                continue
            if kind == "phoenix_batch":
                got = payload
                break
        rq.close()
    finally:
        rcv.stop()
    assert got is not None
    assert got["env_contract_hash"] == "H1"
