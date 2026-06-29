"""Persistence for train-tab GUI preferences (mission selection, etc.)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.engine.mission import normalize_mission_name

MISSION_OPTIONS_DEFAULT = ("only_war", "annihilation")
QSETTINGS_MISSION_KEY = "train/selected_mission"


def _normalize_mission_choice(
    mission: str | None,
    options: tuple[str, ...] | list[str],
) -> str | None:
    raw = (mission or "").strip()
    if not raw:
        return None
    normalized = normalize_mission_name(raw)
    opts = {str(o).strip().lower() for o in options}
    if normalized in opts:
        return normalized
    return None


def load_selected_mission(
    settings: Any,
    *,
    data_json_path: str | Path | None = None,
    options: tuple[str, ...] | list[str] = MISSION_OPTIONS_DEFAULT,
    default: str = "only_war",
) -> str:
    if settings is not None and settings.contains(QSETTINGS_MISSION_KEY):
        saved = _normalize_mission_choice(
            str(settings.value(QSETTINGS_MISSION_KEY, "") or ""),
            options,
        )
        if saved:
            return saved
    if data_json_path is not None:
        path = Path(data_json_path)
        if path.is_file():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                payload = None
            if isinstance(payload, dict):
                saved = _normalize_mission_choice(str(payload.get("mission", "") or ""), options)
                if saved:
                    return saved
    fallback = _normalize_mission_choice(default, options)
    return fallback or str(options[0])


def save_selected_mission(
    settings: Any,
    mission: str,
    *,
    options: tuple[str, ...] | list[str] = MISSION_OPTIONS_DEFAULT,
) -> str:
    normalized = _normalize_mission_choice(mission, options) or "only_war"
    settings.setValue(QSETTINGS_MISSION_KEY, normalized)
    return normalized
