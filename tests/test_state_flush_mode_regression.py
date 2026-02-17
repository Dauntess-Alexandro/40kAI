import unittest
from pathlib import Path


class TestStateFlushModeRegression(unittest.TestCase):
    def test_flush_has_mode_and_throttle_controls(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('os.getenv("STATE_FLUSH_MODE", "auto")', source)
        self.assertIn('os.getenv("STATE_FLUSH_MIN_INTERVAL_MS", "120")', source)
        self.assertIn('self._state_flush_last_ts', source)
        self.assertIn('self._state_flush_pending', source)

    def test_update_board_forces_flush(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('self._flush_state_snapshot(reason="updateBoard", force=True)', source)


if __name__ == "__main__":
    unittest.main()
