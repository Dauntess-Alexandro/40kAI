import unittest
from pathlib import Path


class TestPhaseLoggingRegression(unittest.TestCase):
    def test_phase_logged_once_via_begin_phase(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        calls = [line for line in source.splitlines() if "self._log_phase(" in line]
        # Ожидаем единственный вызов в begin_phase
        self.assertEqual(1, len(calls), f"Ожидался 1 вызов _log_phase, найдено {len(calls)}: {calls}")


if __name__ == "__main__":
    unittest.main()
