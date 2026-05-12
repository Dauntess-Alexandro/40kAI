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
    visibility: Window.Maximized
    title: "40kAI"
    color: bgBase

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
    property int radiusSm: Math.round(8 * uiScale)
    property int radiusMd: Math.round(12 * uiScale)
    property color bgBase: "#0f1319"
    property color bgSurface: "#171d26"
    property color bgElevated: "#1d2632"
    property color borderMuted: "#2a3342"
    property color textPrimary: "#d7dde7"
    property color textSecondary: "#98a4b8"
    property color accentP1: "#2f6ed8"
    property color accentP2: "#cf3f3f"
    property color accentPrimaryAction: "#b88a26"
    property color accentDanger: "#a35345"
    property color accentGhost: "#6f7d92"
    property color uiBgBase: bgSurface
    property color uiBgCard: bgElevated
    property color uiBorder: borderMuted
    property color uiTextMain: textPrimary
    property color uiTextMuted: textSecondary
    property color p1Accent: accentP1
    property color p2Accent: accentP2
    property int evalDrawerTab: 0
    property int evalSectionTitleSize: Math.round(13 * uiScale)
    property int evalCaptionSize: Math.round(11 * uiScale)
    property int actionButtonHeight: Math.round(30 * uiScale)
    property int actionButtonMinWidth: Math.round(120 * uiScale)
    property bool mainLogExpanded: true
    property bool rosterLoadoutFocus: false
    property string fontUiFamily: "Rajdhani"
    property string fontDataFamily: "IBM Plex Mono"

    function extractPercent(text) {
        var raw = text || ""
        var match = raw.match(/([0-9]+(?:[\\.,][0-9]+)?)\s*%/)
        return match ? (match[1] + "%") : "—"
    }

    font.family: fontUiFamily
    font.pixelSize: Math.round(14 * uiScale)
    palette.window: bgBase
    palette.base: bgSurface
    palette.button: bgElevated
    palette.buttonText: textPrimary
    palette.text: textPrimary
    palette.windowText: textPrimary
    palette.highlight: accentP1
    palette.highlightedText: "#ffffff"
    palette.placeholderText: "#7f8ba0"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        TabBar {
            id: mainTabs
            Layout.fillWidth: true
            spacing: root.spacingXs
            background: Rectangle {
                color: root.bgBase
                border.width: 0
            }

            TacticalTabButton { text: "Главная" }
            TacticalTabButton { text: "Ростер" }
            TacticalTabButton { text: "Метрики модели" }
            TacticalTabButton { text: "Метрики эвристики" }
            TacticalTabButton { text: "Игра" }
            TacticalTabButton { text: "Настройки" }
            TacticalTabButton { text: "Оценка" }
        }

        StackLayout {
            id: mainStack
            currentIndex: mainTabs.currentIndex
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ScrollView {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg
                    clip: true

                    ColumnLayout {
                        width: Math.max(parent ? parent.width : 0, root.width - 2 * root.spacingLg)
                        spacing: root.spacingMd

                        ChamferPanel {
                            Layout.fillWidth: true
                            fillColor: root.uiBgBase
                            borderColor: root.uiBorder
                            borderWidth: 1
                            cutSize: Math.round(12 * root.uiScale)
                            contentMargin: 0
                            implicitHeight: heroRow.implicitHeight + root.spacingMd * 2

                            RowLayout {
                                id: heroRow
                                anchors.fill: parent
                                anchors.margins: root.spacingMd
                                spacing: root.spacingMd

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: Math.round(4 * root.uiScale)
                                    Text {
                                        text: "ЦЕНТР УПРАВЛЕНИЯ ТРЕНИРОВКОЙ"
                                        color: root.uiTextMain
                                        font.bold: true
                                        font.pixelSize: Math.round(20 * root.uiScale)
                                        font.family: root.fontUiFamily
                                        font.letterSpacing: 1.0
                                    }
                                    Text {
                                        text: root.statusText
                                        color: root.uiTextMuted
                                        font.family: root.fontDataFamily
                                    }
                                }

                                Rectangle {
                                    radius: 0
                                    color: "#1e2734"
                                    border.width: 1
                                    border.color: controller.running ? "#b88a26" : "#4c5667"
                                    implicitWidth: trainStatusLabel.implicitWidth + Math.round(24 * root.uiScale)
                                    implicitHeight: trainStatusLabel.implicitHeight + Math.round(12 * root.uiScale)
                                    Text {
                                        id: trainStatusLabel
                                        anchors.centerIn: parent
                                        text: controller.running ? "RUNNING" : "IDLE"
                                        color: controller.running ? "#e1be68" : "#9ca3af"
                                        font.bold: true
                                        font.family: root.fontDataFamily
                                        font.pixelSize: Math.round(11 * root.uiScale)
                                        font.letterSpacing: 0.8
                                    }
                                }

                                ColumnLayout {
                                    spacing: Math.round(2 * root.uiScale)
                                    Text {
                                        text: "ПРОГРЕСС"
                                        color: root.uiTextMuted
                                        font.capitalization: Font.AllUppercase
                                        font.family: root.fontUiFamily
                                        font.bold: true
                                        font.letterSpacing: 0.9
                                    }
                                    Text {
                                        text: controller.progressStats
                                        color: root.uiTextMain
                                        font.family: root.fontDataFamily
                                    }
                                }
                            }
                        }

                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: Math.round(28 * root.uiScale)

                            ProgressBar {
                                id: trainingProgress
                                anchors.fill: parent
                                value: controller.progressValue
                                background: Rectangle {
                                    radius: 0
                                    color: "#1a2230"
                                    border.width: 1
                                    border.color: root.uiBorder
                                }
                                contentItem: Item {
                                    Rectangle {
                                        width: trainingProgress.visualPosition * parent.width
                                        height: parent.height
                                        color: "#b88a26"
                                    }
                                }
                            }
                            Text {
                                anchors.centerIn: parent
                                text: controller.progressText
                                color: root.uiTextMain
                                font.bold: true
                                font.family: root.fontDataFamily
                            }
                        }

                        ChamferPanel {
                            Layout.fillWidth: true
                            Layout.minimumWidth: 0
                            fillColor: root.uiBgCard
                            borderColor: root.uiBorder
                            borderWidth: 1
                            cutSize: Math.round(10 * root.uiScale)
                            contentMargin: root.spacingMd
                            implicitHeight: trainCtxRoot.implicitHeight + 2 * root.spacingMd

                            ColumnLayout {
                                id: trainCtxRoot
                                width: parent.width
                                spacing: root.spacingSm

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingMd
                                    TrainMiniBoard {
                                        scaleRef: root.uiScale
                                        Layout.alignment: Qt.AlignTop
                                    }
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingXs

                                        Text {
                                            Layout.fillWidth: true
                                            text: "КОНТЕКСТ ТРЕНИРОВКИ"
                                            color: root.uiTextMain
                                            font.bold: true
                                            font.pixelSize: root.evalSectionTitleSize
                                            font.family: root.fontUiFamily
                                            font.capitalization: Font.AllUppercase
                                            font.letterSpacing: 1.0
                                            wrapMode: Text.Wrap
                                            maximumLineCount: 2
                                        }

                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingXs
                                            Label {
                                                text: "P1:"
                                                color: root.uiTextMuted
                                                font.family: root.fontUiFamily
                                                font.bold: true
                                            }
                                            Image {
                                                source: controller.faction_icon_source(controller.trainRosterP1Faction)
                                                sourceSize.width: Math.min(root.factionIconSize, Math.round(28 * root.uiScale))
                                                sourceSize.height: Math.min(root.factionIconSize, Math.round(28 * root.uiScale))
                                                Layout.preferredWidth: sourceSize.width
                                                Layout.preferredHeight: sourceSize.height
                                                visible: source !== ""
                                                fillMode: Image.PreserveAspectFit
                                                smooth: true
                                            }
                                            Label {
                                                Layout.fillWidth: true
                                                text: controller.trainRosterP1Faction
                                                color: root.uiTextMain
                                                font.family: root.fontUiFamily
                                                font.bold: true
                                                elide: Text.ElideRight
                                            }
                                        }
                                        Label {
                                            visible: controller.trainContextP1RosterLines.length === 0
                                            Layout.fillWidth: true
                                            text: "Состав P1: пусто — задайте на вкладке «Ростер»."
                                            color: root.uiTextMuted
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            wrapMode: Text.Wrap
                                        }
                                        Flow {
                                            visible: controller.trainContextP1RosterLines.length > 0
                                            Layout.fillWidth: true
                                            spacing: Math.round(5 * root.uiScale)
                                            Repeater {
                                                model: controller.trainContextP1RosterLines
                                                delegate: Rectangle {
                                                    implicitHeight: p1ChipLine.implicitHeight + Math.round(8 * root.uiScale)
                                                    implicitWidth: p1ChipLine.width + Math.round(10 * root.uiScale)
                                                    color: "#141b26"
                                                    border.width: 1
                                                    border.color: "#35475c"
                                                    Text {
                                                        id: p1ChipLine
                                                        anchors.verticalCenter: parent.verticalCenter
                                                        anchors.left: parent.left
                                                        anchors.leftMargin: Math.round(5 * root.uiScale)
                                                        width: Math.round(180 * root.uiScale)
                                                        text: modelData
                                                        elide: Text.ElideRight
                                                        color: "#c9d1dc"
                                                        font.family: root.fontDataFamily
                                                        font.pixelSize: Math.round(10 * root.uiScale)
                                                    }
                                                }
                                            }
                                        }
                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingXs
                                            Label {
                                                text: "P2:"
                                                color: root.uiTextMuted
                                                font.family: root.fontUiFamily
                                                font.bold: true
                                            }
                                            Image {
                                                source: controller.faction_icon_source(controller.trainRosterP2Faction)
                                                sourceSize.width: Math.min(root.factionIconSize, Math.round(28 * root.uiScale))
                                                sourceSize.height: Math.min(root.factionIconSize, Math.round(28 * root.uiScale))
                                                Layout.preferredWidth: sourceSize.width
                                                Layout.preferredHeight: sourceSize.height
                                                visible: source !== ""
                                                fillMode: Image.PreserveAspectFit
                                                smooth: true
                                            }
                                            Label {
                                                Layout.fillWidth: true
                                                text: controller.trainRosterP2Faction
                                                color: root.uiTextMain
                                                font.family: root.fontUiFamily
                                                font.bold: true
                                                elide: Text.ElideRight
                                            }
                                        }
                                        Label {
                                            visible: controller.trainContextP2RosterLines.length === 0
                                            Layout.fillWidth: true
                                            text: "Состав P2: пусто — задайте на вкладке «Ростер»."
                                            color: root.uiTextMuted
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            wrapMode: Text.Wrap
                                        }
                                        Flow {
                                            visible: controller.trainContextP2RosterLines.length > 0
                                            Layout.fillWidth: true
                                            spacing: Math.round(5 * root.uiScale)
                                            Repeater {
                                                model: controller.trainContextP2RosterLines
                                                delegate: Rectangle {
                                                    implicitHeight: p2ChipLine.implicitHeight + Math.round(8 * root.uiScale)
                                                    implicitWidth: p2ChipLine.width + Math.round(10 * root.uiScale)
                                                    color: "#141b26"
                                                    border.width: 1
                                                    border.color: "#35475c"
                                                    Text {
                                                        id: p2ChipLine
                                                        anchors.verticalCenter: parent.verticalCenter
                                                        anchors.left: parent.left
                                                        anchors.leftMargin: Math.round(5 * root.uiScale)
                                                        width: Math.round(180 * root.uiScale)
                                                        text: modelData
                                                        elide: Text.ElideRight
                                                        color: "#c9d1dc"
                                                        font.family: root.fontDataFamily
                                                        font.pixelSize: Math.round(10 * root.uiScale)
                                                    }
                                                }
                                            }
                                        }
                                        Text {
                                            Layout.fillWidth: true
                                            text: "Оружие, дроны и опции листа — позже; сейчас только имена и количество из «Ростер»."
                                            color: root.uiTextMuted
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(9 * root.uiScale)
                                            wrapMode: Text.Wrap
                                        }
                                        RowLayout {
                                            Layout.fillWidth: true
                                            Item { Layout.fillWidth: true }
                                            Rectangle {
                                                radius: 0
                                                color: "#141b26"
                                                border.width: 1
                                                border.color: controller.learnerSide === "P1" ? root.p1Accent : root.p2Accent
                                                width: learnerSideBadge.implicitWidth + Math.round(14 * root.uiScale)
                                                height: learnerSideBadge.implicitHeight + Math.round(8 * root.uiScale)
                                                Text {
                                                    id: learnerSideBadge
                                                    anchors.centerIn: parent
                                                    text: "УЧИТСЯ: " + controller.learnerSide
                                                    font.family: root.fontDataFamily
                                                    font.bold: true
                                                    font.pixelSize: root.evalCaptionSize
                                                    color: root.uiTextMain
                                                }
                                            }
                                        }
                                    }
                                }

                                Text {
                                    Layout.fillWidth: true
                                    text: controller.trainSetupSummaryLine
                                    wrapMode: Text.Wrap
                                    color: "#d0d6e0"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: root.evalCaptionSize
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: controller.opponentPreviewText
                                    wrapMode: Text.WordWrap
                                    maximumLineCount: 2
                                    elide: Text.ElideRight
                                    color: root.uiTextMuted
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(10 * root.uiScale)
                                }
                            }
                        }

                        GridLayout {
                            Layout.fillWidth: true
                            columns: 3
                            columnSpacing: root.spacingMd
                            rowSpacing: root.spacingMd

                            ChamferPanel {
                                Layout.fillWidth: true
                                Layout.minimumWidth: 0
                                Layout.preferredHeight: Math.round(280 * root.uiScale)
                                fillColor: root.uiBgCard
                                borderColor: root.uiBorder
                                borderWidth: 1
                                cutSize: Math.round(10 * root.uiScale)
                                contentMargin: root.spacingMd

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingSm

                                    Text {
                                        text: "МИССИЯ"
                                        color: root.uiTextMain
                                        font.bold: true
                                        font.pixelSize: root.evalSectionTitleSize
                                        font.family: root.fontUiFamily
                                        font.capitalization: Font.AllUppercase
                                        font.letterSpacing: 1.0
                                    }

                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Label {
                                            text: "ВЫБОР"
                                            font.bold: true
                                            font.family: root.fontUiFamily
                                            font.letterSpacing: 0.7
                                            color: root.uiTextMuted
                                        }
                                        StyledComboBox {
                                            id: missionCombo
                                            Layout.preferredWidth: Math.max(root.inputWidthSm, Math.round(150 * root.uiScale))
                                            model: controller.missionOptions
                                            currentIndex: Math.max(0, controller.missionOptions.indexOf(controller.selectedMission))
                                            onActivated: controller.set_selected_mission_index(currentIndex)
                                        }
                                    }

                                    GridLayout {
                                        id: missionMetaGrid
                                        columns: 2
                                        columnSpacing: root.spacingMd
                                        rowSpacing: root.spacingXs
                                        Layout.fillWidth: true
                                        property int labelColW: Math.round(124 * root.uiScale)

                                        Label {
                                            Layout.minimumWidth: missionMetaGrid.labelColW
                                            Layout.maximumWidth: missionMetaGrid.labelColW
                                            horizontalAlignment: Text.AlignLeft
                                            text: "РЕЖИМ"
                                            font.bold: true
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMuted
                                        }
                                        Label {
                                            Layout.fillWidth: true
                                            horizontalAlignment: Text.AlignLeft
                                            text: "ONLY WAR"
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMain
                                        }
                                        Label {
                                            Layout.minimumWidth: missionMetaGrid.labelColW
                                            Layout.maximumWidth: missionMetaGrid.labelColW
                                            horizontalAlignment: Text.AlignLeft
                                            text: "РАЗМЕР"
                                            font.bold: true
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMuted
                                        }
                                        Label {
                                            Layout.fillWidth: true
                                            horizontalAlignment: Text.AlignLeft
                                            text: "60×40"
                                            font.family: root.fontDataFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMain
                                        }
                                        Label {
                                            Layout.minimumWidth: missionMetaGrid.labelColW
                                            Layout.maximumWidth: missionMetaGrid.labelColW
                                            horizontalAlignment: Text.AlignLeft
                                            text: "ТОЧКА"
                                            font.bold: true
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMuted
                                        }
                                        Label {
                                            Layout.fillWidth: true
                                            horizontalAlignment: Text.AlignLeft
                                            text: "1, центр (30,20)"
                                            font.family: root.fontDataFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMain
                                        }
                                        Label {
                                            Layout.minimumWidth: missionMetaGrid.labelColW
                                            Layout.maximumWidth: missionMetaGrid.labelColW
                                            horizontalAlignment: Text.AlignLeft
                                            text: "ДЕПЛОЙ"
                                            font.bold: true
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMuted
                                        }
                                        Label {
                                            Layout.fillWidth: true
                                            horizontalAlignment: Text.AlignLeft
                                            text: "Attacker слева / Defender справа"
                                            wrapMode: Text.Wrap
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMain
                                        }
                                        Label {
                                            Layout.minimumWidth: missionMetaGrid.labelColW
                                            Layout.maximumWidth: missionMetaGrid.labelColW
                                            horizontalAlignment: Text.AlignLeft
                                            text: "ПРИМЕЧАНИЕ"
                                            font.bold: true
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMuted
                                        }
                                        Label {
                                            Layout.fillWidth: true
                                            horizontalAlignment: Text.AlignLeft
                                            text: "roll-off определяет роли"
                                            wrapMode: Text.Wrap
                                            font.family: root.fontUiFamily
                                            font.pixelSize: root.evalCaptionSize
                                            color: root.uiTextMain
                                        }
                                    }
                                }
                            }

                            ChamferPanel {
                                Layout.fillWidth: true
                                Layout.minimumWidth: 0
                                Layout.preferredHeight: Math.round(280 * root.uiScale)
                                fillColor: root.uiBgCard
                                borderColor: root.uiBorder
                                borderWidth: 1
                                cutSize: Math.round(10 * root.uiScale)
                                contentMargin: root.spacingMd

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingSm

                                    Text {
                                        text: "КОНФИГУРАЦИЯ"
                                        color: root.uiTextMain
                                        font.bold: true
                                        font.pixelSize: root.evalSectionTitleSize
                                        font.family: root.fontUiFamily
                                        font.capitalization: Font.AllUppercase
                                        font.letterSpacing: 1.0
                                    }

                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Label { text: "ЭПИЗОДЫ"; font.bold: true; color: root.uiTextMuted }
                                        TextField {
                                            id: numGamesField
                                            text: controller.numGames.toString()
                                            validator: IntValidator { bottom: 1 }
                                            Layout.preferredWidth: root.inputWidthMd
                                            font.family: root.fontDataFamily
                                            background: Rectangle {
                                                radius: 0
                                                color: parent.activeFocus ? "#1e2633" : "#141b26"
                                                border.width: 1
                                                border.color: parent.activeFocus ? "#b88a26" : "#2f3848"
                                            }
                                            onEditingFinished: {
                                                var value = parseInt(text)
                                                if (!isNaN(value)) {
                                                    controller.set_num_games(value)
                                                }
                                            }
                                        }
                                    }

                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Label { text: "АЛГОРИТМ"; font.bold: true; color: root.uiTextMuted }
                                        StyledComboBox {
                                            id: trainingAlgoComboMain
                                            Layout.fillWidth: true
                                            model: [
                                                { value: "dqn", label: "DQN" },
                                                { value: "ppo", label: "PPO" },
                                                { value: "alphazero", label: "ALPHAZERO" },
                                                { value: "gumbel_muzero", label: "GUMBEL MUZERO" }
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
                                            text: "ⓘ"
                                            ToolTip.visible: hovered
                                            ToolTip.text: "О моделях и алгоритмах"
                                            ToolTip.delay: 400
                                            implicitWidth: Math.round(36 * root.uiScale)
                                            implicitHeight: Math.round(32 * root.uiScale)
                                            enabled: !controller.running
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.enabled
                                                    ? (parent.hovered ? "#e8c86a" : "#8b95a8")
                                                    : "#5c6474"
                                                font.bold: true
                                                font.pixelSize: Math.round(14 * root.uiScale)
                                                horizontalAlignment: Text.AlignHCenter
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                            background: ChamferPanel {
                                                cutSize: Math.round(6 * root.uiScale)
                                                contentMargin: 0
                                                fillColor: parent.hovered ? "#1e2633" : "transparent"
                                                borderWidth: 1
                                                borderColor: parent.hovered ? "#b88a26" : "#4f5a6b"
                                            }
                                            onClicked: trainingAlgoHelpDialog.open()
                                        }
                                    }

                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Label { text: "СТОРОНА"; font.bold: true; color: root.uiTextMuted }
                                        StyledComboBox {
                                            Layout.preferredWidth: Math.max(root.inputWidthMd, Math.round(170 * root.uiScale))
                                            model: controller.learnerSideOptions
                                            currentIndex: Math.max(0, controller.learnerSideOptions.indexOf(controller.learnerSide))
                                            enabled: !controller.running
                                            onActivated: controller.set_learner_side(currentText)
                                        }
                                    }

                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Label { text: "ОППОНЕНТ"; font.bold: true; color: root.uiTextMuted }
                                        StyledComboBox {
                                            Layout.fillWidth: true
                                            model: [
                                                { value: "heuristic", label: "ЭВРИСТИКА" },
                                                { value: "latest_snapshot", label: "ПОСЛЕДНИЙ СНАПШОТ" },
                                                { value: "specific_agent", label: "КОНКРЕТНЫЙ АГЕНТ" }
                                            ]
                                            textRole: "label"
                                            valueRole: "value"
                                            currentIndex: {
                                                for (var i = 0; i < model.length; i++) {
                                                    if (model[i].value === controller.opponentSource) return i
                                                }
                                                return 0
                                            }
                                            enabled: !controller.running
                                            onActivated: {
                                                if (currentIndex >= 0 && currentIndex < model.length)
                                                    controller.set_opponent_source(model[currentIndex].value)
                                            }
                                        }
                                    }

                                    StyledComboBox {
                                        Layout.fillWidth: true
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
                                        text: controller.opponentPreviewText
                                        color: root.uiTextMuted
                                        Layout.fillWidth: true
                                        wrapMode: Text.NoWrap
                                        elide: Text.ElideRight
                                        maximumLineCount: 1
                                    }
                                }
                            }

                            ChamferPanel {
                                Layout.fillWidth: true
                                Layout.minimumWidth: 0
                                Layout.preferredHeight: Math.round(280 * root.uiScale)
                                fillColor: root.uiBgCard
                                borderColor: root.uiBorder
                                borderWidth: 1
                                cutSize: Math.round(10 * root.uiScale)
                                contentMargin: root.spacingMd

                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: root.spacingSm

                                    Text {
                                        text: "ОПЕРАЦИИ"
                                        color: root.uiTextMain
                                        font.bold: true
                                        font.pixelSize: root.evalSectionTitleSize
                                        font.family: root.fontUiFamily
                                        font.capitalization: Font.AllUppercase
                                        font.letterSpacing: 1.0
                                    }

                                    TacticalCheckBox {
                                        text: "САМООБУЧЕНИЕ ОТ СТАРОЙ МОДЕЛИ"
                                        scaleRef: root.uiScale
                                        labelFontFamily: root.fontUiFamily
                                        labelFontSize: root.evalCaptionSize
                                        labelColorEnabled: root.uiTextMain
                                        checked: controller.selfPlayFromCheckpoint
                                        enabled: !controller.running
                                        onToggled: controller.set_self_play_from_checkpoint(checked)
                                    }
                                    TacticalCheckBox {
                                        text: "ПРОДОЛЖИТЬ ОБУЧЕНИЕ (RESUME_CHECKPOINT)"
                                        scaleRef: root.uiScale
                                        labelFontFamily: root.fontUiFamily
                                        labelFontSize: root.evalCaptionSize
                                        labelColorEnabled: root.uiTextMain
                                        checked: controller.resumeFromCheckpoint
                                        enabled: !controller.running
                                        onToggled: controller.set_resume_from_checkpoint(checked)
                                    }
                                    TacticalCheckBox {
                                        text: "НЕ ЛОГИРОВАТЬ ТРЕНИРОВКУ (SPEED)"
                                        scaleRef: root.uiScale
                                        labelFontFamily: root.fontUiFamily
                                        labelFontSize: root.evalCaptionSize
                                        labelColorEnabled: root.uiTextMain
                                        checked: controller.disableTrainLogging
                                        enabled: !controller.running
                                        onToggled: controller.set_disable_train_logging(checked)
                                    }
                                    TacticalCheckBox {
                                        text: "ДЕТАЛЬНЫЙ ТРЕЙС ДЕЙСТВИЙ (DEBUG)"
                                        scaleRef: root.uiScale
                                        labelFontFamily: root.fontUiFamily
                                        labelFontSize: root.evalCaptionSize
                                        labelColorEnabled: root.uiTextMain
                                        checked: controller.actionTrace
                                        enabled: !controller.running
                                        onToggled: controller.set_action_trace(checked)
                                    }
                                    TacticalCheckBox {
                                        text: "ОЧИЩАТЬ ЛОГИ АВТОМАТИЧЕСКИ"
                                        scaleRef: root.uiScale
                                        labelFontFamily: root.fontUiFamily
                                        labelFontSize: root.evalCaptionSize
                                        labelColorEnabled: root.uiTextMain
                                        checked: controller.autoClearLogs
                                        enabled: !controller.running
                                        onToggled: controller.set_auto_clear_logs(checked)
                                    }

                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Button {
                                            text: "ТРЕНИРОВКА 8X"
                                            enabled: !controller.running
                                            onClicked: controller.start_train_8x()
                                            Layout.preferredWidth: Math.round(150 * root.uiScale)
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.enabled ? "#151102" : "#6a6347"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                            background: ChamferPanel {
                                                cutSize: Math.round(6 * root.uiScale)
                                                contentMargin: 0
                                                fillColor: parent.pressed ? "#d7a719" : (parent.hovered ? "#e8b932" : "#b88a26")
                                                borderWidth: 1
                                                borderColor: parent.hovered ? "#ffe08a" : "#8f6b1f"
                                            }
                                        }
                                        Button {
                                            text: "ОЧИСТИТЬ КЭШ"
                                            enabled: !controller.running
                                            onClicked: clearCacheDialog.open()
                                            Layout.preferredWidth: Math.round(140 * root.uiScale)
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.enabled ? "#d5b15a" : "#737b8a"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                            background: ChamferPanel {
                                                cutSize: Math.round(6 * root.uiScale)
                                                contentMargin: 0
                                                fillColor: parent.hovered ? "#25303d" : "transparent"
                                                borderWidth: 1
                                                borderColor: parent.hovered ? "#e1be68" : "#b88a26"
                                            }
                                        }
                                        Button {
                                            text: "ОЧИСТИТЬ ЛОГИ"
                                            enabled: !controller.running
                                            onClicked: controller.clear_agent_logs()
                                            Layout.preferredWidth: Math.round(140 * root.uiScale)
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.enabled ? "#d5b15a" : "#737b8a"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                            background: ChamferPanel {
                                                cutSize: Math.round(6 * root.uiScale)
                                                contentMargin: 0
                                                fillColor: parent.hovered ? "#25303d" : "transparent"
                                                borderWidth: 1
                                                borderColor: parent.hovered ? "#e1be68" : "#b88a26"
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        ChamferPanel {
                            Layout.fillWidth: true
                            Layout.minimumWidth: 0
                            fillColor: root.uiBgCard
                            borderColor: root.uiBorder
                            borderWidth: 1
                            cutSize: Math.round(10 * root.uiScale)
                            contentMargin: root.spacingMd
                            implicitHeight: mainLogExpanded ? Math.round(320 * root.uiScale) : Math.round(56 * root.uiScale)

                            ColumnLayout {
                                anchors.fill: parent
                                spacing: root.spacingSm

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingXs

                                    RowLayout {
                                        Layout.fillWidth: true
                                        Text {
                                            text: "ЖУРНАЛ"
                                            color: "#e8c86a"
                                            font.bold: true
                                            font.pixelSize: Math.round(14 * root.uiScale)
                                            font.family: root.fontUiFamily
                                            font.capitalization: Font.AllUppercase
                                            font.letterSpacing: 1.4
                                        }
                                        Item { Layout.fillWidth: true }
                                        Button {
                                            text: "ОЧИСТИТЬ"
                                            flat: true
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.hovered ? "#d5b15a" : "#9aa3b2"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                            background: ChamferPanel {
                                                cutSize: Math.round(6 * root.uiScale)
                                                contentMargin: 0
                                                fillColor: parent.hovered ? "#25303d" : "transparent"
                                                borderWidth: 1
                                                borderColor: parent.hovered ? "#b88a26" : "#4f5a6b"
                                            }
                                            onClicked: logArea.text = ""
                                        }
                                        Button {
                                            text: root.mainLogExpanded ? "СВЕРНУТЬ" : "РАЗВЕРНУТЬ"
                                            flat: true
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.hovered ? "#d5b15a" : "#9aa3b2"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                horizontalAlignment: Text.AlignHCenter
                                                verticalAlignment: Text.AlignVCenter
                                            }
                                            background: ChamferPanel {
                                                cutSize: Math.round(6 * root.uiScale)
                                                contentMargin: 0
                                                fillColor: parent.hovered ? "#25303d" : "transparent"
                                                borderWidth: 1
                                                borderColor: parent.hovered ? "#b88a26" : "#4f5a6b"
                                            }
                                            onClicked: root.mainLogExpanded = !root.mainLogExpanded
                                        }
                                    }

                                    Rectangle {
                                        Layout.fillWidth: true
                                        height: 1
                                        color: "#2a3544"
                                    }
                                }

                                ScrollView {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    visible: root.mainLogExpanded
                                    TextArea {
                                        id: logArea
                                        readOnly: true
                                        wrapMode: TextArea.Wrap
                                        text: ""
                                        font.family: root.fontDataFamily
                                        color: root.uiTextMain
                                        background: Rectangle {
                                            radius: 0
                                            color: "#111722"
                                            border.width: 1
                                            border.color: "#2e394d"
                                        }
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

                    ChamferPanel {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Math.round(122 * root.uiScale)
                        Layout.minimumHeight: Math.round(110 * root.uiScale)
                        fillColor: root.uiBgCard
                        borderColor: root.uiBorder
                        borderWidth: 1
                        cutSize: Math.round(10 * root.uiScale)
                        contentMargin: root.spacingSm

                        ColumnLayout {
                            anchors.fill: parent
                            spacing: root.spacingXs

                            RowLayout {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Math.round(30 * root.uiScale)
                                spacing: root.spacingSm

                                Text {
                                    text: "БОЕВАЯ СВОДКА РОСТЕРА"
                                    color: "#e8c86a"
                                    font.bold: true
                                    font.family: root.fontUiFamily
                                    font.pixelSize: root.evalSectionTitleSize
                                    font.capitalization: Font.AllUppercase
                                    font.letterSpacing: 1.0
                                }

                                Item { Layout.fillWidth: true }

                                RowLayout {
                                    spacing: root.spacingXs
                                    Text {
                                        text: controller.rosterSummary + " • " + controller.rosterCompositionDelta + " • "
                                        color: root.uiTextMuted
                                        font.family: root.fontDataFamily
                                        font.pixelSize: root.evalCaptionSize
                                        elide: Text.ElideRight
                                    }
                                    Text {
                                        text: controller.rosterPointsDelta
                                        color: controller.rosterPointsDeltaColor
                                        font.family: root.fontDataFamily
                                        font.pixelSize: root.evalCaptionSize
                                        font.bold: true
                                    }
                                }

                                Button {
                                    text: root.rosterLoadoutFocus ? "FOCUS: ON" : "FOCUS: OFF"
                                    flat: true
                                    onClicked: root.rosterLoadoutFocus = !root.rosterLoadoutFocus
                                    contentItem: Text {
                                        text: parent.text
                                        color: parent.hovered ? "#e8c86a" : "#9aa3b2"
                                        font.bold: true
                                        font.family: root.fontDataFamily
                                        font.pixelSize: root.evalCaptionSize
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    background: ChamferPanel {
                                        cutSize: Math.round(6 * root.uiScale)
                                        contentMargin: 0
                                        fillColor: parent.hovered ? "#25303d" : "transparent"
                                        borderWidth: 1
                                        borderColor: parent.hovered ? "#b88a26" : "#4f5a6b"
                                    }
                                }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Math.round(62 * root.uiScale)
                                spacing: root.spacingMd

                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: Math.round(60 * root.uiScale)
                                    color: "#141b26"
                                    border.width: 1
                                    border.color: "#2f6ed8"
                                    radius: 0
                                    Column {
                                        anchors.fill: parent
                                        anchors.margins: Math.round(6 * root.uiScale)
                                        spacing: 2
                                        Text { text: "P1 СВОДКА"; color: "#9eb6d4"; font.bold: true; font.family: root.fontUiFamily; font.pixelSize: Math.round(10 * root.uiScale) }
                                        Text { text: "Общий бюджет: " + controller.rosterPointsP1; color: root.uiTextMain; font.family: root.fontDataFamily; font.pixelSize: Math.round(10 * root.uiScale); elide: Text.ElideRight }
                                        Text { text: controller.rosterKpiP1; color: root.uiTextMuted; font.family: root.fontDataFamily; font.pixelSize: Math.round(9 * root.uiScale); elide: Text.ElideRight }
                                    }
                                }

                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: Math.round(60 * root.uiScale)
                                    color: "#141b26"
                                    border.width: 1
                                    border.color: "#7b4a4a"
                                    radius: 0
                                    Column {
                                        anchors.fill: parent
                                        anchors.margins: Math.round(6 * root.uiScale)
                                        spacing: 2
                                        Text { text: "P2 СВОДКА"; color: "#d4a69e"; font.bold: true; font.family: root.fontUiFamily; font.pixelSize: Math.round(10 * root.uiScale) }
                                        Text { text: "Общий бюджет: " + controller.rosterPointsP2; color: root.uiTextMain; font.family: root.fontDataFamily; font.pixelSize: Math.round(10 * root.uiScale); elide: Text.ElideRight }
                                        Text { text: controller.rosterKpiP2; color: root.uiTextMuted; font.family: root.fontDataFamily; font.pixelSize: Math.round(9 * root.uiScale); elide: Text.ElideRight }
                                    }
                                }

                                Rectangle {
                                    implicitWidth: Math.round(340 * root.uiScale)
                                    implicitHeight: Math.round(60 * root.uiScale)
                                    color: "#10151d"
                                    border.width: 1
                                    border.color: "#2f3848"
                                    radius: 0
                                    Column {
                                        anchors.fill: parent
                                        anchors.margins: Math.round(6 * root.uiScale)
                                        spacing: 2
                                        Text { text: "АКТИВНЫЙ ПРОФИЛЬ ВООРУЖЕНИЯ"; color: "#e8c86a"; font.bold: true; font.family: root.fontUiFamily; font.pixelSize: Math.round(10 * root.uiScale) }
                                        Text { text: controller.rosterActiveProfile; color: root.uiTextMain; font.family: root.fontDataFamily; font.pixelSize: Math.round(9 * root.uiScale); elide: Text.ElideRight }
                                    }
                                }
                            }
                        }
                    }

                    GridLayout {
                        columns: 5
                        columnSpacing: root.spacingMd
                        rowSpacing: 0
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        GroupBox {
                            title: "Фракции"
                            Layout.fillWidth: true
                            Layout.fillHeight: false
                            Layout.alignment: Qt.AlignTop
                            Layout.minimumWidth: Math.round(220 * root.uiScale)
                            Layout.preferredWidth: Math.round(250 * root.uiScale)
                            Layout.horizontalStretchFactor: 1
                            opacity: root.rosterLoadoutFocus ? 0.45 : 1.0
                            Behavior on opacity { NumberAnimation { duration: 130 } }

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
                                        color: root.bgSurface
                                        border.color: root.uiBorder
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
                                        color: root.bgSurface
                                        border.color: root.uiBorder
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
                            Layout.minimumWidth: Math.round(300 * root.uiScale)
                            Layout.preferredWidth: Math.round(360 * root.uiScale)
                            Layout.horizontalStretchFactor: 3
                            opacity: root.rosterLoadoutFocus ? 0.55 : 1.0
                            Behavior on opacity { NumberAnimation { duration: 130 } }

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: root.spacingXs
                                spacing: Math.round(6 * root.uiScale)

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
                                    onCurrentIndexChanged: controller.set_roster_available_preview_index(currentIndex)
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
                                            color: ListView.isCurrentItem ? "#ffffff" : root.uiTextMain
                                            elide: Text.ElideRight
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: unitIconAvailable.visible ? unitIconAvailable.right : parent.left
                                            anchors.leftMargin: root.spacingSm
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: {
                                                availableUnitsView.currentIndex = index
                                                controller.set_roster_available_preview_index(index)
                                            }
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
                            Layout.minimumWidth: Math.round(230 * root.uiScale)
                            Layout.preferredWidth: Math.round(300 * root.uiScale)
                            Layout.maximumWidth: Math.round(360 * root.uiScale)
                            Layout.horizontalStretchFactor: 2

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: root.spacingXs
                                spacing: root.spacingSm

                                Label {
                                    text: "ВЕРСТАК ВООРУЖЕНИЯ"
                                    font.bold: true
                                    Layout.preferredHeight: Math.round(22 * root.uiScale)
                                    verticalAlignment: Text.AlignVCenter
                                    color: "#e8c86a"
                                    font.family: root.fontUiFamily
                                    font.capitalization: Font.AllUppercase
                                    font.letterSpacing: 1.0
                                }
                                Label {
                                    text: controller.rosterWeaponsPreviewTarget + " · " + controller.rosterWeaponsPreviewUnitName
                                    font.bold: true
                                    color: root.uiTextMain
                                    elide: Text.ElideRight
                                    Layout.fillWidth: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    font.family: root.fontUiFamily
                                }
                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: Math.round(24 * root.uiScale)
                                    color: "#121a26"
                                    border.width: 1
                                    border.color: "#2f3848"
                                    radius: 0
                                    Text {
                                        anchors.fill: parent
                                        anchors.margins: Math.round(6 * root.uiScale)
                                        text: "ДБ: " + controller.rosterWeaponsSelectedRanged + " | ББ: " + controller.rosterWeaponsSelectedMelee
                                        color: root.uiTextMuted
                                        elide: Text.ElideRight
                                        verticalAlignment: Text.AlignVCenter
                                        font.family: root.fontDataFamily
                                        font.pixelSize: Math.round(10 * root.uiScale)
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingXs
                                    Label {
                                        text: "ДАЛЬНИЙ БОЙ:"
                                        color: "#9eb6d4"
                                        font.bold: true
                                        font.family: root.fontUiFamily
                                    }
                                    Item { Layout.fillWidth: true }
                                    Label {
                                        text: controller.rosterWeaponsPreviewRangedCount + " проф."
                                        color: root.uiTextMuted
                                        font.family: root.fontDataFamily
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                    }
                                }
                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: 1
                                    color: "#4b5d76"
                                }
                                Repeater {
                                    model: controller.rosterWeaponsPreviewRanged
                                    delegate: Rectangle {
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(56 * root.uiScale)
                                        color: modelData === controller.rosterWeaponsSelectedRanged ? "#1f2f45" : "#131923"
                                        border.width: 1
                                        border.color: modelData === controller.rosterWeaponsSelectedRanged ? "#6ea0db" : "#2f3848"
                                        radius: 0
                                        RowLayout {
                                            anchors.fill: parent
                                            anchors.margins: Math.round(5 * root.uiScale)
                                            spacing: root.spacingXs
                                            Image {
                                                source: controller.roster_weapon_icon_source(modelData)
                                                sourceSize.width: Math.round(34 * root.uiScale)
                                                sourceSize.height: Math.round(34 * root.uiScale)
                                                Layout.preferredWidth: Math.round(34 * root.uiScale)
                                                Layout.preferredHeight: Math.round(34 * root.uiScale)
                                                fillMode: Image.PreserveAspectFit
                                                visible: source !== ""
                                                smooth: true
                                            }
                                            ColumnLayout {
                                                Layout.fillWidth: true
                                                spacing: 0
                                                Text {
                                                    text: modelData
                                                    color: root.uiTextMain
                                                    font.bold: true
                                                    font.family: root.fontUiFamily
                                                    elide: Text.ElideRight
                                                }
                                                Text {
                                                    text: controller.roster_weapon_statline_for_selected(modelData)
                                                    color: root.uiTextMuted
                                                    font.family: root.fontDataFamily
                                                    font.pixelSize: Math.round(9 * root.uiScale)
                                                    elide: Text.ElideRight
                                                }
                                                Flow {
                                                    visible: modelData === controller.rosterWeaponsSelectedRanged
                                                    Layout.fillWidth: true
                                                    spacing: Math.round(4 * root.uiScale)
                                                    Repeater {
                                                        model: controller.rosterActiveRangedBadges
                                                        delegate: Rectangle {
                                                            implicitHeight: badgeRText.implicitHeight + Math.round(3 * root.uiScale)
                                                            implicitWidth: badgeRText.implicitWidth + Math.round(6 * root.uiScale)
                                                            color: "#243545"
                                                            border.width: 1
                                                            border.color: "#3f5b75"
                                                            radius: 0
                                                            Text {
                                                                id: badgeRText
                                                                anchors.centerIn: parent
                                                                text: modelData
                                                                color: "#d6eefc"
                                                                font.bold: true
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            Rectangle {
                                                visible: modelData === controller.rosterWeaponsSelectedRanged
                                                color: "#5e86b8"
                                                border.width: 1
                                                border.color: "#8fb6e8"
                                                radius: 0
                                                Layout.alignment: Qt.AlignTop
                                                implicitWidth: selectedRText.implicitWidth + Math.round(8 * root.uiScale)
                                                implicitHeight: selectedRText.implicitHeight + Math.round(2 * root.uiScale)
                                                Text {
                                                    id: selectedRText
                                                    anchors.centerIn: parent
                                                    text: "SELECTED"
                                                    color: "#0d1520"
                                                    font.bold: true
                                                    font.family: root.fontDataFamily
                                                    font.pixelSize: Math.round(8 * root.uiScale)
                                                }
                                            }
                                        }
                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: controller.set_selected_roster_ranged_weapon(modelData)
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingXs
                                    Label {
                                        text: "БЛИЖНИЙ БОЙ:"
                                        color: "#c4a882"
                                        font.bold: true
                                        font.family: root.fontUiFamily
                                    }
                                    Item { Layout.fillWidth: true }
                                    Label {
                                        text: controller.rosterWeaponsPreviewMeleeCount + " проф."
                                        color: root.uiTextMuted
                                        font.family: root.fontDataFamily
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                    }
                                }
                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: 1
                                    color: "#6f5a42"
                                }
                                Repeater {
                                    model: controller.rosterWeaponsPreviewMelee
                                    delegate: Rectangle {
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(56 * root.uiScale)
                                        color: modelData === controller.rosterWeaponsSelectedMelee ? "#3a2a1f" : "#131923"
                                        border.width: 1
                                        border.color: modelData === controller.rosterWeaponsSelectedMelee ? "#c79a5a" : "#2f3848"
                                        radius: 0
                                        RowLayout {
                                            anchors.fill: parent
                                            anchors.margins: Math.round(5 * root.uiScale)
                                            spacing: root.spacingXs
                                            Image {
                                                source: controller.roster_weapon_icon_source(modelData)
                                                sourceSize.width: Math.round(34 * root.uiScale)
                                                sourceSize.height: Math.round(34 * root.uiScale)
                                                Layout.preferredWidth: Math.round(34 * root.uiScale)
                                                Layout.preferredHeight: Math.round(34 * root.uiScale)
                                                fillMode: Image.PreserveAspectFit
                                                visible: source !== ""
                                                smooth: true
                                            }
                                            ColumnLayout {
                                                Layout.fillWidth: true
                                                spacing: 0
                                                Text {
                                                    text: modelData
                                                    color: root.uiTextMain
                                                    font.bold: true
                                                    font.family: root.fontUiFamily
                                                    elide: Text.ElideRight
                                                }
                                                Text {
                                                    text: controller.roster_weapon_statline_for_selected(modelData)
                                                    color: root.uiTextMuted
                                                    font.family: root.fontDataFamily
                                                    font.pixelSize: Math.round(9 * root.uiScale)
                                                    elide: Text.ElideRight
                                                }
                                                Flow {
                                                    visible: modelData === controller.rosterWeaponsSelectedMelee
                                                    Layout.fillWidth: true
                                                    spacing: Math.round(4 * root.uiScale)
                                                    Repeater {
                                                        model: controller.rosterActiveMeleeBadges
                                                        delegate: Rectangle {
                                                            implicitHeight: badgeMText.implicitHeight + Math.round(3 * root.uiScale)
                                                            implicitWidth: badgeMText.implicitWidth + Math.round(6 * root.uiScale)
                                                            color: "#3b3022"
                                                            border.width: 1
                                                            border.color: "#6f5a42"
                                                            radius: 0
                                                            Text {
                                                                id: badgeMText
                                                                anchors.centerIn: parent
                                                                text: modelData
                                                                color: "#f5e4cf"
                                                                font.bold: true
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            Rectangle {
                                                visible: modelData === controller.rosterWeaponsSelectedMelee
                                                color: "#8a6238"
                                                border.width: 1
                                                border.color: "#c79a5a"
                                                radius: 0
                                                Layout.alignment: Qt.AlignTop
                                                implicitWidth: selectedMText.implicitWidth + Math.round(8 * root.uiScale)
                                                implicitHeight: selectedMText.implicitHeight + Math.round(2 * root.uiScale)
                                                Text {
                                                    id: selectedMText
                                                    anchors.centerIn: parent
                                                    text: "SELECTED"
                                                    color: "#150f07"
                                                    font.bold: true
                                                    font.family: root.fontDataFamily
                                                    font.pixelSize: Math.round(8 * root.uiScale)
                                                }
                                            }
                                        }
                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: controller.set_selected_roster_melee_weapon(modelData)
                                        }
                                    }
                                }

                                Label {
                                    visible: controller.rosterWeaponsPreviewUnknown.length > 0
                                    text: "Не классифицировано: " + controller.rosterWeaponsPreviewUnknown.join(", ")
                                    color: "#b87a7a"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(9 * root.uiScale)
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                            }
                        }

                        GroupBox {
                            title: ""
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignTop
                            Layout.minimumWidth: Math.round(230 * root.uiScale)
                            Layout.preferredWidth: Math.round(280 * root.uiScale)
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
                                        height: Math.round(78 * root.uiScale)
                                        color: controller.roster_entry_active("P1", index) ? "#1f2f45" : "#141b26"
                                        border.width: 1
                                        border.color: controller.roster_entry_active("P1", index) ? "#d5b15a" : "#2f3848"
                                        radius: 0
                                        Behavior on color { ColorAnimation { duration: 120 } }
                                        Behavior on border.color { ColorAnimation { duration: 120 } }

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

                                        Column {
                                            anchors.left: unitIconPlayer.visible ? unitIconPlayer.right : parent.left
                                            anchors.leftMargin: root.spacingSm
                                            anchors.right: parent.right
                                            anchors.rightMargin: root.spacingSm
                                            anchors.verticalCenter: parent.verticalCenter
                                            spacing: 1
                                            Text {
                                                text: model.display
                                                color: root.uiTextMain
                                                elide: Text.ElideRight
                                                font.bold: true
                                                font.family: root.fontUiFamily
                                            }
                                            Text {
                                                text: controller.roster_entry_role("P1", index) + " • models " + controller.roster_entry_models("P1", index) + " • " + controller.roster_entry_points("P1", index)
                                                color: "#9eb6d4"
                                                elide: Text.ElideRight
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Text {
                                                text: controller.roster_entry_abilities("P1", index)
                                                color: "#d5b15a"
                                                elide: Text.ElideRight
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Text {
                                                text: "ДБ " + controller.roster_entry_ranged_weapon("P1", index) + " • ББ " + controller.roster_entry_melee_weapon("P1", index)
                                                color: root.uiTextMuted
                                                elide: Text.ElideRight
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                        }

                                        Rectangle {
                                            visible: controller.roster_entry_active("P1", index)
                                            anchors.right: parent.right
                                            anchors.top: parent.top
                                            anchors.topMargin: 2
                                            anchors.rightMargin: 2
                                            color: "#c79a32"
                                            border.width: 1
                                            border.color: "#e8c86a"
                                            radius: 0
                                            implicitWidth: activeP1Text.implicitWidth + 8
                                            implicitHeight: activeP1Text.implicitHeight + 2
                                            Text {
                                                id: activeP1Text
                                                anchors.centerIn: parent
                                                text: "ACTIVE"
                                                color: "#120f05"
                                                font.bold: true
                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                font.family: root.fontDataFamily
                                            }
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: {
                                                playerRosterView.currentIndex = index
                                            }
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
                            Layout.minimumWidth: Math.round(230 * root.uiScale)
                            Layout.preferredWidth: Math.round(280 * root.uiScale)
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
                                        height: Math.round(78 * root.uiScale)
                                        color: controller.roster_entry_active("P2", index) ? "#3a2323" : "#141b26"
                                        border.width: 1
                                        border.color: controller.roster_entry_active("P2", index) ? "#d5b15a" : "#2f3848"
                                        radius: 0
                                        Behavior on color { ColorAnimation { duration: 120 } }
                                        Behavior on border.color { ColorAnimation { duration: 120 } }

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

                                        Column {
                                            anchors.left: unitIconModel.visible ? unitIconModel.right : parent.left
                                            anchors.leftMargin: root.spacingSm
                                            anchors.right: parent.right
                                            anchors.rightMargin: root.spacingSm
                                            anchors.verticalCenter: parent.verticalCenter
                                            spacing: 1
                                            Text {
                                                text: model.display
                                                color: root.uiTextMain
                                                elide: Text.ElideRight
                                                font.bold: true
                                                font.family: root.fontUiFamily
                                            }
                                            Text {
                                                text: controller.roster_entry_role("P2", index) + " • models " + controller.roster_entry_models("P2", index) + " • " + controller.roster_entry_points("P2", index)
                                                color: "#d4a69e"
                                                elide: Text.ElideRight
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Text {
                                                text: controller.roster_entry_abilities("P2", index)
                                                color: "#d5b15a"
                                                elide: Text.ElideRight
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Text {
                                                text: "ДБ " + controller.roster_entry_ranged_weapon("P2", index) + " • ББ " + controller.roster_entry_melee_weapon("P2", index)
                                                color: root.uiTextMuted
                                                elide: Text.ElideRight
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                        }

                                        Rectangle {
                                            visible: controller.roster_entry_active("P2", index)
                                            anchors.right: parent.right
                                            anchors.top: parent.top
                                            anchors.topMargin: 2
                                            anchors.rightMargin: 2
                                            color: "#c79a32"
                                            border.width: 1
                                            border.color: "#e8c86a"
                                            radius: 0
                                            implicitWidth: activeP2Text.implicitWidth + 8
                                            implicitHeight: activeP2Text.implicitHeight + 2
                                            Text {
                                                id: activeP2Text
                                                anchors.centerIn: parent
                                                text: "ACTIVE"
                                                color: "#120f05"
                                                font.bold: true
                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                font.family: root.fontDataFamily
                                            }
                                        }

                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: {
                                                modelRosterView.currentIndex = index
                                            }
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
                            color: root.uiTextMuted
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
                                color: root.bgSurface
                                border.color: root.uiBorder
                                border.width: 1
                                implicitHeight: Math.round(92 * root.uiScale)

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: root.spacingSm
                                    spacing: 4

                                    Text { text: "Модель"; font.bold: true; color: root.uiTextMain }
                                    Text { text: "Алгоритм: " + controller.metricsAlgo; color: root.uiTextMuted }
                                    Text { text: "Режим: " + controller.metricsMode; color: root.uiTextMuted }
                                    Text { text: "Run ID: " + controller.metricsRunId; color: "#777777"; elide: Text.ElideRight }
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                radius: 6
                                color: "#1a2a40"
                                border.color: "#2f6ed8"
                                border.width: 1
                                implicitHeight: Math.round(92 * root.uiScale)

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: root.spacingSm
                                    spacing: 4

                                    Text { text: "Последний DET-eval"; font.bold: true; color: root.uiTextMain }
                                    Text { text: "Эпизод: " + controller.detEpisodeLast; color: root.uiTextMuted }
                                    Text { text: "Winrate: " + controller.detWinrateLast; color: root.uiTextMuted }
                                    Text { text: "Reward: " + controller.detRewardLast + " | Ep_len: " + controller.detEpLenLast; color: root.uiTextMuted }
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                radius: 6
                                color: "#332b1d"
                                border.color: "#b88a26"
                                border.width: 1
                                implicitHeight: Math.round(92 * root.uiScale)

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: root.spacingSm
                                    spacing: 4

                                    Text { text: "Оппонент"; font.bold: true; color: root.uiTextMain }
                                    Text { text: "Self-play: " + (controller.selfPlayEnabled ? "включён" : "выключен"); color: root.uiTextMuted }
                                    Text { text: "Источник оппонента: " + controller.opponentSource; color: root.uiTextMuted }
                                    Text { text: "Алгоритм оппонента: " + controller.opponentAlgo + (controller.opponentId.length > 0 ? (" (id=" + controller.opponentId + ")") : ""); color: root.uiTextMuted }
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
                                        color: root.uiTextMuted
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
                                        color: root.uiTextMuted
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
                                        color: root.uiTextMuted
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
                                        color: root.uiTextMuted
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
                                        color: root.uiTextMuted
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
                                        color: root.uiTextMuted
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
                                        color: root.uiTextMuted
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
                                        color: root.uiTextMuted
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
                            color: root.uiTextMuted
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
                                    color: root.uiTextMuted
                                }

                                RowLayout {
                                    visible: controller.playInferenceModeVisible
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm

                                    Label {
                                        text: controller.playInferenceModeLabel
                                        font.bold: true
                                        font.capitalization: Font.AllUppercase
                                        font.letterSpacing: 0.8
                                    }

                                    StyledComboBox {
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
                                        color: root.uiTextMuted
                                        font.capitalization: Font.AllUppercase
                                        font.letterSpacing: 0.8
                                    }

                                    TextField {
                                        visible: controller.playInferenceTemperatureVisible
                                        Layout.preferredWidth: Math.round(80 * root.uiScale)
                                        enabled: !controller.running
                                        text: controller.playInferenceTemperature
                                        placeholderText: "0.10"
                                        font.family: root.fontDataFamily
                                        onEditingFinished: controller.set_play_inference_temperature(text)
                                    }
                                }

                                Rectangle {
                                    visible: controller.playInferenceModeVisible
                                    Layout.fillWidth: true
                                    color: root.uiBgCard
                                    border.color: root.uiBorder
                                    border.width: 1
                                    radius: Math.round(8 * root.uiScale)
                                    implicitHeight: playInferenceHelpText.implicitHeight + Math.round(12 * root.uiScale)
                                    Text {
                                        id: playInferenceHelpText
                                        anchors.fill: parent
                                        anchors.margins: Math.round(6 * root.uiScale)
                                        wrapMode: Text.WordWrap
                                        color: root.uiTextMuted
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
                                    color: root.uiTextMuted
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
                            color: root.uiBgCard
                            border.color: root.uiBorder
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
                                    color: root.uiTextMuted
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
                            color: root.uiBgCard
                            border.color: root.uiBorder
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
                                    color: root.uiTextMuted
                                    Layout.fillWidth: true
                                }

                                StyledComboBox {
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
                                    color: root.uiTextMuted
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            radius: Math.round(10 * root.uiScale)
                            color: root.uiBgCard
                            border.color: root.uiBorder
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

                        ChamferPanel {
                            Layout.fillWidth: true
                            fillColor: root.uiBgBase
                            borderColor: root.uiBorder
                            borderWidth: 1
                            cutSize: Math.round(12 * root.uiScale)
                            contentMargin: 0
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
                                        text: "ОЦЕНКА: P1 VS P2"
                                        font.pixelSize: Math.round(22 * root.uiScale)
                                        font.bold: true
                                        color: root.uiTextMain
                                        font.family: root.fontUiFamily
                                        font.letterSpacing: 1.0
                                    }
                                    Text {
                                        text: controller.evalMiniSummary
                                        color: root.uiTextMuted
                                        font.family: root.fontDataFamily
                                        font.capitalization: Font.AllUppercase
                                    }
                                }

                                Rectangle {
                                    radius: 0
                                    color: "#1e2734"
                                    border.width: 1
                                    border.color: controller.running ? "#b88a26" : "#4c5667"
                                    implicitWidth: evalRunStatus.implicitWidth + Math.round(22 * root.uiScale)
                                    implicitHeight: evalRunStatus.implicitHeight + Math.round(10 * root.uiScale)
                                    Text {
                                        id: evalRunStatus
                                        anchors.centerIn: parent
                                        text: controller.running ? "RUNNING" : "IDLE"
                                        font.bold: true
                                        color: controller.running ? "#e1be68" : "#9ca3af"
                                        font.pixelSize: Math.round(11 * root.uiScale)
                                        font.family: root.fontDataFamily
                                        font.letterSpacing: 0.8
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
                                        font.family: root.fontDataFamily
                                        background: Rectangle {
                                            radius: 0
                                            color: parent.enabled ? "#253244" : "#202734"
                                            border.width: 1
                                            border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                        }
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
                                    color: root.uiBgCard
                                    radius: 0
                                    border.width: 1
                                    border.color: root.uiBorder
                                    implicitHeight: matchupHeadLayout.implicitHeight + root.spacingMd * 2

                                    ColumnLayout {
                                        id: matchupHeadLayout
                                        anchors.fill: parent
                                        anchors.margins: root.spacingMd
                                        spacing: Math.round(4 * root.uiScale)

                                        Text {
                                            text: (controller.evalDuelTitle || "").toUpperCase()
                                            font.bold: true
                                            font.pixelSize: Math.round(22 * root.uiScale)
                                            color: root.uiTextMain
                                            font.family: root.fontUiFamily
                                            font.letterSpacing: 1.0
                                        }
                                        Text {
                                            text: (controller.evalDuelSubtitle || "").toUpperCase()
                                            font.pixelSize: Math.round(13 * root.uiScale)
                                            color: root.uiTextMuted
                                            font.family: root.fontDataFamily
                                        }
                                    }
                                }

                                Text {
                                    text: "deterministic, epsilon=0"
                                    color: root.uiTextMuted
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingMd

                                    ChamferPanel {
                                        Layout.fillWidth: true
                                        fillColor: "#16253a"
                                        borderColor: "#2f6ed8"
                                        borderWidth: 1
                                        cutSize: Math.round(12 * root.uiScale)
                                        contentMargin: 0
                                        implicitHeight: Math.max(p1CardLayout.implicitHeight, p2CardLayout.implicitHeight) + root.spacingSm * 2

                                        ColumnLayout {
                                            id: p1CardLayout
                                            anchors.fill: parent
                                            anchors.margins: root.spacingSm
                                            spacing: root.spacingXs

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                HexAvatar {
                                                    width: Math.round(30 * root.uiScale)
                                                    height: width
                                                    fillColor: "#2f6ed8"
                                                    borderColor: "#84a9ee"
                                                    label: controller.evalP1IconText
                                                }
                                                Text {
                                                    text: "P1"
                                                    color: "#2f6ed8"
                                                    font.bold: true
                                                    font.pixelSize: Math.round(16 * root.uiScale)
                                                    font.family: root.fontUiFamily
                                                    font.letterSpacing: 1.0
                                                }
                                                Item { Layout.fillWidth: true }
                                            }

                                            StyledComboBox {
                                                Layout.fillWidth: true
                                                enabled: !controller.running
                                                model: [
                                                    { value: "agent", label: "АГЕНТ" },
                                                    { value: "heuristic", label: "ЭВРИСТИКА" }
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
                                            StyledComboBox {
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
                                                color: root.uiTextMain
                                                font.bold: true
                                                font.family: root.fontDataFamily
                                            }

                                            Flow {
                                                Layout.fillWidth: true
                                                spacing: Math.round(6 * root.uiScale)
                                                Repeater {
                                                    model: controller.evalP1Badges
                                                    delegate: Rectangle {
                                                        radius: 0
                                                        color: "#1f3552"
                                                        border.width: 1
                                                        border.color: "#2f6ed8"
                                                        implicitWidth: badgeP1Text.implicitWidth + Math.round(12 * root.uiScale)
                                                        implicitHeight: badgeP1Text.implicitHeight + Math.round(6 * root.uiScale)
                                                        Text {
                                                            id: badgeP1Text
                                                            anchors.centerIn: parent
                                                            text: (modelData || "").toString().toUpperCase()
                                                            color: "#9fc2ff"
                                                            font.pixelSize: Math.round(11 * root.uiScale)
                                                            font.bold: true
                                                            font.family: root.fontUiFamily
                                                            font.letterSpacing: 0.6
                                                        }
                                                    }
                                                }
                                            }

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                Button {
                                                    text: "COPY ID"
                                                    flat: true
                                                    enabled: controller.evalP1FullAgentId.length > 0
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.6
                                                    onClicked: controller.copy_eval_agent_id("P1")
                                                    ToolTip.visible: hovered && controller.evalP1FullAgentId.length > 0
                                                    ToolTip.text: controller.evalP1FullAgentId
                                                }
                                                Label {
                                                    text: "Режим:"
                                                    font.bold: true
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.8
                                                    color: root.uiTextMuted
                                                    opacity: controller.evalP1InferenceModeVisible ? 1.0 : 0.55
                                                }
                                                StyledComboBox {
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
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.8
                                                    color: root.uiTextMuted
                                                    opacity: controller.evalP1InferenceTemperatureVisible ? 1.0 : 0.55
                                                }
                                                TextField {
                                                    Layout.preferredWidth: Math.round(80 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP1InferenceTemperatureVisible
                                                    opacity: controller.evalP1InferenceTemperatureVisible ? 1.0 : 0.55
                                                    text: controller.evalP1InferenceTemperature
                                                    placeholderText: "0.10"
                                                    font.family: root.fontDataFamily
                                                    background: Rectangle {
                                                        radius: 0
                                                        color: parent.enabled ? "#253244" : "#202734"
                                                        border.width: 1
                                                        border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                                    }
                                                    onEditingFinished: {
                                                        if (controller.evalP1InferenceTemperatureVisible) {
                                                            controller.set_eval_p1_inference_temperature(text)
                                                        }
                                                    }
                                                }
                                                Button {
                                                    text: "ⓘ"
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

                                    ChamferPanel {
                                        Layout.fillWidth: true
                                        fillColor: "#361f23"
                                        borderColor: "#cf3f3f"
                                        borderWidth: 1
                                        cutSize: Math.round(12 * root.uiScale)
                                        contentMargin: 0
                                        implicitHeight: Math.max(p1CardLayout.implicitHeight, p2CardLayout.implicitHeight) + root.spacingSm * 2

                                        ColumnLayout {
                                            id: p2CardLayout
                                            anchors.fill: parent
                                            anchors.margins: root.spacingSm
                                            spacing: root.spacingXs

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                HexAvatar {
                                                    width: Math.round(30 * root.uiScale)
                                                    height: width
                                                    fillColor: "#cf3f3f"
                                                    borderColor: "#e38c8c"
                                                    label: controller.evalP2IconText
                                                }
                                                Text {
                                                    text: "P2"
                                                    color: "#cf3f3f"
                                                    font.bold: true
                                                    font.pixelSize: Math.round(16 * root.uiScale)
                                                    font.family: root.fontUiFamily
                                                    font.letterSpacing: 1.0
                                                }
                                                Item { Layout.fillWidth: true }
                                            }

                                            StyledComboBox {
                                                Layout.fillWidth: true
                                                enabled: !controller.running
                                                model: [
                                                    { value: "agent", label: "АГЕНТ" },
                                                    { value: "heuristic", label: "ЭВРИСТИКА" }
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
                                            StyledComboBox {
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
                                                color: root.uiTextMain
                                                font.bold: true
                                                font.family: root.fontDataFamily
                                            }

                                            Flow {
                                                Layout.fillWidth: true
                                                spacing: Math.round(6 * root.uiScale)
                                                Repeater {
                                                    model: controller.evalP2Badges
                                                    delegate: Rectangle {
                                                        radius: 0
                                                        color: "#4a282c"
                                                        border.width: 1
                                                        border.color: "#cf3f3f"
                                                        implicitWidth: badgeP2Text.implicitWidth + Math.round(12 * root.uiScale)
                                                        implicitHeight: badgeP2Text.implicitHeight + Math.round(6 * root.uiScale)
                                                        Text {
                                                            id: badgeP2Text
                                                            anchors.centerIn: parent
                                                            text: (modelData || "").toString().toUpperCase()
                                                            color: "#ffb6b6"
                                                            font.pixelSize: Math.round(11 * root.uiScale)
                                                            font.bold: true
                                                            font.family: root.fontUiFamily
                                                            font.letterSpacing: 0.6
                                                        }
                                                    }
                                                }
                                            }

                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: root.spacingSm
                                                Button {
                                                    text: "COPY ID"
                                                    flat: true
                                                    enabled: controller.evalP2FullAgentId.length > 0
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.6
                                                    onClicked: controller.copy_eval_agent_id("P2")
                                                    ToolTip.visible: hovered && controller.evalP2FullAgentId.length > 0
                                                    ToolTip.text: controller.evalP2FullAgentId
                                                }
                                                Label {
                                                    text: "Режим:"
                                                    font.bold: true
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.8
                                                    color: root.uiTextMuted
                                                    opacity: controller.evalP2InferenceModeVisible ? 1.0 : 0.55
                                                }
                                                StyledComboBox {
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
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.8
                                                    color: root.uiTextMuted
                                                    opacity: controller.evalP2InferenceTemperatureVisible ? 1.0 : 0.55
                                                }
                                                TextField {
                                                    Layout.preferredWidth: Math.round(80 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP2InferenceTemperatureVisible
                                                    opacity: controller.evalP2InferenceTemperatureVisible ? 1.0 : 0.55
                                                    text: controller.evalP2InferenceTemperature
                                                    placeholderText: "0.10"
                                                    font.family: root.fontDataFamily
                                                    background: Rectangle {
                                                        radius: 0
                                                        color: parent.enabled ? "#253244" : "#202734"
                                                        border.width: 1
                                                        border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                                    }
                                                    onEditingFinished: {
                                                        if (controller.evalP2InferenceTemperatureVisible) {
                                                            controller.set_eval_p2_inference_temperature(text)
                                                        }
                                                    }
                                                }
                                                Button {
                                                    text: "ⓘ"
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
                                    radius: 0
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
                                            font.family: "Consolas"
                                            font.letterSpacing: 1.1
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
                                            property int decisiveGames: controller.evalLiveP1Wins + controller.evalLiveP2Wins
                                            property real p1Share: decisiveGames > 0 ? (controller.evalLiveP1Wins / decisiveGames) : 0.5
                                            property real p2Share: decisiveGames > 0 ? (controller.evalLiveP2Wins / decisiveGames) : 0.5
                                            property real drawShare: controller.evalLiveGamesDone > 0 ? (controller.evalLiveDraws / controller.evalLiveGamesDone) : 0.0
                                            Layout.fillWidth: true
                                            Layout.preferredHeight: Math.round(22 * root.uiScale)
                                            radius: height / 2
                                            color: "#202a39"
                                            border.color: root.uiBorder
                                            border.width: 1
                                            clip: true

                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.top: parent.top
                                                anchors.bottom: parent.bottom
                                                width: parent.width * Math.max(0.0, Math.min(1.0, snapshotTrack.p1Share))
                                                gradient: Gradient {
                                                    orientation: Gradient.Horizontal
                                                    GradientStop { position: 0.0; color: "#1f4ea8" }
                                                    GradientStop { position: 0.7; color: "#2f6ed8" }
                                                    GradientStop { position: 1.0; color: "#6fb2ff" }
                                                }
                                                radius: parent.radius
                                                Behavior on width {
                                                    NumberAnimation { duration: 260; easing.type: Easing.InOutCubic }
                                                }
                                                Rectangle {
                                                    anchors.left: parent.left
                                                    anchors.right: parent.right
                                                    anchors.top: parent.top
                                                    height: Math.max(1, Math.round(2 * root.uiScale))
                                                    color: "#00ffffff"
                                                }
                                                Rectangle {
                                                    anchors.fill: parent
                                                    radius: parent.radius
                                                    color: "#10000000"
                                                }
                                                Rectangle {
                                                    anchors.left: parent.left
                                                    anchors.top: parent.top
                                                    anchors.bottom: parent.bottom
                                                    width: Math.max(0, parent.width - Math.round(2 * root.uiScale))
                                                    visible: snapshotTrack.p1Share >= 0.6
                                                    radius: parent.radius
                                                    color: "#00ffffff"
                                                    opacity: 0.0
                                                    SequentialAnimation on opacity {
                                                        running: controller.running && snapshotTrack.p1Share >= 0.6
                                                        loops: Animation.Infinite
                                                        NumberAnimation { from: 0.0; to: 0.18; duration: 600; easing.type: Easing.InOutQuad }
                                                        NumberAnimation { from: 0.18; to: 0.0; duration: 600; easing.type: Easing.InOutQuad }
                                                    }
                                                }
                                            }
                                            Rectangle {
                                                anchors.right: parent.right
                                                anchors.top: parent.top
                                                anchors.bottom: parent.bottom
                                                width: parent.width * Math.max(0.0, Math.min(1.0, snapshotTrack.p2Share))
                                                gradient: Gradient {
                                                    orientation: Gradient.Horizontal
                                                    GradientStop { position: 0.0; color: "#ff8c8c" }
                                                    GradientStop { position: 0.3; color: "#cf3f3f" }
                                                    GradientStop { position: 1.0; color: "#9d1e1e" }
                                                }
                                                radius: parent.radius
                                                Behavior on width {
                                                    NumberAnimation { duration: 260; easing.type: Easing.InOutCubic }
                                                }
                                                Rectangle {
                                                    anchors.left: parent.left
                                                    anchors.right: parent.right
                                                    anchors.top: parent.top
                                                    height: Math.max(1, Math.round(2 * root.uiScale))
                                                    color: "#00ffffff"
                                                }
                                                Rectangle {
                                                    anchors.fill: parent
                                                    radius: parent.radius
                                                    color: "#10000000"
                                                }
                                                Rectangle {
                                                    anchors.right: parent.right
                                                    anchors.top: parent.top
                                                    anchors.bottom: parent.bottom
                                                    width: Math.max(0, parent.width - Math.round(2 * root.uiScale))
                                                    visible: snapshotTrack.p2Share >= 0.6
                                                    radius: parent.radius
                                                    color: "#00ffffff"
                                                    opacity: 0.0
                                                    SequentialAnimation on opacity {
                                                        running: controller.running && snapshotTrack.p2Share >= 0.6
                                                        loops: Animation.Infinite
                                                        NumberAnimation { from: 0.0; to: 0.16; duration: 620; easing.type: Easing.InOutQuad }
                                                        NumberAnimation { from: 0.16; to: 0.0; duration: 620; easing.type: Easing.InOutQuad }
                                                    }
                                                }
                                            }

                                            Rectangle {
                                                anchors.verticalCenter: parent.verticalCenter
                                                x: Math.round((parent.width - width) / 2)
                                                width: Math.max(2, Math.round(2 * root.uiScale))
                                                height: Math.round(parent.height * 0.9)
                                                radius: width / 2
                                                color: "#66dce6ff"
                                            }

                                            Rectangle {
                                                width: Math.round(16 * root.uiScale)
                                                height: width
                                                radius: width / 2
                                                anchors.verticalCenter: parent.verticalCenter
                                                x: Math.max(0, Math.min(parent.width - width,
                                                    parent.width * Math.max(0.0, Math.min(1.0, snapshotTrack.p1Share)) - width / 2))
                                                color: "#40fff5c2"
                                                border.width: 1
                                                border.color: "#88ffe3a8"
                                                visible: controller.evalLiveGamesDone > 0
                                                opacity: 0.75
                                                Behavior on x {
                                                    NumberAnimation { duration: 260; easing.type: Easing.InOutCubic }
                                                }
                                                SequentialAnimation on opacity {
                                                    running: controller.running && controller.evalLiveGamesDone > 0
                                                    loops: Animation.Infinite
                                                    NumberAnimation { from: 0.45; to: 0.85; duration: 520; easing.type: Easing.InOutQuad }
                                                    NumberAnimation { from: 0.85; to: 0.45; duration: 520; easing.type: Easing.InOutQuad }
                                                }
                                            }
                                        }

                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingSm
                                            Text {
                                                text: "P1 " + Math.round(snapshotTrack.p1Share * 100) + "%"
                                                color: root.p1Accent
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                            }
                                            Item { Layout.fillWidth: true }
                                            Text {
                                                text: "P2 " + Math.round(snapshotTrack.p2Share * 100) + "%"
                                                color: root.p2Accent
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                            }
                                        }

                                        Rectangle {
                                            Layout.fillWidth: true
                                            Layout.preferredHeight: Math.max(2, Math.round(3 * root.uiScale))
                                            radius: height / 2
                                            color: root.uiBorder
                                            clip: true
                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.top: parent.top
                                                anchors.bottom: parent.bottom
                                                width: parent.width * Math.max(0.0, Math.min(1.0, snapshotTrack.drawShare))
                                                radius: parent.radius
                                                color: "#9ca3af"
                                            }
                                        }

                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingSm
                                            Text {
                                                text: "Счет: P1 " + controller.evalLiveP1Wins + " • P2 " + controller.evalLiveP2Wins + " • Ничьи " + controller.evalLiveDraws
                                                color: root.uiTextMuted
                                                font.pixelSize: root.evalCaptionSize
                                                font.family: "Consolas"
                                            }
                                            Item { Layout.fillWidth: true }
                                        }

                                        RowLayout {
                                            Layout.fillWidth: true
                                            spacing: root.spacingSm
                                            Text {
                                                text: controller.evalLiveProgressText + " • " + controller.evalLiveStatusText
                                                color: root.uiTextMuted
                                                font.pixelSize: root.evalCaptionSize
                                            }
                                            Item { Layout.fillWidth: true }
                                            Text {
                                                text: "D: " + controller.evalLiveDraws + " (" + Math.round(snapshotTrack.drawShare * 100) + "%)"
                                                color: "#6b7280"
                                                font.pixelSize: root.evalCaptionSize
                                            }
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

                                ChamferPanel {
                                    Layout.fillWidth: true
                                    fillColor: root.bgElevated
                                    borderColor: root.uiBorder
                                    borderWidth: 1
                                    cutSize: Math.round(10 * root.uiScale)
                                    contentMargin: 0
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
                                            radius: 0
                                            color: root.borderMuted
                                            clip: true
                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.top: parent.top
                                                anchors.bottom: parent.bottom
                                                width: parent.width * (controller.evalLiveGamesTotal > 0
                                                    ? Math.max(0.0, Math.min(1.0, controller.evalLiveGamesDone / controller.evalLiveGamesTotal))
                                                    : 0.0)
                                                radius: 0
                                                color: controller.running ? root.p1Accent : "#9aa9c6"
                                            }
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: root.spacingMd

                                    Button {
                                        text: "⚙ АКТИВИРОВАТЬ ОЦЕНКУ"
                                        enabled: !controller.running && controller.evalLaunchReady
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: Math.round(root.actionButtonMinWidth * 1.35)
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.enabled ? "#151102" : "#6a6347"
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: ChamferPanel {
                                            cutSize: Math.round(6 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: parent.pressed
                                                ? "#d7a719"
                                                : parent.hovered
                                                    ? "#e8b932"
                                                    : "#b88a26"
                                            borderWidth: 1
                                            borderColor: parent.hovered ? "#ffe08a" : "#8f6b1f"
                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.right: parent.right
                                                anchors.top: parent.top
                                                height: Math.max(1, Math.round(2 * root.uiScale))
                                                color: "#66fff4bf"
                                            }
                                        }
                                        onClicked: controller.start_eval()
                                    }

                                    Button {
                                        text: "■ ОСТАНОВИТЬ"
                                        enabled: controller.running
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        Layout.rightMargin: Math.round(16 * root.uiScale)
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.enabled ? "#d1d5db" : "#9ca3af"
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: ChamferPanel {
                                            cutSize: Math.round(6 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: parent.enabled
                                                ? (parent.hovered ? "#4a2c2c" : "#2e2f33")
                                                : "#2a2c31"
                                            borderWidth: 1
                                            borderColor: parent.enabled ? "#b88a26" : "#4f545f"
                                        }
                                        onClicked: controller.stop_process()
                                    }

                                    Item { Layout.fillWidth: true }

                                    Button {
                                        text: "⟳ ОБНОВИТЬ"
                                        enabled: !controller.running
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.enabled ? "#d5b15a" : "#737b8a"
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: ChamferPanel {
                                            cutSize: Math.round(6 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: parent.hovered ? "#25303d" : "transparent"
                                            borderWidth: 1
                                            borderColor: parent.hovered ? "#e1be68" : "#b88a26"
                                        }
                                        onClicked: controller.refresh_eval_agents()
                                    }

                                    Button {
                                        text: "⌫ ОЧИСТИТЬ"
                                        enabled: !controller.running
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.enabled ? "#d5b15a" : "#737b8a"
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: ChamferPanel {
                                            cutSize: Math.round(6 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: parent.hovered ? "#25303d" : "transparent"
                                            borderWidth: 1
                                            borderColor: parent.hovered ? "#e1be68" : "#b88a26"
                                        }
                                        onClicked: controller.clear_eval_log()
                                    }

                                    Button {
                                        text: "◉ ДЕТАЛИ"
                                        Layout.preferredHeight: root.actionButtonHeight
                                        Layout.preferredWidth: root.actionButtonMinWidth
                                        contentItem: Text {
                                            text: parent.text
                                            color: "#d5b15a"
                                            font.bold: true
                                            font.pixelSize: root.evalCaptionSize
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: ChamferPanel {
                                            cutSize: Math.round(6 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: parent.hovered ? "#25303d" : "transparent"
                                            borderWidth: 1
                                            borderColor: parent.hovered ? "#e1be68" : "#b88a26"
                                        }
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
                                    color: root.uiTextMain
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
                                    color: root.uiTextMuted
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

                                    ChamferPanel {
                                        Layout.fillWidth: true
                                        fillColor: "#1b2738"
                                        borderColor: "#35557f"
                                        borderWidth: 1
                                        cutSize: Math.round(10 * root.uiScale)
                                        contentMargin: 0
                                        implicitHeight: edgeCard.implicitHeight + root.spacingMd * 2
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
                                            RowLayout {
                                                Layout.fillWidth: true
                                                spacing: Math.round(2 * root.uiScale)
                                                Repeater {
                                                    model: 11
                                                    delegate: Rectangle {
                                                        Layout.fillWidth: true
                                                        implicitHeight: 2
                                                        color: index === 5 ? "#6f95cf" : "#3d5270"
                                                        opacity: 0.75
                                                    }
                                                }
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

                                    ChamferPanel {
                                        Layout.fillWidth: true
                                        fillColor: root.uiBgCard
                                        borderColor: "#7a6430"
                                        borderWidth: 1
                                        cutSize: Math.round(10 * root.uiScale)
                                        contentMargin: 0
                                        implicitHeight: confidenceCard.implicitHeight + root.spacingMd * 2
                                        ColumnLayout {
                                            id: confidenceCard
                                            anchors.fill: parent
                                            anchors.margins: root.spacingMd
                                            spacing: Math.round(4 * root.uiScale)
                                            Text {
                                                text: "Надежность"
                                                color: root.uiTextMuted
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
                                                color: root.uiTextMuted
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

                                    ChamferPanel {
                                        Layout.fillWidth: true
                                        fillColor: "#2a1f22"
                                        borderColor: "#8d4a4a"
                                        borderWidth: 1
                                        cutSize: Math.round(10 * root.uiScale)
                                        contentMargin: 0
                                        implicitHeight: scoreCard.implicitHeight + root.spacingMd * 2
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
                                                font.pixelSize: Math.round(28 * root.uiScale)
                                                font.family: "Consolas"
                                                horizontalAlignment: Text.AlignHCenter
                                                Layout.fillWidth: true
                                                style: Text.Outline
                                                styleColor: "#302838"
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
                        color: root.bgElevated
                        border.color: root.uiBorder
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
                                    color: root.uiTextMain
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
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "ИИ, который учится понимать, какой ход выгоднее в текущей ситуации. Для каждого действия он оценивает ожидаемую пользу и выбирает лучший вариант."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "запоминает прошлые ситуации (состояние, действие, результат), потом на этих данных постепенно улучшает оценки действий. Со временем реже ошибается и лучше выбирает ходы в похожих сценариях."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• понятная логика выбора хода;\n• хорошее качество игры после обучения;\n• удобно сравнивать с PPO/AZ/GMZ;\n• обычно предсказуемое поведение в повторяющихся ситуациях;\n• подходит как надежный базовый агент для тестов и долгих прогонов."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• может учиться дольше PPO;\n• чувствителен к настройкам;\n• требует больше вычислений при тренировке;\n• качество сильно зависит от того, насколько удачно подобраны гиперпараметры;\n• в очень сложной тактике может хуже справляться, чем модели с полноценным поиском (MCTS/Search)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
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
                        color: root.bgElevated
                        border.color: root.uiBorder
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
                                    color: root.uiTextMain
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
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "ИИ, который учится напрямую улучшать стратегию выбора действий. Он не просто оценивает отдельные ходы, а постепенно делает всю политику игры более качественной."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "играет серии шагов (rollout), оценивает, какие решения были полезными, и обновляет стратегию небольшими безопасными шагами, чтобы не ломать уже выученное поведение."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• обычно стабильно обучается;\n• хороший баланс между скоростью обучения и качеством;\n• удобен как рабочий режим по умолчанию;\n• часто быстрее и предсказуемее в настройке, чем сложные search-модели;\n• подходит для длительных тренировок без сильных скачков поведения."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• не использует поиск по дереву на каждом ходе;\n• в сложной тактике может уступать AZ/GMZ с MCTS/Search;\n• качество зависит от rollout/epoch/minibatch настроек;\n• иногда требует тонкой подстройки коэффициентов (clip, entropy, value loss)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
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
                        color: root.bgElevated
                        border.color: root.uiBorder
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
                                    color: root.uiTextMain
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
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "ИИ, который сочетает нейросеть и поиск по дереву (MCTS). Нейросеть подсказывает хорошие направления, а MCTS просчитывает варианты вперед и помогает выбрать более сильный ход."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "играет self-play матчи, накапливает позиции и улучшает сеть так, чтобы она лучше оценивала ходы и состояния, опираясь на результаты поиска."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• сильная тактическая игра за счёт просчета вперед;\n• лучше учитывает последствия на несколько ходов;\n• часто заметно усиливается при росте search-бюджета;\n• хорошо подходит для eval/viewer, где важна сила решений."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• медленнее на инференсе из-за MCTS;\n• требует больше CPU/GPU ресурсов;\n• чувствителен к настройкам поиска (simulations, c_puct, temperature);\n• при слишком малом search-бюджете может терять преимущество."
                                }
                                Label {
                                    text: "Режимы инференса"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• Greedy — быстро, без поиска;\n• MCTS — сильнее, но медленнее."
                                }
                                Label {
                                    text: "Температура"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "влияет только в MCTS (в Greedy не используется)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
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
                        color: root.bgElevated
                        border.color: root.uiBorder
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
                                    color: root.uiTextMain
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
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "ИИ с поиском, который дополнительно использует внутреннюю модель динамики. Проще: он не только выбирает ход, но и внутри модели проигрывает возможное будущее."
                                }
                                Label {
                                    text: "Как учится"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "через self-play и unroll-обучение: representation/dynamics/prediction блоки совместно учатся лучше моделировать состояние, последствия действий и полезность решений."
                                }
                                Label {
                                    text: "Сильные стороны"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• высокий потолок качества игры;\n• хорошо работает в сложных и длинных тактических сценариях;\n• search-режим часто дает сильные решения в eval/viewer;\n• мощный инструмент, когда цель — выжать максимум качества."
                                }
                                Label {
                                    text: "Ограничения"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• самый тяжелый режим по вычислениям;\n• дольше тренируется и сложнее в тюнинге;\n• чувствителен к параметрам search/replay/unroll;\n• при малом compute может не раскрывать потенциал полностью."
                                }
                                Label {
                                    text: "Режимы инференса"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "• Greedy — быстрее, без search;\n• Search — сильнее, но медленнее."
                                }
                                Label {
                                    text: "Температура"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
                                    text: "влияет только в Search (в Greedy не используется)."
                                }
                                Label {
                                    text: "Когда выбирать"
                                    font.bold: true
                                    font.pixelSize: Math.round(12 * root.uiScale)
                                    color: root.uiTextMain
                                    Layout.fillWidth: true
                                }
                                Label {
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    color: root.uiTextMuted
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
