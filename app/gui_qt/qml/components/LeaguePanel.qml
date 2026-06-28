// app/gui_qt/qml/components/LeaguePanel.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

Item {
    id: leaguePanel

    function _fmtFloat(val, dec) {
        if (val === undefined || val === null || isNaN(Number(val)))
            return "—"
        return Number(val).toFixed(dec !== undefined ? dec : 2)
    }

    function _fmtPct(val) {
        if (val === undefined || val === null || isNaN(Number(val)))
            return "—"
        return _fmtFloat(Number(val) * 100, 1) + "%"
    }

    function _rebuildOpponentsModel() {
        opponentsModel.clear()
        var payload = controller.opponentPoolState || {}
        var opps = payload.opponents || {}
        var keys = Object.keys(opps)
        keys.sort(function(a, b) {
            var ga = Number((opps[a] || {}).games || 0)
            var gb = Number((opps[b] || {}).games || 0)
            return gb - ga
        })
        for (var i = 0; i < keys.length; i++) {
            var aid = keys[i]
            var stat = opps[aid] || {}
            var games = Number(stat.games || 0)
            var wr = stat.ema_winrate
            var prob = stat.prob
            opponentsModel.append({
                agent_id: aid,
                games: games,
                winrate: (wr !== undefined && wr !== null) ? _fmtFloat(wr, 2) : "—",
                prob: (prob !== undefined && prob !== null) ? _fmtFloat(prob, 2) : "—",
                reason: stat.reason ? String(stat.reason) : ""
            })
        }
    }

    Connections {
        target: controller
        function onOpponentPoolStateChanged() {
            leaguePanel._rebuildOpponentsModel()
        }
    }

    Component.onCompleted: _rebuildOpponentsModel()

    ListModel { id: opponentsModel }

    ScrollView {
        anchors.fill: parent
        clip: true

        ColumnLayout {
            width: leaguePanel.width
            anchors.margins: root.spacingLg
            spacing: root.spacingMd

            Text {
                text: "Лига / Opponent Pool"
                font.pixelSize: Math.round(20 * root.uiScale)
                font.bold: true
                color: root.uiTextMain
                font.family: root.fontUiFamily
            }

            Text {
                text: "PFSP-сэмплинг оппонентов: эвристика-анкер + последние снапшоты модели"
                font.pixelSize: root.evalCaptionSize
                color: root.uiTextMuted
                Layout.bottomMargin: root.spacingSm
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }

            ChamferPanel {
                Layout.fillWidth: true
                fillColor: root.uiBgCard
                borderColor: root.uiBorder
                borderWidth: 1
                cutSize: Math.round(10 * root.uiScale)
                contentMargin: root.spacingMd
                implicitHeight: settingsCol.implicitHeight + root.spacingMd * 2

                ColumnLayout {
                    id: settingsCol
                    width: parent.width
                    spacing: root.spacingMd

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: root.spacingMd

                        TacticalCheckBox {
                            text: "Включить пул оппонентов"
                            scaleRef: root.uiScale
                            labelFontFamily: root.fontUiFamily
                            labelFontSize: root.evalCaptionSize
                            labelColorEnabled: root.uiTextMain
                            checked: controller.poolEnabled
                            enabled: !controller.running
                            onToggled: controller.set_pool_enabled(checked)
                        }

                        Item { Layout.fillWidth: true }

                        Label {
                            text: "Стратегия:"
                            font.bold: true
                            color: root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                        }

                        ButtonGroup { id: strategyGroup }

                        RadioButton {
                            text: "PFSP"
                            checked: controller.poolStrategy === "pfsp"
                            enabled: !controller.running
                            ButtonGroup.group: strategyGroup
                            font.pixelSize: root.evalCaptionSize
                            onClicked: controller.set_pool_strategy("pfsp")
                        }
                        RadioButton {
                            text: "Uniform"
                            checked: controller.poolStrategy === "uniform"
                            enabled: !controller.running
                            ButtonGroup.group: strategyGroup
                            font.pixelSize: root.evalCaptionSize
                            onClicked: controller.set_pool_strategy("uniform")
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: root.spacingSm
                        Label {
                            text: "Доля игр против эвристики (p_heuristic)"
                            color: root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                            Layout.preferredWidth: Math.round(280 * root.uiScale)
                            wrapMode: Text.WordWrap
                        }
                        Slider {
                            Layout.fillWidth: true
                            from: 0.0
                            to: 1.0
                            stepSize: 0.01
                            value: controller.poolPHeuristic
                            enabled: !controller.running
                            onMoved: controller.set_pool_p_heuristic(value)
                        }
                        Label {
                            text: leaguePanel._fmtFloat(controller.poolPHeuristic, 2)
                            color: root.uiTextMain
                            font.family: root.fontDataFamily
                            font.pixelSize: root.evalCaptionSize
                            Layout.preferredWidth: Math.round(44 * root.uiScale)
                            horizontalAlignment: Text.AlignRight
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: root.spacingSm
                        Label {
                            text: "Размер пула (последних снапшотов)"
                            color: root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                            Layout.preferredWidth: Math.round(280 * root.uiScale)
                        }
                        SpinBox {
                            from: 1
                            to: 32
                            stepSize: 1
                            editable: true
                            value: controller.poolSize
                            enabled: !controller.running
                            onValueModified: controller.set_pool_size(value)
                        }
                        Item { Layout.fillWidth: true }
                    }

                    ExpanderSection {
                        Layout.fillWidth: true
                        title: "Advanced"
                        expanded: false
                        uiScale: root.uiScale
                        captionSize: root.evalCaptionSize
                        textMain: root.uiTextMain
                        textMuted: root.uiTextMuted
                        panelFill: root.bgElevated
                        panelBorder: root.uiBorder

                        GridLayout {
                            width: parent.width
                            columns: 2
                            columnSpacing: root.spacingMd
                            rowSpacing: root.spacingSm

                            Label { text: "PFSP power"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                            TextField {
                                Layout.fillWidth: true
                                text: String(controller.poolPfspPower)
                                enabled: !controller.running
                                font.family: root.fontDataFamily
                                background: Rectangle {
                                    radius: 0
                                    color: parent.enabled ? "#253244" : "#202734"
                                    border.width: 1
                                    border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                }
                                onEditingFinished: controller.set_pool_pfsp_power(parseFloat(text))
                            }

                            Label { text: "Uniform floor"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                            TextField {
                                Layout.fillWidth: true
                                text: String(controller.poolUniformFloor)
                                enabled: !controller.running
                                font.family: root.fontDataFamily
                                background: Rectangle {
                                    radius: 0
                                    color: parent.enabled ? "#253244" : "#202734"
                                    border.width: 1
                                    border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                }
                                onEditingFinished: controller.set_pool_uniform_floor(parseFloat(text))
                            }

                            Label { text: "Novelty bonus"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                            TextField {
                                Layout.fillWidth: true
                                text: String(controller.poolNoveltyBonus)
                                enabled: !controller.running
                                font.family: root.fontDataFamily
                                background: Rectangle {
                                    radius: 0
                                    color: parent.enabled ? "#253244" : "#202734"
                                    border.width: 1
                                    border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                }
                                onEditingFinished: controller.set_pool_novelty_bonus(parseFloat(text))
                            }

                            Label { text: "Min games (PFSP)"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                            TextField {
                                Layout.fillWidth: true
                                text: String(controller.poolMinGames)
                                enabled: !controller.running
                                font.family: root.fontDataFamily
                                background: Rectangle {
                                    radius: 0
                                    color: parent.enabled ? "#253244" : "#202734"
                                    border.width: 1
                                    border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                }
                                onEditingFinished: controller.set_pool_min_games(parseInt(text))
                            }

                            Label { text: "EMA α"; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                            TextField {
                                Layout.fillWidth: true
                                text: String(controller.poolEmaAlpha)
                                enabled: !controller.running
                                font.family: root.fontDataFamily
                                background: Rectangle {
                                    radius: 0
                                    color: parent.enabled ? "#253244" : "#202734"
                                    border.width: 1
                                    border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                }
                                onEditingFinished: controller.set_pool_ema_alpha(parseFloat(text))
                            }
                        }
                    }
                }
            }

            ChamferPanel {
                Layout.fillWidth: true
                Layout.preferredHeight: Math.max(Math.round(220 * root.uiScale), liveCol.implicitHeight + root.spacingMd * 2)
                fillColor: root.uiBgCard
                borderColor: root.uiBorder
                borderWidth: 1
                cutSize: Math.round(10 * root.uiScale)
                contentMargin: root.spacingMd

                ColumnLayout {
                    id: liveCol
                    width: parent.width
                    spacing: root.spacingSm

                    Text {
                        text: "Состояние пула (live)"
                        font.bold: true
                        font.pixelSize: root.evalSectionTitleSize
                        color: root.uiTextMain
                        font.family: root.fontUiFamily
                        font.capitalization: Font.AllUppercase
                        font.letterSpacing: 0.8
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: root.spacingMd
                        Label {
                            text: "Записей: " + opponentsModel.count
                            color: root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                        }
                        Label {
                            text: controller.poolEnabled ? "Пул: вкл" : "Пул: выкл"
                            color: controller.poolEnabled ? "#4caf6e" : root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                            font.bold: true
                        }
                        Label {
                            text: "Стратегия: " + (controller.poolStrategy === "uniform" ? "Uniform" : "PFSP")
                            color: root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                        }
                        Label {
                            text: "p_heur: " + leaguePanel._fmtFloat(controller.poolPHeuristic, 2)
                            color: root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                        }
                        Label {
                            text: "размер: " + controller.poolSize
                            color: root.uiTextMuted
                            font.pixelSize: root.evalCaptionSize
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 1
                        color: root.uiBorder
                    }

                    GridLayout {
                        Layout.fillWidth: true
                        columns: 5
                        columnSpacing: root.spacingSm
                        rowSpacing: root.spacingXs

                        Repeater {
                            model: ["agent_id", "games", "winrate", "P(выбора)", "reason"]
                            delegate: Text {
                                text: modelData
                                font.bold: true
                                font.pixelSize: root.evalCaptionSize
                                color: root.uiTextMuted
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                        }
                    }

                    ListView {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Math.min(
                            Math.round(280 * root.uiScale),
                            Math.max(Math.round(48 * root.uiScale), opponentsModel.count * Math.round(28 * root.uiScale))
                        )
                        clip: true
                        spacing: root.spacingXs
                        model: opponentsModel
                        delegate: GridLayout {
                            width: ListView.view.width
                            columns: 5
                            columnSpacing: root.spacingSm

                            Text {
                                text: model.agent_id
                                color: root.uiTextMain
                                font.pixelSize: root.evalCaptionSize
                                font.family: root.fontDataFamily
                                Layout.fillWidth: true
                                elide: Text.ElideMiddle
                            }
                            Text {
                                text: model.games
                                color: root.uiTextMain
                                font.pixelSize: root.evalCaptionSize
                                font.family: root.fontDataFamily
                            }
                            Text {
                                text: model.winrate
                                color: root.uiTextMain
                                font.pixelSize: root.evalCaptionSize
                                font.family: root.fontDataFamily
                            }
                            Text {
                                text: model.prob
                                color: root.uiTextMain
                                font.pixelSize: root.evalCaptionSize
                                font.family: root.fontDataFamily
                            }
                            Text {
                                text: model.reason || "—"
                                color: root.uiTextMuted
                                font.pixelSize: root.evalCaptionSize
                                Layout.fillWidth: true
                                elide: Text.ElideRight
                            }
                        }
                    }

                    Text {
                        visible: opponentsModel.count === 0
                        text: "Нет данных пула — stats появятся после train с источником «ПУЛ / ЛИГА»."
                        color: root.uiTextMuted
                        font.pixelSize: root.evalCaptionSize
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}
