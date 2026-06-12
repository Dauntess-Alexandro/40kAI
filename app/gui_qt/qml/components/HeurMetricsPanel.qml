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
            var status = row.status || "…"
            var reasons = (row.reject_reasons || []).join(", ")
            var isBest = false
            var score = row.score !== undefined && row.score !== null ? row.score : -1
            if (status === "ok" && score > heurPanel.bestScore) {
                heurPanel.bestScore = score
                heurPanel.bestCandidateIdx = row.candidate_idx || 0
                for (var i = 0; i < candidatesModel.count; i++) {
                    candidatesModel.setProperty(i, "isBest", false)
                }
                isBest = true
            }
            candidatesModel.append({
                idx:      "" + (row.candidate_idx !== undefined ? row.candidate_idx : "?"),
                score:    score >= 0 ? _fmt(score, 3) : "…",
                winrate:  _fmt(row.heur_winrate, 3),
                entropy:  _fmt(row.style_entropy_norm, 3),
                draws:    row.draw_rate !== undefined ? _fmt(row.draw_rate * 100, 1) + "%" : "…",
                status:   status,
                reason:   reasons,
                isBest:   isBest
            })
        }
        function onCalibrationFinished(summary) {
            heurPanel.currentRunDir = summary.run_dir || heurCalRunner.currentRunDir
            heurPanel.patchText = summary.patch_lines || ""
            var idx = summary.best_candidate_idx
            if (idx !== null && idx !== undefined) {
                heurPanel.bestCandidateIdx = idx
            }
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

                        property var md: controller.heuristicMetricsDict || {}

                        Grid {
                            columns: 2
                            columnSpacing: Math.round(24 * root.uiScale)
                            rowSpacing: Math.round(3 * root.uiScale)

                            Repeater {
                                model: [
                                    ["Ран",          String(parent.parent.md.run_id || "—")],
                                    ["Обновлено",    String(parent.parent.md.updated_at || "—")],
                                    ["Всего игр",    String(parent.parent.md.total_games || 0)],
                                    ["Invalid rate", _fmt(parent.parent.md.invalid_rate, 4)],
                                    ["Avg risk",     _fmt(parent.parent.md.avg_risk, 3)],
                                    ["Avg cover",    _fmt(parent.parent.md.avg_cover, 3)],
                                    ["Charge succ.", _fmt(parent.parent.md.charge_success_rate, 3)],
                                    ["Shoot overkill",_fmt(parent.parent.md.shoot_overkill_rate, 3)],
                                    ["Fallback rate",_fmt(parent.parent.md.fallback_rate, 3)],
                                    ["Mode kite",    String(parent.parent.md.mode_kite || 0)],
                                    ["Mode hold",    String(parent.parent.md.mode_hold || 0)],
                                    ["Mode commit",  String(parent.parent.md.mode_commit || 0)],
                                    ["Role ranged",  String(parent.parent.md.role_ranged || 0)],
                                    ["Role hybrid",  String(parent.parent.md.role_hybrid || 0)],
                                    ["Role melee",   String(parent.parent.md.role_melee || 0)],
                                ]
                                delegate: Row {
                                    spacing: root.spacingSm
                                    Text { text: modelData[0] + ":"; color: root.textSecondary; font.pixelSize: root.evalCaptionSize; width: Math.round(110 * root.uiScale) }
                                    Text { text: modelData[1]; color: root.textPrimary;    font.pixelSize: root.evalCaptionSize; font.family: "JetBrains Mono" }
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

                            Row {
                                width: parent.width
                                height: Math.round(20 * root.uiScale)
                                Rectangle { width: parent.width; height: parent.height; color: root.bgSurface }
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

                            Repeater {
                                model: benchHistoryModel
                                delegate: Row {
                                    width: parent.width
                                    height: Math.round(22 * root.uiScale)
                                    Rectangle { width: parent.width; height: parent.height; color: index % 2 === 0 ? root.bgElevated : root.bgSurface; z: -1 }
                                    Repeater {
                                        model: [model.time, model.winrate, model.entropy, model.draws, String(model.games)]
                                        delegate: Text {
                                            text: modelData; color: root.textPrimary
                                            font.pixelSize: root.evalCaptionSize
                                            font.family: "JetBrains Mono"
                                            width: [100, 70, 70, 60, 50][index] * root.uiScale
                                            leftPadding: root.spacingSm
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

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingSm

                                Button {
                                    visible: !heurCalRunner.isRunning
                                    text: "▶ Калибровать"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: {
                                        candidatesModel.clear()
                                        heurPanel.bestCandidateIdx = -1
                                        heurPanel.bestScore = 0.0
                                        heurPanel.patchText = ""
                                        heurPanel.calDone = 0
                                        heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                        heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                          parseInt(calGamesInput.text),
                                                          parseInt(calSeedInput.text), false)
                                    }
                                    contentItem: Text { text: parent.text; color: "#e8c060"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: parent.down ? "#100e00" : "#1a1508"; border.color: parent.hovered ? "#d0a030" : "#b88a26"; border.width: 1 }
                                }
                                Button {
                                    visible: !heurCalRunner.isRunning
                                    text: "Dry run"
                                    font.pixelSize: root.evalCaptionSize
                                    onClicked: {
                                        candidatesModel.clear()
                                        heurPanel.bestCandidateIdx = -1
                                        heurPanel.calDone = 0
                                        heurPanel.calTotal = parseInt(calCandidatesInput.text)
                                        heurCalRunner.run(parseInt(calCandidatesInput.text),
                                                          parseInt(calGamesInput.text),
                                                          parseInt(calSeedInput.text), true)
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

                            Row {
                                width: parent.width
                                height: Math.round(20 * root.uiScale)
                                Rectangle { anchors.fill: parent; color: root.bgSurface }
                                Repeater {
                                    model: [["#", 36], ["score", 60], ["winrate", 64], ["entropy", 64], ["draws", 56], ["статус", 0]]
                                    delegate: Text {
                                        text: modelData[0]; color: root.textSecondary
                                        font.pixelSize: Math.round(9 * root.uiScale)
                                        width: modelData[1] > 0 ? Math.round(modelData[1] * root.uiScale) : parent.width - Math.round(340 * root.uiScale)
                                        leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter
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
                                        Repeater {
                                            model: [
                                                [model.idx,     36,  model.isBest ? "#b88a26" : root.textSecondary],
                                                [model.score,   60,  model.isBest ? "#4caf6e" : root.textPrimary],
                                                [model.winrate, 64,  root.textPrimary],
                                                [model.entropy, 64,  parseFloat(model.entropy) >= 0.86 ? "#4caf6e" : parseFloat(model.entropy) >= 0.84 ? "#b88a26" : "#cf3f3f"],
                                                [model.draws,   56,  root.textPrimary],
                                            ]
                                            delegate: Text {
                                                text: modelData[0]; color: modelData[2]
                                                font.pixelSize: root.evalCaptionSize
                                                font.family: "JetBrains Mono"
                                                font.bold: modelData[1] === 60 && model.isBest
                                                width: Math.round(modelData[1] * root.uiScale)
                                                leftPadding: root.spacingSm; verticalAlignment: Text.AlignVCenter
                                            }
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
                                                    : model.status === "ok" ? "✓"
                                                    : model.status === "dry_run" ? "dry"
                                                    : model.status === "в работе" ? "⟳"
                                                    : model.reason.length > 0 ? model.reason.substring(0, 12)
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
                                text: heurPanel.patchText.length > 0
                                    ? heurPanel.patchText
                                    : "(Завершите калибровку для просмотра патча)"
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
                                    enabled: heurPanel.currentRunDir.length > 0 && !heurCalRunner.isRunning
                                    onClicked: heurCalRunner.applyPatch(heurPanel.currentRunDir)
                                    contentItem: Text { text: parent.text; color: parent.enabled ? "#e8c060" : "#6b5010"; font: parent.font; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                    background: Rectangle { color: parent.down ? "#100e00" : "#1a1508"; border.color: parent.enabled ? (parent.hovered ? "#d0a030" : "#b88a26") : "#3a3010"; border.width: 1 }
                                }
                                Button {
                                    text: "Открыть папку"
                                    font.pixelSize: root.evalCaptionSize
                                    enabled: heurPanel.currentRunDir.length > 0
                                    onClicked: Qt.openUrlExternally("file:///" + heurPanel.currentRunDir)
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
