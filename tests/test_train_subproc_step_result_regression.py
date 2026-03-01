import pathlib
import unittest


class TestTrainSubprocStepResultRegression(unittest.TestCase):
    def setUp(self):
        self.source = pathlib.Path("train.py").read_text(encoding="utf-8")

    def test_train_has_step_result_normalizer(self):
        self.assertIn("def _normalize_step_result", self.source)
        self.assertIn("worker вернул error вместо step tuple", self.source)
        self.assertIn("неожиданный формат step result", self.source)

    def test_subproc_step_results_are_normalized_before_unpack(self):
        self.assertIn("step_results[idx] = _normalize_step_result(step_results[idx], idx)", self.source)
        self.assertIn("for idx, (_next_observation, _reward, done, _res, _info) in enumerate(step_results)", self.source)

    def test_train_has_subproc_recovery_on_reset_recv_errors(self):
        self.assertIn("def _recover_subproc_env", self.source)
        self.assertIn("reset не получен из worker (инициализация)", self.source)
        self.assertIn("reset не получен из worker после завершения эпизода", self.source)
        self.assertIn("_recover_subproc_env(ctx, where=\"train.main/episode-reset\")", self.source)

    def test_train_has_subproc_recovery_on_step_and_mask_ipc_errors(self):
        self.assertIn("step send не доставлен в worker", self.source)
        self.assertIn("step recv не получен из worker", self.source)
        self.assertIn("get_shoot_mask send не доставлен", self.source)
        self.assertIn("get_shoot_mask recv не получен", self.source)


if __name__ == "__main__":
    unittest.main()
