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


if __name__ == "__main__":
    unittest.main()
