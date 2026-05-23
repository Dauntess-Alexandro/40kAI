import QtQuick
import QtQuick.Controls

TabButton {
    id: btn

    property color accentColor: "#7c3aed"
    property var rootUi: null

    property real uiScale: rootUi ? rootUi.uiScale : 1.0
    property color textMain: rootUi ? rootUi.uiTextMain : "#d7dde7"
    property color textMuted: rootUi ? rootUi.uiTextMuted : "#98a4b8"

    height: Math.round(34 * uiScale)

    background: Rectangle {
        color: btn.checked
            ? Qt.rgba(btn.accentColor.r, btn.accentColor.g, btn.accentColor.b, 0.22)
            : (btn.hovered ? Qt.rgba(1, 1, 1, 0.05) : "transparent")

        Rectangle {
            visible: btn.checked
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: Math.round(3 * btn.uiScale)
            color: btn.accentColor
        }
    }

    contentItem: Text {
        text: btn.text
        color: btn.checked ? btn.textMain : btn.textMuted
        font.bold: btn.checked
        font.pixelSize: Math.round(12 * btn.uiScale)
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
