import importlib.util
import pathlib
import sys
import unittest


def _load_los_contract_module():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    module_path = repo_root / "gym_mod" / "gym_mod" / "engine" / "los_contract.py"
    spec = importlib.util.spec_from_file_location("los_contract", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


los_contract = _load_los_contract_module()


class TestLosPhase0Contract(unittest.TestCase):
    def test_default_rule_flags_match_hybrid_plan(self):
        flags = los_contract.LosRuleFlags()
        self.assertTrue(flags.see_through_observer_unit_models)
        self.assertTrue(flags.see_through_target_unit_models_for_full)
        self.assertTrue(flags.block_by_terrain)
        self.assertTrue(flags.block_by_models)

    def test_default_sampling_config(self):
        cfg = los_contract.LosSamplingConfig()
        self.assertEqual(cfg.sample_count, 5)
        self.assertFalse(cfg.include_diagonals)
        self.assertEqual(cfg.required_front_arc_samples, 3)

    def test_unit_visibility_aggregation(self):
        model_results = [
            los_contract.LosCheckResult(
                visible=True,
                fully_visible=False,
                reason_codes=(los_contract.LosReason.VISIBLE,),
                passed_rays=1,
                total_rays=4,
            ),
            los_contract.LosCheckResult(
                visible=False,
                fully_visible=False,
                reason_codes=(los_contract.LosReason.BLOCKED_BY_TERRAIN,),
                passed_rays=0,
                total_rays=4,
            ),
        ]
        summary = los_contract.evaluate_unit_visibility(model_results)
        self.assertTrue(summary.unit_visible)
        self.assertFalse(summary.unit_fully_visible)
        self.assertEqual(len(summary.model_results), 2)

    def test_unit_fully_visible_requires_all_models(self):
        model_results = [
            los_contract.LosCheckResult(visible=True, fully_visible=True),
            los_contract.LosCheckResult(visible=True, fully_visible=True),
        ]
        summary = los_contract.evaluate_unit_visibility(model_results)
        self.assertTrue(summary.unit_visible)
        self.assertTrue(summary.unit_fully_visible)


if __name__ == "__main__":
    unittest.main()
