# tests/gui/test_heur_calibrate_runner.py
"""Контракт HeurCalibrateRunner: polling candidates.jsonl, applyPatch."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestApplyPatch(unittest.TestCase):
    """applyPatch парсит best_reward_config_patch.md и обновляет reward_config.py."""

    def _make_patch_md(self, tmp_dir: str) -> Path:
        content = (
            "# Phase 8 best reward_config patch\n\n"
            "baseline_score=0.812000\n"
            "candidate=7\n"
            "score=0.847000\n\n"
            "```python\n"
            "ENEMY_HEUR_RISK_W = 0.312000  # baseline 0.180000, delta +0.132000\n"
            "ENEMY_HEUR_OBJECTIVE_CONTROL_W = 0.501000  # baseline 0.420000, delta +0.081000\n"
            "```\n"
        )
        p = Path(tmp_dir) / "best_reward_config_patch.md"
        p.write_text(content, encoding="utf-8")
        return p

    def _make_reward_config(self, tmp_dir: str) -> Path:
        content = (
            "# reward_config.py\n"
            "ENEMY_HEUR_RISK_W = 0.18\n"
            "ENEMY_HEUR_OBJECTIVE_CONTROL_W = 0.42\n"
            "OTHER_PARAM = 1.0\n"
        )
        p = Path(tmp_dir) / "reward_config.py"
        p.write_text(content, encoding="utf-8")
        return p

    def test_apply_patch_updates_values(self):
        from app.gui_qt.heur_calibrate_runner import _apply_patch_to_reward_config
        with tempfile.TemporaryDirectory() as tmp:
            patch_md = self._make_patch_md(tmp)
            rc_path = self._make_reward_config(tmp)
            changed = _apply_patch_to_reward_config(str(patch_md), str(rc_path))
            result = rc_path.read_text(encoding="utf-8")
            self.assertIn("ENEMY_HEUR_RISK_W = 0.312000", result)
            self.assertIn("ENEMY_HEUR_OBJECTIVE_CONTROL_W = 0.501000", result)
            self.assertIn("OTHER_PARAM = 1.0", result)
            self.assertIn("ENEMY_HEUR_RISK_W", changed)
            self.assertIn("ENEMY_HEUR_OBJECTIVE_CONTROL_W", changed)

    def test_apply_patch_missing_file_raises(self):
        from app.gui_qt.heur_calibrate_runner import _apply_patch_to_reward_config
        with self.assertRaises(FileNotFoundError):
            _apply_patch_to_reward_config("/nonexistent/patch.md", "/nonexistent/rc.py")

    def test_apply_patch_no_python_block_raises(self):
        from app.gui_qt.heur_calibrate_runner import _apply_patch_to_reward_config
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "patch.md"
            p.write_text("no python block here\n", encoding="utf-8")
            rc = Path(tmp) / "reward_config.py"
            rc.write_text("X = 1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                _apply_patch_to_reward_config(str(p), str(rc))


class TestCalibrateRunnerContract(unittest.TestCase):
    def test_module_importable(self):
        from app.gui_qt import heur_calibrate_runner  # noqa: F401

    def test_runner_has_required_signals(self):
        src = Path("app/gui_qt/heur_calibrate_runner.py").read_text(encoding="utf-8")
        for sig in ["calibrationStarted", "candidateResult", "calibrationFinished",
                    "calibrationFailed", "progressChanged", "patchApplied", "patchFailed"]:
            self.assertIn(sig, src, f"Сигнал {sig} не найден")

    def test_runner_has_slots(self):
        src = Path("app/gui_qt/heur_calibrate_runner.py").read_text(encoding="utf-8")
        for name in ["def run(", "def stop(", "def applyPatch("]:
            self.assertIn(name, src, f"Слот {name} не найден")


if __name__ == "__main__":
    unittest.main()
