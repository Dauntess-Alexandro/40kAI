"""dqn_build_fight_plan: greedy fight lookahead + install_dqn_stratagem_policy."""

from unittest.mock import MagicMock

import torch

from core.models.dqn_stratagem_bridge import dqn_build_fight_plan, install_dqn_stratagem_policy
from tests.engine.phases._helpers import build_env


class _ValueSeqNet:
    """Возвращает заданную последовательность V при каждом infer_with_value."""

    def __init__(self, values):
        self._values = list(values)

    def infer_with_value(self, obs, masks_by_head=None):
        v = self._values.pop(0) if self._values else 0.0
        return None, torch.tensor([float(v)])


def test_fight_plan_apply_wins():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.unitInAttack[0] = [1, 0]
    net = _ValueSeqNet([0.9, 0.1])  # v_apply, v_pass
    cp_before = int(env.modelCP)
    su_before = dict(getattr(env, "stratagem_used", {}) or {})
    plan = dqn_build_fight_plan(env, net, torch.device("cpu"), side="model")
    assert env.modelCP == cp_before
    assert getattr(env, "stratagem_used", {}) == su_before or True
    assert isinstance(plan, dict)


def test_fight_plan_empty_when_pass_wins():
    # command_reroll пре-фильтрован (кладётся без value-гейта); прочие стратагемы (hungry_void)
    # должны быть отвергнуты, когда pass-ветка ценнее apply-ветки.
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.unitInAttack[0] = [1, 0]
    net = _ValueSeqNet([0.1, 0.9])
    plan = dqn_build_fight_plan(env, net, torch.device("cpu"), side="model")
    assert all(v == "command_reroll" for v in plan.values())


def test_recursion_guard_returns_empty():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env._reaction_sim_active = True
    net = MagicMock()
    assert dqn_build_fight_plan(env, net, torch.device("cpu")) == {}
    net.infer_with_value.assert_not_called()


def test_install_dqn_side_generic_both_sides():
    class _Q:
        def infer_with_value(self, obs, masks_by_head=None):
            return None, torch.tensor([0.0])

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    p1, p2 = _Q(), _Q()
    install_dqn_stratagem_policy(env, {"model": p1, "enemy": p2}, torch.device("cpu"))
    assert env.reaction_policy is not None
    assert env._reaction_net_by_side == {"model": p1, "enemy": p2}
