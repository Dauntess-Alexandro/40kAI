import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    property string nodeLabel: "ПК1"
    property real progressValue: 0.0
    property string progressLabel: "0/0"
    property string subLine: "—"
    property string statusHint: ""
    property color accentColor: "#b88a26"
    property color cardBg: "#0d1521"
    property color cardBorder: "#243650"
    property color trackBg: "#16202f"
    property color textMain: "#e7edf5"
    property color textMuted: "#7d8ba0"
    property bool waitingMode: false
    property bool doneMode: false
    property bool draining: false
    property bool isRemote: false
    property real uiScale: 1.0
    property string fontUiFamily: "Segoe UI"
    property string fontDataFamily: "Consolas"

    Layout.fillWidth: true
    Layout.preferredHeight: Math.round(72 * uiScale)
    radius: Math.round(6 * uiScale)
    color: cardBg
    border.width: 1
    border.color: doneMode
        ? accentColor
        : (waitingMode && isRemote ? Qt.rgba(accentColor.r, accentColor.g, accentColor.b, 0.75) : cardBorder)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Math.round(8 * uiScale)
        spacing: Math.round(3 * uiScale)

        RowLayout {
            Layout.fillWidth: true
            spacing: Math.round(6 * uiScale)

            Rectangle {
                width: Math.round(10 * uiScale)
                height: Math.round(10 * uiScale)
                radius: Math.round(5 * uiScale)
                color: accentColor
                opacity: draining ? 0.5 : 1.0
                Layout.alignment: Qt.AlignVCenter

                SequentialAnimation on opacity {
                    running: waitingMode && isRemote && root.visible
                    loops: Animation.Infinite
                    NumberAnimation { from: 0.35; to: 1.0; duration: 700 }
                    NumberAnimation { from: 1.0; to: 0.35; duration: 700 }
                }
            }

            Text {
                Layout.fillWidth: true
                text: nodeLabel
                color: textMuted
                font.pixelSize: Math.round(11 * uiScale)
                font.bold: true
                font.letterSpacing: 0.6
                font.family: fontUiFamily
                elide: Text.ElideRight
            }

            Text {
                text: doneMode ? "✓" : (Math.round(progressValue * 100) + "%")
                color: doneMode ? accentColor : textMain
                font.pixelSize: Math.round((doneMode ? 14 : 16) * uiScale)
                font.bold: true
                font.family: fontDataFamily
            }
        }

        Text {
            Layout.fillWidth: true
            text: progressLabel
            color: textMain
            font.pixelSize: Math.round(12 * uiScale)
            font.family: fontDataFamily
            elide: Text.ElideRight
        }

        Text {
            Layout.fillWidth: true
            text: statusHint !== "" ? statusHint : subLine
            color: statusHint !== "" ? Qt.lighter(accentColor, 1.25) : textMuted
            font.pixelSize: Math.round(10 * uiScale)
            font.family: fontUiFamily
            elide: Text.ElideRight
        }

        Rectangle {
            id: track
            Layout.fillWidth: true
            height: Math.round(5 * uiScale)
            radius: Math.round(2.5 * uiScale)
            color: trackBg

            Rectangle {
                height: parent.height
                radius: track.radius
                width: track.width * Math.max(0, Math.min(1, progressValue))
                color: accentColor
                opacity: waitingMode && isRemote ? 0.35 : (draining ? 0.55 : 1.0)
                Behavior on width {
                    NumberAnimation { duration: 400; easing.type: Easing.OutCubic }
                }
            }
        }
    }
}
