from PySide6 import QtGui


class Theme:
    background = QtGui.QColor("#1f2124")
    panel = QtGui.QColor("#2a2d31")
    grid = QtGui.QColor(70, 70, 70)
    text = QtGui.QColor("#e6e6e6")
    muted = QtGui.QColor("#a7a7a7")

    player = QtGui.QColor("#4caf50")
    model = QtGui.QColor("#42a5f5")
    objective = QtGui.QColor("#fbc02d")
    selection = QtGui.QColor("#ffffff")

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
