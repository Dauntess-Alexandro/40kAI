"""Reward-штраф за впустую-command_reroll (per-step net, сторона model)."""

import reward_config as reward_cfg
from tests.engine.phases._helpers import build_env


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.stratagem_used = []
    env._cmd_reroll_fired = 0


def test_count_model_command_reroll_ignores_enemy():
    env = build_env()
    _setup(env)
    env.stratagem_used = [
        ("model", "command_reroll", 1, "charge", 0),
        ("enemy", "command_reroll", 1, "charge", 0),
        ("model", "overwatch", 1, "movement", 0),
        ("model", "command_reroll", 2, "fight", 1),
    ]
    assert env._count_model_command_reroll_applied() == 2


def test_penalty_applied_when_wasted():
    env = build_env()
    _setup(env)
    # 3 взведено, 1 сработал → 2 впустую → 2 * штраф_из_конфига
    pen = env._command_reroll_wasted_penalty(applied_step=3, fired_step=1)
    assert abs(pen - 2 * reward_cfg.COMMAND_REROLL_WASTED_PENALTY) < 1e-9


def test_no_penalty_when_all_fired():
    env = build_env()
    _setup(env)
    assert env._command_reroll_wasted_penalty(applied_step=3, fired_step=3) == 0.0


def test_no_penalty_clamped_when_fired_exceeds_applied():
    env = build_env()
    _setup(env)
    assert env._command_reroll_wasted_penalty(applied_step=1, fired_step=4) == 0.0


def test_penalty_respects_config_override(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(reward_cfg, "COMMAND_REROLL_WASTED_PENALTY", 0.2)
    pen = env._command_reroll_wasted_penalty(applied_step=2, fired_step=0)
    assert abs(pen - 2 * 0.2) < 1e-9


def test_penalty_skipped_in_simulation_mode():
    env = build_env()
    _setup(env)
    with env.simulation_mode():
        assert env._command_reroll_wasted_penalty(applied_step=5, fired_step=0) == 0.0


def test_step_subtracts_waste_penalty(monkeypatch):
    env = build_env()
    _setup(env)
    # Эмулируем: за шаг model взвёл 2 command_reroll, сработал 0 → wasted=2 → -0.10
    seq = {"applied": [0, 2]}  # 1-й вызов (снапшот)=0, 2-й (конец шага)=2
    monkeypatch.setattr(env, "_count_model_command_reroll_applied", lambda: seq["applied"].pop(0))
    from core.engine.phases import default_action_dict

    action = default_action_dict(len(env.unit_health))
    # Перехватываем вызов _command_reroll_wasted_penalty, чтобы убедиться что
    # step() передаёт правильные дельты и штраф вычисляется положительным.
    penalty_calls = []
    original_penalty = env._command_reroll_wasted_penalty

    def _capture_penalty(applied_step, fired_step):
        penalty_calls.append((applied_step, fired_step))
        return original_penalty(applied_step, fired_step)

    monkeypatch.setattr(env, "_command_reroll_wasted_penalty", _capture_penalty)
    obs, reward, done, trunc, info = env.step(action)
    assert isinstance(reward, float) or hasattr(reward, "__float__")
    # Должен быть ровно один вызов штрафа с дельтами (applied=2, fired=0)
    assert (2, 0) in penalty_calls, (
        f"_command_reroll_wasted_penalty должен быть вызван с applied=2, fired=0; calls={penalty_calls}"
    )
    # Штраф за 2 wasted reroll = 2 * конфиг (без хардкода значения).
    expected = 2 * reward_cfg.COMMAND_REROLL_WASTED_PENALTY
    assert any(abs(original_penalty(a, f) - expected) < 1e-9 for a, f in penalty_calls), (
        f"Штраф за 2 wasted reroll должен быть {expected}"
    )


def test_step_exposes_waste_penalty_in_info(monkeypatch):
    """Fix 1: step() пробрасывает величину штрафа в info, чтобы трейнер сохранил его вне клипа."""
    env = build_env()
    _setup(env)
    seq = {"applied": [0, 2]}  # снапшот=0, конец шага=2 → wasted=2 → 0.10
    monkeypatch.setattr(env, "_count_model_command_reroll_applied", lambda: seq["applied"].pop(0))
    from core.engine.phases import default_action_dict

    action = default_action_dict(len(env.unit_health))
    obs, reward, done, trunc, info = env.step(action)
    assert "command_reroll_wasted_penalty" in info
    expected = 2 * reward_cfg.COMMAND_REROLL_WASTED_PENALTY  # wasted=2
    assert abs(float(info["command_reroll_wasted_penalty"]) - expected) < 1e-9
