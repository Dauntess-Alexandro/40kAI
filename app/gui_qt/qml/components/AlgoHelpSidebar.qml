import QtQuick
import QtQuick.Controls

Item {
    id: root

    property int currentIndex: 0
    property var rootUi: null
    signal indexSelected(int idx)

    property real uiScale:    rootUi ? rootUi.uiScale    : 1.0
    property color textMain:  rootUi ? rootUi.uiTextMain  : "#d7dde7"
    property color textMuted: rootUi ? rootUi.uiTextMuted : "#98a4b8"
    property color borderCol: rootUi ? rootUi.uiBorder    : "#334155"

    readonly property var groups: [
        { family: qsTr("Off-policy"), items: [
            { name: "DQN",      idx: 0, color: "#2563eb" },
            { name: "PHOENIX",  idx: 1, color: "#f59e0b" }
        ]},
        { family: qsTr("On-policy"), items: [
            { name: "PPO",      idx: 2, color: "#0d9488" }
        ]},
        { family: qsTr("AlphaZero"), items: [
            { name: "AZ Tree",  idx: 3, color: "#7c3aed" },
            { name: "AZ Proxy", idx: 4, color: "#6366f1" },
            { name: "GAZ",      idx: 7, color: "#0891b2" }
        ]},
        { family: qsTr("MuZero"), items: [
            { name: "GMZ",      idx: 5, color: "#d97706" },
            { name: "SMZ",      idx: 6, color: "#be185d" }
        ]}
    ]

    Rectangle {
        anchors.fill: parent
        color: "#0b1220"
        border.color: root.borderCol
        border.width: 1

        ScrollView {
            id: sv
            anchors.fill: parent
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            ScrollBar.vertical.policy: ScrollBar.AsNeeded

            Column {
                width: sv.width
                spacing: 0

                Repeater {
                    model: root.groups
                    delegate: Column {
                        required property var modelData
                        width: sv.width
                        spacing: 0

                        Item {
                            width: parent.width
                            height: familyLabel.implicitHeight + Math.round(18 * root.uiScale)

                            Text {
                                id: familyLabel
                                anchors.left: parent.left
                                anchors.leftMargin: Math.round(12 * root.uiScale)
                                anchors.bottom: parent.bottom
                                anchors.bottomMargin: Math.round(5 * root.uiScale)
                                text: modelData.family
                                color: "#607396"
                                font.bold: true
                                font.pixelSize: Math.round(10 * root.uiScale)
                                font.letterSpacing: 0.7
                            }
                        }

                        Repeater {
                            model: modelData.items
                            delegate: Item {
                                id: algoItem
                                required property var modelData
                                width: sv.width
                                height: Math.round(32 * root.uiScale)

                                readonly property bool active: root.currentIndex === modelData.idx
                                readonly property color ic:    modelData.color

                                Rectangle {
                                    anchors.fill: parent
                                    color: algoItem.active
                                        ? Qt.rgba(algoItem.ic.r, algoItem.ic.g, algoItem.ic.b, 0.15)
                                        : (rowMa.containsMouse ? Qt.rgba(1, 1, 1, 0.04) : "transparent")

                                    Rectangle {
                                        visible: algoItem.active
                                        width: Math.round(2 * root.uiScale)
                                        height: parent.height
                                        color: algoItem.ic
                                    }

                                    Row {
                                        anchors.verticalCenter: parent.verticalCenter
                                        anchors.left: parent.left
                                        anchors.leftMargin: Math.round(12 * root.uiScale)
                                        anchors.right: parent.right
                                        anchors.rightMargin: Math.round(8 * root.uiScale)
                                        spacing: Math.round(8 * root.uiScale)

                                        Item {
                                            width: Math.round(10 * root.uiScale)
                                            height: Math.round(10 * root.uiScale)
                                            anchors.verticalCenter: parent.verticalCenter

                                            Rectangle {
                                                width: Math.round(7 * root.uiScale)
                                                height: Math.round(7 * root.uiScale)
                                                anchors.centerIn: parent
                                                rotation: 45
                                                color: algoItem.ic
                                            }
                                        }

                                        Text {
                                            width: parent.width - Math.round(18 * root.uiScale)
                                            text: modelData.name
                                            color: algoItem.active ? root.textMain : root.textMuted
                                            font.pixelSize: Math.round(13 * root.uiScale)
                                            font.bold: algoItem.active
                                            elide: Text.ElideRight
                                            anchors.verticalCenter: parent.verticalCenter
                                        }
                                    }

                                    MouseArea {
                                        id: rowMa
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: root.indexSelected(algoItem.modelData.idx)
                                    }
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    width: sv.width - Math.round(20 * root.uiScale)
                    x: Math.round(10 * root.uiScale)
                    height: 1
                    color: root.borderCol
                    anchors.margins: Math.round(10 * root.uiScale)
                }

                Item {
                    id: compareItem
                    width: sv.width
                    height: Math.round(32 * root.uiScale)

                    readonly property bool active: root.currentIndex === 8

                    Rectangle {
                        anchors.fill: parent
                        color: compareItem.active
                            ? Qt.rgba(0.6, 0.63, 0.65, 0.12)
                            : (compMa.containsMouse ? Qt.rgba(1, 1, 1, 0.04) : "transparent")

                        Rectangle {
                            visible: compareItem.active
                            width: Math.round(2 * root.uiScale)
                            height: parent.height
                            color: "#9ca3af"
                        }

                        Row {
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.leftMargin: Math.round(12 * root.uiScale)
                            anchors.right: parent.right
                            anchors.rightMargin: Math.round(8 * root.uiScale)
                            spacing: Math.round(8 * root.uiScale)

                            Item {
                                width: Math.round(10 * root.uiScale)
                                height: Math.round(10 * root.uiScale)
                                anchors.verticalCenter: parent.verticalCenter

                                Rectangle {
                                    width: Math.round(7 * root.uiScale)
                                    height: Math.round(7 * root.uiScale)
                                    anchors.centerIn: parent
                                    rotation: 45
                                    color: "#9ca3af"
                                }
                            }

                            Text {
                                width: parent.width - Math.round(18 * root.uiScale)
                                text: qsTr("Сравнение")
                                color: compareItem.active ? root.textMain : root.textMuted
                                font.pixelSize: Math.round(13 * root.uiScale)
                                font.bold: compareItem.active
                                elide: Text.ElideRight
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }

                        MouseArea {
                            id: compMa
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.indexSelected(8)
                        }
                    }
                }

                Item { width: sv.width; height: Math.round(8 * root.uiScale) }
            }
        }
    }
}
