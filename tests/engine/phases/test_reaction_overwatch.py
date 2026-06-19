"""B3-full Task 6: overwatch решается net-value lookahead.

defender=model стреляет overwatch по двигавшемуся enemy[0]. resolve_trigger(apply)
наносит урон врагу при apply. net «model» = -сумма HP врага → apply (урон) выгоднее.
"""

from core.models.reaction_value_policy import make_reaction_value_policy
from tests.engine.phases._helpers import build_env


class _ModelAdvantageNet:
    """value тем выше для model, чем меньше суммарное HP врага (нанесён урон)."""

    def __init__(self, env):
        self.env = env

    def infer(self, obs, masks_by_head=None):
        import torch

        return None, torch.tensor([-float(sum(self.env.enemy_health))])


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    # Гарантируем overwatch-кандидата: model[0] рядом с enemy[0], не в бою, с оружием.
    env.unit_coords[0] = [0.0, 0.0]
    env.enemy_coords[0] = [1.0, 1.0]
    env.unitInAttack[0] = [0, 0]
    env._reaction_net_by_side = {"model": _ModelAdvantageNet(env)}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")


def test_overwatch_used_when_damage_helps():
    env = build_env()
    _setup(env)

    def trig(apply):
        if apply:  # overwatch-выстрел наносит урон двигавшемуся врагу
            env.enemy_health[0] = max(0.0, env.enemy_health[0] - 3.0)

    env._pending_reaction_trigger = trig
    cp_before = env.modelCP
    env._resolve_overwatch("model", "enemy", 0, "movement")

    assert "overwatch" in [r[1] for r in env.stratagem_used]
    assert env.modelCP == cp_before - 1


def test_overwatch_skipped_on_tie():
    env = build_env()
    _setup(env)
    env._pending_reaction_trigger = lambda apply: None  # урона нет → тай → PASS
    cp_before = env.modelCP
    env._resolve_overwatch("model", "enemy", 0, "movement")

    assert "overwatch" not in [r[1] for r in env.stratagem_used]
    assert env.modelCP == cp_before
