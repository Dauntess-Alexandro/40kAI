"""Контракт HeurMetricsPanel.qml: структура, API, подключение к runners."""
import unittest
from pathlib import Path

QML_PATH = Path("app/gui_qt/qml/components/HeurMetricsPanel.qml")


class TestHeurMetricsPanelContract(unittest.TestCase):
    def setUp(self):
        self.assertTrue(QML_PATH.exists(), f"Нет компонента: {QML_PATH}")
        self.src = QML_PATH.read_text(encoding="utf-8")

    def test_has_three_subtabs(self):
        self.assertIn("Сводка", self.src)
        self.assertIn("Бенчмарк", self.src)
        self.assertIn("Калибровка", self.src)

    def test_uses_stacklayout(self):
        self.assertIn("StackLayout", self.src)

    def test_references_heur_bench_runner(self):
        self.assertIn("heurBenchRunner", self.src)

    def test_references_heur_cal_runner(self):
        self.assertIn("heurCalRunner", self.src)

    def test_references_heuristic_metrics_dict(self):
        self.assertIn("heuristicMetricsDict", self.src)

    def test_benchmark_has_run_and_stop(self):
        self.assertIn("heurBenchRunner.run(", self.src)
        self.assertIn("heurBenchRunner.stop(", self.src)

    def test_calibration_has_run_stop_apply(self):
        self.assertIn("heurCalRunner.run(", self.src)
        self.assertIn("heurCalRunner.stop(", self.src)
        self.assertIn("heurCalRunner.applyPatch(", self.src)

    def test_candidate_list_model(self):
        self.assertIn("ListModel", self.src)
        self.assertIn("candidatesModel", self.src)

    def test_patch_block_visible_condition(self):
        self.assertIn("bestCandidateIdx", self.src)

    def test_stat_cards_winrate_entropy_draws(self):
        for metric in ["winrate", "entropy", "draw_rate"]:
            self.assertIn(metric, self.src)

    def test_target_mode_presets_and_custom(self):
        # Режим цели: пресеты + ручной target winrate.
        self.assertIn("targetWinrate", self.src)
        self.assertIn("Спарринг", self.src)
        self.assertIn("Хард", self.src)
        self.assertIn("Максимум", self.src)
        self.assertIn("calTargetInput", self.src)

    def test_run_passes_target_winrate(self):
        # run() вызывается с targetWinrate шестым/седьмым аргументом.
        self.assertIn("heurPanel.targetWinrate)", self.src)

    def test_leaderboard_live_sort(self):
        # Лидерборд с живой сортировкой по score и рангом/медалью.
        self.assertIn("_rebuildLeaderboard", self.src)
        self.assertIn("scoreNum", self.src)
        self.assertIn("model.rank", self.src)


if __name__ == "__main__":
    unittest.main()
