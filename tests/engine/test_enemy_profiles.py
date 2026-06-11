# tests/engine/test_enemy_profiles.py
import unittest

from core.engine.heuristic_targeting import (
    ENEMY_PROFILE_CONFIG,
    ENEMY_PROFILES,
    pick_enemy_profile,
)


class TestPickEnemyProfile(unittest.TestCase):
    def test_deterministic_by_seed(self):
        self.assertEqual(pick_enemy_profile(0), pick_enemy_profile(0))
        self.assertEqual(pick_enemy_profile(7), pick_enemy_profile(7))

    def test_covers_all_profiles_across_seeds(self):
        seen = {pick_enemy_profile(s) for s in range(len(ENEMY_PROFILES) * 3)}
        self.assertEqual(seen, set(ENEMY_PROFILES))

    def test_returns_valid_profile(self):
        for s in (0, 1, 2, 3, 4, 5, 100, 999):
            self.assertIn(pick_enemy_profile(s), ENEMY_PROFILES)


class TestEnemyProfileConfig(unittest.TestCase):
    def test_all_profiles_have_full_config(self):
        self.assertEqual(set(ENEMY_PROFILE_CONFIG.keys()), set(ENEMY_PROFILES))
        for name, cfg in ENEMY_PROFILE_CONFIG.items():
            self.assertIn("mode_bias", cfg)
            self.assertIn("risk_mult", cfg)
            self.assertIn("obj_mult", cfg)
            self.assertIn(cfg["mode_bias"], (None, "kite", "commit", "hold"))
            self.assertGreater(float(cfg["risk_mult"]), 0.0)
            self.assertGreater(float(cfg["obj_mult"]), 0.0)

    def test_profiles_are_distinct_in_behavior(self):
        # kiter тянет в kite, aggressor — в commit (ключевое для разнообразия)
        self.assertEqual(ENEMY_PROFILE_CONFIG["kiter"]["mode_bias"], "kite")
        self.assertEqual(ENEMY_PROFILE_CONFIG["aggressor"]["mode_bias"], "commit")
        self.assertIsNone(ENEMY_PROFILE_CONFIG["balanced"]["mode_bias"])


class TestProfileModeBias(unittest.TestCase):
    def _stub(self, cfg, ranged_score):
        import types

        s = types.SimpleNamespace()
        s._enemy_profile_cfg = cfg
        s._unit_ranged_score = lambda side, idx: ranged_score
        return s

    def test_kiter_biases_kite_when_ranged_and_natural_hold(self):
        from core.envs.warhamEnv import Warhammer40kEnv

        s = self._stub(ENEMY_PROFILE_CONFIG["kiter"], ranged_score=2.0)
        self.assertEqual(Warhammer40kEnv._enemy_profile_mode_bias(s, 0, "hold"), "kite")

    def test_no_bias_when_natural_mode_not_hold(self):
        from core.envs.warhamEnv import Warhammer40kEnv

        s = self._stub(ENEMY_PROFILE_CONFIG["kiter"], ranged_score=2.0)
        # юнит уже кайтит/коммитит естественно — не трогаем
        self.assertIsNone(Warhammer40kEnv._enemy_profile_mode_bias(s, 0, "commit"))

    def test_kite_bias_skipped_without_ranged(self):
        from core.envs.warhamEnv import Warhammer40kEnv

        s = self._stub(ENEMY_PROFILE_CONFIG["kiter"], ranged_score=0.0)
        self.assertIsNone(Warhammer40kEnv._enemy_profile_mode_bias(s, 0, "hold"))

    def test_balanced_no_bias(self):
        from core.envs.warhamEnv import Warhammer40kEnv

        s = self._stub(ENEMY_PROFILE_CONFIG["balanced"], ranged_score=2.0)
        self.assertIsNone(Warhammer40kEnv._enemy_profile_mode_bias(s, 0, "hold"))

    def test_turtle_hold_bias_is_noop_at_natural_hold(self):
        from core.envs.warhamEnv import Warhammer40kEnv

        # turtle mode_bias='hold' при natural 'hold' не должен маркировать смещение
        s = self._stub(ENEMY_PROFILE_CONFIG["turtle"], ranged_score=2.0)
        self.assertIsNone(Warhammer40kEnv._enemy_profile_mode_bias(s, 0, "hold"))


class TestProfileWiringContract(unittest.TestCase):
    def test_env_uses_profile(self):
        from pathlib import Path

        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("pick_enemy_profile(", source)
        self.assertIn("_enemy_profile_mode_bias(", source)
        self.assertIn("_enemy_game_profile", source)
        self.assertIn("ENEMY_HEUR_PROFILE_RANDOMIZATION_ENABLED", source)

    def test_flag_present(self):
        import reward_config

        self.assertTrue(hasattr(reward_config, "ENEMY_HEUR_PROFILE_RANDOMIZATION_ENABLED"))


if __name__ == "__main__":
    unittest.main()
