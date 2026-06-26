"""Честный eval: side-aware action masks.

Главный инвариант честного P1-vs-P2: обе стороны должны получать маски для
своей собственной стороны, а не всегда для "model". До фикса build_action_masks_by_head
и build_shoot_action_mask хардкодили side="model", из-за чего enemy-оппонент в eval
получал маски model-стороны → выбор действия по чужим legal targets (сегрегация).

Проверка структурная (spy на env.get_legal_action_masks_by_head): фиксируем, что
внутри build_action_masks_by_head / build_shoot_action_mask / EvalAgent.select_action
вызывается env.get_legal_action_masks_by_head(side=<запрошенный side>). Это точно
проверяет инвариант без зависимости от игровой ситуации (fallback-логика env всегда
ставит m[0]=True, что делает count-based сравнение хрупким).
"""
from __future__ import annotations

from core.models.utils import build_action_masks_by_head, build_shoot_action_mask
from tests.engine.phases._helpers import build_env


def test_build_action_masks_by_head_passes_side_to_env():
    """build_action_masks_by_head(side=X) обязан вызвать env.get_legal_action_masks_by_head(side=X)."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_units = len(env.model)

    for requested_side in ("model", "enemy"):
        called_sides: list[str] = []
        original = env.get_legal_action_masks_by_head

        def _spy(side: str = "model", _called=called_sides, _orig=original):
            _called.append(str(side))
            return _orig(side=side)

        env.get_legal_action_masks_by_head = _spy  # type: ignore[assignment]
        try:
            build_action_masks_by_head(env, n_units, side=requested_side)
        finally:
            env.get_legal_action_masks_by_head = original  # type: ignore[assignment]

        assert requested_side in called_sides, (
            f"build_action_masks_by_head(side={requested_side!r}) не передал side в "
            f"env.get_legal_action_masks_by_head. Вызовы: {called_sides}"
        )


def test_build_shoot_action_mask_passes_side_to_env():
    """build_shoot_action_mask(side=X) обязан вызвать env.get_legal_action_masks_by_head(side=X)."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})

    for requested_side in ("model", "enemy"):
        called_sides: list[str] = []
        original = env.get_legal_action_masks_by_head

        def _spy(side: str = "model", _called=called_sides, _orig=original):
            _called.append(str(side))
            return _orig(side=side)

        env.get_legal_action_masks_by_head = _spy  # type: ignore[assignment]
        try:
            build_shoot_action_mask(env, side=requested_side)
        finally:
            env.get_legal_action_masks_by_head = original  # type: ignore[assignment]

        assert requested_side in called_sides, (
            f"build_shoot_action_mask(side={requested_side!r}) не передал side в "
            f"env.get_legal_action_masks_by_head. Вызовы: {called_sides}"
        )


def test_build_action_masks_default_side_is_model():
    """Обратная совместимость: без side — поведение как раньше (side='model')."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_units = len(env.model)

    called_sides: list[str] = []
    original = env.get_legal_action_masks_by_head

    def _spy(side: str = "model", _called=called_sides, _orig=original):
        _called.append(str(side))
        return _orig(side=side)

    env.get_legal_action_masks_by_head = _spy  # type: ignore[assignment]
    try:
        build_action_masks_by_head(env, n_units)  # без side
    finally:
        env.get_legal_action_masks_by_head = original  # type: ignore[assignment]

    assert called_sides == ["model"], (
        f"Без side build_action_masks_by_head должен вызывать с side='model'. Вызовы: {called_sides}"
    )


def test_eval_agent_select_action_uses_side_masks():
    """EvalAgent.select_action(env, side) обязан строить маски для side, а не "model"."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    import core.models.eval_agent as ea_mod

    called_sides: list[str] = []
    original = ea_mod.build_action_masks_by_head

    def _spy(env_arg, len_model, log_fn=None, debug=False, side="model"):
        called_sides.append(str(side))
        return original(env_arg, len_model, log_fn=log_fn, debug=debug, side=side)

    ea_mod.build_action_masks_by_head = _spy
    try:
        from core.models.DQN import make_dqn
        from core.models.eval_agent import EvalAgent, EvalSearchCfg

        obs = env.get_observation_for_side("model")
        masks = original(env, len(env.model), side="model")
        n_actions = [int(m.numel()) for m in masks]
        # make_dqn сам подтягивает kwargs (hidden_size и т.д.) из env/hyperparams.
        net = make_dqn(len(obs), n_actions)
        cfg = EvalSearchCfg(algo="dqn", deterministic=True, epsilon=0.0, search={}, opponent_override_active=False)
        agent = EvalAgent(algo="dqn", net=net, reaction_net=None, search=None, cfg=cfg, len_model=len(env.model))
        agent.select_action(env, "enemy")
    finally:
        ea_mod.build_action_masks_by_head = original

    assert "enemy" in called_sides, (
        f"EvalAgent.select_action не передал side='enemy' в build_action_masks_by_head. "
        f"Вызовы: {called_sides}"
    )


def test_eval_legacy_dqn_helper_uses_requested_side_masks():
    """Legacy eval helper не должен хардкодить side='model' при greedy DQN."""
    import torch
    from eval import select_action_with_epsilon

    class _Policy(torch.nn.Module):
        def forward(self, state):
            return [
                torch.tensor([[10.0, 1.0]], dtype=torch.float32),
                torch.tensor([[0.0]], dtype=torch.float32),
            ]

    class _Env:
        class _ActionSpace:
            def sample(self):
                return {"move": 0, "attack": 0}

        action_space = _ActionSpace()

        def __init__(self):
            self.called_sides: list[str] = []

        def get_legal_action_masks_by_head(self, side="model"):
            self.called_sides.append(str(side))
            return {
                "move": [False, True],
                "attack": [True],
            }

    env = _Env()
    action = select_action_with_epsilon(
        env,
        torch.zeros((1, 3), dtype=torch.float32),
        _Policy(),
        epsilon=0.0,
        len_model=0,
        side="enemy",
    )

    assert env.called_sides == ["enemy"]
    assert action.tolist() == [[1, 0]]


def test_eval_sampled_muzero_helper_uses_requested_side_for_masks(monkeypatch):
    """SMZ eval helper должен передавать side дальше и в epsilon path сэмплить по этим masks."""
    import torch
    import eval as eval_module

    called_sides: list[str] = []
    sampled_masks = []

    def _mock_build_masks(env, len_model, log_fn=None, debug=False, side="model"):
        called_sides.append(str(side))
        return [
            torch.tensor([False, True], dtype=torch.bool),
            torch.tensor([True], dtype=torch.bool),
        ]

    def _mock_sample_action_list_from_space(env, len_model, *, masks_seq=None, legal_by_head=None):
        sampled_masks.extend(list(masks_seq or []))
        return [1, 0]

    monkeypatch.setattr(eval_module, "build_action_masks_by_head", _mock_build_masks)
    monkeypatch.setattr(eval_module, "sample_action_list_from_space", _mock_sample_action_list_from_space)
    action = eval_module.select_action_with_epsilon_sampled_muzero(
        env=object(),
        state=torch.zeros((1, 3), dtype=torch.float32),
        policy_net=object(),
        epsilon=1.0,
        len_model=0,
        side="enemy",
    )

    assert called_sides == ["enemy"]
    assert len(sampled_masks) == 2
    assert action.tolist() == [[1, 0]]
