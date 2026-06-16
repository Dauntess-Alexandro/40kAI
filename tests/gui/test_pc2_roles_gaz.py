"""Тест ПК2-лаунчера: роли gaz_inference / gaz_actors (Gumbel AlphaZero)."""

from app.gui_qt.pc2_launcher_backend import pc2_roles, resolve_role


def test_gaz_roles_present():
    ids = [r.id for r in pc2_roles()]
    assert "gaz_inference" in ids
    assert "gaz_actors" in ids


def test_gaz_inference_role_fields():
    r = resolve_role("gaz_inference")
    assert r is not None
    assert r.script == "tools/pc2_remote_gaz_is.bat"
    assert r.port == 5565
    assert r.requires_gpu is True


def test_gaz_actors_role_fields():
    r = resolve_role("gaz_actors")
    assert r is not None
    assert r.script == "tools/pc2_gaz_actors.bat"
    assert r.port == 5567
    assert r.requires_gpu is False


def test_gaz_ports_do_not_clash_with_az_smz_gmz():
    by_id = {r.id: r for r in pc2_roles()}
    # IS-порты различаются: gmz/az 5555, smz 5560, gaz 5565
    assert by_id["gaz_inference"].port == 5565
    assert by_id["az_inference"].port == 5555
    assert by_id["smz_inference"].port == 5560
    # distributed: az 5557, gaz 5567
    assert by_id["gaz_actors"].port == 5567
    assert by_id["az_actors"].port == 5557
