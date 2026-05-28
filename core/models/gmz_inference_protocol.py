"""Msgpack + numpy serialization for GMZ remote inference (protocol v1)."""

from __future__ import annotations

from typing import Any

import msgpack
import numpy as np

PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 1_048_576


def _encode_array(arr: np.ndarray) -> dict[str, Any]:
    a = np.asarray(arr)
    return {
        "_dtype": str(a.dtype),
        "_shape": list(a.shape),
        "_data": a.tobytes(),
    }


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
        raise ValueError(f"payload too large: {len(raw)} bytes")
    return raw


def decode_message(data: bytes) -> dict[str, Any]:
    if len(data) > MAX_MESSAGE_BYTES:
        raise ValueError(f"payload too large: {len(data)} bytes")
    unpacked = msgpack.unpackb(data, raw=False)
    if not isinstance(unpacked, dict):
        raise TypeError(f"expected dict message, got {type(unpacked)}")
    out = _decode_value(unpacked)
    if not isinstance(out, dict):
        raise TypeError("decoded message is not a dict")
    return out


def build_infer_request(
    *,
    env_id: int,
    obs: np.ndarray,
    legal_masks_by_head: list[np.ndarray],
    step_in_episode: int,
    episode_id: int,
    is_new_episode: bool,
    auth_token: str = "",
    client_timestamp_ms: int | None = None,
) -> dict[str, Any]:
    import time

    return {
        "kind": "infer",
        "protocol_version": PROTOCOL_VERSION,
        "env_id": int(env_id),
        "step_in_episode": int(step_in_episode),
        "episode_id": int(episode_id),
        "obs": np.asarray(obs, dtype=np.float32),
        "legal_masks_by_head": [np.asarray(m) for m in legal_masks_by_head],
        "is_new_episode": bool(is_new_episode),
        "auth_token": str(auth_token or ""),
        "client_timestamp_ms": int(
            client_timestamp_ms if client_timestamp_ms is not None else time.time() * 1000.0
        ),
    }


def build_health_check_request(*, auth_token: str = "") -> dict[str, Any]:
    return {
        "kind": "health_check",
        "protocol_version": PROTOCOL_VERSION,
        "auth_token": str(auth_token or ""),
    }
