import importlib.util
import unittest
from pathlib import Path


def _load_visibility_module():
    module_path = Path("gym_mod/gym_mod/engine/visibility.py")
    spec = importlib.util.spec_from_file_location("visibility_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


visibility = _load_visibility_module()


class TestVisibility(unittest.TestCase):
    def test_empty_map_has_los_without_obscuring(self):
        report = visibility.visibility_report((1, 1), (6, 4), opaque_cells_set=set(), obscuring_cells_set=set())
        self.assertTrue(report["los"])
        self.assertFalse(report["obscured"])
        self.assertIsNone(report["blocked_by"])

    def test_opaque_cell_blocks_line_of_sight(self):
        report = visibility.visibility_report((0, 0), (4, 0), opaque_cells_set={(2, 0)}, obscuring_cells_set=set())
        self.assertFalse(report["los"])
        self.assertEqual(report["blocked_by"], (2, 0))

    def test_obscuring_cell_marks_obscured_without_blocking(self):
        report = visibility.visibility_report((0, 0), (0, 4), opaque_cells_set=set(), obscuring_cells_set={(0, 2)})
        self.assertTrue(report["los"])
        self.assertTrue(report["obscured"])
        self.assertIsNone(report["blocked_by"])

    def test_multi_ray_5_reports_all_rays(self):
        report = visibility.visibility_report((0, 0), (3, 3), visibility_mode="multi_ray_5")
        self.assertEqual(report["visibility_mode"], "multi_ray_5")
        self.assertEqual(report["rays_total"], 5)
        self.assertEqual(report["rays_clear"], 5)
        self.assertTrue(report["fully_visible"])

    def test_multi_ray_5_has_los_if_at_least_one_ray_clear(self):
        report = visibility.visibility_report(
            (0, 0),
            (2, 1),
            visibility_mode="multi_ray_5",
            opaque_cells_set={(1, 0)},
        )
        self.assertTrue(report["los"])
        self.assertFalse(report["fully_visible"])
        self.assertTrue(report["partially_visible"])
        self.assertLess(report["rays_clear"], report["rays_total"])


if __name__ == "__main__":
    unittest.main()
