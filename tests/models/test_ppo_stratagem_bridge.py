"""ppo_stratagem_bridge: install (side-generic) + critic-V (fight-plan функции удалены в Task 3)."""

import torch

from core.models.ppo_stratagem_bridge import (
    install_ppo_stratagem_policy,
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
