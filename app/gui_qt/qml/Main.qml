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
    title: "40kAI"

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
    property bool evalShowLog: true
    property int evalDetailTab: 0
    property int radiusMd: Math.round(12 * uiScale)
    property color uiBgBase: "#eff3f9"
    property color uiBgCard: "#f7f9fd"
    property color uiBorder: "#d7deea"
    property color uiTextMain: "#1f2937"
    property color uiTextMuted: "#5b6472"
    property color p1Accent: "#2f6ed8"
    property color p2Accent: "#cf3f3f"
    property int evalDrawerTab: 0
    property int evalSectionTitleSize: Math.round(13 * uiScale)
    property int evalCaptionSize: Math.round(11 * uiScale)
    property int actionButtonHeight: Math.round(30 * uiScale)
    property int actionButtonMinWidth: Math.round(120 * uiScale)

    function extractPercent(text) {
        var raw = text || ""
        var match = raw.match(/([0-9]+(?:[\\.,][0-9]+)?)\s*%/)
        return match ? (match[1] + "%") : "—"
    }

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
                TabButton { text: "Метрики эвристики" }
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

                                    RowLayout {
                                        spacing: root.spacingSm
                                        Label { text: "Модель обучения:" }
                                        ComboBox {
                                            id: trainingAlgoComboMain
                                            Layout.preferredWidth: Math.max(root.inputWidthMd, Math.round(300 * root.uiScale))
                                            model: [
                                                { value: "dqn", label: "DQN" },
                                                { value: "ppo", label: "PPO" },
                                                { value: "alphazero", label: "AlphaZero" },
                                                { value: "gumbel_muzero", label: "Gumbel MuZero" }
                                            ]
                                            textRole: "label"
                                            valueRole: "value"
                                            currentIndex: {
                                                for (var i = 0; i < model.length; i++) {
                                                    if (model[i].value === controller.trainingAlgo)
                                                        return i
                                                }
                                                return 0
                                            }
                                            enabled: !controller.running
                                            onActivated: {
                                                if (currentIndex >= 0 && currentIndex < model.length)
                                                    controller.set_training_algo(model[currentIndex].value)
                                            }
                                        }
                                        Button {
                                            text: "О моделях"
                                            enabled: !controller.running
                                            onClicked: trainingAlgoHelpDialog.open()
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
                                        text: "Детальный трейс действий модели (debug, пишет много в лог)"
                                        checked: controller.actionTrace
                                        enabled: !controller.running
                                        Layout.columnSpan: 2
                                        onToggled: controller.set_action_trace(checked)
                                    }

                                    CheckBox {
                                        text: "Очищать логи автоматически"
                                        checked: controller.autoClearLogs
                                        enabled: !controller.running
                                        Layout.columnSpan: 2
                                        onToggled: controller.set_auto_clear_logs(checked)
                                    }

                                    Label { text: "Сторона обучения" }
                                    ComboBox {
                                        model: controller.learnerSideOptions
                                        Layout.preferredWidth: Math.max(root.inputWidthMd, Math.round(220 * root.uiScale))
                                        currentIndex: Math.max(0, controller.learnerSideOptions.indexOf(controller.learnerSide))
                                        enabled: !controller.running
                                        onActivated: controller.set_learner_side(currentText)
                                    }

                                    Label { text: "Источник оппонента" }
                                    ComboBox {
                                        Layout.preferredWidth: Math.max(root.inputWidthMd, Math.round(220 * root.uiScale))
                                        model: [
                                            { value: "heuristic", label: "Эвристика" },
                                            { value: "latest_snapshot", label: "Последний снапшот" },
                                            { value: "specific_agent", label: "Конкретный агент" }
                                        ]
                                        textRole: "label"
                                        valueRole: "value"
                                        currentIndex: {
                                            for (var i = 0; i < model.length; i++) {
                                                if (model[i].value === controller.opponentSource)
                                                    return i
                                            }
                                            return 0
                                        }
                                        enabled: !controller.running
                                        onActivated: {
                                            if (currentIndex >= 0 && currentIndex < model.length)
                                                controller.set_opponent_source(model[currentIndex].value)
                                        }
                                    }

                                    Label {
                                        text: "Конкретный агент"
                                    }
                                    ComboBox {
                                        Layout.preferredWidth: Math.max(root.inputWidthMd, Math.round(460 * root.uiScale))
                                        model: controller.specificOpponentAgentOptions
                                        currentIndex: controller.specificOpponentAgentOptions.length > 0
                                            ? Math.max(0, controller.specificOpponentAgentOptions.indexOf(controller.selectedSpecificOpponentLabel))
                                            : -1
                                        enabled: !controller.running
                                                 && controller.opponentSource === "specific_agent"
                                                 && controller.specificOpponentAgentOptions.length > 0
                                        opacity: controller.opponentSource === "specific_agent" ? 1.0 : 0.65
                                        onActivated: controller.set_specific_opponent_agent_by_label(currentText)
                                    }

                                    Label {
                                        Layout.columnSpan: 2
                                        text: controller.opponentPreviewText
                                        color: "#555555"
                                        Layout.fillWidth: true
                                        wrapMode: Text.NoWrap
                                        elide: Text.ElideRight
                                        maximumLineCount: 1
                                    }

                                    Button {
                                        text: "Тренировка 8х"
                                        enabled: !controller.running
                                        onClicked: controller.start_train_8x()
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
                                    text: "P1:"
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
                                    text: "P2:"
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
                                        text: "Добавить в P1"
                                        highlighted: true
                                        onClicked: controller.add_unit_to_player(availableUnitsView.currentIndex)
                                    }
                                    Button {
                                        text: "Добавить в P2"
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
                                    text: "Ростер P1"
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
                                    text: "Ростер P2"
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

                        Label {
                            text: "Оценка DET: детерминированные прогоны против эвристики/настроенного оппонента. Не сырые тренировочные партии."
                            width: parent.width
                            wrapMode: Text.WordWrap
                            color: "#666666"
                        }

                        RowLayout {
                            spacing: root.spacingMd
                            width: parent.width

                            Button {
                                text: "Выбрать модель"
                                onClicked: metricsFileDialog.open()
                            }

                            Button {
                                text: "Последняя модель"
                                onClicked: controller.select_latest_metrics()
                            }

                            Label {
                                text: controller.metricsLabel
                                Layout.fillWidth: true
                                elide: Label.ElideRight
                            }
                        }

                        // Верхняя summary-панель
                        RowLayout {
                            spacing: root.spacingMd
                            width: parent.width

                            Rectangle {
                                Layout.fillWidth: true
                                radius: 6
                                color: "#f5f5f5"
                                border.color: "#dddddd"
                                border.width: 1
                                implicitHeight: Math.round(92 * root.uiScale)

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: root.spacingSm
                                    spacing: 4

                                    Text { text: "Модель"; font.bold: true; color: "#333333" }
                                    Text { text: "Алгоритм: " + controller.metricsAlgo; color: "#555555" }
                                    Text { text: "Режим: " + controller.metricsMode; color: "#555555" }
                                    Text { text: "Run ID: " + controller.metricsRunId; color: "#777777"; elide: Text.ElideRight }
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                radius: 6
                                color: "#f5f9ff"
                                border.color: "#d0e3ff"
                                border.width: 1
                                implicitHeight: Math.round(92 * root.uiScale)

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: root.spacingSm
                                    spacing: 4

                                    Text { text: "Последний DET-eval"; font.bold: true; color: "#333333" }
                                    Text { text: "Эпизод: " + controller.detEpisodeLast; color: "#555555" }
                                    Text { text: "Winrate: " + controller.detWinrateLast; color: "#555555" }
                                    Text { text: "Reward: " + controller.detRewardLast + " | Ep_len: " + controller.detEpLenLast; color: "#555555" }
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                radius: 6
                                color: "#fff9f5"
                                border.color: "#ffe0c2"
                                border.width: 1
                                implicitHeight: Math.round(92 * root.uiScale)

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: root.spacingSm
                                    spacing: 4

                                    Text { text: "Оппонент"; font.bold: true; color: "#333333" }
                                    Text { text: "Self-play: " + (controller.selfPlayEnabled ? "включён" : "выключен"); color: "#555555" }
                                    Text { text: "Источник оппонента: " + controller.opponentSource; color: "#555555" }
                                    Text { text: "Алгоритм оппонента: " + controller.opponentAlgo + (controller.opponentId.length > 0 ? (" (id=" + controller.opponentId + ")") : ""); color: "#555555" }
                                }
                            }
                        }

                        GridLayout {
                            columns: 2
                            columnSpacing: root.spacingMd
                            rowSpacing: root.spacingMd
                            width: parent.width

                            GroupBox {
                                title: "DET: награда"
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
                                            text: "Нет графика det_reward."
                                            color: "#777777"
                                            visible: rewardChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Средняя награда за eval-игру (агрегат по батчу DET)."
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
                                title: "DET: loss обучения"
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
                                            text: "Нет графика det_loss."
                                            color: "#777777"
                                            visible: lossChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Loss на момент чекпоинта обучения (не supervised-loss на игре)."
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
                                title: "DET: длина эпизода"
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
                                            text: "Нет графика det_ep_len."
                                            color: "#777777"
                                            visible: epLenChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Среднее число шагов в eval-эпизодах."
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
                                title: "DET: winrate"
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
                                            text: "Нет графика det_winrate."
                                            color: "#777777"
                                            visible: winrateChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Доля побед по eval-играм."
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
                                title: "DET: Avg VP"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

                                        Image {
                                            id: avgVpChart
                                            anchors.fill: parent
                                            source: controller.metricsAvgVpPath
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                        }

                                        Text {
                                            anchors.centerIn: parent
                                            text: "Нет графика det_avg_vp."
                                            color: "#777777"
                                            visible: avgVpChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Средние Victory Points по DET-eval (модель и противник)."
                                        wrapMode: Text.WordWrap
                                    }

                                    Label {
                                        text: controller.avgVpSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "DET: HP diff"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

                                        Image {
                                            id: hpDiffChart
                                            anchors.fill: parent
                                            source: controller.metricsHpDiffPath
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                        }

                                        Text {
                                            anchors.centerIn: parent
                                            text: "Нет графика det_hp_diff."
                                            color: "#777777"
                                            visible: hpDiffChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Разница HP на конец DET-игры (model − enemy)."
                                        wrapMode: Text.WordWrap
                                    }

                                    Label {
                                        text: controller.hpDiffSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "DET: Kill diff"
                                Layout.fillWidth: true

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingXs

                                    Item {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(230 * root.uiScale)

                                        Image {
                                            id: killDiffChart
                                            anchors.fill: parent
                                            source: controller.metricsKillDiffPath
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                        }

                                        Text {
                                            anchors.centerIn: parent
                                            text: "Нет графика det_kill_diff."
                                            color: "#777777"
                                            visible: killDiffChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Kill diff на конец DET-игры (по моделям): model − enemy."
                                        wrapMode: Text.WordWrap
                                    }

                                    Label {
                                        text: controller.killDiffSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }

                            GroupBox {
                                title: "DET: причины завершения"
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
                                            text: "Нет графика det_endreasons."
                                            color: "#777777"
                                            visible: endReasonChart.status !== Image.Ready
                                        }
                                    }

                                    Label {
                                        text: "Доли wipeout / turn limit по eval-играм."
                                        wrapMode: Text.WordWrap
                                    }

                                    Label {
                                        text: controller.endReasonSummary
                                        wrapMode: Text.WordWrap
                                        color: "#666666"
                                    }
                                }
                            }
                        }

                        // Model Info убрали: эта информация уже есть в верхней панели и карточке "Оппонент".
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
                            text: "Метрики эвристики"
                            font.pixelSize: Math.round(20 * root.uiScale)
                            font.bold: true
                        }

                        Label {
                            text: "Сводка по ENEMY heuristic: роли, режимы, риски, cover, EV и стабильность."
                            wrapMode: Text.WordWrap
                            color: "#666666"
                        }

                        GroupBox {
                            title: "Сводные показатели"
                            width: parent.width

                            ScrollView {
                                width: parent.width
                                height: Math.round(420 * root.uiScale)
                                TextArea {
                                    width: parent.width
                                    text: controller.heuristicMetricsText
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

                                Label {
                                    text: controller.playModelAlgoLabel
                                    wrapMode: Text.WordWrap
                                    color: "#555555"
                                }

                                RowLayout {
                                    visible: controller.playInferenceModeVisible
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm

                                    Label {
                                        text: controller.playInferenceModeLabel
                                        font.bold: true
                                    }

                                    ComboBox {
                                        Layout.preferredWidth: Math.round(190 * root.uiScale)
                                        model: controller.playInferenceModeOptions
                                        textRole: "label"
                                        enabled: !controller.running
                                        currentIndex: {
                                            for (var i = 0; i < model.length; i++) {
                                                if (model[i].value === controller.playInferenceMode) return i
                                            }
                                            return 0
                                        }
                                        onActivated: {
                                            if (model && model[currentIndex]) {
                                                controller.set_play_inference_mode(model[currentIndex].value)
                                            }
                                        }
                                    }

                                    Label {
                                        visible: controller.playInferenceTemperatureVisible
                                        text: "Темп.:"
                                        color: "#2f3b52"
                                    }

                                    TextField {
                                        visible: controller.playInferenceTemperatureVisible
                                        Layout.preferredWidth: Math.round(80 * root.uiScale)
                                        enabled: !controller.running
                                        text: controller.playInferenceTemperature
                                        placeholderText: "0.10"
                                        onEditingFinished: controller.set_play_inference_temperature(text)
                                    }
                                }

                                Rectangle {
                                    visible: controller.playInferenceModeVisible
                                    Layout.fillWidth: true
                                    color: "#f3f4f6"
                                    border.color: "#d1d5db"
                                    border.width: 1
                                    radius: Math.round(8 * root.uiScale)
                                    implicitHeight: playInferenceHelpText.implicitHeight + Math.round(12 * root.uiScale)
                                    Text {
                                        id: playInferenceHelpText
                                        anchors.fill: parent
                                        anchors.margins: Math.round(6 * root.uiScale)
                                        wrapMode: Text.WordWrap
                                        color: "#374151"
                                        text:
                                            "Greedy — ИИ сразу берет лучший ход. Это самый быстрый режим.\n" +
                                            "MCTS/Search — ИИ сначала просчитывает варианты вперед. Обычно сильнее, но медленнее.\n" +
                                            "Температура работает только в MCTS/Search:\n" +
                                            "• меньше (0.03–0.08) — более стабильно;\n" +
                                            "• больше (0.10–0.15) — больше разнообразия.\n" +
                                            "Старт: AZ 0.06, GMZ 0.10.\n" +
                                            "PPO и DQN работают без поиска дерева, поэтому MCTS/Search и температура к ним не применяются.\n" +
                                            "Эвристика — скриптовый бот, не использует нейросеть и температуру."
                                    }
                                }

                                Label {
                                    text: controller.playModelCheckpointLabel
                                    wrapMode: Text.WordWrap
                                    color: "#555555"
                                }

                                Label {
                                    text: "Кто за кого:"
                                    font.bold: true
                                    wrapMode: Text.WordWrap
                                }

                                Label {
                                    text: controller.playViewerPlayerRoleLabel
                                    wrapMode: Text.WordWrap
                                }

                                Label {
                                    text: controller.playViewerModelRoleLabel
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

                        Rectangle {
                            Layout.fillWidth: true
                            radius: Math.round(10 * root.uiScale)
                            color: "#f8f9fb"
                            border.color: "#d9dee8"
                            border.width: 1
                            implicitHeight: hyperparamsCardLayout.implicitHeight + root.spacingMd * 2

                            ColumnLayout {
                                id: hyperparamsCardLayout
                                anchors.fill: parent
                                anchors.margins: root.spacingMd
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

                                RowLayout {
                                    spacing: root.spacingLg
                                    Layout.fillWidth: true

                                    ColumnLayout {
                                        spacing: root.spacingXs
                                        Layout.fillWidth: true
                                        Layout.minimumWidth: Math.round(280 * root.uiScale)

                                        Label {
                                            text: "DQN"
                                            font.bold: true
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

                                    ColumnLayout {
                                        spacing: root.spacingXs
                                        Layout.fillWidth: true
                                        Layout.minimumWidth: Math.round(280 * root.uiScale)

                                        Label {
                                            text: "PPO"
                                            font.bold: true
                                            Layout.fillWidth: true
                                        }

                                        GridLayout {
                                            columns: 2
                                            columnSpacing: root.spacingMd
                                            rowSpacing: root.spacingSm
                                            Layout.fillWidth: true

                                            Label { text: "learning_rate" }
                                            SpinBox {
                                                from: 0
                                                to: 1000000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000000
                                                value: Math.round(controller.hpPpoLearningRate * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 6) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("learning_rate", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Скорость обучения PPO (как в train.py: PPO_LR)."
                                            }

                                            Label { text: "gamma" }
                                            SpinBox {
                                                from: 0
                                                to: 1000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000
                                                value: Math.round(controller.hpPpoGamma * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("gamma", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Дисконтирование для PPO (отдельно от DQN gamma в секции ppo)."
                                            }

                                            Label { text: "gae_lambda" }
                                            SpinBox {
                                                from: 0
                                                to: 1000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000
                                                value: Math.round(controller.hpPpoGaeLambda * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("gae_lambda", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "GAE λ для advantage."
                                            }

                                            Label { text: "clip_ratio" }
                                            SpinBox {
                                                from: 0
                                                to: 1000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000
                                                value: Math.round(controller.hpPpoClipRatio * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("clip_ratio", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "PPO clip (ε)."
                                            }

                                            Label { text: "value_coef" }
                                            SpinBox {
                                                from: 0
                                                to: 100000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000
                                                value: Math.round(controller.hpPpoValueCoef * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("value_coef", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Вес value loss."
                                            }

                                            Label { text: "entropy_coef" }
                                            SpinBox {
                                                from: 0
                                                to: 100000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000
                                                value: Math.round(controller.hpPpoEntropyCoef * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("entropy_coef", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Вес энтропийного бонуса."
                                            }

                                            Label { text: "rollout_steps" }
                                            SpinBox {
                                                from: 1
                                                to: 1000000
                                                stepSize: 64
                                                editable: true
                                                value: controller.hpPpoRolloutSteps
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_ppo_hyperparam("rollout_steps", value.toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Длина rollout перед обновлением."
                                            }

                                            Label { text: "update_epochs" }
                                            SpinBox {
                                                from: 1
                                                to: 256
                                                stepSize: 1
                                                editable: true
                                                value: controller.hpPpoUpdateEpochs
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_ppo_hyperparam("update_epochs", value.toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Эпохи обновления на одном батче rollout."
                                            }

                                            Label { text: "minibatch_size" }
                                            SpinBox {
                                                from: 1
                                                to: 8192
                                                stepSize: 32
                                                editable: true
                                                value: controller.hpPpoMinibatchSize
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_ppo_hyperparam("minibatch_size", value.toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Размер минибатча внутри эпохи."
                                            }

                                            Label { text: "max_grad_norm" }
                                            SpinBox {
                                                from: 0
                                                to: 100000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000
                                                value: Math.round(controller.hpPpoMaxGradNorm * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("max_grad_norm", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Клип градиента (norm)."
                                            }

                                            Label { text: "target_kl" }
                                            SpinBox {
                                                from: 0
                                                to: 100000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000
                                                value: Math.round(controller.hpPpoTargetKl * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 3) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_ppo_hyperparam("target_kl", (value / factor).toString())
                                                ToolTip.visible: hovered
                                                ToolTip.text: "Порог ранней остановки по приближённому KL."
                                            }
                                        }
                                    }

                                    ColumnLayout {
                                        spacing: root.spacingXs
                                        Layout.fillWidth: true
                                        Layout.minimumWidth: Math.round(280 * root.uiScale)

                                        Label {
                                            text: "Gumbel MuZero"
                                            font.bold: true
                                            Layout.fillWidth: true
                                        }

                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingSm
                                            Button { text: "Fast"; onClicked: controller.apply_gmz_profile("fast") }
                                            Button { text: "Balanced"; onClicked: controller.apply_gmz_profile("balanced") }
                                            Button { text: "Heavy"; onClicked: controller.apply_gmz_profile("heavy") }
                                        }

                                        Label {
                                            text: "Текущий пресет: " + controller.hpGmzPresetLabel
                                            color: palette.mid
                                            Layout.fillWidth: true
                                        }

                                        GridLayout {
                                            columns: 2
                                            columnSpacing: root.spacingMd
                                            rowSpacing: root.spacingSm
                                            Layout.fillWidth: true

                                            Label { text: "learning_rate" }
                                            SpinBox {
                                                from: 0
                                                to: 1000000
                                                stepSize: 1
                                                editable: true
                                                property real factor: 1000000
                                                value: Math.round(controller.hpGmzLearningRate * factor)
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 6) }
                                                valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                                                onValueModified: controller.set_gmz_hyperparam("learning_rate", (value / factor).toString())
                                            }

                                            Label { text: "batch_size" }
                                            SpinBox {
                                                from: 1
                                                to: 8192
                                                stepSize: 32
                                                editable: true
                                                value: controller.hpGmzBatchSize
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_gmz_hyperparam("batch_size", value.toString())
                                            }

                                            Label { text: "num_simulations" }
                                            SpinBox {
                                                from: 1
                                                to: 512
                                                stepSize: 1
                                                editable: true
                                                value: controller.hpGmzNumSimulations
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_gmz_hyperparam("num_simulations", value.toString())
                                            }

                                            Label { text: "root_top_k" }
                                            SpinBox {
                                                from: 1
                                                to: 256
                                                stepSize: 1
                                                editable: true
                                                value: controller.hpGmzRootTopK
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_gmz_hyperparam("root_top_k", value.toString())
                                            }

                                            Label { text: "unroll_steps" }
                                            SpinBox {
                                                from: 1
                                                to: 64
                                                stepSize: 1
                                                editable: true
                                                value: controller.hpGmzUnrollSteps
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_gmz_hyperparam("unroll_steps", value.toString())
                                            }

                                            Label { text: "num_actors" }
                                            SpinBox {
                                                from: 1
                                                to: 64
                                                stepSize: 1
                                                editable: true
                                                value: controller.hpGmzNumActors
                                                Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                onValueModified: controller.set_gmz_hyperparam("num_actors", value.toString())
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            radius: Math.round(10 * root.uiScale)
                            color: "#f8f9fb"
                            border.color: "#d9dee8"
                            border.width: 1
                            implicitHeight: deploymentCardLayout.implicitHeight + root.spacingMd * 2

                            ColumnLayout {
                                id: deploymentCardLayout
                                anchors.fill: parent
                                anchors.margins: root.spacingMd
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

                        Rectangle {
                            Layout.fillWidth: true
                            radius: Math.round(10 * root.uiScale)
                            color: "#f8f9fb"
                            border.color: "#d9dee8"
                            border.width: 1
                            implicitHeight: actionRowLayout.implicitHeight + root.spacingMd * 2

                            RowLayout {
                                id: actionRowLayout
                                anchors.fill: parent
                                anchors.margins: root.spacingMd
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
                ScrollView {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg
                    clip: true

                    ColumnLayout {
                        width: Math.max(parent ? parent.width : 0, root.width - 2 * root.spacingLg)
                        spacing: root.spacingLg

                        Rectangle {
                            Layout.fillWidth: true
                            color: root.uiBgBase
                            radius: root.radiusMd
                            border.width: 1
                            border.color: root.uiBorder
                            implicitHeight: evalHeaderLayout.implicitHeight + root.spacingMd * 2

                            RowLayout {
                                id: evalHeaderLayout
                                anchors.fill: parent
                                anchors.margins: root.spacingMd
                                spacing: root.spacingMd

                                ColumnLayout {
                                    spacing: Math.round(4 * root.uiScale)
                                    Layout.fillWidth: true

                                    Text {
                                        text: "Оценка: P1 vs P2"
                                        font.pixelSize: Math.round(22 * root.uiScale)
                                        font.bold: true
                                        color: root.uiTextMain
                                    }
                                    Text {
                                        text: controller.evalMiniSummary
                                        color: root.uiTextMuted
                                    }
                                }

                                Rectangle {
                                    radius: Math.round(10 * root.uiScale)
                                    color: controller.running ? "#e8f1ff" : "#edf2f7"
                                    border.width: 1
                                    border.color: controller.running ? "#b9cff7" : "#d1d9e6"
                                    implicitWidth: evalRunStatus.implicitWidth + Math.round(22 * root.uiScale)
                                    implicitHeight: evalRunStatus.implicitHeight + Math.round(10 * root.uiScale)
                                    Text {
                                        id: evalRunStatus
                                        anchors.centerIn: parent
                                        text: controller.running ? "RUNNING" : "IDLE"
                                        font.bold: true
                                        color: controller.running ? "#2453a4" : "#4b5563"
                                        font.pixelSize: Math.round(11 * root.uiScale)
                                    }
                                }

                                RowLayout {
                                    spacing: root.spacingXs
                                    Label {
                                        text: "Игр:"
                                        font.bold: true
                                    }
                                    TextField {
                                        id: evalGamesField
                                        text: controller.evalGames.toString()
                                        validator: IntValidator { bottom: 1 }
                                        Layout.preferredWidth: Math.round(96 * root.uiScale)
                                        enabled: !controller.running
                                        onEditingFinished: {
                                            var value = parseInt(text)
                                            if (!isNaN(value)) {
                                                controller.set_eval_games(value)
                                                text = controller.evalGames.toString()
                                            } else {
                                                text = controller.evalGames.toString()
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        GroupBox {
                            title: "Сетап матча"
                            Layout.fillWidth: true
                            font.pixelSize: root.evalSectionTitleSize

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingMd

                                Rectangle {
                                    Layout.fillWidth: true
                                    color: "#f7f9fd"
                                    radius: Math.round(10 * root.uiScale)
                                    border.width: 1
                                    border.color: "#d7deea"
                                    implicitHeight: matchupHeadLayout.implicitHeight + root.spacingMd * 2

                                    ColumnLayout {
                                        id: matchupHeadLayout
                                        anchors.fill: parent
                                        anchors.margins: root.spacingMd
                                        spacing: Math.round(4 * root.uiScale)

                                        Text {
                                            text: controller.evalDuelTitle
                                            font.bold: true
                                            font.pixelSize: Math.round(22 * root.uiScale)
                                            color: "#1f2937"
                                        }
                                        Text {
                                            text: controller.evalDuelSubtitle
                                            font.pixelSize: Math.round(13 * root.uiScale)
                                            color: "#5b6472"
                                        }
                                    }
                                }

                                Text {
                                    text: "deterministic, epsilon=0"
                                    color: "#5b6472"
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingMd

                                    Rectangle {
                                        Layout.fillWidth: true
                                        color: "#eef4ff"
                                        border.color: "#2f6ed8"
                                        border.width: 1
                                        radius: Math.round(10 * root.uiScale)
                                        implicitHeight: Math.max(p1CardLayout.implicitHeight, p2CardLayout.implicitHeight) + root.spacingSm * 2

                                        ColumnLayout {
                                            id: p1CardLayout
                                            anchors.fill: parent
                                            anchors.margins: root.spacingSm
                                            spacing: root.spacingXs

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                Rectangle {
                                                    width: Math.round(30 * root.uiScale)
                                                    height: width
                                                    radius: width / 2
                                                    color: "#2f6ed8"
                                                    Text {
                                                        anchors.centerIn: parent
                                                        text: controller.evalP1IconText
                                                        color: "white"
                                                        font.bold: true
                                                    }
                                                }
                                                Text {
                                                    text: "P1"
                                                    color: "#2f6ed8"
                                                    font.bold: true
                                                    font.pixelSize: Math.round(16 * root.uiScale)
                                                }
                                                Item { Layout.fillWidth: true }
                                            }

                                            ComboBox {
                                                Layout.fillWidth: true
                                                enabled: !controller.running
                                                model: [
                                                    { value: "agent", label: "Агент" },
                                                    { value: "heuristic", label: "Эвристика" }
                                                ]
                                                textRole: "label"
                                                currentIndex: {
                                                    for (var i = 0; i < model.length; i++) {
                                                        if (model[i].value === controller.evalP1Policy) return i
                                                    }
                                                    return 0
                                                }
                                                onActivated: controller.set_eval_p1_policy(model[currentIndex].value)
                                            }
                                            ComboBox {
                                                Layout.fillWidth: true
                                                enabled: !controller.running && controller.evalP1Policy === "agent"
                                                opacity: controller.evalP1Policy === "agent" ? 1.0 : 0.55
                                                model: controller.evalP1AgentOptions
                                                currentIndex: controller.evalP1AgentOptions.length > 0
                                                    ? Math.max(0, controller.evalP1AgentOptions.indexOf(controller.evalP1SelectedAgentLabel))
                                                    : -1
                                                onActivated: controller.set_eval_p1_agent_by_label(currentText)
                                            }

                                            Text {
                                                text: controller.evalP1DisplayName
                                                wrapMode: Text.WordWrap
                                                color: "#1f2937"
                                                font.bold: true
                                            }

                                            Flow {
                                                Layout.fillWidth: true
                                                spacing: Math.round(6 * root.uiScale)
                                                Repeater {
                                                    model: controller.evalP1Badges
                                                    delegate: Rectangle {
                                                        radius: Math.round(8 * root.uiScale)
                                                        color: "#dce8ff"
                                                        border.width: 1
                                                        border.color: "#b8cdf6"
                                                        implicitWidth: badgeP1Text.implicitWidth + Math.round(12 * root.uiScale)
                                                        implicitHeight: badgeP1Text.implicitHeight + Math.round(6 * root.uiScale)
                                                        Text {
                                                            id: badgeP1Text
                                                            anchors.centerIn: parent
                                                            text: modelData
                                                            color: "#214f9f"
                                                            font.pixelSize: Math.round(11 * root.uiScale)
                                                            font.bold: true
                                                        }
                                                    }
                                                }
                                            }

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                Button {
                                                    text: "Копировать ID"
                                                    flat: true
                                                    enabled: controller.evalP1FullAgentId.length > 0
                                                    onClicked: controller.copy_eval_agent_id("P1")
                                                    ToolTip.visible: hovered && controller.evalP1FullAgentId.length > 0
                                                    ToolTip.text: controller.evalP1FullAgentId
                                                }
                                                Label {
                                                    text: "Режим:"
                                                    font.bold: true
                                                    color: "#2f3b52"
                                                    opacity: controller.evalP1InferenceModeVisible ? 1.0 : 0.55
                                                }
                                                ComboBox {
                                                    Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP1InferenceModeVisible
                                                    opacity: controller.evalP1InferenceModeVisible ? 1.0 : 0.55
                                                    model: controller.evalP1InferenceModeVisible
                                                        ? controller.evalP1InferenceModeOptions
                                                        : [{ value: "greedy", label: "Greedy" }]
                                                    textRole: "label"
                                                    currentIndex: {
                                                        for (var i = 0; i < model.length; i++) {
                                                            if (model[i].value === controller.evalP1InferenceMode) return i
                                                        }
                                                        return 0
                                                    }
                                                    onActivated: {
                                                        if (controller.evalP1InferenceModeVisible && model && model[currentIndex]) {
                                                            controller.set_eval_p1_inference_mode(model[currentIndex].value)
                                                        }
                                                    }
                                                }
                                                Label {
                                                    text: "Темп.:"
                                                    color: "#2f3b52"
                                                    opacity: controller.evalP1InferenceTemperatureVisible ? 1.0 : 0.55
                                                }
                                                TextField {
                                                    Layout.preferredWidth: Math.round(80 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP1InferenceTemperatureVisible
                                                    opacity: controller.evalP1InferenceTemperatureVisible ? 1.0 : 0.55
                                                    text: controller.evalP1InferenceTemperature
                                                    placeholderText: "0.10"
                                                    onEditingFinished: {
                                                        if (controller.evalP1InferenceTemperatureVisible) {
                                                            controller.set_eval_p1_inference_temperature(text)
                                                        }
                                                    }
                                                }
                                                Button {
                                                    text: "i"
                                                    flat: true
                                                    font.bold: true
                                                    ToolTip.visible: hovered
                                                    ToolTip.text:
                                                        "Greedy — ИИ сразу берет лучший ход. Это самый быстрый режим.\n" +
                                                        "MCTS/Search — ИИ сначала просчитывает варианты вперед. Обычно сильнее, но медленнее.\n" +
                                                        "Температура работает только в MCTS/Search:\n" +
                                                        "• меньше (0.03–0.08) — более стабильно;\n" +
                                                        "• больше (0.10–0.15) — больше разнообразия.\n" +
                                                        "Старт: AZ 0.06, GMZ 0.10.\n" +
                                                        "PPO и DQN работают без поиска дерева, поэтому MCTS/Search и температура к ним не применяются.\n" +
                                                        "Эвристика — скриптовый бот, не использует нейросеть и температуру."
                                                }
                                                Item { Layout.fillWidth: true }
                                                Button {
                                                    text: "ⓘ"
                                                    flat: true
                                                    enabled: controller.evalP1FullAgentId.length > 0
                                                    ToolTip.visible: hovered && controller.evalP1FullAgentId.length > 0
                                                    ToolTip.text: controller.evalP1FullAgentId
                                                }
                                            }
                                        }
                                    }

                                    Rectangle {
                                        Layout.fillWidth: true
                                        color: "#fff1f1"
                                        border.color: "#cf3f3f"
                                        border.width: 1
                                        radius: Math.round(10 * root.uiScale)
                                        implicitHeight: Math.max(p1CardLayout.implicitHeight, p2CardLayout.implicitHeight) + root.spacingSm * 2

                                        ColumnLayout {
                                            id: p2CardLayout
                                            anchors.fill: parent
                                            anchors.margins: root.spacingSm
                                            spacing: root.spacingXs

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                Rectangle {
                                                    width: Math.round(30 * root.uiScale)
                                                    height: width
                                                    radius: width / 2
                                                    color: "#cf3f3f"
                                                    Text {
                                                        anchors.centerIn: parent
                                                        text: controller.evalP2IconText
                                                        color: "white"
                                                        font.bold: true
                                                    }
                                                }
                                                Text {
                                                    text: "P2"
                                                    color: "#cf3f3f"
                                                    font.bold: true
                                                    font.pixelSize: Math.round(16 * root.uiScale)
                                                }
                                                Item { Layout.fillWidth: true }
                                            }

                                            ComboBox {
                                                Layout.fillWidth: true
                                                enabled: !controller.running
                                                model: [
                                                    { value: "agent", label: "Агент" },
                                                    { value: "heuristic", label: "Эвристика" }
                                                ]
                                                textRole: "label"
                                                currentIndex: {
                                                    for (var i = 0; i < model.length; i++) {
                                                        if (model[i].value === controller.evalP2Policy) return i
                                                    }
                                                    return 0
                                                }
                                                onActivated: controller.set_eval_p2_policy(model[currentIndex].value)
                                            }
                                            ComboBox {
                                                Layout.fillWidth: true
                                                enabled: !controller.running && controller.evalP2Policy === "agent"
                                                opacity: controller.evalP2Policy === "agent" ? 1.0 : 0.55
                                                model: controller.evalP2AgentOptions
                                                currentIndex: controller.evalP2AgentOptions.length > 0
                                                    ? Math.max(0, controller.evalP2AgentOptions.indexOf(controller.evalP2SelectedAgentLabel))
                                                    : -1
                                                onActivated: controller.set_eval_p2_agent_by_label(currentText)
                                            }

                                            Text {
                                                text: controller.evalP2DisplayName
                                                wrapMode: Text.WordWrap
                                                color: "#1f2937"
                                                font.bold: true
                                            }

                                            Flow {
                                                Layout.fillWidth: true
                                                spacing: Math.round(6 * root.uiScale)
                                                Repeater {
                                                    model: controller.evalP2Badges
                                                    delegate: Rectangle {
                                                        radius: Math.round(8 * root.uiScale)
                                                        color: "#ffe0e0"
                                                        border.width: 1
                                                        border.color: "#f0b6b6"
                                                        implicitWidth: badgeP2Text.implicitWidth + Math.round(12 * root.uiScale)
                                                        implicitHeight: badgeP2Text.implicitHeight + Math.round(6 * root.uiScale)
                                                        Text {
                                                            id: badgeP2Text
                                                            anchors.centerIn: parent
                                                            text: modelData
                                                            color: "#993434"
                                                            font.pixelSize: Math.round(11 * root.uiScale)
                                                            font.bold: true
                                                        }
                                                    }
                                                }
                                            }

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                Button {
                                                    text: "Копировать ID"
                                                    flat: true
                                                    enabled: controller.evalP2FullAgentId.length > 0
                                                    onClicked: controller.copy_eval_agent_id("P2")
                                                    ToolTip.visible: hovered && controller.evalP2FullAgentId.length > 0
                                                    ToolTip.text: controller.evalP2FullAgentId
                                                }
                                                Label {
                                                    text: "Режим:"
                                                    font.bold: true
                                                    color: "#2f3b52"
                                                    opacity: controller.evalP2InferenceModeVisible ? 1.0 : 0.55
                                                }
                                                ComboBox {
                                                    Layout.preferredWidth: Math.round(180 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP2InferenceModeVisible
                                                    opacity: controller.evalP2InferenceModeVisible ? 1.0 : 0.55
                                                    model: controller.evalP2InferenceModeVisible
                                                        ? controller.evalP2InferenceModeOptions
                                                        : [{ value: "greedy", label: "Greedy" }]
                                                    textRole: "label"
                                                    currentIndex: {
                                                        for (var i = 0; i < model.length; i++) {
                                                            if (model[i].value === controller.evalP2InferenceMode) return i
                                                        }
                                                        return 0
                                                    }
                                                    onActivated: {
                                                        if (controller.evalP2InferenceModeVisible && model && model[currentIndex]) {
                                                            controller.set_eval_p2_inference_mode(model[currentIndex].value)
                                                        }
                                                    }
                                                }
                                                Label {
                                                    text: "Темп.:"
                                                    color: "#2f3b52"
                                                    opacity: controller.evalP2InferenceTemperatureVisible ? 1.0 : 0.55
                                                }
                                                TextField {
                                                    Layout.preferredWidth: Math.round(80 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP2InferenceTemperatureVisible
                                                    opacity: controller.evalP2InferenceTemperatureVisible ? 1.0 : 0.55
                                                    text: controller.evalP2InferenceTemperature
                                                    placeholderText: "0.10"
                                                    onEditingFinished: {
                                                        if (controller.evalP2InferenceTemperatureVisible) {
                                                            controller.set_eval_p2_inference_temperature(text)
                                                        }
                                                    }
                                                }
                                                Button {
                                                    text: "i"
                                                    flat: true
                                                    font.bold: true
                                                    ToolTip.visible: hovered
                                                    ToolTip.text:
                                                        "Greedy — ИИ сразу берет лучший ход. Это самый быстрый режим.\n" +
                                                        "MCTS/Search — ИИ сначала просчитывает варианты вперед. Обычно сильнее, но медленнее.\n" +
                                                        "Температура работает только в MCTS/Search:\n" +
                                                        "• меньше (0.03–0.08) — более стабильно;\n" +
                                                        "• больше (0.10–0.15) — больше разнообразия.\n" +
                                                        "Старт: AZ 0.06, GMZ 0.10.\n" +
                                                        "PPO и DQN работают без поиска дерева, поэтому MCTS/Search и температура к ним не применяются.\n" +
                                                        "Эвристика — скриптовый бот, не использует нейросеть и температуру."
                                                }
                                                Item { Layout.fillWidth: true }
                                                Button {
                                                    text: "ⓘ"
                                                    flat: true
                                                    enabled: controller.evalP2FullAgentId.length > 0
                                                    ToolTip.visible: hovered && controller.evalP2FullAgentId.length > 0
                                                    ToolTip.text: controller.evalP2FullAgentId
                                                }
                                            }
                                        }
                                    }
                                }

                                Rectangle {
                                    Layout.fillWidth: true
                                    color: root.uiBgCard
                                    border.color: root.uiBorder
                                    border.width: 1
                                    radius: root.radiusMd
                                    implicitHeight: centerDuelLayout.implicitHeight + root.spacingMd * 2
                                    Rectangle {
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.top: parent.top
                                        anchors.bottom: parent.bottom
                                        anchors.topMargin: Math.round(2 * root.uiScale)
                                        radius: parent.radius
                                        color: "#12000000"
                                        z: -1
                                    }

                                    ColumnLayout {
                                        id: centerDuelLayout
                                        anchors.fill: parent
                                        anchors.margins: root.spacingMd
                                        spacing: Math.round(6 * root.uiScale)

                                        Text {
                                            text: "LIVE DUEL"
                                            color: root.uiTextMuted
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                            horizontalAlignment: Text.AlignHCenter
                                            Layout.fillWidth: true
                                        }

                                        Text {
                                            Layout.fillWidth: true
                                            horizontalAlignment: Text.AlignHCenter
                                            text: controller.evalLiveGamesDone > 0
                                                ? (controller.evalLiveLeaderSide === "P1"
                                                    ? "Преимущество: P1 +" + Math.abs(Math.round((controller.evalLiveP1Winrate - controller.evalLiveP2Winrate) * 100)) + "%"
                                                    : controller.evalLiveLeaderSide === "P2"
                                                        ? "Преимущество: P2 +" + Math.abs(Math.round((controller.evalLiveP2Winrate - controller.evalLiveP1Winrate) * 100)) + "%"
                                                        : "Баланс сил: паритет")
                                                : "Ожидание первой игры"
                                            color: controller.evalLiveLeaderSide === "P1"
                                                ? root.p1Accent
                                                : controller.evalLiveLeaderSide === "P2"
                                                    ? root.p2Accent
                                                    : root.uiTextMain
                                            font.bold: true
                                            font.pixelSize: Math.round(12 * root.uiScale)
                                        }

                                        Rectangle {
                                            id: snapshotTrack
                                            Layout.fillWidth: true
                                            Layout.preferredHeight: Math.round(22 * root.uiScale)
                                            radius: height / 2
                                            color: "#e9eef7"
                                            border.color: root.uiBorder
                                            border.width: 1
                                            clip: true

                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.top: parent.top
                                                anchors.bottom: parent.bottom
                                                width: parent.width * Math.max(0.0, Math.min(1.0, controller.evalLiveP1Winrate))
                                                color: root.p1Accent
                                                radius: parent.radius
                                                Behavior on width {
                                                    NumberAnimation { duration: 260; easing.type: Easing.InOutCubic }
                                                }
                                            }
                                            Rectangle {
                                                anchors.right: parent.right
                                                anchors.top: parent.top
                                                anchors.bottom: parent.bottom
                                                width: parent.width * Math.max(0.0, Math.min(1.0, controller.evalLiveP2Winrate))
                                                color: root.p2Accent
                                                radius: parent.radius
                                                Behavior on width {
                                                    NumberAnimation { duration: 260; easing.type: Easing.InOutCubic }
                                                }
                                            }
                                        }

                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingSm
                                            Text {
                                                text: "P1 " + Math.round(controller.evalLiveP1Winrate * 100) + "%"
                                                color: root.p1Accent
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                            }
                                            Item { Layout.fillWidth: true }
                                            Text {
                                                text: "P2 " + Math.round(controller.evalLiveP2Winrate * 100) + "%"
                                                color: root.p2Accent
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                            }
                                        }

                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingSm
                                            Text {
                                                text: "Счет: P1 " + controller.evalLiveP1Wins + " • P2 " + controller.evalLiveP2Wins + " • Ничьи " + controller.evalLiveDraws
                                                color: root.uiTextMuted
                                                font.pixelSize: root.evalCaptionSize
                                            }
                                            Item { Layout.fillWidth: true }
                                        }

                                        Text {
                                            Layout.fillWidth: true
                                            text: controller.evalLiveProgressText + " • " + controller.evalLiveStatusText
                                            color: root.uiTextMuted
                                            font.pixelSize: root.evalCaptionSize
                                            horizontalAlignment: Text.AlignHCenter
                                        }
                                    }
                                }
                            }
                        }

                        GroupBox {
                            title: "Действия и запуск"
                            Layout.fillWidth: true
                            font.pixelSize: root.evalSectionTitleSize

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                Rectangle {
                                    Layout.fillWidth: true
                                    radius: Math.round(10 * root.uiScale)
                                    color: "#eef2fa"
                                    border.width: 1
                                    border.color: "#d7deea"
                                    implicitHeight: statusBarLayout.implicitHeight + root.spacingSm * 2

                                    RowLayout {
                                        id: statusBarLayout
                                        anchors.fill: parent
                                        anchors.margins: root.spacingSm
                                        spacing: root.spacingSm

                                        Text {
                                            text: "Статус: " + (controller.running ? "RUNNING" : "IDLE")
                                            color: controller.running ? root.p1Accent : root.uiTextMuted
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                        }
                                        Text { text: "•"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                                        Text {
                                            text: "Прогресс: " + controller.evalLiveProgressText
                                            color: root.uiTextMuted
                                            font.pixelSize: root.evalCaptionSize
                                        }
                                        Text { text: "•"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                                        Text {
                                            text: "Done/Total: " + controller.evalLiveGamesDone + "/" + controller.evalLiveGamesTotal
                                            color: root.uiTextMuted
                                            font.pixelSize: root.evalCaptionSize
                                        }
                                        Text { text: "•"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                                        Text {
                                            text: "Лидер: " + controller.evalLiveLeaderSide
                                            color: controller.evalLiveLeaderSide === "P1"
                                                ? root.p1Accent
                                                : controller.evalLiveLeaderSide === "P2"
                                                    ? root.p2Accent
                                                    : root.uiTextMuted
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                        }
                                        Item { Layout.fillWidth: true }
                                        Rectangle {
                                            Layout.preferredWidth: Math.round(120 * root.uiScale)
                                            Layout.preferredHeight: Math.round(4 * root.uiScale)
                                            radius: height / 2
                                            color: "#d9e1f0"
                                            clip: true
                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.top: parent.top
                                                anchors.bottom: parent.bottom
                                                width: parent.width * (controller.evalLiveGamesTotal > 0
                                                    ? Math.max(0.0, Math.min(1.0, controller.evalLiveGamesDone / controller.evalLiveGamesTotal))
                                                    : 0.0)
                                                radius: parent.radius
                                                color: controller.running ? root.p1Accent : "#9aa9c6"
                                            }
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingMd

                                    Button {
                                        text: "Обновить список агентов"
                                        enabled: !controller.running
                                        flat: true
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        onClicked: controller.refresh_eval_agents()
                                    }

                                    Button {
                                        text: "Запустить оценку"
                                        enabled: !controller.running && controller.evalLaunchReady
                                        highlighted: true
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        onClicked: controller.start_eval()
                                    }

                                    Button {
                                        text: "Остановить"
                                        enabled: controller.running
                                        highlighted: controller.running
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        onClicked: controller.stop_process()
                                    }

                                    Button {
                                        text: "Очистить лог"
                                        enabled: !controller.running
                                        flat: true
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        onClicked: controller.clear_eval_log()
                                    }

                                    Button {
                                        text: "Детали"
                                        flat: true
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        onClicked: evalDetailsDrawer.open()
                                    }
                                }
                            }
                        }

                        GroupBox {
                            title: "Конфигурация матча"
                            Layout.fillWidth: true
                            font.pixelSize: root.evalSectionTitleSize

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingXs

                                Text {
                                    text: controller.evalScenarioText
                                    wrapMode: Text.WordWrap
                                    color: "#2f3b52"
                                    font.bold: true
                                }
                                Text {
                                    text: controller.evalLaunchStatusText
                                    wrapMode: Text.WordWrap
                                    color: controller.evalLaunchReady ? "#2d7d33" : "#b24a00"
                                    font.bold: true
                                }
                                Text {
                                    text: controller.evalMiniSummary
                                    color: "#5b6472"
                                }
                            }
                        }

                        GroupBox {
                            title: "Итог и аналитика"
                            Layout.fillWidth: true
                            font.pixelSize: root.evalSectionTitleSize

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm

                                    Rectangle {
                                        Layout.fillWidth: true
                                        radius: Math.round(8 * root.uiScale)
                                        color: "#eef4ff"
                                        border.color: "#bcd0f8"
                                        border.width: 1
                                        implicitHeight: edgeCard.implicitHeight + root.spacingMd * 2
                                        Rectangle {
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            anchors.topMargin: Math.round(2 * root.uiScale)
                                            radius: parent.radius
                                            color: "#10000000"
                                            z: -1
                                        }
                                        ColumnLayout {
                                            id: edgeCard
                                            anchors.fill: parent
                                            anchors.margins: root.spacingMd
                                            spacing: Math.round(4 * root.uiScale)
                                            Text {
                                                text: "Matchup Edge"
                                                color: root.p1Accent
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                            Text {
                                                text: controller.evalLiveGamesDone > 0
                                                    ? (controller.evalLiveLeaderSide === "P1"
                                                        ? "P1 +" + Math.abs(Math.round((controller.evalLiveP1Winrate - controller.evalLiveP2Winrate) * 100)) + "%"
                                                        : controller.evalLiveLeaderSide === "P2"
                                                            ? "P2 +" + Math.abs(Math.round((controller.evalLiveP2Winrate - controller.evalLiveP1Winrate) * 100)) + "%"
                                                            : "0%")
                                                    : "—"
                                                color: controller.evalLiveLeaderSide === "P1"
                                                    ? root.p1Accent
                                                    : controller.evalLiveLeaderSide === "P2"
                                                        ? root.p2Accent
                                                        : root.uiTextMain
                                                font.bold: true
                                                font.pixelSize: Math.round(24 * root.uiScale)
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                            Text {
                                                text: "Live: P1 " + Math.round(controller.evalLiveP1Winrate * 100) + "% • P2 " + Math.round(controller.evalLiveP2Winrate * 100) + "%"
                                                color: root.uiTextMuted
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                            Text {
                                                text: "Итог P1: " + root.extractPercent(controller.evalResultWinrateP1)
                                                color: root.uiTextMuted
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                        }
                                    }

                                    Rectangle {
                                        Layout.fillWidth: true
                                        radius: Math.round(8 * root.uiScale)
                                        color: "#f7f9fd"
                                        border.color: "#d7deea"
                                        border.width: 1
                                        implicitHeight: confidenceCard.implicitHeight + root.spacingMd * 2
                                        Rectangle {
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            anchors.topMargin: Math.round(2 * root.uiScale)
                                            radius: parent.radius
                                            color: "#10000000"
                                            z: -1
                                        }
                                        ColumnLayout {
                                            id: confidenceCard
                                            anchors.fill: parent
                                            anchors.margins: root.spacingMd
                                            spacing: Math.round(4 * root.uiScale)
                                            Text {
                                                text: "Надежность"
                                                color: "#374151"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                            Text {
                                                text: {
                                                    var done = controller.evalLiveGamesDone
                                                    var diff = Math.abs(Math.round((controller.evalLiveP1Winrate - controller.evalLiveP2Winrate) * 100))
                                                    if (done >= 40 && diff >= 12) return "Высокая"
                                                    if (done >= 20 && diff >= 7) return "Средняя"
                                                    return "Низкая"
                                                }
                                                color: "#374151"
                                                font.bold: true
                                                font.pixelSize: Math.round(22 * root.uiScale)
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                            Text {
                                                text: "Игр: " + controller.evalLiveGamesDone + " • Разница: " + Math.abs(Math.round((controller.evalLiveP1Winrate - controller.evalLiveP2Winrate) * 100)) + "%"
                                                color: root.uiTextMuted
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                        }
                                    }

                                    Rectangle {
                                        Layout.fillWidth: true
                                        radius: Math.round(8 * root.uiScale)
                                        color: "#fff1f1"
                                        border.color: "#f0b6b6"
                                        border.width: 1
                                        implicitHeight: scoreCard.implicitHeight + root.spacingMd * 2
                                        Rectangle {
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            anchors.topMargin: Math.round(2 * root.uiScale)
                                            radius: parent.radius
                                            color: "#10000000"
                                            z: -1
                                        }
                                        ColumnLayout {
                                            id: scoreCard
                                            anchors.fill: parent
                                            anchors.margins: root.spacingMd
                                            spacing: Math.round(4 * root.uiScale)
                                            Text {
                                                text: "Итоговый счет"
                                                color: root.p2Accent
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                            Text {
                                                text: "P1 " + controller.evalLiveP1Wins + " • P2 " + controller.evalLiveP2Wins + " • D " + controller.evalLiveDraws
                                                color: root.uiTextMain
                                                font.bold: true
                                                font.pixelSize: Math.round(21 * root.uiScale)
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                            Text {
                                                text: "Winrate: P1 " + Math.round(controller.evalLiveP1Winrate * 100) + "% • P2 " + Math.round(controller.evalLiveP2Winrate * 100) + "%"
                                                color: root.uiTextMuted
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        GroupBox {
                            title: "Детали и лог"
                            visible: false
                            Layout.fillWidth: true
                            Layout.preferredHeight: root.evalShowLog ? Math.round(300 * root.uiScale) : Math.round(56 * root.uiScale)
                            Behavior on Layout.preferredHeight {
                                NumberAnimation { duration: 180; easing.type: Easing.InOutCubic }
                            }

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm
                                    Text {
                                        text: "Детали матча"
                                        font.bold: true
                                        color: "#334155"
                                    }
                                    Item { Layout.fillWidth: true }
                                    Button {
                                        text: root.evalShowLog ? "Свернуть лог" : "Показать лог"
                                        flat: true
                                        onClicked: root.evalShowLog = !root.evalShowLog
                                    }
                                }

                                TabBar {
                                    Layout.fillWidth: true
                                    visible: root.evalShowLog
                                    currentIndex: root.evalDetailTab
                                    onCurrentIndexChanged: root.evalDetailTab = currentIndex
                                    TabButton { text: "События" }
                                    TabButton { text: "Сводка" }
                                }

                                StackLayout {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    visible: root.evalShowLog
                                    currentIndex: root.evalDetailTab

                                    ScrollView {
                                        Layout.fillWidth: true
                                        Layout.fillHeight: true

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

                                    ScrollView {
                                        Layout.fillWidth: true
                                        Layout.fillHeight: true
                                        TextArea {
                                            readOnly: true
                                            wrapMode: TextArea.Wrap
                                            text: controller.evalSummaryText
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Drawer {
        id: evalDetailsDrawer
        edge: Qt.RightEdge
        width: Math.round(Math.min(root.width * 0.42, 640 * root.uiScale))
        height: root.height
        modal: false
        interactive: true

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: root.spacingMd
            spacing: root.spacingSm

            RowLayout {
                Layout.fillWidth: true
                Text {
                    text: "Детали матча"
                    font.bold: true
                    font.pixelSize: Math.round(16 * root.uiScale)
                    color: root.uiTextMain
                }
                Item { Layout.fillWidth: true }
                Button {
                    text: "Закрыть"
                    flat: true
                    onClicked: evalDetailsDrawer.close()
                }
            }

            TabBar {
                Layout.fillWidth: true
                currentIndex: root.evalDrawerTab
                onCurrentIndexChanged: root.evalDrawerTab = currentIndex
                TabButton { text: "События" }
                TabButton { text: "Сводка" }
            }

            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: root.evalDrawerTab

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    TextArea {
                        readOnly: true
                        wrapMode: TextArea.Wrap
                        text: controller.evalLogText
                    }
                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    TextArea {
                        readOnly: true
                        wrapMode: TextArea.Wrap
                        text: controller.evalSummaryText
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

    Dialog {
        id: trainingAlgoHelpDialog
        title: "Подсказка по моделям обучения"
        modal: true
        width: root.dialogWidthLg
        height: Math.round(700 * root.uiScale)
        anchors.centerIn: Overlay.overlay

        contentItem: ColumnLayout {
            spacing: root.spacingSm

            ScrollView {
                id: trainingAlgoHelpScroll
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                ColumnLayout {
                    id: trainingAlgoHelpColumn
                    width: Math.max(200, trainingAlgoHelpScroll.availableWidth)
                    spacing: root.spacingMd

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: root.spacingSm

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.minimumHeight: summarySpeedColumn.implicitHeight + Math.round(16 * root.uiScale)
                            radius: Math.round(10 * root.uiScale)
                            color: "#eff6ff"
                            border.color: "#bfdbfe"
                            border.width: 1

                            ColumnLayout {
                                id: summarySpeedColumn
                                anchors.fill: parent
                                anchors.margins: Math.round(10 * root.uiScale)
                                spacing: Math.round(4 * root.uiScale)

                                Label {
                                    text: "Скорость и простота"
                                    font.bold: true
                                    font.pixelSize: Math.round(13 * root.uiScale)
                                    color: "#1e3a8a"
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                                Label {
                                    text: "DQN · PPO — быстрые итерации, удобный старт обучения."
                                    wrapMode: Text.WordWrap
                                    color: "#334155"
                                    Layout.fillWidth: true
                                }
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.minimumHeight: summaryQualityColumn.implicitHeight + Math.round(16 * root.uiScale)
                            radius: Math.round(10 * root.uiScale)
                            color: "#faf5ff"
                            border.color: "#e9d5ff"
                            border.width: 1

                            ColumnLayout {
                                id: summaryQualityColumn
                                anchors.fill: parent
                                anchors.margins: Math.round(10 * root.uiScale)
                                spacing: Math.round(4 * root.uiScale)

                                Label {
                                    text: "Качество и поиск"
                                    font.bold: true
                                    font.pixelSize: Math.round(13 * root.uiScale)
                                    color: "#581c87"
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                                Label {
                                    text: "AlphaZero · Gumbel MuZero — сильнее за счёт просчёта вперёд, дороже по времени."
                                    wrapMode: Text.WordWrap
                                    color: "#334155"
                                    Layout.fillWidth: true
                                }
                            }
                        }
                    }

                    // DQN
                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: dqnCardRow.implicitHeight
                        radius: Math.round(12 * root.uiScale)
                        color: "#ffffff"
                        border.color: "#e5e7eb"
                        border.width: 1

                        RowLayout {
                            id: dqnCardRow
                            width: parent.width
                            spacing: 0

                            Rectangle {
                                width: Math.round(6 * root.uiScale)
                                Layout.fillHeight: true
                                color: "#2563eb"
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Layout.margins: Math.round(12 * root.uiScale)

                                Text {
                                    text: "DQN (Deep Q-Network)"
                                    font.bold: true
                                    font.pixelSize: Math.round(16 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }

                                Flow {
                                    Layout.fillWidth: true
                                    spacing: Math.round(6 * root.uiScale)

                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#dbeafe"
                                        implicitHeight: dqnB1.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: dqnB1.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: dqnB1
                                            anchors.centerIn: parent
                                            text: "Классика+"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#1e40af"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#e0e7ff"
                                        implicitHeight: dqnB2.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: dqnB2.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: dqnB2
                                            anchors.centerIn: parent
                                            text: "Надёжный"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#3730a3"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#dbeafe"
                                        implicitHeight: dqnB3.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: dqnB3.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: dqnB3
                                            anchors.centerIn: parent
                                            text: "Средний train"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#1e40af"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#e0e7ff"
                                        implicitHeight: dqnB4.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: dqnB4.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: dqnB4
                                            anchors.centerIn: parent
                                            text: "Q-оценки"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#3730a3"
                                        }
                                    }
                                }

                                Label {
                                    text: "Что это"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "ИИ, который учится понимать, какой ход выгоднее в текущей ситуации. Для каждого действия он оценивает ожидаемую пользу и выбирает лучший вариант."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "запоминает прошлые ситуации (состояние, действие, результат), потом на этих данных постепенно улучшает оценки действий. Со временем реже ошибается и лучше выбирает ходы в похожих сценариях."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• понятная логика выбора хода;\n• хорошее качество игры после обучения;\n• удобно сравнивать с PPO/AZ/GMZ;\n• обычно предсказуемое поведение в повторяющихся ситуациях;\n• подходит как надежный базовый агент для тестов и долгих прогонов."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• может учиться дольше PPO;\n• чувствителен к настройкам;\n• требует больше вычислений при тренировке;\n• качество сильно зависит от того, насколько удачно подобраны гиперпараметры;\n• в очень сложной тактике может хуже справляться, чем модели с полноценным поиском (MCTS/Search)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "когда нужен надежный агент с понятным поведением и есть готовность подождать обучение ради качества итоговой модели."
                                }
                            }
                        }
                    }

                    // PPO
                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: ppoCardRow.implicitHeight
                        radius: Math.round(12 * root.uiScale)
                        color: "#ffffff"
                        border.color: "#e5e7eb"
                        border.width: 1

                        RowLayout {
                            id: ppoCardRow
                            width: parent.width
                            spacing: 0

                            Rectangle {
                                width: Math.round(6 * root.uiScale)
                                Layout.fillHeight: true
                                color: "#0d9488"
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Layout.margins: Math.round(12 * root.uiScale)

                                Text {
                                    text: "PPO (Proximal Policy Optimization)"
                                    font.bold: true
                                    font.pixelSize: Math.round(16 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }

                                Flow {
                                    Layout.fillWidth: true
                                    spacing: Math.round(6 * root.uiScale)

                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#ccfbf1"
                                        implicitHeight: ppoB1.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: ppoB1.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: ppoB1
                                            anchors.centerIn: parent
                                            text: "Рабочий дефолт"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#115e59"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#99f6e4"
                                        implicitHeight: ppoB2.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: ppoB2.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: ppoB2
                                            anchors.centerIn: parent
                                            text: "Стабильный"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#134e4a"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#ccfbf1"
                                        implicitHeight: ppoB3.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: ppoB3.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: ppoB3
                                            anchors.centerIn: parent
                                            text: "Быстрый train"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#115e59"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#99f6e4"
                                        implicitHeight: ppoB4.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: ppoB4.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: ppoB4
                                            anchors.centerIn: parent
                                            text: "Policy-RL"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#134e4a"
                                        }
                                    }
                                }

                                Label {
                                    text: "Что это"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "ИИ, который учится напрямую улучшать стратегию выбора действий. Он не просто оценивает отдельные ходы, а постепенно делает всю политику игры более качественной."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "играет серии шагов (rollout), оценивает, какие решения были полезными, и обновляет стратегию небольшими безопасными шагами, чтобы не ломать уже выученное поведение."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• обычно стабильно обучается;\n• хороший баланс между скоростью обучения и качеством;\n• удобен как рабочий режим по умолчанию;\n• часто быстрее и предсказуемее в настройке, чем сложные search-модели;\n• подходит для длительных тренировок без сильных скачков поведения."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• не использует поиск по дереву на каждом ходе;\n• в сложной тактике может уступать AZ/GMZ с MCTS/Search;\n• качество зависит от rollout/epoch/minibatch настроек;\n• иногда требует тонкой подстройки коэффициентов (clip, entropy, value loss)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "когда нужен надежный универсальный агент с хорошим балансом скорость обучения / качество игры."
                                }
                            }
                        }
                    }

                    // AlphaZero
                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: azCardRow.implicitHeight
                        radius: Math.round(12 * root.uiScale)
                        color: "#ffffff"
                        border.color: "#e5e7eb"
                        border.width: 1

                        RowLayout {
                            id: azCardRow
                            width: parent.width
                            spacing: 0

                            Rectangle {
                                width: Math.round(6 * root.uiScale)
                                Layout.fillHeight: true
                                color: "#7c3aed"
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Layout.margins: Math.round(12 * root.uiScale)

                                Text {
                                    text: "AlphaZero (AZ)"
                                    font.bold: true
                                    font.pixelSize: Math.round(16 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }

                                Flow {
                                    Layout.fillWidth: true
                                    spacing: Math.round(6 * root.uiScale)

                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#ede9fe"
                                        implicitHeight: azB1.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: azB1.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: azB1
                                            anchors.centerIn: parent
                                            text: "Тактика+"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#5b21b6"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#ddd6fe"
                                        implicitHeight: azB2.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: azB2.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: azB2
                                            anchors.centerIn: parent
                                            text: "Качество"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#4c1d95"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#ede9fe"
                                        implicitHeight: azB3.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: azB3.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: azB3
                                            anchors.centerIn: parent
                                            text: "Compute-heavy"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#5b21b6"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#ddd6fe"
                                        implicitHeight: azB4.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: azB4.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: azB4
                                            anchors.centerIn: parent
                                            text: "MCTS"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#4c1d95"
                                        }
                                    }
                                }

                                Label {
                                    text: "Что это"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "ИИ, который сочетает нейросеть и поиск по дереву (MCTS). Нейросеть подсказывает хорошие направления, а MCTS просчитывает варианты вперед и помогает выбрать более сильный ход."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "играет self-play матчи, накапливает позиции и улучшает сеть так, чтобы она лучше оценивала ходы и состояния, опираясь на результаты поиска."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• сильная тактическая игра за счёт просчета вперед;\n• лучше учитывает последствия на несколько ходов;\n• часто заметно усиливается при росте search-бюджета;\n• хорошо подходит для eval/viewer, где важна сила решений."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• медленнее на инференсе из-за MCTS;\n• требует больше CPU/GPU ресурсов;\n• чувствителен к настройкам поиска (simulations, c_puct, temperature);\n• при слишком малом search-бюджете может терять преимущество."
                                }
                                Label {
                                    text: "Режимы инференса"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• Greedy — быстро, без поиска;\n• MCTS — сильнее, но медленнее."
                                }
                                Label {
                                    text: "Температура"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "влияет только в MCTS (в Greedy не используется)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "когда приоритет — качество решений и сила игры, а не максимальная скорость."
                                }
                            }
                        }
                    }

                    // Gumbel MuZero
                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: gmzCardRow.implicitHeight
                        radius: Math.round(12 * root.uiScale)
                        color: "#ffffff"
                        border.color: "#e5e7eb"
                        border.width: 1

                        RowLayout {
                            id: gmzCardRow
                            width: parent.width
                            spacing: 0

                            Rectangle {
                                width: Math.round(6 * root.uiScale)
                                Layout.fillHeight: true
                                color: "#d97706"
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Layout.margins: Math.round(12 * root.uiScale)

                                Text {
                                    text: "Gumbel MuZero (GMZ)"
                                    font.bold: true
                                    font.pixelSize: Math.round(16 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }

                                Flow {
                                    Layout.fillWidth: true
                                    spacing: Math.round(6 * root.uiScale)

                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#fef3c7"
                                        implicitHeight: gmzB1.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: gmzB1.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: gmzB1
                                            anchors.centerIn: parent
                                            text: "Топ Качество"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#92400e"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#fde68a"
                                        implicitHeight: gmzB2.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: gmzB2.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: gmzB2
                                            anchors.centerIn: parent
                                            text: "Тяжёлый режим"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#78350f"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#fef3c7"
                                        implicitHeight: gmzB3.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: gmzB3.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: gmzB3
                                            anchors.centerIn: parent
                                            text: "Very Compute-heavy"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#92400e"
                                        }
                                    }
                                    Rectangle {
                                        radius: Math.round(999 * root.uiScale)
                                        color: "#fde68a"
                                        implicitHeight: gmzB4.implicitHeight + Math.round(6 * root.uiScale)
                                        implicitWidth: gmzB4.implicitWidth + Math.round(14 * root.uiScale)
                                        Text {
                                            id: gmzB4
                                            anchors.centerIn: parent
                                            text: "Search+"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            color: "#78350f"
                                        }
                                    }
                                }

                                Label {
                                    text: "Что это"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "ИИ с поиском, который дополнительно использует внутреннюю модель динамики. Проще: он не только выбирает ход, но и внутри модели проигрывает возможное будущее."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "через self-play и unroll-обучение: representation/dynamics/prediction блоки совместно учатся лучше моделировать состояние, последствия действий и полезность решений."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• высокий потолок качества игры;\n• хорошо работает в сложных и длинных тактических сценариях;\n• search-режим часто дает сильные решения в eval/viewer;\n• мощный инструмент, когда цель — выжать максимум качества."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• самый тяжелый режим по вычислениям;\n• дольше тренируется и сложнее в тюнинге;\n• чувствителен к параметрам search/replay/unroll;\n• при малом compute может не раскрывать потенциал полностью."
                                }
                                Label {
                                    text: "Режимы инференса"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "• Greedy — быстрее, без search;\n• Search — сильнее, но медленнее."
                                }
                                Label {
                                    text: "Температура"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "влияет только в Search (в Greedy не используется)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: "#111827"
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: "#374151"
                                    text: "когда нужен максимум силы модели и есть бюджет по времени/ресурсам для обучения и оценки."
                                }
                            }
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Item { Layout.fillWidth: true }
                Button {
                    text: "Закрыть"
                    onClicked: trainingAlgoHelpDialog.close()
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
        function onEvalGamesChanged(value) {
            if (typeof evalGamesField !== "undefined" && evalGamesField) {
                evalGamesField.text = value.toString()
            }
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
