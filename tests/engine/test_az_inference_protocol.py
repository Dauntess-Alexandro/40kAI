"""Unit tests: AZ inference protocol encode/decode roundtrip."""

from __future__ import annotations

import numpy as np
import pytest

from core.models.az_inference_protocol import (
    AZ_PROTOCOL_VERSION,
    build_health_check_request,
    build_infer_request,
    build_infer_response,
    decode_message,
    encode_message,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _roundtrip(msg: dict) -> dict:
    return decode_message(encode_message(msg))


def _make_masks(batch_size: int, action_sizes: list[int]) -> list[np.ndarray]:
    return [np.ones((batch_size, a), dtype=bool) for a in action_sizes]


# ---------------------------------------------------------------------------
# encode / decode primitives
# ---------------------------------------------------------------------------

class TestEncodeDecode:
    def test_scalar_fields(self):
        msg = {"kind": "infer", "worker_id": 3, "request_id": 42, "flag": True, "val": 1.5}
        rt = _roundtrip(msg)
        assert rt["kind"] == "infer"
        assert rt["worker_id"] == 3
        assert rt["request_id"] == 42
        assert rt["flag"] is True
        assert abs(rt["val"] - 1.5) < 1e-6

    def test_numpy_array_float32(self):
        arr = np.array([[1.0, 2.0, 3.0]], dtype=np.float32)
        rt = _roundtrip({"arr": arr})["arr"]
        assert isinstance(rt, np.ndarray)
        assert rt.dtype == np.float32
        np.testing.assert_array_almost_equal(rt, arr)

    def test_numpy_array_bool(self):
        arr = np.array([[True, False, True]], dtype=bool)
        rt = _roundtrip({"m": arr})["m"]
        assert rt.dtype == bool
        np.testing.assert_array_equal(rt, arr)

    def test_list_of_arrays(self):
        arrays = [np.ones((2, 3), dtype=np.float32), np.zeros((2, 5), dtype=bool)]
        rt = _roundtrip({"a": arrays})["a"]
        assert len(rt) == 2
        np.testing.assert_array_almost_equal(rt[0], arrays[0])
        np.testing.assert_array_equal(rt[1], arrays[1])

    def test_payload_too_large_raises(self):
        big = np.zeros((1025, 1025), dtype=np.float32)  # >4MB
        with pytest.raises(ValueError, match="payload too large"):
            encode_message({"big": big})


# ---------------------------------------------------------------------------
# build_infer_request
# ---------------------------------------------------------------------------

class TestBuildInferRequest:
    @pytest.mark.parametrize("batch_size", [1, 4])
    @pytest.mark.parametrize("action_sizes", [[10], [10, 5, 8]])
    def test_roundtrip_infer(self, batch_size, action_sizes):
        obs_dim = 64
        obs = np.random.randn(batch_size, obs_dim).astype(np.float32)
        masks = _make_masks(batch_size, action_sizes)
        req = build_infer_request(
            worker_id=2,
            request_id=99,
            obs=obs,
            legal_masks_by_head=masks,
            want_priors=True,
            episode_id=7,
            move_id=3,
        )
        rt = _roundtrip(req)

        assert rt["kind"] == "infer"
        assert rt["protocol_version"] == AZ_PROTOCOL_VERSION
        assert rt["worker_id"] == 2
        assert rt["request_id"] == 99
        assert rt["want_priors"] is True
        np.testing.assert_array_almost_equal(rt["obs"], obs)
        assert len(rt["legal_masks_by_head"]) == len(masks)
        for h, m in enumerate(masks):
            np.testing.assert_array_equal(rt["legal_masks_by_head"][h], m)

    def test_want_priors_false(self):
        obs = np.ones((8, 32), dtype=np.float32)
        masks = _make_masks(8, [10])
        req = build_infer_request(
            worker_id=0, request_id=0, obs=obs,
            legal_masks_by_head=masks, want_priors=False,
        )
        rt = _roundtrip(req)
        assert rt["want_priors"] is False

    def test_obs_shape_preserved(self):
        # B=1, obs_dim=128
        obs = np.random.randn(1, 128).astype(np.float32)
        masks = _make_masks(1, [20, 15])
        req = build_infer_request(
            worker_id=0, request_id=0, obs=obs, legal_masks_by_head=masks,
        )
        rt = _roundtrip(req)
        assert rt["obs"].shape == (1, 128)
        assert rt["legal_masks_by_head"][0].shape == (1, 20)
        assert rt["legal_masks_by_head"][1].shape == (1, 15)


# ---------------------------------------------------------------------------
# build_infer_response
# ---------------------------------------------------------------------------

class TestBuildInferResponse:
    def test_roundtrip_with_priors(self):
        B, heads, obs_dim = 4, 3, 64
        action_sizes = [10, 5, 8]
        priors = [np.random.rand(B, a).astype(np.float32) for a in action_sizes]
        values = np.random.rand(B).astype(np.float32)
        resp = build_infer_response(
            worker_id=1, request_id=7,
            priors=priors, value=values, policy_version=42,
        )
        rt = _roundtrip(resp)
        assert rt["kind"] == "infer_response"
        assert rt["worker_id"] == 1
        assert rt["request_id"] == 7
        assert rt["policy_version"] == 42
        assert len(rt["priors"]) == len(priors)
        for h in range(heads):
            np.testing.assert_array_almost_equal(rt["priors"][h], priors[h])
        np.testing.assert_array_almost_equal(rt["value"], values)

    def test_roundtrip_no_priors(self):
        values = np.array([0.1, -0.3], dtype=np.float32)
        resp = build_infer_response(
            worker_id=0, request_id=1, priors=[], value=values, policy_version=0,
        )
        rt = _roundtrip(resp)
        assert rt["priors"] == []
        np.testing.assert_array_almost_equal(rt["value"], values)


# ---------------------------------------------------------------------------
# build_health_check_request
# ---------------------------------------------------------------------------

class TestHealthCheck:
    def test_roundtrip(self):
        req = build_health_check_request(auth_token="secret")
        rt = _roundtrip(req)
        assert rt["kind"] == "health_check"
        assert rt["protocol_version"] == AZ_PROTOCOL_VERSION
        assert rt["auth_token"] == "secret"

    def test_empty_token(self):
        req = build_health_check_request()
        rt = _roundtrip(req)
        assert rt["auth_token"] == ""


# ---------------------------------------------------------------------------
# Factorized heads: разные размеры на голову
# ---------------------------------------------------------------------------

class TestFactorizedHeads:
    def test_different_head_sizes_batch4(self):
        """Проверяет корректность для реалистичных factorized action heads."""
        action_sizes = [12, 7, 3, 20]
        B = 4
        obs = np.random.randn(B, 96).astype(np.float32)
        masks = [np.random.rand(B, a) > 0.3 for a in action_sizes]
        # Убедиться что каждая маска хотя бы 1 True
        for m in masks:
            m[:, 0] = True

        req = build_infer_request(
            worker_id=5, request_id=123, obs=obs,
            legal_masks_by_head=masks, want_priors=True,
        )
        rt = _roundtrip(req)
        for h, (m, a) in enumerate(zip(masks, action_sizes)):
            rt_m = rt["legal_masks_by_head"][h]
            assert rt_m.shape == (B, a), f"head {h}: shape mismatch"
            np.testing.assert_array_equal(rt_m, m)
