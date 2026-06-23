"""Тесты для episode_stratagem_summary_line — per-episode сводка стратагем из env."""
from __future__ import annotations

import unittest
from types import SimpleNamespace

from core.telemetry.stratagem_trace import episode_stratagem_summary_line


class TestEpisodeStratagemSummaryLine(unittest.TestCase):
    """episode_stratagem_summary_line: сборка строки сводки из env-журнала + счётчиков."""

    def test_summary_line_counts_journal_and_counters(self) -> None:
        """Несколько записей разных id + ненулевые счётчики реролла → корректная строка."""
        env = SimpleNamespace(
            stratagem_used=[
                ("model", "insane_bravery", 1, "command", 0),
                ("enemy", "insane_bravery", 1, "command", 2),
                ("model", "overwatch", 2, "shoot", 1),
                ("model", "insane_bravery", 2, "command", 0),
            ],
            _cmd_reroll_fired=3,
            _cmd_reroll_wasted=1,
        )
        line = episode_stratagem_summary_line(env, ep_label=42, tag="TRAIN")
        assert line is not None, "Ожидалась строка, получен None"
        # Тег и маркер
        assert "[TRAIN][STRATAGEM_SUMMARY]" in line
        assert "ep=42" in line
        # applied подсчёт: insane_bravery=3 (2 model + 1 enemy), overwatch=1
        assert "applied_total=4" in line
        assert "'insane_bravery': 3" in line
        assert "'overwatch': 1" in line
        # Счётчики реролла
        assert "cmd_reroll_fired=3" in line
        assert "cmd_reroll_wasted=1" in line

    def test_summary_line_none_when_empty(self) -> None:
        """Пустой журнал + нулевые счётчики → None (не спамим пустые строки)."""
        env = SimpleNamespace(
            stratagem_used=[],
            _cmd_reroll_fired=0,
            _cmd_reroll_wasted=0,
        )
        result = episode_stratagem_summary_line(env, ep_label=1, tag="TRAIN")
        assert result is None

    def test_summary_line_none_when_no_attrs(self) -> None:
        """Env без атрибутов stratagem_used/_cmd_reroll_* → None (безопасный fallback)."""
        env = SimpleNamespace()
        result = episode_stratagem_summary_line(env, ep_label=5, tag="TRAIN")
        assert result is None

    def test_summary_line_only_reroll_counters(self) -> None:
        """Нет журнала, но есть ненулевые реролл-счётчики → строка есть."""
        env = SimpleNamespace(
            stratagem_used=[],
            _cmd_reroll_fired=2,
            _cmd_reroll_wasted=0,
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
            "_strat_applied": {"insane_bravery": 2, "overwatch": 1},
            "_strat_applied_total": 3,
            "_cmd_reroll_fired": 1,
            "_cmd_reroll_wasted": 0,
        }
        line = episode_stratagem_summary_line(payload, ep_label=7, tag="TRAIN")
        assert line is not None
        assert "[TRAIN][STRATAGEM_SUMMARY]" in line
        assert "ep=7" in line
        assert "applied_total=3" in line
        assert "cmd_reroll_fired=1" in line
        assert "cmd_reroll_wasted=0" in line

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
            _cmd_reroll_wasted=0,
        )
        line = episode_stratagem_summary_line(env, ep_label="ep5", tag="EVAL")
        assert line is not None
        assert "[EVAL][STRATAGEM_SUMMARY]" in line
        assert "ep=ep5" in line


if __name__ == "__main__":
    unittest.main()
