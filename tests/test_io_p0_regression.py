import unittest
from pathlib import Path


class TestIoP0Regression(unittest.TestCase):
    def test_state_export_uses_tail_read_for_log(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn('with open(path, "rb") as handle', source)
        self.assertIn('handle.seek(-read_size, os.SEEK_END)', source)
        self.assertIn('max_bytes=65536', source)

    def test_state_export_events_limit_is_configurable_and_reduced(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn('def _read_event_tail(default_max_events=500):', source)
        self.assertIn('os.getenv("STATE_MODEL_EVENTS_LIMIT", str(default_max_events))', source)

    def test_gui_flush_has_safer_default_interval(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('"STATE_FLUSH_MIN_INTERVAL_MS" not in os.environ', source)
        self.assertIn('min_interval_ms = max(min_interval_ms, 180)', source)

    def test_checklist_marks_p0_done(self):
        source = Path("I_O_PERF_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("✅ P0 выполнен.", source)
        self.assertIn("- [x] **Оптимизировать чтение `response.txt`", source)
        self.assertIn("- [x] **Снизить объём `model_events` в `state.json`**", source)
        self.assertIn("- [x] **Ограничить частоту тяжёлых state flush в GUI**", source)


if __name__ == "__main__":
    unittest.main()
