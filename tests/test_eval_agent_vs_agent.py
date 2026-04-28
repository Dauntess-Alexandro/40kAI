import unittest
from pathlib import Path


class TestEvalAgentVsAgent(unittest.TestCase):
    def test_eval_supports_agent_ids(self):
        source = Path("eval.py").read_text(encoding="utf-8")
        self.assertIn("--learner-agent-id", source)
        self.assertIn("--opponent-agent-id", source)
        self.assertIn("compatible_contracts", source)

    def test_eval_emits_summary_v2_fields(self):
        source = Path("eval.py").read_text(encoding="utf-8")
        self.assertIn("[SUMMARY_V2]", source)
        self.assertIn("p1_wins=", source)
        self.assertIn("p2_wins=", source)
        self.assertIn("avg_vp_diff_p1_minus_p2=", source)
        self.assertIn("turn_limit_count=", source)


if __name__ == "__main__":
    unittest.main()

