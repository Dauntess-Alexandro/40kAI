"""ZMQ PULL receiver → mp.Queue for AZ distributed self-play on learner (PC1)."""

from __future__ import annotations

import queue
import threading
import time
from collections.abc import Callable
from typing import Any

from core.models.az_rollout_protocol import decode_rollout_message, validate_wire_message


class RolloutReceiver:
    def __init__(
        self,
        data_q,
        *,
        bind_host: str = "0.0.0.0",
        bind_port: int = 5557,
        expected_contract_hash: str = "",
        auth_token: str = "",
        zmq_hwm: int = 256,
        log_fn: Callable[[str], None] | None = None,
    ) -> None:
        self._data_q = data_q
        self._bind_host = str(bind_host or "0.0.0.0")
        self._bind_port = int(bind_port)
        self._contract_hash = str(expected_contract_hash or "")
        self._auth = str(auth_token or "")
        self._hwm = max(1, int(zmq_hwm))
        self._log = log_fn or (lambda _msg: None)
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._remote_workers: set[int] = set()
        self._last_heartbeat: dict[int, float] = {}
        self._dropped_contract = 0
        self._received_rollouts = 0
        self._received_eps = 0

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="az-rollout-receiver", daemon=True)
        self._thread.start()
        self._log(
            f"[AZ][DIST][RECEIVER] started bind=tcp://{self._bind_host}:{self._bind_port} "
            f"contract_hash={self._contract_hash or '-'}"
        )

    def active_remote_workers(self, *, stale_sec: float = 30.0) -> int:
        """Сколько PC2-воркеров слали hello/heartbeat недавно (для [TRAIN][DIST] прогресса)."""
        if not self._last_heartbeat:
            return len(self._remote_workers)
        now = time.time()
        return sum(1 for ts in self._last_heartbeat.values() if (now - ts) <= float(stale_sec))

    def stop(self, *, join_timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=float(join_timeout))
        self._log(
            f"[AZ][DIST][RECEIVER] stopped eps={self._received_eps} rollouts={self._received_rollouts} "
            f"dropped_contract={self._dropped_contract}"
        )

    def _run(self) -> None:
        import zmq

        ctx = zmq.Context.instance()
        pull = ctx.socket(zmq.PULL)
        pull.setsockopt(zmq.RCVHWM, self._hwm)
        pull.setsockopt(zmq.LINGER, 0)
        pull.bind(f"tcp://{self._bind_host}:{self._bind_port}")
        poller = zmq.Poller()
        poller.register(pull, zmq.POLLIN)
        try:
            while not self._stop.is_set():
                socks = dict(poller.poll(timeout=200))
                if pull not in socks:
                    continue
                try:
                    data = pull.recv(zmq.NOBLOCK)
                except zmq.Again:
                    continue
                self._handle_message(data)
        finally:
            try:
                pull.close(linger=0)
            except Exception:
                pass

    def _handle_message(self, data: bytes) -> None:
        try:
            wire = decode_rollout_message(data)
            kind, payload = validate_wire_message(
                wire,
                auth_token=self._auth,
                expected_contract_hash=self._contract_hash,
            )
        except Exception as exc:
            self._dropped_contract += 1
            self._log(
                f"[AZ][DIST][RECEIVER] drop invalid message: {exc}. "
                "Где: RolloutReceiver._handle_message. "
                "Что делать: проверьте auth_token, protocol_version и env_contract_hash PC1↔PC2."
            )
            return

        wid = int(payload.get("worker_id", payload.get("actor_idx", -1)) or -1)
        if kind == "hello":
            self._remote_workers.add(wid)
            self._last_heartbeat[wid] = time.time()
            self._log(f"[AZ][DIST][RECEIVER] hello worker={wid} hash={payload.get('env_contract_hash', '')}")
            return

        if kind in ("heartbeat",):
            self._last_heartbeat[wid] = time.time()
            return

        if kind == "error":
            self._enqueue("error", payload.get("message", payload))
            return

        if kind not in ("rollout", "ep", "batch"):
            return

        self._last_heartbeat[wid] = time.time()
        payload.setdefault("source", "remote")
        self._enqueue(kind, payload)
        if kind in ("rollout", "batch"):
            self._received_rollouts += 1
        elif kind == "ep":
            self._received_eps += 1

    def _enqueue(self, kind: str, payload: Any) -> None:
        try:
            self._data_q.put_nowait((kind, payload))
        except queue.Full:
            self._log(
                "[AZ][DIST] queue_full — data_q переполнена, rollout отброшен. "
                "Где: RolloutReceiver. Что делать: увеличьте AZ_ACTOR_QUEUE_MAX или снизьте число PC2-воркеров."
            )
