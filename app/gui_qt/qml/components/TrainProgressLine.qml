import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

RowLayout {
    id: root
    property string lineLabel: ""
    property real lineValue: 0.0
    property string lineRight: ""
    property int barHeight: 11
    property color barColor: "#b88a26"
    property color trackColor: "#1a2230"
    property color borderColor: "#243650"
    property bool waitingMode: false
    property real uiScale: 1.0
    property color uiTextMuted: "#7d8ba0"
    property color uiTextMain: "#e7edf5"
    property string fontUiFamily: "Segoe UI"
    property string fontDataFamily: "Consolas"

    spacing: Math.round(8 * root.uiScale)

    Text {
        Layout.preferredWidth: Math.round(52 * root.uiScale)
        text: root.lineLabel
        color: root.uiTextMuted
        font.pixelSize: Math.round(10 * root.uiScale)
        font.bold: true
        font.letterSpacing: 0.8
        font.family: root.fontUiFamily
    }

    Item {
        Layout.fillWidth: true
        Layout.preferredHeight: root.barHeight

        Rectangle {
            anchors.fill: parent
            color: root.trackColor
            border.width: 1
            border.color: root.borderColor
        }

        Rectangle {
            width: root.waitingMode
                ? parent.width * 0.18
                : parent.width * Math.max(0, Math.min(1, root.lineValue))
            height: parent.height
            color: root.barColor
            opacity: root.waitingMode ? 0.35 : 1.0
            Behavior on width {
                NumberAnimation { duration: 450; easing.type: Easing.OutCubic }
            }
        }
    }

    Text {
        Layout.preferredWidth: Math.round(118 * root.uiScale)
        horizontalAlignment: Text.AlignRight
        text: root.lineRight
        color: root.uiTextMain
        font.pixelSize: Math.round(11 * root.uiScale)
        font.family: root.fontDataFamily
    }
}
