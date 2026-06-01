#!/usr/bin/env python
"""PC1: write az_remote_search_cfg.json from GUI roster + hyperparams.json.

Содержит obs_dim, action_sizes и арх сети (hidden_size, num_layers, value_ensemble),
которые нужны az_remote_inference_server на ПК2 чтобы собрать совместимую сеть.
Копия кладётся в artifacts/models/actor_sync/ (SMB-папка learner).
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
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


def main() -> int:
    hp = _load_json(_REPO_ROOT / "hyperparams.json")
    az = hp.get("alphazero_tree", {}) if isinstance(hp, dict) else {}

    # obs_dim / action_sizes требуют поднять env по ростеру. Чтобы не дублировать
    # тяжёлую логику train.py, читаем из последнего env_contract в checkpoint, если есть.
    obs_dim = 0
    action_sizes: list[int] = []
    ckpt_dir = _REPO_ROOT / "artifacts" / "models" / "alphazero_tree"
    if ckpt_dir.is_dir():
        ckpts = sorted(ckpt_dir.glob("checkpoint_ep*.pth"), key=os.path.getmtime, reverse=True)
        if ckpts:
            try:
                import torch
                payload = torch.load(ckpts[0], map_location="cpu", weights_only=False)
                contract = payload.get("env_contract", {}) if isinstance(payload, dict) else {}
                obs_dim = int(contract.get("n_observations", 0) or 0)
                action_sizes = [int(x) for x in (contract.get("n_actions", []) or [])]
            except Exception as exc:
                print(f"[WARN] не удалось прочитать env_contract из checkpoint: {exc}")

    if obs_dim <= 0 or not action_sizes:
        print(
            "[ERROR] obs_dim/action_sizes не определены. "
            "Сначала запустите train (создастся checkpoint с env_contract), "
            "затем повторите write_az_remote_search_cfg."
        )
        return 1

    cfg = {
        "obs_dim": int(obs_dim),
        "action_sizes": list(action_sizes),
        "hidden_size": int(az.get("hidden_size", 256)),
        "num_layers": int(az.get("num_layers", 2)),
        "n_value_ensemble": int(az.get("value_ensemble", 1)),
        "num_simulations": int(az.get("mcts_simulations", 32)),
        "_generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "_sources": ["hyperparams.json:alphazero_tree", "checkpoint env_contract"],
    }

    out_state = _REPO_ROOT / "runtime" / "state" / "az_remote_search_cfg.json"
    out_state.parent.mkdir(parents=True, exist_ok=True)
    out_state.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] {out_state}")

    out_smb = _REPO_ROOT / "artifacts" / "models" / "actor_sync" / "az_remote_search_cfg.json"
    try:
        out_smb.parent.mkdir(parents=True, exist_ok=True)
        out_smb.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] {out_smb} (SMB copy)")
    except Exception as exc:
        print(f"[WARN] не удалось записать SMB-копию: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
