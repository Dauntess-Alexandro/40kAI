// app/gui_qt/qml/components/HeurMetricsPanel.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.settings 1.0

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
    property var    _top3:            []     // топ-3 по score для подиума
    property var    _bestHistory:     []     // лучший score после каждого кандидата (спарклайн)
    property real   _calStartMs:      0
    property int    _calElapsed:      0      // сек с начала прогона (тикает таймером)
    property bool   _advOpen:         false  // раскрыт ли блок «Дополнительно» (Seed/Агент)
    property int    _runGames:        0      // игр в текущем прогоне (для оценки скорости)
    property real   _secPerGame:      0.0    // средняя сек/партия по прошлым прогонам (для ETA)

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
    function _pct(val, dec) {
        if (val === undefined || val === null) return "—"
        return _fmt(Number(val) * 100, dec !== undefined ? dec : 1) + "%"
    }
    function _intText(val) {
        if (val === undefined || val === null || Number(val) <= 0) return "—"
        return Number(val).toLocaleString(Qt.locale("ru_RU"), "f", 0)
    }
    function _runComboIndex() {
        var runs = controller.heuristicMetricsRuns || []
        var selected = ""
        var d = controller.heuristicMetricsDict || {}
        if (d.selected_run_id !== undefined) selected = String(d.selected_run_id)
        for (var i = 0; i < runs.length; i++) {
            if (String(runs[i].run_id) === selected) return i
        }
        return runs.length > 0 ? 0 : -1
    }
    function _profileStatus(win, draw) {
        if (draw > 0.012) return "Ничьи"
        if (win < 0.48) return "Проверить"
        return "OK"
    }
    function _profileStatusColor(win, draw) {
        if (draw > 0.012 || win < 0.48) return "#b88a26"
        return "#4caf6e"
    }
    function _qualityBadge(key, val) {
        if (key === "charge_success_rate") return "Справочно"
        if (key === "avg_risk") return val >= 0.55 ? "Высокий" : val >= 0.25 ? "Средний" : "Низкий"
        if (key === "avg_cover") return val > 0.25 ? "OK" : "Низкое"
        return val <= 0.0001 ? "OK" : "Проверить"
    }
    function _qualityBadgeColor(key, val) {
        if (key === "charge_success_rate") return root.textSecondary
        if (key === "avg_risk") return val >= 0.55 ? "#cf3f3f" : val >= 0.25 ? "#b88a26" : "#4caf6e"
        if (key === "avg_cover") return val > 0.25 ? "#4caf6e" : root.textSecondary
        return val <= 0.0001 ? "#4caf6e" : "#b88a26"
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

    // ── Конфигурация запуска: валидация / степперы / оценка ────────────────
    function _numValid(t, minVal) {
        var v = parseInt(t)
        return t !== "" && !isNaN(v) && v >= minVal
    }
    // Все обязательные поля корректны (кандидаты ≥1, игр ≥1, seed ≥0).
    function _paramsValid() {
        return _numValid(calCandidatesInput.text, 1)
            && _numValid(calGamesInput.text, 1)
            && _numValid(calSeedInput.text, 0)
    }
    // Шаг по полю (кнопки −/+ и колесо мыши), с нижней границей.
    function _bump(field, delta, minVal) {
        var v = parseInt(field.text)
        if (isNaN(v)) v = minVal
        field.text = "" + Math.max(minVal, v + delta)
    }
    function _randomSeed() {
        return "" + (Math.floor(Math.random() * 9000000) + 1000)
    }
    // Копирование в буфер обмена через скрытый TextEdit (в QtQuick нет прямого API).
    function _copyToClipboard(t) {
        clipHelper.text = t
        clipHelper.selectAll()
        clipHelper.copy()
        clipHelper.text = ""
    }
    // «N × M = K партий · ≈ T» — оценка объёма прогона до запуска.
    function _estimateText() {
        var c = parseInt(calCandidatesInput.text)
        var g = parseInt(calGamesInput.text)
        if (isNaN(c) || isNaN(g) || c <= 0 || g <= 0) return "укажите кандидатов и игр"
        var total = c * g
        var s = c + " × " + g + " = " + total.toLocaleString(Qt.locale("ru_RU"), "f", 0) + " партий"
        if (heurPanel._secPerGame > 0) {
            var sec = Math.round(total * heurPanel._secPerGame)
            s += " · ≈ " + (sec < 90 ? sec + " сек" : Math.round(sec / 60) + " мин")
        }
        return s
    }

    // ETA по уже пройденным кандидатам.
    function _etaText() {
        if (calDone <= 0 || calDone >= calTotal || _calElapsed <= 0) return ""
        var per = _calElapsed / calDone
        var rem = Math.round(per * (calTotal - calDone))
        return rem < 60 ? "≈" + rem + " сек" : "≈" + Math.round(rem / 60) + " мин"
    }
    // Короткий тег статуса (полная причина — в tooltip).
    function _statusShort(status, reason, isBest) {
        if (isBest) return "★ лучший"
        if (status === "ok") return "✓ принят"
        if (status === "dry_run") return "dry"
        if (reason && reason.indexOf("entropy") >= 0) return "⚠ entropy"
        if (reason && reason.indexOf("winrate") >= 0) return "⚠ winrate"
        if (reason && reason.indexOf("draw") >= 0) return "⚠ draws"
        if (reason && reason.indexOf("invalid") >= 0) return "⚠ invalid"
        if (reason && reason.indexOf("fallback") >= 0) return "⚠ fallback"
        return status
    }

    // ── лидерборд кандидатов (живая сортировка по score) ──────────────────
    function _resetLeaderboard() {
        _calRows = []
        _top3 = []
        _bestHistory = []
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
            winrate:  row.heur_winrate !== undefined ? _fmt(row.heur_winrate * 100, 1) + "%" : "…",
            entropy:  _fmt(row.style_entropy_norm, 3),
            draws:    row.draw_rate !== undefined ? _fmt(row.draw_rate * 100, 1) + "%" : "…",
            status:   status,
            reason:   (row.reject_reasons || []).join(", ")
        })
        // история лучшего score (для спарклайна) — реассайн для перерисовки.
        var h = _bestHistory.slice()
        h.push(heurPanel.bestScore)
        _bestHistory = h
        _rebuildLeaderboard()
    }
    function _rebuildLeaderboard() {
        var rows = _calRows.slice()
        // Принятые (ok) выше отклонённых, внутри группы — по score убыв.
        // Иначе отклонённый с высоким score получал золото выше «лучшего».
        rows.sort(function(a, b) {
            var ao = a.status === "ok" ? 1 : 0
            var bo = b.status === "ok" ? 1 : 0
            if (ao !== bo) return bo - ao
            return b.scoreNum - a.scoreNum
        })
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
        // Подиум — только принятые (status ok), иначе медали у отрицательных score.
        var okRows = rows.filter(function (r) { return r.status === "ok" })
        heurPanel._top3 = okRows.slice(0, 3)
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

    // Тик ETA во время прогона калибровки.
    Timer {
        running: heurCalRunner.isRunning
        interval: 1000; repeat: true
        onTriggered: {
            heurPanel._calElapsed = Math.round((Date.now() - heurPanel._calStartMs) / 1000)
            // учим среднюю скорость (сек/партия) для оценки следующего прогона
            if (heurPanel.calDone > 0 && heurPanel._runGames > 0 && heurPanel._calElapsed > 0) {
                heurPanel._secPerGame = heurPanel._calElapsed / (heurPanel.calDone * heurPanel._runGames)
            }
        }
    }

    // Память значений между сессиями (QSettings через Qt.labs.settings).
    Settings {
        category: "heurCalibration"
        property alias candidates:   calCandidatesInput.text
        property alias games:        calGamesInput.text
        property alias seed:         calSeedInput.text
        property alias advancedOpen: heurPanel._advOpen
        property alias secPerGame:   heurPanel._secPerGame
        property alias targetCustom: calTargetInput.text
        property alias targetWinrate: heurPanel.targetWinrate
    }

    // Скрытый помощник для копирования в буфер обмена.
    TextEdit { id: clipHelper; visible: false; width: 0; height: 0 }

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
                font.pixelSize: Math.round(15 * root.uiScale)
                implicitHeight: Math.round(34 * root.uiScale)
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
                font.pixelSize: Math.round(15 * root.uiScale)
                implicitHeight: Math.round(34 * root.uiScale)
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
                font.pixelSize: Math.round(15 * root.uiScale)
                implicitHeight: Math.round(34 * root.uiScale)
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
                    id: summaryCol
                    property real calZoom: 1.0
                    property var md: controller.heuristicMetricsDict || ({})
                    width: innerStack.width / calZoom
                    scale: calZoom
                    transformOrigin: Item.TopLeft
                    spacing: root.spacingMd
                    topPadding: root.spacingMd

                    Row {
                        id: runContextRow
                        spacing: root.spacingSm
                        width: parent.width

                        Rectangle {
                            id: runSelectorCard
                            width: Math.round((parent.width - root.spacingSm) * 0.36)
                            height: Math.round(138 * root.uiScale)
                            radius: 6
                            color: root.bgElevated
                            border.color: root.borderMuted
                            border.width: 1

                            Column {
                                anchors.fill: parent
                                anchors.margins: root.spacingMd
                                spacing: root.spacingSm

                                Text {
                                    text: "Прогон эвристики"
                                    color: "#9fbbe0"
                                    font.pixelSize: Math.round(10 * root.uiScale)
                                    font.bold: true
                                    font.letterSpacing: 0.8
                                }
                                ComboBox {
                                    id: heurRunCombo
                                    width: parent.width
                                    height: Math.round(34 * root.uiScale)
                                    model: controller.heuristicMetricsRuns
                                    textRole: "label"
                                    currentIndex: _runComboIndex()
                                    enabled: count > 0
                                    onActivated: function(index) {
                                        var runs = controller.heuristicMetricsRuns || []
                                        if (index >= 0 && index < runs.length) {
                                            controller.selectHeuristicMetricsRun(String(runs[index].run_id))
                                        }
                                    }
                                    contentItem: Text {
                                        text: heurRunCombo.displayText.length > 0 ? heurRunCombo.displayText : "Нет сохранённых прогонов"
                                        color: heurRunCombo.enabled ? root.textPrimary : root.textSecondary
                                        font.pixelSize: root.evalCaptionSize
                                        elide: Text.ElideRight
                                        verticalAlignment: Text.AlignVCenter
                                        leftPadding: root.spacingSm
                                    }
                                    background: Rectangle {
                                        color: root.bgSurface
                                        border.color: heurRunCombo.activeFocus ? root.accentPrimaryAction : root.borderMuted
                                        border.width: 1
                                        radius: 4
                                    }
                                }
                                Text {
                                    width: parent.width
                                    text: "По умолчанию открывается последний snapshot; здесь можно выбрать любой сохранённый run."
                                    color: root.textSecondary
                                    font.pixelSize: Math.round(10 * root.uiScale)
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        Rectangle {
                            width: parent.width - runSelectorCard.width - root.spacingSm
                            height: Math.round(138 * root.uiScale)
                            radius: 6
                            color: root.bgElevated
                            border.color: root.borderMuted
                            border.width: 1
                            clip: true

                            Rectangle {
                                anchors.left: parent.left
                                anchors.top: parent.top
                                anchors.bottom: parent.bottom
                                width: 3
                                color: "#7db4f5"
                            }

                            Column {
                                anchors.fill: parent
                                anchors.margins: root.spacingMd
                                spacing: root.spacingSm

                                Row {
                                    width: parent.width
                                    spacing: root.spacingSm

                                    Rectangle {
                                        width: Math.round(42 * root.uiScale)
                                        height: width
                                        radius: 6
                                        color: "#132943"
                                        border.color: "#2f6ed8"
                                        border.width: 1
                                        Text {
                                            anchors.centerIn: parent
                                            text: String(summaryCol.md.matchup_model_algo_label || "AI").substring(0, 3)
                                            color: "#dcecff"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            font.bold: true
                                        }
                                    }

                                    Column {
                                        width: parent.width - Math.round(42 * root.uiScale) - statusBadge.width - 2 * root.spacingSm
                                        spacing: 1
                                        Text {
                                            text: "ОППОНЕНТ ЭВРИСТИКИ В ВЫБРАННОМ ПРОГОНЕ"
                                            color: "#9fbbe0"
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            font.bold: true
                                            font.letterSpacing: 0.8
                                        }
                                        Text {
                                            width: parent.width
                                            text: String(summaryCol.md.matchup_model_algo_label || "Модель") + " · " + String(summaryCol.md.matchup_model_name || "не указана")
                                            color: root.textPrimary
                                            font.pixelSize: Math.round(14 * root.uiScale)
                                            font.bold: true
                                            elide: Text.ElideRight
                                        }
                                        Text {
                                            width: parent.width
                                            text: String(summaryCol.md.matchup_model_path || "Путь к модели не найден в snapshot/data-json")
                                            color: root.textSecondary
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            elide: Text.ElideMiddle
                                        }
                                    }

                                    Rectangle {
                                        id: statusBadge
                                        width: statusText.implicitWidth + Math.round(14 * root.uiScale)
                                        height: Math.round(22 * root.uiScale)
                                        radius: height / 2
                                        color: "#0d2918"
                                        border.color: "#1f5030"
                                        border.width: 1
                                        Text {
                                            id: statusText
                                            anchors.centerIn: parent
                                            text: summaryCol.md.matchup_status || "частично"
                                            color: "#8ee0a9"
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            font.bold: true
                                        }
                                    }
                                }

                                Row {
                                    width: parent.width
                                    spacing: root.spacingSm
                                    Repeater {
                                        model: [
                                            ["Эпизодов модели", "matchup_model_episodes", "int"],
                                            ["Сторона эвристики", "heuristic_side", "str"],
                                            ["Сценарий", "matchup_scenario", "str"]
                                        ]
                                        delegate: Rectangle {
                                            width: (parent.width - 2 * root.spacingSm) / 3
                                            height: Math.round(40 * root.uiScale)
                                            radius: 5
                                            color: root.bgSurface
                                            border.color: "#24354c"
                                            border.width: 1
                                            Column {
                                                anchors.fill: parent
                                                anchors.margins: Math.round(6 * root.uiScale)
                                                spacing: 1
                                                Text {
                                                    width: parent.width
                                                    text: modelData[0]
                                                    color: root.textSecondary
                                                    font.pixelSize: Math.round(8 * root.uiScale)
                                                    elide: Text.ElideRight
                                                }
                                                Text {
                                                    width: parent.width
                                                    text: modelData[2] === "int"
                                                        ? _intText(summaryCol.md[modelData[1]])
                                                        : String(summaryCol.md[modelData[1]] || "—")
                                                    color: root.textPrimary
                                                    font.pixelSize: Math.round(11 * root.uiScale)
                                                    font.bold: true
                                                    elide: Text.ElideRight
                                                }
                                            }
                                        }
                                    }
                                }

                                Text {
                                    width: parent.width
                                    text: String(summaryCol.md.matchup_source_note || "")
                                    color: root.textSecondary
                                    font.pixelSize: Math.round(10 * root.uiScale)
                                    elide: Text.ElideRight
                                }
                            }
                        }
                    }

                    Row {
                        spacing: root.spacingSm
                        width: parent.width

                        Repeater {
                            model: [
                                { label: "Победы", key: "winrate", note: "баланс около целевого диапазона", color: "#4caf6e", kind: "pct" },
                                { label: "Разнообразие стилей", key: "entropy", note: "режимы не схлопнулись в один паттерн", color: "#7db4f5", kind: "raw" },
                                { label: "Ничьи", key: "draw_rate", note: "низкий draw rate, без тревоги", color: "#b88a26", kind: "pct" },
                            ]
                            delegate: Rectangle {
                                width: (parent.width - 2 * root.spacingSm) / 3
                                height: Math.round(86 * root.uiScale)
                                color: root.bgElevated
                                border.color: root.borderMuted
                                border.width: 1
                                radius: 6
                                property real rawVal: Number(summaryCol.md[modelData.key] || 0)
                                property string displayVal: modelData.kind === "pct" ? _pct(rawVal, 1) : _fmt(rawVal, 3)

                                Rectangle {
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.bottom: parent.bottom
                                    width: 3
                                    color: modelData.color
                                }

                                Column {
                                    anchors.fill: parent
                                    anchors.margins: root.spacingMd
                                    spacing: root.spacingSm
                                    Text {
                                        text: modelData.label.toUpperCase()
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                        color: root.textSecondary
                                        font.letterSpacing: 0.8
                                    }
                                    Text {
                                        text: parent.parent.displayVal
                                        font.pixelSize: Math.round(25 * root.uiScale)
                                        font.bold: true
                                        color: modelData.color
                                    }
                                    Text {
                                        width: parent.width
                                        text: modelData.note
                                        font.pixelSize: Math.round(10 * root.uiScale)
                                        color: root.textSecondary
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }
                    }

                    Row {
                        width: parent.width
                        spacing: root.spacingSm

                        GroupBox {
                            id: sumMetricsCard
                            width: (parent.width - root.spacingSm) / 2
                            height: Math.max(sumMetricsCard.implicitHeight, sumStyleCard.implicitHeight)
                            title: "Качество решений"
                            label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                            background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1; radius: 6 }

                            Column {
                                width: parent.width
                                spacing: Math.round(6 * root.uiScale)
                                Repeater {
                                    model: [
                                        ["Резервный выбор", "fallback_rate", "pct"],
                                        ["Ошибочные действия", "invalid_rate", "pct"],
                                        ["Избыточная стрельба", "shoot_overkill_rate", "pct"],
                                        ["Успешные чарджи", "charge_success_rate", "pct"],
                                        ["Средний риск", "avg_risk", "raw"],
                                        ["Среднее укрытие", "avg_cover", "raw"],
                                    ]
                                    delegate: Rectangle {
                                        width: parent.width
                                        height: Math.round(28 * root.uiScale)
                                        radius: 4
                                        color: root.bgSurface
                                        border.color: "#24354c"
                                        border.width: 1
                                        property real raw: Number(summaryCol.md[modelData[1]] || 0)
                                        Row {
                                            anchors.fill: parent
                                            anchors.leftMargin: root.spacingSm
                                            anchors.rightMargin: root.spacingSm
                                            spacing: root.spacingSm
                                            Text {
                                                text: modelData[0]
                                                color: root.textSecondary
                                                font.pixelSize: root.evalCaptionSize
                                                width: parent.width - Math.round(190 * root.uiScale)
                                                verticalAlignment: Text.AlignVCenter
                                                elide: Text.ElideRight
                                            }
                                            Text {
                                                text: modelData[2] === "pct" ? _pct(parent.parent.raw, 1) : _fmt(parent.parent.raw, 3)
                                                color: root.textPrimary
                                                font.pixelSize: root.evalCaptionSize
                                                font.family: "JetBrains Mono"
                                                width: Math.round(70 * root.uiScale)
                                                verticalAlignment: Text.AlignVCenter
                                                horizontalAlignment: Text.AlignRight
                                            }
                                            Rectangle {
                                                width: Math.round(96 * root.uiScale)
                                                height: Math.round(18 * root.uiScale)
                                                radius: height / 2
                                                color: "#111b2b"
                                                border.color: _qualityBadgeColor(modelData[1], parent.parent.raw)
                                                border.width: 1
                                                anchors.verticalCenter: parent.verticalCenter
                                                Text {
                                                    anchors.centerIn: parent
                                                    text: _qualityBadge(modelData[1], parent.parent.parent.raw)
                                                    color: _qualityBadgeColor(modelData[1], parent.parent.parent.raw)
                                                    font.pixelSize: Math.round(10 * root.uiScale)
                                                    font.bold: true
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        GroupBox {
                            id: sumStyleCard
                            width: (parent.width - root.spacingSm) / 2
                            height: Math.max(sumMetricsCard.implicitHeight, sumStyleCard.implicitHeight)
                            title: "Стиль игры"
                            label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                            background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1; radius: 6 }

                            Column {
                                id: styleCol
                                width: parent.width
                                spacing: Math.round(6 * root.uiScale)
                                property real modeTotal: Math.max(1, (summaryCol.md.mode_kite || 0) + (summaryCol.md.mode_hold || 0) + (summaryCol.md.mode_commit || 0))
                                property real roleTotal: Math.max(1, (summaryCol.md.role_ranged || 0) + (summaryCol.md.role_hybrid || 0) + (summaryCol.md.role_melee || 0))

                                Text { text: "Режимы"; color: root.textSecondary; font.pixelSize: Math.round(10 * root.uiScale); font.bold: true }
                                Repeater {
                                    model: [
                                        ["kite",   "mode_kite",   "#7db4f5"],
                                        ["hold",   "mode_hold",   "#b88a26"],
                                        ["commit", "mode_commit", "#4caf6e"],
                                    ]
                                    delegate: Column {
                                        width: styleCol.width
                                        spacing: 1
                                        property real pct: ((summaryCol.md[modelData[1]] || 0) / styleCol.modeTotal) * 100
                                        Row {
                                            width: parent.width
                                            Text { text: modelData[0]; color: modelData[2]; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"; width: Math.round(70 * root.uiScale) }
                                            Text { text: _fmt(parent.parent.pct, 0) + "%"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"; width: Math.round(44 * root.uiScale); horizontalAlignment: Text.AlignRight }
                                        }
                                        Rectangle {
                                            width: parent.width; height: Math.round(8 * root.uiScale); radius: 4; color: "#0a0f1a"
                                            Rectangle { width: parent.width * parent.parent.pct / 100; height: parent.height; radius: 3; color: modelData[2] }
                                        }
                                    }
                                }

                                Item { width: 1; height: Math.round(6 * root.uiScale) }
                                Text { text: "Роли"; color: root.textSecondary; font.pixelSize: Math.round(10 * root.uiScale); font.bold: true }
                                Repeater {
                                    model: [
                                        ["ranged", "role_ranged", "#7db4f5"],
                                        ["hybrid", "role_hybrid", "#b88a26"],
                                        ["melee",  "role_melee",  "#cf3f3f"],
                                    ]
                                    delegate: Column {
                                        width: styleCol.width
                                        spacing: 1
                                        property real pct: ((summaryCol.md[modelData[1]] || 0) / styleCol.roleTotal) * 100
                                        Row {
                                            width: parent.width
                                            Text { text: modelData[0]; color: modelData[2]; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"; width: Math.round(70 * root.uiScale) }
                                            Text { text: _fmt(parent.parent.pct, 0) + "%"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"; width: Math.round(44 * root.uiScale); horizontalAlignment: Text.AlignRight }
                                        }
                                        Rectangle {
                                            width: parent.width; height: Math.round(8 * root.uiScale); radius: 4; color: "#0a0f1a"
                                            Rectangle { width: parent.width * parent.parent.pct / 100; height: parent.height; radius: 3; color: modelData[2] }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // ── Исходы по профилям ───────────────────────────────────
                    GroupBox {
                        width: parent.width
                        title: "Исходы по профилям"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1; radius: 6 }

                        Column {
                            id: profCol
                            width: parent.width
                            spacing: 0
                            property var profs: (controller.heuristicMetricsDict && controller.heuristicMetricsDict.profiles)
                                ? controller.heuristicMetricsDict.profiles : []

                            Rectangle {
                                width: parent.width; height: Math.round(20 * root.uiScale); color: root.bgSurface
                                Row {
                                    anchors.fill: parent
                                    Repeater {
                                        model: [["профиль", 130], ["игр", 70], ["win", 70], ["draw", 70], ["сигнал", 0], ["статус", 90]]
                                        delegate: Text {
                                            text: modelData[0]; color: root.textSecondary
                                            font.pixelSize: Math.round(9 * root.uiScale)
                                            width: modelData[1] > 0 ? Math.round(modelData[1] * root.uiScale) : parent.width - Math.round(430 * root.uiScale)
                                            leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                }
                            }
                            Repeater {
                                model: profCol.profs
                                delegate: Rectangle {
                                    width: parent.width; height: Math.round(24 * root.uiScale)
                                    color: index % 2 === 0 ? root.bgElevated : root.bgSurface
                                    Row {
                                        anchors.fill: parent
                                        Text { text: modelData.name; color: root.textPrimary; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(130 * root.uiScale); leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter }
                                        Text { text: modelData.games; color: root.textSecondary; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(70 * root.uiScale); leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter }
                                        Text { text: _pct(modelData.win, 0); color: modelData.win < 0.48 ? "#b88a26" : "#4caf6e"; font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(70 * root.uiScale); leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter }
                                        Text { text: _pct(modelData.draw, 1)
                                            color: modelData.draw > 0.012 ? "#b88a26" : root.textPrimary
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            width: Math.round(70 * root.uiScale); leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter }
                                        Item {
                                            width: parent.width - Math.round(430 * root.uiScale); height: parent.height
                                            Rectangle {
                                                anchors.verticalCenter: parent.verticalCenter; x: root.spacingSm
                                                width: (parent.width - 2 * root.spacingSm) * Math.max(0, Math.min(1, modelData.win)); height: Math.round(6 * root.uiScale)
                                                radius: 3; color: modelData.win >= 0.50 ? "#b88a26" : "#4caf6e"
                                            }
                                        }
                                        Rectangle {
                                            width: Math.round(86 * root.uiScale)
                                            height: Math.round(18 * root.uiScale)
                                            radius: height / 2
                                            color: "#111b2b"
                                            border.color: _profileStatusColor(modelData.win, modelData.draw)
                                            border.width: 1
                                            anchors.verticalCenter: parent.verticalCenter
                                            Text {
                                                anchors.centerIn: parent
                                                text: _profileStatus(modelData.win, modelData.draw)
                                                color: _profileStatusColor(modelData.win, modelData.draw)
                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                font.bold: true
                                            }
                                        }
                                    }
                                }
                            }
                            Text {
                                visible: profCol.profs.length === 0
                                text: "Нет данных по профилям (нужны записи heur_decisions за прогон)."
                                color: root.textSecondary; font.pixelSize: root.evalCaptionSize
                                leftPadding: root.spacingSm; topPadding: root.spacingSm
                            }
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
                    property real calZoom: 1.15
                    width: innerStack.width / calZoom
                    scale: calZoom
                    transformOrigin: Item.TopLeft
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
                    // Лёгкий зум всей вкладки (на больших мониторах мелко).
                    // distance-field текст масштабируется без размытия.
                    property real calZoom: 1.12
                    width: innerStack.width / calZoom
                    scale: calZoom
                    transformOrigin: Item.TopLeft
                    topPadding: root.spacingMd

                    // ═══ Двухколоночная раскладка: пульт слева, лидерборд справа ═══
                    RowLayout {
                        width: parent.width
                        spacing: root.spacingMd

                        // ─────────────── ЛЕВАЯ КОЛОНКА: пульт запуска ───────────────
                        ColumnLayout {
                            Layout.preferredWidth: Math.round(parent.width * 0.35)
                            Layout.minimumWidth: Math.round(320 * root.uiScale)
                            Layout.alignment: Qt.AlignTop
                            spacing: root.spacingMd

                    GroupBox {
                        Layout.fillWidth: true
                        title: "Конфигурация запуска"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ColumnLayout {
                            width: parent.width
                            spacing: root.spacingSm

                            // ── Профили прогона (пресеты) ─────────────────────────────
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Repeater {
                                    model: [
                                        { label: "Быстрый",  c: 10, g: 20  },
                                        { label: "Стандарт", c: 40, g: 50  },
                                        { label: "Глубокий", c: 80, g: 200 },
                                    ]
                                    delegate: Button {
                                        id: presetBtn
                                        Layout.fillWidth: true
                                        enabled: !heurCalRunner.isRunning
                                        implicitHeight: Math.round(34 * root.uiScale)
                                        property bool active: parseInt(calCandidatesInput.text) === modelData.c
                                                           && parseInt(calGamesInput.text) === modelData.g
                                        onClicked: {
                                            calCandidatesInput.text = "" + modelData.c
                                            calGamesInput.text = "" + modelData.g
                                        }
                                        contentItem: Column {
                                            spacing: 0
                                            Text {
                                                anchors.horizontalCenter: parent.horizontalCenter
                                                text: modelData.label
                                                color: presetBtn.active ? "#e8c060" : root.textPrimary
                                                font.pixelSize: Math.round(11 * root.uiScale); font.bold: presetBtn.active
                                            }
                                            Text {
                                                anchors.horizontalCenter: parent.horizontalCenter
                                                text: modelData.c + "×" + modelData.g
                                                color: root.textSecondary
                                                font.pixelSize: Math.round(9 * root.uiScale); font.family: "JetBrains Mono"
                                            }
                                        }
                                        background: Rectangle {
                                            radius: Math.round(5 * root.uiScale)
                                            color: presetBtn.active ? "#15130a" : root.bgSurface
                                            border.color: presetBtn.active ? "#b88a26" : root.borderMuted; border.width: 1
                                        }
                                    }
                                }
                            }

                            // ── Кандидатов (степпер −/+, колесо мыши, валидация) ──────
                            Rectangle {
                                Layout.fillWidth: true
                                implicitHeight: Math.round(36 * root.uiScale)
                                color: "#0a0f1a"; radius: Math.round(5 * root.uiScale)
                                border.width: 1
                                border.color: heurPanel._numValid(calCandidatesInput.text, 1) ? root.borderMuted : "#cf3f3f"
                                HoverHandler { id: candHover }
                                ToolTip.visible: candHover.hovered
                                ToolTip.text: "Сколько наборов весов перебрать. Больше — точнее подбор, но дольше прогон."
                                WheelHandler { onWheel: function(e) { if (!heurCalRunner.isRunning) heurPanel._bump(calCandidatesInput, e.angleDelta.y > 0 ? 5 : -5, 1) } }
                                Text {
                                    anchors.left: parent.left; anchors.leftMargin: root.spacingSm
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: "Кандидатов"; color: root.textSecondary; font.pixelSize: Math.round(11 * root.uiScale)
                                }
                                Row {
                                    anchors.right: parent.right; anchors.rightMargin: Math.round(4 * root.uiScale)
                                    anchors.verticalCenter: parent.verticalCenter
                                    spacing: Math.round(3 * root.uiScale)
                                    Rectangle {
                                        width: Math.round(24 * root.uiScale); height: Math.round(26 * root.uiScale); radius: Math.round(4 * root.uiScale)
                                        color: stepCandMinus.pressed ? "#0d1422" : root.bgSurface; border.color: root.borderMuted; border.width: 1
                                        Text { anchors.centerIn: parent; text: "−"; color: root.textPrimary; font.pixelSize: Math.round(14 * root.uiScale) }
                                        MouseArea { id: stepCandMinus; anchors.fill: parent; enabled: !heurCalRunner.isRunning; onClicked: heurPanel._bump(calCandidatesInput, -5, 1) }
                                    }
                                    TextField {
                                        id: calCandidatesInput; text: "40"
                                        anchors.verticalCenter: parent.verticalCenter
                                        validator: IntValidator { bottom: 1; top: 999 }
                                        horizontalAlignment: Text.AlignHCenter
                                        font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                        color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                        implicitWidth: Math.round(44 * root.uiScale)
                                        padding: 0
                                        background: Rectangle { color: "transparent" }
                                    }
                                    Rectangle {
                                        width: Math.round(24 * root.uiScale); height: Math.round(26 * root.uiScale); radius: Math.round(4 * root.uiScale)
                                        color: stepCandPlus.pressed ? "#0d1422" : root.bgSurface; border.color: root.borderMuted; border.width: 1
                                        Text { anchors.centerIn: parent; text: "+"; color: root.textPrimary; font.pixelSize: Math.round(14 * root.uiScale) }
                                        MouseArea { id: stepCandPlus; anchors.fill: parent; enabled: !heurCalRunner.isRunning; onClicked: heurPanel._bump(calCandidatesInput, 5, 1) }
                                    }
                                }
                            }

                            // ── Игр (степпер −/+, колесо мыши, валидация) ─────────────
                            Rectangle {
                                Layout.fillWidth: true
                                implicitHeight: Math.round(36 * root.uiScale)
                                color: "#0a0f1a"; radius: Math.round(5 * root.uiScale)
                                border.width: 1
                                border.color: heurPanel._numValid(calGamesInput.text, 1) ? root.borderMuted : "#cf3f3f"
                                HoverHandler { id: gamesHover }
                                ToolTip.visible: gamesHover.hovered
                                ToolTip.text: "Сколько партий играет каждый кандидат. Больше — стабильнее winrate, но дольше."
                                WheelHandler { onWheel: function(e) { if (!heurCalRunner.isRunning) heurPanel._bump(calGamesInput, e.angleDelta.y > 0 ? 10 : -10, 1) } }
                                Text {
                                    anchors.left: parent.left; anchors.leftMargin: root.spacingSm
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: "Игр"; color: root.textSecondary; font.pixelSize: Math.round(11 * root.uiScale)
                                }
                                Row {
                                    anchors.right: parent.right; anchors.rightMargin: Math.round(4 * root.uiScale)
                                    anchors.verticalCenter: parent.verticalCenter
                                    spacing: Math.round(3 * root.uiScale)
                                    Rectangle {
                                        width: Math.round(24 * root.uiScale); height: Math.round(26 * root.uiScale); radius: Math.round(4 * root.uiScale)
                                        color: stepGamesMinus.pressed ? "#0d1422" : root.bgSurface; border.color: root.borderMuted; border.width: 1
                                        Text { anchors.centerIn: parent; text: "−"; color: root.textPrimary; font.pixelSize: Math.round(14 * root.uiScale) }
                                        MouseArea { id: stepGamesMinus; anchors.fill: parent; enabled: !heurCalRunner.isRunning; onClicked: heurPanel._bump(calGamesInput, -10, 1) }
                                    }
                                    TextField {
                                        id: calGamesInput; text: "50"
                                        anchors.verticalCenter: parent.verticalCenter
                                        validator: IntValidator { bottom: 1; top: 9999 }
                                        horizontalAlignment: Text.AlignHCenter
                                        font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                        color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                        implicitWidth: Math.round(44 * root.uiScale)
                                        padding: 0
                                        background: Rectangle { color: "transparent" }
                                    }
                                    Rectangle {
                                        width: Math.round(24 * root.uiScale); height: Math.round(26 * root.uiScale); radius: Math.round(4 * root.uiScale)
                                        color: stepGamesPlus.pressed ? "#0d1422" : root.bgSurface; border.color: root.borderMuted; border.width: 1
                                        Text { anchors.centerIn: parent; text: "+"; color: root.textPrimary; font.pixelSize: Math.round(14 * root.uiScale) }
                                        MouseArea { id: stepGamesPlus; anchors.fill: parent; enabled: !heurCalRunner.isRunning; onClicked: heurPanel._bump(calGamesInput, 10, 1) }
                                    }
                                }
                            }

                            // ── Оценка объёма прогона ─────────────────────────────────
                            Text {
                                Layout.fillWidth: true
                                color: heurPanel._paramsValid() ? root.textSecondary : "#cf3f3f"
                                font.pixelSize: Math.round(10 * root.uiScale); font.family: "JetBrains Mono"
                                wrapMode: Text.WordWrap
                                text: heurPanel._estimateText()
                            }

                            // ── Агент (на видном месте, вне «Дополнительно») ──────────
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: Math.round(36 * root.uiScale)
                                    color: "#0a0f1a"; border.color: root.borderMuted; border.width: 1
                                    radius: Math.round(5 * root.uiScale)
                                    HoverHandler { id: agentHover }
                                    ToolTip.visible: agentHover.hovered
                                    ToolTip.text: "Learner-агент. Эвристика калибруется на противоположной стороне."
                                    Text {
                                        id: agentLbl
                                        anchors.left: parent.left; anchors.leftMargin: root.spacingSm
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: "Агент"; color: root.textSecondary
                                        font.pixelSize: Math.round(11 * root.uiScale)
                                    }
                                    ComboBox {
                                        id: calAgentCombo
                                        anchors.left: agentLbl.right; anchors.leftMargin: Math.round(6 * root.uiScale)
                                        anchors.right: parent.right; anchors.rightMargin: Math.round(4 * root.uiScale)
                                        anchors.verticalCenter: parent.verticalCenter
                                        enabled: !heurCalRunner.isRunning
                                        model: controller.calibrationAgents
                                        textRole: "label"
                                        font.pixelSize: root.evalCaptionSize
                                        contentItem: Text {
                                            text: calAgentCombo.displayText
                                            color: root.textPrimary
                                            font: calAgentCombo.font
                                            horizontalAlignment: Text.AlignRight
                                            verticalAlignment: Text.AlignVCenter
                                            elide: Text.ElideLeft
                                        }
                                        background: Rectangle { color: "transparent" }
                                    }
                                }
                                Button {
                                    text: "⟳"
                                    enabled: !heurCalRunner.isRunning
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: controller.refreshCalibrationAgents()
                                    contentItem: Text { text: parent.text; color: root.textSecondary; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1; radius: Math.round(5 * root.uiScale) }
                                    implicitWidth: Math.round(36 * root.uiScale)
                                    implicitHeight: Math.round(36 * root.uiScale)
                                }
                            }

                            // ── Дополнительно (Seed) — сворачиваемо ───────────────────
                            Item {
                                Layout.fillWidth: true
                                implicitHeight: Math.round(26 * root.uiScale)
                                Row {
                                    anchors.left: parent.left; anchors.verticalCenter: parent.verticalCenter
                                    spacing: Math.round(6 * root.uiScale)
                                    Text { text: heurPanel._advOpen ? "▾" : "▸"; color: root.textSecondary; font.pixelSize: Math.round(11 * root.uiScale) }
                                    Text { text: "Дополнительно"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                }
                                Text {
                                    visible: !heurPanel._advOpen
                                    anchors.right: parent.right; anchors.rightMargin: root.spacingSm
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: "seed " + calSeedInput.text
                                    color: "#5a6a82"; font.pixelSize: Math.round(9 * root.uiScale); font.family: "JetBrains Mono"
                                }
                                MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: heurPanel._advOpen = !heurPanel._advOpen }
                            }
                            ColumnLayout {
                                Layout.fillWidth: true
                                visible: heurPanel._advOpen
                                spacing: root.spacingSm

                                // Seed + 🎲 новый + копировать
                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: Math.round(36 * root.uiScale)
                                    color: "#0a0f1a"; radius: Math.round(5 * root.uiScale)
                                    border.width: 1
                                    border.color: heurPanel._numValid(calSeedInput.text, 0) ? root.borderMuted : "#cf3f3f"
                                    Text {
                                        anchors.left: parent.left; anchors.leftMargin: root.spacingSm
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: "Seed"; color: root.textSecondary; font.pixelSize: Math.round(11 * root.uiScale)
                                    }
                                    Row {
                                        anchors.right: parent.right; anchors.rightMargin: Math.round(4 * root.uiScale)
                                        anchors.verticalCenter: parent.verticalCenter
                                        spacing: Math.round(3 * root.uiScale)
                                        TextField {
                                            id: calSeedInput; text: "1390520"
                                            anchors.verticalCenter: parent.verticalCenter
                                            validator: IntValidator { bottom: 0 }
                                            horizontalAlignment: Text.AlignRight
                                            font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                            color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                            implicitWidth: Math.round(96 * root.uiScale)
                                            padding: 0
                                            background: Rectangle { color: "transparent" }
                                        }
                                        Rectangle {
                                            width: Math.round(28 * root.uiScale); height: Math.round(26 * root.uiScale); radius: Math.round(4 * root.uiScale)
                                            color: seedRandBtn.pressed ? "#0d1422" : root.bgSurface; border.color: root.borderMuted; border.width: 1
                                            Text { anchors.centerIn: parent; text: "🎲"; font.pixelSize: Math.round(13 * root.uiScale) }
                                            HoverHandler { id: seedRandHover }
                                            ToolTip.visible: seedRandHover.hovered; ToolTip.text: "Новый случайный сид"
                                            MouseArea { id: seedRandBtn; anchors.fill: parent; enabled: !heurCalRunner.isRunning; onClicked: calSeedInput.text = heurPanel._randomSeed() }
                                        }
                                        Rectangle {
                                            width: Math.round(28 * root.uiScale); height: Math.round(26 * root.uiScale); radius: Math.round(4 * root.uiScale)
                                            color: seedCopyBtn.pressed ? "#0d1422" : root.bgSurface; border.color: root.borderMuted; border.width: 1
                                            Text { anchors.centerIn: parent; text: "⧉"; color: root.textSecondary; font.pixelSize: Math.round(13 * root.uiScale) }
                                            HoverHandler { id: seedCopyHover }
                                            ToolTip.visible: seedCopyHover.hovered; ToolTip.text: "Скопировать сид"
                                            MouseArea { id: seedCopyBtn; anchors.fill: parent; onClicked: heurPanel._copyToClipboard(calSeedInput.text) }
                                        }
                                    }
                                }
                            }

                            // ── Режим цели: крупные карточки ──────────────────────────
                            Text {
                                text: "Режим цели"; color: root.textSecondary
                                font.pixelSize: root.evalCaptionSize
                                Layout.topMargin: root.spacingSm
                            }
                            Repeater {
                                model: [
                                    { label: "Спарринг", val: 0.50, desc: "сбалансированный враг", icon: "⚔", danger: false },
                                    { label: "Хард",     val: 0.65, desc: "сильнее игрока",        icon: "🛡", danger: false },
                                    { label: "Максимум", val: 1.00, desc: "максимум давления",     icon: "💀", danger: true  },
                                ]
                                delegate: Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: Math.round(50 * root.uiScale)
                                    radius: Math.round(6 * root.uiScale)
                                    property bool active: Math.abs(heurPanel.targetWinrate - modelData.val) < 0.001
                                    property color accent: modelData.danger ? "#cf3f3f" : "#b88a26"
                                    color: active ? (modelData.danger ? "#1c0c0c" : "#15130a") : root.bgSurface
                                    border.color: active ? accent : root.borderMuted
                                    border.width: active ? 2 : 1

                                    Text {
                                        id: tgtIcon
                                        anchors.left: parent.left; anchors.leftMargin: Math.round(12 * root.uiScale)
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: modelData.icon
                                        color: active ? accent : root.textSecondary
                                        font.pixelSize: Math.round(18 * root.uiScale)
                                    }
                                    Column {
                                        anchors.left: tgtIcon.right; anchors.leftMargin: Math.round(12 * root.uiScale)
                                        anchors.verticalCenter: parent.verticalCenter
                                        spacing: 0
                                        Text { text: modelData.label; color: active ? root.textPrimary : root.textSecondary
                                            font.pixelSize: Math.round(13 * root.uiScale); font.bold: active }
                                        Text { text: modelData.desc; color: root.textSecondary
                                            font.pixelSize: Math.round(10 * root.uiScale) }
                                    }
                                    Text {
                                        anchors.right: parent.right
                                        anchors.rightMargin: active ? Math.round(36 * root.uiScale) : Math.round(14 * root.uiScale)
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: modelData.val.toFixed(2)
                                        color: active ? accent : root.textSecondary
                                        font.pixelSize: Math.round(17 * root.uiScale); font.bold: true
                                        font.family: "JetBrains Mono"
                                    }
                                    Rectangle {
                                        visible: active
                                        anchors.right: parent.right; anchors.rightMargin: Math.round(10 * root.uiScale)
                                        anchors.verticalCenter: parent.verticalCenter
                                        width: Math.round(18 * root.uiScale); height: width; radius: width / 2
                                        color: accent
                                        Text { anchors.centerIn: parent; text: "✓"; color: "#0a0f1a"
                                            font.pixelSize: Math.round(11 * root.uiScale); font.bold: true }
                                    }
                                    MouseArea {
                                        anchors.fill: parent
                                        enabled: !heurCalRunner.isRunning
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            heurPanel.targetWinrate = modelData.val
                                            calTargetInput.text = modelData.val.toFixed(2)
                                        }
                                    }
                                }
                            }

                            // свой target + подпись стороны эвристики
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm
                                Text { text: "свой target:"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                                TextField {
                                    id: calTargetInput
                                    text: "0.50"
                                    validator: DoubleValidator { bottom: 0.0; top: 1.0; decimals: 2; notation: DoubleValidator.StandardNotation }
                                    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono"
                                    color: root.textPrimary; enabled: !heurCalRunner.isRunning
                                    implicitWidth: Math.round(56 * root.uiScale)
                                    horizontalAlignment: Text.AlignHCenter
                                    background: Rectangle { color: "#0a0f1a"; border.color: root.borderMuted; border.width: 1; radius: Math.round(4 * root.uiScale) }
                                    onEditingFinished: {
                                        var v = parseFloat(text)
                                        if (!isNaN(v) && v >= 0.0 && v <= 1.0) heurPanel.targetWinrate = v
                                    }
                                }
                                Item { Layout.fillWidth: true }
                            }
                            Text {
                                Layout.fillWidth: true
                                color: root.textSecondary; font.pixelSize: Math.round(10 * root.uiScale)
                                font.family: "JetBrains Mono"
                                wrapMode: Text.WordWrap
                                text: heurPanel.targetWinrate >= 0.95
                                    ? "макс. сила · эвристика " + _heuristicSide()
                                    : "цель winrate=" + heurPanel.targetWinrate.toFixed(2) + " · эвристика " + _heuristicSide()
                            }

                            // ── Запуск: крупный CTA, затем вторичные действия ─────────
                            Button {
                                visible: !heurCalRunner.isRunning
                                enabled: heurPanel._paramsValid()
                                Layout.fillWidth: true
                                Layout.topMargin: root.spacingSm
                                implicitHeight: Math.round(38 * root.uiScale)
                                text: "▶ Калибровать"
                                font.pixelSize: Math.round(14 * root.uiScale); font.bold: true
                                onClicked: {
                                    heurPanel._resetLeaderboard()
                                    heurPanel.bestCandidateIdx = -1
                                    heurPanel.bestScore = 0.0
                                    heurPanel.patchText = ""
                                    heurPanel.calDone = 0
                                    heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                    heurPanel._runGames = parseInt(calGamesInput.text)
                                    heurPanel._calStartMs = Date.now()
                                    heurPanel._calElapsed = 0
                                    var a = _selectedAgent()
                                    heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                      parseInt(calGamesInput.text),
                                                      parseInt(calSeedInput.text), false,
                                                      a.agent_id, a.side, heurPanel.targetWinrate)
                                }
                                contentItem: Text { text: parent.text; color: parent.enabled ? "#0a0f1a" : "#5a5230"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                background: Rectangle { radius: Math.round(5 * root.uiScale)
                                    color: !parent.enabled ? "#2a2410" : parent.down ? "#9a7420" : parent.hovered ? "#d0a030" : "#b88a26" }
                            }
                            Button {
                                visible: !heurCalRunner.isRunning
                                enabled: heurPanel._paramsValid()
                                Layout.fillWidth: true
                                implicitHeight: Math.round(32 * root.uiScale)
                                text: "Dry run"
                                font.pixelSize: root.evalCaptionSize
                                onClicked: {
                                    heurPanel._resetLeaderboard()
                                    heurPanel.bestCandidateIdx = -1
                                    heurPanel.calDone = 0
                                    heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                    heurPanel._runGames = parseInt(calGamesInput.text)
                                    heurPanel._calStartMs = Date.now()
                                    heurPanel._calElapsed = 0
                                    var a = _selectedAgent()
                                    heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                      parseInt(calGamesInput.text),
                                                      parseInt(calSeedInput.text), true,
                                                      a.agent_id, a.side, heurPanel.targetWinrate)
                                }
                                contentItem: Text { text: parent.text; color: parent.enabled ? root.textSecondary : "#3a4a5a"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                background: Rectangle { radius: Math.round(5 * root.uiScale)
                                    color: parent.down ? "#0d1422" : root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                            }
                            Text {
                                visible: !heurCalRunner.isRunning && !heurPanel._paramsValid()
                                Layout.fillWidth: true
                                text: "⚠ Заполните «Кандидатов», «Игр» и Seed корректными числами"
                                color: "#d08a5a"; font.pixelSize: Math.round(10 * root.uiScale)
                                wrapMode: Text.WordWrap
                            }
                            Button {
                                visible: heurCalRunner.isRunning
                                Layout.fillWidth: true
                                Layout.topMargin: root.spacingSm
                                implicitHeight: Math.round(38 * root.uiScale)
                                text: "■ Стоп"
                                font.pixelSize: Math.round(14 * root.uiScale); font.bold: true
                                onClicked: heurCalRunner.stop()
                                contentItem: Text { text: parent.text; color: "#e08a8a"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                background: Rectangle { radius: Math.round(5 * root.uiScale)
                                    color: parent.down ? "#1a0808" : "#1a0c0c"; border.color: "#6b2020"; border.width: 1 }
                            }

                            // прогресс + ETA
                            ColumnLayout {
                                Layout.fillWidth: true
                                Layout.topMargin: root.spacingSm
                                spacing: Math.round(4 * root.uiScale)
                                visible: heurCalRunner.isRunning || heurPanel.calDone > 0
                                RowLayout {
                                    Layout.fillWidth: true
                                    Text { text: "Прогресс"; color: root.textSecondary; font.pixelSize: Math.round(10 * root.uiScale) }
                                    Item { Layout.fillWidth: true }
                                    Text {
                                        text: heurPanel.calTotal > 0 ? Math.round(100 * heurPanel.calDone / heurPanel.calTotal) + "%" : "0%"
                                        color: root.textPrimary; font.pixelSize: Math.round(10 * root.uiScale)
                                        font.bold: true; font.family: "JetBrains Mono"
                                    }
                                }
                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: Math.round(8 * root.uiScale)
                                    color: "#0a0f1a"; border.color: root.borderMuted; border.width: 1
                                    radius: Math.round(3 * root.uiScale)
                                    Rectangle {
                                        x: 1; y: 1
                                        width: heurPanel.calTotal > 0
                                            ? Math.max(height, (parent.width - 2) * heurPanel.calDone / heurPanel.calTotal)
                                            : 0
                                        height: parent.height - 2; radius: parent.radius
                                        color: heurPanel.targetWinrate >= 0.95 ? "#cf3f3f" : "#b88a26"
                                        opacity: heurPanel.calDone > 0 ? 1.0 : 0.0
                                        Behavior on width { NumberAnimation { duration: 300 } }
                                    }
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: heurPanel.calDone + " / " + heurPanel.calTotal
                                        + (heurPanel._etaText() ? " · " + heurPanel._etaText() : "")
                                        + (heurPanel.bestCandidateIdx >= 0 ? " · лучший " + _fmt(heurPanel.bestScore, 3) : "")
                                    color: root.textSecondary; font.pixelSize: Math.round(10 * root.uiScale)
                                    font.family: "JetBrains Mono"; wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }

                        } // ← конец ЛЕВОЙ колонки

                        // ─────────────── ПРАВАЯ КОЛОНКА: лидерборд ───────────────
                        ColumnLayout {
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignTop
                            spacing: root.spacingMd

                            // ── hero «Лучший кандидат» ──
                            Rectangle {
                                Layout.fillWidth: true
                                visible: heurPanel.bestCandidateIdx >= 0
                                radius: Math.round(6 * root.uiScale)
                                color: "#0d2010"; border.color: "#1f5030"; border.width: 1
                                implicitHeight: heroCol.implicitHeight + 2 * root.spacingMd

                                ColumnLayout {
                                    id: heroCol
                                    anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top
                                    anchors.margins: root.spacingMd
                                    spacing: root.spacingSm

                                    Text {
                                        text: "🏆 Лучший кандидат #" + heurPanel.bestCandidateIdx
                                        color: "#4caf6e"; font.pixelSize: root.evalCaptionSize; font.bold: true
                                    }
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingMd
                                        Text {
                                            text: _fmt(heurPanel.bestScore, 3); color: "#4caf6e"
                                            font.pixelSize: Math.round(30 * root.uiScale); font.bold: true
                                            font.family: "JetBrains Mono"
                                        }
                                        Text {
                                            Layout.alignment: Qt.AlignVCenter
                                            visible: heurPanel._top3.length > 0
                                            text: heurPanel._top3.length > 0
                                                ? "winrate " + heurPanel._top3[0].winrate
                                                  + "   ·   entropy " + heurPanel._top3[0].entropy
                                                  + "   ·   draws " + heurPanel._top3[0].draws
                                                : ""
                                            color: root.textSecondary; font.pixelSize: root.evalCaptionSize
                                            font.family: "JetBrains Mono"
                                        }
                                        Item { Layout.fillWidth: true }
                                    }
                                    TextArea {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(74 * root.uiScale)
                                        // Патч-файл пишется только при ПОЛНОМ завершении калибровки.
                                        text: heurPanel.patchText.length > 0
                                            ? heurPanel.patchText
                                            : heurCalRunner.isRunning
                                                ? "(Идёт калибровка — патч появится после прохода всех кандидатов)"
                                                : "(Патч создаётся только при полном завершении. Остановленный прогон патча не даёт.)"
                                        readOnly: true
                                        color: "#7db4f5"
                                        font.pixelSize: Math.round(10 * root.uiScale); font.family: "JetBrains Mono"
                                        background: Rectangle { color: root.bgSurface; border.color: root.borderMuted; border.width: 1; radius: Math.round(4 * root.uiScale) }
                                    }
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Button {
                                            text: "✓ Применить патч"
                                            font.pixelSize: root.evalCaptionSize
                                            enabled: !heurCalRunner.isRunning && heurPanel.patchText.length > 0
                                            onClicked: heurCalRunner.applyPatch(heurCalRunner.currentRunDir)
                                            contentItem: Text { text: parent.text; color: parent.enabled ? "#0a0f1a" : "#6b5010"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                            background: Rectangle { radius: Math.round(5 * root.uiScale)
                                                color: parent.enabled ? (parent.down ? "#9a7420" : parent.hovered ? "#d0a030" : "#b88a26") : "#2a2410" }
                                        }
                                        Button {
                                            text: "Открыть папку"
                                            font.pixelSize: root.evalCaptionSize
                                            enabled: heurCalRunner.currentRunDir.length > 0
                                            onClicked: Qt.openUrlExternally("file:///" + heurCalRunner.currentRunDir)
                                            contentItem: Text { text: parent.text; color: parent.enabled ? root.textSecondary : "#3a4a5a"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                            background: Rectangle { radius: Math.round(5 * root.uiScale)
                                                color: root.bgSurface; border.color: root.borderMuted; border.width: 1 }
                                        }
                                        Text {
                                            id: patchStatusText
                                            text: ""
                                            font.pixelSize: root.evalCaptionSize
                                            font.family: "JetBrains Mono"
                                        }
                                        Item { Layout.fillWidth: true }
                                    }
                                }
                            }

                            // ── empty-state (до первого результата) ──
                            Rectangle {
                                Layout.fillWidth: true
                                visible: heurPanel.bestCandidateIdx < 0
                                implicitHeight: Math.round(96 * root.uiScale)
                                radius: Math.round(6 * root.uiScale)
                                color: root.bgElevated; border.color: root.borderMuted; border.width: 1
                                Column {
                                    anchors.centerIn: parent
                                    spacing: Math.round(4 * root.uiScale)
                                    Text {
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        text: "🏁"; font.pixelSize: Math.round(24 * root.uiScale); color: root.textSecondary
                                    }
                                    Text {
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        text: heurCalRunner.isRunning
                                            ? "Идёт калибровка — кандидаты появятся в таблице ниже"
                                            : "Запустите калибровку, чтобы подобрать веса эвристики"
                                        color: root.textSecondary; font.pixelSize: root.evalCaptionSize
                                    }
                                }
                            }

                    GroupBox {
                        Layout.fillWidth: true
                        title: "Кандидаты — live"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        ListModel { id: candidatesModel }

                        Column {
                            width: parent.width
                            spacing: 0

                            // ── Подиум топ-3 ───────────────────────────────────
                            Row {
                                width: parent.width
                                spacing: root.spacingSm
                                visible: heurPanel._top3.length > 0
                                bottomPadding: root.spacingMd
                                Repeater {
                                    model: heurPanel._top3
                                    delegate: Rectangle {
                                        // фиксированная ширина — 1 победитель = аккуратная карточка, не пустой баннер
                                        width: Math.round(240 * root.uiScale)
                                        height: Math.round(64 * root.uiScale)
                                        radius: Math.round(4 * root.uiScale)
                                        property color medalColor: index === 0 ? "#b88a26" : index === 1 ? "#9aa7b8" : "#a06a3a"
                                        color: index === 0 ? "#15130a" : root.bgSurface
                                        border.color: medalColor; border.width: index === 0 ? 2 : 1

                                        // медаль + место слева
                                        Rectangle {
                                            id: podMedal
                                            x: Math.round(10 * root.uiScale); anchors.verticalCenter: parent.verticalCenter
                                            width: Math.round(26 * root.uiScale); height: Math.round(26 * root.uiScale); radius: width / 2
                                            color: medalColor
                                            Text { anchors.centerIn: parent; text: index + 1; color: "#0a0f1a"
                                                font.pixelSize: Math.round(13 * root.uiScale); font.bold: true }
                                        }
                                        // данные справа от медали
                                        Column {
                                            anchors.left: podMedal.right; anchors.leftMargin: Math.round(10 * root.uiScale)
                                            anchors.verticalCenter: parent.verticalCenter
                                            spacing: Math.round(1 * root.uiScale)
                                            Text {
                                                text: "#" + (modelData.idxNum >= 0 ? modelData.idxNum : "?")
                                                color: root.textSecondary; font.family: "JetBrains Mono"
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Text {
                                                text: modelData.score
                                                color: index === 0 ? "#4caf6e" : root.textPrimary
                                                font.family: "JetBrains Mono"; font.bold: true
                                                font.pixelSize: Math.round(18 * root.uiScale)
                                            }
                                            Text {
                                                text: "wr " + modelData.winrate + " · ent " + modelData.entropy
                                                color: root.textSecondary; font.family: "JetBrains Mono"
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                        }
                                    }
                                }
                            }

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
                                height: Math.min(candidatesModel.count * Math.round(28 * root.uiScale), Math.round(360 * root.uiScale))
                                model: candidatesModel
                                clip: true
                                ScrollBar.vertical: ScrollBar {}

                                delegate: Rectangle {
                                    width: ListView.view.width
                                    height: Math.round(28 * root.uiScale)
                                    color: model.isBest ? "#0d2010"
                                         : index % 2 === 0 ? root.bgElevated : root.bgSurface

                                    // акцент-полоса слева у лучшего
                                    Rectangle {
                                        visible: model.isBest
                                        anchors.left: parent.left; anchors.top: parent.top; anchors.bottom: parent.bottom
                                        width: Math.round(3 * root.uiScale)
                                        color: "#4caf6e"
                                    }

                                    Row {
                                        anchors.fill: parent
                                        // Явные колонки: читаем model.* напрямую (вложенный Repeater
                                        // с массивом [model.*] ловит коллизию имени model → пустые ячейки).
                                        // место — медаль ранга
                                        Item {
                                            width: Math.round(46 * root.uiScale); height: parent.height
                                            Rectangle {
                                                // медаль только у принятых (ok) в топ-3; отклонённые — простой номер
                                                property bool isMedal: model.status === "ok" && model.rank <= 3
                                                x: root.spacingSm; anchors.verticalCenter: parent.verticalCenter
                                                width: Math.round(16 * root.uiScale); height: Math.round(16 * root.uiScale)
                                                radius: width / 2
                                                color: !isMedal ? "transparent"
                                                     : model.rank === 1 ? "#b88a26"
                                                     : model.rank === 2 ? "#9aa7b8" : "#a06a3a"
                                                border.color: isMedal ? "transparent" : root.borderMuted
                                                border.width: isMedal ? 0 : 1
                                                Text {
                                                    anchors.centerIn: parent
                                                    text: model.rank
                                                    color: parent.isMedal ? "#0a0f1a" : root.textSecondary
                                                    font.pixelSize: Math.round(9 * root.uiScale); font.bold: parent.isMedal
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
                                            // трек + заливка мини-бара score
                                            Rectangle {
                                                anchors.left: parent.left; anchors.leftMargin: root.spacingSm
                                                anchors.bottom: parent.bottom; anchors.bottomMargin: Math.round(3 * root.uiScale)
                                                height: Math.round(4 * root.uiScale)
                                                width: Math.round(44 * root.uiScale)
                                                color: "#0a0f1a"; radius: 1
                                                Rectangle {
                                                    anchors.left: parent.left; anchors.top: parent.top; anchors.bottom: parent.bottom
                                                    radius: 1
                                                    width: {
                                                        var b = heurPanel.bestScore > 0.001 ? heurPanel.bestScore : 1.0
                                                        var f = Math.max(0, Math.min(1, model.scoreNum / b))
                                                        return f * parent.width
                                                    }
                                                    color: model.isBest ? "#4caf6e" : "#3a5a8a"
                                                }
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
                                            // мягкий терракот для «низко», ярко-красный только для совсем плохого
                                            color: parseFloat(model.entropy) >= 0.86 ? "#4caf6e"
                                                 : parseFloat(model.entropy) >= 0.84 ? "#b88a26" : "#b5654a"
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
                                            radius: 2
                                            color: model.isBest ? "#0d2918"
                                                 : model.status === "ok" ? "#0d2918"
                                                 : model.status === "dry_run" ? "#0e1f3a"
                                                 : "#1f1208"
                                            border.color: model.isBest ? "#1f5030"
                                                        : model.status === "ok" ? "#1f5030"
                                                        : model.status === "dry_run" ? "#2f6ed8"
                                                        : "#6b4a20"
                                            border.width: 1
                                            // лёгкое свечение у лучшего
                                            Rectangle {
                                                visible: model.isBest
                                                anchors.fill: parent; anchors.margins: -1
                                                radius: 3; color: "transparent"
                                                border.color: "#2f7a48"; border.width: 1
                                            }
                                            Text {
                                                id: statusTagText
                                                anchors.centerIn: parent
                                                text: _statusShort(model.status, model.reason, model.isBest)
                                                color: model.isBest ? "#4caf6e"
                                                     : model.status === "ok" ? "#4caf6e"
                                                     : model.status === "dry_run" ? "#7db4f5"
                                                     : "#d08a5a"
                                                font.pixelSize: Math.round(11 * root.uiScale)
                                            }
                                            // полная причина в tooltip
                                            ToolTip.visible: tagHover.hovered && model.reason.length > 0
                                            ToolTip.text: model.reason
                                            HoverHandler { id: tagHover }
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

                    // ── Динамика лучшего score (спарклайн) ───────────────────
                    GroupBox {
                        Layout.fillWidth: true
                        visible: heurPanel._bestHistory.length >= 2
                        title: "Динамика лучшего score"
                        label: Text { text: parent.title; color: root.textSecondary; font.pixelSize: root.evalCaptionSize }
                        background: Rectangle { color: root.bgElevated; border.color: root.borderMuted; border.width: 1 }

                        Item {
                            width: parent.width
                            height: Math.round(70 * root.uiScale)

                            Canvas {
                                id: sparkCanvas
                                anchors.fill: parent
                                property var bestData: heurPanel._bestHistory
                                onBestDataChanged: requestPaint()
                                onPaint: {
                                    var ctx = getContext("2d")
                                    ctx.reset()
                                    var d = bestData
                                    var n = d.length
                                    if (n < 2) return
                                    var pad = Math.round(10 * root.uiScale)
                                    var w = width - 2 * pad
                                    var h = height - 2 * pad
                                    var mn = d[0], mx = d[0]
                                    for (var i = 1; i < n; i++) { mn = Math.min(mn, d[i]); mx = Math.max(mx, d[i]) }
                                    var flat = (mx - mn) < 1e-9
                                    var rng = flat ? 1 : (mx - mn)
                                    function px(i) { return pad + w * i / (n - 1) }
                                    function py(v) { return flat ? pad + h / 2 : pad + h * (1 - (v - mn) / rng) }
                                    // Плоская история (лучший не менялся) → только тонкая
                                    // линия по центру, без заливки и базовой линии — иначе
                                    // получается сплошной зелёный «брус».
                                    if (!flat) {
                                        // пунктирная базовая линия
                                        ctx.beginPath(); ctx.moveTo(pad, py(d[n - 1])); ctx.lineTo(width - pad, py(d[n - 1]))
                                        ctx.strokeStyle = "rgba(184,138,38,0.35)"; ctx.lineWidth = 1; ctx.setLineDash([3, 3]); ctx.stroke(); ctx.setLineDash([])
                                        // заливка под линией
                                        ctx.beginPath(); ctx.moveTo(px(0), height - pad)
                                        for (var j = 0; j < n; j++) ctx.lineTo(px(j), py(d[j]))
                                        ctx.lineTo(px(n - 1), height - pad); ctx.closePath()
                                        ctx.fillStyle = "rgba(76,175,110,0.12)"; ctx.fill()
                                    }
                                    // линия
                                    ctx.beginPath(); ctx.moveTo(px(0), py(d[0]))
                                    for (var k = 1; k < n; k++) ctx.lineTo(px(k), py(d[k]))
                                    ctx.strokeStyle = flat ? "rgba(76,175,110,0.55)" : "#4caf6e"
                                    ctx.lineWidth = Math.max(1, Math.round(1.5 * root.uiScale)); ctx.stroke()
                                    // последняя точка
                                    ctx.beginPath(); ctx.arc(px(n - 1), py(d[n - 1]), Math.round(2.5 * root.uiScale), 0, 2 * Math.PI)
                                    ctx.fillStyle = "#b88a26"; ctx.fill()
                                }
                            }
                            // подпись текущего лучшего
                            Text {
                                anchors.right: parent.right; anchors.top: parent.top
                                anchors.rightMargin: root.spacingSm; anchors.topMargin: Math.round(2 * root.uiScale)
                                text: "лучший: " + _fmt(heurPanel.bestScore, 3)
                                color: "#4caf6e"; font.family: "JetBrains Mono"; font.pixelSize: Math.round(9 * root.uiScale)
                            }
                        }
                    }

                        } // ← конец ПРАВОЙ колонки
                    } // ← конец двухколоночного RowLayout
                }
            }
        }
    }
}
