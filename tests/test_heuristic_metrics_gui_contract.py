import unittest
from pathlib import Path


class TestHeuristicMetricsGuiContract(unittest.TestCase):
    def test_train_exports_heur_metrics_snapshot(self):
        source = Path("train.py").read_text(encoding="utf-8")
        self.assertIn("def save_heuristic_metrics_snapshot(", source)
        self.assertIn("heur_metrics_latest.json", source)
        self.assertIn("[HEUR][METRICS] saved=", source)

    def test_gui_has_heuristic_metrics_tab_and_property(self):
        main_py = Path("gui_qt/main.py").read_text(encoding="utf-8")
        qml = Path("gui_qt/qml/Main.qml").read_text(encoding="utf-8")
        self.assertIn("heuristicMetricsChanged", main_py)
        self.assertIn("def heuristicMetricsText", main_py)
        self.assertIn("def _load_latest_heuristic_metrics(", main_py)
        self.assertIn("Метрики эвристики", qml)
        self.assertIn("controller.heuristicMetricsText", qml)


if __name__ == "__main__":
    unittest.main()
