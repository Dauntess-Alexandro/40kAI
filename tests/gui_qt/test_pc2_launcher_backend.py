"""PC2 Launcher: чистая логика ролей и проверки SMB (без Qt-зависимостей)."""

from __future__ import annotations

from app.gui_qt.pc2_launcher_backend import (
    build_launch_env,
    pc2_roles,
    resolve_role,
    validate_share_root,
)


def test_roles_have_required_metadata():
    roles = pc2_roles()
    assert roles, "должна быть хотя бы одна роль ПК2"
    for r in roles:
        assert r.id and r.label and r.script
        assert isinstance(r.requires_gpu, bool)


def test_dqn_role_does_not_require_gpu_az_is_does():
    by_id = {r.id: r for r in pc2_roles()}
    assert by_id["dqn_actors"].requires_gpu is False
    assert by_id["az_inference"].requires_gpu is True


def test_inference_roles_share_port_5555():
    # AZ-IS и GMZ-IS оба слушают :5555 — нельзя поднимать одновременно.
    by_id = {r.id: r for r in pc2_roles()}
    assert by_id["az_inference"].port == 5555
    assert by_id["gmz_inference"].port == 5555


def test_resolve_role_unknown_returns_none():
    assert resolve_role("not_a_role") is None
    assert resolve_role("dqn_actors") is not None


def test_build_launch_env_sets_share_root_and_keeps_base():
    base = {"EXISTING": "1"}
    env = build_launch_env(r"\\PC1\40kai_models", base=base)
    assert env["40KAI_SHARE_ROOT"] == r"\\PC1\40kai_models"
    assert env["EXISTING"] == "1"


def test_validate_share_root_missing_path():
    res = validate_share_root(r"\\PC1\does_not_exist_xyz")
    assert res.ok is False
    assert res.exists is False
    assert res.message


def test_validate_share_root_existing_writable(tmp_path):
    res = validate_share_root(str(tmp_path))
    assert res.exists is True
    assert res.writable is True
    assert res.ok is True
    assert res.has_weights is False


def test_validate_share_root_detects_weights(tmp_path):
    actor_sync = tmp_path / "actor_sync"
    actor_sync.mkdir()
    (actor_sync / "latest_policy.pth").write_bytes(b"x")
    res = validate_share_root(str(tmp_path))
    assert res.has_weights is True
    assert res.ok is True
