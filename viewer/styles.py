from PySide6 import QtGui


class Theme:
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

    @staticmethod
    def font(size=10, bold=False):
        font = QtGui.QFont("Inter", pointSize=size)
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
        return f"""
        QMainWindow {{
            background-color: {Theme.background.name()};
        }}
        QGroupBox {{
            border: 1px solid {Theme.accent_dark.name()};
            border-radius: 6px;
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
            border-radius: 4px;
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
            border: 1px solid {Theme.accent_dark.name()};
            border-radius: 4px;
        }}
        QHeaderView::section {{
            background-color: {Theme.panel_alt.name()};
            color: {Theme.accent.name()};
            border: 1px solid {Theme.accent_dark.name()};
            padding: 4px 6px;
        }}
        QPlainTextEdit {{
            background-color: {Theme.panel.name()};
            border: 1px solid {Theme.accent_dark.name()};
            border-radius: 4px;
            color: {Theme.text.name()};
        }}
        QPushButton {{
            background-color: {Theme.panel_alt.name()};
            border: 1px solid {Theme.accent_dark.name()};
            color: {Theme.text.name()};
            padding: 4px 10px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {Theme.accent_dark.name()};
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
