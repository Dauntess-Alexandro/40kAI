import QtQuick 2.15
import QtQuick.Controls 2.15

Popup {
    id: confirmRoot
    modal: true
    focus: true
    visible: hasDialogs && viewerDialogs.confirmOpen
    anchors.centerIn: parent
    width: Math.min(440, parent ? parent.width - 32 : 440)
    padding: spacingMd
    background: Rectangle {
        color: bgElevatedColor
        radius: radiusMd
        border.color: borderMutedColor
    }
    contentItem: Column {
        spacing: spacingSm
        width: confirmRoot.availableWidth
        Label {
            width: parent.width
            text: hasDialogs ? viewerDialogs.confirmTitle : ""
            font.bold: true
            color: textPrimaryColor
            font.family: headerFontFamily
            font.pixelSize: headerFontSize
        }
        Label {
            width: parent.width
            text: hasDialogs ? viewerDialogs.confirmBody : ""
            wrapMode: Text.Wrap
            color: textSecondaryColor
            font.pixelSize: bodyFontSize
        }
        Row {
            spacing: spacingSm
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
    readonly property bool hasDialogs: viewerDialogs !== null && viewerDialogs !== undefined
}
