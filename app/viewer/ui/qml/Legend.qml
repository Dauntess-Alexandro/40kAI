import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ColumnLayout {
    id: legendRoot
    spacing: spacingXs
    Layout.fillWidth: true

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined

    RowLayout {
        Layout.fillWidth: true
        spacing: spacingXs

        ToolButton {
            checkable: true
            checked: hasCtrl && viewerController.sideHighlightPlayer
            text: "● " + (hasCtrl ? viewerController.playerRoleLabel : legendPlayer)
            font.pixelSize: fontSm
            onToggled: if (hasCtrl) viewerController.setSideHighlight("player", checked)
        }
        ToolButton {
            checkable: true
            checked: hasCtrl && viewerController.sideHighlightModel
            text: "● " + (hasCtrl ? viewerController.modelRoleLabel : legendModel)
            font.pixelSize: fontSm
            onToggled: if (hasCtrl) viewerController.setSideHighlight("model", checked)
        }
        ToolButton {
            checkable: true
            checked: hasCtrl && viewerController.objectiveHighlight
            text: "● " + qsTr("Цель")
            font.pixelSize: fontSm
            onToggled: if (hasCtrl) viewerController.setObjectiveHighlight(checked)
        }
        Item { Layout.fillWidth: true }
    }

    Flow {
        Layout.fillWidth: true
        spacing: 6
        visible: hasCtrl && viewerController.mapOverlayLegend.length > 0

        Repeater {
            model: hasCtrl ? viewerController.mapOverlayLegend : []
            delegate: RowLayout {
                required property var modelData
                spacing: 4

                Rectangle {
                    width: 10
                    height: 10
                    radius: 5
                    color: modelData.color || borderMutedColor
                }
                Label {
                    text: modelData.label || ""
                    color: textSecondaryColor
                    font.pixelSize: fontSm
                }
            }
        }
    }
}
