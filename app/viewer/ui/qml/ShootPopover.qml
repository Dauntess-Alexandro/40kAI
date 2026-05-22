import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Popup {
    id: shootPopup
    modal: false
    focus: true
    padding: spacingMd
    closePolicy: Popup.CloseOnEscape
    visible: hasCtrl && viewerController.shootPopoverOpen
    width: Math.min(380, parent ? parent.width - 16 : 380)

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined

    background: Rectangle {
        radius: radiusMd
        color: bgElevatedColor
        border.color: borderMutedColor
        border.width: 1
    }

    contentItem: ColumnLayout {
        spacing: spacingSm
        width: shootPopup.availableWidth

        Label {
            text: "FIRE"
            font.bold: true
            font.pixelSize: headerFontSize
            font.family: headerFontFamily
            color: textPrimaryColor
        }
        Label {
            Layout.fillWidth: true
            text: hasCtrl ? viewerController.shootTargetText : ""
            font.bold: true
            color: textPrimaryColor
            wrapMode: Text.Wrap
        }
        Label {
            Layout.fillWidth: true
            text: hasCtrl ? viewerController.shootMetaText : ""
            color: textSecondaryColor
            font.pixelSize: fontSm
            wrapMode: Text.Wrap
        }
        Label {
            Layout.fillWidth: true
            text: hasCtrl ? viewerController.shootStepperText : ""
            color: textSecondaryColor
            font.pixelSize: fontSm
        }
        Label {
            Layout.fillWidth: true
            text: hasCtrl ? viewerController.shootStepTitle : ""
            font.bold: true
            color: textPrimaryColor
        }

        TextField {
            id: diceField
            Layout.fillWidth: true
            visible: hasCtrl && viewerController.shootNeedsDiceInput
            placeholderText: qsTr("4 1 6 или 416…")
            text: hasCtrl ? viewerController.shootDiceInput : ""
            font.family: monoFontFamily
            font.pixelSize: monoFontSize
            onTextChanged: if (hasCtrl) viewerController.setShootDiceInput(text)
        }
        Label {
            visible: hasCtrl && viewerController.shootNeedsDiceInput
            text: hasCtrl ? viewerController.shootDiceCounter : ""
            color: textSecondaryColor
            font.family: monoFontFamily
            font.pixelSize: monoFontSize
        }
        Label {
            Layout.fillWidth: true
            text: hasCtrl ? viewerController.shootInfoText : ""
            color: textSecondaryColor
            font.pixelSize: fontSm
            wrapMode: Text.Wrap
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: spacingSm
            Button {
                Layout.fillWidth: true
                text: hasCtrl ? viewerController.shootActionLabel : qsTr("Roll")
                highlighted: true
                onClicked: if (hasCtrl) viewerController.submitShootStep("confirm")
            }
            Button {
                text: qsTr("Cancel")
                onClicked: if (hasCtrl) viewerController.submitShootStep("cancel")
            }
        }
    }
}
