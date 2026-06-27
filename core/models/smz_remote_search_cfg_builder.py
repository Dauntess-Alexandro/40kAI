"""Сборка smz_remote_search_cfg.json для remote IS (те же поля, что train → search_cfg_payload)."""
from __future__ import annotations

import collections
import os
from dataclasses import dataclass
from datetime import UTC, datetime
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
from core.models.remote_is_search_cfg_common import (
    TRAIN_DATA_SNAPSHOT_NAME,
    copy_train_data_snapshot,
    current_env_obs_dim,
    ensure_remote_search_cfg,
    load_roster_for_search,
    measure_env_dims_from_roster,
    resolve_smb_paths,
    search_cfg_local_targets,
    write_payload_to_targets,
)
from core.models.remote_is_search_cfg_common import (
    RemoteIsEnsureResult as SmzEnsureResult,
)
from project_paths import (
    RUNTIME_STATE_DIR,
    TRAIN_DATA_PATH,
    ensure_runtime_dirs,
    share_actor_sync_dir,
)

ACTOR_SYNC_SEARCH_CFG_NAME = "smz_remote_search_cfg.json"
SMZ_WEIGHTS_NAME = "latest_smz_policy.pth"
SMZ_TRAIN_DATA_SNAPSHOT_NAME = TRAIN_DATA_SNAPSHOT_NAME  # legacy alias


@dataclass(frozen=True)
class SmzSmbPaths:
    """Пути к весам и search_cfg на SMB-шаре (или локальном actor_sync)."""

    actor_sync_dir: str
    search_cfg_path: str
    weights_path: str


# Совместимость: SmzEnsureResult = RemoteIsEnsureResult


def resolve_smz_smb_paths(share_root: str) -> SmzSmbPaths:
    paths = resolve_smb_paths(
        share_root,
        search_cfg_name=ACTOR_SYNC_SEARCH_CFG_NAME,
        weights_name=SMZ_WEIGHTS_NAME,
    )
    return SmzSmbPaths(
        actor_sync_dir=paths.actor_sync_dir,
        search_cfg_path=paths.search_cfg_path,
        weights_path=paths.weights_path,
    )


def ensure_smz_remote_search_cfg(share_root: str) -> SmzEnsureResult:
    return ensure_remote_search_cfg(
        share_root,
        search_cfg_name=ACTOR_SYNC_SEARCH_CFG_NAME,
        publish_from_repo=lambda **kw: publish_smz_remote_search_cfg_from_repo(
            sources=["ensure_smz_remote_search_cfg:auto"],
            **kw,
        ),
        resolve_paths=lambda root: resolve_smb_paths(
            root,
            search_cfg_name=ACTOR_SYNC_SEARCH_CFG_NAME,
            weights_name=SMZ_WEIGHTS_NAME,
        ),
        local_targets=lambda **kw: search_cfg_local_targets(ACTOR_SYNC_SEARCH_CFG_NAME, **kw),
        current_obs_dim_fn=lambda: current_env_obs_dim(),
    )


def _search_cfg_targets(*, extra_actor_sync: str | None = None) -> list[Path]:
    return search_cfg_local_targets(ACTOR_SYNC_SEARCH_CFG_NAME, extra_actor_sync=extra_actor_sync)


def _write_payload_to_targets(payload: dict[str, Any], targets: list[Path]) -> list[str]:
    return write_payload_to_targets(payload, targets)


def _is_valid_search_cfg(path: str) -> bool:
    from core.models.remote_is_search_cfg_common import is_valid_search_cfg

    return is_valid_search_cfg(path)


# --- legacy helpers below (payload build) ---


def build_smz_remote_search_cfg_payload_from_dims(
    *,
    obs_dim: int,
    action_sizes: list[int],
    latent_dim: int,
    hidden_dim: int,
    num_layers: int,
    action_embed_dim: int,
    num_samples: int,
    discount: float,
    temperature: float,
    sample_temperature: float,
    prior_weight: float,
    dedup: bool,
    sources: list[str] | str | None = None,
    mission: str = "",
) -> dict[str, Any]:
    src_list: list[str]
    if isinstance(sources, str):
        src_list = [sources]
    elif sources:
        src_list = list(sources)
    else:
        src_list = ["smz_remote_search_cfg_builder"]
    return {
        "obs_dim": int(obs_dim),
        "action_sizes": [int(x) for x in action_sizes],
        "latent_dim": int(latent_dim),
        "hidden_dim": int(hidden_dim),
        "num_layers": int(num_layers),
        "action_embed_dim": int(action_embed_dim),
        "num_samples": int(num_samples),
        "discount": float(discount),
        "temperature": float(temperature),
        "sample_temperature": float(sample_temperature),
        "prior_weight": float(prior_weight),
        "dedup": int(1 if dedup else 0),
        "_generated_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_sources": src_list,
        **({"_mission": normalize_mission_name(mission)} if mission else {}),
    }


def publish_smz_remote_search_cfg(
    *,
    obs_dim: int,
    action_sizes: list[int],
    latent_dim: int,
    hidden_dim: int,
    num_layers: int,
    action_embed_dim: int,
    num_samples: int,
    discount: float,
    temperature: float,
    sample_temperature: float,
    prior_weight: float,
    dedup: bool,
    sources: list[str] | str | None = None,
    mission: str = "",
    extra_actor_sync: str | None = None,
) -> list[str]:
    """Записать search_cfg на SMB actor_sync и в runtime/state (как AZ publish)."""
    payload = build_smz_remote_search_cfg_payload_from_dims(
        obs_dim=obs_dim,
        action_sizes=action_sizes,
        latent_dim=latent_dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
        action_embed_dim=action_embed_dim,
        num_samples=num_samples,
        discount=discount,
        temperature=temperature,
        sample_temperature=sample_temperature,
        prior_weight=prior_weight,
        dedup=dedup,
        sources=sources,
        mission=mission,
    )
    return _write_payload_to_targets(payload, _search_cfg_targets(extra_actor_sync=extra_actor_sync))


def _payload_kwargs_from_roster(roster_path: Path) -> dict[str, Any]:
    import train as tr  # noqa: WPS433

    roster = load_roster_for_search(roster_path)
    obs_dim, action_sizes = measure_env_dims_from_roster(roster, tr._build_units_from_config)
    return {
        "obs_dim": obs_dim,
        "action_sizes": action_sizes,
        "latent_dim": int(tr.SMZ_LATENT_DIM),
        "hidden_dim": int(tr.SMZ_HIDDEN_DIM),
        "num_layers": int(tr.SMZ_NUM_LAYERS),
        "action_embed_dim": int(tr.SMZ_ACTION_EMBED_DIM),
        "num_samples": int(tr.SMZ_NUM_SAMPLES),
        "discount": float(tr.SMZ_DISCOUNT),
        "temperature": float(tr.SMZ_SEARCH_TEMP),
        "sample_temperature": float(tr.SMZ_SAMPLE_TEMP),
        "prior_weight": float(tr.SMZ_PRIOR_WEIGHT),
        "dedup": bool(tr.SMZ_DEDUP),
        "mission": normalize_mission_name(roster.get("mission", "")),
    }


def publish_smz_remote_search_cfg_from_repo(
    *,
    roster_path: str | Path | None = None,
    sources: list[str] | str | None = None,
    extra_actor_sync: str | None = None,
    snapshot_actor_sync: str | None = None,
    share_only: bool = False,
) -> list[str]:
    """ПК1 GUI / ПК2 ensure: опубликовать search_cfg без запуска train."""
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
            "Нет runtime/state/data.json и снимка ростера на шаре. "
            "Откройте Qt GUI на ПК1 — ростер запишется на шару автоматически."
        )
    copy_train_data_snapshot(sync_dir, resolved)
    return publish_smz_remote_search_cfg(
        **_payload_kwargs_from_roster(resolved),
        sources=sources or ["repo:auto"],
        extra_actor_sync=extra_actor_sync or sync_dir,
    )


def _payload_kwargs_from_train() -> dict[str, Any]:
    resolved = _resolve_roster_path()
    if resolved is None:
        import train as tr  # noqa: WPS433

        roster = tr._load_roster_config()
        obs_dim, action_sizes = _measure_env_dims(roster, tr._build_units_from_config)
        return {
            "obs_dim": obs_dim,
            "action_sizes": action_sizes,
            "latent_dim": int(tr.SMZ_LATENT_DIM),
            "hidden_dim": int(tr.SMZ_HIDDEN_DIM),
            "num_layers": int(tr.SMZ_NUM_LAYERS),
            "action_embed_dim": int(tr.SMZ_ACTION_EMBED_DIM),
            "num_samples": int(tr.SMZ_NUM_SAMPLES),
            "discount": float(tr.SMZ_DISCOUNT),
            "temperature": float(tr.SMZ_SEARCH_TEMP),
            "sample_temperature": float(tr.SMZ_SAMPLE_TEMP),
            "prior_weight": float(tr.SMZ_PRIOR_WEIGHT),
            "dedup": bool(tr.SMZ_DEDUP),
            "mission": normalize_mission_name(roster.get("mission", "")),
        }
    return _payload_kwargs_from_roster(resolved)


def _measure_env_dims(roster_config: dict, build_units_from_config) -> tuple[int, list[int]]:
    """obs_dim и action_sizes — как в train._main_actor_learner_gumbel_muzero."""
    b_len = int(roster_config["b_len"])
    b_hei = int(roster_config["b_hei"])
    mission_name = normalize_mission_name(roster_config.get("mission", "only_war"))
    old_mission = os.environ.get("MISSION_NAME")
    old_ruleset = os.environ.get("RULESET_VERSION")
    old_env_ruleset = os.environ.get("ENV_RULESET_VERSION")
    ruleset_version = str(roster_config.get("ruleset_version") or f"{mission_name}_v2")
    os.environ["MISSION_NAME"] = mission_name
    os.environ["RULESET_VERSION"] = ruleset_version
    os.environ["ENV_RULESET_VERSION"] = ruleset_version

    try:
        enemy, model = build_units_from_config(roster_config, b_len, b_hei)
        from core.envs.warhamEnv import roll_off_attacker_defender

        attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
        deploy_for_mission(
            mission_name,
            model_units=model,
            enemy_units=enemy,
            b_len=b_len,
            b_hei=b_hei,
            attacker_side=attacker_side,
            log_fn=None,
        )
        post_deploy_setup(log_fn=None)
        env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        env0.attacker_side = attacker_side
        env0.defender_side = defender_side
        state0, _ = env0.reset(options={"m": model, "e": enemy, "trunc": True})
        if isinstance(state0, (dict, collections.OrderedDict)):
            n_observations = len(list(state0.values()))
        else:
            n_observations = int(np.array(state0).shape[0])
        len_model = int(len(model))
        n_actions = action_sizes_from_env(env0, len_model)
        try:
            env0.close()
        except Exception:
            pass
        return int(n_observations), [int(x) for x in n_actions]
    finally:
        if old_mission is None:
            os.environ.pop("MISSION_NAME", None)
        else:
            os.environ["MISSION_NAME"] = old_mission
        if old_ruleset is None:
            os.environ.pop("RULESET_VERSION", None)
        else:
            os.environ["RULESET_VERSION"] = old_ruleset
        if old_env_ruleset is None:
            os.environ.pop("ENV_RULESET_VERSION", None)
        else:
            os.environ["ENV_RULESET_VERSION"] = old_env_ruleset


def build_smz_remote_search_cfg_payload(*, train_module: Any) -> dict[str, Any]:
    """Поля совпадают с train.search_cfg_payload (SMZ) + служебные _meta."""
    tr = train_module
    roster = tr._load_roster_config()
    obs_dim, action_sizes = _measure_env_dims(roster, tr._build_units_from_config)
    payload = build_smz_remote_search_cfg_payload_from_dims(
        obs_dim=obs_dim,
        action_sizes=action_sizes,
        latent_dim=int(tr.SMZ_LATENT_DIM),
        hidden_dim=int(tr.SMZ_HIDDEN_DIM),
        num_layers=int(tr.SMZ_NUM_LAYERS),
        action_embed_dim=int(tr.SMZ_ACTION_EMBED_DIM),
        num_samples=int(tr.SMZ_NUM_SAMPLES),
        discount=float(tr.SMZ_DISCOUNT),
        temperature=float(tr.SMZ_SEARCH_TEMP),
        sample_temperature=float(tr.SMZ_SAMPLE_TEMP),
        prior_weight=float(tr.SMZ_PRIOR_WEIGHT),
        dedup=bool(tr.SMZ_DEDUP),
        mission=normalize_mission_name(roster.get("mission", "")),
    )
    payload["_sources"] = {
        "roster": str(TRAIN_DATA_PATH) if os.path.isfile(str(TRAIN_DATA_PATH)) else "train defaults",
        "hyperparams": "hyperparams.json → sampled_muzero",
        "mission": normalize_mission_name(roster.get("mission", "")),
    }
    return payload


def actor_sync_search_cfg_path() -> Path:
    return Path(share_actor_sync_dir()) / ACTOR_SYNC_SEARCH_CFG_NAME


def write_smz_remote_search_cfg(
    output_path: str | Path | None = None,
    *,
    repo_root: str | Path | None = None,
    copy_to_actor_sync: bool = True,
) -> tuple[Path, Path | None]:
    if repo_root is not None:
        os.chdir(str(repo_root))
    ensure_runtime_dirs()
    out = Path(output_path) if output_path else Path(RUNTIME_STATE_DIR) / ACTOR_SYNC_SEARCH_CFG_NAME

    import train as tr  # noqa: WPS433 — после chdir, те же SMZ_* что при train

    payload = build_smz_remote_search_cfg_payload(train_module=tr)
    targets = [out]
    if copy_to_actor_sync:
        for path in _search_cfg_targets():
            if path not in targets:
                targets.append(path)
    written = _write_payload_to_targets(payload, targets)
    smb_out: Path | None = None
    share_path = Path(share_actor_sync_dir()) / ACTOR_SYNC_SEARCH_CFG_NAME
    if str(share_path) in written:
        smb_out = share_path
    elif copy_to_actor_sync:
        smb_out = actor_sync_search_cfg_path()
    return out, smb_out
