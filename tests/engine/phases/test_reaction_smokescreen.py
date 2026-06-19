"""B3-full Task 5: smokescreen решается net-value lookahead (резолв входящего выстрела).

Как go_to_ground, но defender имеет keyword SMOKE и стратагема — smokescreen.
"""

from core.models.reaction_value_policy import make_reaction_value_policy
from tests.engine.phases._helpers import build_env


class _EnemyHpNet:
    def __init__(self, env):
        self.env = env

    def infer(self, obs, masks_by_head=None):
        import torch

        return None, torch.tensor([float(sum(self.env.enemy_health))])


def test_smokescreen_applied_when_cover_saves_damage():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 3
    env.enemy_data[0]["Keywords"] = ["Smoke"]
    env.stratagem_used = []
    net = _EnemyHpNet(env)
    env._reaction_net_by_side = {"enemy": net}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")

    def trig(apply):
        if not apply:
            env.enemy_health[0] = max(0.0, env.enemy_health[0] - 3.0)

    env._pending_reaction_trigger = trig

    cp_before = env.enemyCP
    effect = env._maybe_use_smokescreen("enemy", 0, "shooting")

    assert effect == "benefit of cover"
    assert "smokescreen" in [r[1] for r in env.stratagem_used]
    assert env.enemyCP == cp_before - 1


def test_smokescreen_skipped_on_tie():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 3
    env.enemy_data[0]["Keywords"] = ["Smoke"]
    env.stratagem_used = []
    net = _EnemyHpNet(env)
    env._reaction_net_by_side = {"enemy": net}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")
    env._pending_reaction_trigger = lambda apply: None

    cp_before = env.enemyCP
    effect = env._maybe_use_smokescreen("enemy", 0, "shooting")

    assert effect is None
    assert "smokescreen" not in [r[1] for r in env.stratagem_used]
    assert env.enemyCP == cp_before
