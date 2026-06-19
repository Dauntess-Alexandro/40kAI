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

    assert isinstance(effect, dict)
    assert effect.get("cover") is True
    assert int(effect.get("hit_penalty", 0)) == 1
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


def test_smokescreen_returns_cover_and_stealth():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.unit_data[0]["Keywords"] = ["Smoke"]
    eff = env._maybe_use_smokescreen("model", 0, "shooting")
    assert isinstance(eff, dict)
    assert eff.get("cover") is True
    assert int(eff.get("hit_penalty", 0)) == 1


def test_smokescreen_not_reapplied_same_phase():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.reaction_policy = None
    env.modelCP = 3
    env.battle_round = 1
    env.stratagem_used = []
    env.unit_data[0]["Keywords"] = ["Smoke"]
    eff1 = env._maybe_use_smokescreen("model", 0, "shooting")
    cp_after_first = env.modelCP
    n_after_first = len([r for r in env.stratagem_used if r[1] == "smokescreen"])
    eff2 = env._maybe_use_smokescreen("model", 0, "shooting")  # повтор той же фазы
    assert eff1 == {"cover": True, "hit_penalty": 1}
    assert eff2 == {"cover": True, "hit_penalty": 1}
    assert env.modelCP == cp_after_first  # CP не списан повторно
    assert len([r for r in env.stratagem_used if r[1] == "smokescreen"]) == n_after_first
    assert n_after_first == 1
