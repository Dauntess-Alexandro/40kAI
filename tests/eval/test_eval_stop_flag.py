import os
import unittest
from pathlib import Path
from unittest.mock import patch

from project_paths import EVAL_STOP_FLAG_PATH, ensure_runtime_dirs


class TestEvalStopFlag(unittest.TestCase):
    def setUp(self) -> None:
        ensure_runtime_dirs()
        if EVAL_STOP_FLAG_PATH.is_file():
            EVAL_STOP_FLAG_PATH.unlink()

    def tearDown(self) -> None:
        if EVAL_STOP_FLAG_PATH.is_file():
            EVAL_STOP_FLAG_PATH.unlink()

    def test_eval_stop_requested_false_when_flag_missing(self) -> None:
        from eval import eval_stop_requested

        self.assertFalse(eval_stop_requested())

    def test_eval_stop_requested_true_when_flag_exists(self) -> None:
        from eval import eval_stop_requested

        EVAL_STOP_FLAG_PATH.write_text("stop\n", encoding="utf-8")
        self.assertTrue(eval_stop_requested())

    def test_clear_eval_stop_flag_removes_file(self) -> None:
        from eval import clear_eval_stop_flag, eval_stop_requested

        EVAL_STOP_FLAG_PATH.write_text("stop\n", encoding="utf-8")
        clear_eval_stop_flag()
        self.assertFalse(eval_stop_requested())

    def test_custom_flag_path_from_env(self) -> None:
        from eval import clear_eval_stop_flag, eval_stop_requested

        custom = Path(os.environ.get("TEMP", ".")) / "40kai_eval_stop_test.flag"
        if custom.is_file():
            custom.unlink()
        with patch.dict(os.environ, {"EVAL_STOP_FLAG_PATH": str(custom)}):
            custom.write_text("stop\n", encoding="utf-8")
            self.assertTrue(eval_stop_requested())
            clear_eval_stop_flag()
            self.assertFalse(custom.exists())


if __name__ == "__main__":
    unittest.main()
