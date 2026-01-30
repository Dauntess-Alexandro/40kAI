import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    width: 1200
    height: 780
    visible: true
    title: "40kAI — второй GUI (Qt)"

    property string statusText: "Готово к запуску."

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        TabBar {
            id: mainTabs
            Layout.fillWidth: true

            TabButton { text: "Train" }
            TabButton { text: "Model Metrics" }
            TabButton { text: "Play" }
            TabButton { text: "Settings" }
            TabButton { text: "Оценка" }
        }

        StackLayout {
            id: mainStack
            currentIndex: mainTabs.currentIndex
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                anchors.fill: parent

                Item {
                    anchors.fill: parent
                    anchors.margins: 16

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 12

                    Text {
                        text: "Train Model:"
                        font.pixelSize: 20
                        font.bold: true
                    }

                    GridLayout {
                        columns: 2
                        columnSpacing: 16
                        rowSpacing: 12
                        Layout.fillWidth: true

                        ColumnLayout {
                            spacing: 10
                            Layout.fillWidth: true

                            GroupBox {
                                title: "Настройки"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: 8
                                    anchors.fill: parent

                                    RowLayout {
                                        spacing: 8
                                        Label { text: "# of Games in Training:" }
                                        TextField {
                                            id: numGamesField
                                            text: controller.numGames.toString()
                                            validator: IntValidator { bottom: 1 }
                                            Layout.preferredWidth: 100
                                            onEditingFinished: {
                                                var value = parseInt(text)
                                                if (!isNaN(value)) {
                                                    controller.set_num_games(value)
                                                }
                                            }
                                        }
                                    }

                                    RowLayout {
                                        spacing: 8
                                        Label { text: "Model Faction:" }
                                        RadioButton { text: "Necrons"; checked: true }
                                    }

                                    RowLayout {
                                        spacing: 8
                                        Label { text: "Player Faction:" }
                                        RadioButton { text: "Necrons"; checked: true }
                                    }
                                }
                            }

                            GroupBox {
                                title: "Размеры поля"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: 8
                                    anchors.fill: parent

                                    RowLayout {
                                        spacing: 6
                                        Label { text: "X:" }
                                        TextField {
                                            id: boardXField
                                            text: controller.boardX.toString()
                                            validator: IntValidator { bottom: 1 }
                                            Layout.preferredWidth: 80
                                            onEditingFinished: {
                                                var value = parseInt(text)
                                                if (!isNaN(value)) {
                                                    controller.set_board_x(value)
                                                }
                                            }
                                        }
                                        Button { text: "+"; onClicked: controller.increment_board_x() }
                                        Button { text: "-"; onClicked: controller.decrement_board_x() }
                                    }

                                    RowLayout {
                                        spacing: 6
                                        Label { text: "Y:" }
                                        TextField {
                                            id: boardYField
                                            text: controller.boardY.toString()
                                            validator: IntValidator { bottom: 1 }
                                            Layout.preferredWidth: 80
                                            onEditingFinished: {
                                                var value = parseInt(text)
                                                if (!isNaN(value)) {
                                                    controller.set_board_y(value)
                                                }
                                            }
                                        }
                                        Button { text: "+"; onClicked: controller.increment_board_y() }
                                        Button { text: "-"; onClicked: controller.decrement_board_y() }
                                    }
                                }
                            }
                        }

                        ColumnLayout {
                            spacing: 10
                            Layout.fillWidth: true

                            GroupBox {
                                title: "Ростер"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: 8
                                    anchors.fill: parent

                                    Button {
                                        text: "Army Viewer"
                                        onClicked: armyViewerDialog.open()
                                    }

                                    Label {
                                        text: controller.rosterSummary
                                    }
                                }
                            }

                            GroupBox {
                                title: "Действия"
                                Layout.fillWidth: true

                                GridLayout {
                                    columns: 2
                                    columnSpacing: 8
                                    rowSpacing: 8
                                    anchors.fill: parent

                                    Button {
                                        text: "Clear Model Cache"
                                        enabled: !controller.running
                                        onClicked: clearCacheDialog.open()
                                    }

                                    Button {
                                        text: "Самообучение"
                                        enabled: !controller.running
                                        onClicked: controller.start_self_play()
                                    }

                                    Button {
                                        text: "Train"
                                        enabled: !controller.running
                                        onClicked: controller.start_train()
                                    }

                                    Button {
                                        text: "Тренировать 8x"
                                        enabled: !controller.running
                                        onClicked: controller.start_train_8x()
                                    }
                                }
                            }
                        }
                    }

                    Label {
                        text: root.statusText
                    }

                    Label {
                        text: controller.progressLabel
                    }

                    Item {
                        Layout.fillWidth: true
                        height: 24

                        ProgressBar {
                            id: trainingProgress
                            anchors.fill: parent
                            value: controller.progressValue
                        }

                        Text {
                            anchors.centerIn: parent
                            text: controller.progressText
                            color: "#ffffff"
                        }
                    }

                    Label {
                        text: controller.progressStats
                    }

                    GroupBox {
                        title: "Логи"
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        ScrollView {
                            anchors.fill: parent

                            TextArea {
                                id: logArea
                                readOnly: true
                                wrapMode: TextArea.Wrap
                                text: ""
                            }
                        }
                    }
                    }
                }
            }

            Item {
                anchors.fill: parent
                Label {
                    anchors.centerIn: parent
                    text: "Скоро"
                }
            }

            Item {
                anchors.fill: parent
                Label {
                    anchors.centerIn: parent
                    text: "Скоро"
                }
            }

            Item {
                anchors.fill: parent
                Label {
                    anchors.centerIn: parent
                    text: "Скоро"
                }
            }

            Item {
                anchors.fill: parent
                Label {
                    anchors.centerIn: parent
                    text: "Скоро"
                }
            }
        }
    }

    Dialog {
        id: clearCacheDialog
        title: "Очистка кэша"
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        onAccepted: controller.clear_model_cache()

        contentItem: Text {
            text: "Вы действительно хотите удалить все сохранённые модели и метрики?"
            wrapMode: Text.WordWrap
            width: 360
        }
    }

    Dialog {
        id: armyViewerDialog
        title: "Army Viewer"
        modal: true
        standardButtons: Dialog.Close
        width: 900
        height: 500

        ColumnLayout {
            anchors.fill: parent
            spacing: 12

            RowLayout {
                spacing: 12
                Layout.fillWidth: true
                Layout.fillHeight: true

                GroupBox {
                    title: "Доступные юниты (Necrons)"
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8

                        ListView {
                            id: availableUnitsView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: controller.availableUnitsModel
                            clip: true
                            delegate: ItemDelegate {
                                text: modelData
                                width: parent.width
                                highlighted: ListView.isCurrentItem
                            }
                        }

                        RowLayout {
                            spacing: 8
                            Button {
                                text: "Добавить в игрока"
                                onClicked: controller.add_unit_to_player(availableUnitsView.currentIndex)
                            }
                            Button {
                                text: "Добавить в модель"
                                onClicked: controller.add_unit_to_model(availableUnitsView.currentIndex)
                            }
                        }
                    }
                }

                GroupBox {
                    title: "Ростер игрока"
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8

                        ListView {
                            id: playerRosterView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: controller.playerRosterModel
                            clip: true
                            delegate: ItemDelegate {
                                text: modelData
                                width: parent.width
                                highlighted: ListView.isCurrentItem
                            }
                        }

                        RowLayout {
                            spacing: 8
                            Button {
                                text: "Удалить"
                                onClicked: controller.remove_player_unit(playerRosterView.currentIndex)
                            }
                            Button {
                                text: "Очистить"
                                onClicked: controller.clear_player_roster()
                            }
                        }
                    }
                }

                GroupBox {
                    title: "Ростер модели"
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8

                        ListView {
                            id: modelRosterView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: controller.modelRosterModel
                            clip: true
                            delegate: ItemDelegate {
                                text: modelData
                                width: parent.width
                                highlighted: ListView.isCurrentItem
                            }
                        }

                        RowLayout {
                            spacing: 8
                            Button {
                                text: "Удалить"
                                onClicked: controller.remove_model_unit(modelRosterView.currentIndex)
                            }
                            Button {
                                text: "Очистить"
                                onClicked: controller.clear_model_roster()
                            }
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: controller
        function onLogLine(message) {
            logArea.text += message + "\n"
            logArea.cursorPosition = logArea.length
        }
        function onStatusChanged(message) {
            root.statusText = message
        }
        function onNumGamesChanged(value) {
            numGamesField.text = value.toString()
        }
        function onBoardXChanged(value) {
            boardXField.text = value.toString()
        }
        function onBoardYChanged(value) {
            boardYField.text = value.toString()
        }
    }
}
