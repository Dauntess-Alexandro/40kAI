import unittest
from pathlib import Path


class TestMatchmakerCompatibility(unittest.TestCase):
    def test_matchmaker_uses_contract_validation(self):
        source = Path("core/engine/matchmaker.py").read_text(encoding="utf-8")
        self.assertIn("compatible_contracts", source)
        self.assertIn("def choose_opponent(", source)
        self.assertIn("mirror", source)
        self.assertIn("cross_faction", source)
        self.assertIn("league", source)


if __name__ == "__main__":
    unittest.main()


