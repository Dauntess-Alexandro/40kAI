"""Msgpack + numpy wire format for AZ distributed self-play rollouts (protocol v1)."""

from __future__ import annotations

from typing import Any

import msgpack
import numpy as np

from core.models.az_inference_protocol import _decode_value, _encode_value

AZ_DIST_PROTOCOL_VERSION = 1
AZ_DIST_MAX_MESSAGE_BYTES = 16 * 1024 * 1024  # rollouts with batch_send transitions can be large


def encode_rollout_message(msg: dict[str, Any]) -> bytes:
    raw = msgpack.packb(_encode_value(msg), use_bin_type=True)
    if len(raw) > AZ_DIST_MAX_MESSAGE_BYTES:
        raise ValueError(
            f"[AZ][DIST] payload too large: {len(raw)} bytes (max {AZ_DIST_MAX_MESSAGE_BYTES}). "
            "Где: az_rollout_protocol.encode_rollout_message. "
            "Что делать: уменьшите actor_batch_send или число transitions в батче."
        )
    return raw


def decode_rollout_message(data: bytes) -> dict[str, Any]:
    if len(data) > AZ_DIST_MAX_MESSAGE_BYTES:
        raise ValueError(f"[AZ][DIST] payload too large: {len(data)} bytes")
    unpacked = msgpack.unpackb(data, raw=False)
    if not isinstance(unpacked, dict):
        raise TypeError(f"[AZ][DIST] expected dict wire message, got {type(unpacked)}")
    return _decode_value(unpacked)  # type: ignore[return-value]


def build_wire_message(
    *,
    kind: str,
    payload: dict[str, Any],
    auth_token: str = "",
) -> dict[str, Any]:
    return {
        "protocol_version": int(AZ_DIST_PROTOCOL_VERSION),
        "auth_token": str(auth_token or ""),
        "kind": str(kind),
        "payload": dict(payload),
    }


def parse_wire_message(msg: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    kind = str(msg.get("kind", "") or "")
    payload = msg.get("payload")
    if not kind:
        raise ValueError("[AZ][DIST] wire message missing kind")
    if not isinstance(payload, dict):
        raise TypeError(f"[AZ][DIST] payload must be dict, got {type(payload)}")
    return kind, payload


def validate_wire_message(
    msg: dict[str, Any],
    *,
    auth_token: str = "",
    expected_contract_hash: str = "",
) -> tuple[str, dict[str, Any]]:
    ver = int(msg.get("protocol_version", 0) or 0)
    if ver != AZ_DIST_PROTOCOL_VERSION:
        raise ValueError(
            f"[AZ][DIST] protocol_version mismatch: got {ver}, expected {AZ_DIST_PROTOCOL_VERSION}"
        )
    expected_auth = str(auth_token or "")
    got_auth = str(msg.get("auth_token", "") or "")
    if expected_auth and got_auth != expected_auth:
        raise ValueError("[AZ][DIST] auth_token mismatch")
    kind, payload = parse_wire_message(msg)
    if expected_contract_hash and kind in ("hello", "rollout"):
        got_hash = str(payload.get("env_contract_hash", "") or "")
        if got_hash and got_hash != str(expected_contract_hash):
            raise ValueError(
                f"[AZ][DIST] env_contract_hash mismatch: remote={got_hash} local={expected_contract_hash}"
            )
    return kind, payload


def build_hello_payload(
    *,
    worker_id: int,
    env_contract_hash: str,
    source: str = "remote",
) -> dict[str, Any]:
    return {
        "worker_id": int(worker_id),
        "env_contract_hash": str(env_contract_hash or ""),
        "protocol_version": int(AZ_DIST_PROTOCOL_VERSION),
        "source": str(source),
    }
