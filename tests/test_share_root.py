"""Централизованный резолв общего корня моделей (SMB) для ПК1↔ПК2.

Единая точка вместо разрозненных os.getenv("MODELS_DIR")/("40KAI_MODELS_DIR")
в dqn_dist / az_rollout_sink / agent_registry. Приоритет:
40KAI_SHARE_ROOT → 40KAI_MODELS_DIR → MODELS_DIR → локальный artifacts/models.
"""

import os

import project_paths as pp

_VARS = ("40KAI_SHARE_ROOT", "40KAI_MODELS_DIR", "MODELS_DIR")


def _clear_env(monkeypatch):
    for v in _VARS:
        monkeypatch.delenv(v, raising=False)


def test_share_root_wins_over_models_dir(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("MODELS_DIR", r"\\PC1\old_models")
    monkeypatch.setenv("40KAI_MODELS_DIR", r"\\PC1\mid_models")
    monkeypatch.setenv("40KAI_SHARE_ROOT", r"\\PC1\share_models")
    assert pp.resolve_share_models_root() == r"\\PC1\share_models"


def test_models_dir_alias_precedence_preserved(monkeypatch):
    # Существующее поведение agent_registry: 40KAI_MODELS_DIR важнее MODELS_DIR.
    _clear_env(monkeypatch)
    monkeypatch.setenv("MODELS_DIR", r"\\PC1\old_models")
    monkeypatch.setenv("40KAI_MODELS_DIR", r"\\PC1\mid_models")
    assert pp.resolve_share_models_root() == r"\\PC1\mid_models"


def test_models_dir_used_when_only_one(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("MODELS_DIR", r"\\PC1\40kai_models")
    assert pp.resolve_share_models_root() == r"\\PC1\40kai_models"


def test_falls_back_to_local_models_when_unset(monkeypatch):
    _clear_env(monkeypatch)
    assert pp.resolve_share_models_root() == str(pp.ARTIFACTS_MODELS_DIR)


def test_share_root_pointing_at_actor_sync_is_stripped(monkeypatch):
    # Forgiving UX: юзер указал прямо на actor_sync — резолвим корень models.
    _clear_env(monkeypatch)
    monkeypatch.setenv("40KAI_SHARE_ROOT", r"\\PC1\40kai_models\actor_sync")
    assert pp.resolve_share_models_root() == r"\\PC1\40kai_models"


def test_share_actor_sync_dir_appends_actor_sync(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("40KAI_SHARE_ROOT", r"\\PC1\40kai_models")
    assert pp.share_actor_sync_dir() == os.path.join(r"\\PC1\40kai_models", "actor_sync")


def test_unc_share_named_actor_sync_not_doubled(monkeypatch):
    # Шара называется actor_sync (\\PC1\actor_sync): на UNC os.path.basename даёт '',
    # обрезка раньше не срабатывала → путь удваивался в \\PC1\actor_sync\actor_sync.
    _clear_env(monkeypatch)
    monkeypatch.setenv("40KAI_SHARE_ROOT", r"\\USER-PC\actor_sync")
    assert pp.share_actor_sync_dir() == r"\\USER-PC\actor_sync"


def test_mapped_drive_root_keeps_backslash(monkeypatch):
    # Z:\ (mapped drive) не должен схлопнуться в drive-relative 'Z:actor_sync'.
    _clear_env(monkeypatch)
    monkeypatch.setenv("40KAI_SHARE_ROOT", "Z:\\")
    assert pp.resolve_share_models_root() == "Z:\\"
    assert pp.share_actor_sync_dir() == "Z:\\actor_sync"


def test_dqn_dist_paths_honor_share_root(monkeypatch):
    # Раньше dqn_dist знал только MODELS_DIR; теперь — общий резолвер.
    from core.models import dqn_dist

    _clear_env(monkeypatch)
    monkeypatch.delenv("DQN_DIST_STOP_FLAG_PATH", raising=False)
    monkeypatch.delenv("DQN_DIST_CONTEXT_PATH", raising=False)
    monkeypatch.setenv("40KAI_SHARE_ROOT", r"\\PC1\40kai_models")

    assert dqn_dist.dqn_dist_stop_flag_path() == os.path.join(
        r"\\PC1\40kai_models", "actor_sync", "dqn_dist_stop.flag"
    )
    assert dqn_dist.dqn_dist_context_path() == os.path.join(
        r"\\PC1\40kai_models", "actor_sync", "dqn_dist_train_context.json"
    )


def test_az_rollout_sink_paths_honor_share_root(monkeypatch):
    from core.models import az_rollout_sink

    _clear_env(monkeypatch)
    monkeypatch.delenv("AZ_DIST_STOP_FLAG_PATH", raising=False)
    monkeypatch.delenv("AZ_DIST_CONTEXT_PATH", raising=False)
    monkeypatch.setenv("40KAI_SHARE_ROOT", r"\\PC1\40kai_models")

    assert az_rollout_sink.az_dist_stop_flag_path() == os.path.join(
        r"\\PC1\40kai_models", "actor_sync", "az_dist_stop.flag"
    )


def test_agent_registry_models_dir_honors_share_root(monkeypatch):
    from core.engine import agent_registry

    _clear_env(monkeypatch)
    monkeypatch.setenv("40KAI_SHARE_ROOT", r"\\PC1\40kai_models")
    assert agent_registry.models_dir() == r"\\PC1\40kai_models"
