"""Regression: _masked_normalize must always yield a valid prob distribution.

Иначе np.random.choice в MCTS роняет весь эпизод обучения
('probabilities are not non-negative' при NaN/neg, 'do not sum to 1' при пустой маске).
"""

from __future__ import annotations

import numpy as np
import torch

from core.models.alphazero_mcts import (
    AlphaZeroFactorizedMCTS,
    MCTSConfig,
    _masked_normalize,
)


def _assert_valid(p: np.ndarray, legal: np.ndarray) -> None:
    assert np.all(np.isfinite(p)), f"non-finite: {p}"
    assert np.all(p >= 0.0), f"negative: {p}"
    assert abs(float(p.sum()) - 1.0) < 1e-5, f"sum != 1: {p.sum()}"
    # масса только на легальных (если легальные есть)
    if bool(legal.any()):
        assert float(p[~legal].sum()) < 1e-6, f"mass on illegal: {p}"


class TestMaskedNormalizeRobust:
    def test_nan_priors(self):
        legal = np.array([True, True, False, True])
        p = _masked_normalize(np.array([np.nan, 0.2, 0.3, 0.5], dtype=np.float32), legal)
        _assert_valid(p, legal)

    def test_inf_priors(self):
        legal = np.array([True, True, True, True])
        p = _masked_normalize(np.array([np.inf, 1.0, 2.0, 3.0], dtype=np.float32), legal)
        _assert_valid(p, legal)

    def test_negative_priors(self):
        legal = np.array([True, True, True, True])
        p = _masked_normalize(np.array([-0.5, 0.1, 0.2, 0.2], dtype=np.float32), legal)
        _assert_valid(p, legal)

    def test_all_zero_priors(self):
        legal = np.array([True, False, True, True])
        p = _masked_normalize(np.zeros(4, dtype=np.float32), legal)
        _assert_valid(p, legal)

    def test_no_legal_actions(self):
        legal = np.array([False, False, False, False])
        p = _masked_normalize(np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32), legal)
        # нет легальных → uniform по всем, всё ещё валидно
        assert np.all(np.isfinite(p)) and abs(float(p.sum()) - 1.0) < 1e-5


class TestTreeSurvivesNanPriors:
    """Полный tree-прогон с evaluator, возвращающим NaN — не должен падать."""

    class _NanEvaluator:
        def evaluate_one(self, obs, masks):
            priors = [np.full(int(np.asarray(m).shape[-1]), np.nan, dtype=np.float32) for m in masks]
            return priors, float("nan")

        def evaluate_batch(self, leaves):
            return [float("nan") for _ in leaves]

    def test_tree_run_no_crash(self):
        from core.models.action_contract import ordered_action_keys
        import tests.engine.test_alphazero_mcts_tree_basic as T

        heads = [5, 2, 4, 4, 5, 2, 24]
        len_model = 1
        n_obs = 64
        mcts = AlphaZeroFactorizedMCTS(
            None,
            config=MCTSConfig(mode="tree", simulations=12, max_depth=2, parallel_simulations=4, batch_eval_size=8),
            device=torch.device("cpu"),
            evaluator=self._NanEvaluator(),
        )
        env = T._FakeTreeEnv(n_obs=n_obs, n_actions=heads, len_model=len_model, terminal_on_step=False)
        obs = np.random.randn(n_obs).astype(np.float32)
        ld = env.get_legal_action_masks_by_head(side="model")
        masks = [ld[k] for k in ordered_action_keys(len_model)]
        pi, actions, _v = mcts.run(
            obs=obs, legal_masks_by_head=masks, temperature=1.0,
            env=env, len_model=len_model, move_count=0,
        )
        assert len(actions) == len(heads)
        # все действия легальны
        for h, a in enumerate(actions):
            assert bool(masks[h][a]), f"head {h}: action {a} illegal"
