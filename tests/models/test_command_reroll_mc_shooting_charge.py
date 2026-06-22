import torch

from core.engine.phases import stratagem_engine  # noqa: F401
from core.models.dqn_stratagem_bridge import install_dqn_stratagem_policy
from tests.engine.phases._helpers import build_env, flat_default_action


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


def test_mc_shooting_apply_beats_pass_when_reroll_adds_damage(monkeypatch):
    env = build_env()
    _setup(env)
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._invalidate_target_cache("mc_sh")
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}

    def fake_shoot(side, shooter, target):
        dmg = 4.0 if env._command_reroll_record_exists(side, shooter, "shooting") else 1.0
        env._apply_health_update("enemy", target, max(0.0, float(env.enemy_health[target]) - dmg), reason="shooting_sim")

    monkeypatch.setattr(env, "_simulate_shoot_attack", fake_shoot)
    monkeypatch.setattr(env, "_best_shoot_target", lambda side, u: 0)
    ma, mp = env._mc_value_command_reroll_shooting("model", 0, "wound", samples=4)
    assert ma > mp


def test_mc_shooting_zero_when_no_target(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    monkeypatch.setattr(env, "_best_shoot_target", lambda side, u: None)
    assert env._mc_value_command_reroll_shooting("model", 0, "wound", samples=4) == (0.0, 0.0)


def test_best_charge_target_picks_max_advantage(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(env, "get_charge_targets_for_unit", lambda side, u: [0, 1])
    monkeypatch.setattr(
        env, "_melee_strength_score",
        lambda side, idx: 9.0 if side == "model" else (1.0 if idx == 1 else 5.0),
    )
    # advantage vs t1 = 9-1=8 > vs t0 = 9-5=4 → t1
    assert env._best_charge_target("model", 0) == 1


def test_mc_charge_apply_beats_pass_when_reroll_makes_charge(monkeypatch):
    env = build_env()
    _setup(env)
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    monkeypatch.setattr(env, "_best_charge_target", lambda side, u: 0)

    def fake_charge(side, u, t):
        # apply (реролл-запись) → успех (engaged); pass → нет
        if env._command_reroll_record_exists(side, u, "charge"):
            env.unitInAttack[u] = [1, t]
            env.enemy_health[t] = max(0.0, float(env.enemy_health[t]) - 2.0)

    monkeypatch.setattr(env, "_simulate_charge_attempt", fake_charge)
    ma, mp = env._mc_value_command_reroll_charge("model", 0, "charge", samples=4)
    assert ma > mp


def test_value_pick_shooting_uses_mc(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: False
    monkeypatch.setattr(
        env, "_mc_value_command_reroll_shooting",
        lambda side, u, sub, n: (5.0, 1.0) if sub == "wound" else (1.0, 1.0),
    )
    assert env._value_pick_command_reroll("model", 0, "shooting", ("hit", "wound")) == "wound"


def test_value_pick_charge_uses_mc(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: False
    monkeypatch.setattr(env, "_mc_value_command_reroll_charge", lambda side, u, sub, n: (5.0, 1.0))
    assert env._value_pick_command_reroll("model", 0, "charge", ("charge",)) == "charge"


def test_value_pick_shooting_none_below_eps(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: True
    monkeypatch.setattr(env, "_mc_value_command_reroll_shooting", lambda *a, **k: (1.0, 1.0))
    assert env._value_pick_command_reroll("model", 0, "shooting", ("hit", "wound")) is None


# ---------------------------------------------------------------------------
# e2e: shooting_phase с DQN reaction policy + parity без policy
# ---------------------------------------------------------------------------


def _engage_shoot(env):
    """Сетап для стрельбы: unit 0 → enemy 0 в range, остальные мертвы."""
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._invalidate_target_cache("engage_shoot")


def test_shooting_phase_value_applies_command_reroll(monkeypatch):
    """shooting_phase с DQN policy + MC monkeypatch → command_reroll записан."""
    env = build_env()
    _setup(env)
    _engage_shoot(env)
    install_dqn_stratagem_policy(env, {"model": _HpAwareNet(env, "model")}, torch.device("cpu"))
    # MC: реролл выгоден.
    monkeypatch.setattr(env, "_mc_value_command_reroll_shooting", lambda side, u, sub, n: (5.0, 1.0) if sub == "wound" else (1.0, 1.0))
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=flat_default_action(len(env.unit_health), shoot_num_0=0))
    assert any(r[1] == "command_reroll" and r[3] == "shooting" for r in env.stratagem_used)


def test_shooting_phase_parity_without_policy():
    """shooting_phase без policy → command_reroll НЕ записан, CP не тратится."""
    env = build_env()
    _setup(env)
    _engage_shoot(env)
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=flat_default_action(len(env.unit_health), shoot_num_0=0))
    assert not any(r[1] == "command_reroll" for r in env.stratagem_used)
    assert env.modelCP == 3


def test_movement_phase_does_not_apply_command_reroll_even_with_policy():
    """Регрессия: movement НЕ предлагает Command Re-roll (advance вне области MC);
    даже с установленной reaction_policy юнит не тратит CP на реролл в движении."""
    env = build_env()
    _setup(env)
    install_dqn_stratagem_policy(env, {"model": _HpAwareNet(env, "model")}, torch.device("cpu"))
    cp_before = env.modelCP
    with env.simulation_mode():
        env.movement_phase(
            "model",
            action=flat_default_action(len(env.unit_health)),
            battle_shock=[False] * len(env.unit_health),
        )
    assert not any(r[1] == "command_reroll" for r in env.stratagem_used)
    assert env.modelCP == cp_before
