import random

import numpy as np

from core.engine.phases import phase_engine, stratagem_engine
from core.engine.phases.option_generator import fight_stratagem_options_for_unit
from core.engine.phases.stratagems import by_id
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env


def test_registry_has_command_reroll():
    d = by_id("command_reroll")
    assert d.cp_cost == 1
    assert d.effect_id == "command_reroll"


def test_fight_window_offers_command_reroll():
    env = build_env()
    env.modelCP = 1
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    ids = [o.meta["stratagem_id"] for o in opts if o.kind is ActionKind.USE_STRATAGEM]
    assert "command_reroll" in ids


def test_fight_window_offers_command_reroll_hit_and_wound():
    env = build_env()
    env.modelCP = 1
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    rolls = {
        o.param.get("reroll_roll")
        for o in opts
        if o.kind is ActionKind.USE_STRATAGEM and o.meta.get("stratagem_id") == "command_reroll"
    }
    assert rolls == {"hit", "wound"}


def test_apply_command_reroll_writes_reroll_effect():
    """Arm command_reroll: CP НЕ списывается (pay-on-apply переносится на consume);
    эффект помечается consumed=False + paid=False (armed, не оплачен)."""
    env = build_env()
    env.modelCP = 2
    env.battle_round = 3
    env.stratagem_used = []
    env.active_stratagem_effects = []
    res = stratagem_engine.apply(env, "model", "command_reroll", 0, phase="fight")
    assert res == {"ok": True, "cp_spent": 0, "reason": None}
    assert env.modelCP == 2  # arm бесплатен — CP не списан
    assert ("model", "command_reroll", 3, "fight", 0) in env.stratagem_used
    assert any(
        rec.get("effect_id") == "command_reroll"
        and rec.get("reroll_roll") == "wound"
        and rec.get("consumed") is False
        and rec.get("paid") is False
        for rec in env.active_stratagem_effects
    )


def test_apply_command_reroll_arm_does_not_charge_cp():
    """Подзадача 2.1: arm command_reroll НЕ списывает CP (cp_spent=0), CP неизменен."""
    env = build_env()
    env.modelCP = 2
    env.stratagem_used = []
    env.active_stratagem_effects = []
    res = stratagem_engine.apply(env, "model", "command_reroll", 0, phase="fight", reroll_roll="hit")
    assert res == {"ok": True, "cp_spent": 0, "reason": None}
    assert env.modelCP == 2  # arm бесплатен


def test_apply_command_reroll_arm_marks_effect_unpaid():
    """Подзадача 2.1: armed-эффект помечается paid=False (не оплачен на arm)."""
    env = build_env()
    env.modelCP = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="shooting", reroll_roll="wound")
    recs = [r for r in env.active_stratagem_effects if r.get("effect_id") == "command_reroll"]
    assert recs and recs[0].get("paid") is False
    assert recs[0].get("consumed") is False


def test_apply_command_reroll_arm_no_cp_returns_not_enough():
    """Подзадача 2.1: CP-check на arm сохраняется — при CP < cost отказ без эффекта и без журнала."""
    env = build_env()
    env.modelCP = 0
    env.stratagem_used = []
    env.active_stratagem_effects = []
    res = stratagem_engine.apply(env, "model", "command_reroll", 0, phase="fight")
    assert res == {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
    assert env.modelCP == 0  # CP не ушёл в минус
    assert env.stratagem_used == []  # без журнала
    assert env.active_stratagem_effects == []  # без эффекта


def test_apply_command_reroll_arm_still_appends_stratagem_used():
    """Подзадача 2.1: stratagem_used append остаётся на arm (action-telemetry/applied)."""
    env = build_env()
    env.modelCP = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="charge", reroll_roll="charge")
    assert ("model", "command_reroll", env.battle_round, "charge", 0) in env.stratagem_used
    assert env.modelCP == 1  # arm бесплатен, но запись в журнале есть


def test_fight_effects_for_attacker_returns_reroll_wounds():
    env = build_env()
    env.active_stratagem_effects = [
        {
            "side": "model",
            "unit_idx": 0,
            "round": int(env.battle_round),
            "phase": "fight",
            "effect_id": "command_reroll",
            "reroll_roll": "wound",
            "consumed": False,
        }
    ]
    eff = env._fight_effects_for_attacker("model", 0)
    assert eff == {"reroll_wounds": "one"}


def test_fight_effect_consumed_after_first_read():
    env = build_env()
    env.battle_round = 1
    env.active_stratagem_effects = [
        {
            "side": "model",
            "unit_idx": 0,
            "round": 1,
            "phase": "fight",
            "effect_id": "command_reroll",
            "reroll_roll": "wound",
            "consumed": False,
        }
    ]
    first = env._fight_effects_for_attacker("model", 0)
    assert first == {"reroll_wounds": "one"}
    second = env._fight_effects_for_attacker("model", 0)
    assert second is None


def _engaged(env):
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env.modelCP = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("test")


def _pick(unit_idx, sid):
    def decide(window):
        for o in window.options:
            if o.kind is ActionKind.USE_STRATAGEM and o.meta.get("stratagem_id") == sid and o.unit_idx == unit_idx:
                return o
        return window.options[0]

    return decide


def test_run_fight_command_reroll_arms_without_cp_charge():
    """Подзадача 2.1: arm command_reroll в fight НЕ списывает CP (pay-on-apply — отдельная подзадача).
    Запись в stratagem_used остаётся (action-telemetry); CP переносится на consume-точку."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    _engaged(env)
    random.seed(7)
    np.random.seed(7)
    with env.simulation_mode():
        phase_engine.run_fight(env, "model", _pick(0, "command_reroll"))
    assert env.modelCP == 1  # arm бесплатен — CP не списан (pay-on-apply перенесён)
    assert ("model", "command_reroll", env.battle_round, "fight", 0) in env.stratagem_used
