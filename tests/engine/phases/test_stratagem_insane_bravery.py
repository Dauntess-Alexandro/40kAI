"""B1a: Insane Bravery end-to-end — командная фаза, провал Battle-shock → 1 CP → auto-pass.

Сценарий синтетический: юнит ниже половины состава + Ld=13 (2D6 всегда < Ld) → тест Battle-shock
гарантированно провален. Проверяем, что выбор стратагемы тратит ровно 1 CP, снимает battle-shock
и пишется в журнал stratagem_used (основа eval-метрики cp_used>0).
"""

from core.engine.phases import phase_engine
from core.engine.phases.types import ActionKind, Phase
from tests.engine.phases._helpers import build_env


def _setup_shock_scenario(cp: int = 5):
    """Юнит 0 ниже половины состава, Battle-shock детерминированно проваливается."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    # health < W*#OfModels/2 = 3 → ниже половины; Ld=13 → sum(2D6)<=12 < Ld → провал.
    env.unit_health[0] = 1
    env.unit_data[0]["Ld"] = 13
    env.phase = "command"
    return env


def _pick_insane_bravery(window):
    for opt in window.options:
        if opt.kind is ActionKind.USE_STRATAGEM and opt.param.get("stratagem_id") == "insane_bravery":
            return opt
    return window.options[0]


def _pick_pass(window):
    for opt in window.options:
        if opt.kind is not ActionKind.USE_STRATAGEM:
            return opt
    return window.options[0]


def test_insane_bravery_option_offered_in_command_window():
    env = _setup_shock_scenario()
    win = phase_engine.command_window(env, "model")
    assert win.phase is Phase.COMMAND
    sids = {opt.param.get("stratagem_id") for opt in win.options if opt.kind is ActionKind.USE_STRATAGEM}
    assert "insane_bravery" in sids


def test_insane_bravery_spends_one_cp_and_passes_shock():
    env = _setup_shock_scenario(cp=5)
    state = phase_engine.run_command(env, "model", _pick_insane_bravery)
    # CP: +1 (старт командной фазы) − 1 (стратагема) = исходное значение.
    assert env.modelCP == 5
    assert state.battle_shock[0] is False
    used_ids = [rec[1] for rec in env.stratagem_used]
    assert "insane_bravery" in used_ids


def test_pass_leaves_shock_and_keeps_cp():
    env = _setup_shock_scenario(cp=5)
    state = phase_engine.run_command(env, "model", _pick_pass)
    # Без стратагемы: только +1 CP за командную фазу, battle-shock остаётся.
    assert env.modelCP == 6
    assert state.battle_shock[0] is True
    assert all(rec[1] != "insane_bravery" for rec in env.stratagem_used)


def test_insane_bravery_blocked_without_cp():
    env = _setup_shock_scenario(cp=0)
    # modelCP станет 1 в начале фазы — хватит на 1 CP стратагему; занулим после +1, проверим отказ.
    # Чтобы смоделировать «нет CP», ставим cp=-1 → после +1 = 0 < cost.
    env.modelCP = -1
    state = phase_engine.run_command(env, "model", _pick_insane_bravery)
    assert env.modelCP == 0
    assert state.battle_shock[0] is True
    assert all(rec[1] != "insane_bravery" for rec in env.stratagem_used)


def test_insane_bravery_value_gate_used_when_policy(monkeypatch):
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    calls = {}
    def fake_gate(sid, side, chosen, cand, phase, cp, **k):
        calls["sid"] = sid
        return True
    env.reaction_policy = object()  # не None
    monkeypatch.setattr(env, "_should_use_stratagem", fake_gate)
    # форсим провал battle-shock на юните 0
    monkeypatch.setattr("core.envs.warhamEnv.dice", lambda num=1: [1, 1])
    env.unit_health[0] = 1
    env.unit_data[0]["W"] = 4  # ниже половины
    env.modelCP = 3
    env.command_phase("model", action={"use_cp": 0, "cp_on": -1})
    assert calls.get("sid") == "insane_bravery"
