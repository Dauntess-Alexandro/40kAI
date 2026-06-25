"""Тесты для episode_stratagem_summary_line — per-episode сводка стратагем из env.

wasted считается арифметикой: max(0, applied['command_reroll'] − fired).
После реактивного гейта это диагностика armed-not-fired, CP не потрачен.
"""
from __future__ import annotations

import unittest
from types import SimpleNamespace

from core.telemetry.stratagem_trace import episode_stratagem_summary_line


class TestEpisodeStratagemSummaryLine(unittest.TestCase):
    """episode_stratagem_summary_line: сборка строки сводки из env-журнала + счётчиков."""

    def test_summary_line_counts_journal_and_counters(self) -> None:
        """Несколько записей разных id + ненулевые счётчики реролла → корректная строка.

        command_reroll applied=2, fired=3 → wasted=max(0, 2−3)=0 (кламп).
        """
        env = SimpleNamespace(
            stratagem_used=[
                ("model", "insane_bravery", 1, "command", 0),
                ("enemy", "insane_bravery", 1, "command", 2),
                ("model", "command_reroll", 2, "shoot", 1),
                ("model", "command_reroll", 2, "fight", 0),
            ],
            _cmd_reroll_fired=3,
        )
        line = episode_stratagem_summary_line(env, ep_label=42, tag="TRAIN")
        assert line is not None, "Ожидалась строка, получен None"
        # Тег и маркер
        assert "[TRAIN][STRATAGEM_SUMMARY]" in line
        assert "ep=42" in line
        # applied подсчёт: insane_bravery=2, command_reroll=2
        assert "applied_total=4" in line
        assert "'insane_bravery': 2" in line
        assert "'command_reroll': 2" in line
        # Счётчики реролла: wasted = max(0, 2 − 3) = 0
        assert "cmd_reroll_fired=3" in line
        assert "cmd_reroll_wasted=0" in line

    def test_wasted_computed_from_applied_minus_fired(self) -> None:
        """applied command_reroll=10, fired=3 → armed-not-fired диагностика=7."""
        env = SimpleNamespace(
            stratagem_used=[("model", "command_reroll", r, "shoot", 0) for r in range(10)],
            _cmd_reroll_fired=3,
        )
        line = episode_stratagem_summary_line(env, ep_label=100, tag="TRAIN")
        assert line is not None
        assert "cmd_reroll_fired=3" in line
        assert "cmd_reroll_wasted=7" in line

    def test_wasted_clamped_to_zero(self) -> None:
        """applied command_reroll=2, fired=5 → wasted=max(0, 2−5)=0 (кламп)."""
        env = SimpleNamespace(
            stratagem_used=[
                ("model", "command_reroll", 1, "shoot", 0),
                ("model", "command_reroll", 2, "fight", 0),
            ],
            _cmd_reroll_fired=5,
        )
        line = episode_stratagem_summary_line(env, ep_label=200, tag="EVAL")
        assert line is not None
        assert "cmd_reroll_fired=5" in line
        assert "cmd_reroll_wasted=0" in line

    def test_summary_line_none_when_empty(self) -> None:
        """Пустой журнал + нулевые счётчики → None (не спамим пустые строки)."""
        env = SimpleNamespace(
            stratagem_used=[],
            _cmd_reroll_fired=0,
        )
        result = episode_stratagem_summary_line(env, ep_label=1, tag="TRAIN")
        assert result is None

    def test_summary_line_none_when_no_attrs(self) -> None:
        """Env без атрибутов stratagem_used/_cmd_reroll_* → None (безопасный fallback)."""
        env = SimpleNamespace()
        result = episode_stratagem_summary_line(env, ep_label=5, tag="TRAIN")
        assert result is None

    def test_summary_line_only_reroll_counters(self) -> None:
        """Нет журнала, но есть ненулевой fired → строка есть (wasted=0)."""
        env = SimpleNamespace(
            stratagem_used=[],
            _cmd_reroll_fired=2,
        )
        line = episode_stratagem_summary_line(env, ep_label=10, tag="TRAIN")
        assert line is not None
        assert "applied={}" in line
        assert "applied_total=0" in line
        assert "cmd_reroll_fired=2" in line
        assert "cmd_reroll_wasted=0" in line

    def test_summary_line_from_payload_dict(self) -> None:
        """Работа с payload-словарём (вместо env) для learner-стороны."""
        payload = {
            "_strat_applied": {"insane_bravery": 2, "command_reroll": 5},
            "_strat_applied_total": 7,
            "_cmd_reroll_fired": 1,
        }
        line = episode_stratagem_summary_line(payload, ep_label=7, tag="TRAIN")
        assert line is not None
        assert "[TRAIN][STRATAGEM_SUMMARY]" in line
        assert "ep=7" in line
        assert "applied_total=7" in line
        assert "cmd_reroll_fired=1" in line
        # cmd_reroll_wasted = armed-not-fired диагностика: max(0, 5 − 1) = 4
        assert "cmd_reroll_wasted=4" in line

    def test_summary_line_from_payload_dict_empty(self) -> None:
        """Payload без стратагемных данных → None."""
        payload: dict = {}
        result = episode_stratagem_summary_line(payload, ep_label=1, tag="TRAIN")
        assert result is None

    def test_summary_line_custom_tag(self) -> None:
        """Кастомный tag корректно попадает в строку."""
        env = SimpleNamespace(
            stratagem_used=[("model", "fire_overwatch", 1, "shoot", 0)],
            _cmd_reroll_fired=0,
        )
        line = episode_stratagem_summary_line(env, ep_label="ep5", tag="EVAL")
        assert line is not None
        assert "[EVAL][STRATAGEM_SUMMARY]" in line
        assert "ep=ep5" in line


if __name__ == "__main__":
    unittest.main()
