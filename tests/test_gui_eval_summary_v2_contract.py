import unittest
from pathlib import Path


class TestGuiEvalSummaryV2Contract(unittest.TestCase):
    def test_gui_parser_supports_summary_v2_and_legacy_fallback(self):
        source = Path("gui_qt/main.py").read_text(encoding="utf-8")
        self.assertIn("[EVAL][SUMMARY_V2]", source)
        self.assertIn("def _format_eval_summary_v2(", source)
        self.assertIn("def _format_eval_summary(", source)

    def test_gui_exposes_eval_result_kpi_properties(self):
        source = Path("gui_qt/main.py").read_text(encoding="utf-8")
        self.assertIn("def evalResultHeadline", source)
        self.assertIn("def evalResultWinrateP1", source)
        self.assertIn("def evalResultWinrateP2", source)
        self.assertIn("def evalResultAvgVpDiff", source)
        self.assertIn("def evalResultTurnLimitRate", source)
        self.assertIn("def evalResultQualityHint", source)


if __name__ == "__main__":
    unittest.main()
