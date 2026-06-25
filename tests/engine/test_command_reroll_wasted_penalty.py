"""Back-compat поле penalty для command_reroll после реактивного гейта.

armed-not-fired теперь не тратит CP, поэтому command_reroll_wasted_penalty всегда 0.0.
"""

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


def test_wasted_penalty_zero_when_applied_exceeds_fired():
    env = build_env()
    _setup(env)
    # 3 взведено, 1 сработал → 2 armed-not-fired, но CP не потрачен → штрафа нет.
    pen = env._command_reroll_wasted_penalty(applied_step=3, fired_step=1)
    assert pen == 0.0


def test_wasted_penalty_zero_when_all_fired():
    env = build_env()
    _setup(env)
    assert env._command_reroll_wasted_penalty(applied_step=3, fired_step=3) == 0.0


def test_wasted_penalty_zero_when_fired_exceeds_applied():
    env = build_env()
    _setup(env)
    assert env._command_reroll_wasted_penalty(applied_step=1, fired_step=4) == 0.0


def test_wasted_penalty_ignores_config_override(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(reward_cfg, "COMMAND_REROLL_WASTED_PENALTY", 0.2)
    pen = env._command_reroll_wasted_penalty(applied_step=2, fired_step=0)
    assert pen == 0.0


def test_wasted_penalty_zero_in_simulation_mode():
    env = build_env()
    _setup(env)
    with env.simulation_mode():
        assert env._command_reroll_wasted_penalty(applied_step=5, fired_step=0) == 0.0


def test_step_passes_correct_deltas_to_neutralized_penalty(monkeypatch):
    env = build_env()
    _setup(env)
    # Эмулируем: за шаг model взвёл 2 command_reroll, сработал 0 → armed-not-fired=2.
    seq = {"applied": [0, 2]}  # 1-й вызов (снапшот)=0, 2-й (конец шага)=2
    monkeypatch.setattr(env, "_count_model_command_reroll_applied", lambda: seq["applied"].pop(0))
    from core.engine.phases import default_action_dict

    action = default_action_dict(len(env.unit_health))
    # Перехватываем вызов _command_reroll_wasted_penalty, чтобы убедиться что
    # step() продолжает передавать правильные дельты, но штраф нейтрализован.
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
    assert all(original_penalty(a, f) == 0.0 for a, f in penalty_calls)


def test_step_exposes_waste_penalty_in_info(monkeypatch):
    """step() сохраняет back-compat поле info, но penalty всегда 0.0."""
    env = build_env()
    _setup(env)
    seq = {"applied": [0, 2]}  # снапшот=0, конец шага=2 → armed-not-fired=2 → 0.0
    monkeypatch.setattr(env, "_count_model_command_reroll_applied", lambda: seq["applied"].pop(0))
    from core.engine.phases import default_action_dict

    action = default_action_dict(len(env.unit_health))
    obs, reward, done, trunc, info = env.step(action)
    assert "command_reroll_wasted_penalty" in info
    assert float(info["command_reroll_wasted_penalty"]) == 0.0
