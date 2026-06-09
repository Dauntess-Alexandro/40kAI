# tests/models/test_dqn_dist_ep_marker.py
"""ПК2-прогресс в GUI берётся из приёмника (своевременно), а не из learner-TRACE.

RolloutReceiver вызывает ep_marker_fn(received_eps) сразу при приёме каждого ep —
независимо от пропускной способности обучения на ПК1.
"""
import queue
import time

import pytest

from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import make_rollout_sink
from core.models.dqn_dist import RemoteDataQ

zmq = pytest.importorskip("zmq")


def test_ep_marker_fn_called_with_received_count():
    port = 5601
    q: queue.Queue = queue.Queue()
    seen: list[int] = []
    rcv = RolloutReceiver(
        q,
        bind_host="127.0.0.1",
        bind_port=port,
        auth_token="t",
        ep_marker_fn=seen.append,
    )
    rcv.start()
    time.sleep(0.6)  # дать PULL забиндиться
    try:
        sink = make_rollout_sink(
            mode="remote", source="remote", remote_host="127.0.0.1",
            remote_port=port, auth_token="t", worker_id=101, env_contract_hash="",
        )
        rq = RemoteDataQ(sink)
        rq.put(("ep", {"episode": 1, "actor_idx": 101, "ep_reward": 0.0}))
        rq.put(("ep", {"episode": 2, "actor_idx": 101, "ep_reward": 0.0}))
        deadline = time.time() + 5.0
        while time.time() < deadline and len(seen) < 2:
            time.sleep(0.05)
        rq.close()
    finally:
        rcv.stop()

    assert seen == [1, 2], f"ожидали накопительный счётчик ep [1, 2], получили {seen}"
