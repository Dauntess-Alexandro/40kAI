import unittest
from pathlib import Path


class TestStateRefreshRegression(unittest.TestCase):
    def test_health_update_flushes_state_snapshot(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _flush_state_snapshot", source)
        self.assertIn('self._flush_state_snapshot(reason=f"health_update:{side}:{idx}")', source)

    def test_state_watcher_uses_mtime_ns_and_size(self):
        source = Path("viewer/state.py").read_text(encoding="utf-8")
        self.assertIn("mtime_ns: int = 0", source)
        self.assertIn("size: int = -1", source)
        self.assertIn("st_mtime_ns", source)
        self.assertIn("st_size", source)


if __name__ == "__main__":
    unittest.main()
