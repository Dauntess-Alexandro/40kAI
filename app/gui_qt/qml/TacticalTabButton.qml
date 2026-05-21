import QtQuick 2.15
import QtQuick.Controls 2.15

TabButton {
    id: control

    leftPadding: 18
    rightPadding: 18
    topPadding: 10
    bottomPadding: 10
    spacing: 6

    contentItem: Text {
        text: (control.text || "").toUpperCase()
        color: control.checked ? "#120f05" : (control.hovered ? "#e5e7eb" : "#9ca3af")
        font.family: "Rajdhani"
        font.bold: true
        font.pixelSize: 16
        font.letterSpacing: 1.0
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    // Rectangle вместо ChamferPanel (Canvas): при Qt 6 / RHI Canvas на первом кадре часто «догружает»
    // фон вкладок → пустые слоты в TabBar; прямоугольник сразу попадает в scene graph.
    background: Rectangle {
        color: control.checked ? "#c79a32" : (control.hovered ? "#222c39" : "#171d26")
        border.color: control.checked ? "#d3b061" : (control.hovered ? "#8a97ad" : "#4f5a6b")
        border.width: 1
        radius: 6
    }
}
