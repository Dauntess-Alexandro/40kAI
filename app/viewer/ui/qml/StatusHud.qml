import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "tokens.js" as Tokens

Rectangle {
    id: hudRoot
    implicitHeight: detailsBlock.visible ? (mainCol.implicitHeight + detailsBlock.implicitHeight + spacingSm) : mainCol.implicitHeight
    color: "transparent"

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined
    readonly property string phaseRaw: hasCtrl ? viewerController.phaseRaw : ""
    readonly property string activeSide: hasCtrl ? viewerController.activeSideRaw : ""
    property bool showDetails: false

    ColumnLayout {
        id: mainCol
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        spacing: spacingXs

        RowLayout {
            Layout.fillWidth: true
            spacing: spacingXs

            Label {
                text: hasCtrl ? viewerController.roundText.replace("Раунд: ", "R") : "R—"
                color: textPrimaryColor
                font.pixelSize: bodyFontSize
                font.bold: true
            }
            Label {
                text: hasCtrl ? viewerController.turnText.replace("Ход: ", "T") : "T—"
                color: textPrimaryColor
                font.pixelSize: bodyFontSize
                font.bold: true
            }

            Rectangle {
                Layout.preferredHeight: 22
                Layout.preferredWidth: phasePill.implicitWidth + 16
                radius: 11
                color: Tokens.phaseColor(phaseRaw, phaseColors)
                Label {
                    id: phasePill
                    anchors.centerIn: parent
                    text: Tokens.phaseIcon(phaseRaw) + " " + (hasCtrl ? viewerController.phaseText.split(":")[0].replace("Фаза", "").trim() : "—")
                    color: "#ffffff"
                    font.pixelSize: fontMd
                    font.bold: true
                }
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                id: activeSideCapsule
                Layout.preferredHeight: 24
                Layout.preferredWidth: activeCapsule.implicitWidth + 20
                radius: 12
                color: Tokens.sideColor(activeSide, playerColor, modelColor)
                property real pulseOpacity: 1.0
                opacity: (hasCtrl && viewerController.engineBusy) ? pulseOpacity : 1.0
                Label {
                    id: activeCapsule
                    anchors.centerIn: parent
                    text: hasCtrl ? ("▶ " + viewerController.activeLabelText.replace("Активен: ", "")) : "—"
                    color: "#ffffff"
                    font.pixelSize: fontMd
                    font.bold: true
                }
                SequentialAnimation {
                    id: activePulse
                    running: hasCtrl && viewerController.engineBusy
                    loops: Animation.Infinite
                    onRunningChanged: if (!running) activeSideCapsule.pulseOpacity = 1.0
                    NumberAnimation {
                        target: activeSideCapsule
                        property: "pulseOpacity"
                        from: 0.55
                        to: 1.0
                        duration: 800
                    }
                    NumberAnimation {
                        target: activeSideCapsule
                        property: "pulseOpacity"
                        from: 1.0
                        to: 0.55
                        duration: 800
                    }
                }
            }

            Label {
                readonly property string selSource: hasCtrl ? viewerController.selectionSource : ""
                visible: selSource.length > 0
                text: "· " + selSource
                color: textSecondaryColor
                font.pixelSize: fontSm
            }

            BusyIndicator {
                visible: hasCtrl && viewerController.engineBusy
                Layout.preferredWidth: 18
                Layout.preferredHeight: 18
            }

            ToolButton {
                text: showDetails ? "▾" : "▸"
                font.pixelSize: fontSm
                onClicked: showDetails = !showDetails
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: spacingSm

            Rectangle {
                Layout.preferredHeight: 20
                Layout.fillWidth: true
                radius: radiusSm
                color: playerColor
                opacity: 0.25
                Label {
                    anchors.fill: parent
                    anchors.margins: 4
                    text: hasCtrl ? viewerController.vpPlayerText : "VP —"
                    color: textPrimaryColor
                    font.pixelSize: fontSm
                    elide: Text.ElideRight
                }
            }
            Rectangle {
                Layout.preferredHeight: 20
                Layout.fillWidth: true
                radius: radiusSm
                color: modelColor
                opacity: 0.25
                Label {
                    anchors.fill: parent
                    anchors.margins: 4
                    text: hasCtrl ? viewerController.vpModelText : "VP —"
                    color: textPrimaryColor
                    font.pixelSize: fontSm
                    elide: Text.ElideRight
                }
            }
        }

        Label {
            Layout.fillWidth: true
            text: hasCtrl ? (viewerController.cpPlayerText + "  •  " + viewerController.cpModelText) : ""
            color: textSecondaryColor
            font.pixelSize: fontSm
            elide: Text.ElideRight
        }

        ColumnLayout {
            id: detailsBlock
            Layout.fillWidth: true
            visible: showDetails
            spacing: 2

            Label {
                Layout.fillWidth: true
                visible: hasCtrl && viewerController.deploymentText.length > 0
                text: hasCtrl ? viewerController.deploymentText : ""
                color: textSecondaryColor
                font.pixelSize: fontSm
                wrapMode: Text.Wrap
            }
            Label {
                Layout.fillWidth: true
                visible: hasCtrl && viewerController.pendingRequest.length > 0
                text: hasCtrl ? viewerController.pendingRequest : ""
                color: textSecondaryColor
                font.pixelSize: fontSm
                wrapMode: Text.Wrap
            }
        }
    }
}
