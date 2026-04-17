import unittest
from pathlib import Path


class TestCommandPhaseReanimationSyncRegression(unittest.TestCase):
    def test_env_has_reanimation_sync_hook(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _sync_after_command_phase_reanimation", source)
        self.assertIn('self._flush_state_snapshot(reason=f"command_phase_reanimation:{side}", force=True)', source)

    def test_command_phase_calls_sync_hook(self):
        source = Path("gym_mod/gym_mod/engine/skills.py").read_text(encoding="utf-8")
        self.assertIn('if hasattr(env, "_sync_after_command_phase_reanimation")', source)
        self.assertIn("env._sync_after_command_phase_reanimation(side)", source)

    def test_model_command_phase_paces_before_reanimation(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('self._viewer_do_pace("command", None, "command_resolve")', source)
        self.assertIn('step_kind in ("before_unit", "command_resolve")', source)
        # Двойной pace в конце command для per_phase убран — остаётся только ack до реанимации.
        self.assertNotIn('_viewer_model_pacing_after_model_phase("command")', source)

    def test_viewer_pace_summary_handles_command_resolve(self):
        source = Path("viewer/app.py").read_text(encoding="utf-8")
        self.assertIn('step_kind == "command_resolve"', source)
        self.assertIn("завершение фазы", source)
        self.assertIn('"command": "командование"', source)
        self.assertIn('detail = f"{phase_ru}', source)


if __name__ == "__main__":
    unittest.main()
