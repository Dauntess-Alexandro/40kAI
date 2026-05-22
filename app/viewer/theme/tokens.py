"""Map shared ``theme/tokens.json`` to viewer ``Theme`` colour names."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from PySide6 import QtGui

from app.viewer.config import load_viewer_config, viewer_flag
from theme.loader import ThemeTokenError, load_tokens


@dataclass(frozen=True)
class ViewerPalette:
    background: QtGui.QColor
    panel: QtGui.QColor
    panel_alt: QtGui.QColor
    grid: QtGui.QColor
    text: QtGui.QColor
    muted: QtGui.QColor
    accent: QtGui.QColor
    accent_dark: QtGui.QColor
    outline: QtGui.QColor
    player: QtGui.QColor
    model: QtGui.QColor
    objective: QtGui.QColor
    selection: QtGui.QColor
    highlight: QtGui.QColor
    ui_font_family: str
    ui_font_size: int
    header_font_family: str
    header_font_size: int
    mono_font_family: str
    mono_font_size: int
    radius_sm: int
    radius_md: int
    radius_btn: int
    radius_groupbox: int
    spacing_xs: int
    spacing_sm: int
    spacing_md: int
    spacing_lg: int
    spacing_xl: int


def _q(hex_value: str) -> QtGui.QColor:
    return QtGui.QColor(hex_value)


def _int_val(data: Dict[str, Any], key: str, default: int) -> int:
    try:
        return int(data.get(key, default))
    except (TypeError, ValueError):
        return default


def palette_from_tokens(tokens: Optional[Dict[str, Any]] = None) -> ViewerPalette:
    data = tokens if tokens is not None else load_tokens()
    color = data.get("color") or {}
    bg = color.get("bg") or {}
    border = color.get("border") or {}
    text = color.get("text") or {}
    accent = color.get("accent") or {}
    game = color.get("game") or {}
    font_ui = (data.get("font") or {}).get("ui") or {}
    font_viewer = (data.get("font") or {}).get("viewerBody") or {}
    font_data = (data.get("font") or {}).get("data") or {}
    radius = data.get("radius") or {}
    spacing = data.get("spacing") or {}

    border_muted = str(border.get("borderMuted", "#334155"))
    return ViewerPalette(
        background=_q(str(bg.get("bgBase", "#0F172A"))),
        panel=_q(str(bg.get("bgSurface", "#131b2d"))),
        panel_alt=_q(str(bg.get("bgElevated", "#1E293B"))),
        grid=_q(border_muted),
        text=_q(str(text.get("textPrimary", "#d7dde7"))),
        muted=_q(str(text.get("textSecondary", "#98a4b8"))),
        accent=_q(str(accent.get("accentPrimaryAction", "#b88a26"))),
        accent_dark=_q(border_muted),
        outline=_q(str(bg.get("bgBase", "#0F172A"))),
        player=_q(str(game.get("player", accent.get("accentP1", "#2f6ed8")))),
        model=_q(str(game.get("model", accent.get("accentP2", "#cf3f3f")))),
        objective=_q(str(game.get("objective", accent.get("accentPrimaryAction", "#b88a26")))),
        selection=_q(str(game.get("selection", "#d7b66f"))),
        highlight=_q(str(accent.get("accentP1", "#2f6ed8"))),
        ui_font_family=str(font_viewer.get("family") or font_ui.get("family") or "Segoe UI"),
        ui_font_size=_int_val(font_viewer, "sizePx", _int_val(font_ui, "sizePx", 11)),
        header_font_family=str(font_ui.get("family") or "Rajdhani"),
        header_font_size=_int_val(font_ui, "sizePx", 14),
        mono_font_family=str(font_data.get("family") or "Consolas"),
        mono_font_size=_int_val(font_data, "sizePx", 12),
        radius_sm=_int_val(radius, "sm", 8),
        radius_md=_int_val(radius, "md", 12),
        radius_btn=_int_val(radius, "button", 4),
        radius_groupbox=_int_val(radius, "groupBox", 6),
        spacing_xs=_int_val(spacing, "xs", 6),
        spacing_sm=_int_val(spacing, "sm", 8),
        spacing_md=_int_val(spacing, "md", 12),
        spacing_lg=_int_val(spacing, "lg", 16),
        spacing_xl=_int_val(spacing, "xl", 20),
    )


def viewer_palette_v2_enabled(cfg: Optional[Dict[str, Any]] = None) -> bool:
    return viewer_flag("viewer.theme.v2", cfg)


_LEGACY_PALETTE = ViewerPalette(
    background=_q("#1c1a17"),
    panel=_q("#2b2824"),
    panel_alt=_q("#332f2a"),
    grid=_q("#3d382f"),
    text=_q("#e7dfd4"),
    muted=_q("#b3a99c"),
    accent=_q("#b08d57"),
    accent_dark=_q("#6f4b2a"),
    outline=_q("#140f0b"),
    player=_q("#6a8f3a"),
    model=_q("#4a7aa8"),
    objective=_q("#d1a21b"),
    selection=_q("#d7b66f"),
    highlight=_q("#4a7aa8"),
    ui_font_family="Inter",
    ui_font_size=10,
    header_font_family="Inter",
    header_font_size=12,
    mono_font_family="Consolas",
    mono_font_size=10,
    radius_sm=6,
    radius_md=8,
    radius_btn=4,
    radius_groupbox=6,
    spacing_xs=6,
    spacing_sm=8,
    spacing_md=12,
    spacing_lg=16,
    spacing_xl=20,
)


def resolve_palette(cfg: Optional[Dict[str, Any]] = None) -> ViewerPalette:
    if viewer_palette_v2_enabled(cfg):
        try:
            return palette_from_tokens()
        except (ThemeTokenError, OSError, ValueError) as exc:
            print(f"[VIEWER] theme v2 load failed ({exc}); using legacy palette.", flush=True)
    return _LEGACY_PALETTE
