# tests/tools/test_heur_learner_side.py
"""Калибровка/бенчмарк против learner на любой стороне (P1 или P2).

Сторона эвристики — противоположна стороне learner. Сторона learner
выводится из выбранного агента (или явного override), иначе P1 по умолчанию.
"""
import unittest

import tools.heur_calibrate as hc
from tools.heur_benchmark import heuristic_side_for_learner, summarize


class TestHeuristicSideForLearner(unittest.TestCase):
    def test_learner_p1_means_heuristic_p2(self):
        self.assertEqual(heuristic_side_for_learner("P1"), "p2")

    def test_learner_p2_means_heuristic_p1(self):
        self.assertEqual(heuristic_side_for_learner("P2"), "p1")

    def test_case_insensitive_and_default_p1(self):
        self.assertEqual(heuristic_side_for_learner("p2"), "p1")
        self.assertEqual(heuristic_side_for_learner(""), "p2")
        self.assertEqual(heuristic_side_for_learner("bogus"), "p2")

    def test_summarize_uses_p1_wins_when_heuristic_is_p1(self):
        parsed = {"p1_wins": 6, "p2_wins": 3, "draws": 1, "mode_counts": {"kite": 1}}
        s = summarize(parsed, heuristic_side=heuristic_side_for_learner("P2"))
        # эвристика на P1 → её победы = p1_wins = 6 из 10
        self.assertAlmostEqual(s["heur_winrate_all"], 0.6, places=6)


class TestResolveLearnerSide(unittest.TestCase):
    def test_explicit_side_wins(self):
        self.assertEqual(hc.resolve_learner_side("any_agent", "P2"), "P2")
        self.assertEqual(hc.resolve_learner_side("any_agent", "p1"), "P1")

    def test_side_derived_from_agent_registry(self):
        original = hc.collect_registered_agents_meta
        try:
            hc.collect_registered_agents_meta = lambda: [
                {"agent_id": "AG_P2", "side": "P2"},
                {"agent_id": "AG_P1", "side": "P1"},
            ]
            self.assertEqual(hc.resolve_learner_side("AG_P2", ""), "P2")
            self.assertEqual(hc.resolve_learner_side("AG_P1", ""), "P1")
        finally:
            hc.collect_registered_agents_meta = original

    def test_default_p1_when_unknown(self):
        original = hc.collect_registered_agents_meta
        try:
            hc.collect_registered_agents_meta = lambda: []
            self.assertEqual(hc.resolve_learner_side("", ""), "P1")
            self.assertEqual(hc.resolve_learner_side("not_in_registry", ""), "P1")
        finally:
            hc.collect_registered_agents_meta = original


if __name__ == "__main__":
    unittest.main()
