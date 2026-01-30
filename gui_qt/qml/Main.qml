import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.platform 1.1 as Platform

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
                Layout.fillWidth: true
                Layout.fillHeight: true

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

                                    Label {
                                        text: controller.rosterSummary
                                        font.bold: true
                                    }

                                    Label {
                                        text: "Доступные юниты (Necrons)"
                                    }

                                    ListView {
                                        id: availableUnitsInline
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 180
                                        model: controller.availableUnitsModel
                                        clip: true
                                        delegate: ItemDelegate {
                                            text: modelData
                                            width: ListView.view ? ListView.view.width : 0
                                            highlighted: ListView.isCurrentItem
                                        }
                                    }

                                    RowLayout {
                                        spacing: 8
                                        Button {
                                            text: "Добавить в игрока"
                                            onClicked: controller.add_unit_to_player(availableUnitsInline.currentIndex)
                                        }
                                        Button {
                                            text: "Добавить в модель"
                                            onClicked: controller.add_unit_to_model(availableUnitsInline.currentIndex)
                                        }
                                    }

                                    Button {
                                        text: "Army Viewer"
                                        onClicked: armyViewerDialog.open()
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
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 12

                    Text {
                        text: "Model Metrics"
                        font.pixelSize: 20
                        font.bold: true
                    }

                    RowLayout {
                        spacing: 12
                        Layout.fillWidth: true

                        Button {
                            text: "Выбрать модель"
                            onClicked: metricsFileDialog.open()
                        }

                        Label {
                            text: controller.metricsLabel
                            Layout.fillWidth: true
                            elide: Label.ElideRight
                        }
                    }

                    GridLayout {
                        columns: 2
                        columnSpacing: 12
                        rowSpacing: 12
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        GroupBox {
                            title: "Награда за эпизод"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: 6

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true

                                    Image {
                                        id: rewardChart
                                        anchors.fill: parent
                                        source: controller.metricsRewardPath
                                        fillMode: Image.PreserveAspectFit
                                        smooth: true
                                    }

                                    Text {
                                        anchors.centerIn: parent
                                        text: "Нет данных по наградам."
                                        color: "#777777"
                                        visible: rewardChart.status !== Image.Ready
                                    }
                                }

                                Label {
                                    text: "Средняя награда по ходу обучения."
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        GroupBox {
                            title: "Потери (loss)"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: 6

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true

                                    Image {
                                        id: lossChart
                                        anchors.fill: parent
                                        source: controller.metricsLossPath
                                        fillMode: Image.PreserveAspectFit
                                        smooth: true
                                    }

                                    Text {
                                        anchors.centerIn: parent
                                        text: "Нет данных по loss."
                                        color: "#777777"
                                        visible: lossChart.status !== Image.Ready
                                    }
                                }

                                Label {
                                    text: "Динамика функции потерь."
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        GroupBox {
                            title: "Длина эпизода"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: 6

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true

                                    Image {
                                        id: epLenChart
                                        anchors.fill: parent
                                        source: controller.metricsEpLenPath
                                        fillMode: Image.PreserveAspectFit
                                        smooth: true
                                    }

                                    Text {
                                        anchors.centerIn: parent
                                        text: "Нет данных по длине эпизода."
                                        color: "#777777"
                                        visible: epLenChart.status !== Image.Ready
                                    }
                                }

                                Label {
                                    text: "Сколько ходов длится партия."
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        GroupBox {
                            title: "Winrate"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: 6

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true

                                    Image {
                                        id: winrateChart
                                        anchors.fill: parent
                                        source: controller.metricsWinratePath
                                        fillMode: Image.PreserveAspectFit
                                        smooth: true
                                    }

                                    Text {
                                        anchors.centerIn: parent
                                        text: "Нет данных по winrate."
                                        color: "#777777"
                                        visible: winrateChart.status !== Image.Ready
                                    }
                                }

                                Label {
                                    text: "Доля побед модели по играм."
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        GroupBox {
                            title: "Разница VP"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: 6

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true

                                    Image {
                                        id: vpDiffChart
                                        anchors.fill: parent
                                        source: controller.metricsVpDiffPath
                                        fillMode: Image.PreserveAspectFit
                                        smooth: true
                                    }

                                    Text {
                                        anchors.centerIn: parent
                                        text: "Нет данных по VP."
                                        color: "#777777"
                                        visible: vpDiffChart.status !== Image.Ready
                                    }
                                }

                                Label {
                                    text: "Разница очков победы между сторонами."
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        GroupBox {
                            title: "Причины завершения"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: 6

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true

                                    Image {
                                        id: endReasonChart
                                        anchors.fill: parent
                                        source: controller.metricsEndReasonPath
                                        fillMode: Image.PreserveAspectFit
                                        smooth: true
                                    }

                                    Text {
                                        anchors.centerIn: parent
                                        text: "Нет данных по причинам завершения."
                                        color: "#777777"
                                        visible: endReasonChart.status !== Image.Ready
                                    }
                                }

                                Label {
                                    text: "Почему эпизоды завершались."
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Label {
                    anchors.centerIn: parent
                    text: "Скоро"
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Label {
                    anchors.centerIn: parent
                    text: "Скоро"
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
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
        implicitWidth: 420
        onAccepted: controller.clear_model_cache()

        contentItem: Text {
            text: "Вы действительно хотите удалить все сохранённые модели и метрики?"
            wrapMode: Text.WordWrap
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
                                width: ListView.view ? ListView.view.width : 0
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
                                width: ListView.view ? ListView.view.width : 0
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
                                width: ListView.view ? ListView.view.width : 0
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

    Platform.FileDialog {
        id: metricsFileDialog
        title: "Выберите модель (.pickle)"
        nameFilters: ["Pickle Files (*.pickle)"]
        folder: Platform.StandardPaths.writableLocation(Platform.StandardPaths.DocumentsLocation)
        onAccepted: controller.select_metrics_file(fileUrl)
    }
}
