import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: logRoot
    color: bgSurfaceColor
    clip: true

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined

    readonly property var filterDefs: [
        { key: "movement", icon: "👣", tip: qsTr("Движение") },
        { key: "shooting", icon: "🎯", tip: qsTr("Стрельба") },
        { key: "charge", icon: "⚡", tip: qsTr("Заряд") },
        { key: "fight", icon: "⚔️", tip: qsTr("Бой") },
        { key: "result", icon: "🏁", tip: qsTr("Итог") },
        { key: "errors", icon: "⚠️", tip: qsTr("Ошибки") },
        { key: "debug", icon: "🧪", tip: qsTr("Отладка") }
    ]

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 4
        spacing: 4

        TextField {
            id: searchField
            Layout.fillWidth: true
            placeholderText: qsTr("Поиск в журнале…")
            font.family: monoFontFamily
            font.pixelSize: monoFontSize
            onTextChanged: if (hasCtrl) viewerController.setLogSearchText(text)
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 2
            Repeater {
                model: filterDefs
                delegate: Item {
                    required property var modelData
                    implicitWidth: filterBtn.width + (badge.visible ? 8 : 0)
                    implicitHeight: filterBtn.height

                    ToolButton {
                        id: filterBtn
                        text: modelData.icon
                        checkable: true
                        checked: hasCtrl && (viewerController.logFilters[modelData.key] === true)
                        onToggled: if (hasCtrl) viewerController.setLogFilter(modelData.key, checked)
                        ToolTip.visible: hovered
                        ToolTip.text: modelData.tip
                    }

                    Rectangle {
                        id: badge
                        visible: hasCtrl
                            && !filterBtn.checked
                            && viewerController.logFilterHiddenCounts[modelData.key] > 0
                        anchors.right: filterBtn.right
                        anchors.top: filterBtn.top
                        anchors.margins: -2
                        width: badgeLbl.implicitWidth + 6
                        height: badgeLbl.implicitHeight + 4
                        radius: 6
                        color: "#e06c75"
                        Label {
                            id: badgeLbl
                            anchors.centerIn: parent
                            text: hasCtrl ? String(viewerController.logFilterHiddenCounts[modelData.key]) : ""
                            color: "#ffffff"
                            font.pixelSize: fontXs
                            font.bold: true
                        }
                    }
                }
            }
            ToolButton {
                text: "🧹"
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Очистить всё")
                onClicked: if (hasCtrl) viewerController.onLogClearRequested()
            }
        }

        ListView {
            id: logList
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            spacing: 2
            model: viewerLogModel
            cacheBuffer: 400

            ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }

            delegate: Item {
                width: logList.width
                height: headerBlock.visible ? headerBlock.height : rowBlock.height

                Rectangle {
                    id: headerBlock
                    anchors.left: parent.left
                    anchors.right: parent.right
                    visible: model.logIsHeader
                    height: visible ? headerLbl.implicitHeight + 10 : 0
                    color: model.logIsCurrentTurn ? Qt.rgba(0.18, 0.35, 0.55, 0.35) : bgElevatedColor
                    radius: radiusSm
                    Label {
                        id: headerLbl
                        anchors.fill: parent
                        anchors.margins: 5
                        text: model.logHeaderText
                        color: accentColor
                        font.bold: true
                        font.pixelSize: fontMd
                    }
                }

                Rectangle {
                    id: rowBlock
                    anchors.fill: parent
                    visible: !model.logIsHeader
                    color: rowMouse.containsMouse ? "#1b2740" : (model.logIsCurrentTurn ? Qt.rgba(0.1, 0.2, 0.35, 0.2) : "transparent")
                    radius: 4

                    Rectangle {
                        width: 3
                        height: parent.height - 4
                        anchors.left: parent.left
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.leftMargin: 2
                        color: {
                            var k = model.logKind || "system"
                            if (k === "movement") return playerColor
                            if (k === "shooting") return objectiveColor
                            if (k === "charge") return "#d97706"
                            if (k === "fight") return modelColor
                            if (k === "errors") return "#e06c75"
                            return borderMutedColor
                        }
                    }

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 4
                        anchors.leftMargin: 8
                        spacing: 6

                        Label {
                            text: {
                                var k = model.logKind || "system"
                                if (k === "movement") return "👣"
                                if (k === "shooting") return "🎯"
                                if (k === "charge") return "⚡"
                                if (k === "fight") return "⚔️"
                                if (k === "result") return "🏁"
                                if (k === "errors") return "⚠️"
                                if (k === "debug") return "🧪"
                                return "•"
                            }
                            font.pixelSize: fontSm
                        }
                        Label {
                            text: model.logTimestamp
                            color: textSecondaryColor
                            font.family: monoFontFamily
                            font.pixelSize: fontXs
                            Layout.preferredWidth: 36
                        }
                        Label {
                            Layout.fillWidth: true
                            text: model.logText
                            color: model.logColor
                            wrapMode: Text.Wrap
                            font.family: monoFontFamily
                            font.pixelSize: monoFontSize
                        }
                    }

                    MouseArea {
                        id: rowMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        acceptedButtons: Qt.LeftButton
                        onClicked: { if (hasCtrl) viewerController.onLogRowClicked(index) }
                        onEntered: { if (hasCtrl) viewerController.onLogRowHovered(index) }
                        onExited: { if (hasCtrl) viewerController.onLogHoverExited() }
                    }
                }
            }

            ColumnLayout {
                anchors.centerIn: parent
                visible: logList.count === 0
                spacing: spacingSm
                width: logList.width - 20

                Label {
                    Layout.fillWidth: true
                    text: qsTr("Сделайте ход — здесь появится лента событий")
                    color: textSecondaryColor
                    font.pixelSize: fontMd
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignHCenter
                }
                Button {
                    Layout.alignment: Qt.AlignHCenter
                    text: qsTr("Открыть быструю партию")
                    onClicked: if (hasCtrl) viewerController.startQuickMatch()
                }
            }

            Connections {
                target: hasCtrl ? viewerController : null
                enabled: hasCtrl
                function onLogRevisionChanged() {
                    Qt.callLater(function () { logList.positionViewAtEnd() })
                }
            }
        }
    }
}
