"""Load and validate ``theme/tokens.json`` for Python and QML consumers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from project_paths import PROJECT_ROOT


class ThemeTokenError(ValueError):
    pass


TOKENS_PATH = PROJECT_ROOT / "theme" / "tokens.json"
SCHEMA_PATH = PROJECT_ROOT / "theme" / "tokens.schema.json"

_REQUIRED_COLOR_PATHS: Tuple[Tuple[str, ...], ...] = (
    ("bg", "bgBase"),
    ("bg", "bgSurface"),
    ("bg", "bgElevated"),
    ("text", "textPrimary"),
    ("text", "textSecondary"),
    ("accent", "accentP1"),
    ("accent", "accentP2"),
    ("accent", "accentPrimaryAction"),
)


def _dig(mapping: Mapping[str, Any], path: Tuple[str, ...]) -> Any:
    cur: Any = mapping
    for key in path:
        if not isinstance(cur, Mapping) or key not in cur:
            raise ThemeTokenError(f"Missing token path: {'.'.join(path)}")
        cur = cur[key]
    return cur


def _hex_color(value: Any, path: str) -> str:
    text = str(value).strip()
    if not text.startswith("#") or len(text) not in (4, 7, 9):
        raise ThemeTokenError(f"Expected #RRGGBB color at {path}, got {value!r}")
    return text


def validate_tokens(data: Mapping[str, Any]) -> None:
    if not isinstance(data, Mapping):
        raise ThemeTokenError("tokens root must be an object")
    if "schema_version" not in data:
        raise ThemeTokenError("schema_version is required")
    color = data.get("color")
    if not isinstance(color, Mapping):
        raise ThemeTokenError("color section must be an object")
    for path in _REQUIRED_COLOR_PATHS:
        raw = _dig(color, path)
        _hex_color(raw, ".".join(("color",) + path))


def load_tokens(path: Optional[Path] = None) -> Dict[str, Any]:
    token_path = path or TOKENS_PATH
    with token_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ThemeTokenError("tokens.json must be a JSON object")
    validate_tokens(data)
    return data


def load_tokens_flat_for_qml(path: Optional[Path] = None) -> Dict[str, str]:
    """Flatten colors for QML ``themeTokens`` context property (Main.qml keys)."""
    data = load_tokens(path)
    color = data.get("color") or {}
    bg = color.get("bg") or {}
    border = color.get("border") or {}
    text = color.get("text") or {}
    accent = color.get("accent") or {}

    flat: Dict[str, str] = {
        "bgBase": _hex_color(bg.get("bgBase"), "bg.bgBase"),
        "bgSurface": _hex_color(bg.get("bgSurface"), "bg.bgSurface"),
        "bgElevated": _hex_color(bg.get("bgElevated"), "bg.bgElevated"),
        "borderMuted": _hex_color(
            border.get("borderMuted", "#334155"),
            "border.borderMuted",
        ),
        "textPrimary": _hex_color(text.get("textPrimary"), "text.textPrimary"),
        "textSecondary": _hex_color(text.get("textSecondary"), "text.textSecondary"),
        "accentP1": _hex_color(accent.get("accentP1"), "accent.accentP1"),
        "accentP2": _hex_color(accent.get("accentP2"), "accent.accentP2"),
        "accentPrimaryAction": _hex_color(
            accent.get("accentPrimaryAction"),
            "accent.accentPrimaryAction",
        ),
        "accentDanger": _hex_color(
            accent.get("accentDanger", "#a35345"),
            "accent.accentDanger",
        ),
        "accentGhost": _hex_color(
            accent.get("accentGhost", "#6f7d92"),
            "accent.accentGhost",
        ),
    }
    return flat


def relative_luminance(hex_color: str) -> float:
    """WCAG relative luminance for #RRGGBB."""
    h = hex_color.lstrip("#")
    if len(h) == 6:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    else:
        raise ThemeTokenError(f"Unsupported color for luminance: {hex_color}")

    def channel(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    l1 = relative_luminance(fg_hex)
    l2 = relative_luminance(bg_hex)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
