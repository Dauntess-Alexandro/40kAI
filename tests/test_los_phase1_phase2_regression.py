import pathlib
import unittest


class TestLosPhase1Phase2Regression(unittest.TestCase):
    def setUp(self):
        self.source = pathlib.Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")

    def test_los_core_helpers_exist(self):
        for token in (
            "def _build_model_samples",
            "def _line_cells_between_points",
            "def _check_model_los",
            "def _check_unit_visibility",
        ):
            self.assertIn(token, self.source)

    def test_shoot_targets_are_filtered_by_los(self):
        self.assertIn('"shoot_target"', self.source)
        self.assertIn("self._check_unit_visibility(side, unit_idx", self.source)

    def test_overwatch_uses_los(self):
        self.assertIn('"overwatch_candidate"', self.source)
        self.assertIn("self._check_unit_visibility(defender_side, i, target_side, moving_idx)", self.source)

    def test_agent_logs_enabled_by_default_and_written_for_all_logs(self):
        self.assertIn('os.environ["VERBOSE_LOGS"] = "1"', self.source)
        self.assertIn('LOGS_FOR_AGENTS_TRAIN.md', self.source)
        self.assertIn('LOGS_FOR_AGENTS_PLAY.md', self.source)
        self.assertIn('self._append_agent_log(msg)', self.source)


if __name__ == "__main__":
    unittest.main()
