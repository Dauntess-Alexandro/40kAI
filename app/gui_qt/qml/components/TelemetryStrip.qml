import QtQuick 2.15
import QtQuick.Layouts 1.15

RowLayout {
    id: strip
    spacing: 8
    Layout.fillWidth: true

    property color cardBg: "#0d1521"
    property color cardBorder: "#243650"
    property color pc2Border: "#3a6ea5"
    property color trackBg: "#16202f"
    property color textMain: "#e7edf5"
    property color textMuted: "#7d8ba0"

    Repeater {
        model: telemetry.cardsModel
        delegate: Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 64
            radius: 6
            color: strip.cardBg
            border.width: 1
            border.color: model.variant === "remote" ? strip.pc2Border : strip.cardBorder

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 3

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 6
                    Rectangle {
                        width: 10; height: 10; radius: 5
                        color: model.barColor
                        Layout.alignment: Qt.AlignVCenter
                    }
                    Text {
                        Layout.fillWidth: true
                        text: model.label
                        color: strip.textMuted
                        font.pixelSize: 11
                        elide: Text.ElideRight
                    }
                    Text {
                        text: model.valueText
                        color: strip.textMain
                        font.pixelSize: 16
                        font.bold: true
                    }
                }

                Text {
                    text: model.sub
                    color: strip.textMuted
                    font.pixelSize: 10
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                }

                Rectangle {
                    id: track
                    Layout.fillWidth: true
                    height: 5
                    radius: 2.5
                    color: strip.trackBg
                    Rectangle {
                        height: parent.height
                        radius: 2.5
                        width: track.width * Math.max(0, Math.min(100, model.pct)) / 100.0
                        color: model.barColor
                        Behavior on width { NumberAnimation { duration: 400; easing.type: Easing.OutCubic } }
                    }
                }
            }
        }
    }
}
