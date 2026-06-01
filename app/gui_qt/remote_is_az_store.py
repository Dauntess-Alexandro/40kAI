"""Local config for AZ remote inference server (separate from GMZ remote_is.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_REMOTE_IS_AZ: dict[str, Any] = {
    "enabled": False,
    "user_enabled_lan": False,
    "host": "127.0.0.1",
    "port": 5556,  # отдельный от GMZ (5555)
    "timeout": 5.0,
    "auth_token": "",
    "weights_share_path": "",
    "smb_unc_hint": "",
}


def normalize_remote_is_az(data: dict[str, Any]) -> dict[str, Any]:
    """LAN активен только при user_enabled_lan (как GMZ remote_is_store)."""
    merged = dict(DEFAULT_REMOTE_IS_AZ)
    merged.update(data or {})
    user = bool(merged.get("user_enabled_lan", False))
    if bool(merged.get("enabled", False)) and not user:
        user = False
    merged["user_enabled_lan"] = user
    merged["enabled"] = user
    return merged


def remote_is_az_lan_active(data: dict[str, Any]) -> bool:
    return bool(normalize_remote_is_az(data).get("user_enabled_lan", False))


def remote_is_az_config_path(repo_root: str | Path) -> Path:
    return Path(repo_root) / "runtime" / "state" / "remote_is_az.json"


def load_remote_is_az(repo_root: str | Path) -> dict[str, Any]:
    path = remote_is_az_config_path(repo_root)
    if not path.is_file():
        return normalize_remote_is_az({})
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return normalize_remote_is_az({})
    if not isinstance(raw, dict):
        return normalize_remote_is_az({})
    merged = normalize_remote_is_az(raw)
    if raw.get("enabled") != merged.get("enabled") or raw.get("user_enabled_lan") != merged.get(
        "user_enabled_lan"
    ):
        try:
            save_remote_is_az(repo_root, merged)
        except OSError:
            pass
    return merged


def save_remote_is_az(repo_root: str | Path, data: dict[str, Any]) -> None:
    path = remote_is_az_config_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = normalize_remote_is_az(data)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
