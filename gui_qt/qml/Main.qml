import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import Qt.labs.platform 1.1 as Platform

ApplicationWindow {
    id: root
    width: Math.round(Screen.width * 0.85)
    height: Math.round(Screen.height * 0.85)
    visible: true
    title: "40kAI — второй GUI (Qt)"

    property string statusText: "Готово к запуску."
    property real uiScale: Math.max(1.0, Math.min(Screen.width / 1920, Screen.height / 1080))
    property int spacingXs: Math.round(6 * uiScale)
    property int spacingSm: Math.round(8 * uiScale)
    property int spacingMd: Math.round(12 * uiScale)
    property int spacingLg: Math.round(16 * uiScale)
    property int spacingXl: Math.round(20 * uiScale)
    property int inputWidthSm: Math.round(80 * uiScale)
    property int inputWidthMd: Math.round(100 * uiScale)
    property int listHeightSm: Math.round(180 * uiScale)
    property int dialogWidthSm: Math.round(420 * uiScale)
    property int dialogWidthLg: Math.round(720 * uiScale)
    property int dialogWidthXl: Math.round(900 * uiScale)
    property int dialogHeightMd: Math.round(520 * uiScale)
    property int dialogHeightLg: Math.round(500 * uiScale)

    font.pixelSize: Math.round(14 * uiScale)

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
                    anchors.margins: root.spacingLg

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: root.spacingMd

                    Text {
                        text: "Train Model:"
                        font.pixelSize: Math.round(20 * root.uiScale)
                        font.bold: true
                    }

                    GridLayout {
                        columns: 2
                        columnSpacing: root.spacingLg
                        rowSpacing: root.spacingMd
                        Layout.fillWidth: true

                        ColumnLayout {
                            spacing: root.spacingSm
                            Layout.fillWidth: true

                            GroupBox {
                                title: "Настройки"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: root.spacingSm
                                    anchors.fill: parent

                                    RowLayout {
                                        spacing: root.spacingSm
                                        Label { text: "# of Games in Training:" }
                                        TextField {
                                            id: numGamesField
                                            text: controller.numGames.toString()
                                            validator: IntValidator { bottom: 1 }
                                            Layout.preferredWidth: root.inputWidthMd
                                            onEditingFinished: {
                                                var value = parseInt(text)
                                                if (!isNaN(value)) {
                                                    controller.set_num_games(value)
                                                }
                                            }
                                        }
                                    }

                                    RowLayout {
                                        spacing: root.spacingSm
                                        Label { text: "Model Faction:" }
                                        RadioButton { text: "Necrons"; checked: true }
                                    }

                                    RowLayout {
                                        spacing: root.spacingSm
                                        Label { text: "Player Faction:" }
                                        RadioButton { text: "Necrons"; checked: true }
                                    }
                                }
                            }

                            GroupBox {
                                title: "Миссия"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: root.spacingSm
                                    anchors.fill: parent

                                    Label { text: "Выбор миссии" }
                                    ComboBox {
                                        id: missionCombo
                                        Layout.preferredWidth: root.inputWidthMd
                                        model: controller.missionOptions
                                        currentIndex: Math.max(0, controller.missionOptions.indexOf(controller.selectedMission))
                                        onActivated: controller.set_selected_mission_index(currentIndex)
                                    }
                                    Label {
                                        text: "Only War: 60x40, 1 objective по центру, деплой attacker/defender слева/справа"
                                        wrapMode: Text.Wrap
                                    }
                                }
                            }
                        }

                        ColumnLayout {
                            spacing: root.spacingSm
                            Layout.fillWidth: true

                            GroupBox {
                                title: "Ростер"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: root.spacingSm
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
                                        Layout.preferredHeight: root.listHeightSm
                                        model: controller.availableUnitsModel
                                        clip: true
                                        delegate: Rectangle {
                                            width: ListView.view ? ListView.view.width : 0
                                            height: unitNameInline.implicitHeight + root.spacingSm
                                            color: ListView.isCurrentItem ? "#2d89ef" : "transparent"

                                            Text {
                                                id: unitNameInline
                                                text: model.display
                                                color: ListView.isCurrentItem ? "#ffffff" : "#1f1f1f"
                                                elide: Text.ElideRight
                                                anchors.verticalCenter: parent.verticalCenter
                                                anchors.left: parent.left
                                                anchors.leftMargin: root.spacingSm
                                            }
                                        }
                                    }

                                    RowLayout {
                                        spacing: root.spacingSm
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
                                    columnSpacing: root.spacingSm
                                    rowSpacing: root.spacingSm
                                    anchors.fill: parent

                                    CheckBox {
                                        text: "Самообучение от старой модели"
                                        checked: controller.selfPlayFromCheckpoint
                                        enabled: !controller.running
                                        Layout.columnSpan: 2
                                        onToggled: controller.set_self_play_from_checkpoint(checked)
                                    }

                                    Button {
                                        text: "Тренировка 8х"
                                        enabled: !controller.running
                                        onClicked: controller.start_train_8x()
                                    }

                                    Button {
                                        text: "Самообучение"
                                        enabled: !controller.running
                                        onClicked: controller.start_self_play()
                                    }

                                    Button {
                                        text: "Очистить кеш"
                                        enabled: !controller.running
                                        onClicked: clearCacheDialog.open()
                                    }

                                    Button {
                                        text: "Очистить логи"
                                        enabled: !controller.running
                                        onClicked: controller.clear_agent_logs()
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
                        height: Math.round(24 * root.uiScale)

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
                    anchors.margins: root.spacingLg
                    spacing: root.spacingMd

                    Text {
                        text: "Model Metrics"
                        font.pixelSize: Math.round(20 * root.uiScale)
                        font.bold: true
                    }

                    RowLayout {
                        spacing: root.spacingMd
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
                        columnSpacing: root.spacingMd
                        rowSpacing: root.spacingMd
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        GroupBox {
                            title: "Награда за эпизод"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingXs

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
                                spacing: root.spacingXs

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
                                spacing: root.spacingXs

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
                                spacing: root.spacingXs

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
                                spacing: root.spacingXs

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
                                spacing: root.spacingXs

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
                Item {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: root.spacingLg

                        Text {
                            text: "Играть против модели"
                            font.pixelSize: Math.round(20 * root.uiScale)
                            font.bold: true
                        }

                        GroupBox {
                            title: "Модель"
                            Layout.fillWidth: true

                            ColumnLayout {
                                spacing: root.spacingSm
                                anchors.fill: parent

                                RowLayout {
                                    spacing: root.spacingSm
                                    Label { text: "Выбрать модель:" }
                                    Button {
                                        text: "Выбрать"
                                        onClicked: playModelDialog.open()
                                    }
                                    Button {
                                        text: "Последняя"
                                        onClicked: controller.select_latest_play_model()
                                    }
                                }

                                Label {
                                    text: controller.playModelLabel
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        GroupBox {
                            title: "Запуск"
                            Layout.fillWidth: true

                            RowLayout {
                                spacing: root.spacingMd
                                anchors.fill: parent

                                Button {
                                    text: "Играть в терминале"
                                    onClicked: controller.play_in_terminal()
                                }
                                Button {
                                    text: "Играть в GUI"
                                    onClicked: controller.play_in_gui()
                                }
                                Button {
                                    text: "Показать ASCII карту"
                                    onClicked: asciiBoardDialog.open()
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
        }
    }

    Dialog {
        id: clearCacheDialog
        title: "Очистка кэша"
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        implicitWidth: root.dialogWidthSm
        onAccepted: controller.clear_model_cache()

        contentItem: Text {
            text: "Вы действительно хотите удалить все сохранённые модели и метрики?"
            wrapMode: Text.WordWrap
        }
    }

    Platform.FileDialog {
        id: playModelDialog
        title: "Выбрать модель"
        folder: controller.modelsFolderUrl
        nameFilters: ["Pickle Files (*.pickle)", "All Files (*)"]
        onAccepted: controller.select_play_model(playModelDialog.fileUrl)
    }

    Dialog {
        id: asciiBoardDialog
        title: "ASCII карта"
        modal: true
        standardButtons: Dialog.Close
        width: root.dialogWidthLg
        height: root.dialogHeightMd
        onOpened: controller.refresh_board_text()

        ColumnLayout {
            anchors.fill: parent
            spacing: root.spacingSm

            TextArea {
                text: controller.boardText
                readOnly: true
                wrapMode: TextEdit.NoWrap
                font.family: "monospace"
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }

        Timer {
            interval: 1000
            repeat: true
            running: asciiBoardDialog.visible
            onTriggered: controller.refresh_board_text()
        }
    }

    Dialog {
        id: armyViewerDialog
        title: "Army Viewer"
        modal: true
        standardButtons: Dialog.Close
        width: root.dialogWidthXl
        height: root.dialogHeightLg

        ColumnLayout {
            anchors.fill: parent
            spacing: root.spacingMd

            RowLayout {
                spacing: root.spacingMd
                Layout.fillWidth: true
                Layout.fillHeight: true

                GroupBox {
                    title: "Доступные юниты (Necrons)"
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: root.spacingSm

                        ListView {
                            id: availableUnitsView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: controller.availableUnitsModel
                            clip: true
                            delegate: Rectangle {
                                width: ListView.view ? ListView.view.width : 0
                                height: unitNameAvailable.implicitHeight + root.spacingSm
                                color: ListView.isCurrentItem ? "#2d89ef" : "transparent"

                                Text {
                                    id: unitNameAvailable
                                    text: model.display
                                    color: ListView.isCurrentItem ? "#ffffff" : "#1f1f1f"
                                    elide: Text.ElideRight
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.left: parent.left
                                    anchors.leftMargin: root.spacingSm
                                }
                            }
                        }

                        RowLayout {
                            spacing: root.spacingSm
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
                        spacing: root.spacingSm

                        ListView {
                            id: playerRosterView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: controller.playerRosterModel
                            clip: true
                            delegate: Rectangle {
                                width: ListView.view ? ListView.view.width : 0
                                height: unitNamePlayer.implicitHeight + root.spacingSm
                                color: ListView.isCurrentItem ? "#2d89ef" : "transparent"

                                Text {
                                    id: unitNamePlayer
                                    text: model.display
                                    color: ListView.isCurrentItem ? "#ffffff" : "#1f1f1f"
                                    elide: Text.ElideRight
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.left: parent.left
                                    anchors.leftMargin: root.spacingSm
                                }
                            }
                        }

                        RowLayout {
                            spacing: root.spacingSm
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
                        spacing: root.spacingSm

                        ListView {
                            id: modelRosterView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            model: controller.modelRosterModel
                            clip: true
                            delegate: Rectangle {
                                width: ListView.view ? ListView.view.width : 0
                                height: unitNameModel.implicitHeight + root.spacingSm
                                color: ListView.isCurrentItem ? "#2d89ef" : "transparent"

                                Text {
                                    id: unitNameModel
                                    text: model.display
                                    color: ListView.isCurrentItem ? "#ffffff" : "#1f1f1f"
                                    elide: Text.ElideRight
                                    anchors.verticalCenter: parent.verticalCenter
                                    anchors.left: parent.left
                                    anchors.leftMargin: root.spacingSm
                                }
                            }
                        }

                        RowLayout {
                            spacing: root.spacingSm
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
    }

    Platform.FileDialog {
        id: metricsFileDialog
        title: "Выберите модель (.pickle)"
        nameFilters: ["Pickle Files (*.pickle)"]
        folder: Platform.StandardPaths.writableLocation(Platform.StandardPaths.DocumentsLocation)
        onAccepted: controller.select_metrics_file(fileUrl)
    }
}
