"""Unit tests: AZ distributed rollout protocol."""

from __future__ import annotations

import numpy as np
import pytest

from core.models.az_rollout_protocol import (
    AZ_DIST_PROTOCOL_VERSION,
    build_hello_payload,
    build_wire_message,
    decode_rollout_message,
    encode_rollout_message,
    validate_wire_message,
)


def _roundtrip_wire(kind: str, payload: dict) -> tuple[str, dict]:
    wire = build_wire_message(kind=kind, payload=payload, auth_token="secret")
    decoded = decode_rollout_message(encode_rollout_message(wire))
    return validate_wire_message(decoded, auth_token="secret", expected_contract_hash="abc123")


class TestRolloutProtocol:
    def test_rollout_roundtrip(self):
        transitions = [
            {
                "state": np.random.randn(64).astype(np.float32),
                "policy_targets": [np.ones(10, dtype=np.float32), np.ones(5, dtype=np.float32)],
                "value_target": 0.5,
                "policy_version": 3,
            }
        ]
        payload = {
            "actor_idx": 101,
            "policy_version": 3,
            "source": "remote",
            "env_contract_hash": "abc123",
            "transitions": transitions,
        }
        kind, rt = _roundtrip_wire("rollout", payload)
        assert kind == "rollout"
        assert rt["actor_idx"] == 101
        assert rt["source"] == "remote"
        assert len(rt["transitions"]) == 1
        np.testing.assert_allclose(rt["transitions"][0]["state"], transitions[0]["state"], rtol=1e-6)

    def test_hello_contract_mismatch(self):
        wire = build_wire_message(
            kind="hello",
            payload=build_hello_payload(worker_id=5, env_contract_hash="wrong"),
        )
        decoded = decode_rollout_message(encode_rollout_message(wire))
        with pytest.raises(ValueError, match="env_contract_hash"):
            validate_wire_message(decoded, expected_contract_hash="abc123")

    def test_protocol_version_mismatch(self):
        wire = build_wire_message(kind="ep", payload={"actor_idx": 1})
        wire["protocol_version"] = 99
        decoded = decode_rollout_message(encode_rollout_message(wire))
        with pytest.raises(ValueError, match="protocol_version"):
            validate_wire_message(decoded)
