"""Tests for AZInferenceEngine: batched evaluate + server-side cache (CPU)."""

from __future__ import annotations

import os
import tempfile

import numpy as np
import torch
import pytest

from core.models.alphazero_model import make_alphazero_net
from core.models.az_inference_server import AZInferenceEngine

N_OBS = 32
ACTION_SIZES = [6, 4]
DEVICE = torch.device("cpu")


@pytest.fixture
def engine():
    net = make_alphazero_net(N_OBS, ACTION_SIZES, hidden_size=64, num_layers=1).to(DEVICE)
    net.eval()
    # sync_path указывает на несуществующий файл → polling просто пропускает
    sync_path = os.path.join(tempfile.gettempdir(), "az_test_nonexistent_sync.pth")
    eng = AZInferenceEngine(net=net, device=DEVICE, sync_path=sync_path, sync_check_interval=10.0)
    yield eng
    eng.stop()


def _masks(b: int) -> list[np.ndarray]:
    return [np.ones((b, a), dtype=bool) for a in ACTION_SIZES]


class TestEvaluateBatch:
    def test_shapes_with_priors(self, engine):
        b = 5
        obs = np.random.randn(b, N_OBS).astype(np.float32)
        priors, values, version = engine.evaluate_batch(obs, _masks(b), want_priors=True)
        assert len(priors) == len(ACTION_SIZES)
        for h, a in enumerate(ACTION_SIZES):
            assert priors[h].shape == (b, a)
        assert values.shape == (b,)
        assert isinstance(version, int)

    def test_no_priors(self, engine):
        b = 3
        obs = np.random.randn(b, N_OBS).astype(np.float32)
        priors, values, _ = engine.evaluate_batch(obs, _masks(b), want_priors=False)
        assert priors == []
        assert values.shape == (b,)

    def test_values_match_net_infer(self, engine):
        b = 4
        obs = np.random.randn(b, N_OBS).astype(np.float32)
        masks = _masks(b)
        priors, values, _ = engine.evaluate_batch(obs, masks, want_priors=True)

        obs_t = torch.tensor(obs, dtype=torch.float32, device=DEVICE)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=DEVICE) for m in masks]
        with torch.no_grad():
            ref_priors, ref_values = engine.net.infer(obs_t, masks_by_head=masks_t)
        np.testing.assert_allclose(values, ref_values.cpu().numpy(), atol=1e-5)
        for h in range(len(ACTION_SIZES)):
            np.testing.assert_allclose(priors[h], ref_priors[h].cpu().numpy(), atol=1e-5)


class TestServerSideCache:
    def test_cache_hit_on_repeated_obs(self, engine):
        obs_row = np.random.randn(N_OBS).astype(np.float32)
        obs = np.stack([obs_row, obs_row, obs_row])  # 3 одинаковые строки
        masks = _masks(3)
        engine.evaluate_batch(obs, masks, want_priors=True)  # прогрев кэша
        hits_before = engine._cache.hits
        # Второй вызов: все 3 строки бьют в один cache-entry → точное равенство
        _, values, _ = engine.evaluate_batch(obs, masks, want_priors=True)
        assert values[0] == values[1] == values[2]
        assert engine._cache.hits >= hits_before + 3

    def test_cache_persists_across_calls(self, engine):
        obs = np.random.randn(2, N_OBS).astype(np.float32)
        masks = _masks(2)
        engine.evaluate_batch(obs, masks, want_priors=True)
        hits_before = engine._cache.hits
        # Повторный вызов с тем же obs → всё из кэша
        engine.evaluate_batch(obs, masks, want_priors=True)
        assert engine._cache.hits >= hits_before + 2

    def test_cached_values_equal_fresh(self, engine):
        obs = np.random.randn(4, N_OBS).astype(np.float32)
        masks = _masks(4)
        _, v1, _ = engine.evaluate_batch(obs, masks, want_priors=True)
        _, v2, _ = engine.evaluate_batch(obs, masks, want_priors=False)
        np.testing.assert_array_equal(v1, v2)

    def test_different_masks_different_cache_entry(self, engine):
        obs_row = np.random.randn(N_OBS).astype(np.float32)
        obs = np.stack([obs_row, obs_row])
        masks_a = [np.ones((2, a), dtype=bool) for a in ACTION_SIZES]
        masks_b = [np.ones((2, a), dtype=bool) for a in ACTION_SIZES]
        masks_b[0][:, -1] = False  # другая маска на первой голове

        engine.evaluate_batch(obs[:1], [m[:1] for m in masks_a], want_priors=True)
        misses_before = engine._cache.misses
        # Тот же obs, но другая маска → промах (новый ключ)
        engine.evaluate_batch(obs[:1], [m[:1] for m in masks_b], want_priors=True)
        assert engine._cache.misses > misses_before
