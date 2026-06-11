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


def _stat_float_stub(data, keys, default=0.0):
    if isinstance(data, dict):
        return float(data.get(keys[0], default))
    return float(default)


def _risk_stub(los):
    s = types.SimpleNamespace()
    s.unit_health = [10.0]
    s.unit_weapon = [{"Range": 24}]
    s.unit_coords = [[0, 0]]
    s._stat_float = _stat_float_stub
    s._grid_distance_euclid = lambda a, b: 6.0  # в пределах дальности
    s._model_has_los_to_cell = lambda idx, x, y: los
    return s


def _threat_stub(los):
    s = types.SimpleNamespace()
    s.unit_health = [10.0]
    s.unit_data = [{"Movement": 6}]
    s.unit_weapon = [{"Range": 24}]
    s.unit_coords = [[0, 0]]
    s._cell_from_coord = lambda c: (int(c[0]), int(c[1]))
    s._stat_float = _stat_float_stub
    s._grid_distance_euclid = lambda a, b: 6.0
    s._model_has_los_to_cell = lambda idx, x, y: los
    return s


class TestRiskThreatGateBehavior(unittest.TestCase):
    def setUp(self):
        import reward_config
        self._rc = reward_config
        self._orig = reward_config.ENEMY_HEUR_LOS_GATE_ENABLED

    def tearDown(self):
        self._rc.ENEMY_HEUR_LOS_GATE_ENABLED = self._orig

    def test_risk_gate_on_blocks_without_los(self):
        self._rc.ENEMY_HEUR_LOS_GATE_ENABLED = 1
        self.assertEqual(Warhammer40kEnv._enemy_heur_exposure_risk(_risk_stub(False), 0, 1, 1), 0.0)

    def test_risk_gate_on_counts_with_los(self):
        self._rc.ENEMY_HEUR_LOS_GATE_ENABLED = 1
        self.assertGreater(Warhammer40kEnv._enemy_heur_exposure_risk(_risk_stub(True), 0, 1, 1), 0.0)

    def test_risk_gate_off_is_backward_compatible(self):
        # флаг=0 -> прежнее поведение: риск считается без учёта LoS
        self._rc.ENEMY_HEUR_LOS_GATE_ENABLED = 0
        self.assertGreater(Warhammer40kEnv._enemy_heur_exposure_risk(_risk_stub(False), 0, 1, 1), 0.0)

    def test_threat_charge_term_not_gated_by_los(self):
        # стрельба заблокирована (нет LoS), но чардж-вклад остаётся -> threat>0
        self._rc.ENEMY_HEUR_LOS_GATE_ENABLED = 1
        self.assertGreater(Warhammer40kEnv._enemy_cell_threat_score(_threat_stub(False), 1, 1), 0.0)

    def test_threat_shoot_term_added_with_los(self):
        self._rc.ENEMY_HEUR_LOS_GATE_ENABLED = 1
        t_nolos = Warhammer40kEnv._enemy_cell_threat_score(_threat_stub(False), 1, 1)
        t_los = Warhammer40kEnv._enemy_cell_threat_score(_threat_stub(True), 1, 1)
        self.assertGreater(t_los, t_nolos)


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
