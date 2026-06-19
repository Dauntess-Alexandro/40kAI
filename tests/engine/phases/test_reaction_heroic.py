"""B3-full Task 7: heroic_intervention решается net-value lookahead.

defender=model контратакует зашедшего enemy[0]. resolve_trigger(apply) ставит
model[0] в бой (engagement). net «model» = 1 если model[0] в бою → counter-charge
выгоднее → heroic выбирается и тратит 2 CP.
"""

from core.models.reaction_value_policy import make_reaction_value_policy
from tests.engine.phases._helpers import build_env


class _EngagementNet:
    def __init__(self, env):
        self.env = env

    def infer(self, obs, masks_by_head=None):
        import torch

        return None, torch.tensor([float(self.env.unitInAttack[0][0])])


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.unit_coords[0] = [0.0, 0.0]
    env.enemy_coords[0] = [1.0, 1.0]
    env.unitInAttack[0] = [0, 0]
    env._reaction_net_by_side = {"model": _EngagementNet(env)}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")


def test_heroic_used_when_counter_charge_helps():
    # Реальный call-site trigger (_rt_heroic) ставит model[0] в бой; net ценит engagement → used.
    env = build_env()
    _setup(env)
    cp_before = env.modelCP
    env._resolve_heroic_intervention("model", "enemy", 0, "charge")

    assert "heroic_intervention" in [r[1] for r in env.stratagem_used]
    assert env.modelCP == cp_before - 2


class _ConstNet:
    def infer(self, obs, masks_by_head=None):
        import torch

        return None, torch.tensor([0.0])


def test_heroic_skipped_when_value_indifferent():
    # net безразличен к engagement → apply == pass → тай → PASS.
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _ConstNet()}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")
    cp_before = env.modelCP
    env._resolve_heroic_intervention("model", "enemy", 0, "charge")

    assert "heroic_intervention" not in [r[1] for r in env.stratagem_used]
    assert env.modelCP == cp_before
