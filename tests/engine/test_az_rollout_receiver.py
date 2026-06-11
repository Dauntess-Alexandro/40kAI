"""Integration: ZMQ PUSH → PULL → mp.Queue via RolloutReceiver."""

from __future__ import annotations

import multiprocessing as mp
import threading
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


def test_enqueue_ep_blocks_instead_of_drop_when_queue_full():
    """ep не должен теряться при переполнении data_q (блокирующий put)."""
    import queue as std_queue

    class _BlockingQueue:
        def __init__(self) -> None:
            self._items: list = []
            self._max = 1
            self.put_nowait_calls = 0
            self.blocking_puts = 0

        def put_nowait(self, item) -> None:
            self.put_nowait_calls += 1
            if len(self._items) >= self._max:
                raise std_queue.Full
            self._items.append(item)

        def put(self, item, timeout=None) -> None:
            self.blocking_puts += 1
            deadline = time.time() + float(timeout or 1.0)
            while len(self._items) >= self._max:
                if time.time() >= deadline:
                    raise std_queue.Full
                time.sleep(0.01)
            self._items.append(item)

    q = _BlockingQueue()
    receiver = RolloutReceiver(q, bind_host="127.0.0.1", bind_port=15562)
    q.put_nowait(("batch", {"steps": []}))

    def _drain_one() -> None:
        time.sleep(0.05)
        if q._items:
            q._items.pop(0)

    threading.Thread(target=_drain_one, daemon=True).start()
    receiver._enqueue("ep", {"result": "win"})
    assert len(q._items) == 1
    assert q._items[0][0] == "ep"
    assert q.blocking_puts >= 1


def test_enqueue_batch_dropped_on_queue_full():
    import queue as std_queue

    class _FullQueue:
        def put_nowait(self, _item) -> None:
            raise std_queue.Full

        def put(self, *_args, **_kwargs) -> None:
            raise AssertionError("batch не должен блокировать")

    logs: list[str] = []
    q = _FullQueue()
    receiver = RolloutReceiver(q, bind_host="127.0.0.1", bind_port=15563, log_fn=logs.append)
    receiver._enqueue("batch", {"steps": []})
    assert receiver._dropped_queue == 1
    assert any("queue_full" in line for line in logs)


def test_enqueue_batch_uses_custom_log_prefix_when_queue_full():
    import queue as std_queue

    class _FullQueue:
        def put_nowait(self, _item) -> None:
            raise std_queue.Full

        def put(self, *_args, **_kwargs) -> None:
            raise AssertionError("batch must not block")

    logs: list[str] = []
    q = _FullQueue()
    receiver = RolloutReceiver(
        q,
        bind_host="127.0.0.1",
        bind_port=15564,
        log_fn=logs.append,
        log_prefix="[DQN][DIST]",
    )

    receiver._enqueue("batch", {"steps": []})

    assert receiver.dropped_queue_count() == 1
    assert any(line.startswith("[DQN][DIST] queue_full") for line in logs)
    assert not any(line.startswith("[AZ][DIST] queue_full") for line in logs)


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
