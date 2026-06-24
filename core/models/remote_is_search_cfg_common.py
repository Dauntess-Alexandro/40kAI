"""Общая логика search_cfg для remote inference server (ПК1↔ПК2)."""
from __future__ import annotations

import json
import os
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from project_paths import ARTIFACTS_MODELS_DIR, RUNTIME_STATE_DIR, TRAIN_DATA_PATH, share_actor_sync_dir

# Единый снимок ростера на SMB; smz_train_data.json — legacy.
TRAIN_DATA_SNAPSHOT_NAME = "remote_is_train_data.json"
LEGACY_TRAIN_DATA_SNAPSHOT_NAMES = ("smz_train_data.json",)


@dataclass(frozen=True)
class RemoteIsSmbPaths:
    actor_sync_dir: str
    search_cfg_path: str
    weights_path: str


@dataclass(frozen=True)
class RemoteIsEnsureResult:
    ok: bool
    message: str
    search_cfg_path: str = ""
    weights_path: str = ""
    action: str = ""


def actor_sync_of(share_root: str) -> str:
    base = str(share_root or "").rstrip("\\/")
    if not base:
        return share_actor_sync_dir()
    if os.path.basename(base).lower() == "actor_sync":
        return base
    return os.path.join(base, "actor_sync")


def first_existing_file(*candidates: str) -> str | None:
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def is_valid_search_cfg(path: str) -> bool:
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return False
    obs_dim = int(data.get("obs_dim", 0) or 0)
    action_sizes = data.get("action_sizes") or []
    return obs_dim > 0 and bool(action_sizes)


def load_roster_dict(roster_path: Path) -> dict[str, Any]:
    with roster_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"roster JSON не dict: {roster_path}")
    return data


def resolve_roster_path_on_share(actor_sync_dir: str) -> Path | None:
    for name in (TRAIN_DATA_SNAPSHOT_NAME, *LEGACY_TRAIN_DATA_SNAPSHOT_NAMES):
        candidate = Path(actor_sync_dir) / name
        if candidate.is_file():
            return candidate
    return None


def load_roster_for_search(roster_path: Path | None = None, *, actor_sync_dir: str | None = None) -> dict[str, Any]:
    if roster_path is not None and roster_path.is_file():
        roster = load_roster_dict(roster_path)
        if "b_len" in roster and "enemy_units" in roster:
            return roster
        if roster_path.resolve() == Path(TRAIN_DATA_PATH).resolve():
            import train as tr  # noqa: WPS433

            return tr._load_roster_config()
        raise ValueError(
            "Снимок ростера на шаре устарел. Откройте Qt GUI на ПК1 — search_cfg обновится автоматически."
        )
    if actor_sync_dir:
        snap = resolve_roster_path_on_share(actor_sync_dir)
        if snap is not None:
            return load_roster_for_search(snap)
    local = Path(TRAIN_DATA_PATH)
    if local.is_file():
        return load_roster_for_search(local)
    raise FileNotFoundError(
        "Нет runtime/state/data.json и снимка ростера на шаре. "
        "Откройте Qt GUI на ПК1 — ростер запишется на шару автоматически."
    )


def copy_train_data_snapshot(target_actor_sync: str, roster_path: Path) -> None:
    dest = Path(target_actor_sync) / TRAIN_DATA_SNAPSHOT_NAME
    src = roster_path.resolve()
    if src == dest.resolve():
        return
    roster = load_roster_for_search(roster_path)
    text = json.dumps(roster, indent=2, ensure_ascii=False, default=str) + "\n"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")


def resolve_smb_paths(
    share_root: str,
    *,
    search_cfg_name: str,
    weights_name: str,
) -> RemoteIsSmbPaths:
    actor_sync = actor_sync_of(share_root)
    base = str(share_root or "").rstrip("\\/")
    search_cfg = first_existing_file(
        os.path.join(actor_sync, search_cfg_name),
        os.path.join(base, search_cfg_name),
    )
    weights = first_existing_file(
        os.path.join(actor_sync, weights_name),
        os.path.join(base, weights_name),
    )
    return RemoteIsSmbPaths(
        actor_sync_dir=actor_sync,
        search_cfg_path=search_cfg or os.path.join(actor_sync, search_cfg_name),
        weights_path=weights or os.path.join(actor_sync, weights_name),
    )


def search_cfg_local_targets(
    search_cfg_name: str,
    *,
    extra_actor_sync: str | None = None,
) -> list[Path]:
    targets: list[Path] = [Path(RUNTIME_STATE_DIR) / search_cfg_name]
    for directory in (share_actor_sync_dir(), str(Path(ARTIFACTS_MODELS_DIR) / "actor_sync")):
        candidate = Path(directory) / search_cfg_name
        if candidate not in targets:
            targets.append(candidate)
    if extra_actor_sync:
        candidate = Path(extra_actor_sync) / search_cfg_name
        if candidate not in targets:
            targets.append(candidate)
    return targets


def measure_env_dims_from_roster(roster_config: dict, build_units_from_config) -> tuple[int, list[int]]:
    import collections

    import gymnasium as gym
    import numpy as np

    from core.engine.mission import deploy_for_mission, normalize_mission_name, post_deploy_setup
    from core.models.action_contract import action_sizes_from_env

    b_len = int(roster_config["b_len"])
    b_hei = int(roster_config["b_hei"])
    mission_name = normalize_mission_name(roster_config.get("mission", "only_war"))

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


def write_payload_to_targets(payload: dict[str, Any], targets: list[Path]) -> list[str]:
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    written: list[str] = []
    for path in targets:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            written.append(str(path))
        except OSError:
            continue
    return written


def current_env_obs_dim(actor_sync_dir: str | None = None) -> int:
    """Текущий obs_dim env (с учётом phase_obs). 0 при невозможности измерить (тогда сверка пропускается)."""
    try:
        import train as tr  # noqa: WPS433

        roster = load_roster_for_search(actor_sync_dir=actor_sync_dir)
        obs_dim, _ = measure_env_dims_from_roster(roster, tr._build_units_from_config)
        return int(obs_dim)
    except Exception:
        return 0


def _obs_dim_requires_republish(paths: RemoteIsSmbPaths, current_obs_dim_fn) -> bool:
    """True, если obs_dim существующего cfg не совпадает с текущим env → нужно перепубликовать.

    Побочно: при подтверждённом несовпадении удаляет устаревшие веса (форма не сойдётся),
    чтобы сервер сгенерил bootstrap заново. Любая ошибка измерения → False (откат к старому).
    """
    if current_obs_dim_fn is None:
        return False
    try:
        cur = int(current_obs_dim_fn() or 0)
        with open(paths.search_cfg_path, encoding="utf-8") as handle:
            cfg_obs = int(json.load(handle).get("obs_dim", 0) or 0)
    except Exception:
        return False
    if cur > 0 and cfg_obs > 0 and cur != cfg_obs:
        print(
            f"[REMOTE_IS] obs_dim cfg={cfg_obs} != env={cur} → перепубликую search_cfg "
            "и удаляю устаревшие latest_*_policy.pth.",
            flush=True,
        )
        try:
            if os.path.isfile(paths.weights_path):
                os.remove(paths.weights_path)
        except OSError:
            pass
        return True
    return False


def ensure_remote_search_cfg(
    share_root: str,
    *,
    search_cfg_name: str,
    publish_from_repo: Callable[..., list[str]],
    resolve_paths: Callable[[str], RemoteIsSmbPaths],
    local_targets: Callable[..., list[Path]],
    current_obs_dim_fn: Callable[[], int] | None = None,
) -> RemoteIsEnsureResult:
    paths = resolve_paths(share_root)
    if os.path.isfile(paths.search_cfg_path) and is_valid_search_cfg(paths.search_cfg_path):
        if not _obs_dim_requires_republish(paths, current_obs_dim_fn):
            return RemoteIsEnsureResult(
                ok=True,
                message=f"search_cfg на месте: {paths.search_cfg_path}",
                search_cfg_path=paths.search_cfg_path,
                weights_path=paths.weights_path,
                action="found",
            )

    try:
        written = publish_from_repo(
            extra_actor_sync=paths.actor_sync_dir,
            snapshot_actor_sync=paths.actor_sync_dir,
            share_only=True,
        )
        target = paths.search_cfg_path
        if not os.path.isfile(target) and written:
            os.makedirs(paths.actor_sync_dir, exist_ok=True)
            shutil.copy2(written[0], target)
        final_path = target if os.path.isfile(target) else (written[0] if written else "")
        if final_path and is_valid_search_cfg(final_path):
            return RemoteIsEnsureResult(
                ok=True,
                message=f"search_cfg сгенерирован: {final_path}",
                search_cfg_path=final_path,
                weights_path=paths.weights_path,
                action="generated",
            )
    except FileNotFoundError:
        pass
    except Exception:
        pass

    for src in local_targets(extra_actor_sync=paths.actor_sync_dir):
        src_s = str(src)
        if os.path.isfile(src_s) and is_valid_search_cfg(src_s):
            try:
                os.makedirs(paths.actor_sync_dir, exist_ok=True)
                shutil.copy2(src_s, paths.search_cfg_path)
            except OSError as exc:
                return RemoteIsEnsureResult(
                    ok=False,
                    message=f"Не удалось скопировать search_cfg на шару: {exc}",
                )
            return RemoteIsEnsureResult(
                ok=True,
                message=f"search_cfg скопирован на шару: {paths.search_cfg_path}",
                search_cfg_path=paths.search_cfg_path,
                weights_path=paths.weights_path,
                action="copied",
            )

    return RemoteIsEnsureResult(
        ok=False,
        message=(
            "search_cfg не найден на шаре и не удалось создать. "
            "Откройте Qt GUI на ПК1 — все search_cfg появятся на шаре автоматически."
        ),
    )
