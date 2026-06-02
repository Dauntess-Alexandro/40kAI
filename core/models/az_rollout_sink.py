"""Rollout emission: local mp.Queue or remote ZMQ PUSH to learner."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Protocol

from core.models.az_rollout_protocol import (
    build_hello_payload,
    build_wire_message,
    encode_rollout_message,
)


def az_dist_stop_flag_path() -> str:
    custom = str(os.getenv("AZ_DIST_STOP_FLAG_PATH", "") or "").strip()
    if custom:
        return custom
    root = os.getenv("MODELS_DIR", os.path.join(os.getcwd(), "artifacts", "models"))
    return os.path.join(root, "actor_sync", "az_dist_stop.flag")


def az_dist_stop_requested(flag_path: str | None = None) -> bool:
    path = str(flag_path or az_dist_stop_flag_path())
    return bool(path) and os.path.isfile(path)


def az_dist_context_path() -> str:
    custom = str(os.getenv("AZ_DIST_CONTEXT_PATH", "") or "").strip()
    if custom:
        return custom
    return os.path.join(os.path.dirname(az_dist_stop_flag_path()), "az_dist_train_context.json")


def write_az_dist_train_context(payload: dict[str, Any]) -> str:
    path = az_dist_context_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    body = dict(payload or {})
    body.setdefault("written_at", time.strftime("%Y-%m-%dT%H:%M:%S"))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(body, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def read_az_dist_train_context() -> dict[str, Any]:
    path = az_dist_context_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


class RolloutSink(Protocol):
    def put(self, kind: str, payload: Any) -> None: ...

    def close(self) -> None: ...


def make_rollout_sink(
    *,
    mode: str,
    data_q=None,
    source: str = "local",
    remote_host: str = "",
    remote_port: int = 5557,
    auth_token: str = "",
    worker_id: int = 0,
    env_contract_hash: str = "",
    zmq_hwm: int = 256,
) -> RolloutSink:
    m = str(mode or "local").strip().lower()
    if m == "remote":
        return RemoteRolloutSink(
            host=str(remote_host or "127.0.0.1"),
            port=int(remote_port),
            auth_token=str(auth_token or ""),
            source=str(source or "remote"),
            worker_id=int(worker_id),
            env_contract_hash=str(env_contract_hash or ""),
            zmq_hwm=int(zmq_hwm),
        )
    if data_q is None:
        raise ValueError("LocalRolloutSink requires data_q")
    return LocalRolloutSink(data_q, source=str(source or "local"))


class LocalRolloutSink:
    def __init__(self, data_q, *, source: str = "local") -> None:
        self._q = data_q
        self._source = str(source or "local")

    def put(self, kind: str, payload: Any) -> None:
        if kind in ("rollout", "ep") and isinstance(payload, dict):
            out = dict(payload)
            out.setdefault("source", self._source)
            self._q.put((kind, out))
            return
        self._q.put((kind, payload))

    def close(self) -> None:
        return None


class RemoteRolloutSink:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        auth_token: str = "",
        source: str = "remote",
        worker_id: int = 0,
        env_contract_hash: str = "",
        zmq_hwm: int = 256,
    ) -> None:
        import zmq

        self._auth = str(auth_token or "")
        self._source = str(source or "remote")
        self._worker_id = int(worker_id)
        self._ctx = zmq.Context.instance()
        self._sock = self._ctx.socket(zmq.PUSH)
        self._sock.setsockopt(zmq.SNDHWM, max(1, int(zmq_hwm)))
        self._sock.setsockopt(zmq.LINGER, 2000)
        endpoint = f"tcp://{host}:{int(port)}"
        self._sock.connect(endpoint)
        hello = build_hello_payload(
            worker_id=self._worker_id,
            env_contract_hash=env_contract_hash,
            source=self._source,
        )
        self._send("hello", hello)

    def _send(self, kind: str, payload: dict[str, Any]) -> None:
        import zmq

        wire = build_wire_message(kind=kind, payload=payload, auth_token=self._auth)
        data = encode_rollout_message(wire)
        try:
            self._sock.send(data, flags=0)
        except zmq.Again:
            print(
                f"[AZ][DIST][SINK] queue_full worker={self._worker_id} kind={kind} "
                "(ZMQ SNDHWM). Где: RemoteRolloutSink. Что делать: увеличьте HWM или снизьте нагрузку PC2.",
                flush=True,
            )
        except zmq.ZMQError as exc:
            print(
                f"[AZ][DIST][SINK] send failed worker={self._worker_id} kind={kind}: {exc}",
                flush=True,
            )

    def put(self, kind: str, payload: Any) -> None:
        if kind == "done":
            return
        if not isinstance(payload, dict):
            if kind == "error":
                self._send("error", {"message": str(payload)})
            return
        out = dict(payload)
        out.setdefault("source", self._source)
        if kind == "rollout":
            out.setdefault("env_contract_hash", out.get("env_contract_hash", ""))
        self._send(str(kind), out)

    def close(self) -> None:
        try:
            self._sock.close(linger=0)
        except Exception:
            pass
