import unittest
from pathlib import Path


class TestEvalAgentVsAgent(unittest.TestCase):
    def test_eval_supports_agent_ids(self):
        source = Path("eval.py").read_text(encoding="utf-8")
        self.assertIn("--learner-agent-id", source)
        self.assertIn("--opponent-agent-id", source)
        self.assertIn("compatible_contracts", source)


if __name__ == "__main__":
    unittest.main()

