"""Stage 4: value-driven выбор Command Re-roll во всех фазах (DQN/PPO reaction-policy)."""

import torch

from core.engine.phases import stratagem_engine
from core.models.dqn_stratagem_bridge import install_dqn_stratagem_policy
from tests.engine.phases._helpers import build_env, flat_default_action


class _ValueSeqNet:
    """Стаб value-сети: отдаёт заданную последовательность V на каждый infer_with_value."""

    def __init__(self, values):
        self._values = list(values)

    def infer_with_value(self, obs, masks_by_head=None):
        v = self._values.pop(0) if self._values else 0.0
        return None, torch.tensor([float(v)])


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("command_reroll_value_test")


# --- _value_pick_command_reroll ---


def test_value_pick_none_without_policy():
    env = build_env()
    _setup(env)
    assert env._value_pick_command_reroll("model", 0, "shooting", ("hit", "wound")) is None


def test_value_pick_picks_first_subtype_when_apply_wins():
    # generic-policy loop (вырожденный путь) теперь обслуживает только movement;
    # shooting/charge идут через MC-оценщики (см. test_command_reroll_mc_shooting_charge).
    env = build_env()
    _setup(env)
    net = _ValueSeqNet([0.1, 0.9])  # pass=0.1, apply=0.9 → apply > pass на первом под-типе
    install_dqn_stratagem_policy(env, {"model": net}, torch.device("cpu"))
    assert env._value_pick_command_reroll("model", 0, "movement", ("hit", "wound")) == "hit"


def test_value_pick_none_when_pass_wins_all_subtypes():
    env = build_env()
    _setup(env)
    net = _ValueSeqNet([0.9, 0.1, 0.9, 0.1])  # оба под-типа: pass > apply
    install_dqn_stratagem_policy(env, {"model": net}, torch.device("cpu"))
    assert env._value_pick_command_reroll("model", 0, "shooting", ("hit", "wound")) is None


def test_value_pick_none_without_net_for_side():
    env = build_env()
    _setup(env)
    net = _ValueSeqNet([0.1, 0.9])
    install_dqn_stratagem_policy(env, {"model": net}, torch.device("cpu"))
    assert env._value_pick_command_reroll("enemy", 0, "shooting", ("hit",)) is None


def test_value_pick_none_when_record_already_exists():
    env = build_env()
    _setup(env)
    net = _ValueSeqNet([0.1, 0.9])
    install_dqn_stratagem_policy(env, {"model": net}, torch.device("cpu"))
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="shooting", reroll_roll="hit")
    assert env._value_pick_command_reroll("model", 0, "shooting", ("hit", "wound")) is None


# --- интеграция в фазы (env.step-путь) ---


def _engage_shoot(env):
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._invalidate_target_cache("engage_shoot")


def test_shooting_phase_value_applies_command_reroll(monkeypatch):
    # shooting теперь идёт через MC-оценщик, а не через generic-policy loop;
    # подменяем MC чтобы «apply всегда выигрывает».
    env = build_env()
    _setup(env)
    _engage_shoot(env)
    net = _ValueSeqNet([0.1, 0.9] * 64)
    install_dqn_stratagem_policy(env, {"model": net}, torch.device("cpu"))
    monkeypatch.setattr(
        env, "_mc_value_command_reroll_shooting",
        lambda side, u, sub, n: (5.0, 1.0) if sub == "wound" else (1.0, 1.0),
    )
    with env.simulation_mode():
        env.shooting_phase(
            "model",
            advanced_flags=[False] * len(env.unit_health),
            action=flat_default_action(len(env.unit_health), shoot_num_0=0),
        )
    assert any(r[1] == "command_reroll" and r[3] == "shooting" for r in env.stratagem_used)


def test_shooting_phase_no_policy_is_parity():
    env = build_env()
    _setup(env)
    _engage_shoot(env)
    with env.simulation_mode():
        env.shooting_phase(
            "model",
            advanced_flags=[False] * len(env.unit_health),
            action=flat_default_action(len(env.unit_health), shoot_num_0=0),
        )
    assert not any(r[1] == "command_reroll" for r in env.stratagem_used)
    assert env.modelCP == 2


def test_charge_phase_value_applies_command_reroll(monkeypatch):
    # charge теперь идёт через MC-оценщик; подменяем MC чтобы «apply выигрывает».
    env = build_env()
    _setup(env)
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [19, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env._invalidate_target_cache("engage_charge")
    net = _ValueSeqNet([0.1, 0.9] * 64)
    install_dqn_stratagem_policy(env, {"model": net}, torch.device("cpu"))
    monkeypatch.setattr(
        env, "_mc_value_command_reroll_charge",
        lambda side, u, sub, n: (5.0, 1.0),
    )
    with env.simulation_mode():
        env.charge_phase(
            "model",
            advanced_flags=[False] * len(env.unit_health),
            action=flat_default_action(len(env.unit_health), attack=1, charge_num_0=0),
        )
    assert any(r[1] == "command_reroll" and r[3] == "charge" for r in env.stratagem_used)
