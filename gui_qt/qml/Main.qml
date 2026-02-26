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
    property int factionIconSize: controller.factionIconSize
    property int unitIconSize: controller.unitIconSize
    property string modelFactionName: modelFactionNecrons.checked ? "Necrons" : "-"
    property string playerFactionName: playerFactionNecrons.checked ? "Necrons" : "-"

    font.pixelSize: Math.round(14 * uiScale)

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        TabBar {
            id: mainTabs
            Layout.fillWidth: true

            TabButton { text: "Главная" }
            TabButton { text: "Ростер" }
            TabButton { text: "Метрики модели" }
            TabButton { text: "Игра" }
            TabButton { text: "Настройки" }
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

                    GridLayout {
                        columns: 2
                        columnSpacing: root.spacingLg
                        rowSpacing: root.spacingMd
                        Layout.fillWidth: true

                        ColumnLayout {
                            spacing: root.spacingSm
                            Layout.fillWidth: true

                            GroupBox {
                                title: "Миссия"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: root.spacingSm
                                    anchors.fill: parent

                                    RowLayout {
                                        spacing: root.spacingSm
                                        Label { text: "Выбор миссии" }
                                        ComboBox {
                                            id: missionCombo
                                            Layout.preferredWidth: root.inputWidthMd
                                            model: controller.missionOptions
                                            currentIndex: Math.max(0, controller.missionOptions.indexOf(controller.selectedMission))
                                            onActivated: controller.set_selected_mission_index(currentIndex)
                                        }
                                    }

                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingXs

                                        Label {
                                            text: "Only War"
                                            font.bold: true
                                        }

                                        GridLayout {
                                            columns: 2
                                            columnSpacing: root.spacingMd
                                            rowSpacing: root.spacingXs
                                            Layout.fillWidth: true

                                            Label { text: "Размер стола:"; font.bold: true }
                                            Label { text: "60×40" }

                                            Label { text: "Контрольная точка:"; font.bold: true }
                                            Label { text: "1, центр (30,20)" }

                                            Label { text: "Деплой:"; font.bold: true }
                                            Label { text: "Attacker слева / Defender справа"; wrapMode: Text.Wrap }

                                            Label { text: "Примечание:"; font.bold: true }
                                            Label { text: "roll-off определяет роли"; wrapMode: Text.Wrap }
                                        }
                                    }
                                }
                            }

                            GroupBox {
                                title: "Настройки"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    spacing: root.spacingSm
                                    anchors.fill: parent

                                    RowLayout {
                                        spacing: root.spacingSm
                                        Label { text: "# эпизодов для Тренировки:" }
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

                                }
                            }
                        }

                        ColumnLayout {
                            spacing: root.spacingSm
                            Layout.fillWidth: true

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

                                    CheckBox {
                                        text: "Продолжить обучение (RESUME_CHECKPOINT)"
                                        checked: controller.resumeFromCheckpoint
                                        enabled: !controller.running
                                        Layout.columnSpan: 2
                                        onToggled: controller.set_resume_from_checkpoint(checked)
                                    }

                                    CheckBox {
                                        text: "Не логировать тренировку (speed)"
                                        checked: controller.disableTrainLogging
                                        enabled: !controller.running
                                        Layout.columnSpan: 2
                                        onToggled: controller.set_disable_train_logging(checked)
                                    }

                                    CheckBox {
                                        text: "Очищать логи автоматически"
                                        checked: controller.autoClearLogs
                                        enabled: !controller.running
                                        Layout.columnSpan: 2
                                        onToggled: controller.set_auto_clear_logs(checked)
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

                    Frame {
                        Layout.fillWidth: true
                        padding: root.spacingSm

                        RowLayout {
                            anchors.fill: parent
                            spacing: root.spacingMd

                            Label {
                                text: "Статус ростера:"
                                font.bold: true
                            }

                            Label {
                                text: controller.rosterSummary
                                Layout.fillWidth: true
                                elide: Label.ElideRight
                            }

                            RowLayout {
                                spacing: root.spacingXs

                                Label {
                                    text: "Игрок:"
                                    color: "#666666"
                                }

                                Image {
                                    source: controller.faction_icon_source(root.playerFactionName)
                                    sourceSize.width: root.factionIconSize
                                    sourceSize.height: root.factionIconSize
                                    Layout.preferredWidth: root.factionIconSize
                                    Layout.preferredHeight: root.factionIconSize
                                    visible: source !== ""
                                    fillMode: Image.PreserveAspectFit
                                    smooth: true
                                }

                                Label {
                                    text: root.playerFactionName
                                    color: "#666666"
                                }

                                Label {
                                    text: "•"
                                    color: "#666666"
                                }

                                Label {
                                    text: "Модель:"
                                    color: "#666666"
                                }

                                Image {
                                    source: controller.faction_icon_source(root.modelFactionName)
                                    sourceSize.width: root.factionIconSize
                                    sourceSize.height: root.factionIconSize
                                    Layout.preferredWidth: root.factionIconSize
                                    Layout.preferredHeight: root.factionIconSize
                                    visible: source !== ""
                                    fillMode: Image.PreserveAspectFit
                                    smooth: true
                                }

                                Label {
                                    text: root.modelFactionName
                                    color: "#666666"
                                }
                            }
                        }
                    }

                    GridLayout {
                        columns: 4
                        columnSpacing: root.spacingMd
                        rowSpacing: 0
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        GroupBox {
                            title: "Фракции"
                            Layout.fillWidth: true
                            Layout.fillHeight: false
                            Layout.alignment: Qt.AlignTop
                            Layout.horizontalStretchFactor: 1

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingMd

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm
                                    Label {
                                        text: "Фракция модели:"
                                        Layout.preferredWidth: Math.round(115 * root.uiScale)
                                    }
                                    Rectangle {
                                        Layout.fillWidth: true
                                        radius: Math.round(6 * root.uiScale)
                                        color: "#f6f6f6"
                                        border.color: "#d7d7d7"
                                        border.width: 1
                                        implicitHeight: modelFactionNecrons.implicitHeight + root.spacingSm

                                        RadioButton {
                                            id: modelFactionNecrons
                                            anchors.left: modelFactionIcon.right
                                            anchors.leftMargin: root.spacingXs
                                            anchors.verticalCenter: parent.verticalCenter
                                            text: root.modelFactionName
                                            checked: true
                                            autoExclusive: false
                                            onClicked: checked = true
                                        }

                                        Image {
                                            id: modelFactionIcon
                                            anchors.left: parent.left
                                            anchors.leftMargin: root.spacingSm
                                            anchors.verticalCenter: parent.verticalCenter
                                            source: controller.faction_icon_source(root.modelFactionName)
                                            sourceSize.width: root.factionIconSize
                                            sourceSize.height: root.factionIconSize
                                            width: root.factionIconSize
                                            height: root.factionIconSize
                                            visible: source !== ""
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm
                                    Label {
                                        text: "Фракция игрока:"
                                        Layout.preferredWidth: Math.round(115 * root.uiScale)
                                    }
                                    Rectangle {
                                        Layout.fillWidth: true
                                        radius: Math.round(6 * root.uiScale)
                                        color: "#f6f6f6"
                                        border.color: "#d7d7d7"
                                        border.width: 1
                                        implicitHeight: playerFactionNecrons.implicitHeight + root.spacingSm

                                        RadioButton {
                                            id: playerFactionNecrons
                                            anchors.left: playerFactionIcon.right
                                            anchors.leftMargin: root.spacingXs
                                            anchors.verticalCenter: parent.verticalCenter
                                            text: root.playerFactionName
                                            checked: true
                                            autoExclusive: false
                                            onClicked: checked = true
                                        }

                                        Image {
                                            id: playerFactionIcon
                                            anchors.left: parent.left
                                            anchors.leftMargin: root.spacingSm
                                            anchors.verticalCenter: parent.verticalCenter
                                            source: controller.faction_icon_source(root.playerFactionName)
                                            sourceSize.width: root.factionIconSize
                                            sourceSize.height: root.factionIconSize
                                            width: root.factionIconSize
                                            height: root.factionIconSize
                                            visible: source !== ""
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                        }
                                    }
                                }
                            }
                        }

                        GroupBox {
                            title: ""
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignTop
                            Layout.horizontalStretchFactor: 3

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: root.spacingXs
                                spacing: root.spacingSm

                                RowLayout {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: Math.round(24 * root.uiScale)
                                    spacing: root.spacingXs

                                    Image {
                                        source: controller.faction_icon_source(root.playerFactionName)
                                        sourceSize.width: root.factionIconSize
                                        sourceSize.height: root.factionIconSize
                                        Layout.preferredWidth: root.factionIconSize
                                        Layout.preferredHeight: root.factionIconSize
                                        visible: source !== ""
                                        fillMode: Image.PreserveAspectFit
                                        smooth: true
                                    }

                                    Label {
                                        text: "Доступные юниты (" + root.playerFactionName + ")"
                                        font.bold: true
                                    }
                                }

                                ListView {
                                    id: availableUnitsView
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    model: controller.availableUnitsModel
                                    clip: true
                                    delegate: Rectangle {
                                        width: ListView.view ? ListView.view.width : 0
                                        height: Math.max(unitNameAvailable.implicitHeight, unitIconAvailable.height) + root.spacingSm
                                        color: ListView.isCurrentItem ? "#2d89ef" : "transparent"

                                        Image {
                                            id: unitIconAvailable
                                            source: controller.unit_icon_source(model.display)
                                            width: root.unitIconSize
                                            height: root.unitIconSize
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: parent.left
                                            anchors.leftMargin: root.spacingSm
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                            visible: source !== ""
                                        }

                                        Text {
                                            id: unitNameAvailable
                                            text: model.display
                                            color: ListView.isCurrentItem ? "#ffffff" : "#1f1f1f"
                                            elide: Text.ElideRight
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: unitIconAvailable.visible ? unitIconAvailable.right : parent.left
                                            anchors.leftMargin: root.spacingSm
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: availableUnitsView.currentIndex = index
                                        }
                                    }
                                }

                                RowLayout {
                                    spacing: root.spacingSm
                                    Button {
                                        text: "Добавить в игрока"
                                        highlighted: true
                                        onClicked: controller.add_unit_to_player(availableUnitsView.currentIndex)
                                    }
                                    Button {
                                        text: "Добавить в модель"
                                        flat: true
                                        onClicked: controller.add_unit_to_model(availableUnitsView.currentIndex)
                                    }
                                }
                            }
                        }

                        GroupBox {
                            title: ""
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignTop
                            Layout.horizontalStretchFactor: 2

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: root.spacingXs
                                spacing: root.spacingSm

                                Label {
                                    text: "Ростер игрока"
                                    font.bold: true
                                    Layout.preferredHeight: Math.round(24 * root.uiScale)
                                    verticalAlignment: Text.AlignVCenter
                                }

                                ListView {
                                    id: playerRosterView
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    model: controller.playerRosterModel
                                    clip: true
                                    delegate: Rectangle {
                                        width: ListView.view ? ListView.view.width : 0
                                        height: Math.max(unitNamePlayer.implicitHeight, unitIconPlayer.height) + root.spacingSm
                                        color: ListView.isCurrentItem ? "#2d89ef" : "transparent"

                                        Image {
                                            id: unitIconPlayer
                                            source: controller.unit_icon_source(model.display)
                                            width: root.unitIconSize
                                            height: root.unitIconSize
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: parent.left
                                            anchors.leftMargin: root.spacingSm
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                            visible: source !== ""
                                        }

                                        Text {
                                            id: unitNamePlayer
                                            text: model.display
                                            color: ListView.isCurrentItem ? "#ffffff" : "#1f1f1f"
                                            elide: Text.ElideRight
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: unitIconPlayer.visible ? unitIconPlayer.right : parent.left
                                            anchors.leftMargin: root.spacingSm
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: playerRosterView.currentIndex = index
                                        }
                                    }
                                }

                                RowLayout {
                                    spacing: root.spacingSm
                                    Button {
                                        text: "Удалить"
                                        enabled: playerRosterView.currentIndex >= 0
                                        onClicked: controller.remove_player_unit(playerRosterView.currentIndex)
                                    }
                                    Button {
                                        flat: true
                                        icon.source: ""
                                        icon.width: 0
                                        icon.height: 0
                                        display: AbstractButton.TextOnly
                                        text: "⚠ Очистить"
                                        onClicked: controller.clear_player_roster()
                                    }
                                }
                            }
                        }

                        GroupBox {
                            title: ""
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignTop
                            Layout.horizontalStretchFactor: 2

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: root.spacingXs
                                spacing: root.spacingSm

                                Label {
                                    text: "Ростер модели"
                                    font.bold: true
                                    Layout.preferredHeight: Math.round(24 * root.uiScale)
                                    verticalAlignment: Text.AlignVCenter
                                }

                                ListView {
                                    id: modelRosterView
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    model: controller.modelRosterModel
                                    clip: true
                                    delegate: Rectangle {
                                        width: ListView.view ? ListView.view.width : 0
                                        height: Math.max(unitNameModel.implicitHeight, unitIconModel.height) + root.spacingSm
                                        color: ListView.isCurrentItem ? "#2d89ef" : "transparent"

                                        Image {
                                            id: unitIconModel
                                            source: controller.unit_icon_source(model.display)
                                            width: root.unitIconSize
                                            height: root.unitIconSize
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: parent.left
                                            anchors.leftMargin: root.spacingSm
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                            visible: source !== ""
                                        }

                                        Text {
                                            id: unitNameModel
                                            text: model.display
                                            color: ListView.isCurrentItem ? "#ffffff" : "#1f1f1f"
                                            elide: Text.ElideRight
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: unitIconModel.visible ? unitIconModel.right : parent.left
                                            anchors.leftMargin: root.spacingSm
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: modelRosterView.currentIndex = index
                                        }
                                    }
                                }

                                RowLayout {
                                    spacing: root.spacingSm
                                    Button {
                                        text: "Удалить"
                                        enabled: modelRosterView.currentIndex >= 0
                                        onClicked: controller.remove_model_unit(modelRosterView.currentIndex)
                                    }
                                    Button {
                                        flat: true
                                        icon.source: ""
                                        icon.width: 0
                                        icon.height: 0
                                        display: AbstractButton.TextOnly
                                        text: "⚠ Очистить"
                                        onClicked: controller.clear_model_roster()
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ScrollView {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg
                    clip: true

                    Column {
                        width: Math.max(parent ? parent.width : 0, root.width - 2 * root.spacingLg)
                        spacing: root.spacingMd

                        Text {
                            text: "Model Metrics"
                            font.pixelSize: Math.round(20 * root.uiScale)
                            font.bold: true
                        }

                        RowLayout {
                            spacing: root.spacingMd
                            width: parent.width

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
                            width: parent.width

                            GroupBox {
                                title: "Награда за эпизод"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

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

                                    Label {
                                        text: controller.rewardSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "Потери (loss)"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

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

                                    Label {
                                        text: controller.lossSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "Длина эпизода"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

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

                                    Label {
                                        text: controller.epLenSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "Winrate"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

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

                                    Label {
                                        text: controller.winrateSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "Разница VP"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

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

                                    Label {
                                        text: controller.vpDiffSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "Причины завершения"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

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

                        GroupBox {
                            title: "Состояние модели"
                            width: parent.width

                            ScrollView {
                                width: parent.width
                                height: Math.round(230 * root.uiScale)

                                TextArea {
                                    width: parent.width
                                    text: controller.modelStateText
                                    readOnly: true
                                    wrapMode: Text.WordWrap
                                    selectByMouse: true
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

                ScrollView {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg
                    clip: true

                    contentWidth: availableWidth

                    ColumnLayout {
                        width: Math.max(parent.width, root.dialogWidthLg)
                        spacing: root.spacingMd

                        Item {
                            Layout.fillWidth: true
                            implicitHeight: 1
                        }

                        Label {
                            text: "Настройка параметров тренировки"
                            font.pixelSize: Math.round(20 * root.uiScale)
                            font.bold: true
                            Layout.fillWidth: true
                        }

                        Frame {
                            Layout.fillWidth: true
                            background: Rectangle {
                                radius: Math.round(10 * root.uiScale)
                                color: "#f8f9fb"
                                border.color: "#d9dee8"
                                border.width: 1
                            }

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                Label {
                                    text: "Гиперпараметры (hyperparams.json)"
                                    font.bold: true
                                    Layout.fillWidth: true
                                }

                                Label {
                                    text: "Изменения применяются после сохранения файла."
                                    color: "#666666"
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }

                                GridLayout {
                                    columns: 2
                                    columnSpacing: root.spacingMd
                                    rowSpacing: root.spacingSm
                                    Layout.fillWidth: true

                                    Label { text: "lr" }
                                    SpinBox {
                                        from: 0
                                        to: 1000000
                                        stepSize: 1
                                        editable: true
                                        property real factor: 1000000
                                        value: Math.round(controller.hpLr * factor)
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 6) }
                                        valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                        onValueModified: controller.set_training_hyperparam("lr", (value / factor).toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Скорость обучения модели."
                                    }

                                    Label { text: "tau" }
                                    SpinBox {
                                        from: 0
                                        to: 1000000
                                        stepSize: 1
                                        editable: true
                                        property real factor: 1000000
                                        value: Math.round(controller.hpTau * factor)
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 6) }
                                        valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                        onValueModified: controller.set_training_hyperparam("tau", (value / factor).toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Скорость обновления target-сети."
                                    }

                                    Label { text: "eps_start" }
                                    SpinBox {
                                        from: 0
                                        to: 1000
                                        stepSize: 1
                                        editable: true
                                        property real factor: 1000
                                        value: Math.round(controller.hpEpsStart * factor)
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                        valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                        onValueModified: controller.set_training_hyperparam("eps_start", (value / factor).toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Начальное значение epsilon для exploration."
                                    }

                                    Label { text: "eps_end" }
                                    SpinBox {
                                        from: 0
                                        to: 1000
                                        stepSize: 1
                                        editable: true
                                        property real factor: 1000
                                        value: Math.round(controller.hpEpsEnd * factor)
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                        valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                        onValueModified: controller.set_training_hyperparam("eps_end", (value / factor).toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Минимальное epsilon к концу decay."
                                    }

                                    Label { text: "gamma" }
                                    SpinBox {
                                        from: 0
                                        to: 1000
                                        stepSize: 1
                                        editable: true
                                        property real factor: 1000
                                        value: Math.round(controller.hpGamma * factor)
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                        valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                        onValueModified: controller.set_training_hyperparam("gamma", (value / factor).toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Коэффициент дисконтирования будущей награды."
                                    }

                                    Label { text: "eps_decay" }
                                    SpinBox {
                                        from: 1
                                        to: 10000000
                                        stepSize: 100
                                        editable: true
                                        value: controller.hpEpsDecay
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        onValueModified: controller.set_training_hyperparam("eps_decay", value.toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Длина затухания epsilon."
                                    }

                                    Label { text: "batch_size" }
                                    SpinBox {
                                        from: 1
                                        to: 8192
                                        stepSize: 32
                                        editable: true
                                        value: controller.hpBatchSize
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        onValueModified: controller.set_training_hyperparam("batch_size", value.toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Размер батча при обучении."
                                    }

                                    Label { text: "updates_per_step" }
                                    SpinBox {
                                        from: 1
                                        to: 256
                                        stepSize: 1
                                        editable: true
                                        value: controller.hpUpdatesPerStep
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        onValueModified: controller.set_training_hyperparam("updates_per_step", value.toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Сколько градиентных обновлений делать за шаг."
                                    }

                                    Label { text: "warmup_steps" }
                                    SpinBox {
                                        from: 0
                                        to: 10000000
                                        stepSize: 100
                                        editable: true
                                        value: controller.hpWarmupSteps
                                        Layout.preferredWidth: Math.round(180 * root.uiScale)
                                        onValueModified: controller.set_training_hyperparam("warmup_steps", value.toString())
                                        ToolTip.visible: hovered
                                        ToolTip.text: "Шаги прогрева буфера до полноценного обучения."
                                    }
                                }
                            }
                        }

                        Frame {
                            Layout.fillWidth: true
                            background: Rectangle {
                                radius: Math.round(10 * root.uiScale)
                                color: "#f8f9fb"
                                border.color: "#d9dee8"
                                border.width: 1
                            }

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                Label {
                                    text: "Настройки деплоя"
                                    font.bold: true
                                    Layout.fillWidth: true
                                }

                                Label {
                                    text: "Выберите режим расстановки юнитов перед боем."
                                    wrapMode: Text.WordWrap
                                    color: "#666666"
                                    Layout.fillWidth: true
                                }

                                ComboBox {
                                    id: deploymentModeCombo
                                    Layout.preferredWidth: Math.max(root.inputWidthMd, Math.round(420 * root.uiScale))
                                    model: [
                                        { value: "manual_player", label: "Ручной деплой игрока (через Viewer)" },
                                        { value: "auto", label: "Автоматический деплой" },
                                        { value: "rl_phase", label: "RL-деплой модели + ручной игрок" }
                                    ]
                                    textRole: "label"
                                    valueRole: "value"
                                    currentIndex: {
                                        for (var i = 0; i < model.length; i++) {
                                            if (model[i].value === controller.deploymentMode)
                                                return i
                                        }
                                        return 0
                                    }
                                    onActivated: {
                                        if (currentIndex >= 0 && currentIndex < model.length)
                                            controller.set_deployment_mode(model[currentIndex].value)
                                    }
                                }

                                Label {
                                    text: "Текущий режим: " + controller.deploymentMode
                                    color: "#555555"
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        Frame {
                            Layout.fillWidth: true
                            background: Rectangle {
                                radius: Math.round(10 * root.uiScale)
                                color: "#f8f9fb"
                                border.color: "#d9dee8"
                                border.width: 1
                            }

                            RowLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                Button {
                                    text: "Сохранить"
                                    font.bold: true
                                    highlighted: true
                                    onClicked: controller.save_training_hyperparams()
                                }

                                Button {
                                    text: "Перечитать"
                                    onClicked: controller.reload_training_hyperparams()
                                }

                                Button {
                                    text: "По умолчанию"
                                    onClicked: controller.reset_training_hyperparams()
                                }

                                Item { Layout.fillWidth: true }

                                Label {
                                    text: controller.settingsSaveState
                                    color: controller.settingsDirty ? "#b24a00" : "#2f7d32"
                                    font.bold: true
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }
                        }

                        Item {
                            Layout.fillWidth: true
                            implicitHeight: root.spacingSm
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
                            text: "Оценка модели"
                            font.pixelSize: Math.round(20 * root.uiScale)
                            font.bold: true
                        }

                        GroupBox {
                            title: "Параметры оценки"
                            Layout.fillWidth: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                RowLayout {
                                    spacing: root.spacingSm
                                    Label { text: "Количество игр:" }
                                    TextField {
                                        id: evalGamesField
                                        text: controller.evalGames.toString()
                                        validator: IntValidator { bottom: 1 }
                                        Layout.preferredWidth: root.inputWidthMd
                                        onEditingFinished: {
                                            var value = parseInt(text)
                                            if (!isNaN(value)) {
                                                controller.set_eval_games(value)
                                                text = controller.evalGames.toString()
                                            }
                                        }
                                    }
                                }

                                RowLayout {
                                    spacing: root.spacingSm
                                    Label { text: "Модель:" }
                                    Button {
                                        text: "Выбрать"
                                        enabled: !controller.running
                                        onClicked: evalModelDialog.open()
                                    }
                                    Button {
                                        text: "Последняя"
                                        enabled: !controller.running
                                        onClicked: controller.select_latest_eval_model()
                                    }
                                    Button {
                                        text: "Лучшая"
                                        enabled: !controller.running
                                        onClicked: controller.select_best_eval_model()
                                    }
                                }

                                Label {
                                    text: controller.evalModelLabel
                                    wrapMode: Text.WordWrap
                                }

                                Label {
                                    text: "Запуск: модель против эвристики, без исследования (epsilon=0)."
                                    wrapMode: Text.WordWrap
                                    color: "#555555"
                                }
                            }
                        }

                        GroupBox {
                            title: "Действия"
                            Layout.fillWidth: true

                            RowLayout {
                                anchors.fill: parent
                                spacing: root.spacingMd

                                Button {
                                    text: "Запустить оценку"
                                    enabled: !controller.running
                                    onClicked: controller.start_eval()
                                }

                                Button {
                                    text: "Остановить"
                                    enabled: controller.running
                                    onClicked: controller.stop_process()
                                }
                            }
                        }

                        GroupBox {
                            title: "Подробный результат"
                            Layout.fillWidth: true

                            TextArea {
                                text: controller.evalSummaryText
                                readOnly: true
                                wrapMode: TextArea.Wrap
                                Layout.fillWidth: true
                                Layout.preferredHeight: Math.round(190 * root.uiScale)
                            }
                        }

                        GroupBox {
                            title: "Лог оценки"
                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            ScrollView {
                                anchors.fill: parent

                                TextArea {
                                    id: evalLogArea
                                    readOnly: true
                                    wrapMode: TextArea.Wrap
                                    text: controller.evalLogText
                                    onTextChanged: {
                                        cursorPosition = length
                                    }
                                }
                            }
                        }
                    }
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

    Platform.FileDialog {
        id: evalModelDialog
        title: "Выбрать модель для оценки"
        folder: controller.modelsFolderUrl
        nameFilters: ["Pickle Files (*.pickle)", "All Files (*)"]
        onAccepted: controller.select_eval_model(evalModelDialog.fileUrl)
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
