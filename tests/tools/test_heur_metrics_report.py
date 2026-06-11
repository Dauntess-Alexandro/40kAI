# tests/tools/test_heur_metrics_report.py
import unittest

from tools.heur_metrics_report import outcomes_by_profile


class TestOutcomesByProfile(unittest.TestCase):
    def test_counts_wins_draws_per_profile(self):
        records = [
            {"profile": "turtle", "winner": "enemy", "end_reason": "wipeout_model"},
            {"profile": "turtle", "winner": "model", "end_reason": "wipeout_enemy"},
            {"profile": "turtle", "winner": "", "end_reason": "turn_limit"},
            {"profile": "aggressor", "winner": "enemy", "end_reason": "wipeout_model"},
        ]
        out = outcomes_by_profile(records)
        self.assertEqual(out["turtle"]["games"], 3)
        self.assertEqual(out["turtle"]["draws"], 1)
        self.assertEqual(out["turtle"]["heur_wins"], 1)
        self.assertEqual(out["aggressor"]["games"], 1)
        self.assertEqual(out["aggressor"]["heur_wins"], 1)
        self.assertEqual(out["aggressor"]["draws"], 0)

    def test_draw_when_winner_not_model_or_enemy(self):
        records = [{"profile": "kiter", "winner": "draw", "end_reason": "turn_limit"}]
        out = outcomes_by_profile(records)
        self.assertEqual(out["kiter"]["draws"], 1)

    def test_empty(self):
        self.assertEqual(outcomes_by_profile([]), {})


if __name__ == "__main__":
    unittest.main()
