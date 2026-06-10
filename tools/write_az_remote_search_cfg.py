#!/usr/bin/env python
"""PC1: write az_remote_search_cfg.json from GUI roster + hyperparams.json.

Содержит obs_dim, action_sizes и арх сети (hidden_size, num_layers, value_ensemble),
которые нужны az_remote_inference_server на ПК2 чтобы собрать совместимую сеть.
Копия кладётся в artifacts/models/actor_sync/ (SMB-папка learner).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
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
        except Exception:
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


def _dims_from_latest_checkpoint(ckpt_dir: Path) -> tuple[int, list[int], str]:
    if not ckpt_dir.is_dir():
        return 0, [], ""
    ckpts = sorted(ckpt_dir.glob("checkpoint_ep*.pth"), key=os.path.getmtime, reverse=True)
    if not ckpts:
        return 0, [], ""
    path = ckpts[0]
    try:
        import torch

        payload = torch.load(path, map_location="cpu", weights_only=False)
        contract = payload.get("env_contract", {}) if isinstance(payload, dict) else {}
        obs, acts = _dims_from_env_contract(contract)
        if obs > 0 and acts:
            return obs, acts, str(path)
    except Exception as exc:
        print(f"[WARN] checkpoint {path}: {exc}")
    return 0, [], ""


def _dims_from_latest_agent_contract(agents_root: Path) -> tuple[int, list[int], str]:
    if not agents_root.is_dir():
        return 0, [], ""
    candidates = sorted(
        agents_root.glob("**/env_contract.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for path in candidates:
        contract = _load_json(path)
        obs, acts = _dims_from_env_contract(contract)
        if obs > 0 and acts:
            return obs, acts, str(path)
    return 0, [], ""


def _dims_from_roster_bootstrap() -> tuple[int, list[int], str]:
    """Поднять env по train_data / roster — без checkpoint."""
    try:
        import gymnasium as gym
        import numpy as np

        import train as train_mod

        roster = train_mod._load_roster_config()
        b_len = int(roster["b_len"])
        b_hei = int(roster["b_hei"])
        enemy, model = train_mod._build_units_from_config(roster, b_len, b_hei)
        env = gym.make(
            "40kAI-v0",
            disable_env_checker=True,
            enemy=enemy,
            model=model,
            b_len=b_len,
            b_hei=b_hei,
        )
        state0, _ = env.reset(options={"m": model, "e": enemy, "trunc": True})
        if isinstance(state0, (dict,)):
            n_obs = len(list(state0.values()))
        else:
            n_obs = int(np.asarray(state0).shape[0])
        n_actions = train_mod.action_sizes_from_env(env, len(model))
        try:
            env.close()
        except Exception:
            pass
        if n_obs > 0 and n_actions:
            return int(n_obs), [int(x) for x in n_actions], "roster_bootstrap"
    except Exception as exc:
        print(f"[WARN] roster bootstrap: {exc}")
    return 0, [], ""


def main() -> int:
    hp = _load_json(_REPO_ROOT / "hyperparams.json")
    az = hp.get("alphazero_tree", {}) if isinstance(hp, dict) else {}

    tried: list[str] = []
    obs_dim = 0
    action_sizes: list[int] = []
    source = ""

    for algo in ("alphazero_tree", "alphazero_proxy"):
        ckpt_dir = _REPO_ROOT / "artifacts" / "models" / algo
        obs, acts, src = _dims_from_latest_checkpoint(ckpt_dir)
        tried.append(f"{ckpt_dir} ({len(list(ckpt_dir.glob('checkpoint_ep*.pth')))} checkpoint_ep*.pth)")
        if obs > 0 and acts:
            obs_dim, action_sizes, source = obs, acts, src
            break

    if obs_dim <= 0 or not action_sizes:
        agents_root = _REPO_ROOT / "artifacts" / "models" / "agents"
        obs, acts, src = _dims_from_latest_agent_contract(agents_root)
        tried.append(f"{agents_root}/**/env_contract.json")
        if obs > 0 and acts:
            obs_dim, action_sizes, source = obs, acts, src

    if obs_dim <= 0 or not action_sizes:
        obs, acts, src = _dims_from_roster_bootstrap()
        tried.append("train_data/roster bootstrap")
        if obs > 0 and acts:
            obs_dim, action_sizes, source = obs, acts, src

    if obs_dim <= 0 or not action_sizes:
        print(
            "[ERROR] obs_dim/action_sizes не определены.\n"
            "Проверено:\n  - " + "\n  - ".join(tried) + "\n"
            "Частые причины:\n"
            "  1) SAVE_EVERY=0 — периодические checkpoint_ep*.pth не пишутся "
            "(остаётся только final agent в artifacts/models/agents/).\n"
            "  2) Папка artifacts/models на другом диске / 40KAI_INSTALL_ROOT.\n"
            "  3) Train не дошёл до сохранения агента (прерван до конца).\n"
            "Что делать: убедитесь что есть train_data.txt, или задайте SAVE_EVERY>=50 и "
            "дождитесь одного checkpoint, или завершите один полный прогон AZ."
        )
        return 1

    # Единый писатель (тот же формат/пути, что и авто-запись из train.py).
    from core.models.az_rollout_sink import write_az_remote_search_cfg

    written = write_az_remote_search_cfg(
        obs_dim=int(obs_dim),
        action_sizes=list(action_sizes),
        hidden_size=int(az.get("hidden_size", 256)),
        num_layers=int(az.get("num_layers", 2)),
        n_value_ensemble=int(az.get("value_ensemble", 1)),
        num_simulations=int(az.get("mcts_simulations", 32)),
        sources=["hyperparams.json:alphazero_tree", f"dims_from={source}"],
    )
    if not written:
        print("[ERROR] не удалось записать ни одного файла az_remote_search_cfg.json")
        return 1
    for path in written:
        print(f"[OK] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
