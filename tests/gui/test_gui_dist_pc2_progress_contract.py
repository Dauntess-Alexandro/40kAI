"""Контракт GUI: прогресс ПК2 идёт из маркера приёмника, не из learner-TRACE."""
import unittest
from pathlib import Path


class TestGuiDistPc2ProgressContract(unittest.TestCase):
    def setUp(self) -> None:
        self.source = Path("app/gui_qt/main.py").read_text(encoding="utf-8")

    def test_gui_parses_receiver_pc2_ep_accepted_marker(self):
        # GUI должен парсить своевременный маркер приёмника pc2_ep_accepted=N.
        self.assertIn("pc2_ep_accepted", self.source)

    def test_record_dist_actor_episode_does_not_count_pc2_from_trace(self):
        # ПК2 (100..TOPUP) больше не считается из TRACE — иначе двойной счёт
        # с маркером приёмника. Из TRACE остаются только ПК1 (<100) и topup.
        marker = "def _record_dist_actor_episode(self, actor_idx: int) -> None:"
        start = self.source.index(marker)
        end = self.source.index("def _update_dist_progress_display", start)
        body = self.source[start:end]
        self.assertNotIn("self._dist_pc2_ep_done += 1", body)
        self.assertIn("self._dist_pc1_ep_done += 1", body)

    def test_gui_has_pc2_collection_finished_status(self):
        # При remote_alive=0 в фазе сбора показываем «ПК2 завершил сбор», а не «воркеров 8/8».
        self.assertIn("ПК2 завершил сбор", self.source)

    def test_pc1_progress_uses_actor_collection_marker(self):
        # ПК1-полоска — сбор, а не обработка learner'ом: актор печатает своевременный
        # маркер pc1_ep_collected (аналог pc2_ep_accepted), GUI считает по нему.
        train_src = Path("train.py").read_text(encoding="utf-8")
        self.assertIn("[TRAIN][DIST][PC1] pc1_ep_collected actor=", train_src)
        self.assertIn("pc1_ep_collected", self.source)

    def test_trace_pc1_count_disabled_when_marker_seen(self):
        # После первого маркера сбора learner-TRACE для ПК1 игнорируется — иначе двойной счёт.
        marker = "def _record_dist_actor_episode(self, actor_idx: int) -> None:"
        start = self.source.index(marker)
        end = self.source.index("def _update_dist_progress_display", start)
        body = self.source[start:end]
        self.assertIn("_dist_pc1_marker_seen", body)

    def test_az_dist_progress_uses_pool_mode(self):
        self.assertIn('self._dist_progress_mode = "pool"', self.source)
        self.assertIn("alphazero_tree", self.source)
        self.assertIn(r"\[AZ\]\s+ep=\d+/\d+\s+actor=(\d+)", self.source)

    def test_az_rollout_receiver_emits_pc2_ep_marker(self):
        train_src = Path("train.py").read_text(encoding="utf-8")
        self.assertIn("ep_marker_fn=lambda n: print(f\"[TRAIN][DIST][PC2] pc2_ep_accepted={n}\"", train_src)

    def test_az_train_complete_clears_running_before_process_exit(self):
        self.assertIn("def _mark_az_train_complete(self)", self.source)
        self.assertIn(r"\[AZ\]\[ACTOR_LEARNER\] done\b", self.source)
        self.assertIn("self._set_running(False)", self.source)
        train_src = Path("train.py").read_text(encoding="utf-8")
        self.assertIn("print(az_done_msg, flush=True)", train_src)


if __name__ == "__main__":
    unittest.main()
