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
        bind_retry_sec: float = 25.0,
        ep_marker_fn: Callable[[int], None] | None = None,
        log_prefix: str = "[AZ][DIST]",
    ) -> None:
        self._data_q = data_q
        self._bind_host = str(bind_host or "0.0.0.0")
        self._bind_port = int(bind_port)
        self._contract_hash = str(expected_contract_hash or "")
        self._auth = str(auth_token or "")
        self._hwm = max(1, int(zmq_hwm))
        self._log = log_fn or (lambda _msg: None)
        self._log_prefix = str(log_prefix or "[AZ][DIST]").strip() or "[AZ][DIST]"
        self._receiver_prefix = f"{self._log_prefix}[RECEIVER]"
        # Колбэк своевременного прогресса: дёргается из потока приёмника на каждый ep
        # с накопительным счётчиком. Нужен GUI ПК1, чтобы прогресс ПК2 не зависел от
        # пропускной способности обучения learner'а (TRACE эмитится только при drain ep).
        self._ep_marker_fn = ep_marker_fn
        self._bind_retry_sec = max(0.0, float(bind_retry_sec))
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._pull = None
        self._remote_workers: set[int] = set()
        self._last_heartbeat: dict[int, float] = {}
        self._workers_lock = threading.Lock()
        self._dropped_contract = 0
        self._dropped_queue = 0
        self._received_rollouts = 0
        self._received_eps = 0

    def start(self, *, bind_retry_sec: float | None = None) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        if bind_retry_sec is not None:
            self._bind_retry_sec = max(0.0, float(bind_retry_sec))
        self._stop.clear()
        self._bind_pull_socket()
        self._thread = threading.Thread(target=self._run, name="az-rollout-receiver", daemon=True)
        self._thread.start()
        self._log(
            f"{self._receiver_prefix} started bind=tcp://{self._bind_host}:{self._bind_port} "
            f"contract_hash={self._contract_hash or '-'}"
        )

    def remote_worker_count(self) -> int:
        """Сколько distinct PC2-воркеров прислали hello (для ожидания перед стартом train)."""
        with self._workers_lock:
            return len(self._remote_workers)

    def active_remote_workers(self, *, stale_sec: float = 30.0) -> int:
        """Сколько PC2-воркеров слали hello/heartbeat недавно (для [TRAIN][DIST] прогресса)."""
        with self._workers_lock:
            if not self._last_heartbeat:
                return len(self._remote_workers)
            now = time.time()
            return sum(1 for ts in self._last_heartbeat.values() if (now - ts) <= float(stale_sec))

    def dropped_queue_count(self) -> int:
        return int(self._dropped_queue)

    def stop(self, *, join_timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=float(join_timeout))
        self._log(
            f"{self._receiver_prefix} stopped eps={self._received_eps} rollouts={self._received_rollouts} "
            f"dropped_contract={self._dropped_contract} dropped_queue={self._dropped_queue}"
        )

    def _bind_pull_socket(self) -> None:
        import zmq

        ctx = zmq.Context.instance()
        pull = ctx.socket(zmq.PULL)
        pull.setsockopt(zmq.RCVHWM, self._hwm)
        pull.setsockopt(zmq.LINGER, 0)
        endpoint = f"tcp://{self._bind_host}:{self._bind_port}"
        deadline = time.monotonic() + self._bind_retry_sec
        while True:
            try:
                pull.bind(endpoint)
                self._pull = pull
                return
            except zmq.ZMQError as exc:
                if getattr(exc, "errno", None) != zmq.EADDRINUSE:
                    raise RuntimeError(
                        f"Не удалось занять порт {self._bind_port} для приёма rollout. "
                        f"Где: RolloutReceiver._bind_pull_socket. Ошибка: {exc}"
                    ) from exc
                if time.monotonic() >= deadline:
                    raise RuntimeError(
                        f"Порт {self._bind_port} занят (Address in use) — не дождались освобождения за "
                        f"{int(self._bind_retry_sec)} с. Где: RolloutReceiver._bind_pull_socket. "
                        "Что делать: остановите прошлый train/GUI-процесс на ПК1 "
                        f"(netstat -ano | findstr :{self._bind_port}) и перезапустите."
                    ) from exc
                self._log(
                    f"{self._receiver_prefix} порт {self._bind_port} занят — повтор через 1 с "
                    f"(осталось ~{max(0, int(deadline - time.monotonic()))} с)"
                )
                time.sleep(1.0)

    def _run(self) -> None:
        import zmq

        pull = self._pull
        if pull is None:
            return
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
            self._pull = None

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
                f"{self._receiver_prefix} drop invalid message: {exc}. "
                "Где: RolloutReceiver._handle_message. "
                "Что делать: проверьте auth_token, protocol_version и env_contract_hash PC1↔PC2."
            )
            return

        wid = int(payload.get("worker_id", payload.get("actor_idx", -1)) or -1)
        if kind == "hello":
            with self._workers_lock:
                self._remote_workers.add(wid)
                self._last_heartbeat[wid] = time.time()
            self._log(f"{self._receiver_prefix} hello worker={wid} hash={payload.get('env_contract_hash', '')}")
            return

        if kind in ("heartbeat",):
            with self._workers_lock:
                self._last_heartbeat[wid] = time.time()
            return

        if kind == "error":
            self._enqueue("error", payload.get("message", payload))
            return

        if kind not in ("rollout", "ep", "batch"):
            return

        with self._workers_lock:
            self._last_heartbeat[wid] = time.time()
        payload.setdefault("source", "remote")
        self._enqueue(kind, payload)
        if kind in ("rollout", "batch"):
            self._received_rollouts += 1
        elif kind == "ep":
            self._received_eps += 1
            if self._ep_marker_fn is not None:
                try:
                    self._ep_marker_fn(self._received_eps)
                except Exception:
                    pass

    def _enqueue(self, kind: str, payload: Any) -> None:
        # ep/error не дропаем: иначе learner зависает на ep_done < total.
        if kind in ("ep", "error"):
            while not self._stop.is_set():
                try:
                    self._data_q.put((kind, payload), timeout=0.25)
                    return
                except queue.Full:
                    continue
            return
        try:
            self._data_q.put_nowait((kind, payload))
        except queue.Full:
            self._dropped_queue += 1
            self._log(
                f"{self._log_prefix} queue_full — data_q переполнена, {kind} отброшен. "
                "Где: RolloutReceiver. Что делать: увеличьте ACTOR_QUEUE_MAX или снизьте нагрузку PC2."
            )
