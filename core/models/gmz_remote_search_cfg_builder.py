"""Сборка gmz_remote_search_cfg.json для remote IS (те же поля, что train → search_cfg_payload)."""
from __future__ import annotations

import collections
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

from core.engine.mission import (
    deploy_for_mission,
    normalize_mission_name,
    post_deploy_setup,
)
from core.models.action_contract import action_sizes_from_env
from project_paths import ARTIFACTS_MODELS_DIR, RUNTIME_STATE_DIR, TRAIN_DATA_PATH, ensure_runtime_dirs, share_actor_sync_dir
from core.models.remote_is_search_cfg_common import (
    copy_train_data_snapshot,
    ensure_remote_search_cfg,
    load_roster_for_search,
    measure_env_dims_from_roster,
    resolve_smb_paths,
    search_cfg_local_targets,
    write_payload_to_targets,
)

ACTOR_SYNC_SEARCH_CFG_NAME = "gmz_remote_search_cfg.json"
WEIGHTS_NAME = "latest_gmz_policy.pth"


def _measure_env_dims(roster_config: dict, build_units_from_config) -> tuple[int, list[int]]:
    return measure_env_dims_from_roster(roster_config, build_units_from_config)


def build_gmz_remote_search_cfg_payload_from_dims(
    *,
    obs_dim: int,
    action_sizes: list[int],
    latent_dim: int,
    hidden_dim: int,
    num_layers: int,
    action_embed_dim: int,
    num_simulations: int,
    root_top_k: int,
    discount: float,
    temperature: float,
    gumbel_scale: float,
    prior_weight: float,
    batch_recurrent: bool,
    tree_reuse: bool,
    sources: list[str] | str | None = None,
    mission: str = "",
) -> dict[str, Any]:
    from datetime import datetime, timezone

    src_list: list[str]
    if isinstance(sources, str):
        src_list = [sources]
    elif sources:
        src_list = list(sources)
    else:
        src_list = ["gmz_remote_search_cfg_builder"]
    return {
        "obs_dim": int(obs_dim),
        "action_sizes": [int(x) for x in action_sizes],
        "latent_dim": int(latent_dim),
        "hidden_dim": int(hidden_dim),
        "num_layers": int(num_layers),
        "action_embed_dim": int(action_embed_dim),
        "num_simulations": int(num_simulations),
        "root_top_k": int(root_top_k),
        "discount": float(discount),
        "temperature": float(temperature),
        "gumbel_scale": float(gumbel_scale),
        "prior_weight": float(prior_weight),
        "batch_recurrent": int(1 if batch_recurrent else 0),
        "tree_reuse": int(1 if tree_reuse else 0),
        "_generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_sources": src_list,
        **({"_mission": normalize_mission_name(mission)} if mission else {}),
    }


def publish_gmz_remote_search_cfg(
    *,
    obs_dim: int,
    action_sizes: list[int],
    latent_dim: int,
    hidden_dim: int,
    num_layers: int,
    action_embed_dim: int,
    num_simulations: int,
    root_top_k: int,
    discount: float,
    temperature: float,
    gumbel_scale: float,
    prior_weight: float,
    batch_recurrent: bool,
    tree_reuse: bool,
    sources: list[str] | str | None = None,
    mission: str = "",
    extra_actor_sync: str | None = None,
) -> list[str]:
    payload = build_gmz_remote_search_cfg_payload_from_dims(
        obs_dim=obs_dim,
        action_sizes=action_sizes,
        latent_dim=latent_dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
        action_embed_dim=action_embed_dim,
        num_simulations=num_simulations,
        root_top_k=root_top_k,
        discount=discount,
        temperature=temperature,
        gumbel_scale=gumbel_scale,
        prior_weight=prior_weight,
        batch_recurrent=batch_recurrent,
        tree_reuse=tree_reuse,
        sources=sources,
        mission=mission,
    )
    targets = search_cfg_local_targets(ACTOR_SYNC_SEARCH_CFG_NAME, extra_actor_sync=extra_actor_sync)
    return write_payload_to_targets(payload, targets)


def _payload_kwargs_from_roster(roster_path: Path) -> dict[str, Any]:
    import train as tr  # noqa: WPS433

    roster = load_roster_for_search(roster_path)
    obs_dim, action_sizes = measure_env_dims_from_roster(roster, tr._build_units_from_config)
    return {
        "obs_dim": obs_dim,
        "action_sizes": action_sizes,
        "latent_dim": int(tr.GMZ_LATENT_DIM),
        "hidden_dim": int(tr.GMZ_HIDDEN_DIM),
        "num_layers": int(tr.GMZ_NUM_LAYERS),
        "action_embed_dim": int(tr.GMZ_ACTION_EMBED_DIM),
        "num_simulations": int(tr.GMZ_MCTS_SIMS),
        "root_top_k": int(tr.GMZ_ROOT_TOP_K),
        "discount": float(tr.GMZ_DISCOUNT),
        "temperature": float(tr.GMZ_SEARCH_TEMP),
        "gumbel_scale": float(tr.GMZ_GUMBEL_SCALE),
        "prior_weight": float(tr.GMZ_PRIOR_WEIGHT),
        "batch_recurrent": bool(tr.GMZ_BATCH_RECURRENT),
        "tree_reuse": bool(tr.GMZ_TREE_REUSE),
        "mission": normalize_mission_name(roster.get("mission", "")),
    }


def publish_gmz_remote_search_cfg_from_repo(
    *,
    roster_path: str | Path | None = None,
    sources: list[str] | str | None = None,
    extra_actor_sync: str | None = None,
    snapshot_actor_sync: str | None = None,
    share_only: bool = False,
) -> list[str]:
    from core.models.remote_is_search_cfg_common import resolve_roster_path_on_share

    sync_dir = str(snapshot_actor_sync or extra_actor_sync or share_actor_sync_dir())
    resolved: Path | None = None
    if roster_path is not None and Path(roster_path).is_file():
        resolved = Path(roster_path)
    elif not share_only and Path(TRAIN_DATA_PATH).is_file():
        resolved = Path(TRAIN_DATA_PATH)
    else:
        resolved = resolve_roster_path_on_share(sync_dir)
    if resolved is None:
        raise FileNotFoundError(
            "GMZ: нет ростера для search_cfg. Откройте Qt GUI на ПК1."
        )
    copy_train_data_snapshot(sync_dir, resolved)
    kwargs = _payload_kwargs_from_roster(resolved)
    return publish_gmz_remote_search_cfg(
        **kwargs,
        sources=sources or ["repo:auto"],
        extra_actor_sync=sync_dir,
    )


def resolve_gmz_smb_paths(share_root: str):
    return resolve_smb_paths(share_root, search_cfg_name=ACTOR_SYNC_SEARCH_CFG_NAME, weights_name=WEIGHTS_NAME)


def ensure_gmz_remote_search_cfg(share_root: str):
    return ensure_remote_search_cfg(
        share_root,
        search_cfg_name=ACTOR_SYNC_SEARCH_CFG_NAME,
        publish_from_repo=lambda **kw: publish_gmz_remote_search_cfg_from_repo(
            sources=["ensure_gmz_remote_search_cfg:auto"],
            **kw,
        ),
        resolve_paths=resolve_gmz_smb_paths,
        local_targets=lambda **kw: search_cfg_local_targets(ACTOR_SYNC_SEARCH_CFG_NAME, **kw),
    )


def build_gmz_remote_search_cfg_payload(*, train_module: Any) -> dict[str, Any]:
    """Поля совпадают с train.search_cfg_payload + служебные _meta."""
    tr = train_module
    roster = tr._load_roster_config()
    obs_dim, action_sizes = _measure_env_dims(roster, tr._build_units_from_config)

    payload: dict[str, Any] = {
        "obs_dim": int(obs_dim),
        "action_sizes": list(action_sizes),
        "latent_dim": int(tr.GMZ_LATENT_DIM),
        "hidden_dim": int(tr.GMZ_HIDDEN_DIM),
        "num_layers": int(tr.GMZ_NUM_LAYERS),
        "action_embed_dim": int(tr.GMZ_ACTION_EMBED_DIM),
        "num_simulations": int(tr.GMZ_MCTS_SIMS),
        "root_top_k": int(tr.GMZ_ROOT_TOP_K),
        "discount": float(tr.GMZ_DISCOUNT),
        "temperature": float(tr.GMZ_SEARCH_TEMP),
        "gumbel_scale": float(tr.GMZ_GUMBEL_SCALE),
        "prior_weight": float(tr.GMZ_PRIOR_WEIGHT),
        "batch_recurrent": int(tr.GMZ_BATCH_RECURRENT),
        "tree_reuse": int(tr.GMZ_TREE_REUSE),
        "_generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_sources": {
            "roster": str(TRAIN_DATA_PATH) if os.path.isfile(str(TRAIN_DATA_PATH)) else "train defaults",
            "hyperparams": "hyperparams.json → gumbel_muzero",
            "mission": normalize_mission_name(roster.get("mission", "")),
        },
    }
    return payload


def actor_sync_search_cfg_path() -> Path:
    return Path(ARTIFACTS_MODELS_DIR) / "actor_sync" / ACTOR_SYNC_SEARCH_CFG_NAME


def write_gmz_remote_search_cfg(
    output_path: str | Path | None = None,
    *,
    repo_root: str | Path | None = None,
    copy_to_actor_sync: bool = True,
) -> tuple[Path, Path | None]:
    if repo_root is not None:
        os.chdir(str(repo_root))
    ensure_runtime_dirs()
    out = Path(output_path) if output_path else Path(RUNTIME_STATE_DIR) / ACTOR_SYNC_SEARCH_CFG_NAME
    out.parent.mkdir(parents=True, exist_ok=True)

    import train as tr  # noqa: WPS433 — после chdir, те же GMZ_* что при train

    payload = build_gmz_remote_search_cfg_payload(train_module=tr)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    out.write_text(text, encoding="utf-8")

    smb_out: Path | None = None
    if copy_to_actor_sync:
        smb_out = actor_sync_search_cfg_path()
        smb_out.parent.mkdir(parents=True, exist_ok=True)
        smb_out.write_text(text, encoding="utf-8")
    return out, smb_out
