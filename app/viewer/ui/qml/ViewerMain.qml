import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    color: bgSurfaceColor
    clip: true

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined
    readonly property bool hasDialogs: viewerDialogs !== null && viewerDialogs !== undefined

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        Label {
            text: qsTr("СТАТУС")
            font.pixelSize: 11
            font.bold: true
            color: textSecondaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.roundText : qsTr("Раунд: —")
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.turnText : qsTr("Ход: —")
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.phaseText : qsTr("Фаза: —")
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.activeLabelText : qsTr("Активен: —")
            wrapMode: Text.Wrap
            color: accentColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.deploymentText : ""
            wrapMode: Text.Wrap
            color: textSecondaryColor
            Layout.fillWidth: true
        }

        Label {
            text: qsTr("ОЧКИ")
            font.pixelSize: 11
            font.bold: true
            color: textSecondaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.vpPlayerText : qsTr("Player VP: —")
            color: playerColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.vpModelText : qsTr("Model VP: —")
            color: modelColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.cpPlayerText : qsTr("Player CP: —")
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.cpModelText : qsTr("Model CP: —")
            color: textPrimaryColor
            Layout.fillWidth: true
        }

        Label {
            text: qsTr("ЛЕГЕНДА")
            font.pixelSize: 11
            font.bold: true
            color: textSecondaryColor
            Layout.fillWidth: true
        }
        RowLayout {
            Layout.fillWidth: true
            Rectangle { width: 12; height: 12; radius: 6; color: playerColor }
            Label { text: legendPlayer; color: textPrimaryColor; Layout.fillWidth: true }
        }
        RowLayout {
            Layout.fillWidth: true
            Rectangle { width: 12; height: 12; radius: 6; color: modelColor }
            Label { text: legendModel; color: textPrimaryColor; Layout.fillWidth: true }
        }
        RowLayout {
            Layout.fillWidth: true
            Rectangle { width: 12; height: 12; radius: 6; color: objectiveColor }
            Label { text: qsTr("Цель"); color: textPrimaryColor; Layout.fillWidth: true }
        }

        Label {
            text: hasCtrl ? viewerController.unitsSummaryText : ""
            visible: hasCtrl && viewerController.unitsSummaryText.length > 0
            wrapMode: Text.Wrap
            color: textSecondaryColor
            Layout.fillWidth: true
            font.pixelSize: 10
        }

        Label {
            text: qsTr("КОМАНДЫ")
            font.pixelSize: 11
            font.bold: true
            color: textSecondaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.commandPromptText : qsTr("Ожидаю команду...")
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: hasCtrl ? viewerController.commandHintText : ""
            visible: hasCtrl && viewerController.commandHintText.length > 0
            wrapMode: Text.Wrap
            color: textSecondaryColor
            Layout.fillWidth: true
            font.pixelSize: 10
        }
        Flow {
            id: cmdFlow
            Layout.fillWidth: true
            spacing: 6
            Repeater {
                model: commandLabelModel
                delegate: Button {
                    required property int index
                    required property string modelData
                    enabled: hasCtrl
                    text: modelData
                    onClicked: {
                        if (hasCtrl)
                            viewerController.submitChoiceAtIndex(index)
                    }
                }
            }
        }
    }

    Popup {
        id: toastPopup
        parent: root
        modal: false
        focus: false
        padding: 12
        closePolicy: Popup.NoAutoClose
        visible: hasDialogs && viewerDialogs.toastVisible
        width: Math.min(520, root.width - 24)
        x: Math.max(8, (root.width - width) / 2)
        y: Math.max(8, root.height - height - 14)
        background: Rectangle {
            radius: 8
            color: "#1E293B"
            border.color: "#334155"
        }
        contentItem: Label {
            text: hasDialogs ? viewerDialogs.toastText : ""
            color: textPrimaryColor
            wrapMode: Text.Wrap
            width: toastPopup.availableWidth
        }
    }

    Popup {
        id: confirmPopup
        parent: root
        modal: true
        focus: true
        visible: hasDialogs && viewerDialogs.confirmOpen
        anchors.centerIn: parent
        width: Math.min(440, root.width - 32)
        padding: 16
        background: Rectangle {
            color: "#1E293B"
            radius: 10
            border.color: "#334155"
        }
        contentItem: Column {
            spacing: 10
            width: confirmPopup.availableWidth
            Label {
                width: parent.width
                text: hasDialogs ? viewerDialogs.confirmTitle : ""
                font.bold: true
                color: textPrimaryColor
            }
            Label {
                width: parent.width
                text: hasDialogs ? viewerDialogs.confirmBody : ""
                wrapMode: Text.Wrap
                color: textSecondaryColor
            }
            Row {
                spacing: 8
                anchors.horizontalCenter: parent.horizontalCenter
                Button {
                    text: qsTr("OK")
                    enabled: hasDialogs
                    onClicked: viewerDialogs.acceptConfirm()
                }
                Button {
                    text: qsTr("Отмена")
                    enabled: hasDialogs
                    onClicked: viewerDialogs.rejectConfirm()
                }
            }
        }
    }
}
