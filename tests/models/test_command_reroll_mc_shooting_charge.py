import torch

from tests.engine.phases._helpers import build_env


class _HpAwareNet:
    """value = -sum(HP врага стороны): меньше HP врага → выше value."""

    def __init__(self, env, side):
        self.env = env
        self.side = side

    def infer_with_value(self, obs, masks_by_head=None):
        opp = self.env.enemy_health if self.side == "model" else self.env.unit_health
        return None, torch.tensor([-float(sum(opp))])


def _setup(env, cp=3):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("mc_sc_test")


def test_expected_shoot_damage_positive_for_valid_target():
    env = build_env()
    _setup(env)
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._invalidate_target_cache("ev")
    ev = env._expected_shoot_damage("model", 0, 0)
    assert ev > 0.0


def test_best_shoot_target_picks_max_ev(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(env, "get_shoot_targets_for_unit", lambda side, i: [0, 1])
    monkeypatch.setattr(
        env, "_expected_shoot_damage",
        lambda side, s, t: 5.0 if t == 1 else 1.0,
    )
    assert env._best_shoot_target("model", 0) == 1


def test_best_shoot_target_none_without_targets(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(env, "get_shoot_targets_for_unit", lambda side, i: [])
    assert env._best_shoot_target("model", 0) is None
