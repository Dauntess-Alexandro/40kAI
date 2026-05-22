"""Viewer configuration and feature flags."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from project_paths import APP_DIR

VIEWER_CONFIG_PATH = str(APP_DIR / "viewer" / "viewer_config.json")

_DEFAULTS: Dict[str, Any] = {
    "cell_size": 24,
    "unit_icon_scale": 2.75,
    "model_icon_scale": 0.75,
    "terrain_barrel_cell_scale": 0.92,
    "move_base_ms": 155,
    "move_per_cell_ms": 88,
    "move_cap_ms": 920,
    "move_seq_floor_new_step_ms": 260,
    "move_seq_floor_default_ms": 180,
    "move_ease": "smoothstep",
    "fx_quality": "high",
    "flags": {
        "viewer.theme.v2": True,
        "viewer.controller.v1": True,
        "viewer.render.layers_v2": True,
        "viewer.fx.v2": True,
        "viewer.ui.qml_panels": True,
        "viewer.debug.overlay": False,
        "viewer.shaders.highlights": False,
    },
}


def load_viewer_config() -> Dict[str, Any]:
    cfg = dict(_DEFAULTS)
    flags_default = dict(_DEFAULTS["flags"])
    try:
        with open(VIEWER_CONFIG_PATH, "r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return cfg
    if not isinstance(loaded, dict):
        return cfg
    for key, value in loaded.items():
        if key == "flags" and isinstance(value, dict):
            flags_default.update(value)
            cfg["flags"] = flags_default
        else:
            cfg[key] = value
    cfg["flags"] = flags_default
    return cfg


def viewer_flag(name: str, cfg: Optional[Dict[str, Any]] = None) -> bool:
    """Resolve a migration flag (config ``flags`` block or env ``VIEWER_FLAG_<NAME>``)."""
    env_key = "VIEWER_FLAG_" + name.upper().replace(".", "_").replace("-", "_")
    env_raw = os.environ.get(env_key, "").strip().lower()
    if env_raw in {"1", "true", "yes", "on"}:
        return True
    if env_raw in {"0", "false", "no", "off"}:
        return False
    config = cfg if cfg is not None else load_viewer_config()
    flags = config.get("flags")
    if isinstance(flags, dict) and name in flags:
        return bool(flags[name])
    if name in config:
        return bool(config[name])
    return False
