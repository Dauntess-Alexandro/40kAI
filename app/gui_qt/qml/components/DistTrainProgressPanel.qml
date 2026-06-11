import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

ChamferPanel {
    id: root
    property var ctrl: null
    property real uiScale: 1.0
    property color uiBorder: "#243650"
    property color uiTextMain: "#e7edf5"
    property color uiTextMuted: "#7d8ba0"
    property string fontUiFamily: "Segoe UI"
    property string fontDataFamily: "Consolas"

    readonly property color pc1Color: "#b88a26"
    readonly property color pc2Color: "#3a6ea5"
    readonly property bool poolMode: ctrl && ctrl.distProgressMode === "pool"
    readonly property string phase: ctrl ? (ctrl.progressPhase || "") : ""
    readonly property bool waitingPc2: phase === "waiting_pc2"
    readonly property bool draining: phase === "draining"
    readonly property bool topup: phase === "topup"

    property int _hwTick: 0

    visible: ctrl && ctrl.distProgressVisible
    Layout.fillWidth: true
    fillColor: "#0d1521"
    borderWidth: 1
    cutSize: Math.round(10 * uiScale)
    contentMargin: Math.round(10 * uiScale)
    borderColor: waitingPc2
        ? Qt.rgba(pc2Color.r, pc2Color.g, pc2Color.b, 0.85)
        : (draining ? Qt.rgba(pc1Color.r, pc1Color.g, pc1Color.b, 0.65) : uiBorder)
    implicitHeight: distInner.implicitHeight + Math.round(20 * uiScale)

    function parseProgressLabel(label) {
        if (!label)
            return { cur: 0, total: 1 }
        var clean = String(label).replace(" готово", "").trim()
        var parts = clean.split("/")
        return {
            cur: parseInt(parts[0], 10) || 0,
            total: Math.max(1, parseInt(parts[1], 10) || 1)
        }
    }

    function phaseLabel(ph) {
        switch (ph) {
        case "waiting_pc2": return "Ожидание ПК2"
        case "collecting": return "Сбор эпизодов"
        case "topup": return "Добор на ПК1"
        case "draining": return "Завершение ПК2"
        case "evaluating": return "Оценка"
        case "done": return "Готово"
        default: return "Распределённый сбор"
        }
    }

    function hardwareLine(isPc2) {
        if (typeof telemetry === "undefined" || !telemetry)
            return isPc2 ? "ПК2 · —" : "ПК1 · —"
        var cards = telemetry.cards || []
        for (var i = 0; i < cards.length; ++i) {
            var c = cards[i]
            if (!c)
                continue
            if (isPc2 && c.id === "pc2")
                return (c.label || "ПК2") + " · " + (c.valueText || "—")
            if (!isPc2 && String(c.id).indexOf("gpu") === 0)
                return (c.label || "GPU") + " · " + (c.valueText || "—")
        }
        return isPc2 ? "ПК2 · —" : "ПК1 · —"
    }

    readonly property var pc1Parsed: parseProgressLabel(ctrl ? ctrl.pc1ProgressLabel : "")
    readonly property var pc2Parsed: parseProgressLabel(ctrl ? ctrl.pc2ProgressLabel : "")
    readonly property real pc1SegmentShare: {
        if (poolMode) {
            var sum = pc1Parsed.cur + pc2Parsed.cur
            return sum > 0 ? pc1Parsed.cur / sum : 0.5
        }
        var tot = pc1Parsed.total + pc2Parsed.total
        return tot > 0 ? pc1Parsed.total / tot : 0.5
    }
    readonly property bool pc2Done: ctrl && !poolMode && pc2Parsed.cur >= pc2Parsed.total
    readonly property string pc1SubHint: topup ? "добор квоты на ПК1" : ""
    readonly property string pc2SubHint: ctrl ? (ctrl.pc2StatusHint || "") : ""
    readonly property string pc1HwLine: { var _d = _hwTick; return hardwareLine(false) }
    readonly property string pc2HwLine: { var _d = _hwTick; return hardwareLine(true) }

    Connections {
        target: (typeof telemetry !== "undefined" && telemetry) ? telemetry : null
        function onCardsChanged() { root._hwTick++ }
    }

    ColumnLayout {
        id: distInner
        width: parent.width
        spacing: Math.round(10 * uiScale)

        RowLayout {
            Layout.fillWidth: true
            spacing: Math.round(8 * uiScale)

            Text {
                text: "РАСПРЕДЕЛЁННЫЙ СБОР"
                color: uiTextMuted
                font.pixelSize: Math.round(10 * uiScale)
                font.bold: true
                font.letterSpacing: 0.7
                font.family: fontUiFamily
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                radius: Math.round(10 * uiScale)
                color: waitingPc2
                    ? Qt.rgba(pc2Color.r, pc2Color.g, pc2Color.b, 0.18)
                    : (draining
                        ? Qt.rgba(pc1Color.r, pc1Color.g, pc1Color.b, 0.15)
                        : Qt.rgba(pc1Color.r, pc1Color.g, pc1Color.b, 0.12))
                border.width: 1
                border.color: waitingPc2
                    ? Qt.rgba(pc2Color.r, pc2Color.g, pc2Color.b, 0.55)
                    : Qt.rgba(pc1Color.r, pc1Color.g, pc1Color.b, 0.35)
                implicitWidth: phaseBadge.implicitWidth + Math.round(12 * uiScale)
                implicitHeight: phaseBadge.implicitHeight + Math.round(6 * uiScale)

                Text {
                    id: phaseBadge
                    anchors.centerIn: parent
                    text: phaseLabel(root.phase)
                    color: waitingPc2 ? Qt.lighter(pc2Color, 1.35) : Qt.lighter(pc1Color, 1.2)
                    font.pixelSize: Math.round(10 * uiScale)
                    font.bold: true
                    font.letterSpacing: 0.5
                    font.family: fontUiFamily
                }
            }
        }

        Text {
            Layout.fillWidth: true
            visible: poolMode
            text: "вклад в общий лимит (квота не фиксирована)"
            color: uiTextMuted
            font.pixelSize: Math.round(10 * uiScale)
            font.family: fontUiFamily
            wrapMode: Text.WordWrap
        }

        Text {
            Layout.fillWidth: true
            visible: !poolMode && pc2SubHint !== "" && !waitingPc2
            text: pc2SubHint
            color: uiTextMuted
            font.pixelSize: Math.round(10 * uiScale)
            font.family: fontUiFamily
            elide: Text.ElideRight
        }

        DistStackedProgressBar {
            Layout.fillWidth: true
            uiScale: root.uiScale
            poolMode: root.poolMode
            waitingPc2: root.waitingPc2
            draining: root.draining
            pc1SegmentShare: root.pc1SegmentShare
            pc1Fill: ctrl ? ctrl.pc1ProgressValue : 0
            pc2Fill: ctrl ? ctrl.pc2ProgressValue : 0
            pc1Color: root.pc1Color
            pc2Color: root.pc2Color
            borderColor: root.uiBorder
            barHeight: Math.round(10 * uiScale)
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: Math.round(8 * uiScale)

            DistNodeProgressCard {
                nodeLabel: "ПК1 · learner"
                progressValue: ctrl ? ctrl.pc1ProgressValue : 0
                progressLabel: ctrl ? ctrl.pc1ProgressLabel : "0/0"
                subLine: pc1HwLine
                statusHint: pc1SubHint
                accentColor: root.pc1Color
                waitingMode: waitingPc2
                draining: draining
                doneMode: false
                isRemote: false
                uiScale: root.uiScale
                textMain: root.uiTextMain
                textMuted: root.uiTextMuted
                fontUiFamily: root.fontUiFamily
                fontDataFamily: root.fontDataFamily
            }

            DistNodeProgressCard {
                nodeLabel: "ПК2 · actors"
                progressValue: ctrl ? ctrl.pc2ProgressValue : 0
                progressLabel: ctrl ? ctrl.pc2ProgressLabel : "0/0"
                subLine: pc2HwLine
                statusHint: waitingPc2 ? (ctrl ? ctrl.pc2StatusHint : "") : (pc2Done ? "квота выполнена" : pc2SubHint)
                accentColor: root.pc2Color
                waitingMode: waitingPc2
                draining: draining
                doneMode: pc2Done && !poolMode
                isRemote: true
                uiScale: root.uiScale
                textMain: root.uiTextMain
                textMuted: root.uiTextMuted
                fontUiFamily: root.fontUiFamily
                fontDataFamily: root.fontDataFamily
            }
        }
    }
}
