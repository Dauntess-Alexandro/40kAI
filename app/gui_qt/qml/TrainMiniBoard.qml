import QtQuick 2.15

// Упрощённая схема стола 60×40: зоны деплоя слева/справа, центр, маркер цели.
Item {
    id: root
    property real scaleRef: 1.0

    implicitWidth: Math.round(112 * scaleRef)
    implicitHeight: Math.round(76 * scaleRef)

    Rectangle {
        anchors.fill: parent
        color: "#0e1218"
        border.width: 1
        border.color: "#2f3848"

        Rectangle {
            width: Math.round(parent.width * 0.2)
            height: parent.height
            color: "#1a3352"
            opacity: 0.65
        }
        Rectangle {
            anchors.right: parent.right
            width: Math.round(parent.width * 0.2)
            height: parent.height
            color: "#4a2525"
            opacity: 0.55
        }
        Rectangle {
            width: 1
            height: parent.height
            anchors.horizontalCenter: parent.horizontalCenter
            color: "#4f5a6b"
            opacity: 0.55
        }
        Rectangle {
            anchors.centerIn: parent
            width: Math.max(4, Math.round(6 * scaleRef))
            height: width
            radius: 0
            color: "#c79a32"
        }
        Text {
            anchors.left: parent.left
            anchors.leftMargin: Math.round(3 * scaleRef)
            anchors.top: parent.top
            anchors.topMargin: Math.round(2 * scaleRef)
            text: "P1"
            font.pixelSize: Math.round(8 * scaleRef)
            font.bold: true
            font.family: "Rajdhani"
            color: "#6b8ab8"
        }
        Text {
            anchors.right: parent.right
            anchors.rightMargin: Math.round(3 * scaleRef)
            anchors.top: parent.top
            anchors.topMargin: Math.round(2 * scaleRef)
            text: "P2"
            font.pixelSize: Math.round(8 * scaleRef)
            font.bold: true
            font.family: "Rajdhani"
            color: "#b87a7a"
        }
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: Math.round(2 * scaleRef)
            text: "60×40"
            font.pixelSize: Math.round(7 * scaleRef)
            font.family: "IBM Plex Mono"
            color: "#5c6578"
        }
    }
}
