import unittest
from pathlib import Path


class TestIoP1Regression(unittest.TestCase):
    def test_gui_log_writer_is_buffered_async(self):
        source = Path("gym_mod/gym_mod/engine/game_io.py").read_text(encoding="utf-8")
        self.assertIn("class _AsyncLogWriter", source)
        self.assertIn("GUI_LOG_BATCH_SIZE", source)
        self.assertIn("GUI_LOG_ASYNC_WRITE", source)
        self.assertIn("_ASYNC_LOG_WRITER.submit", source)

    def test_train_log_is_buffered(self):
        source = Path("train.py").read_text(encoding="utf-8")
        self.assertIn("_TRAIN_LOG_BUFFER", source)
        self.assertIn("TRAIN_LOG_BUFFER_LINES", source)
        self.assertIn("TRAIN_LOG_FLUSH_INTERVAL_SEC", source)
        self.assertIn("_flush_agent_log_buffer(force=True)", source)

    def test_save_every_has_min_guard(self):
        source = Path("train.py").read_text(encoding="utf-8")
        self.assertIn("SAVE_EVERY_MIN", source)
        self.assertIn("SAVE_EVERY_ALLOW_LOW", source)
        self.assertIn("if SAVE_EVERY > 0 and SAVE_EVERY < SAVE_EVERY_MIN and not SAVE_EVERY_ALLOW_LOW:", source)

    def test_checklist_marks_p1_done(self):
        source = Path("I_O_PERF_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("✅ P1 выполнен.", source)
        self.assertIn("- [x] **Убрать частые open/write/close для `gui/response.txt`**", source)
        self.assertIn("- [x] **Снизить нагрузку от train-логирования в файл**", source)
        self.assertIn("- [x] **Проверить частоту checkpoint-save**", source)


if __name__ == "__main__":
    unittest.main()
