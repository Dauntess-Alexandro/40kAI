# tests/models/test_dqn_dist_contract_guard.py
"""DQN dist: receiver кладёт 'batch' в очередь и дропает чужой env_contract_hash."""
import queue

from core.models.az_rollout_protocol import (
    build_wire_message,
    encode_rollout_message,
)
from core.models.az_rollout_receiver import RolloutReceiver


def _batch_wire(hash_val: str):
    payload = {"worker_id": 1, "steps": [], "priority": None, "env_contract_hash": hash_val}
    wire = build_wire_message(kind="batch", payload=payload, auth_token="")
    return encode_rollout_message(wire)


def test_batch_enqueued_when_hash_matches():
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, expected_contract_hash="H1")
    rcv._handle_message(_batch_wire("H1"))
    kind, payload = q.get_nowait()
    assert kind == "batch"
    assert payload["source"] == "remote"


def test_batch_dropped_when_hash_mismatch():
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, expected_contract_hash="H1")
    rcv._handle_message(_batch_wire("H2"))
    assert q.empty()
