from __future__ import annotations

from typing import Any, Dict, Optional

from PySide6 import QtGui

from app.viewer.theme.tokens import ViewerPalette, resolve_palette

_active_palette: Optional[ViewerPalette] = None


class Theme:
    """Viewer colours and stylesheet; v2 palette from ``theme/tokens.json`` when flagged."""

    background = QtGui.QColor("#1c1a17")
    panel = QtGui.QColor("#2b2824")
    panel_alt = QtGui.QColor("#332f2a")
    grid = QtGui.QColor("#3d382f")
    text = QtGui.QColor("#e7dfd4")
    muted = QtGui.QColor("#b3a99c")
    accent = QtGui.QColor("#b08d57")
    accent_dark = QtGui.QColor("#6f4b2a")
    outline = QtGui.QColor("#140f0b")
    player = QtGui.QColor("#6a8f3a")
    model = QtGui.QColor("#4a7aa8")
    objective = QtGui.QColor("#d1a21b")
    selection = QtGui.QColor("#d7b66f")
    highlight = QtGui.QColor("#4a7aa8")
    _ui_font_family = "Inter"
    _ui_font_size = 10

    @classmethod
    def apply_from_config(cls, cfg: Optional[Dict[str, Any]] = None) -> ViewerPalette:
        global _active_palette
        palette = resolve_palette(cfg)
        _active_palette = palette
        cls.background = palette.background
        cls.panel = palette.panel
        cls.panel_alt = palette.panel_alt
        cls.grid = palette.grid
        cls.text = palette.text
        cls.muted = palette.muted
        cls.accent = palette.accent
        cls.accent_dark = palette.accent_dark
        cls.outline = palette.outline
        cls.player = palette.player
        cls.model = palette.model
        cls.objective = palette.objective
        cls.selection = palette.selection
        cls.highlight = palette.highlight
        cls._ui_font_family = palette.ui_font_family
        cls._ui_font_size = palette.ui_font_size
        return palette

    @classmethod
    def active_palette(cls) -> ViewerPalette:
        if _active_palette is None:
            return cls.apply_from_config()
        return _active_palette

    @classmethod
    def is_v2(cls, cfg: Optional[Dict[str, Any]] = None) -> bool:
        from app.viewer.theme.tokens import viewer_palette_v2_enabled

        return viewer_palette_v2_enabled(cfg)

    @staticmethod
    def font(size: Optional[int] = None, bold: bool = False):
        point = size if size is not None else Theme._ui_font_size
        font = QtGui.QFont(Theme._ui_font_family, pointSize=point)
        font.setBold(bold)
        return font

    @staticmethod
    def pen(color, width=1.0):
        pen = QtGui.QPen(color)
        pen.setWidthF(width)
        return pen

    @staticmethod
    def brush(color):
        return QtGui.QBrush(color)

    @staticmethod
    def stylesheet():
        radius_gb = 6
        radius_btn = 4
        return f"""
        QMainWindow {{
            background-color: {Theme.background.name()};
        }}
        QGroupBox {{
            border: 1px solid {Theme.accent_dark.name()};
            border-radius: {radius_gb}px;
            margin-top: 16px;
            padding: 8px;
            font-weight: 600;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 2px 8px;
            color: {Theme.accent.name()};
            background-color: {Theme.panel_alt.name()};
            border: 1px solid {Theme.accent_dark.name()};
            border-radius: {radius_btn}px;
        }}
        QLabel {{
            color: {Theme.text.name()};
        }}
        QTableWidget {{
            background-color: {Theme.panel.name()};
            alternate-background-color: {Theme.panel_alt.name()};
            gridline-color: {Theme.grid.name()};
            selection-background-color: {Theme.accent_dark.name()};
            selection-color: {Theme.text.name()};
            color: {Theme.text.name()};
            border: 1px solid {Theme.accent_dark.name()};
            border-radius: {radius_btn}px;
        }}
        QTableWidget::item {{
            color: {Theme.text.name()};
        }}
        QTableWidget::item:selected {{
            background-color: {Theme.accent_dark.name()};
            color: {Theme.text.name()};
        }}
        QHeaderView::section {{
            background-color: {Theme.panel_alt.name()};
            color: {Theme.accent.name()};
            border: 1px solid {Theme.accent_dark.name()};
            padding: 4px 6px;
        }}
        QPlainTextEdit, QTextEdit {{
            background-color: {Theme.panel.name()};
            border: 1px solid {Theme.accent_dark.name()};
            border-radius: {radius_btn}px;
            color: {Theme.text.name()};
        }}
        QToolButton {{
            background-color: {Theme.panel_alt.name()};
            border: 1px solid {Theme.accent_dark.name()};
            color: {Theme.text.name()};
            padding: 2px 6px;
        }}
        QToolButton:checked {{
            background-color: {Theme.accent_dark.name()};
            color: {Theme.accent.name()};
        }}
        QToolButton:hover {{
            background-color: {Theme.accent_dark.name()};
        }}
        QPushButton {{
            background-color: {Theme.panel_alt.name()};
            border: 1px solid {Theme.accent_dark.name()};
            color: {Theme.text.name()};
            padding: 4px 10px;
            border-radius: {radius_btn}px;
        }}
        QPushButton:hover {{
            background-color: {Theme.accent_dark.name()};
        }}
        QPushButton:focus {{
            border: 1px solid {Theme.accent.name()};
        }}
        QPushButton:pressed {{
            background-color: {Theme.accent.name()};
            color: {Theme.background.name()};
        }}
        QSplitter::handle {{
            background-color: {Theme.panel_alt.name()};
        }}
        QScrollBar:vertical {{
            background: {Theme.panel.name()};
            width: 10px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical {{
            background: {Theme.accent_dark.name()};
            border-radius: 4px;
            min-height: 20px;
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """
