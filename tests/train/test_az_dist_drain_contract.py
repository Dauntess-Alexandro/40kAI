"""AZ distributed drain: stop-flag в воркеры и выход learner после drain budget."""
import unittest
from pathlib import Path


class TestAzDistDrainContract(unittest.TestCase):
    def setUp(self) -> None:
        self.train_src = Path("train.py").read_text(encoding="utf-8")

    def test_az_env_workers_receive_dist_stop_flag_path(self):
        start = self.train_src.index("def _main_actor_learner_alphazero")
        end = self.train_src.index("\ndef _gmz_rollout_dict_from_transition", start)
        body = self.train_src[start:end]
        self.assertIn("_az_dist_stop_flag", body)
        self.assertIn("az_dist_stop_flag_path(TRAIN_ALGO)", body)
        # IS env workers и variant-A акторы должны получать путь, а не пустую строку.
        self.assertNotIn(
            "str(_az_contract_hash),\n                        \"\",\n                    ),\n                    daemon=True,\n                )\n                p.start()\n                procs.append(p)",
            body,
        )

    def test_az_dist_should_finish_drain_helper_exists(self):
        self.assertIn("def _az_dist_should_finish_drain()", self.train_src)

    def test_az_dist_checks_drain_on_queue_empty(self):
        marker = "def _az_dist_should_finish_drain()"
        start = self.train_src.index(marker)
        end = self.train_src.index("\n    if rollout_receiver is not None:", start)
        body = self.train_src[start:end]
        self.assertIn("except mp_queue.Empty:", body)
        self.assertIn("drain_done reason=", body)

    def test_az_dist_drain_does_not_require_all_local_done_after_budget(self):
        marker = "def _az_dist_should_finish_drain()"
        start = self.train_src.index(marker)
        end = self.train_src.index("\n    while True:", start)
        body = self.train_src[start:end]
        self.assertIn("drain_budget_elapsed", body)
        self.assertNotIn("done_actors >= active_actors:\n            return True, \"drain_budget_elapsed\"", body)


if __name__ == "__main__":
    unittest.main()
