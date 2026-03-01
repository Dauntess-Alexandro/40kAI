import importlib.util
from pathlib import Path


_module_path = Path("gym_mod/gym_mod/engine/visibility.py").resolve()
_spec = importlib.util.spec_from_file_location("visibility_module", _module_path)
_visibility_module = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_visibility_module)
visibility_report = _visibility_module.visibility_report


def test_visibility_empty_map_has_los():
    report = visibility_report((0, 0), (5, 0), opaque_set=set(), obscuring_set=set())
    assert report["los"] is True
    assert report["obscured"] is False
    assert report["blocked_by"] is None


def test_visibility_blocked_by_opaque_cell():
    report = visibility_report((0, 0), (5, 0), opaque_set={(3, 0)}, obscuring_set=set())
    assert report["los"] is False
    assert report["blocked_by"] == (3, 0)


def test_visibility_obscured_without_blocking():
    report = visibility_report((0, 0), (5, 0), opaque_set=set(), obscuring_set={(2, 0)})
    assert report["los"] is True
    assert report["obscured"] is True
    assert report["blocked_by"] is None
