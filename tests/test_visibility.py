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


if __name__ == "__main__":
    unittest.main()
