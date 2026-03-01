import pathlib
import unittest


class TestLosPhase3Phase5Regression(unittest.TestCase):
    def setUp(self):
        self.env_source = pathlib.Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.state_export_source = pathlib.Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")

    def test_phase3_has_unified_los_decision_logs(self):
        self.assertIn("def _log_los_decision", self.env_source)
        self.assertIn("[LOS:", self.env_source)
        self.assertIn("unit_fully_visible", self.env_source)

    def test_phase4_exports_los_snapshot_to_state_payload(self):
        self.assertIn('"los": los if isinstance(los, dict) else None', self.state_export_source)
        self.assertIn("_build_unit_los_snapshot(\"enemy\", idx)", self.state_export_source)
        self.assertIn("_build_unit_los_snapshot(\"model\", idx)", self.state_export_source)

    def test_phase5_uses_tunable_sampling_env(self):
        self.assertIn('LOS_SAMPLE_COUNT', self.env_source)
        self.assertIn('LOS_INCLUDE_DIAGONALS', self.env_source)
        self.assertIn('LOS_FRONT_ARC_SAMPLES', self.env_source)

    def test_phase5_unit_visibility_aggregates_over_model_results(self):
        self.assertIn("model_results = []", self.env_source)
        self.assertIn("summary = evaluate_unit_visibility(tuple(model_results))", self.env_source)


if __name__ == "__main__":
    unittest.main()
