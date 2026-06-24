"""Fix 1: штраф за впустую-command_reroll должен переживать per-step клиппинг reward.

Раньше полный reward шага (с уже вычтенным штрафом) клиппился в [-1,+1]; на «полезных»
шагах (стрельба/чардж/бой) reward и так >= 1, и -0.05 штрафа исчезал при клипе → сигнал
не доходил до агента. Helper клипует игровую часть, сохраняя штраф вне клипа.
"""

import train


def test_penalty_survives_clip_on_positive_step():
    # env вернул reward=1.15 (игровая часть 1.20 минус штраф 0.05); клип [-1,1].
    # base = 1.15 + 0.05 = 1.20 → clip → 1.0 → -0.05 = 0.95 (штраф виден).
    r = train.clip_reward_preserving_penalty(1.15, 0.05, True, -1.0, 1.0)
    assert abs(r - 0.95) < 1e-9


def test_no_penalty_matches_plain_clip():
    # Без штрафа поведение идентично обычному клипу.
    r = train.clip_reward_preserving_penalty(1.15, 0.0, True, -1.0, 1.0)
    assert abs(r - 1.0) < 1e-9


def test_disabled_clip_returns_reward_unchanged():
    r = train.clip_reward_preserving_penalty(1.15, 0.05, False, -1.0, 1.0)
    assert abs(r - 1.15) < 1e-9


def test_within_range_no_double_penalty():
    # Игровая часть 0.5, штраф 0.05 → env reward 0.45; клип не трогает → результат 0.45.
    r = train.clip_reward_preserving_penalty(0.45, 0.05, True, -1.0, 1.0)
    assert abs(r - 0.45) < 1e-9
