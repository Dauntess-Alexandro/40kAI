import unittest
from pathlib import Path


class TestStateFlushTrainingPerfRegression(unittest.TestCase):
    def test_force_flush_in_train_requires_opt_in_env(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('os.getenv("STATE_FLUSH_ALLOW_FORCE_IN_TRAIN", "0")', source)

    def test_update_board_fallback_write_is_gui_only(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('if bool(getattr(self, "playType", False)):', source)
        self.assertIn('write_state_json(self)', source)


if __name__ == "__main__":
    unittest.main()
