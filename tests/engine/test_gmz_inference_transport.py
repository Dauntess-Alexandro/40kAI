"""Unit tests for GMZ inference transport and msgpack protocol."""

from __future__ import annotations

import threading

import numpy as np
import pytest

from core.models.gmz_inference_protocol import (
    PROTOCOL_VERSION,
    build_health_check_request,
    build_infer_request,
    decode_message,
    encode_message,
)
from core.models.gmz_inference_transport import LocalInferenceTransport


def test_msgpack_roundtrip_infer_request():
    req = build_infer_request(
        env_id=2,
        obs=np.zeros(8, dtype=np.float32),
        legal_masks_by_head=[np.ones(5, dtype=bool), np.zeros(3, dtype=bool)],
        step_in_episode=1,
        episode_id=9,
        is_new_episode=True,
    )
    wire = decode_message(encode_message(req))
    assert int(wire["env_id"]) == 2
    assert int(wire["protocol_version"]) == PROTOCOL_VERSION
    assert np.asarray(wire["obs"]).shape == (8,)
    assert len(wire["legal_masks_by_head"]) == 2


def test_health_check_request_roundtrip():
    msg = build_health_check_request(auth_token="secret")
    out = decode_message(encode_message(msg))
    assert out["kind"] == "health_check"
    assert out["auth_token"] == "secret"


def test_local_transport_roundtrip():
    import multiprocessing as mp

    ctx = mp.get_context("spawn")
    request_q = ctx.Queue()
    reply_q = ctx.Queue()
    transport = LocalInferenceTransport(request_q, reply_q)

    def _server():
        req = request_q.get(timeout=2.0)
        reply_q.put(
            {
                "env_id": int(req["env_id"]),
                "selected_actions": [0, 1],
                "policy_targets": [np.ones(4, dtype=np.float32) / 4.0],
                "behavior_logits": [np.zeros(4, dtype=np.float32)],
                "value_est": 0.5,
                "policy_version": 3,
            }
        )

    t = threading.Thread(target=_server, daemon=True)
    t.start()
    transport.send(
        {
            "env_id": 0,
            "obs": np.zeros(4, dtype=np.float32),
            "legal_masks_by_head": [np.ones(4, dtype=bool)],
            "is_new_episode": True,
        }
    )
    resp = transport.recv(timeout=1.0)
    assert resp["policy_version"] == 3


def test_make_transport_factory():
    from core.models.gmz_inference_transport import make_transport

    import multiprocessing as mp

    ctx = mp.get_context("spawn")
    rq, rp = ctx.Queue(), ctx.Queue()
    local = make_transport("local", request_q=rq, reply_q=rp)
    assert isinstance(local, LocalInferenceTransport)
    with pytest.raises(ValueError):
        make_transport("local")


@pytest.mark.skipif(
    not __import__("importlib").util.find_spec("zmq"),
    reason="pyzmq not installed",
)
def test_remote_transport_mock_zmq(monkeypatch):
    from core.models.gmz_inference_transport import RemoteInferenceTransport

    sent: list[bytes] = []

    class _FakeSock:
        def setsockopt(self, *args, **kwargs):
            pass

        def connect(self, addr):
            self._addr = addr

        def send(self, data):
            sent.append(data)

        def recv(self):
            return encode_message(
                {
                    "kind": "infer_response",
                    "env_id": 1,
                    "selected_actions": [0],
                    "policy_targets": [np.ones(2, dtype=np.float32)],
                    "behavior_logits": [np.zeros(2, dtype=np.float32)],
                    "value_est": 0.0,
                    "policy_version": 1,
                }
            )

        def close(self, **kwargs):
            pass

    class _FakeCtx:
        def socket(self, _type):
            return _FakeSock()

    class _FakePoll:
        def register(self, *args):
            pass

        def poll(self, _timeout):
            return [(None, 0)]

    monkeypatch.setattr(
        "core.models.gmz_inference_transport.zmq.Context.instance",
        lambda: _FakeCtx(),
    )
    monkeypatch.setattr("core.models.gmz_inference_transport.zmq.Poller", _FakePoll)

    transport = RemoteInferenceTransport(worker_id=1, host="127.0.0.1", port=5555)
    transport.send(build_infer_request(
        env_id=1,
        obs=np.zeros(2, dtype=np.float32),
        legal_masks_by_head=[np.ones(2, dtype=bool)],
        step_in_episode=0,
        episode_id=0,
        is_new_episode=True,
    ))
    assert sent
    resp = transport.recv(timeout=1.0)
    assert resp["policy_version"] == 1
