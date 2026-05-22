import QtQuick 2.15
import QtQuick.Controls 2.15

Popup {
    id: toastRoot
    modal: false
    focus: false
    padding: 12
    closePolicy: Popup.NoAutoClose
    visible: hasDialogs && viewerDialogs.toastVisible
    width: Math.min(520, parent ? parent.width - 24 : 520)
    x: parent ? Math.max(8, (parent.width - width) / 2) : 8
    y: parent ? Math.max(8, parent.height - height - 14) : 8
    background: Rectangle {
        radius: radiusMd
        color: bgElevatedColor
        border.color: borderMutedColor
    }
    contentItem: Label {
        text: hasDialogs ? viewerDialogs.toastText : ""
        color: textPrimaryColor
        wrapMode: Text.Wrap
        width: toastRoot.availableWidth
        font.family: headerFontFamily
        font.pixelSize: headerFontSize
    }
    readonly property bool hasDialogs: viewerDialogs !== null && viewerDialogs !== undefined
}
