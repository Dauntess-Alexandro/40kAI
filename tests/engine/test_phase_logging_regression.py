import unittest
from pathlib import Path


class TestPhaseLoggingRegression(unittest.TestCase):
    def test_phase_logged_once_via_begin_phase(self):
        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        calls = [line for line in source.splitlines() if "self._log_phase(" in line]
        # РћР¶РёРґР°РµРј РµРґРёРЅСЃС‚РІРµРЅРЅС‹Р№ РІС‹Р·РѕРІ РІ begin_phase
        self.assertEqual(1, len(calls), f"РћР¶РёРґР°Р»СЃСЏ 1 РІС‹Р·РѕРІ _log_phase, РЅР°Р№РґРµРЅРѕ {len(calls)}: {calls}")


if __name__ == "__main__":
    unittest.main()

