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
            TabButton { text: "Турнир" }
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
                Item {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: root.spacingMd

                        Text {
                            text: "Турнир self-play"
                            font.pixelSize: Math.round(20 * root.uiScale)
                            font.bold: true
                        }

                        GroupBox {
                            title: "Источник данных"
                            Layout.fillWidth: true

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm

                                    TextField {
                                        id: tournamentPathField
                                        Layout.fillWidth: true
                                        text: controller.tournamentJsonPath
                                        placeholderText: "Путь к tournament_results.json"
                                        onEditingFinished: controller.set_tournament_json_path(text)
                                    }

                                    Button {
                                        text: "Выбрать"
                                        onClicked: tournamentJsonDialog.open()
                                    }

                                    Button {
                                        text: "Обновить"
                                        onClicked: {
                                            controller.set_tournament_json_path(tournamentPathField.text)
                                            controller.reload_tournament_data()
                                        }
                                    }
                                }

                                Label {
                                    text: controller.tournamentStatus
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            spacing: root.spacingMd

                            GroupBox {
                                title: "Сетка (по раундам)"
                                Layout.fillWidth: true
                                Layout.fillHeight: true

                                ScrollView {
                                    anchors.fill: parent
                                    TextArea {
                                        readOnly: true
                                        wrapMode: TextArea.Wrap
                                        text: controller.tournamentRoundsText
                                    }
                                }
                            }

                            GroupBox {
                                title: "Рейтинг"
                                Layout.fillWidth: true
                                Layout.fillHeight: true

                                ListView {
                                    anchors.fill: parent
                                    model: controller.tournamentLeaderboardModel
                                    clip: true
                                    delegate: Label {
                                        width: ListView.view ? ListView.view.width : 0
                                        text: model.display
                                        wrapMode: Text.WordWrap
                                        padding: root.spacingXs
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
                Label {
                    anchors.centerIn: parent
                    text: "Скоро"
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

    Platform.FileDialog {
        id: tournamentJsonDialog
        title: "Выбрать JSON турнира"
        folder: controller.modelsFolderUrl
        nameFilters: ["JSON Files (*.json)", "All Files (*)"]
        onAccepted: {
            var localPath = tournamentJsonDialog.fileUrl
            controller.set_tournament_json_path(localPath)
            tournamentPathField.text = controller.tournamentJsonPath
            controller.reload_tournament_data()
        }
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
