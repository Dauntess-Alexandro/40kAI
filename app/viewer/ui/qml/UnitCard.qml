import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "tokens.js" as Tokens

Rectangle {
    id: cardRoot
    height: 58
    radius: radiusSm
    color: unitIsSelected ? bgElevatedColor : (rowMouse.containsMouse ? "#1b2740" : "transparent")
    border.width: unitIsActive ? 2 : (unitIsSelected ? 1 : 0)
    border.color: unitIsActive ? selectionColor : borderMutedColor

    property int unitId: -1
    property string unitSide: ""
    property string unitName: "—"
    property string unitHp: "—"
    property string unitModels: "—"
    property string unitIconPath: ""
    property string unitFactionLabel: ""
    property bool unitIsActive: false
    property bool unitIsSelected: false
    property bool unitIsDamaged: false
    property string unitSection: ""

    Rectangle {
        visible: unitIsDamaged
        width: 8
        height: 8
        radius: 4
        color: "#e06c75"
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.margins: 4
        z: 2
    }

    Rectangle {
        width: 4
        height: parent.height - 8
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        anchors.leftMargin: 4
        radius: 2
        color: Tokens.sideColor(unitSide, playerColor, modelColor)
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: spacingXs
        anchors.leftMargin: spacingSm
        spacing: spacingSm

        Rectangle {
            Layout.preferredWidth: 36
            Layout.preferredHeight: 36
            radius: radiusSm
            color: bgElevatedColor
            Image {
                anchors.fill: parent
                anchors.margins: 2
                source: unitIconPath.length > 0 ? ("file:///" + unitIconPath) : ""
                fillMode: Image.PreserveAspectFit
                visible: unitIconPath.length > 0
            }
            Label {
                anchors.centerIn: parent
                visible: unitIconPath.length === 0
                text: "✦"
                color: textSecondaryColor
                font.pixelSize: fontLg
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2
            Label {
                text: unitName
                color: textPrimaryColor
                font.pixelSize: bodyFontSize
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
            RowLayout {
                Layout.fillWidth: true
                Label {
                    text: unitFactionLabel + " #" + unitId
                    color: textSecondaryColor
                    font.pixelSize: fontSm
                }
                Item { Layout.fillWidth: true }
                Label {
                    text: unitHp
                    color: unitIsDamaged ? "#e06c75" : textPrimaryColor
                    font.family: monoFontFamily
                    font.pixelSize: fontLg
                    font.bold: true
                }
                Label {
                    text: "M:" + unitModels
                    color: unitIsDamaged ? "#e06c75" : textSecondaryColor
                    font.family: monoFontFamily
                    font.pixelSize: fontLg
                    font.bold: true
                }
            }
        }
    }

    MouseArea {
        id: rowMouse
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton
        onClicked: {
            if (viewerController)
                viewerController.selectUnit(unitId)
        }
        onDoubleClicked: {
            if (viewerController)
                viewerController.centerCameraOnUnit(unitId)
        }
        onEntered: {
            if (viewerController)
                viewerController.previewUnit(unitId)
        }
    }
}
