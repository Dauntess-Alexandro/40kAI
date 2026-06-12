// app/gui_qt/qml/components/HeurMetricsPanel.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: heurPanel

    // ── состояние бенчмарка ──────────────────────────────────────────────
    property string benchStatusText: "Нет данных."
    property bool   benchHasError:   false
    property var    benchHistory:     []

    // ── состояние калибровки ─────────────────────────────────────────────
    property int    calDone:          0
    property int    calTotal:         40
    property int    bestCandidateIdx: -1
    property real   bestScore:        0.0
    property string currentRunDir:    ""
    property string patchText:        ""
    property real   targetWinrate:    0.50   // цель калибровки (0.50 спарринг, 0.65 хард, 1.0 максимум)
    property var    _calRows:         []     // сырые строки кандидатов для живой сортировки

    // ── helpers ──────────────────────────────────────────────────────────
    function _colorForValue(val, good, warn) {
        if (val >= good)  return "#4caf6e"
        if (val >= warn)  return "#b88a26"
        return "#cf3f3f"
    }
    function _fmt(val, dec) {
        if (val === undefined || val === null) return "—"
        return Number(val).toFixed(dec !== undefined ? dec : 3)
    }
    // Выбранный learner-агент из дропдауна калибровки (или «Авто»).
    function _selectedAgent() {
        var list = controller.calibrationAgents
        var i = calAgentCombo.currentIndex
        if (list && i >= 0 && i < list.length) return list[i]
        return { agent_id: "", side: "" }
    }
    // Сторона эвристики = противоположна стороне learner.
    function _heuristicSide() {
        var a = _selectedAgent()
        return (a && a.side === "P2") ? "P1" : "P2"
    }

    // ── лидерборд кандидатов (живая сортировка по score) ──────────────────
    function _resetLeaderboard() {
        _calRows = []
        candidatesModel.clear()
    }
    function _addCandidate(row) {
        var status = row.status || "…"
        var hasScore = row.score !== undefined && row.score !== null
        var scoreNum = hasScore ? row.score : -1e9
        if (status === "ok" && scoreNum > heurPanel.bestScore) {
            heurPanel.bestScore = scoreNum
            heurPanel.bestCandidateIdx = row.candidate_idx !== undefined ? row.candidate_idx : 0
        }
        _calRows.push({
            idxNum:   row.candidate_idx !== undefined ? row.candidate_idx : -1,
            scoreNum: scoreNum,
            score:    hasScore ? _fmt(row.score, 3) : "…",
            winrate:  _fmt(row.heur_winrate, 3),
            entropy:  _fmt(row.style_entropy_norm, 3),
            draws:    row.draw_rate !== undefined ? _fmt(row.draw_rate * 100, 1) + "%" : "…",
            status:   status,
            reason:   (row.reject_reasons || []).join(", ")
        })
        _rebuildLeaderboard()
    }
    function _rebuildLeaderboard() {
        var rows = _calRows.slice()
        rows.sort(function(a, b) { return b.scoreNum - a.scoreNum })
        candidatesModel.clear()
        for (var i = 0; i < rows.length; i++) {
            var r = rows[i]
            candidatesModel.append({
                rank:     i + 1,
                idx:      "" + (r.idxNum >= 0 ? r.idxNum : "?"),
                score:    r.score,
                scoreNum: r.scoreNum,
                winrate:  r.winrate,
                entropy:  r.entropy,
                draws:    r.draws,
                status:   r.status,
                reason:   r.reason,
                isBest:   r.idxNum === heurPanel.bestCandidateIdx
            })
        }
    }

    // ── сигналы runners ──────────────────────────────────────────────────
    Connections {
        target: heurBenchRunner
        function onBenchmarkFinished(result) {
            var w  = _fmt(result.heur_winrate || result.heur_winrate_all, 3)
            var e  = _fmt(result.style_entropy_norm, 3)
            var dr = _fmt((result.draw_rate || 0) * 100, 1)
            benchStatusText = "winrate=" + w + "  entropy=" + e + "  draws=" + dr + "%"
            benchHasError   = false
            var now = Qt.formatDateTime(new Date(), "dd.MM hh:mm")
            if (benchHistory.length >= 5) benchHistory.splice(0, 1)
            benchHistory.push({time: now, winrate: w, entropy: e, draws: dr + "%", games: result.games || 0})
            benchHistoryModel.clear()
            for (var i = benchHistory.length - 1; i >= 0; i--) {
                benchHistoryModel.append(benchHistory[i])
            }
        }
        function onBenchmarkFailed(error) {
            benchStatusText = "Ошибка: " + error
            benchHasError   = true
        }
    }

    Connections {
        target: heurCalRunner
        function onCandidateResult(row) {
            heurPanel._addCandidate(row)
        }
        function onCalibrationFinished(summary) {
            heurPanel.currentRunDir = summary.run_dir || heurCalRunner.currentRunDir
            heurPanel.patchText = summary.patch_lines || ""
            var idx = summary.best_candidate_idx
            if (idx !== null && idx !== undefined) {
                heurPanel.bestCandidateIdx = idx
            }
            heurPanel._rebuildLeaderboard()
        }
        function onCalibrationFailed(error) {
            benchStatusText = "Калибровка: ошибка — " + error
        }
        function onPatchApplied(keys) {
            patchStatusText.text = "✓ Применено: " + keys.join(", ")
            patchStatusText.color = "#4caf6e"
        }
        function onPatchFailed(error) {
            patchStatusText.text = "Ошибка патча: " + error
            patchStatusText.color = "#cf3f3f"
        }
    }

    // ════════════════════════════════════════════════════════════════════
    //  Layout
    // ════════════════════════════════════════════════════════════════════
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: root.spacingLg
        spacing: 0

        Text {
            text: "Метрики эвристики"
            font.pixelSize: Math.round(20 * root.uiScale)
            font.bold: true
            color: root.textPrimary
        }
        Text {
            text: "ENEMY heuristic · Сводка, бенчмарк и калибровка весов"
            font.pixelSize: root.evalCaptionSize
            color: root.textSecondary
            Layout.bottomMargin: root.spacingMd
        }

        TabBar {
            id: innerTabs
            Layout.fillWidth: true
            background: Rectangle { color: root.bgSurface; border.width: 0 }
            TabButton {
                text: "Сводка"
                font.pixelSize: root.evalCaptionSize
                background: Rectangle {
                    color: innerTabs.currentIndex === 0 ? root.bgElevated : "transparent"
                    border.width: 0
                    Rectangle {
                        anchors.bottom: parent.bottom; width: parent.width; height: 2
                        color: innerTabs.currentIndex === 0 ? root.accentPrimaryAction : "transparent"
                    }
                }
                contentItem: Text {
                    text: parent.text; color: innerTabs.currentIndex === 0 ? root.textPrimary : root.textSecondary
                    font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }
            }
            TabButton {
                text: "Бенчмарк"
                font.pixelSize: root.evalCaptionSize
                background: Rectangle {
                    color: innerTabs.currentIndex === 1 ? root.bgElevated : "transparent"
                    border.width: 0
                    Rectangle {
                        anchors.bottom: parent.bottom; width: parent.width; height: 2
                        color: innerTabs.currentIndex === 1 ? root.accentP1 : "transparent"
                    }
                }
                contentItem: Text {
                    text: parent.text; color: innerTabs.currentIndex === 1 ? root.textPrimary : root.textSecondary
                    font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }
            }
            TabButton {
                text: "Калибровка"
                font.pixelSize: root.evalCaptionSize
                background: Rectangle {
                    color: innerTabs.currentIndex === 2 ? root.bgElevated : "transparent"
                    border.width: 0
                    Rectangle {
                        anchors.bottom: parent.bottom; width: parent.width; height: 2
                        color: innerTabs.currentIndex === 2 ? root.accentP1 : "transparent"
                    }
                }
                contentItem: Text {
                    text: parent.text; color: innerTabs.currentIndex === 2 ? root.textPrimary : root.textSecondary
                    font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }
            }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: root.borderMuted }

        StackLayout {
            id: innerStack
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: innerTabs.currentIndex

            // ══════════════════════════════════════
            // ВКЛАДКА 0: СВОДКА
            // ══════════════════════════════════════
            ScrollView {
                clip: true
                Column {
                    width: innerStack.width
                    spacing: root.spacingMd
                    topPadding: root.spacingMd

                    Row {
                        spacing: root.spacingSm
                        width: parent.width

                        Repeater {
                            model: [
                                { label: "Winrate",        key: "winrate",    good: 0.46, warn: 0.40 },
                                { label: "Entropy (стили)",key: "entropy",    good: 0.86, warn: 0.80 },
                                { label: "Draw rate %",    key: "draw_rate",  good: 0,    warn: 0     },
                            ]
                            delegate: Rectangle {
                                width: (innerStack.width - 2 * root.spacingSm) / 3
                                height: Math.round(60 * root.uiScale)
                                color: root.bgElevated
                                border.color: root.borderMuted
                                border.width: 1
                                radius: 2

                                property real rawVal: {
                                    var d = controller.heuristicMetricsDict
                                    if (!d) return 0
                                    var v = d[modelData.key]
                                    return v !== undefined ? (modelData.key === "draw_rate" ? v * 100 : v) : 0
                                }
                                property string displayVal: modelData.key === "draw_rate"
                                    ? _fmt(rawVal, 1) + "%"
                                    : _fmt(rawVal, 3)
                                property color valColor: {
                                    if (modelData.key === "draw_rate")
                                        return rawVal < 3.0 ? "#4caf6e" : rawVal < 5.0 ? "#b88a26" : "#cf3f3f"
                                    return _colorForValue(rawVal, modelData.good, modelData.warn)
                                }

                                Column {
                                    anchors.centerIn: parent
                                    spacing: 2
                                    Text {
                                        text: displayVal
                                        font.pixelSize: Math.round(20 * root.uiScale)
                                        font.bold: true
                                        color: valColor
                                        anchors.horizontalCenter: parent.horizontalCenter
                                    }
                                    Text {
                                        text: modelData.label.toUpperCase()
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                        color: root.textSecondary
                                        font.letterSpacing: 0.8
                                        anchors.horizontalCenter: parent.horizontalCenter
                                    }
                                }
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        title: "Показатели"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        // Каждая строка: [подпись, ключ в heuristicMetricsDict, формат].
                        // Формат: "str" — как есть, "int" — целое, "f3"/"f4" — float с N знаков.
                        // Значение резолвится в делегате (реактивно к controller.heuristicMetricsDict).
                        Grid {
                            columns: 2
                            columnSpacing: Math.round(24 * root.uiScale)
                            rowSpacing: Math.round(3 * root.uiScale)

                            Repeater {
                                model: [
                                    ["Ран",           "run_id",              "str"],
                                    ["Обновлено",     "updated_at",          "str"],
                                    ["Всего игр",     "total_games",         "int"],
                                    ["Invalid rate",  "invalid_rate",        "f4"],
                                    ["Avg risk",      "avg_risk",            "f3"],
                                    ["Avg cover",     "avg_cover",           "f3"],
                                    ["Charge succ.",  "charge_success_rate", "f3"],
                                    ["Shoot overkill","shoot_overkill_rate", "f3"],
                                    ["Fallback rate", "fallback_rate",       "f3"],
                                    ["Mode kite",     "mode_kite",           "int"],
                                    ["Mode hold",     "mode_hold",           "int"],
                                    ["Mode commit",   "mode_commit",         "int"],
                                    ["Role ranged",   "role_ranged",         "int"],
                                    ["Role hybrid",   "role_hybrid",         "int"],
                                    ["Role melee",    "role_melee",          "int"],
                                ]
                                delegate: Row {
                                    spacing: root.spacingSm
                                    property var md: controller.heuristicMetricsDict || ({})
                                    property var raw: md[modelData[1]]
                                    property string valStr: {
                                        var fmt = modelData[2]
                                        if (fmt === "str") return String(raw !== undefined ? raw : "—")
                                        if (fmt === "int") return String(raw !== undefined ? raw : 0)
                                        if (fmt === "f4")  return _fmt(raw, 4)
                                        return _fmt(raw, 3)
                                    }
                                    Text { text: modelData[0] + ":"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize; width: Math.round(110 * root.uiScale) }
                                    Text { text: parent.valStr; color: root.textPrimary; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono" }
                                }
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        title: "Сводный отчёт"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }
                        TextArea {
                            width: parent.width
                            height: Math.round(160 * root.uiScale)
                            text: controller.heuristicMetricsText
                            readOnly: true
                            wrapMode: Text.WordWrap
                            selectByMouse: true
                            color: root.textSecondary
                            font.pixelSize: root.evalCaptionSize
                            font.family: "JetBrains Mono"
                            background: Rectangle { color: root.bgSurface }
                        }
                    }
                }
            }

            // ══════════════════════════════════════
            // ВКЛАДКА 1: БЕНЧМАРК
            // ══════════════════════════════════════
            ScrollView {
                clip: true
                Column {
                    width: innerStack.width
                    spacing: root.spacingMd
                    topPadding: root.spacingMd

                    GroupBox {
                        width: parent.width
                        title: "Параметры"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        RowLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            Text { text: "Игр:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                            TextField {
                                id: benchGamesInput
                                text: "30"
                                validator: IntValidator { bottom: 1; top: 9999 }
                                font.pixelSize: root.evalCaptionSize
                                font.family: "JetBrains Mono"
                                color: root.textPrimary
                                background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                implicitWidth: Math.round(60 * root.uiScale)
                                enabled: !heurBenchRunner.isRunning
                            }

                            Text { text: "Оппонент:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                            ComboBox {
                                id: benchPolicyCombo
                                model: ["heuristic_auto"]
                                font.pixelSize: root.evalCaptionSize
                                enabled: !heurBenchRunner.isRunning
                                implicitWidth: Math.round(150 * root.uiScale)
                                contentItem: Text {
                                    text: benchPolicyCombo.displayText
                                    color: root.textPrimary
                                    font: benchPolicyCombo.font
                                    verticalAlignment: Text.AlignVCenter
                                    leftPadding: root.spacingSm
                                }
                                background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                            }

                            Item { Layout.fillWidth: true }

                            Button {
                                visible: !heurBenchRunner.isRunning
                                text: "▶ Запустить бенчмарк"
                                font.pixelSize: root.evalCaptionSize
                                onClicked: heurBenchRunner.run(parseInt(benchGamesInput.text), benchPolicyCombo.currentText)
                                contentItem: Text { text: parent.text; color: "#7db4f5"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                background: Rectangle { color: parent.down ? "#0a1525" : "#0e1f3a"; border.color: parent.hovered ? "#5090d0" : "#2f6ed8"; border.width: 1 }
                            }
                            Button {
                                visible: heurBenchRunner.isRunning
                                text: "■ Стоп"
                                font.pixelSize: root.evalCaptionSize
                                onClicked: heurBenchRunner.stop()
                                contentItem: Text { text: parent.text; color: "#c05050"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                background: Rectangle { color: "#1a0c0c"; border.color: "#6b2020"; border.width: 1 }
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        title: "Результат"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ColumnLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            Rectangle {
                                Layout.fillWidth: true
                                height: Math.round(28 * root.uiScale)
                                color: root.bgSurface
                                border.color: heurPanel.benchHasError ? "#6b2020" : root.borderMuted
                                border.width: 1
                                Text {
                                    anchors.fill: parent; anchors.leftMargin: root.spacingSm
                                    text: heurBenchRunner.isRunning ? "Запущен…" : heurPanel.benchStatusText
                                    color: heurPanel.benchHasError ? "#cf3f3f" : root.textSecondary
                                    font.pixelSize: root.evalCaptionSize
                                    font.family: "JetBrains Mono"
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        title: "История прогонов"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ListModel { id: benchHistoryModel }

                        Column {
                            width: parent.width
                            spacing: 0

                            Rectangle {
                                width: parent.width
                                height: Math.round(20 * root.uiScale)
                                color: root.bgSurface
                                Row {
                                    anchors.fill: parent
                                    Repeater {
                                        model: ["Время", "Winrate", "Entropy", "Draws", "Игр"]
                                        delegate: Text {
                                            text: modelData; color: root.textSecondary
                                            font.pixelSize: Math.round(9 * root.uiScale)
                                            width: [100, 70, 70, 60, 50][index] * root.uiScale
                                            leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                }
                            }

                            Repeater {
                                model: benchHistoryModel
                                delegate: Rectangle {
                                    width: parent.width
                                    height: Math.round(22 * root.uiScale)
                                    color: index % 2 === 0 ? root.bgElevated : root.bgSurface
                                    Row {
                                        anchors.fill: parent
                                        // Явные колонки (см. таблицу кандидатов: вложенный Repeater
                                        // с [model.*] ловит коллизию имени model → пустые ячейки).
                                        Text {
                                            text: model.time; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(100 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Text {
                                            text: model.winrate; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(70 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Text {
                                            text: model.entropy; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(70 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Text {
                                            text: model.draws; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(60 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Text {
                                            text: String(model.games); color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(50 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                }
                            }

                            Text {
                                visible: benchHistoryModel.count === 0
                                text: "Нет прогонов в этой сессии."
                                color: root.textSecondary
                                font.pixelSize: root.evalCaptionSize
                                leftPadding: root.spacingSm
                                topPadding: root.spacingSm
                            }
                        }
                    }
                }
            }

            // ══════════════════════════════════════
            // ВКЛАДКА 2: КАЛИБРОВКА
            // ══════════════════════════════════════
            ScrollView {
                clip: true
                Column {
                    width: innerStack.width
                    spacing: root.spacingMd
                    topPadding: root.spacingMd

                    GroupBox {
                        width: parent.width
                        title: "Параметры"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ColumnLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Text { text: "Кандидатов:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calCandidatesInput; text: "40"
                                    validator: IntValidator { bottom: 1; top: 999 }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(55 * root.uiScale)
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Text { text: "Игр/кандидат:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calGamesInput; text: "50"
                                    validator: IntValidator { bottom: 1; top: 9999 }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(55 * root.uiScale)
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Text { text: "Seed:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calSeedInput; text: "1390520"
                                    validator: IntValidator { bottom: 0 }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(75 * root.uiScale)
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Item { Layout.fillWidth: true }
                            }

                            // Выбор learner-агента (P1/P2). Сторона эвристики — противоположная.
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Text { text: "Learner-агент:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                ComboBox {
                                    id: calAgentCombo
                                    Layout.fillWidth: true
                                    enabled: !heurCalRunner.isRunning
                                    model: controller.calibrationAgents
                                    textRole: "label"
                                    font.pixelSize: root.evalCaptionSize
                                    contentItem: Text {
                                        text: calAgentCombo.displayText
                                        color: root.textPrimary
                                        font: calAgentCombo.font
                                        verticalAlignment: Text.AlignVCenter
                                        leftPadding: root.spacingSm
                                        elide: Text.ElideRight
                                    }
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Button {
                                    text: "⟳"
                                    enabled: !heurCalRunner.isRunning
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: controller.refreshCalibrationAgents()
                                    contentItem: Text { text: parent.text; color: root.textSecondary; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                    implicitWidth: Math.round(28 * root.uiScale)
                                }
                            }
                            Text {
                                Layout.fillWidth: true
                                wrapMode: Text.WordWrap
                                color: root.textSecondary
                                font.pixelSize: Math.round(9 * root.uiScale)
                                text: {
                                    var a = _selectedAgent()
                                    if (!a || !a.agent_id) return "Эвристика играет P2 против последнего агента (по умолчанию)."
                                    var heur = a.side === "P2" ? "P1" : "P2"
                                    return "Learner на стороне " + a.side + " · эвристика играет " + heur
                                }
                            }

                            // ── Режим цели: пресеты + ручной target winrate ──────────
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Text { text: "Цель:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }

                                Repeater {
                                    model: [
                                        { label: "Спарринг 0.50", val: 0.50 },
                                        { label: "Хард 0.65",     val: 0.65 },
                                        { label: "Максимум",      val: 1.00 },
                                    ]
                                    delegate: Button {
                                        enabled: !heurCalRunner.isRunning
                                        text: modelData.label
                                        font.pixelSize: root.evalCaptionSize
                                        property bool active: Math.abs(heurPanel.targetWinrate - modelData.val) < 0.001
                                        onClicked: {
                                            heurPanel.targetWinrate = modelData.val
                                            calTargetInput.text = modelData.val.toFixed(2)
                                        }
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.active ? "#e8c060" : root.textSecondary
                                            font: parent.font
                                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                                        }
                                        background: Rectangle {
                                            color: parent.active ? "#1a1508" : root.bgSurface
                                            border.color: parent.active ? "#b88a26" : root.borderMuted
                                            border.width: 1
                                        }
                                    }
                                }

                                Text { text: "свой:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calTargetInput
                                    text: "0.50"
                                    validator: DoubleValidator { bottom: 0.0; top: 1.0; decimals: 2; notation: DoubleValidator.StandardNotation }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(50 * root.uiScale)
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                    onEditingFinished: {
                                        var v = parseFloat(text)
                                        if (!isNaN(v) && v >= 0.0 && v <= 1.0) heurPanel.targetWinrate = v
                                    }
                                }
                                Item { Layout.fillWidth: true }
                                Text {
                                    color: root.textSecondary; font.pixelSize: Math.round(9 * root.uiScale)
                                    font.family: "JetBrains Mono"
                                    text: heurPanel.targetWinrate >= 0.95
                                        ? "макс. сила · эвристика " + _heuristicSide()
                                        : "цель winrate=" + heurPanel.targetWinrate.toFixed(2) + " · эвристика " + _heuristicSide()
                                }
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm

                                Button {
                                    visible: !heurCalRunner.isRunning
                                    text: "▶ Калибровать"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: {
                                        heurPanel._resetLeaderboard()
                                        heurPanel.bestCandidateIdx = -1
                                        heurPanel.bestScore = 0.0
                                        heurPanel.patchText = ""
                                        heurPanel.calDone = 0
                                        heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                        var a = _selectedAgent()
                                        heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                          parseInt(calGamesInput.text),
                                                          parseInt(calSeedInput.text), false,
                                                          a.agent_id, a.side, heurPanel.targetWinrate)
                                    }
                                    contentItem: Text { text: parent.text; color: "#e8c060"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: parent.down ? "#100e00" : "#1a1508"; border.color: parent.hovered ? "#d0a030" : "#b88a26"; border.width: 1 }
                                }
                                Button {
                                    visible: !heurCalRunner.isRunning
                                    text: "Dry run"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: {
                                        heurPanel._resetLeaderboard()
                                        heurPanel.bestCandidateIdx = -1
                                        heurPanel.calDone = 0
                                        heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                        var a = _selectedAgent()
                                        heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                          parseInt(calGamesInput.text),
                                                          parseInt(calSeedInput.text), true,
                                                          a.agent_id, a.side, heurPanel.targetWinrate)
                                    }
                                    contentItem: Text { text: parent.text; color: root.textSecondary; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Button {
                                    visible: heurCalRunner.isRunning
                                    text: "■ Стоп"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: heurCalRunner.stop()
                                    contentItem: Text { text: parent.text; color: "#c05050"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: "#1a0c0c"; border.color: "#6b2020"; border.width: 1 }
                                }

                                Item { Layout.fillWidth: true }
                                Text {
                                    visible: heurCalRunner.isRunning
                                    text: heurPanel.calDone + " / " + heurPanel.calTotal
                                    color: root.textSecondary; font.pixelSize: root.evalCaptionSize
                                    font.family: "JetBrains Mono"
                                }
                            }

                            Rectangle {
                                Layout.fillWidth: true
                                height: Math.round(8 * root.uiScale)
                                visible: heurCalRunner.isRunning || heurPanel.calDone > 0
                                color: root.bgSurface
                                border.color: root.borderMuted; border.width: 1
                                Rectangle {
                                    width: heurPanel.calTotal > 0
                                        ? parent.width * heurPanel.calDone / heurPanel.calTotal
                                        : 0
                                    height: parent.height
                                    color: "#b88a26"
                                    Behavior on width { NumberAnimation { duration: 300 } }
                                }
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        title: "Кандидаты — live"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ListModel { id: candidatesModel }

                        Column {
                            width: parent.width
                            spacing: 0

                            Rectangle {
                                width: parent.width
                                height: Math.round(20 * root.uiScale)
                                color: root.bgSurface
                                Row {
                                    anchors.fill: parent
                                    Repeater {
                                        model: [["место", 46], ["#", 32], ["score", 58], ["winrate", 60], ["entropy", 60], ["draws", 52], ["статус", 0]]
                                        delegate: Text {
                                            text: modelData[0]; color: root.textSecondary
                                            font.pixelSize: Math.round(9 * root.uiScale)
                                            width: modelData[1] > 0 ? Math.round(modelData[1] * root.uiScale) : parent.width - Math.round(308 * root.uiScale)
                                            leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                }
                            }

                            ListView {
                                width: parent.width
                                height: Math.min(candidatesModel.count * Math.round(22 * root.uiScale), Math.round(260 * root.uiScale))
                                model: candidatesModel
                                clip: true
                                ScrollBar.vertical: ScrollBar {}

                                delegate: Rectangle {
                                    width: ListView.view.width
                                    height: Math.round(22 * root.uiScale)
                                    color: model.isBest ? "#0d2010"
                                         : index % 2 === 0 ? root.bgElevated : root.bgSurface

                                    Row {
                                        anchors.fill: parent
                                        // Явные колонки: читаем model.* напрямую (вложенный Repeater
                                        // с массивом [model.*] ловит коллизию имени model → пустые ячейки).
                                        // место — медаль ранга
                                        Item {
                                            width: Math.round(46 * root.uiScale); height: parent.height
                                            Rectangle {
                                                x: root.spacingSm; anchors.verticalCenter: parent.verticalCenter
                                                width: Math.round(16 * root.uiScale); height: Math.round(16 * root.uiScale)
                                                radius: width / 2
                                                color: model.rank === 1 ? "#b88a26"
                                                     : model.rank === 2 ? "#9aa7b8"
                                                     : model.rank === 3 ? "#a06a3a" : "transparent"
                                                border.color: model.rank <= 3 ? "transparent" : root.borderMuted
                                                border.width: model.rank <= 3 ? 0 : 1
                                                Text {
                                                    anchors.centerIn: parent
                                                    text: model.rank
                                                    color: model.rank <= 3 ? "#0a0f1a" : root.textSecondary
                                                    font.pixelSize: Math.round(9 * root.uiScale); font.bold: model.rank <= 3
                                                }
                                            }
                                        }
                                        Text {
                                            text: "#" + model.idx; color: model.isBest ? "#b88a26" : root.textSecondary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(32 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        // score + мини-бар
                                        Item {
                                            width: Math.round(58 * root.uiScale); height: parent.height
                                            Text {
                                                anchors.left: parent.left; anchors.leftMargin: root.spacingSm
                                                anchors.top: parent.top; anchors.topMargin: Math.round(2 * root.uiScale)
                                                text: model.score; color: model.isBest ? "#4caf6e" : root.textPrimary
                                                font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"; font.bold: model.isBest
                                            }
                                            Rectangle {
                                                anchors.left: parent.left; anchors.leftMargin: root.spacingSm
                                                anchors.bottom: parent.bottom; anchors.bottomMargin: Math.round(2 * root.uiScale)
                                                height: Math.round(2 * root.uiScale)
                                                width: {
                                                    var b = heurPanel.bestScore > 0.001 ? heurPanel.bestScore : 1.0
                                                    var f = Math.max(0, Math.min(1, model.scoreNum / b))
                                                    return f * Math.round(44 * root.uiScale)
                                                }
                                                color: model.isBest ? "#4caf6e" : "#3a5a8a"
                                            }
                                        }
                                        Text {
                                            text: model.winrate; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(60 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Text {
                                            text: model.entropy
                                            color: parseFloat(model.entropy) >= 0.86 ? "#4caf6e"
                                                 : parseFloat(model.entropy) >= 0.84 ? "#b88a26" : "#cf3f3f"
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(60 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Text {
                                            text: model.draws; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(52 * root.uiScale); leftPadding: root.spacingSm
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        Rectangle {
                                            height: Math.round(16 * root.uiScale)
                                            width: statusTagText.implicitWidth + Math.round(10 * root.uiScale)
                                            anchors.verticalCenter: parent.verticalCenter
                                            color: model.isBest ? "#0d2918"
                                                 : model.status === "ok" ? "#0d2918"
                                                 : model.status === "dry_run" ? "#0e1f3a"
                                                 : "#1a0808"
                                            border.color: model.isBest ? "#1f5030"
                                                        : model.status === "ok" ? "#1f5030"
                                                        : model.status === "dry_run" ? "#2f6ed8"
                                                        : "#5a1515"
                                            border.width: 1
                                            Text {
                                                id: statusTagText
                                                anchors.centerIn: parent
                                                text: model.isBest ? "★ лучший"
                                                    : model.status === "ok" ? "✓ принят"
                                                    : model.status === "dry_run" ? "dry"
                                                    : model.status === "в работе" ? "⟳"
                                                    : model.reason.length > 0 ? model.reason
                                                    : model.status
                                                color: model.isBest ? "#4caf6e"
                                                     : model.status === "ok" ? "#4caf6e"
                                                     : model.status === "dry_run" ? "#7db4f5"
                                                     : "#cf3f3f"
                                                font.pixelSize: Math.round(8 * root.uiScale)
                                            }
                                        }
                                    }
                                }
                            }

                            Text {
                                visible: candidatesModel.count === 0
                                text: "Нет данных. Запустите калибровку."
                                color: root.textSecondary; font.pixelSize: root.evalCaptionSize
                                leftPadding: root.spacingSm; topPadding: root.spacingSm
                            }
                        }
                    }

                    GroupBox {
                        width: parent.width
                        visible: heurPanel.bestCandidateIdx >= 0
                        title: "Лучший патч — кандидат #" + heurPanel.bestCandidateIdx
                        label: Text { text: parent.title; color: "#4caf6e"; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: "#0d2010"; border.color: "#1f5030"; border.width: 1 }

                        ColumnLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            Text {
                                text: "score=" + _fmt(heurPanel.bestScore, 3)
                                color: "#4caf6e"
                                font.pixelSize: root.evalCaptionSize
                                font.family: "JetBrains Mono"
                                font.bold: true
                            }

                            TextArea {
                                Layout.fillWidth: true
                                height: Math.round(80 * root.uiScale)
                                // Патч-файл пишется только при ПОЛНОМ завершении калибровки.
                                // Стоп на середине → патча нет (видны только живые кандидаты).
                                text: heurPanel.patchText.length > 0
                                    ? heurPanel.patchText
                                    : heurCalRunner.isRunning
                                        ? "(Идёт калибровка — патч появится после прохода всех кандидатов)"
                                        : "(Патч создаётся только при полном завершении. Остановленный прогон патча не даёт — запустите без «Стоп».)"
                                readOnly: true
                                color: "#7db4f5"
                                font.pixelSize: Math.round(9 * root.uiScale)
                                font.family: "JetBrains Mono"
                                background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                            }

                            RowLayout {
                                spacing: root.spacingSm
                                Button {
                                    text: "✓ Применить патч"
                                    font.pixelSize: root.evalCaptionSize
                                    // Доступно только когда есть реальный патч (полное завершение).
                                    enabled: !heurCalRunner.isRunning && heurPanel.patchText.length > 0
                                    onClicked: heurCalRunner.applyPatch(heurCalRunner.currentRunDir)
                                    contentItem: Text { text: parent.text; color: parent.enabled ? "#e8c060" : "#6b5010"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: parent.down ? "#100e00" : "#1a1508"; border.color: parent.enabled ? (parent.hovered ? "#d0a030" : "#b88a26") : "#3a3010"; border.width: 1 }
                                }
                                Button {
                                    text: "Открыть папку"
                                    font.pixelSize: root.evalCaptionSize
                                    enabled: heurCalRunner.currentRunDir.length > 0
                                    onClicked: Qt.openUrlExternally("file:///" + heurCalRunner.currentRunDir)
                                    contentItem: Text { text: parent.text; color: parent.enabled ? root.textSecondary : "#3a4a5a"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                }
                                Text {
                                    id: patchStatusText
                                    text: ""
                                    font.pixelSize: root.evalCaptionSize
                                    font.family: "JetBrains Mono"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
