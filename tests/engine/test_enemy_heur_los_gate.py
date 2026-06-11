# tests/engine/test_enemy_heur_los_gate.py
import types
import unittest

from core.envs.warhamEnv import Warhammer40kEnv


def _stub(opaque_cells):
    """Минимальный self для _model_has_los_to_cell: model-стрелок в клетке (row0,col0)."""
    stub = types.SimpleNamespace()
    stub.terrain_opaque_cells = set(opaque_cells)
    stub.visibility_mode = "single_ray"
    stub.get_terrain_obscuring_cells_set = lambda: set()
    stub._unit_cells_for_los = lambda side, idx: [(0, 0)]
    return stub


class TestModelHasLosToCell(unittest.TestCase):
    def test_clear_los_to_cell(self):
        stub = _stub(opaque_cells=set())
        # цель: cell_x=4, cell_y=0 -> target_cell (row0,col4), чистая линия
        self.assertTrue(Warhammer40kEnv._model_has_los_to_cell(stub, 0, 4, 0))

    def test_wall_blocks_los_to_cell(self):
        stub = _stub(opaque_cells={(0, 2)})  # стена в (row0,col2) между (0,0) и (0,4)
        self.assertFalse(Warhammer40kEnv._model_has_los_to_cell(stub, 0, 4, 0))

    def test_no_attacker_cells_means_no_los(self):
        stub = _stub(opaque_cells=set())
        stub._unit_cells_for_los = lambda side, idx: []
        self.assertFalse(Warhammer40kEnv._model_has_los_to_cell(stub, 0, 4, 0))


class TestLosGateWiringContract(unittest.TestCase):
    def test_risk_and_threat_use_los_gate(self):
        from pathlib import Path

        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _model_has_los_to_cell(", source)
        self.assertIn("ENEMY_HEUR_LOS_GATE_ENABLED", source)
        # гейт вызывается в скоринге risk/threat
        self.assertIn("self._model_has_los_to_cell(", source)

    def test_flag_present_in_reward_config(self):
        import reward_config

        self.assertTrue(hasattr(reward_config, "ENEMY_HEUR_LOS_GATE_ENABLED"))


if __name__ == "__main__":
    unittest.main()
