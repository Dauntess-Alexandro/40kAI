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
from project_paths import ARTIFACTS_MODELS_DIR, RUNTIME_STATE_DIR, TRAIN_DATA_PATH, ensure_runtime_dirs

ACTOR_SYNC_SEARCH_CFG_NAME = "gmz_remote_search_cfg.json"


def _measure_env_dims(roster_config: dict, build_units_from_config) -> tuple[int, list[int]]:
    """obs_dim и action_sizes — как в train._main_actor_learner_gumbel_muzero."""
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
