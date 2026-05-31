"""Parity tests: LocalNetEvaluator vs net.infer напрямую + evaluator=None invariant."""

from __future__ import annotations

import numpy as np
import torch
import pytest

from core.models.alphazero_model import make_alphazero_net
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.az_inference_client import LocalNetEvaluator


N_OBS = 32
ACTION_SIZES = [6, 4]
DEVICE = torch.device("cpu")


@pytest.fixture(scope="module")
def net():
    n = make_alphazero_net(N_OBS, ACTION_SIZES, hidden_size=64, num_layers=1).to(DEVICE)
    n.eval()
    return n


@pytest.fixture
def obs():
    return np.random.randn(N_OBS).astype(np.float32)


@pytest.fixture
def masks():
    return [np.ones(a, dtype=bool) for a in ACTION_SIZES]


# ---------------------------------------------------------------------------
# LocalNetEvaluator.evaluate_one == net.infer (B=1)
# ---------------------------------------------------------------------------

class TestLocalNetEvaluatorParity:
    def test_evaluate_one_priors_match(self, net, obs, masks):
        ev = LocalNetEvaluator(net, DEVICE, eval_cache_size=100)
        priors_ev, value_ev = ev.evaluate_one(obs, masks)

        obs_t = torch.tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=DEVICE).unsqueeze(0) for m in masks]
        with torch.no_grad():
            priors_ref, value_ref = net.infer(obs_t, masks_by_head=masks_t)

        for h in range(len(ACTION_SIZES)):
            ref_np = priors_ref[h].squeeze(0).cpu().numpy()
            np.testing.assert_allclose(priors_ev[h], ref_np, atol=1e-5, err_msg=f"head {h}")
        assert abs(value_ev - float(value_ref.item())) < 1e-5

    def test_evaluate_one_cached_second_call(self, net, obs, masks):
        ev = LocalNetEvaluator(net, DEVICE, eval_cache_size=100)
        p1, v1 = ev.evaluate_one(obs, masks)
        p2, v2 = ev.evaluate_one(obs, masks)
        for h in range(len(ACTION_SIZES)):
            np.testing.assert_array_equal(p1[h], p2[h])
        assert v1 == v2
        assert ev._eval_cache.hits >= 1

    def test_evaluate_batch_values_match_one_by_one(self, net, obs, masks):
        ev = LocalNetEvaluator(net, DEVICE, eval_cache_size=100)
        B = 4
        leaves = [
            {"obs": np.random.randn(N_OBS).astype(np.float32), "legal_masks": masks}
            for _ in range(B)
        ]
        batch_vals = ev.evaluate_batch(leaves)

        for i, leaf in enumerate(leaves):
            _, v_ref = ev.evaluate_one(leaf["obs"], leaf["legal_masks"])
            assert abs(batch_vals[i] - v_ref) < 1e-5, f"leaf {i}"

    def test_evaluate_batch_empty(self, net):
        ev = LocalNetEvaluator(net, DEVICE)
        assert ev.evaluate_batch([]) == []


# ---------------------------------------------------------------------------
# evaluator=None — zero-diff: MCTS использует внутренний net напрямую
# ---------------------------------------------------------------------------

class TestMCTSEvaluatorNoneInvariant:
    def _make_fake_env(self):
        from tests.engine.test_alphazero_mcts_tree_basic import _FakeTreeEnv
        from core.models.action_contract import ordered_action_keys
        keys = ordered_action_keys(1)
        return _FakeTreeEnv(n_obs=N_OBS, n_actions=ACTION_SIZES, len_model=1)

    def test_proxy_mode_no_evaluator(self, net, obs, masks):
        mcts = AlphaZeroFactorizedMCTS(net, config=MCTSConfig(mode="proxy"), device=DEVICE)
        assert mcts._evaluator is None
        pi, actions, value = mcts.run(obs=obs, legal_masks_by_head=masks)
        assert len(pi) == len(ACTION_SIZES)
        assert len(actions) == len(ACTION_SIZES)

    def test_proxy_mode_with_local_evaluator_same_shapes(self, net, obs, masks):
        ev = LocalNetEvaluator(net, DEVICE)
        mcts_no_ev = AlphaZeroFactorizedMCTS(net, config=MCTSConfig(mode="proxy"), device=DEVICE)
        mcts_ev = AlphaZeroFactorizedMCTS(net, config=MCTSConfig(mode="proxy"), device=DEVICE, evaluator=ev)

        np.random.seed(42)
        torch.manual_seed(42)
        pi_no, act_no, v_no = mcts_no_ev.run(obs=obs, legal_masks_by_head=masks)

        np.random.seed(42)
        torch.manual_seed(42)
        pi_ev, act_ev, v_ev = mcts_ev.run(obs=obs, legal_masks_by_head=masks)

        # Shapes и dtype должны совпадать
        assert len(pi_no) == len(pi_ev)
        for h in range(len(ACTION_SIZES)):
            assert pi_no[h].shape == pi_ev[h].shape
            assert pi_no[h].dtype == pi_ev[h].dtype
