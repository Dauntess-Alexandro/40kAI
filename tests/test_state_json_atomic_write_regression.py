import unittest
from pathlib import Path


class TestStateJsonAtomicWriteRegression(unittest.TestCase):
    def test_state_export_uses_atomic_replace(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn("import tempfile", source)
        self.assertIn("NamedTemporaryFile", source)
        self.assertIn("os.replace(temp_path, state_path)", source)

    def test_state_watcher_handles_partial_json(self):
        source = Path("viewer/state.py").read_text(encoding="utf-8")
        self.assertIn("except json.JSONDecodeError", source)
        self.assertIn("time.sleep(0.02)", source)


if __name__ == "__main__":
    unittest.main()
