import QtQuick
import ".."

// Сворачиваемая секция: кликабельная строка-заголовок (шеврон + текст) и контент,
// который показывается только когда expanded === true.
// Контент кладётся как дочерние элементы; каждый должен задавать width: parent.width.
Item {
    id: sec

    property string title: ""
    property bool expanded: false
    property real uiScale: 1.0
    property int captionSize: 11
    property color textMain: "#d7dde7"
    property color textMuted: "#98a4b8"
    property color panelFill: "#161f31"
    property color panelBorder: "#2f3d58"

    default property alias contentData: bodyHolder.data

    implicitHeight: headerBar.height
                    + (expanded ? bodyHolder.childrenRect.height + Math.round(8 * uiScale) : 0)

    ChamferPanel {
        id: headerBar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: Math.round(36 * sec.uiScale)
        cutSize: Math.round(6 * sec.uiScale)
        contentMargin: 0
        fillColor: sec.panelFill
        borderWidth: 1
        borderColor: sec.panelBorder
    }

    Row {
        anchors.left: headerBar.left
        anchors.leftMargin: Math.round(12 * sec.uiScale)
        anchors.verticalCenter: headerBar.verticalCenter
        spacing: Math.round(8 * sec.uiScale)

        Text {
            text: sec.expanded ? "▾" : "▸"   // ▾ / ▸
            color: sec.textMuted
            font.pixelSize: sec.captionSize + 2
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            text: sec.title
            color: sec.textMain
            font.bold: true
            font.pixelSize: sec.captionSize + 1
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    MouseArea {
        anchors.fill: headerBar
        cursorShape: Qt.PointingHandCursor
        onClicked: sec.expanded = !sec.expanded
    }

    Item {
        id: bodyHolder
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: headerBar.bottom
        anchors.topMargin: Math.round(8 * sec.uiScale)
        height: sec.expanded ? childrenRect.height : 0
        visible: sec.expanded
        clip: true
    }
}
