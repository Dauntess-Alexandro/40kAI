"""GAZ remote search_cfg: publish/ensure для remote IS (ПК1↔ПК2).

Gumbel AlphaZero использует ту же сеть AlphaZeroPolicyValueNet, что и AZ tree →
форма search_cfg (obs_dim/action_sizes/hidden_size/num_layers/n_value_ensemble)
идентична AZ. Отличия только в именах файлов и секции гиперпараметров:
  - cfg:   gaz_remote_search_cfg.json
  - веса:  latest_az_gumbel_az_policy.pth (пишет learner, _az_sync_tag="gumbel_az")
  - секция hyperparams: gumbel_az
Тонкий слой: переиспускает общие хелперы remote_is_search_cfg_common и
write_az_remote_search_cfg (с filename), не дублируя логику AZ.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from core.models.az_rollout_sink import write_az_remote_search_cfg
from core.models.remote_is_search_cfg_common import (
    copy_train_data_snapshot,
    ensure_remote_search_cfg,
    load_roster_for_search,
    measure_env_dims_from_roster,
    resolve_smb_paths,
    search_cfg_local_targets,
)
from project_paths import ARTIFACTS_MODELS_DIR, PROJECT_ROOT, TRAIN_DATA_PATH

SEARCH_CFG_NAME = "gaz_remote_search_cfg.json"
WEIGHTS_NAME = "latest_az_gumbel_az_policy.pth"


def resolve_gaz_smb_paths(share_root: str):
    return resolve_smb_paths(share_root, search_cfg_name=SEARCH_CFG_NAME, weights_name=WEIGHTS_NAME)


def _load_hyperparams_gaz() -> dict[str, Any]:
    path = PROJECT_ROOT / "hyperparams.json"
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            gaz = data.get("gumbel_az", {}) if isinstance(data, dict) else {}
            return gaz if isinstance(gaz, dict) else {}
        except (OSError, json.JSONDecodeError):
            pass
    return {}


def _dims_from_env_contract(contract: dict) -> tuple[int, list[int]]:
    if not isinstance(contract, dict):
        return 0, []
    if contract.get("n_observations") and contract.get("n_actions"):
        try:
            obs = int(contract.get("n_observations", 0) or 0)
            acts = [int(x) for x in (contract.get("n_actions", []) or [])]
            if obs > 0 and acts:
                return obs, acts
        except (TypeError, ValueError):
            pass
    obs_sig = str(contract.get("obs_space_signature", "") or "")
    act_sig = str(contract.get("action_space_signature", "") or "")
    obs_dim = 0
    m_obs = re.match(r"vec:(\d+)", obs_sig)
    if m_obs:
        obs_dim = int(m_obs.group(1))
    action_sizes: list[int] = []
    if act_sig.startswith("heads:"):
        tail = act_sig.split(":", 1)[1].strip()
        if tail:
            action_sizes = [int(x) for x in tail.split(",") if str(x).strip().isdigit()]
    return obs_dim, action_sizes


def _dims_from_roster(*, actor_sync_dir: str | None) -> tuple[int, list[int]]:
    import train as tr  # noqa: WPS433

    roster = load_roster_for_search(actor_sync_dir=actor_sync_dir)
    obs_dim, action_sizes = measure_env_dims_from_roster(roster, tr._build_units_from_config)
    return int(obs_dim), [int(x) for x in action_sizes]


def _resolve_obs_action_sizes(*, actor_sync_dir: str | None, share_only: bool) -> tuple[int, list[int]]:
    # obs/action dims определяются env/ростером (не алго) — для GAZ те же, что для AZ.
    # Предпочитаем чекпойнт gumbel_az, далее любые AZ-чекпойнты/агентов, иначе ростер.
    if not share_only:
        for algo in ("gumbel_az", "alphazero_tree", "alphazero_proxy"):
            ckpt_dir = Path(ARTIFACTS_MODELS_DIR) / algo
            if ckpt_dir.is_dir():
                ckpts = sorted(ckpt_dir.glob("checkpoint_ep*.pth"), key=os.path.getmtime, reverse=True)
                if ckpts:
                    try:
                        import torch

                        payload = torch.load(ckpts[0], map_location="cpu", weights_only=False)
                        contract = payload.get("env_contract", {}) if isinstance(payload, dict) else {}
                        obs, acts = _dims_from_env_contract(contract)
                        if obs > 0 and acts:
                            return obs, acts
                    except Exception:
                        pass
        agents_root = Path(ARTIFACTS_MODELS_DIR) / "agents"
        if agents_root.is_dir():
            for path in sorted(agents_root.glob("**/env_contract.json"), key=os.path.getmtime, reverse=True):
                try:
                    contract = json.loads(path.read_text(encoding="utf-8"))
                    obs, acts = _dims_from_env_contract(contract)
                    if obs > 0 and acts:
                        return obs, acts
                except (OSError, json.JSONDecodeError):
                    continue
    return _dims_from_roster(actor_sync_dir=actor_sync_dir)


def publish_gaz_remote_search_cfg_from_repo(
    *,
    roster_path: str | Path | None = None,
    sources: list[str] | str | None = None,
    extra_actor_sync: str | None = None,
    snapshot_actor_sync: str | None = None,
    share_only: bool = False,
) -> list[str]:
    sync_dir = str(snapshot_actor_sync or extra_actor_sync or "")
    if roster_path is not None and Path(roster_path).is_file():
        copy_train_data_snapshot(sync_dir, Path(roster_path))
    elif sync_dir and not share_only and Path(TRAIN_DATA_PATH).is_file():
        copy_train_data_snapshot(sync_dir, Path(TRAIN_DATA_PATH))

    obs_dim, action_sizes = _resolve_obs_action_sizes(
        actor_sync_dir=sync_dir or None,
        share_only=share_only,
    )
    if obs_dim <= 0 or not action_sizes:
        raise FileNotFoundError("GAZ: obs_dim/action_sizes не определены из ростера/checkpoint.")

    gaz = _load_hyperparams_gaz()
    src_list = [sources] if isinstance(sources, str) else list(sources or ["repo:auto"])
    return write_az_remote_search_cfg(
        obs_dim=int(obs_dim),
        action_sizes=list(action_sizes),
        hidden_size=int(gaz.get("hidden_size", 256)),
        num_layers=int(gaz.get("num_layers", 2)),
        n_value_ensemble=int(gaz.get("value_ensemble", 1)),
        num_simulations=int(gaz.get("num_simulations", 32)),
        sources=src_list,
        filename=SEARCH_CFG_NAME,
    )


def ensure_gaz_remote_search_cfg(share_root: str):
    return ensure_remote_search_cfg(
        share_root,
        search_cfg_name=SEARCH_CFG_NAME,
        publish_from_repo=lambda **kw: publish_gaz_remote_search_cfg_from_repo(
            sources=["ensure_gaz_remote_search_cfg:auto"],
            **kw,
        ),
        resolve_paths=resolve_gaz_smb_paths,
        local_targets=lambda **kw: search_cfg_local_targets(SEARCH_CFG_NAME, **kw),
    )
