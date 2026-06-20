"""ppo_stratagem_bridge: install (side-generic) + critic-V."""

from unittest.mock import MagicMock

import torch

from core.models.ppo_stratagem_bridge import (
    install_ppo_stratagem_policy,
    ppo_build_fight_plan,
    ppo_reaction_value_policy_enabled,
    ppo_value,
)
from tests.engine.phases._helpers import build_env


class _ConstNet:
    """Возвращает фиксированный V на каждый infer_with_value."""

    def __init__(self, value):
        self._value = float(value)

    def infer_with_value(self, obs, masks_by_head=None):
        return None, torch.tensor([self._value])


def test_flag_enabled_default(monkeypatch):
    monkeypatch.delenv("PPO_REACTION_VALUE_POLICY", raising=False)
    assert ppo_reaction_value_policy_enabled() is True


def test_flag_off(monkeypatch):
    monkeypatch.setenv("PPO_REACTION_VALUE_POLICY", "0")
    assert ppo_reaction_value_policy_enabled() is False


def test_install_side_generic_sets_policy():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    net = _ConstNet(0.5)
    install_ppo_stratagem_policy(env, torch.device("cpu"), {"model": net})
    assert env.reaction_policy is not None
    assert env._reaction_net_by_side == {"model": net}


def test_install_accepts_both_sides():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    p1, p2 = _ConstNet(0.1), _ConstNet(0.2)
    install_ppo_stratagem_policy(env, torch.device("cpu"), {"model": p1, "enemy": p2})
    assert env._reaction_net_by_side == {"model": p1, "enemy": p2}


def test_ppo_value_returns_critic():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    v = ppo_value(env, _ConstNet(0.73), torch.device("cpu"), "model")
    assert abs(v - 0.73) < 1e-6


class _ValueSeqNet:
    """Возвращает заданную последовательность V при каждом infer_with_value."""

    def __init__(self, values):
        self._values = list(values)

    def infer_with_value(self, obs, masks_by_head=None):
        v = self._values.pop(0) if self._values else 0.0
        return None, torch.tensor([float(v)])


def test_fight_plan_snapshot_invariant():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.unitInAttack[0] = [1, 0]
    cp_before = int(env.modelCP)
    su_before = dict(getattr(env, "stratagem_used", {}) or {})
    plan = ppo_build_fight_plan(
        env, _ValueSeqNet([0.9, 0.1]), torch.device("cpu"), side="model"
    )
    assert isinstance(plan, dict)
    assert env.modelCP == cp_before  # snapshot/restore не испортил состояние
    assert dict(getattr(env, "stratagem_used", {}) or {}) == su_before


def test_fight_plan_empty_when_pass_wins():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.unitInAttack[0] = [1, 0]
    plan = ppo_build_fight_plan(
        env, _ValueSeqNet([0.1, 0.9]), torch.device("cpu"), side="model"
    )
    assert plan == {}


def test_fight_plan_skips_when_no_cp():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 0
    env.unitInAttack[0] = [1, 0]
    plan = ppo_build_fight_plan(
        env, _ValueSeqNet([0.9, 0.1]), torch.device("cpu"), side="model"
    )
    assert plan == {}


def test_fight_plan_recursion_guard():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env._reaction_sim_active = True
    net = MagicMock()
    assert ppo_build_fight_plan(env, net, torch.device("cpu")) == {}
    net.infer_with_value.assert_not_called()
