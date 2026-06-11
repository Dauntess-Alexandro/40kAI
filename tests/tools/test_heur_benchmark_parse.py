# tests/tools/test_heur_benchmark_parse.py
import math
import unittest

from tools.heur_benchmark import parse_eval_output, summarize


class TestHeurBenchmarkParse(unittest.TestCase):
    def test_parse_win_counts_from_eval_detail_line(self):
        text = "blah\n[DETAIL] Итог серии P1/P2/Draw: 7/2/1\nmore\n"
        res = parse_eval_output(text)
        self.assertEqual(res["p1_wins"], 7)
        self.assertEqual(res["p2_wins"], 2)
        self.assertEqual(res["draws"], 1)

    def test_parse_mode_distribution_from_heur_move_lines(self):
        text = (
            "[ENEMY][HEUR][MOVE] unit=11 target=21 mode=kite enemy_role=ranged\n"
            "[ENEMY][HEUR][MOVE] unit=12 target=21 mode=commit enemy_role=melee\n"
            "[ENEMY][HEUR][MOVE] unit=13 target=22 mode=kite enemy_role=ranged\n"
            "[ENEMY][HEUR][MOVE] unit=14 target=22 mode=hold enemy_role=hybrid\n"
        )
        res = parse_eval_output(text)
        self.assertEqual(res["mode_counts"], {"kite": 2, "commit": 1, "hold": 1})

    def test_summarize_computes_winrate_and_style_entropy(self):
        parsed = {"p1_wins": 6, "p2_wins": 3, "draws": 1,
                  "mode_counts": {"kite": 2, "commit": 2, "hold": 2}}
        s = summarize(parsed, heuristic_side="p2")
        self.assertAlmostEqual(s["heur_winrate_all"], 0.3, places=6)
        self.assertAlmostEqual(s["heur_winrate_decisive"], 3 / 9, places=6)
        # три равновероятных режима => энтропия = log2(3) (нормируем по log2(3) => 1.0)
        self.assertAlmostEqual(s["style_entropy_norm"], 1.0, places=6)

    def test_summarize_entropy_zero_when_single_mode(self):
        parsed = {"p1_wins": 5, "p2_wins": 5, "draws": 0,
                  "mode_counts": {"kite": 10}}
        s = summarize(parsed, heuristic_side="p2")
        self.assertAlmostEqual(s["style_entropy_norm"], 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
