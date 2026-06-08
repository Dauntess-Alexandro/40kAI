# tests/models/test_dqn_dist_self_connect.py
"""DQN dist smoke: RemoteRolloutSink PUSH → RolloutReceiver PULL → data_q (127.0.0.1)."""
import queue
import time

import numpy as np
import pytest

from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import make_rollout_sink
from core.models.dqn_dist import RemoteDataQ

zmq = pytest.importorskip("zmq")


def test_batch_flows_sink_to_receiver():
    port = 5599
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, bind_host="127.0.0.1", bind_port=port, auth_token="t")
    rcv.start()
    time.sleep(0.6)  # дать PULL забиндиться
    try:
        sink = make_rollout_sink(
            mode="remote", source="remote", remote_host="127.0.0.1",
            remote_port=port, auth_token="t", worker_id=42, env_contract_hash="",
        )
        rq = RemoteDataQ(sink)
        s = np.arange(3, dtype=np.float32)
        rq.put(("batch", [(s, [1, 0, 0], 0.5, s, False, 2)]))
        # дождаться доставки
        got_kind = None
        got_payload = None
        deadline = time.time() + 5.0
        while time.time() < deadline:
            try:
                got_kind, got_payload = q.get(timeout=0.5)
                if got_kind == "batch":
                    break
            except queue.Empty:
                continue
        assert got_kind == "batch"
        assert isinstance(got_payload, dict)
        steps = got_payload["steps"]
        assert len(steps) == 1
        assert int(steps[0][5]) == 2
        rq.close()
    finally:
        rcv.stop()
