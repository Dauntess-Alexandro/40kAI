import unittest
from pathlib import Path


class TestGuiStopProcessAsync(unittest.TestCase):
    def test_stop_process_does_not_block_on_wait_for_finished(self) -> None:
        source = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
        stop_fn = source.split("def stop_process(self)", 1)[1].split("\n    @QtCore.Slot()", 1)[0]
        self.assertNotIn("waitForFinished", stop_fn)
        self.assertIn("_stop_kill_timer", stop_fn)
        self.assertIn("_write_eval_stop_flag", stop_fn)

    def test_on_finished_clears_eval_stop_flag(self) -> None:
        source = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
        finished_fn = source.split("def _on_finished(self", 1)[1].split("\n    def _cleanup_process", 1)[0]
        self.assertIn("_clear_eval_stop_flag", finished_fn)
        self.assertIn("stopped_by_user", finished_fn)


if __name__ == "__main__":
    unittest.main()
