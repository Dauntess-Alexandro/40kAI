import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: card

    property string algoTitle: ""
    property string tldr: ""
    property color accentColor: "#7c3aed"
    property var badges: []
    property var sections: []
    property var rootUi: null

    property real uiScale: rootUi ? rootUi.uiScale : 1.0
    property color textMain: rootUi ? rootUi.uiTextMain : "#d7dde7"
    property color textMuted: rootUi ? rootUi.uiTextMuted : "#98a4b8"
    property color bgFill: rootUi ? rootUi.bgElevated : "#1E293B"
    property color borderColor: rootUi ? rootUi.uiBorder : "#334155"

    radius: Math.round(12 * uiScale)
    color: bgFill
    border.color: borderColor
    border.width: 1
    implicitHeight: cardRow.implicitHeight + Math.round(4 * uiScale)

    RowLayout {
        id: cardRow
        width: parent.width
        spacing: 0

        Rectangle {
            width: Math.round(6 * card.uiScale)
            Layout.fillHeight: true
            color: card.accentColor
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.margins: Math.round(14 * card.uiScale)
            spacing: Math.round(8 * card.uiScale)

            Text {
                text: card.algoTitle
                font.bold: true
                font.pixelSize: Math.round(16 * card.uiScale)
                color: card.textMain
                Layout.fillWidth: true
            }

            Text {
                visible: card.tldr.length > 0
                text: card.tldr
                wrapMode: Text.WordWrap
                color: card.accentColor
                font.italic: true
                font.pixelSize: Math.round(12 * card.uiScale)
                Layout.fillWidth: true
            }

            Flow {
                Layout.fillWidth: true
                spacing: Math.round(6 * card.uiScale)
                visible: card.badges.length > 0

                Repeater {
                    model: card.badges
                    delegate: Rectangle {
                        required property var modelData
                        radius: Math.round(999 * card.uiScale)
                        color: modelData.bg
                        implicitHeight: badgeText.implicitHeight + Math.round(6 * card.uiScale)
                        implicitWidth: badgeText.implicitWidth + Math.round(14 * card.uiScale)

                        Text {
                            id: badgeText
                            anchors.centerIn: parent
                            text: parent.modelData.text
                            font.pixelSize: Math.round(11 * card.uiScale)
                            color: parent.modelData.fg
                        }
                    }
                }
            }

            GridLayout {
                Layout.fillWidth: true
                columns: card.width > Math.round(620 * card.uiScale) ? 2 : 1
                columnSpacing: Math.round(20 * card.uiScale)
                rowSpacing: Math.round(12 * card.uiScale)

                Repeater {
                    model: card.sections
                    delegate: ColumnLayout {
                        required property var modelData
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                        Layout.preferredWidth: 1
                        spacing: Math.round(3 * card.uiScale)

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: Math.round(6 * card.uiScale)

                            Text {
                                text: modelData.icon
                                color: card.accentColor
                                font.bold: true
                                font.pixelSize: Math.round(13 * card.uiScale)
                            }
                            Text {
                                text: modelData.title
                                color: card.textMain
                                font.bold: true
                                font.pixelSize: Math.round(12 * card.uiScale)
                                Layout.fillWidth: true
                            }
                        }

                        Text {
                            text: modelData.text
                            color: card.textMuted
                            wrapMode: Text.WordWrap
                            font.pixelSize: Math.round(12 * card.uiScale)
                            lineHeight: 1.25
                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }
    }
}
