# tests/gui/test_heur_metrics_dict_property.py
"""Контракт: GUIController выставляет heuristicMetricsDict как QVariantMap с нужными ключами."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestHeuristicMetricsDictProperty(unittest.TestCase):
    def _make_metrics_json(self, tmp_dir: str) -> str:
        data = {
            "run_id": "test_run",
            "updated_at": "2026-06-12T10:00:00",
            "train_heur_winrate": 0.503,
            "train_draw_rate": 0.012,
            "train_total_games": 100,
            "invalid_rate_total": 0.0,
            "avg_risk": 0.42,
            "avg_cover": 0.05,
            "charge_success_rate": 0.88,
            "shoot_overkill_rate": 0.01,
            "fallback_rate": 0.00,
            "style_entropy_norm": 0.889,
            "mode_usage": {"kite": 30, "hold": 50, "commit": 20},
            "role_usage": {"ranged": 80, "hybrid": 0, "melee": 20},
        }
        path = os.path.join(tmp_dir, "heur_metrics_latest.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def test_load_builds_flat_dict(self):
        import app.gui_qt.main as m_mod

        # GUIController — QObject, object.__new__ не работает.
        # Используем простой stub с нужными атрибутами и вызываем метод напрямую.
        class _FakeSignal:
            def emit(self):
                pass

        class _Stub:
            pass

        with tempfile.TemporaryDirectory() as tmp:
            self._make_metrics_json(tmp)
            orig = m_mod.ARTIFACTS_METRICS_DIR
            try:
                m_mod.ARTIFACTS_METRICS_DIR = Path(tmp)
                ctrl = _Stub()
                ctrl._heuristic_metrics = {}
                ctrl._heuristic_metrics_text = ""
                ctrl._heuristic_metrics_dict = {}
                ctrl.heuristicMetricsChanged = _FakeSignal()
                ctrl.heuristicMetricsDictChanged = _FakeSignal()
                m_mod.GUIController._load_latest_heuristic_metrics(ctrl)
                d = ctrl._heuristic_metrics_dict
                self.assertAlmostEqual(d["winrate"], 0.503, places=3)
                self.assertAlmostEqual(d["draw_rate"], 0.012, places=3)
                self.assertAlmostEqual(d["entropy"], 0.889, places=3)
                self.assertEqual(d["mode_kite"], 30)
                self.assertEqual(d["mode_hold"], 50)
                self.assertIn("run_id", d)
            finally:
                m_mod.ARTIFACTS_METRICS_DIR = orig


if __name__ == "__main__":
    unittest.main()
