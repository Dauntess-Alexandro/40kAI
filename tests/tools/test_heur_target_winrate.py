# tests/tools/test_heur_target_winrate.py
"""Настраиваемый target_winrate в score/reject/acceptance калибровки.

target=0.50 воспроизводит текущее поведение; 0.65 сдвигает окно; 1.0 (Максимум)
награждает высокий winrate монотонно и снимает верхний winrate-reject.
"""
import unittest

import tools.heur_calibrate as hc


def _m(**kw):
    base = {
        "heur_winrate": 0.50,
        "draw_rate": 0.0,
        "invalid_rate": 0.0,
        "style_entropy_norm": 0.90,
        "hold_ratio": 0.50,
        "fallback_rate": 0.0,
        "actual_games": 10,
    }
    base.update(kw)
    return base


class TestScoreTarget(unittest.TestCase):
    def test_default_target_matches_legacy(self):
        # При target=0.50 формула совпадает со старой (дефолт = 0.50).
        metrics = _m(heur_winrate=0.50, style_entropy_norm=0.90)
        self.assertAlmostEqual(
            hc.score_candidate(metrics),
            hc.score_candidate(metrics, target_winrate=0.50),
            places=9,
        )

    def test_sparring_peaks_near_050(self):
        # Для спарринга winrate=0.50 лучше, чем 0.70.
        s50 = hc.score_candidate(_m(heur_winrate=0.50), target_winrate=0.50)
        s70 = hc.score_candidate(_m(heur_winrate=0.70), target_winrate=0.50)
        self.assertGreater(s50, s70)

    def test_max_mode_monotonic_in_winrate(self):
        # target=1.0: чем больше winrate, тем больше score.
        lo = hc.score_candidate(_m(heur_winrate=0.50), target_winrate=1.0)
        hi = hc.score_candidate(_m(heur_winrate=0.90), target_winrate=1.0)
        self.assertGreater(hi, lo)


class TestRejectTarget(unittest.TestCase):
    def test_sparring_rejects_high_winrate(self):
        reasons = hc.reject_reasons(_m(heur_winrate=0.70), requested_games=10, target_winrate=0.50)
        self.assertTrue(any("heur_winrate >" in r for r in reasons))

    def test_hard_allows_065_rejects_above_071(self):
        ok = hc.reject_reasons(_m(heur_winrate=0.64), requested_games=10, target_winrate=0.65)
        self.assertFalse(any("heur_winrate >" in r for r in ok))
        bad = hc.reject_reasons(_m(heur_winrate=0.80), requested_games=10, target_winrate=0.65)
        self.assertTrue(any("heur_winrate >" in r for r in bad))

    def test_max_mode_no_upper_winrate_reject(self):
        reasons = hc.reject_reasons(_m(heur_winrate=0.95), requested_games=10, target_winrate=1.0)
        self.assertFalse(any("heur_winrate >" in r for r in reasons))


class TestAcceptanceTarget(unittest.TestCase):
    def test_window_shifts_with_target(self):
        # winrate 0.65 принимается при target=0.65, но не при target=0.50.
        acc_hard = hc.acceptance_reasons(_m(heur_winrate=0.65, score=1.0), baseline_score=0.0, target_winrate=0.65)
        self.assertFalse(any("outside" in r for r in acc_hard))
        acc_spar = hc.acceptance_reasons(_m(heur_winrate=0.65, score=1.0), baseline_score=0.0, target_winrate=0.50)
        self.assertTrue(any("outside" in r for r in acc_spar))

    def test_max_mode_no_winrate_window(self):
        acc = hc.acceptance_reasons(_m(heur_winrate=0.75, score=1.0), baseline_score=0.0, target_winrate=1.0)
        self.assertFalse(any("outside" in r for r in acc))


if __name__ == "__main__":
    unittest.main()
