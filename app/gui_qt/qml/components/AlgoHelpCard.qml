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
    property string role: ""
    property string abbr: ""
    property var stats: []

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

            // --- датащит-шапка (когда задана аббревиатура) ---
            Row {
                visible: card.abbr.length > 0
                Layout.fillWidth: true
                spacing: Math.round(14 * card.uiScale)

                Item {
                    width: Math.round(54 * card.uiScale)
                    height: Math.round(54 * card.uiScale)

                    Rectangle {
                        width: Math.round(38 * card.uiScale)
                        height: Math.round(38 * card.uiScale)
                        anchors.centerIn: parent
                        rotation: 45
                        color: card.accentColor

                        Text {
                            anchors.centerIn: parent
                            rotation: -45
                            text: card.abbr
                            color: "white"
                            font.bold: true
                            font.pixelSize: Math.round(13 * card.uiScale)
                        }
                    }
                }

                Column {
                    width: parent.width - Math.round(68 * card.uiScale)
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: Math.round(3 * card.uiScale)

                    Text {
                        width: parent.width
                        text: card.algoTitle
                        font.bold: true
                        font.pixelSize: Math.round(18 * card.uiScale)
                        color: card.textMain
                        elide: Text.ElideRight
                    }
                    Text {
                        visible: card.role.length > 0
                        width: parent.width
                        text: card.role.toUpperCase()
                        color: card.accentColor
                        font.bold: true
                        font.pixelSize: Math.round(11 * card.uiScale)
                        font.letterSpacing: 0.7
                        elide: Text.ElideRight
                    }
                    Text {
                        visible: card.tldr.length > 0
                        width: parent.width
                        text: card.tldr
                        wrapMode: Text.WordWrap
                        color: card.textMuted
                        font.italic: true
                        font.pixelSize: Math.round(12 * card.uiScale)
                    }
                }
            }

            // --- блок стат-баров ---
            Rectangle {
                visible: card.stats.length > 0
                Layout.fillWidth: true
                implicitHeight: statsCol.implicitHeight + Math.round(24 * card.uiScale)
                color: "#0b1322"
                radius: Math.round(9 * card.uiScale)
                border.color: "#21314c"
                border.width: 1

                Column {
                    id: statsCol
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: Math.round(12 * card.uiScale)
                    spacing: Math.round(8 * card.uiScale)

                    Repeater {
                        model: card.stats
                        delegate: Row {
                            required property var modelData
                            width: statsCol.width
                            spacing: Math.round(10 * card.uiScale)

                            Text {
                                width: Math.round(130 * card.uiScale)
                                text: modelData.label
                                color: "#93a6c0"
                                font.bold: true
                                font.pixelSize: Math.round(11 * card.uiScale)
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            Rectangle {
                                width: parent.width - Math.round(172 * card.uiScale)
                                height: Math.round(8 * card.uiScale)
                                radius: Math.round(4 * card.uiScale)
                                color: "#1a2742"
                                anchors.verticalCenter: parent.verticalCenter

                                Rectangle {
                                    width: parent.width * modelData.value / 5
                                    height: parent.height
                                    radius: parent.radius
                                    color: "#5a8fff"
                                }
                            }

                            Text {
                                width: Math.round(32 * card.uiScale)
                                text: modelData.value + "/5"
                                color: "#dfeaff"
                                font.pixelSize: Math.round(12 * card.uiScale)
                                font.family: "Courier New"
                                horizontalAlignment: Text.AlignRight
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }
                    }
                }
            }

            // --- простой заголовок (когда аббревиатуры нет, напр. таблица сравнения) ---
            Text {
                visible: card.abbr.length === 0
                text: card.algoTitle
                font.bold: true
                font.pixelSize: Math.round(16 * card.uiScale)
                color: card.textMain
                Layout.fillWidth: true
            }

            Text {
                visible: card.abbr.length === 0 && card.tldr.length > 0
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
