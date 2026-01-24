from PySide6 import QtGui


class Theme:
    background = QtGui.QColor("#181a1e")
    panel = QtGui.QColor("#23262b")
    card = QtGui.QColor("#262a30")
    grid = QtGui.QColor("#2f3439")
    text = QtGui.QColor("#e6e9ef")
    muted = QtGui.QColor("#a7abb3")
    accent = QtGui.QColor("#f7d154")

    player = QtGui.QColor("#4caf50")
    model = QtGui.QColor("#42a5f5")
    objective = QtGui.QColor("#fbc02d")
    selection = QtGui.QColor("#ffffff")
    unit_outline = QtGui.QColor("#0f1114")

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
