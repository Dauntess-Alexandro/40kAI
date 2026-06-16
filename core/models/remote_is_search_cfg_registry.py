"""Реестр remote IS search_cfg — единая точка для ПК2-лаунчера, GUI и bat.

Новый алгоритм: добавить RemoteIsAlgoSpec в REMOTE_IS_SEARCH_CFG_SPECS и роль в pc2_launcher_backend.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from core.models.remote_is_search_cfg_common import RemoteIsEnsureResult, RemoteIsSmbPaths


@dataclass(frozen=True)
class RemoteIsAlgoSpec:
    algo_id: str
    label: str
    search_cfg_filename: str
    weights_filename: str
    env_search_key: str
    env_weights_key: str
    pc2_role_ids: tuple[str, ...]
    ensure_fn: Callable[[str], RemoteIsEnsureResult]
    resolve_paths_fn: Callable[[str], RemoteIsSmbPaths]
    publish_from_repo_fn: Callable[..., list[str]]


def _spec_gmz() -> RemoteIsAlgoSpec:
    from core.models.gmz_remote_search_cfg_builder import (
        ACTOR_SYNC_SEARCH_CFG_NAME,
        ensure_gmz_remote_search_cfg,
        publish_gmz_remote_search_cfg_from_repo,
        resolve_gmz_smb_paths,
    )

    return RemoteIsAlgoSpec(
        algo_id="gmz",
        label="GMZ",
        search_cfg_filename=ACTOR_SYNC_SEARCH_CFG_NAME,
        weights_filename="latest_gmz_policy.pth",
        env_search_key="GMZ_REMOTE_SEARCH_CONFIG",
        env_weights_key="GMZ_REMOTE_WEIGHTS_PATH",
        pc2_role_ids=("gmz_inference",),
        ensure_fn=ensure_gmz_remote_search_cfg,
        resolve_paths_fn=resolve_gmz_smb_paths,
        publish_from_repo_fn=publish_gmz_remote_search_cfg_from_repo,
    )


def _spec_az() -> RemoteIsAlgoSpec:
    from core.models.az_remote_search_cfg_builder import (
        SEARCH_CFG_NAME,
        WEIGHTS_NAME,
        ensure_az_remote_search_cfg,
        publish_az_remote_search_cfg_from_repo,
        resolve_az_smb_paths,
    )

    return RemoteIsAlgoSpec(
        algo_id="az",
        label="AZ",
        search_cfg_filename=SEARCH_CFG_NAME,
        weights_filename=WEIGHTS_NAME,
        env_search_key="AZ_REMOTE_SEARCH_CONFIG",
        env_weights_key="AZ_REMOTE_WEIGHTS_PATH",
        pc2_role_ids=("az_inference",),
        ensure_fn=ensure_az_remote_search_cfg,
        resolve_paths_fn=resolve_az_smb_paths,
        publish_from_repo_fn=publish_az_remote_search_cfg_from_repo,
    )


def _spec_smz() -> RemoteIsAlgoSpec:
    from core.models.smz_remote_search_cfg_builder import (
        ACTOR_SYNC_SEARCH_CFG_NAME,
        SMZ_WEIGHTS_NAME,
        ensure_smz_remote_search_cfg,
        publish_smz_remote_search_cfg_from_repo,
        resolve_smz_smb_paths,
    )

    return RemoteIsAlgoSpec(
        algo_id="smz",
        label="SMZ",
        search_cfg_filename=ACTOR_SYNC_SEARCH_CFG_NAME,
        weights_filename=SMZ_WEIGHTS_NAME,
        env_search_key="SMZ_REMOTE_SEARCH_CONFIG",
        env_weights_key="SMZ_REMOTE_WEIGHTS_PATH",
        pc2_role_ids=("smz_inference",),
        ensure_fn=ensure_smz_remote_search_cfg,
        resolve_paths_fn=resolve_smz_smb_paths,
        publish_from_repo_fn=publish_smz_remote_search_cfg_from_repo,
    )


REMOTE_IS_SEARCH_CFG_SPECS: tuple[RemoteIsAlgoSpec, ...] = (
    _spec_gmz(),
    _spec_az(),
    _spec_smz(),
)

_ROLE_TO_SPEC: dict[str, RemoteIsAlgoSpec] = {
    role_id: spec for spec in REMOTE_IS_SEARCH_CFG_SPECS for role_id in spec.pc2_role_ids
}


@dataclass(frozen=True)
class InferenceLaunchPrep:
    ok: bool
    message: str
    search_cfg_path: str = ""
    weights_path: str = ""
    env_extra: tuple[tuple[str, str], ...] = ()


def spec_for_pc2_role(role_id: str) -> RemoteIsAlgoSpec | None:
    return _ROLE_TO_SPEC.get(str(role_id or ""))


def ensure_for_algo(algo_id: str, share_root: str) -> RemoteIsEnsureResult:
    for spec in REMOTE_IS_SEARCH_CFG_SPECS:
        if spec.algo_id == algo_id:
            return spec.ensure_fn(share_root)
    return RemoteIsEnsureResult(ok=False, message=f"Неизвестный алгоритм remote IS: {algo_id}")


def prepare_inference_launch(role_id: str, share_root: str) -> InferenceLaunchPrep:
    spec = spec_for_pc2_role(role_id)
    if spec is None:
        return InferenceLaunchPrep(ok=True, message="")
    path = str(share_root or "").strip()
    if not path:
        return InferenceLaunchPrep(ok=False, message="Путь к общей папке не задан.")

    result = spec.ensure_fn(path)
    if not result.ok:
        return InferenceLaunchPrep(ok=False, message=f"{spec.label}: {result.message}")

    paths = spec.resolve_paths_fn(path)
    env_pairs: list[tuple[str, str]] = []
    search_cfg = result.search_cfg_path or paths.search_cfg_path
    if search_cfg:
        env_pairs.append((spec.env_search_key, search_cfg))
    if paths.weights_path:
        env_pairs.append((spec.env_weights_key, paths.weights_path))

    action_labels = {
        "found": "найден на шаре",
        "copied": "скопирован на шару",
        "generated": "сгенерирован",
    }
    action_txt = action_labels.get(result.action, result.action or "готов")
    return InferenceLaunchPrep(
        ok=True,
        message=f"{spec.label} search_cfg {action_txt}: {search_cfg}",
        search_cfg_path=search_cfg,
        weights_path=paths.weights_path,
        env_extra=tuple(env_pairs),
    )


def publish_all_remote_search_cfgs_from_repo(*, sources: list[str] | str | None = None) -> dict[str, Any]:
    """ПК1 GUI: обновить все search_cfg на SMB actor_sync."""
    src = sources if isinstance(sources, list) else [str(sources or "gui:auto")]
    out: dict[str, Any] = {}
    for spec in REMOTE_IS_SEARCH_CFG_SPECS:
        try:
            paths = spec.publish_from_repo_fn(sources=[*src, f"algo={spec.algo_id}"])
            out[spec.algo_id] = {"ok": True, "paths": paths}
        except FileNotFoundError as exc:
            out[spec.algo_id] = {"ok": False, "skipped": str(exc)}
        except Exception as exc:
            out[spec.algo_id] = {"ok": False, "error": str(exc)}
    return out
