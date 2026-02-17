import unittest
from pathlib import Path


class TestStateExportRegression(unittest.TestCase):
    def test_state_export_contains_model_metadata_fields(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")

        self.assertIn('"alive_models"', source)
        self.assertIn('"anchor_x"', source)
        self.assertIn('"anchor_y"', source)
        self.assertIn('_alive_models_from_pool("enemy", idx)', source)
        self.assertIn('_alive_models_from_pool("model", idx)', source)


if __name__ == "__main__":
    unittest.main()
