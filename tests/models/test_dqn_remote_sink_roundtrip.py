# tests/models/test_dqn_remote_sink_roundtrip.py
"""DQN dist: 'batch' проходит encode→decode и сохраняет форму 6-кортежей."""
import numpy as np

from core.models.az_rollout_protocol import (
    build_wire_message,
    decode_rollout_message,
    encode_rollout_message,
    validate_wire_message,
)


def _make_batch():
    s = np.arange(4, dtype=np.float32)
    ns = np.arange(4, dtype=np.float32) + 1.0
    # (s_np, a_list, r_sum, ns_np, done_flag, n_count)
    return [
        (s, [1, 0, 2], 0.5, ns, False, 3),
        (s, [0, 0, 0], -1.0, None, True, 1),
    ]


def test_batch_wire_roundtrip_preserves_tuples():
    batch = _make_batch()
    # Sink конвертирует кортежи в списки перед отправкой (tuple не сериализуются msgpack).
    steps_as_lists = [list(t) for t in batch]
    payload = {"worker_id": 7, "steps": steps_as_lists, "priority": None}
    wire = build_wire_message(kind="batch", payload=payload, auth_token="tok")
    raw = encode_rollout_message(wire)
    decoded = decode_rollout_message(raw)
    kind, got = validate_wire_message(decoded, auth_token="tok")
    assert kind == "batch"
    steps = got["steps"]
    assert len(steps) == 2
    s_np, a_list, r_sum, ns_np, done_flag, n_count = steps[0]
    assert list(np.asarray(s_np, dtype=np.float32)) == [0.0, 1.0, 2.0, 3.0]
    assert list(a_list) == [1, 0, 2]
    assert abs(float(r_sum) - 0.5) < 1e-6
    assert ns_np is not None
    assert int(n_count) == 3
    assert steps[1][3] is None
    assert bool(steps[1][4]) is True
