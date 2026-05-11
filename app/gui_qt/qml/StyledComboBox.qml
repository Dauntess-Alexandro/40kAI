import QtQuick 2.15
import QtQuick.Controls 2.15

ComboBox {
    id: control
    font.family: "IBM Plex Mono"
    leftPadding: 10
    rightPadding: 28
    topPadding: 4
    bottomPadding: 4
    implicitHeight: Math.max(32, Math.round(font.pixelSize * 2.1))

    contentItem: Text {
        leftPadding: control.leftPadding
        rightPadding: control.rightPadding
        topPadding: control.topPadding
        bottomPadding: control.bottomPadding
        text: control.displayText
        font: control.font
        color: control.enabled ? "#d7dde7" : "#8a93a6"
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    indicator: Text {
        text: "▾"
        color: control.enabled ? "#aeb8c8" : "#6f7888"
        font.family: control.font.family
        font.pixelSize: Math.max(10, Math.round(control.font.pixelSize * 0.9))
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        anchors.rightMargin: 10
    }

    background: Rectangle {
        radius: 0
        color: control.enabled ? "#141b26" : "#10151d"
        border.width: 1
        border.color: control.visualFocus
            ? "#b88a26"
            : control.hovered
                ? "#5c6b82"
                : "#2f3848"
    }
}
