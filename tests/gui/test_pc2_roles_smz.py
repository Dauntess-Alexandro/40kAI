"""Тест ПК2-лаунчера: роль smz_inference (Sampled MuZero inference server)."""

from app.gui_qt.pc2_launcher_backend import pc2_roles, resolve_role


def test_smz_inference_role_present():
    """smz_inference должна быть в списке ролей."""
    ids = [r.id for r in pc2_roles()]
    assert "smz_inference" in ids


def test_smz_inference_role_fields():
    """smz_inference роль должна иметь правильные параметры."""
    r = resolve_role("smz_inference")
    assert r is not None
    assert r.script == "tools/pc2_remote_smz_is.bat"
    assert r.port == 5560
    assert r.requires_gpu is True


def test_gmz_role_still_present():
    """gmz_inference остаётся доступна (не конфликт портов)."""
    assert resolve_role("gmz_inference") is not None
