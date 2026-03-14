import unittest
from pathlib import Path


class TestStayModeRegression(unittest.TestCase):
    def test_viewer_backspace_sends_stay_mode(self):
        source = Path("viewer/app.py").read_text(encoding="utf-8")
        self.assertIn('"mode": "stay"', source)
        self.assertIn('Backspace', source)

    def test_gui_io_keeps_stay_payload(self):
        source = Path("gym_mod/gym_mod/engine/game_io.py").read_text(encoding="utf-8")
        self.assertIn('payload["mode"] = str(answer.get("mode"))', source)
        self.assertIn('payload["skip_movement"] = bool(answer.get("skip_movement"))', source)

    def test_env_manual_movement_supports_stay_mode(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('if mode == "stay" or skip_requested:', source)
        self.assertIn('move_mode = "stay"', source)
        self.assertIn('используйте mode=stay', source)


if __name__ == "__main__":
    unittest.main()
