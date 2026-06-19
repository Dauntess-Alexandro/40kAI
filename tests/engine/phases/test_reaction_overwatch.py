"""B3-full Task 6/8b: overwatch решается net-value lookahead через реальный call-site trigger.

defender=model стреляет overwatch по двигавшемуся enemy[0]. Call-site строит реальный
trigger (overwatch-выстрел). net «model» = -сумма HP врага → если выстрел наносит урон,
apply выгоднее; если урона нет — тай → PASS.
"""

import core.envs.warhamEnv as warham_mod
from core.models.reaction_value_policy import make_reaction_value_policy
from tests.engine.phases._helpers import build_env


class _ModelAdvantageNet:
    def __init__(self, env):
        self.env = env

    def infer(self, obs, masks_by_head=None):
        import torch

        return None, torch.tensor([-float(sum(self.env.enemy_health))])


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.unit_coords[0] = [0.0, 0.0]
    env.enemy_coords[0] = [1.0, 1.0]
    env.unitInAttack[0] = [0, 0]
    env._reaction_net_by_side = {"model": _ModelAdvantageNet(env)}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")


def test_overwatch_used_when_damage_helps(monkeypatch):
    def fake_attack(ah, w, ad, dh, dd, *a, **k):
        return [3.0], max(0.0, dh - 3.0)  # overwatch наносит урон

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    _setup(env)
    cp_before = env.modelCP
    env._resolve_overwatch("model", "enemy", 0, "movement")

    assert "overwatch" in [r[1] for r in env.stratagem_used]
    assert env.modelCP == cp_before - 1


def test_overwatch_skipped_when_no_damage(monkeypatch):
    def fake_attack(ah, w, ad, dh, dd, *a, **k):
        return [0.0], dh  # урона нет → тай → PASS

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    _setup(env)
    cp_before = env.modelCP
    env._resolve_overwatch("model", "enemy", 0, "movement")

    assert "overwatch" not in [r[1] for r in env.stratagem_used]
    assert env.modelCP == cp_before
