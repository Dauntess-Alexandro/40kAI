import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: logRoot
    color: bgSurfaceColor
    clip: true

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined

    ListView {
        id: logList
        anchors.fill: parent
        anchors.margins: 4
        clip: true
        spacing: 2
        model: viewerLogModel
        cacheBuffer: 400

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
        }

        delegate: Rectangle {
            width: logList.width
            height: Math.max(txt.implicitHeight + 10, 20)
            color: rowMouse.containsMouse ? "#1b2740" : "transparent"
            radius: 4

            Label {
                id: txt
                anchors.fill: parent
                anchors.margins: 4
                text: model.logText
                color: model.logColor
                wrapMode: Text.Wrap
                font.family: "Consolas"
                font.pixelSize: 11
            }
            MouseArea {
                id: rowMouse
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.LeftButton
                onClicked: { if (logRoot.hasCtrl) viewerController.onLogRowClicked(index) }
                onEntered: { if (logRoot.hasCtrl) viewerController.onLogRowHovered(index) }
                onExited: { if (logRoot.hasCtrl) viewerController.onLogHoverExited() }
            }
        }

        Connections {
            target: logRoot.hasCtrl ? viewerController : null
            enabled: logRoot.hasCtrl
            function onLogRevisionChanged() {
                Qt.callLater(function () {
                    logList.positionViewAtEnd()
                })
            }
        }
    }
}
