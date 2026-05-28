"""Local config for GMZ remote inference server (not in hyperparams.json)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_REMOTE_IS: dict[str, Any] = {
    "enabled": False,
    # Явное согласие пользователя (два ПК). Без этого LAN не включается при загрузке.
    "user_enabled_lan": False,
    "host": "127.0.0.1",
    "port": 5555,
    "timeout": 5.0,
    "auth_token": "",
    "weights_share_path": "",
    "smb_unc_hint": "",
}


def normalize_remote_is(data: dict[str, Any]) -> dict[str, Any]:
    """LAN активен только если user_enabled_lan. Старый enabled=true без флага → выкл."""
    merged = dict(DEFAULT_REMOTE_IS)
    merged.update(data)
    user = bool(merged.get("user_enabled_lan", False))
    if bool(merged.get("enabled", False)) and not user:
        user = False
    merged["user_enabled_lan"] = user
    merged["enabled"] = user
    return merged


def remote_is_lan_active(data: dict[str, Any]) -> bool:
    return bool(normalize_remote_is(data).get("user_enabled_lan", False))


def remote_is_config_path(repo_root: str | Path) -> Path:
    return Path(repo_root) / "runtime" / "state" / "remote_is.json"


def load_remote_is(repo_root: str | Path) -> dict[str, Any]:
    path = remote_is_config_path(repo_root)
    if not path.is_file():
        return normalize_remote_is({})
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return normalize_remote_is({})
    if not isinstance(raw, dict):
        return normalize_remote_is({})
    before = dict(raw)
    merged = normalize_remote_is(raw)
    if before.get("enabled") != merged.get("enabled") or before.get("user_enabled_lan") != merged.get(
        "user_enabled_lan"
    ):
        try:
            save_remote_is(repo_root, merged)
        except OSError:
            pass
    return merged


def save_remote_is(repo_root: str | Path, data: dict[str, Any]) -> None:
    path = remote_is_config_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = normalize_remote_is(data)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def apply_remote_is_to_qsettings(settings: Any, data: dict[str, Any]) -> None:
    settings.setValue("remote_is/enabled", bool(data.get("enabled", False)))
    settings.setValue("remote_is/host", str(data.get("host", "127.0.0.1")))
    settings.setValue("remote_is/port", int(data.get("port", 5555)))
    settings.setValue("remote_is/timeout", float(data.get("timeout", 5.0)))
    settings.setValue("remote_is/auth_token", str(data.get("auth_token", "")))
    settings.setValue("remote_is/weights_share_path", str(data.get("weights_share_path", "")))
    settings.setValue("remote_is/smb_unc_hint", str(data.get("smb_unc_hint", "")))


def load_remote_is_from_qsettings(settings: Any) -> dict[str, Any]:
    data = dict(DEFAULT_REMOTE_IS)
    if settings.contains("remote_is/enabled"):
        data["enabled"] = bool(int(settings.value("remote_is/enabled", 0) or 0))
    if settings.contains("remote_is/host"):
        data["host"] = str(settings.value("remote_is/host", data["host"]) or data["host"])
    if settings.contains("remote_is/port"):
        data["port"] = int(settings.value("remote_is/port", data["port"]) or data["port"])
    if settings.contains("remote_is/timeout"):
        data["timeout"] = float(settings.value("remote_is/timeout", data["timeout"]) or data["timeout"])
    if settings.contains("remote_is/auth_token"):
        data["auth_token"] = str(settings.value("remote_is/auth_token", "") or "")
    if settings.contains("remote_is/weights_share_path"):
        data["weights_share_path"] = str(settings.value("remote_is/weights_share_path", "") or "")
    if settings.contains("remote_is/smb_unc_hint"):
        data["smb_unc_hint"] = str(settings.value("remote_is/smb_unc_hint", "") or "")
    return data
