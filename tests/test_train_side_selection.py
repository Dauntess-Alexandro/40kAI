import unittest
from pathlib import Path


class TestTrainSideSelection(unittest.TestCase):
    def test_train_has_side_and_faction_env(self):
        source = Path("train.py").read_text(encoding="utf-8")
        self.assertIn('LEARNER_SIDE', source)
        self.assertIn('LEARNER_FACTION', source)
        self.assertIn('save_agent_artifact(', source)


if __name__ == "__main__":
    unittest.main()

