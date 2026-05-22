import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "tokens.js" as Tokens

Rectangle {
    id: root
    color: bgSurfaceColor
    clip: true

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined
    readonly property bool hasDialogs: viewerDialogs !== null && viewerDialogs !== undefined
    readonly property bool commandPanelVisible: hasCtrl
        && (viewerController.commandKind !== "idle"
            || (viewerController.pendingRequest && viewerController.pendingRequest.length > 0))

    Rectangle {
        width: 4
        height: parent.height
        anchors.left: parent.left
        color: Tokens.sideColor(hasCtrl ? viewerController.activeSideRaw : "", playerColor, modelColor)
        z: 10
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.leftMargin: 6
        anchors.margins: spacingSm
        spacing: spacingSm

        StatusHud { Layout.fillWidth: true }

        Legend { Layout.fillWidth: true }

        TabBar {
            id: tabBar
            Layout.fillWidth: true
            currentIndex: hasCtrl ? viewerController.rightPanelTab : 0
            onCurrentIndexChanged: {
                if (hasCtrl)
                    viewerController.setRightPanelTab(currentIndex)
            }
            TabButton { text: qsTr("Отряды") }
            TabButton { text: qsTr("Журнал") }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: tabBar.currentIndex

            UnitsList { }

            LogPanel { }
        }

        CommandPanel {
            id: commandPanel
            Layout.fillWidth: true
            visible: commandPanelVisible
            opacity: commandPanelVisible ? 1.0 : 0.0
            Layout.preferredHeight: visible ? implicitHeight : 0
            Layout.maximumHeight: visible ? 280 : 0

            Behavior on opacity {
                NumberAnimation { duration: 120 }
            }
        }
    }

    Toast { parent: root }
    ConfirmDialog { parent: root }

    Component.onCompleted: {
        if (hasCtrl)
            tabBar.currentIndex = viewerController.rightPanelTab
    }
}
