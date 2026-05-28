"""Transport layer for GMZ inference client (local mp.Queue or remote ZMQ)."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

import zmq

from core.models.gmz_inference_protocol import (
    PROTOCOL_VERSION,
    build_health_check_request,
    build_infer_request,
    decode_message,
    encode_message,
)


class InferenceTransport(ABC):
    @abstractmethod
    def send(self, request: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def recv(self, timeout: float) -> dict[str, Any]:
        raise NotImplementedError

    def close(self) -> None:
        pass


class LocalInferenceTransport(InferenceTransport):
    """mp.Queue roundtrip (variant B-local)."""

    def __init__(self, request_q: Any, reply_q: Any) -> None:
        self._request_q = request_q
        self._reply_q = reply_q

    def send(self, request: dict[str, Any]) -> None:
        self._request_q.put(request)

    def recv(self, timeout: float) -> dict[str, Any]:
        resp = self._reply_q.get(timeout=float(timeout))
        if not isinstance(resp, dict):
            raise TypeError(f"expected dict response, got {type(resp)}")
        return resp


class RemoteInferenceTransport(InferenceTransport):
    """ZMQ DEALER client (variant B-remote). Identity = worker_id bytes."""

    def __init__(
        self,
        *,
        worker_id: int,
        host: str,
        port: int,
        auth_token: str = "",
        protocol_version: int = PROTOCOL_VERSION,
    ) -> None:
        self.worker_id = int(worker_id)
        self.host = str(host or "127.0.0.1").strip()
        self.port = int(port)
        self.auth_token = str(auth_token or "")
        self.protocol_version = int(protocol_version)
        self._context = zmq.Context.instance()
        self._socket = self._context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.IDENTITY, str(self.worker_id).encode("utf-8"))
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.setsockopt(zmq.RCVTIMEO, -1)
        self._socket.setsockopt(zmq.SNDTIMEO, -1)
        self._socket.connect(f"tcp://{self.host}:{self.port}")

    def send(self, request: dict[str, Any]) -> None:
        payload = dict(request)
        payload.setdefault("protocol_version", self.protocol_version)
        payload.setdefault("auth_token", self.auth_token)
        self._socket.send(encode_message(payload))

    def recv(self, timeout: float) -> dict[str, Any]:
        deadline = time.perf_counter() + float(timeout)
        poll = zmq.Poller()
        poll.register(self._socket, zmq.POLLIN)
        remaining_ms = max(1, int((deadline - time.perf_counter()) * 1000.0))
        if not poll.poll(remaining_ms):
            raise TimeoutError(
                f"[GMZ][REMOTE_CLIENT] worker_id={self.worker_id} recv timeout after {timeout}s"
            )
        data = self._socket.recv()
        msg = decode_message(data)
        kind = str(msg.get("kind", "")).strip().lower()
        if kind == "error":
            raise RuntimeError(str(msg.get("message", "remote inference error")))
        if kind == "backpressure":
            wait_ms = int(msg.get("wait_ms", 50) or 50)
            time.sleep(max(0.001, wait_ms / 1000.0))
            raise TimeoutError(f"[GMZ][REMOTE_CLIENT] backpressure wait_ms={wait_ms}")
        return msg

    def close(self) -> None:
        try:
            self._socket.close(linger=0)
        except Exception:
            pass


def make_transport(
    mode: str,
    *,
    request_q: Any = None,
    reply_q: Any = None,
    worker_id: int = 0,
    host: str = "127.0.0.1",
    port: int = 5555,
    auth_token: str = "",
) -> InferenceTransport:
    m = str(mode or "local").strip().lower()
    if m == "remote":
        return RemoteInferenceTransport(
            worker_id=int(worker_id),
            host=host,
            port=int(port),
            auth_token=auth_token,
        )
    if request_q is None or reply_q is None:
        raise ValueError("local transport requires request_q and reply_q")
    return LocalInferenceTransport(request_q, reply_q)


def remote_health_check(
    *,
    host: str,
    port: int,
    auth_token: str = "",
    timeout: float = 3.0,
) -> dict[str, Any]:
    """One-shot HealthCheck RPC (GUI / pre-train validation)."""
    ctx = zmq.Context.instance()
    sock = ctx.socket(zmq.DEALER)
    sock.setsockopt(zmq.IDENTITY, b"healthcheck")
    sock.setsockopt(zmq.LINGER, 0)
    sock.setsockopt(zmq.RCVTIMEO, int(float(timeout) * 1000.0))
    sock.setsockopt(zmq.SNDTIMEO, int(float(timeout) * 1000.0))
    try:
        sock.connect(f"tcp://{str(host).strip()}:{int(port)}")
        sock.send(encode_message(build_health_check_request(auth_token=auth_token)))
        data = sock.recv()
        msg = decode_message(data)
        kind = str(msg.get("kind", "")).strip().lower()
        if kind == "error":
            raise RuntimeError(str(msg.get("message", "health_check failed")))
        return msg
    finally:
        try:
            sock.close(linger=0)
        except Exception:
            pass
