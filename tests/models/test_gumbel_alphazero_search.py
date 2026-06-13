import numpy as np
import torch

from core.models.gumbel_alphazero_search import (
    GumbelAlphaZeroSearch,
    GumbelAZSearchConfig,
    sequential_halving_keep_schedule,
)


class _StubNet:
    """policy = uniform логиты, value = const. Совместим с net.infer()."""

    def __init__(self, action_sizes, value=0.0):
        self.action_sizes = action_sizes
        self._value = float(value)

    @torch.no_grad()
    def infer(self, obs, masks_by_head=None):
        b = obs.shape[0]
        probs = []
        for i, n in enumerate(self.action_sizes):
            p = torch.full((b, n), 1.0 / n)
            probs.append(p)
        value = torch.full((b,), self._value)
        return probs, value


def test_keep_schedule_halves_to_one():
    sched = sequential_halving_keep_schedule(m=8)
    assert sched[0] == 8
    assert sched[-1] == 1
    # монотонно невозрастающая, делит пополам
    for a, b in zip(sched, sched[1:]):
        assert b <= a


def test_run_returns_az_contract_no_env():
    # depth-1 без env: оценка кандидатов через net-value на корне (terminal None → root value)
    net = _StubNet([5, 3], value=0.2)
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=4, simulate_enemy=False)
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    legal = [np.array([1, 1, 1, 0, 0], dtype=bool), np.array([1, 1, 0], dtype=bool)]
    pi, actions, value = search.run(
        obs=np.zeros(7, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=0.0,
        env=None,
        len_model=None,
    )
    assert len(pi) == 2 and len(actions) == 2
    for head_pi, head_legal in zip(pi, legal):
        assert head_pi.shape == head_legal.shape
        assert np.all(head_pi[~head_legal] == 0.0)
        assert abs(float(head_pi.sum()) - 1.0) < 1e-5
        assert np.all(head_pi >= 0.0)
    assert -1.0 <= value <= 1.0
    # выбранные действия — только легальные
    for a, head_legal in zip(actions, legal):
        assert bool(head_legal[a])


def test_head_without_legal_actions_uniform_fallback():
    net = _StubNet([4], value=0.0)
    cfg = GumbelAZSearchConfig(num_simulations=4, num_considered_actions=4, simulate_enemy=False)
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    legal = [np.array([0, 0, 0, 0], dtype=bool)]
    pi, actions, value = search.run(
        obs=np.zeros(7, dtype=np.float32), legal_masks_by_head=legal, temperature=0.0
    )
    assert abs(float(pi[0].sum()) - 1.0) < 1e-5
    assert not np.any(np.isnan(pi[0]))


def test_nan_priors_fallback_uniform():
    class _NanNet(_StubNet):
        @torch.no_grad()
        def infer(self, obs, masks_by_head=None):
            probs, value = super().infer(obs, masks_by_head)
            probs[0] = probs[0] * float("nan")
            return probs, value

    net = _NanNet([4], value=0.0)
    cfg = GumbelAZSearchConfig(num_simulations=4, num_considered_actions=4, simulate_enemy=False)
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    legal = [np.array([1, 1, 1, 1], dtype=bool)]
    pi, actions, value = search.run(
        obs=np.zeros(7, dtype=np.float32), legal_masks_by_head=legal, temperature=0.0
    )
    assert not np.any(np.isnan(pi[0]))
    assert abs(float(pi[0].sum()) - 1.0) < 1e-5


def test_deterministic_with_seed():
    net = _StubNet([6], value=0.1)
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=4, simulate_enemy=False)
    legal = [np.array([1, 1, 1, 1, 1, 0], dtype=bool)]
    obs = np.zeros(7, dtype=np.float32)

    np.random.seed(123)
    s1 = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    pi1, a1, _ = s1.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)
    np.random.seed(123)
    s2 = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    pi2, a2, _ = s2.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)
    assert a1 == a2
    assert np.allclose(pi1[0], pi2[0])


def test_joint_action_default_off():
    assert GumbelAZSearchConfig().joint_action is False


def _run_capturing_base_action(joint: bool):
    """Прогоняет поиск, перехватывая base_action, который видит каждая голова."""
    net = _StubNet([3, 3, 3], value=0.0)
    legal = [np.ones(3, dtype=bool) for _ in range(3)]
    obs = np.zeros(5, dtype=np.float32)
    cfg = GumbelAZSearchConfig(
        num_simulations=8, num_considered_actions=3, simulate_enemy=False, joint_action=joint
    )
    np.random.seed(7)
    s = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    seen: list[tuple[int, list[int]]] = []
    orig = s._search_head

    def _wrapped(*, head_idx, base_action, **kw):
        seen.append((int(head_idx), list(base_action)))
        return orig(head_idx=head_idx, base_action=base_action, **kw)

    s._search_head = _wrapped
    _pi, actions, _v = s.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)
    return actions, seen


def test_joint_action_off_keeps_greedy_context():
    # per-head: каждая голова видит исходный greedy base_action (argmax uniform = 0)
    _actions, seen = _run_capturing_base_action(joint=False)
    for _head_idx, base in seen:
        assert base == [0, 0, 0]


def test_joint_action_on_propagates_winners_to_later_heads():
    # joint: голова h+1 видит уже ВЫБРАННОЕ действие головы h в base_action
    actions, seen = _run_capturing_base_action(joint=True)
    # seen[k] = (head_idx=k, base_action на момент поиска головы k)
    assert seen[1][1][0] == actions[0]  # голова 1 увидела победителя головы 0
    assert seen[2][1][0] == actions[0]
    assert seen[2][1][1] == actions[1]  # голова 2 увидела победителя головы 1


def test_inference_temperature_deterministic_vs_stochastic():
    net = _StubNet([6], value=0.0)
    legal = [np.ones(6, dtype=bool)]
    obs = np.zeros(7, dtype=np.float32)
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=6, simulate_enemy=False)
    # инференс (move_count=None), T≈0 → детерминированный argmax улучшённой политики
    s = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    a0 = {s.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)[1][0] for _ in range(6)}
    assert len(a0) == 1
    # высокая T → появляется разнообразие выбора
    np.random.seed(0)
    s2 = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    a1 = {s2.run(obs=obs, legal_masks_by_head=legal, temperature=1.0)[1][0] for _ in range(40)}
    assert len(a1) > 1


def test_build_inference_search_config_and_run():
    from core.models.gumbel_alphazero_search import build_gumbel_inference_search

    net = _StubNet([4, 3], value=0.0)
    s = build_gumbel_inference_search(
        net, num_simulations=16, num_considered_actions=4, joint_action=True,
        device=torch.device("cpu"),
    )
    # инференс: без симуляции врага, joint прокинут, depth-1
    assert s.cfg.simulate_enemy is False
    assert s.cfg.joint_action is True
    assert s.cfg.max_depth == 1
    legal = [np.ones(4, dtype=bool), np.ones(3, dtype=bool)]
    pi, actions, value = s.run(
        obs=np.zeros(5, dtype=np.float32), legal_masks_by_head=legal, temperature=0.0
    )
    assert len(actions) == 2
    for p in pi:
        assert abs(float(p.sum()) - 1.0) < 1e-5
    for a, lg in zip(actions, legal):
        assert bool(lg[a])
    assert -1.0 <= float(value) <= 1.0
