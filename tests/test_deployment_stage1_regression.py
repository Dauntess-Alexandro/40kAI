import importlib.util
import sys
import types
import unittest
from pathlib import Path


class DummyUnit:
    def __init__(self, name: str):
        self.unit_data = {"Name": name, "#OfModels": 5}
        self.instance_id = name
        self.unit_coords = [0, 0]

    def set_anchor(self, x, y):
        self.unit_coords = [int(x), int(y)]


def _load_mission_module(module_name: str, io_instance=None):
    logging_utils = types.ModuleType("gym_mod.engine.logging_utils")
    logging_utils.format_unit = lambda unit_id, unit_data, **kwargs: f"{unit_id}:{unit_data.get('Name', 'Unknown')}"

    game_io = types.ModuleType("gym_mod.engine.game_io")
    game_io.get_active_io = lambda: io_instance

    sys.modules.setdefault("gym_mod", types.ModuleType("gym_mod"))
    sys.modules.setdefault("gym_mod.engine", types.ModuleType("gym_mod.engine"))
    sys.modules["gym_mod.engine.logging_utils"] = logging_utils
    sys.modules["gym_mod.engine.game_io"] = game_io

    mission_path = Path("gym_mod/gym_mod/engine/mission.py")
    spec = importlib.util.spec_from_file_location(module_name, mission_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestDeploymentStage1Regression(unittest.TestCase):
    def _build_units(self, n, prefix):
        return [DummyUnit(f"{prefix}-{idx}") for idx in range(n)]

    def test_seeded_deployment_is_deterministic(self):
        mission = _load_mission_module("mission_under_test_stage1")

        model_a = self._build_units(4, "m")
        enemy_a = self._build_units(4, "e")
        mission.deploy_only_war(
            model_a,
            enemy_a,
            b_len=40,
            b_hei=60,
            attacker_side="model",
            deployment_seed=123,
            deployment_strategy="template_jitter",
        )
        coords_a = [tuple(u.unit_coords) for u in (model_a + enemy_a)]

        model_b = self._build_units(4, "m")
        enemy_b = self._build_units(4, "e")
        mission.deploy_only_war(
            model_b,
            enemy_b,
            b_len=40,
            b_hei=60,
            attacker_side="model",
            deployment_seed=123,
            deployment_strategy="template_jitter",
        )
        coords_b = [tuple(u.unit_coords) for u in (model_b + enemy_b)]

        self.assertEqual(coords_a, coords_b)

    def test_deploy_coords_are_unique_and_in_zones(self):
        mission = _load_mission_module("mission_under_test_stage1_zones")
        model = self._build_units(5, "m")
        enemy = self._build_units(5, "e")

        mission.deploy_only_war(
            model,
            enemy,
            b_len=40,
            b_hei=60,
            attacker_side="enemy",
            deployment_seed=77,
            deployment_strategy="template_jitter",
        )

        occupied = set()
        for idx, unit in enumerate(enemy):
            coord = tuple(unit.unit_coords)
            self.assertNotIn(coord, occupied)
            occupied.add(coord)
            self.assertTrue(mission.is_in_deploy_zone("model", coord, 40, 60), msg=f"enemy idx={idx} out of attacker zone")

        for idx, unit in enumerate(model):
            coord = tuple(unit.unit_coords)
            self.assertNotIn(coord, occupied)
            occupied.add(coord)
            self.assertTrue(mission.is_in_deploy_zone("enemy", coord, 40, 60), msg=f"model idx={idx} out of defender zone")

    def test_validate_deploy_coord_reasons(self):
        mission = _load_mission_module("mission_under_test_stage1_validate")
        ok, reason = mission.validate_deploy_coord("model", (0, 0), 40, 60, occupied=[])
        self.assertTrue(ok)
        self.assertEqual("ok", reason)

        ok, reason = mission.validate_deploy_coord("model", (-1, 0), 40, 60, occupied=[])
        self.assertFalse(ok)
        self.assertEqual("out_of_bounds", reason)

        ok, reason = mission.validate_deploy_coord("model", (0, 50), 40, 60, occupied=[])
        self.assertFalse(ok)
        self.assertEqual("outside_deploy_zone", reason)

        ok, reason = mission.validate_deploy_coord("model", (0, 0), 40, 60, occupied=[(0, 0)])
        self.assertFalse(ok)
        self.assertEqual("occupied", reason)


class TestDeploymentStage2ManualRegression(unittest.TestCase):
    def _build_units(self, n, prefix):
        return [DummyUnit(f"{prefix}-{idx}") for idx in range(n)]

    def test_manual_player_deploy_retries_and_can_fallback_to_auto(self):
        class FakeIO:
            def __init__(self):
                self.answers = iter([
                    {"x": 30, "y": 10},  # invalid zone for manual player side
                    {"x": 45, "y": 6},   # valid
                    None,                   # cancel -> auto fallback for next unit
                ])

            def request_deploy_coord(self, prompt, **kwargs):
                return next(self.answers)

        logs = []
        mission = _load_mission_module("mission_under_test_stage2_manual", io_instance=FakeIO())
        model = self._build_units(2, "m")
        enemy = self._build_units(2, "e")

        mission.deploy_only_war(
            model,
            enemy,
            b_len=40,
            b_hei=60,
            attacker_side="model",
            deployment_seed=13,
            deployment_mode="manual_player",
            log_fn=logs.append,
        )

        self.assertEqual((6, 45), tuple(enemy[0].unit_coords))
        self.assertTrue(mission.is_in_deploy_zone("enemy", tuple(enemy[1].unit_coords), 40, 60))
        self.assertTrue(any("invalid" in line for line in logs))
        self.assertTrue(any("ручной ввод отменён" in line for line in logs))


if __name__ == "__main__":
    unittest.main()
