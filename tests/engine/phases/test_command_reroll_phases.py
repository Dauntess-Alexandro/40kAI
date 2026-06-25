import numpy as np

import core.envs.warhamEnv as warham_mod
from core.engine.phases import phase_engine, stratagem_engine
from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases.stratagems import by_id, stratagem_choice_index
from core.engine.phases.types import ActionKind, Phase
from tests.engine.phases._helpers import build_env, flat_default_action


def _pick_reroll_window(unit_idx, roll):
    """decide: выбрать опцию Command Re-roll нужного под-типа в стратагем-окне; иначе options[0]."""

    def decide(window):
        for o in window.options:
            if (
                o.kind is ActionKind.USE_STRATAGEM
                and o.meta.get("stratagem_id") == "command_reroll"
                and o.param.get("reroll_roll") == roll
                and o.unit_idx == unit_idx
            ):
                return o
        return window.options[0]

    return decide


def _shooting_setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.modelCP = 2
    env.enemyCP = 2
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("command_reroll_phases_test")


def _shoot_action(env):
    return flat_default_action(len(env.unit_health), shoot_num_0=0)


def _charge_setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [19, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env.modelCP = 2
    env.enemyCP = 0
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("command_reroll_charge_test")


def _movement_setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [2, 2]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.modelCP = 2
    env.enemyCP = 0
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("command_reroll_movement_test")


def _advance_option_with_non_max_roll(env):
    opts = movement_options_for_unit(env, "model", 0)
    base_m = int(env.unit_data[0]["Movement"])
    row, col = [int(v) for v in env.unit_coords[0]]
    fallback = None
    for opt in opts:
        if opt.kind is not ActionKind.ADVANCE:
            continue
        dest_x, dest_y = opt.param["dest"]
        distance = env._grid_distance_chebyshev((row, col), (int(dest_y), int(dest_x)))
        advance_roll = max(1, min(6, int(distance) - base_m))
        fallback = fallback or opt
        if advance_roll != 6:
            return opt
    if fallback is None:
        raise AssertionError("no advance option for movement command reroll test")
    return fallback


def test_command_reroll_registry_includes_shooting_phase():
    assert Phase.SHOOTING in by_id("command_reroll").phases


def test_command_reroll_registry_includes_movement_phase_for_advance():
    assert Phase.MOVEMENT in by_id("command_reroll").phases


def test_command_reroll_registry_includes_charge_phase():
    assert Phase.CHARGE in by_id("command_reroll").phases


def test_movement_command_reroll_advance_is_illegal_option(monkeypatch):
    """Подзадача 3.3A: command_reroll:advance — нелегальная опция в movement-окне.

    advance не имеет pass/fail-критерия, поэтому option_generator не предлагает его,
    а direct action-head strat_movement=command_reroll:advance не arm-ит effect
    и не тратит CP (action-контракт не меняется — подтип остаётся в choices).
    """
    calls = []

    def fake_dice(*, min=1, max=6, num=1):
        calls.append((min, max, num))
        return 6

    monkeypatch.setattr(warham_mod, "dice", fake_dice)
    env = build_env()
    _movement_setup(env)
    start_cp = env.modelCP
    chosen = _advance_option_with_non_max_roll(env)
    action = flat_default_action(len(env.unit_health), **chosen.legacy_patch)
    # direct action-head выставляет command_reroll:advance (контракт не меняется),
    # но guard должен не arm-ить effect и не тратить CP.
    action["strat_movement"] = stratagem_choice_index(Phase.MOVEMENT, "command_reroll:advance")
    action["strat_movement_unit"] = 0

    with env.simulation_mode():
        env.movement_phase("model", action=action, battle_shock=[False] * len(env.unit_health))

    # advance reroll не arm-ится → нет записи command_reroll в movement-окне.
    assert not any(
        r.get("effect_id") == "command_reroll" and r.get("phase") == "movement"
        for r in env.active_stratagem_effects
    )
    assert not any(r[1] == "command_reroll" and r[3] == "movement" for r in env.stratagem_used)
    # CP не тратится (arm бесплатен + advance не arm-ится).
    assert env.modelCP == start_cp
    # reroll-броска advance не происходит (advance_roll остаётся исходным).
    assert calls == []


def _armed_charge_reroll(env, side="model", unit_idx=0):
    """Вручную вставить armed command_reroll:charge (paid=False), как делает apply при CP>=1."""
    rec = {
        "effect_id": "command_reroll",
        "phase": "charge",
        "side": side,
        "unit_idx": int(unit_idx),
        "reroll_roll": "charge",
        "round": int(getattr(env, "battle_round", 1)),
        "consumed": False,
        "paid": False,
    }
    env.active_stratagem_effects.append(rec)
    return rec


def test_charge_reroll_first_roll_success_keeps_cp(monkeypatch):
    """Подзадача 3.3B: первый 2D6 успешен → CP не тратится, reroll не применяется.

    rolls [6,6]=12, цель в дистанции 9 (required=4). armed charge reroll, modelCP=1.
    Ожидание: один бросок 2D6, CP остаётся 1, charge успешен.
    """
    calls = []

    def fake_dice(*, min=1, max=6, num=1):
        calls.append((min, max, num))
        return np.array([6, 6])

    monkeypatch.setattr(warham_mod, "dice", fake_dice)
    env = build_env()
    _charge_setup(env)
    env.modelCP = 1
    rec = _armed_charge_reroll(env)
    action = flat_default_action(len(env.unit_health), attack=1, charge_num_0=0)

    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * len(env.unit_health), action=action)

    assert calls == [(1, 6, 2)]  # только первый бросок — reroll не нужен
    assert env.modelCP == 1  # успешный first roll → CP не тратится
    assert rec["paid"] is False
    assert rec["consumed"] is False
    assert env.unitCharged[0] == 1  # charge успешен


def test_charge_reroll_first_fail_then_reroll_succeeds_spends_cp(monkeypatch):
    """Подзадача 3.3B: первый 2D6 провален → reroll, CP тратится на actual failed charge.

    rolls [1,1]=2 (провал, required=4) затем [6,6]=12 (успех). modelCP=1.
    Ожидание: два броска 2D6, CP=0, charge успешен.
    """
    rolls = [np.array([1, 1]), np.array([6, 6])]
    calls = []

    def fake_dice(*, min=1, max=6, num=1):
        calls.append((min, max, num))
        return rolls.pop(0)

    monkeypatch.setattr(warham_mod, "dice", fake_dice)
    env = build_env()
    _charge_setup(env)
    env.modelCP = 1
    rec = _armed_charge_reroll(env)
    action = flat_default_action(len(env.unit_health), attack=1, charge_num_0=0)

    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * len(env.unit_health), action=action)

    assert calls == [(1, 6, 2), (1, 6, 2)]  # первый провален → reroll
    assert env.modelCP == 0  # actual failed charge → CP списан один раз
    assert rec["paid"] is True
    assert rec["consumed"] is True
    assert env.unitCharged[0] == 1  # reroll успешен → charge удался


def test_charge_reroll_first_fail_no_cp_no_reroll(monkeypatch):
    """Подзадача 3.3B: первый 2D6 провален, но CP=0 → reroll не применяется, CP не в минус.

    rolls [1,1]=2 (провал, required=4). armed rec paid=False, но modelCP=0.
    Ожидание: один бросок 2D6, reroll не применяется, CP=0 (не в минус), charge провален.
    """
    calls = []

    def fake_dice(*, min=1, max=6, num=1):
        calls.append((min, max, num))
        return np.array([1, 1])

    monkeypatch.setattr(warham_mod, "dice", fake_dice)
    env = build_env()
    _charge_setup(env)
    env.modelCP = 0
    # Вручную вставляем armed rec (apply при CP=0 не arm-ит) — моделируем «был CP, потратили».
    rec = _armed_charge_reroll(env)
    action = flat_default_action(len(env.unit_health), attack=1, charge_num_0=0)

    with env.simulation_mode():
        env.charge_phase("model", advanced_flags=[False] * len(env.unit_health), action=action)

    assert calls == [(1, 6, 2)]  # нет CP → reroll не применяется
    assert env.modelCP == 0  # CP не ушёл в минус
    assert rec["paid"] is False
    assert rec["consumed"] is False
    assert env.unitCharged[0] == 0  # charge провален


def test_command_reroll_unlimited_allows_two_rolls_same_phase():
    """Подзадача 2.1: два arm command_reroll в одной фазе разрешены (UNLIMITED); CP НЕ списывается на arm."""
    env = build_env()
    _shooting_setup(env)
    env.modelCP = 2

    first = stratagem_engine.apply(env, "model", "command_reroll", 0, phase="shooting", reroll_roll="hit")
    second = stratagem_engine.apply(env, "model", "command_reroll", 0, phase="shooting", reroll_roll="wound")

    assert first["ok"] is True
    assert second["ok"] is True
    assert env.modelCP == 2  # arm бесплатен — CP не списан за оба arm
    rolls = [
        rec.get("reroll_roll")
        for rec in env.active_stratagem_effects
        if rec.get("effect_id") == "command_reroll"
    ]
    assert rolls == ["hit", "wound"]


def test_shooting_command_reroll_wound_reaches_attack_effect(monkeypatch):
    """Подзадача 3.2: command_reroll wound НЕ попадает в static effects (effects без reroll_wounds),
    а проходит через reroll_decider. fake_attack проверяет: effects не содержит command_reroll-ключей,
    а decider("wound", [1], 4) возвращает True и списывает CP."""
    calls = []

    def fake_attack(attacker_health, weapon, attacker_data, defender_health, defender_data, *args, **kwargs):
        effects = kwargs.get("effects")
        decider = kwargs.get("reroll_decider")
        # command_reroll НЕ должен попасть в static effects.
        assert effects is None or "reroll_wounds" not in (effects or {})
        assert effects is None or "reroll_hits" not in (effects or {})
        # decider есть и вызывается с фактическим failed die → списывает CP.
        decider_result = None
        if decider is not None:
            decider_result = bool(decider("wound", np.array([1]), 4))
        calls.append(decider_result)
        return [0.0], defender_health

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    _shooting_setup(env)
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="shooting", reroll_roll="wound")

    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=_shoot_action(env))

    # decider вызван с failed die (1 < 4) → True, CP списан.
    assert calls and calls[0] is True
    assert env.modelCP == 1  # _shooting_setup ставит modelCP=2; arm бесплатен, decider списал 1 → 1


def test_shooting_command_reroll_save_belongs_to_defender(monkeypatch):
    calls = []

    def fake_attack(attacker_health, weapon, attacker_data, defender_health, defender_data, *args, **kwargs):
        decider = kwargs.get("reroll_decider")
        calls.append(
            {
                "hit": bool(decider("hit", np.array([2]), 4)),
                "save": bool(decider("save", np.array([2]), 4)),
            }
        )
        return [0.0], defender_health

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    _shooting_setup(env)
    stratagem_engine.apply(env, "enemy", "command_reroll", 0, phase="shooting", reroll_roll="save")

    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=_shoot_action(env))

    assert calls == [{"hit": False, "save": True}]


def test_run_movement_window_does_not_offer_advance_reroll():
    """Подзадача 3.3A: windowed movement больше не предлагает command_reroll:advance."""
    env = build_env()
    _movement_setup(env)
    start_cp = env.modelCP
    with env.simulation_mode():
        phase_engine.run_movement(env, "model", _pick_reroll_window(0, "advance"))
    assert ("model", "command_reroll", env.battle_round, "movement", 0) not in env.stratagem_used
    assert env.modelCP == start_cp


def test_run_shooting_window_offers_and_arms_command_reroll():
    """Подзадача 2.1: windowed-путь shooting — arm command_reroll пишет запись, CP НЕ списывается."""
    env = build_env()
    _shooting_setup(env)
    start_cp = env.modelCP
    with env.simulation_mode():
        phase_engine.run_shooting(env, "model", _pick_reroll_window(0, "wound"))
    assert ("model", "command_reroll", env.battle_round, "shooting", 0) in env.stratagem_used
    assert env.modelCP == start_cp  # arm бесплатен — CP не списан


def test_run_charge_window_offers_and_arms_command_reroll():
    """Подзадача 2.1: windowed-путь charge — arm command_reroll пишет запись, CP НЕ списывается."""
    env = build_env()
    _charge_setup(env)
    start_cp = env.modelCP
    with env.simulation_mode():
        phase_engine.run_charge(env, "model", _pick_reroll_window(0, "charge"))
    assert ("model", "command_reroll", env.battle_round, "charge", 0) in env.stratagem_used
    assert env.modelCP == start_cp  # arm бесплатен — CP не списан


def test_run_movement_window_default_decide_does_not_use_cp():
    """Регрессия: дефолтный decide (options[0]=PASS) не тратит CP в movement-стратагем-окне."""
    env = build_env()
    _movement_setup(env)
    start_cp = env.modelCP
    with env.simulation_mode():
        phase_engine.run_movement(env, "model", lambda w: w.options[0])
    assert env.modelCP == start_cp
    assert not any(rec[1] == "command_reroll" for rec in env.stratagem_used)
