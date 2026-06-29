// app/gui_qt/qml/components/LeaguePanel.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

Item {
    id: leaguePanel

    readonly property real _colId: Math.round(190 * root.uiScale)
    readonly property real _colAlgo: Math.round(44 * root.uiScale)
    readonly property real _colAge: Math.round(58 * root.uiScale)
    readonly property real _colNum: Math.round(58 * root.uiScale)
    readonly property real _colWr: Math.round(108 * root.uiScale)
    readonly property real _colProb: Math.round(118 * root.uiScale)
    readonly property real _colWdl: Math.round(82 * root.uiScale)
    readonly property real _colUpdated: Math.round(112 * root.uiScale)
    readonly property real _colReason: Math.round(64 * root.uiScale)
    readonly property real _colPool: Math.round(36 * root.uiScale)
    readonly property real _tableWidth: _colId + _colAlgo + _colAge + _colNum * 4 + _colWr + _colProb * 3 + _colWdl + _colReason + root.spacingSm * 12
    readonly property real _historyTableWidth: _colId + _colAlgo + _colPool + _colAge + _colNum * 3 + _colWr + _colWdl + _colUpdated + root.spacingSm * 9
    readonly property real _rowH: Math.round(26 * root.uiScale)

    property var poolContext: ({})
    property var heuristicState: ({})

    function _fmtFloat(val, dec) {
        if (val === undefined || val === null || isNaN(Number(val)))
            return "—"
        return Number(val).toFixed(dec !== undefined ? dec : 2)
    }

    function _fmtPct(val) {
        if (val === undefined || val === null || isNaN(Number(val)) || Number(val) < 0)
            return "—"
        return _fmtFloat(Number(val) * 100, 1) + "%"
    }

    function _fmtSigned(val, dec) {
        if (val === undefined || val === null || isNaN(Number(val)))
            return "—"
        var n = Number(val)
        var sign = n > 0 ? "+" : ""
        return sign + n.toFixed(dec !== undefined ? dec : 2)
    }

    function _reasonBadge(reason) {
        var r = String(reason || "").toLowerCase()
        if (r === "novelty") return "novelty"
        if (r === "pfsp") return "pfsp"
        if (r === "uniform_floor") return "uniform"
        if (r.indexOf("heur") >= 0) return "anchor"
        return r || "—"
    }

    function _algoColor(algo) {
        var a = String(algo || "").toUpperCase()
        if (a === "PPO") return "#4a9fd4"
        if (a === "DQN") return "#b88a26"
        if (a === "AZ" || a === "AZP") return "#9b59b6"
        if (a === "GAZ") return "#e67e22"
        if (a === "GMZ") return "#1abc9c"
        if (a === "SMZ") return "#3498db"
        return root.uiTextMuted
    }

    function _fmtEp(val) {
        var ep = Number(val)
        if (isNaN(ep) || ep < 0)
            return "—"
        return String(ep)
    }

    function _fmtWdl(wins, draws, losses) {
        return Number(wins || 0) + "/" + Number(draws || 0) + "/" + Number(losses || 0)
    }

    function _rebuildFromState() {
        var payload = controller.opponentPoolState || {}
        poolContext = payload.context || {}
        heuristicState = payload.heuristic || {}

        candidatesModel.clear()
        var cands = payload.candidates || []
        for (var ci = 0; ci < cands.length; ci++) {
            var c = cands[ci] || {}
            candidatesModel.append({
                label: c.label || c.agent_id || "—",
                agent_id: c.agent_id || "",
                algo: c.algo_short || c.algo || "?",
                age: c.age || "—",
                games: Number(c.games || 0),
                winrate: leaguePanel._fmtPct(c.winrate),
                draw_pct: leaguePanel._fmtPct(c.draw_pct),
                vp_per_game: leaguePanel._fmtSigned(c.vp_per_game, 2),
                prob_snapshot: leaguePanel._fmtPct(c.prob_snapshot),
                prob_episode: leaguePanel._fmtPct(c.prob_episode),
                run_games: Number(c.run_games || 0),
                run_actual: leaguePanel._fmtPct(c.run_actual_prob),
                run_wdl: leaguePanel._fmtWdl(c.run_wins, c.run_draws, c.run_losses),
                reason: leaguePanel._reasonBadge(c.reason),
                created_at: c.created_at || "",
                updated_at: c.updated_at || ""
            })
        }

        historyModel.clear()
        var hist = payload.history || []
        for (var hi = 0; hi < hist.length; hi++) {
            var h = hist[hi] || {}
            historyModel.append({
                label: h.label || h.agent_id || "—",
                agent_id: h.agent_id || "",
                algo: h.algo_short || h.algo || "?",
                in_pool: h.in_pool === true,
                age: h.age || "—",
                games: Number(h.games || 0),
                winrate: leaguePanel._fmtPct(h.winrate),
                draw_pct: leaguePanel._fmtPct(h.draw_pct),
                vp_per_game: leaguePanel._fmtSigned(h.vp_per_game, 2),
                wdl: leaguePanel._fmtWdl(h.wins, h.tracked_draws, h.losses)
                     + (Number(h.unclassified_games || 0) > 0 ? (" +?" + Number(h.unclassified_games)) : ""),
                created_at: h.created_at || "",
                updated_at: h.updated_at || "—"
            })
        }

        trainLiveModel.clear()
        var live = payload.train_live || []
        for (var li = 0; li < live.length; li++) {
            var row = live[li] || {}
            trainLiveModel.append({
                text: row.text || "",
                kind: row.kind || "info"
            })
        }
    }

    Connections {
        target: controller
        function onOpponentPoolStateChanged() {
            leaguePanel._rebuildFromState()
        }
    }

    Component.onCompleted: _rebuildFromState()

    ListModel { id: candidatesModel }
    ListModel { id: historyModel }
    ListModel { id: trainLiveModel }

    component HelpLabel: Label {
        property string labelText: ""
        property string helpText: ""
        text: labelText + "  ⓘ"
        color: helpMouse.containsMouse ? root.uiTextMain : root.uiTextMuted
        font.pixelSize: root.evalCaptionSize
        ToolTip.visible: helpMouse.containsMouse
        ToolTip.text: helpText
        ToolTip.delay: 250
        ToolTip.timeout: 12000
        MouseArea {
            id: helpMouse
            anchors.fill: parent
            hoverEnabled: true
            acceptedButtons: Qt.NoButton
        }
    }

    component CandidateTableHeader: RowLayout {
        width: leaguePanel._tableWidth
        spacing: root.spacingSm
        Repeater {
            model: [
                { label: "ID", w: leaguePanel._colId, fill: true },
                { label: "Algo", w: leaguePanel._colAlgo, fill: false },
                { label: "Возраст", w: leaguePanel._colAge, fill: false },
                { label: "Games", w: leaguePanel._colNum, fill: false },
                { label: "EMA WR learner", w: leaguePanel._colWr, fill: false },
                { label: "Draw%", w: leaguePanel._colNum, fill: false },
                { label: "VP/ep", w: leaguePanel._colNum, fill: false },
                { label: "P среди снапшотов", w: leaguePanel._colProb, fill: false },
                { label: "P эпизода", w: leaguePanel._colProb, fill: false },
                { label: "Run игр", w: leaguePanel._colNum, fill: false },
                { label: "Факт.", w: leaguePanel._colProb, fill: false },
                { label: "Run W/D/L", w: leaguePanel._colWdl, fill: false },
                { label: "Reason", w: leaguePanel._colReason, fill: false }
            ]
            delegate: Text {
                text: modelData.label
                font.bold: true
                font.pixelSize: root.evalCaptionSize
                color: root.uiTextMuted
                Layout.preferredWidth: modelData.w
                Layout.fillWidth: modelData.fill
                horizontalAlignment: modelData.fill ? Text.AlignLeft : Text.AlignRight
                elide: Text.ElideRight
            }
        }
    }

    component HistoryTableHeader: RowLayout {
        width: leaguePanel._historyTableWidth
        spacing: root.spacingSm
        Repeater {
            model: [
                { label: "Agent", w: leaguePanel._colId, fill: true },
                { label: "Algo", w: leaguePanel._colAlgo, fill: false },
                { label: "Пул", w: leaguePanel._colPool, fill: false },
                { label: "Возраст", w: leaguePanel._colAge, fill: false },
                { label: "Games", w: leaguePanel._colNum, fill: false },
                { label: "EMA WR learner", w: leaguePanel._colWr, fill: false },
                { label: "W/D/L tracked", w: leaguePanel._colWdl, fill: false },
                { label: "Draw%", w: leaguePanel._colNum, fill: false },
                { label: "VP/ep", w: leaguePanel._colNum, fill: false },
                { label: "Stats updated", w: leaguePanel._colUpdated, fill: false }
            ]
            delegate: Text {
                text: modelData.label
                font.bold: true
                font.pixelSize: root.evalCaptionSize
                color: root.uiTextMuted
                Layout.preferredWidth: modelData.w
                Layout.fillWidth: modelData.fill
                horizontalAlignment: modelData.fill ? Text.AlignLeft : Text.AlignRight
                elide: Text.ElideRight
            }
        }
    }

    component CandidateRow: RowLayout {
        property string labelText: ""
        property string agentIdText: ""
        property string algoText: "?"
        property string ageText: "—"
        property int gamesVal: 0
        property string wrText: "—"
        property string drawText: "—"
        property string vpText: "—"
        property string probSnapshotText: "—"
        property string probEpisodeText: "—"
        property int runGamesVal: 0
        property string runActualText: "—"
        property string runWdlText: "0/0/0"
        property string reasonText: "—"
        width: leaguePanel._tableWidth
        spacing: root.spacingSm

        Text {
            id: idCell
            text: labelText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colId
            Layout.fillWidth: true
            elide: Text.ElideMiddle
            ToolTip.visible: idTipMouse.containsMouse && agentIdText.length > 0
            ToolTip.text: agentIdText
            ToolTip.delay: 400
            MouseArea {
                id: idTipMouse
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.NoButton
            }
        }
        Text {
            text: algoText
            color: leaguePanel._algoColor(algoText)
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            font.bold: true
            Layout.preferredWidth: leaguePanel._colAlgo
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: ageText
            color: root.uiTextMuted
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colAge
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: gamesVal
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colNum
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: wrText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colWr
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: drawText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colNum
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: vpText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colNum
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: probSnapshotText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colProb
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: probEpisodeText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colProb
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: runGamesVal
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colNum
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: runActualText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colProb
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: runWdlText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colWdl
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: reasonText
            color: reasonText === "novelty" ? "#e6a23c"
                 : (reasonText === "pfsp" ? "#4caf6e" : root.uiTextMuted)
            font.pixelSize: root.evalCaptionSize
            font.bold: reasonText === "novelty" || reasonText === "pfsp"
            Layout.preferredWidth: leaguePanel._colReason
            horizontalAlignment: Text.AlignRight
        }
    }

    component HistoryRow: RowLayout {
        property string labelText: ""
        property string agentIdText: ""
        property string algoText: "?"
        property bool inPool: false
        property string ageText: "—"
        property int gamesVal: 0
        property string wrText: "—"
        property string wdlText: "—"
        property string drawText: "—"
        property string vpText: "—"
        property string updatedText: "—"
        width: leaguePanel._historyTableWidth
        spacing: root.spacingSm

        Text {
            id: histIdCell
            text: labelText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colId
            Layout.fillWidth: true
            elide: Text.ElideMiddle
            ToolTip.visible: histTipMouse.containsMouse && agentIdText.length > 0
            ToolTip.text: agentIdText
            ToolTip.delay: 400
            MouseArea {
                id: histTipMouse
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.NoButton
            }
        }
        Text {
            text: algoText
            color: leaguePanel._algoColor(algoText)
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            font.bold: true
            Layout.preferredWidth: leaguePanel._colAlgo
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: inPool ? "✓" : "—"
            color: inPool ? "#4caf6e" : root.uiTextMuted
            font.pixelSize: root.evalCaptionSize
            font.bold: inPool
            Layout.preferredWidth: leaguePanel._colPool
            horizontalAlignment: Text.AlignHCenter
        }
        Text {
            text: ageText
            color: root.uiTextMuted
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colAge
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: gamesVal
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colNum
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: wrText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colWr
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: wdlText
            color: wdlText.indexOf("+?") >= 0 ? "#e6a23c" : root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colWdl
            horizontalAlignment: Text.AlignRight
            ToolTip.visible: histWdlMouse.containsMouse && wdlText.indexOf("+?") >= 0
            ToolTip.text: "Игры schema v1 не содержали отдельных W/L; +? — честно не классифицированные старые игры."
            MouseArea {
                id: histWdlMouse
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.NoButton
            }
        }
        Text {
            text: drawText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colNum
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: vpText
            color: root.uiTextMain
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colNum
            horizontalAlignment: Text.AlignRight
        }
        Text {
            text: updatedText
            color: root.uiTextMuted
            font.pixelSize: root.evalCaptionSize
            font.family: root.fontDataFamily
            Layout.preferredWidth: leaguePanel._colUpdated
            horizontalAlignment: Text.AlignRight
        }
    }

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

                            HelpLabel {
                                labelText: "PFSP power"
                                helpText: "Степень в формуле (1 − EMA WR learner)^power. Чем выше значение, тем сильнее пул концентрируется на оппонентах, которым learner чаще проигрывает."
                            }
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

                            HelpLabel {
                                labelText: "Uniform floor"
                                helpText: "Доля равномерной смеси внутри snapshot-ветки. 0.10 означает: 90% распределения даёт PFSP, 10% делятся поровну между всеми снапшотами."
                            }
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

                            HelpLabel {
                                labelText: "Novelty bonus"
                                helpText: "Добавочный вес новым снапшотам, по которым ещё мало игр. Нужен, чтобы быстро собрать первичную статистику и не игнорировать новичка."
                            }
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

                            HelpLabel {
                                labelText: "Min games (PFSP)"
                                helpText: "Сколько игр нужно накопить до перехода от режима novelty к обычному PFSP-весу по EMA WR learner."
                            }
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

                            HelpLabel {
                                labelText: "EMA α"
                                helpText: "Скорость реакции EMA WR на последний результат: новое EMA = (1−α)·старое + α·результат, где win=1, draw=0.5, loss=0."
                            }
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
                Layout.preferredHeight: Math.max(Math.round(320 * root.uiScale), liveCol.implicitHeight + root.spacingMd * 2)
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

                    Flow {
                        Layout.fillWidth: true
                        spacing: root.spacingSm

                        Rectangle {
                            radius: 0
                            color: poolContext.learner_side === "P2" ? "#1a2a33" : "#1a2333"
                            border.color: poolContext.learner_side === "P2" ? "#4a9fd4" : "#b88a26"
                            border.width: 1
                            implicitWidth: chipLearner.implicitWidth + root.spacingSm * 2
                            implicitHeight: chipLearner.implicitHeight + root.spacingXs * 2
                            Text {
                                id: chipLearner
                                anchors.centerIn: parent
                                text: (poolContext.learner_side || controller.learnerSide || "P1") + " learner"
                                      + (poolContext.learner_algo ? (" · " + poolContext.learner_algo) : "")
                                      + (poolContext.learner_faction ? (" · " + poolContext.learner_faction) : "")
                                color: root.uiTextMain
                                font.pixelSize: root.evalCaptionSize
                                font.bold: true
                            }
                        }

                        Rectangle {
                            radius: 0
                            color: poolContext.pool_enabled ? "#142318" : "#1f2430"
                            border.color: poolContext.pool_enabled ? "#4caf6e" : root.uiBorder
                            border.width: 1
                            implicitWidth: chipPool.implicitWidth + root.spacingSm * 2
                            implicitHeight: chipPool.implicitHeight + root.spacingXs * 2
                            Text {
                                id: chipPool
                                anchors.centerIn: parent
                                text: (poolContext.pool_enabled ? "Пул вкл" : "Пул выкл")
                                      + " · " + (poolContext.pool_fill || ("0/" + controller.poolSize))
                                      + (poolContext.registry_opponent_count !== undefined
                                         ? (" · реестр " + poolContext.opponent_side + ": " + poolContext.registry_opponent_count)
                                         : "")
                                color: poolContext.pool_enabled ? "#4caf6e" : root.uiTextMuted
                                font.pixelSize: root.evalCaptionSize
                            }
                        }

                        Rectangle {
                            visible: poolContext.draw_rate !== undefined && Number(poolContext.draw_rate) >= 0
                            radius: 0
                            color: "#2a2418"
                            border.color: "#e6a23c"
                            border.width: 1
                            implicitWidth: chipDraw.implicitWidth + root.spacingSm * 2
                            implicitHeight: chipDraw.implicitHeight + root.spacingXs * 2
                            Text {
                                id: chipDraw
                                anchors.centerIn: parent
                                text: "draw train " + leaguePanel._fmtPct(poolContext.draw_rate)
                                color: "#e6a23c"
                                font.pixelSize: root.evalCaptionSize
                            }
                        }

                        Rectangle {
                            visible: poolContext.mission !== undefined && String(poolContext.mission).length > 0
                            radius: 0
                            color: "#1f2430"
                            border.color: root.uiBorder
                            border.width: 1
                            implicitWidth: chipMission.implicitWidth + root.spacingSm * 2
                            implicitHeight: chipMission.implicitHeight + root.spacingXs * 2
                            Text {
                                id: chipMission
                                anchors.centerIn: parent
                                text: String(poolContext.mission)
                                color: root.uiTextMuted
                                font.pixelSize: root.evalCaptionSize
                            }
                        }

                        Rectangle {
                            visible: poolContext.pool_algo_mix !== undefined && String(poolContext.pool_algo_mix).length > 0
                            radius: 0
                            color: "#1f2430"
                            border.color: root.uiBorder
                            border.width: 1
                            implicitWidth: chipMix.implicitWidth + root.spacingSm * 2
                            implicitHeight: chipMix.implicitHeight + root.spacingXs * 2
                            Text {
                                id: chipMix
                                anchors.centerIn: parent
                                text: "оппоненты: " + String(poolContext.pool_algo_mix)
                                color: root.uiTextMuted
                                font.pixelSize: root.evalCaptionSize
                            }
                        }

                        Rectangle {
                            visible: poolContext.last_pick_label !== undefined && String(poolContext.last_pick_label).length > 0
                            radius: 0
                            color: "#1a2333"
                            border.color: "#4a9fd4"
                            border.width: 1
                            implicitWidth: chipLast.implicitWidth + root.spacingSm * 2
                            implicitHeight: chipLast.implicitHeight + root.spacingXs * 2
                            Text {
                                id: chipLast
                                anchors.centerIn: parent
                                text: "последний [POOL]: " + String(poolContext.last_pick_label)
                                      + (poolContext.last_pick_reason ? (" · " + poolContext.last_pick_reason) : "")
                                      + (poolContext.last_pick_result ? (" · " + poolContext.last_pick_result) : "")
                                      + (poolContext.last_pick_at ? (" · " + poolContext.last_pick_at) : "")
                                color: "#4a9fd4"
                                font.pixelSize: root.evalCaptionSize
                            }
                        }

                        Rectangle {
                            visible: poolContext.train_running === true
                            radius: 0
                            color: "#142318"
                            border.color: "#4caf6e"
                            border.width: 1
                            implicitWidth: chipRun.implicitWidth + root.spacingSm * 2
                            implicitHeight: chipRun.implicitHeight + root.spacingXs * 2
                            Text {
                                id: chipRun
                                anchors.centerIn: parent
                                text: "train running"
                                color: "#4caf6e"
                                font.pixelSize: root.evalCaptionSize
                                font.bold: true
                            }
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        text: "Ожидаемо: эвристика " + leaguePanel._fmtPct(poolContext.p_heuristic)
                              + " · снапшоты " + leaguePanel._fmtPct(1.0 - Number(poolContext.p_heuristic || 0))
                              + (Number(poolContext.run_total_games || 0) > 0
                                 ? ("    Фактически за run (" + Number(poolContext.run_total_games) + "): эвристика "
                                    + leaguePanel._fmtPct(poolContext.run_heuristic_actual) + " · снапшоты "
                                    + leaguePanel._fmtPct(poolContext.run_snapshot_actual) + " · W/D/L "
                                    + leaguePanel._fmtWdl(poolContext.run_wins, poolContext.run_draws, poolContext.run_losses))
                                 : "    Текущий run: данных пока нет")
                        color: root.uiTextMain
                        font.pixelSize: root.evalCaptionSize
                        font.family: root.fontDataFamily
                        wrapMode: Text.WordWrap
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: poolContext.formation !== undefined
                        property var f: poolContext.formation || ({})
                        text: "Формирование: реестр всего " + Number(f.registry_total || 0)
                              + " → сторона " + String(f.opponent_side || poolContext.opponent_side || "P?")
                              + " " + Number(f.side_compatible || 0)
                              + " → контракт совместим " + Number(f.contract_compatible || 0)
                              + " → взято " + Number(f.selected || 0)
                              + ". Отброшено: другая сторона " + Number(f.filtered_side || 0)
                              + ", контракт " + Number(f.filtered_contract || 0)
                              + ", дубль " + Number(f.filtered_duplicate || 0)
                              + ", вне лимита " + Number(f.limited_out || 0) + "."
                        color: root.uiTextMuted
                        font.pixelSize: Math.round(11 * root.uiScale)
                        wrapMode: Text.WordWrap
                    }

                    Flow {
                        Layout.fillWidth: true
                        spacing: root.spacingSm

                        Rectangle {
                            visible: Number(poolContext.draw_rate) >= 0
                            color: poolContext.draw_pit_alert ? "#3a201c" : "#142318"
                            border.color: poolContext.draw_pit_alert ? "#e05a47" : "#4caf6e"
                            border.width: 1
                            implicitWidth: healthDraw.implicitWidth + root.spacingSm * 2
                            implicitHeight: healthDraw.implicitHeight + root.spacingXs * 2
                            Text {
                                id: healthDraw
                                anchors.centerIn: parent
                                text: (poolContext.draw_pit_alert ? "⚠ Ничейная яма " : "✓ Draw под порогом ")
                                      + leaguePanel._fmtPct(poolContext.draw_rate) + " / 70%"
                                color: poolContext.draw_pit_alert ? "#e05a47" : "#4caf6e"
                                font.pixelSize: root.evalCaptionSize
                                font.bold: true
                            }
                        }

                        Rectangle {
                            color: poolContext.concentration_alert ? "#3a201c" : "#142318"
                            border.color: poolContext.concentration_alert ? "#e05a47" : "#4caf6e"
                            border.width: 1
                            implicitWidth: healthConcentration.implicitWidth + root.spacingSm * 2
                            implicitHeight: healthConcentration.implicitHeight + root.spacingXs * 2
                            Text {
                                id: healthConcentration
                                anchors.centerIn: parent
                                text: (poolContext.concentration_alert ? "⚠ Концентрация PFSP " : "✓ Концентрация PFSP нормальная · max ")
                                      + leaguePanel._fmtPct(poolContext.max_snapshot_prob)
                                color: poolContext.concentration_alert ? "#e05a47" : "#4caf6e"
                                font.pixelSize: root.evalCaptionSize
                                font.bold: true
                            }
                        }

                        Rectangle {
                            visible: String(poolContext.stats_updated_at || "").length > 0
                            color: "#1f2430"
                            border.color: root.uiBorder
                            border.width: 1
                            implicitWidth: healthUpdated.implicitWidth + root.spacingSm * 2
                            implicitHeight: healthUpdated.implicitHeight + root.spacingXs * 2
                            Text {
                                id: healthUpdated
                                anchors.centerIn: parent
                                text: "stats обновлены " + String(poolContext.stats_updated_at)
                                color: root.uiTextMuted
                                font.pixelSize: root.evalCaptionSize
                            }
                        }
                    }

                    TabBar {
                        id: poolTabs
                        Layout.fillWidth: true
                        background: Rectangle { color: "transparent"; border.width: 0 }

                        TabButton {
                            text: "Кандидаты"
                            font.pixelSize: root.evalCaptionSize
                            implicitHeight: Math.round(32 * root.uiScale)
                            background: Rectangle {
                                color: poolTabs.currentIndex === 0 ? root.bgElevated : "transparent"
                                border.width: 0
                                Rectangle {
                                    anchors.bottom: parent.bottom
                                    width: parent.width
                                    height: 2
                                    color: poolTabs.currentIndex === 0 ? "#b88a26" : "transparent"
                                }
                            }
                            contentItem: Text {
                                text: parent.text
                                color: poolTabs.currentIndex === 0 ? root.uiTextMain : root.uiTextMuted
                                font: parent.font
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                        TabButton {
                            text: "История stats"
                            font.pixelSize: root.evalCaptionSize
                            implicitHeight: Math.round(32 * root.uiScale)
                            background: Rectangle {
                                color: poolTabs.currentIndex === 1 ? root.bgElevated : "transparent"
                                border.width: 0
                                Rectangle {
                                    anchors.bottom: parent.bottom
                                    width: parent.width
                                    height: 2
                                    color: poolTabs.currentIndex === 1 ? "#b88a26" : "transparent"
                                }
                            }
                            contentItem: Text {
                                text: parent.text
                                color: poolTabs.currentIndex === 1 ? root.uiTextMain : root.uiTextMuted
                                font: parent.font
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                        TabButton {
                            text: "Train live"
                            font.pixelSize: root.evalCaptionSize
                            implicitHeight: Math.round(32 * root.uiScale)
                            background: Rectangle {
                                color: poolTabs.currentIndex === 2 ? root.bgElevated : "transparent"
                                border.width: 0
                                Rectangle {
                                    anchors.bottom: parent.bottom
                                    width: parent.width
                                    height: 2
                                    color: poolTabs.currentIndex === 2 ? "#b88a26" : "transparent"
                                }
                            }
                            contentItem: Text {
                                text: parent.text
                                color: poolTabs.currentIndex === 2 ? root.uiTextMain : root.uiTextMuted
                                font: parent.font
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 1
                        color: root.uiBorder
                    }

                    StackLayout {
                        id: poolStack
                        Layout.fillWidth: true
                        currentIndex: poolTabs.currentIndex

                        // ── Кандидаты ──
                        ColumnLayout {
                            spacing: root.spacingXs

                            ScrollView {
                                Layout.fillWidth: true
                                clip: true
                                ScrollBar.horizontal.policy: ScrollBar.AsNeeded
                                ScrollBar.vertical.policy: ScrollBar.AlwaysOff
                                contentWidth: leaguePanel._tableWidth
                                implicitHeight: Math.min(
                                    Math.round(268 * root.uiScale),
                                    Math.max(Math.round(56 * root.uiScale), (candidatesModel.count + 1) * leaguePanel._rowH)
                                )

                                Column {
                                    width: leaguePanel._tableWidth
                                    spacing: root.spacingXs
                                    CandidateTableHeader {}
                                    Repeater {
                                        model: candidatesModel
                                        delegate: CandidateRow {
                                            labelText: model.label
                                            agentIdText: model.agent_id
                                            algoText: model.algo
                                            ageText: model.age
                                            gamesVal: model.games
                                            wrText: model.winrate
                                            drawText: model.draw_pct
                                            vpText: model.vp_per_game
                                            probSnapshotText: model.prob_snapshot
                                            probEpisodeText: model.prob_episode
                                            runGamesVal: model.run_games
                                            runActualText: model.run_actual
                                            runWdlText: model.run_wdl
                                            reasonText: model.reason
                                        }
                                    }
                                }
                            }

                            Text {
                                visible: candidatesModel.count === 0
                                text: poolContext.has_contract === false
                                      ? "Нет совместимого контракта в реестре — кандидаты не отфильтрованы."
                                      : "Нет кандидатов в пуле — нужны снапшоты стороны "
                                        + (poolContext.opponent_side || "P?")
                                        + " в реестре (train с «ПУЛ / ЛИГА»)."
                                color: root.uiTextMuted
                                font.pixelSize: root.evalCaptionSize
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }

                            Text {
                                visible: candidatesModel.count > 0
                                text: "Эвристика-анкер: P эпизода "
                                      + leaguePanel._fmtPct(heuristicState.prob_episode)
                                      + " · run игр " + Number(heuristicState.run_games || 0)
                                      + " · факт. " + leaguePanel._fmtPct(heuristicState.run_actual_prob)
                                      + " · run W/D/L " + leaguePanel._fmtWdl(
                                            heuristicState.run_wins,
                                            heuristicState.run_draws,
                                            heuristicState.run_losses)
                                color: root.uiTextMuted
                                font.pixelSize: Math.round(11 * root.uiScale)
                                Layout.fillWidth: true
                            }
                        }

                        // ── История stats ──
                        ColumnLayout {
                            spacing: root.spacingXs

                            Text {
                                text: "Накопленный opponent_pool_stats.json · " + historyModel.count + " записей · ✓ = в активном пуле"
                                color: root.uiTextMuted
                                font.pixelSize: Math.round(11 * root.uiScale)
                                Layout.fillWidth: true
                            }

                            ScrollView {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Math.round(280 * root.uiScale)
                                clip: true
                                ScrollBar.horizontal.policy: ScrollBar.AsNeeded
                                ScrollBar.vertical.policy: ScrollBar.AsNeeded
                                contentWidth: leaguePanel._historyTableWidth

                                Column {
                                    width: leaguePanel._historyTableWidth
                                    spacing: root.spacingXs
                                    HistoryTableHeader {}
                                    Repeater {
                                        model: historyModel
                                        delegate: HistoryRow {
                                            labelText: model.label
                                            agentIdText: model.agent_id
                                            algoText: model.algo
                                            inPool: model.in_pool
                                            ageText: model.age
                                            gamesVal: model.games
                                            wrText: model.winrate
                                            wdlText: model.wdl
                                            drawText: model.draw_pct
                                            vpText: model.vp_per_game
                                            updatedText: model.updated_at
                                        }
                                    }
                                }
                            }

                            Text {
                                visible: historyModel.count === 0
                                text: "История пуста — stats появятся после train с источником «ПУЛ / ЛИГА»."
                                color: root.uiTextMuted
                                font.pixelSize: root.evalCaptionSize
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                        }

                        // ── Train live ──
                        ColumnLayout {
                            spacing: root.spacingXs

                            Text {
                                text: "Последние строки [POOL] из train-лога · " + trainLiveModel.count + " строк"
                                color: root.uiTextMuted
                                font.pixelSize: Math.round(11 * root.uiScale)
                                Layout.fillWidth: true
                            }

                            ListView {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Math.min(
                                    Math.round(280 * root.uiScale),
                                    Math.max(Math.round(48 * root.uiScale), trainLiveModel.count * Math.round(20 * root.uiScale))
                                )
                                clip: true
                                spacing: 2
                                model: trainLiveModel
                                delegate: Text {
                                    width: ListView.view.width
                                    text: model.text
                                    color: model.kind === "warn" ? "#e6a23c"
                                         : (model.kind === "result" ? "#4caf6e" : root.uiTextMuted)
                                    font.pixelSize: Math.round(11 * root.uiScale)
                                    font.family: root.fontDataFamily
                                    wrapMode: Text.WrapAnywhere
                                }
                            }

                            Text {
                                visible: trainLiveModel.count === 0
                                text: "Нет строк [POOL] в логе — запустите train с «ПУЛ / ЛИГА»."
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
    }
}
