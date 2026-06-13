"""Интеграция GumbelAlphaZeroSearch с env-роллаутом (depth-1).

Переиспользуем _FakeTreeEnv из test_alphazero_mcts_tree_basic (тот же контракт env,
что у AZ MCTS), и гоняем через него реальный путь поиска: snapshot → step →
enemyTurn → терминальная развязка/value-сеть → restore. Контракт run() совпадает с
AlphaZeroFactorizedMCTS, поэтому проверяем валидность policy targets, value и
восстановление env.
"""

import numpy as np
import torch

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.gumbel_alphazero_search import GumbelAlphaZeroSearch, GumbelAZSearchConfig
from tests.engine.test_alphazero_mcts_tree_basic import _FakeTreeEnv


def _run(net, env, cfg, len_model, *, temperature=1.0, move_count=None):
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    pi, act, value = search.run(
        obs=np.zeros(env.n_obs, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=temperature,
        env=env,
        len_model=len_model,
        move_count=move_count,
    )
    return legal, pi, act, value


def test_gumbel_az_env_rollout_valid_targets_and_restore():
    len_model = 1
    n_obs = 16
    n_actions = [5, 2, 6, 6, 5, 3, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    env = _FakeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model)
    cfg = GumbelAZSearchConfig(num_simulations=16, num_considered_actions=4, simulate_enemy=True)

    legal, pi, act, value = _run(net, env, cfg, len_model)

    assert len(pi) == len(n_actions) and len(act) == len(n_actions)
    for head_idx, p in enumerate(pi):
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
        assert np.all(p[~legal[head_idx]] <= 1e-12)
        assert bool(legal[head_idx][act[head_idx]])
    assert -1.0 <= float(value) <= 1.0
    # env восстановлен после depth-1 роллаутов (snapshot/restore)
    assert env.game_over is False


def test_gumbel_az_prefers_winning_attack():
    # attack head index = 1; action 1 = терминальный выигрыш в _FakeTreeEnv
    len_model = 1
    n_obs = 12
    n_actions = [5, 2, 4, 4, 5, 2, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    env = _FakeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model)
    cfg = GumbelAZSearchConfig(num_simulations=32, num_considered_actions=2)

    _legal, pi, _act, _value = _run(net, env, cfg, len_model, temperature=0.0)

    # completed-Q должен подтянуть массу к выигрышному действию attack=1
    assert float(pi[1][1]) >= float(pi[1][0])
    assert float(pi[1][1]) > 0.2


def test_gumbel_az_nonterminal_uses_net_value_and_restores():
    len_model = 1
    n_obs = 12
    n_actions = [5, 2, 4, 4, 5, 2, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    env = _FakeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model, terminal_on_step=False)
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=4, simulate_enemy=True, batch_eval_size=4)

    legal, pi, act, value = _run(net, env, cfg, len_model)

    assert len(pi) == len(n_actions) and len(act) == len(n_actions)
    for head_idx, p in enumerate(pi):
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
        assert not np.any(np.isnan(p))
        assert np.all(p[~legal[head_idx]] <= 1e-12)
    assert -1.0 <= float(value) <= 1.0
    assert env.game_over is False
