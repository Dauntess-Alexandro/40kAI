"""Transport layer for AZ inference client (local mp.Queue or remote ZMQ)."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

import zmq

from core.models.az_inference_protocol import (
    AZ_PROTOCOL_VERSION,
    build_health_check_request,
    decode_message,
    encode_message,
)

AZ_DEFAULT_REMOTE_PORT = 5555


class AZInferenceTransport(ABC):
    @abstractmethod
    def send(self, request: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def recv(self, timeout: float) -> dict[str, Any]:
        raise NotImplementedError

    def close(self) -> None:
        pass


class LocalAZInferenceTransport(AZInferenceTransport):
    """mp.Queue roundtrip (variant B-local). Передача dict — не сериализованным msgpack."""

    def __init__(self, request_q: Any, reply_q: Any) -> None:
        self._request_q = request_q
        self._reply_q = reply_q

    def send(self, request: dict[str, Any]) -> None:
        self._request_q.put(request)

    def recv(self, timeout: float) -> dict[str, Any]:
        resp = self._reply_q.get(timeout=float(timeout))
        if not isinstance(resp, dict):
            raise TypeError(f"[AZ][LOCAL_TRANSPORT] ожидался dict, получен {type(resp)}")
        return resp


class RemoteAZInferenceTransport(AZInferenceTransport):
    """ZMQ DEALER клиент (variant B-remote). Identity = worker_id bytes."""

    def __init__(
        self,
        *,
        worker_id: int,
        host: str,
        port: int = AZ_DEFAULT_REMOTE_PORT,
        auth_token: str = "",
    ) -> None:
        self.worker_id = int(worker_id)
        self.host = str(host or "127.0.0.1").strip()
        self.port = int(port)
        self.auth_token = str(auth_token or "")
        self._context = zmq.Context.instance()
        self._socket = self._context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.IDENTITY, str(self.worker_id).encode("utf-8"))
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.setsockopt(zmq.RCVTIMEO, -1)
        self._socket.setsockopt(zmq.SNDTIMEO, -1)
        self._socket.connect(f"tcp://{self.host}:{self.port}")

    def send(self, request: dict[str, Any]) -> None:
        payload = dict(request)
        payload.setdefault("protocol_version", AZ_PROTOCOL_VERSION)
        payload.setdefault("auth_token", self.auth_token)
        self._socket.send(encode_message(payload))

    def recv(self, timeout: float) -> dict[str, Any]:
        deadline = time.perf_counter() + float(timeout)
        poll = zmq.Poller()
        poll.register(self._socket, zmq.POLLIN)
        remaining_ms = max(1, int((deadline - time.perf_counter()) * 1000.0))
        if not poll.poll(remaining_ms):
            raise TimeoutError(
                f"[AZ][REMOTE_CLIENT] worker_id={self.worker_id} recv timeout after {timeout}s. "
                "Где: az_inference_transport.RemoteAZInferenceTransport.recv. "
                "Что делать: проверьте, что az_remote_inference_server запущен на ПК2."
            )
        data = self._socket.recv()
        msg = decode_message(data)
        kind = str(msg.get("kind", "")).strip().lower()
        if kind == "error":
            raise RuntimeError(str(msg.get("message", "remote inference error")))
        if kind == "backpressure":
            wait_ms = int(msg.get("wait_ms", 50) or 50)
            time.sleep(max(0.001, wait_ms / 1000.0))
            raise TimeoutError(f"[AZ][REMOTE_CLIENT] backpressure wait_ms={wait_ms}")
        return msg

    def close(self) -> None:
        try:
            self._socket.close(linger=0)
        except Exception:
            pass


def make_az_transport(
    mode: str,
    *,
    request_q: Any = None,
    reply_q: Any = None,
    worker_id: int = 0,
    host: str = "127.0.0.1",
    port: int = AZ_DEFAULT_REMOTE_PORT,
    auth_token: str = "",
) -> AZInferenceTransport:
    m = str(mode or "local").strip().lower()
    if m == "remote":
        return RemoteAZInferenceTransport(
            worker_id=int(worker_id),
            host=host,
            port=int(port),
            auth_token=auth_token,
        )
    if request_q is None or reply_q is None:
        raise ValueError("local transport требует request_q и reply_q")
    return LocalAZInferenceTransport(request_q, reply_q)


def az_remote_health_check(
    *,
    host: str,
    port: int = AZ_DEFAULT_REMOTE_PORT,
    auth_token: str = "",
    timeout: float = 3.0,
) -> dict[str, Any]:
    """One-shot health check (GUI / pre-train проверка). Возвращает dict ответа."""
    ctx = zmq.Context.instance()
    sock = ctx.socket(zmq.DEALER)
    sock.setsockopt(zmq.IDENTITY, b"az_healthcheck")
    sock.setsockopt(zmq.LINGER, 0)
    sock.setsockopt(zmq.RCVTIMEO, int(float(timeout) * 1000.0))
    sock.setsockopt(zmq.SNDTIMEO, int(float(timeout) * 1000.0))
    host_s = str(host).strip() or "127.0.0.1"
    try:
        sock.connect(f"tcp://{host_s}:{int(port)}")
        sock.send(encode_message(build_health_check_request(auth_token=auth_token)))
        data = sock.recv()
        msg = decode_message(data)
        kind = str(msg.get("kind", "")).strip().lower()
        if kind == "error":
            raise RuntimeError(
                f"[AZ][REMOTE_CLIENT] health_check вернул ошибку: {msg.get('message', '?')}"
            )
        return msg
    except zmq.Again as exc:
        hint = ""
        if host_s in ("127.0.0.1", "localhost", "::1"):
            hint = (
                " Для IS LAN на ПК2 укажите inference_remote_host = IPv4 второго ПК "
                "(не 127.0.0.1 на ПК1)."
            )
        raise TimeoutError(
            f"[AZ][REMOTE_CLIENT] health_check timeout ({timeout}s) tcp://{host_s}:{int(port)}.{hint} "
            "Проверьте: pc2_remote_az_is.bat на ПК2, firewall TCP 5555, IP/порт."
        ) from exc
    finally:
        try:
            sock.close(linger=0)
        except Exception:
            pass
