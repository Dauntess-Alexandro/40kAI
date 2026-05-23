import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: table

    property var rootUi: null
    property real uiScale: rootUi ? rootUi.uiScale : 1.0
    property color textMain: rootUi ? rootUi.uiTextMain : "#d7dde7"
    property color textMuted: rootUi ? rootUi.uiTextMuted : "#98a4b8"
    property color bgFill: rootUi ? rootUi.bgElevated : "#1E293B"
    property color borderColor: rootUi ? rootUi.uiBorder : "#334155"

    readonly property var algoColors: [
        "#2563eb", "#0d9488", "#7c3aed", "#6366f1", "#d97706"
    ]
    readonly property var algoNames: ["DQN", "PPO", "AZ Tree", "AZ Proxy", "GMZ"]

    readonly property var rows: [
        { label: "Поиск на ходу",  values: ["—", "—", "MCTS", "proxy", "MCTS + model"] },
        { label: "Self-play",      values: ["—", "—", "+", "+", "+"] },
        { label: "Скорость train", values: ["★★★", "★★★★", "★★", "★★★", "★"] },
        { label: "Скорость хода",  values: ["★★★★", "★★★★", "★★", "★★★", "★★"] },
        { label: "Потолок силы",   values: ["★★", "★★★", "★★★★★", "★★★", "★★★★★"] },
        { label: "Compute",        values: ["low", "low", "very high", "mid", "very high"] },
        { label: "Сложность тюна", values: ["mid", "low", "high", "mid", "very high"] },
        { label: "Температура",    values: ["—", "—", "в MCTS", "в search", "в Search"] }
    ]

    readonly property int cols: 6
    readonly property int firstColWidth: Math.round(150 * uiScale)
    readonly property int otherColWidth: Math.max(
        Math.round(70 * uiScale),
        Math.floor((width - firstColWidth - Math.round(28 * uiScale) - 5 * Math.round(8 * uiScale)) / 5)
    )

    function cellText(rowIdx, colIdx) {
        if (rowIdx < 0 || rowIdx >= rows.length || colIdx < 0 || colIdx >= cols)
            return ""
        var row = rows[rowIdx]
        if (!row)
            return ""
        if (colIdx === 0)
            return row.label ? String(row.label) : ""
        var vals = row.values
        if (!vals || colIdx - 1 < 0 || colIdx - 1 >= vals.length)
            return ""
        var v = vals[colIdx - 1]
        return (v === undefined || v === null) ? "" : String(v)
    }

    radius: Math.round(12 * uiScale)
    color: bgFill
    border.color: borderColor
    border.width: 1
    implicitHeight: tableColumn.implicitHeight + Math.round(24 * uiScale)

    ColumnLayout {
        id: tableColumn
        anchors.fill: parent
        anchors.margins: Math.round(14 * table.uiScale)
        spacing: Math.round(8 * table.uiScale)

        Text {
            text: "Сравнение моделей"
            font.bold: true
            font.pixelSize: Math.round(15 * table.uiScale)
            color: table.textMain
            Layout.fillWidth: true
        }
        Text {
            text: "Звёзды — относительная оценка внутри проекта (не бенчмарк)."
            color: table.textMuted
            font.italic: true
            font.pixelSize: Math.round(11 * table.uiScale)
            Layout.fillWidth: true
        }

        Column {
            id: grid
            spacing: Math.round(4 * table.uiScale)

            Row {
                spacing: Math.round(8 * table.uiScale)
                Item {
                    width: table.firstColWidth
                    height: Math.round(28 * table.uiScale)
                }
                Repeater {
                    model: table.algoNames.length
                    delegate: Rectangle {
                        required property int index
                        width: table.otherColWidth
                        height: Math.round(28 * table.uiScale)
                        radius: Math.round(6 * table.uiScale)
                        color: {
                            var c = Qt.color(table.algoColors[index])
                            return Qt.rgba(c.r, c.g, c.b, 0.22)
                        }

                        Text {
                            anchors.centerIn: parent
                            text: table.algoNames[parent.index]
                            color: table.textMain
                            font.bold: true
                            font.pixelSize: Math.round(12 * table.uiScale)
                        }
                    }
                }
            }

            Repeater {
                model: table.rows.length
                delegate: Row {
                    id: dataRow
                    required property int index
                    spacing: Math.round(8 * table.uiScale)

                    property int rowIdx: index

                    Rectangle {
                        width: table.firstColWidth
                        height: Math.round(26 * table.uiScale)
                        radius: Math.round(4 * table.uiScale)
                        color: dataRow.rowIdx % 2 === 0 ? Qt.rgba(1, 1, 1, 0.025) : "transparent"

                        Text {
                            anchors.left: parent.left
                            anchors.leftMargin: Math.round(6 * table.uiScale)
                            anchors.verticalCenter: parent.verticalCenter
                            text: table.cellText(dataRow.rowIdx, 0)
                            color: table.textMuted
                            font.bold: true
                            font.pixelSize: Math.round(12 * table.uiScale)
                        }
                    }

                    Repeater {
                        model: table.algoNames.length
                        delegate: Rectangle {
                            required property int index
                            width: table.otherColWidth
                            height: Math.round(26 * table.uiScale)
                            radius: Math.round(4 * table.uiScale)
                            color: dataRow.rowIdx % 2 === 0 ? Qt.rgba(1, 1, 1, 0.025) : "transparent"

                            Text {
                                anchors.centerIn: parent
                                text: table.cellText(dataRow.rowIdx, parent.index + 1)
                                color: table.textMain
                                font.pixelSize: Math.round(12 * table.uiScale)
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                    }
                }
            }
        }
    }
}
