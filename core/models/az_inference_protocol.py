"""Msgpack + numpy serialization for AZ remote inference (protocol v1)."""

from __future__ import annotations

import time
from typing import Any

import msgpack
import numpy as np

AZ_PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 4_194_304  # 4 MB — больше чем GMZ, т.к. передаём батч obs


def _encode_array(arr: np.ndarray) -> dict[str, Any]:
    a = np.asarray(arr)
    return {"_dtype": str(a.dtype), "_shape": list(a.shape), "_data": a.tobytes()}


def _decode_array(payload: dict[str, Any]) -> np.ndarray:
    dtype = np.dtype(str(payload.get("_dtype", "float32")))
    shape = tuple(int(x) for x in (payload.get("_shape") or []))
    data = payload.get("_data", b"")
    if not isinstance(data, (bytes, bytearray)):
        data = bytes(data)
    return np.frombuffer(data, dtype=dtype).reshape(shape)


def _encode_value(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return {"_np": _encode_array(value)}
    if isinstance(value, list):
        return [_encode_value(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _encode_value(v) for k, v in value.items()}
    return value


def _decode_value(value: Any) -> Any:
    if isinstance(value, dict):
        if "_np" in value:
            return _decode_array(value["_np"])
        return {k: _decode_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_decode_value(v) for v in value]
    return value


def encode_message(msg: dict[str, Any]) -> bytes:
    raw = msgpack.packb(_encode_value(msg), use_bin_type=True)
    if len(raw) > MAX_MESSAGE_BYTES:
        raise ValueError(f"AZ protocol: payload too large: {len(raw)} bytes (max {MAX_MESSAGE_BYTES})")
    return raw


def decode_message(data: bytes) -> dict[str, Any]:
    if len(data) > MAX_MESSAGE_BYTES:
        raise ValueError(f"AZ protocol: payload too large: {len(data)} bytes")
    unpacked = msgpack.unpackb(data, raw=False)
    if not isinstance(unpacked, dict):
        raise TypeError(f"AZ protocol: expected dict, got {type(unpacked)}")
    return _decode_value(unpacked)  # type: ignore[return-value]


def build_infer_request(
    *,
    worker_id: int,
    request_id: int,
    obs: np.ndarray,
    legal_masks_by_head: list[np.ndarray],
    want_priors: bool = True,
    episode_id: int = 0,
    move_id: int = 0,
    auth_token: str = "",
    client_timestamp_ms: int | None = None,
) -> dict[str, Any]:
    """Построить infer-запрос.

    obs: float32 [B, obs_dim] — батч наблюдений (B=1 для single eval).
    legal_masks_by_head: list длины num_heads, каждый элемент bool [B, head_size].
    want_priors: True → сервер вернёт priors; False → только values (для leaf batch).
    """
    return {
        "kind": "infer",
        "protocol_version": AZ_PROTOCOL_VERSION,
        "worker_id": int(worker_id),
        "request_id": int(request_id),
        "obs": np.asarray(obs, dtype=np.float32),
        "legal_masks_by_head": [np.asarray(m) for m in legal_masks_by_head],
        "want_priors": bool(want_priors),
        "episode_id": int(episode_id),
        "move_id": int(move_id),
        "auth_token": str(auth_token or ""),
        "client_timestamp_ms": int(
            client_timestamp_ms if client_timestamp_ms is not None else time.time() * 1000.0
        ),
    }


def build_health_check_request(*, auth_token: str = "") -> dict[str, Any]:
    return {
        "kind": "health_check",
        "protocol_version": AZ_PROTOCOL_VERSION,
        "auth_token": str(auth_token or ""),
    }


def build_infer_response(
    *,
    worker_id: int,
    request_id: int,
    priors: list[np.ndarray],
    value: np.ndarray,
    policy_version: int,
) -> dict[str, Any]:
    """Построить ответ на infer-запрос.

    priors: list длины num_heads, каждый float32 [B, head_size]; пусто если want_priors=False.
    value: float32 [B].
    """
    return {
        "kind": "infer_response",
        "protocol_version": AZ_PROTOCOL_VERSION,
        "worker_id": int(worker_id),
        "request_id": int(request_id),
        "priors": [np.asarray(p, dtype=np.float32) for p in priors],
        "value": np.asarray(value, dtype=np.float32),
        "policy_version": int(policy_version),
    }


def build_health_response(
    *,
    policy_version: int,
    gpu_name: str,
    queue_depth: int,
    uptime_s: int,
    avg_batch: float | None = None,
    gpu_util: float | None = None,
    gpu_mem_used_mb: float | None = None,
    gpu_mem_total_mb: float | None = None,
    gpu_temp_c: float | None = None,
    cpu_name: str | None = None,
    cpu_pct_system: float | None = None,
    ram_pct_system: float | None = None,
    ram_gb_system: float | None = None,
) -> dict[str, Any]:
    # cpu_*/ram_* — опциональны (P1: телеметрия CPU/RAM ПК2). Старый ПК2 их не шлёт → None,
    # старый ПК1 (GUI) их игнорирует. Обратная совместимость по протоколу сохраняется.
    return {
        "kind": "health_check",
        "status": "ok",
        "protocol_version": AZ_PROTOCOL_VERSION,
        "policy_version": int(policy_version),
        "gpu_name": str(gpu_name),
        "queue_depth": int(queue_depth),
        "uptime_s": int(uptime_s),
        "avg_batch": None if avg_batch is None else float(avg_batch),
        "gpu_util": gpu_util,
        "gpu_mem_used_mb": gpu_mem_used_mb,
        "gpu_mem_total_mb": gpu_mem_total_mb,
        "gpu_temp_c": gpu_temp_c,
        "cpu_name": None if cpu_name is None else str(cpu_name),
        "cpu_pct_system": cpu_pct_system,
        "ram_pct_system": ram_pct_system,
        "ram_gb_system": ram_gb_system,
    }
