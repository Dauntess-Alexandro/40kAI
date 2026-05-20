import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    color: bgSurfaceColor
    clip: true

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
            text: viewerController.roundText
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.turnText
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.phaseText
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.activeLabelText
            wrapMode: Text.Wrap
            color: accentColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.deploymentText
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
            text: viewerController.vpPlayerText
            color: playerColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.vpModelText
            color: modelColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.cpPlayerText
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.cpModelText
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
            text: viewerController.unitsSummaryText
            visible: viewerController.unitsSummaryText.length > 0
            wrapMode: Text.Wrap
            color: textSecondaryColor
            Layout.fillWidth: true
            font.pixelSize: 10
        }

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: qsTr("FX:")
                color: textSecondaryColor
                font.pixelSize: 11
            }
            ComboBox {
                id: fxBox
                Layout.fillWidth: true
                model: ["low", "medium", "high"]
                onActivated: (i) => viewerController.setFxQuality(model[i])
                Component.onCompleted: {
                    var q = viewerController.fxQuality
                    var j = model.indexOf(q)
                    if (j >= 0)
                        currentIndex = j
                }
                Connections {
                    target: viewerController
                    function onFxQualityChanged() {
                        var j = fxBox.model.indexOf(viewerController.fxQuality)
                        if (j >= 0)
                            fxBox.currentIndex = j
                    }
                }
            }
        }

        Label {
            text: qsTr("КОМАНДЫ")
            font.pixelSize: 11
            font.bold: true
            color: textSecondaryColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.commandPromptText
            wrapMode: Text.Wrap
            color: textPrimaryColor
            Layout.fillWidth: true
        }
        Label {
            text: viewerController.commandHintText
            visible: viewerController.commandHintText.length > 0
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
                    text: modelData
                    onClicked: viewerController.submitChoiceAtIndex(index)
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
        visible: viewerDialogs.toastVisible
        width: Math.min(520, root.width - 24)
        x: Math.max(8, (root.width - width) / 2)
        y: Math.max(8, root.height - height - 14)
        background: Rectangle {
            radius: 8
            color: "#1E293B"
            border.color: "#334155"
        }
        contentItem: Label {
            text: viewerDialogs.toastText
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
        visible: viewerDialogs.confirmOpen
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
                text: viewerDialogs.confirmTitle
                font.bold: true
                color: textPrimaryColor
            }
            Label {
                width: parent.width
                text: viewerDialogs.confirmBody
                wrapMode: Text.Wrap
                color: textSecondaryColor
            }
            Row {
                spacing: 8
                anchors.horizontalCenter: parent.horizontalCenter
                Button {
                    text: qsTr("OK")
                    onClicked: viewerDialogs.acceptConfirm()
                }
                Button {
                    text: qsTr("Отмена")
                    onClicked: viewerDialogs.rejectConfirm()
                }
            }
        }
    }
}
