import unittest
from pathlib import Path


class TestIoP2Regression(unittest.TestCase):
    def test_state_payload_has_light_and_full_modes(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn('"payload_kind": "light"', source)
        self.assertIn('os.getenv("STATE_PAYLOAD_MODE", "auto")', source)
        self.assertIn('STATE_FULL_PAYLOAD_INTERVAL_MS', source)
        self.assertIn('payload["payload_kind"] = "full"', source)

    def test_io_profiler_categories_are_wired(self):
        state_src = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        io_src = Path("gym_mod/gym_mod/engine/game_io.py").read_text(encoding="utf-8")
        train_src = Path("train.py").read_text(encoding="utf-8")

        self.assertIn('timed("state export")', state_src)
        self.assertIn('timed("log append")', io_src)
        self.assertIn('timed("checkpoint save")', train_src)
        self.assertIn('timed("metrics save")', train_src)
        self.assertIn('IO_PROFILER.write_snapshot()', train_src)

    def test_checklist_marks_p2_items_done(self):
        source = Path("I_O_PERF_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("- [x] **Разделить “лёгкий” и “полный” state payload**", source)
        self.assertIn("- [x] **Сделать профилирование I/O по категориям**", source)


if __name__ == "__main__":
    unittest.main()
