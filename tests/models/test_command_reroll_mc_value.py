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


def _engage(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env._invalidate_target_cache("mc_test")


def test_mc_value_apply_beats_pass_when_reroll_adds_damage(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}

    # Детерминированная замена реальной атаки: при активной reroll-записи бьём сильнее.
    def fake_attack(side, att_idx, def_idx):
        dmg = 4.0 if env._command_reroll_record_exists(side, att_idx, "fight") else 1.0
        new_hp = max(0.0, float(env.enemy_health[def_idx]) - dmg)
        env._apply_health_update("enemy", def_idx, new_hp, reason="fight_sim")

    monkeypatch.setattr(env, "_simulate_fight_attack", fake_attack)
    mean_apply, mean_pass = env._mc_value_command_reroll_fight("model", 0, "wound", samples=4)
    assert mean_apply > mean_pass  # apply наносит больше урона → ниже HP врага → выше value


def test_mc_value_equal_when_reroll_no_benefit(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}

    def fake_attack(side, att_idx, def_idx):
        new_hp = max(0.0, float(env.enemy_health[def_idx]) - 1.0)  # одинаково в обеих ветках
        env._apply_health_update("enemy", def_idx, new_hp, reason="fight_sim")

    monkeypatch.setattr(env, "_simulate_fight_attack", fake_attack)
    mean_apply, mean_pass = env._mc_value_command_reroll_fight("model", 0, "wound", samples=4)
    assert mean_apply == mean_pass


def test_cmdreroll_mc_config_defaults(monkeypatch):
    import core.envs.warhamEnv as w
    monkeypatch.delenv("CMDREROLL_MC_SAMPLES", raising=False)
    monkeypatch.delenv("CMDREROLL_MC_EPS", raising=False)
    assert w._cmdreroll_mc_samples() == 8
    assert abs(w._cmdreroll_mc_eps() - 1e-3) < 1e-9
    monkeypatch.setenv("CMDREROLL_MC_SAMPLES", "3")
    monkeypatch.setenv("CMDREROLL_MC_EPS", "0.05")
    assert w._cmdreroll_mc_samples() == 3
    assert abs(w._cmdreroll_mc_eps() - 0.05) < 1e-9
