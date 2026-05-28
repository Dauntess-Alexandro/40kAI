import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

RowLayout {
    id: row
    required property var rootUi
    required property string title
    required property string subtitle
    required property string tooltipText
    property bool active: false
    property bool switchChecked: false
    property bool switchEnabled: true
    property color accentOn: "#3ecf8e"
    property color accentOff: "#5a6270"

    signal toggled(bool checked)

    Layout.fillWidth: true
    spacing: rootUi.spacingMd

    Rectangle {
        Layout.preferredWidth: Math.round(4 * rootUi.uiScale)
        Layout.preferredHeight: Math.max(localSwitch.implicitHeight, titleLabel.implicitHeight + 8)
        radius: 2
        color: switchChecked && switchEnabled ? row.accentOn : row.accentOff
        opacity: switchEnabled ? 1.0 : 0.35
    }

    Switch {
        id: localSwitch
        checked: row.switchChecked
        enabled: row.switchEnabled
        scale: Math.max(1.0, rootUi.uiScale * 0.92)
        onToggled: row.toggled(checked)
        ToolTip.visible: hovered
        ToolTip.delay: 400
        ToolTip.timeout: 16000
        ToolTip.text: row.tooltipText
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 2

        Label {
            id: titleLabel
            text: row.title
            font.bold: true
            font.pixelSize: Math.round(13 * rootUi.uiScale)
            font.family: rootUi.fontUiFamily
            color: row.active ? rootUi.uiTextMain : rootUi.uiTextMuted
            Layout.fillWidth: true
            ToolTip.visible: titleMouse.containsMouse
            ToolTip.delay: 400
            ToolTip.timeout: 16000
            ToolTip.text: row.tooltipText

            MouseArea {
                id: titleMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: row.switchEnabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                onClicked: {
                    if (!row.switchEnabled)
                        return
                    localSwitch.checked = !localSwitch.checked
                }
            }
        }

        Label {
            visible: row.subtitle.length > 0
            text: row.subtitle
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
            color: rootUi.uiTextMuted
            font.pixelSize: Math.round(10 * rootUi.uiScale)
            opacity: row.active ? 0.95 : 0.75
        }
    }
}
