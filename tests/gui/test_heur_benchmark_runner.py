# tests/gui/test_heur_benchmark_runner.py
"""Контракт HeurBenchmarkRunner: signals, isRunning, stop."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestParseBenchmarkStdout(unittest.TestCase):
    def test_parses_json_block(self):
        from app.gui_qt.heur_benchmark_runner import _parse_benchmark_stdout
        stdout = (
            "[HEUR-BENCH] games=30 winrate_all=0.503\n"
            '{"games": 30, "heur_winrate_all": 0.503, "draw_rate": 0.02, '
            '"style_entropy_norm": 0.891, "heur_winrate": 0.503}\n'
        )
        result = _parse_benchmark_stdout(stdout)
        self.assertAlmostEqual(result["heur_winrate_all"], 0.503, places=3)
        self.assertAlmostEqual(result["style_entropy_norm"], 0.891, places=3)

    def test_fallback_to_heur_bench_line(self):
        from app.gui_qt.heur_benchmark_runner import _parse_benchmark_stdout
        stdout = "[HEUR-BENCH] games=20 winrate_all=0.480 draw_rate=0.015 style_entropy_norm=0.870\n"
        result = _parse_benchmark_stdout(stdout)
        self.assertAlmostEqual(result.get("winrate_all", result.get("heur_winrate_all", 0)), 0.480, places=2)

    def test_empty_returns_empty_dict(self):
        from app.gui_qt.heur_benchmark_runner import _parse_benchmark_stdout
        self.assertEqual(_parse_benchmark_stdout(""), {})


class TestHeurBenchmarkRunnerContract(unittest.TestCase):
    def test_module_importable(self):
        from app.gui_qt import heur_benchmark_runner  # noqa: F401

    def test_runner_has_required_signals(self):
        src = Path("app/gui_qt/heur_benchmark_runner.py").read_text(encoding="utf-8")
        self.assertIn("benchmarkStarted", src)
        self.assertIn("benchmarkFinished", src)
        self.assertIn("benchmarkFailed", src)
        self.assertIn("isRunningChanged", src)

    def test_runner_has_run_and_stop_slots(self):
        src = Path("app/gui_qt/heur_benchmark_runner.py").read_text(encoding="utf-8")
        self.assertIn("def run(", src)
        self.assertIn("def stop(", src)

    def test_runner_has_is_running_property(self):
        src = Path("app/gui_qt/heur_benchmark_runner.py").read_text(encoding="utf-8")
        self.assertIn("isRunning", src)
        self.assertIn("lastResult", src)


if __name__ == "__main__":
    unittest.main()
