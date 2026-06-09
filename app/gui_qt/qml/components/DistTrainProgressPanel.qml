import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ColumnLayout {
    id: root
    property var ctrl: null
    property real uiScale: 1.0
    property color uiBorder: "#243650"
    property color uiTextMain: "#e7edf5"
    property color uiTextMuted: "#7d8ba0"
    property string fontUiFamily: "Segoe UI"
    property string fontDataFamily: "Consolas"
    visible: ctrl && ctrl.distProgressVisible
    spacing: Math.round(6 * uiScale)
    Layout.fillWidth: true

    Rectangle {
        Layout.fillWidth: true
        color: "#0d1521"
        border.width: 1
        border.color: uiBorder
        implicitHeight: distInner.implicitHeight + Math.round(20 * uiScale)

        ColumnLayout {
            id: distInner
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: Math.round(10 * uiScale)
            spacing: Math.round(8 * uiScale)

            Text {
                text: "РАСПРЕДЕЛЁННЫЙ СБОР"
                color: uiTextMuted
                font.pixelSize: Math.round(10 * uiScale)
                font.bold: true
                font.letterSpacing: 0.7
                font.family: fontUiFamily
            }

            TrainProgressLine {
                Layout.fillWidth: true
                uiScale: root.uiScale
                uiTextMuted: root.uiTextMuted
                uiTextMain: root.uiTextMain
                fontUiFamily: root.fontUiFamily
                fontDataFamily: root.fontDataFamily
                lineLabel: "ПК1"
                lineValue: ctrl ? ctrl.pc1ProgressValue : 0
                lineRight: ctrl ? ctrl.pc1ProgressLabel : "0/0"
                barHeight: Math.round(11 * uiScale)
                barColor: "#b88a26"
                trackColor: "#1a2230"
                borderColor: uiBorder
                waitingMode: ctrl && ctrl.progressPhase === "waiting_pc2"
            }

            TrainProgressLine {
                Layout.fillWidth: true
                uiScale: root.uiScale
                uiTextMuted: root.uiTextMuted
                uiTextMain: root.uiTextMain
                fontUiFamily: root.fontUiFamily
                fontDataFamily: root.fontDataFamily
                lineLabel: "ПК2"
                lineValue: ctrl ? ctrl.pc2ProgressValue : 0
                lineRight: ctrl ? ctrl.pc2ProgressLabel : "0/0"
                barHeight: Math.round(11 * uiScale)
                barColor: "#3a6ea5"
                trackColor: "#1a2230"
                borderColor: uiBorder
                waitingMode: ctrl && ctrl.progressPhase === "waiting_pc2"
            }
        }
    }

    Rectangle {
        Layout.fillWidth: true
        implicitHeight: pc2StatusRow.implicitHeight + Math.round(16 * uiScale)
        color: "#0d1521"
        border.width: 1
        border.color: {
            if (!ctrl) return uiBorder
            if (ctrl.pc2StatusTone === "waiting") return "#b88a26"
            if (ctrl.pc2StatusTone === "done") return "#3a6ea5"
            return uiBorder
        }

        RowLayout {
            id: pc2StatusRow
            anchors.fill: parent
            anchors.margins: Math.round(8 * uiScale)
            spacing: Math.round(8 * uiScale)

            Text {
                Layout.fillWidth: true
                text: ctrl ? ctrl.pc2StatusLine : ""
                color: uiTextMain
                font.pixelSize: Math.round(12 * uiScale)
                font.bold: true
                font.family: fontDataFamily
                elide: Text.ElideRight
            }

            Text {
                text: ctrl ? ctrl.pc2StatusHint : ""
                color: uiTextMuted
                font.pixelSize: Math.round(11 * uiScale)
                font.family: fontDataFamily
                horizontalAlignment: Text.AlignRight
                elide: Text.ElideLeft
                Layout.maximumWidth: parent.width * 0.55
            }
        }
    }
}
