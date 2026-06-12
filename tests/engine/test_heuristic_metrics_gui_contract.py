import unittest
from pathlib import Path


class TestHeuristicMetricsGuiContract(unittest.TestCase):
    def test_train_exports_heur_metrics_snapshot(self):
        source = Path("train.py").read_text(encoding="utf-8")
        self.assertIn("def save_heuristic_metrics_snapshot(", source)
        self.assertIn("heur_metrics_latest.json", source)
        self.assertIn("[HEUR][METRICS] saved=", source)

    def test_gui_has_heuristic_metrics_tab_and_property(self):
        main_py = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
        main_qml = Path("app/gui_qt/qml/Main.qml").read_text(encoding="utf-8")
        # После редизайна вкладка вынесена в отдельный компонент HeurMetricsPanel.
        panel_qml = Path("app/gui_qt/qml/components/HeurMetricsPanel.qml").read_text(encoding="utf-8")
        self.assertIn("heuristicMetricsChanged", main_py)
        self.assertIn("def heuristicMetricsText", main_py)
        self.assertIn("def _load_latest_heuristic_metrics(", main_py)
        # Main.qml монтирует панель метрик эвристики.
        self.assertIn("HeurMetricsPanel", main_qml)
        # Заголовок и привязка данных живут в самой панели.
        self.assertIn("Метрики эвристики", panel_qml)
        self.assertIn("controller.heuristicMetricsDict", panel_qml)


if __name__ == "__main__":
    unittest.main()

