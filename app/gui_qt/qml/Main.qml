import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import Qt.labs.platform 1.1 as Platform
import "components"

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

    function themeColor(key, fallback) {
        if (typeof themeTokens !== "undefined" && themeTokens !== null) {
            var v = themeTokens[key]
            if (v !== undefined && v !== "")
                return v
        }
        return fallback
    }

    property color bgBase: themeColor("bgBase", "#0F172A")
    property color bgSurface: themeColor("bgSurface", "#131b2d")
    property color bgElevated: themeColor("bgElevated", "#1E293B")
    property color borderMuted: themeColor("borderMuted", "#334155")
    property color textPrimary: themeColor("textPrimary", "#d7dde7")
    property color textSecondary: themeColor("textSecondary", "#98a4b8")
    property color accentP1: themeColor("accentP1", "#2f6ed8")
    property color accentP2: themeColor("accentP2", "#cf3f3f")
    property color accentPrimaryAction: themeColor("accentPrimaryAction", "#b88a26")
    property color accentDanger: themeColor("accentDanger", "#a35345")
    property color accentGhost: themeColor("accentGhost", "#6f7d92")
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
    property var rosterWeaponStatHdrs: ["RNG", "A", "BS/WS", "S", "AP", "D"]
    readonly property var rosterWeaponStatColWidths: [
        Math.round(44 * uiScale),
        Math.round(26 * uiScale),
        Math.round(54 * uiScale),
        Math.round(26 * uiScale),
        Math.round(36 * uiScale),
        Math.round(26 * uiScale)
    ]
    readonly property var rosterCoreStatHdrs: ["M", "T", "SV", "W", "LD", "OC"]
    readonly property var rosterCoreStatColWidths: [
        Math.round(30 * uiScale),
        Math.round(24 * uiScale),
        Math.round(30 * uiScale),
        Math.round(24 * uiScale),
        Math.round(30 * uiScale),
        Math.round(24 * uiScale)
    ]
    /** Модульный шаг 4 px × uiScale — отступы между блоками карточки ростера кратны ему. */
    readonly property int rosterSlateGridStep: Math.round(4 * uiScale)
    readonly property int rosterSlateBlockGap: 2 * rosterSlateGridStep
    /** «Воздух» между крупными блоками карточки ростера (статы → теги → способности → оружие). */
    readonly property int rosterSlateSectionGap: Math.round(10 * uiScale)
    readonly property color rosterSlateInstrumentBg: "#0e131c"
    readonly property color rosterTitleUnderline: "#26ffffff"
    property string fontUiFamily: "Rajdhani"
    property string fontDataFamily: "IBM Plex Mono"
    readonly property string inferenceSearchHelpText:
        "Для AZ, GMZ и GAZ по умолчанию лучше использовать MCTS/Search: это обычно сильнее Greedy, но ход считается дольше.\n" +
        "Greedy — один быстрый проход сети без поиска. Подходит для smoke-теста, слабого ПК или сравнения baseline.\n" +
        "AZ MCTS — классический AlphaZero-поиск. GMZ Search — Gumbel MuZero search. GAZ Search — Gumbel AlphaZero с батчингом leaf-eval.\n" +
        "MCTS sims / Search sims — число симуляций поиска (старт 32). Больше = чаще сильнее, но медленнее.\n" +
        "Температура (для AZ/GMZ/GAZ) работает только в MCTS/Search:\n" +
        "• меньше (0.03–0.08) — стабильнее;\n" +
        "• больше (0.10–0.15) — больше разнообразия.\n" +
        "Старт: AZ 0.06, GMZ 0.10, GAZ 0.05.\n" +
        "PPO — режимы Greedy/Stochastic. Stochastic сэмплит из политики с температурой (поле «Темп.»):\n" +
        "• <1 (0.5–0.7) — стабильнее/сильнее; 1.0 — родное распределение сети; >1 (до 2.0) — разнообразнее, но слабее. Старт 1.0.\n" +
        "DQN — режимы Greedy/Epsilon. Epsilon (то же числовое поле) — доля случайных легальных ходов:\n" +
        "• 0 — всегда лучший ход (замер силы); 0.05–0.10 — лёгкое разнообразие; ≥0.2 — стресс-тест робастности (слабее). Старт 0.10.\n" +
        "Эвристика — скриптовый бот, не использует нейросеть, поиск и температуру."

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

    component TacticalRosterTip : Popup {
        id: tacticalRosterTip
        property var card: null
        property Item anchorItem: null
        property color accentColor: "#2f6ed8"
        property color secondaryAccentColor: "#d97706"
        property real scaleUnit: root.uiScale

        parent: Overlay.overlay
        modal: false
        focus: false
        closePolicy: Popup.NoAutoClose
        padding: 0
        implicitWidth: Math.round(520 * scaleUnit)
        implicitHeight: tipPanel.implicitHeight
        visible: card && card.kind === "unit" && anchorItem && anchorItem.containsMouse
        opacity: visible ? 1.0 : 0.0
        x: {
            if (!anchorItem || !parent)
                return 0
            var p = anchorItem.mapToItem(parent, anchorItem.width + Math.round(12 * scaleUnit), -Math.round(8 * scaleUnit))
            return Math.min(Math.max(Math.round(8 * scaleUnit), p.x), parent.width - width - Math.round(8 * scaleUnit))
        }
        y: {
            if (!anchorItem || !parent)
                return 0
            var p = anchorItem.mapToItem(parent, anchorItem.width + Math.round(12 * scaleUnit), -Math.round(8 * scaleUnit))
            return Math.min(Math.max(Math.round(8 * scaleUnit), p.y), parent.height - height - Math.round(8 * scaleUnit))
        }

        Behavior on opacity { NumberAnimation { duration: 100; easing.type: Easing.OutQuad } }

        background: Item {}

        contentItem: ChamferPanel {
            id: tipPanel
            width: tacticalRosterTip.implicitWidth
            fillColor: "#0b1220"
            borderColor: Qt.rgba(tacticalRosterTip.accentColor.r, tacticalRosterTip.accentColor.g, tacticalRosterTip.accentColor.b, 0.85)
            borderWidth: 1
            cutSize: Math.round(10 * tacticalRosterTip.scaleUnit)
            contentMargin: Math.round(10 * tacticalRosterTip.scaleUnit)
            implicitHeight: tipContent.implicitHeight + Math.round(20 * tacticalRosterTip.scaleUnit)

            Rectangle {
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: Math.round(3 * tacticalRosterTip.scaleUnit)
                color: tacticalRosterTip.accentColor
            }

            ColumnLayout {
                id: tipContent
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: Math.round(10 * tacticalRosterTip.scaleUnit)
                anchors.leftMargin: Math.round(14 * tacticalRosterTip.scaleUnit)
                spacing: Math.round(8 * tacticalRosterTip.scaleUnit)

                RowLayout {
                    Layout.fillWidth: true
                    spacing: Math.round(8 * tacticalRosterTip.scaleUnit)
                    Text {
                        Layout.fillWidth: true
                        text: tacticalRosterTip.card && tacticalRosterTip.card.title
                            ? String(tacticalRosterTip.card.title).toUpperCase()
                            : "UNIT"
                        color: "#f8fafc"
                        font.family: root.fontUiFamily
                        font.bold: true
                        font.pixelSize: Math.round(14 * tacticalRosterTip.scaleUnit)
                        font.letterSpacing: 0.8
                        elide: Text.ElideRight
                    }
                    Rectangle {
                        visible: tacticalRosterTip.card && tacticalRosterTip.card.instanceId && String(tacticalRosterTip.card.instanceId).length > 0
                        color: Qt.rgba(1, 1, 1, 0.05)
                        border.width: 1
                        border.color: "#475569"
                        radius: 0
                        implicitWidth: sysRefTxt.implicitWidth + Math.round(12 * tacticalRosterTip.scaleUnit)
                        implicitHeight: sysRefTxt.implicitHeight + Math.round(6 * tacticalRosterTip.scaleUnit)
                        Text {
                            id: sysRefTxt
                            anchors.centerIn: parent
                            text: "SYS.REF: " + (tacticalRosterTip.card ? tacticalRosterTip.card.instanceId : "—")
                            color: "#94a3b8"
                            font.family: root.fontDataFamily
                            font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                            font.bold: true
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: Qt.rgba(1, 1, 1, 0.10)
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: Math.round(10 * tacticalRosterTip.scaleUnit)

                    ColumnLayout {
                        Layout.preferredWidth: Math.round(190 * tacticalRosterTip.scaleUnit)
                        Layout.maximumWidth: Math.round(190 * tacticalRosterTip.scaleUnit)
                        spacing: Math.round(8 * tacticalRosterTip.scaleUnit)

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: Math.round(8 * tacticalRosterTip.scaleUnit)
                            Rectangle {
                                Layout.preferredWidth: Math.round(54 * tacticalRosterTip.scaleUnit)
                                Layout.preferredHeight: Math.round(54 * tacticalRosterTip.scaleUnit)
                                color: "#0a0e14"
                                border.width: 1
                                border.color: "#334155"
                                radius: 0
                                Image {
                                    anchors.fill: parent
                                    anchors.margins: Math.round(4 * tacticalRosterTip.scaleUnit)
                                    fillMode: Image.PreserveAspectFit
                                    smooth: true
                                    source: tacticalRosterTip.card && tacticalRosterTip.card.unitIcon ? tacticalRosterTip.card.unitIcon : ""
                                    visible: source !== ""
                                }
                            }
                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: Math.round(3 * tacticalRosterTip.scaleUnit)
                                Text {
                                    Layout.fillWidth: true
                                    text: "UNIT PROFILE"
                                    color: tacticalRosterTip.accentColor
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    font.letterSpacing: 0.8
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: tacticalRosterTip.card && tacticalRosterTip.card.unitName ? tacticalRosterTip.card.unitName : "—"
                                    color: "#cbd5e1"
                                    font.family: root.fontUiFamily
                                    font.pixelSize: Math.round(11 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    wrapMode: Text.WordWrap
                                    maximumLineCount: 2
                                    elide: Text.ElideRight
                                }
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            color: "#0f172a"
                            border.width: 1
                            border.color: "#334155"
                            radius: 0
                            implicitHeight: coreStatsCol.implicitHeight + Math.round(12 * tacticalRosterTip.scaleUnit)
                            ColumnLayout {
                                id: coreStatsCol
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.margins: Math.round(6 * tacticalRosterTip.scaleUnit)
                                spacing: Math.round(4 * tacticalRosterTip.scaleUnit)
                                Text {
                                    Layout.fillWidth: true
                                    text: "CORE STATS"
                                    color: "#94a3b8"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    font.letterSpacing: 0.7
                                }
                                Row {
                                    spacing: 0
                                    Repeater {
                                        model: root.rosterCoreStatHdrs.length
                                        delegate: Column {
                                            width: Math.round(29 * tacticalRosterTip.scaleUnit)
                                            spacing: Math.round(2 * tacticalRosterTip.scaleUnit)
                                            Text {
                                                width: parent.width
                                                horizontalAlignment: Text.AlignHCenter
                                                text: root.rosterCoreStatHdrs[index]
                                                color: "#64748b"
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(7 * tacticalRosterTip.scaleUnit)
                                                font.bold: true
                                            }
                                            Text {
                                                width: parent.width
                                                horizontalAlignment: Text.AlignHCenter
                                                text: tacticalRosterTip.card && tacticalRosterTip.card.coreStats && tacticalRosterTip.card.coreStats.length > index
                                                    ? tacticalRosterTip.card.coreStats[index]
                                                    : "—"
                                                color: "#f8fafc"
                                                font.family: root.fontDataFamily
                                                font.pixelSize: Math.round(10 * tacticalRosterTip.scaleUnit)
                                                font.bold: true
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: Math.round(5 * tacticalRosterTip.scaleUnit)
                            Text {
                                Layout.fillWidth: true
                                text: "KEYWORDS"
                                color: "#94a3b8"
                                font.family: root.fontDataFamily
                                font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                                font.bold: true
                                font.letterSpacing: 0.7
                            }
                            Flow {
                                Layout.fillWidth: true
                                spacing: Math.round(4 * tacticalRosterTip.scaleUnit)
                                Repeater {
                                    model: tacticalRosterTip.card && tacticalRosterTip.card.keywords ? tacticalRosterTip.card.keywords : []
                                    delegate: Rectangle {
                                        color: Qt.rgba(1, 1, 1, 0.05)
                                        border.width: 1
                                        border.color: "#475569"
                                        radius: 0
                                        implicitWidth: keywordTipTxt.implicitWidth + Math.round(10 * tacticalRosterTip.scaleUnit)
                                        implicitHeight: keywordTipTxt.implicitHeight + Math.round(4 * tacticalRosterTip.scaleUnit)
                                        Text {
                                            id: keywordTipTxt
                                            anchors.centerIn: parent
                                            text: modelData
                                            color: "#cbd5e1"
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(7 * tacticalRosterTip.scaleUnit)
                                            font.bold: true
                                        }
                                    }
                                }
                            }
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: Math.round(7 * tacticalRosterTip.scaleUnit)

                        Rectangle {
                            Layout.fillWidth: true
                            color: Qt.rgba(1, 1, 1, 0.035)
                            border.width: 1
                            border.color: "#334155"
                            radius: 0
                            implicitHeight: abilityTipCol.implicitHeight + Math.round(12 * tacticalRosterTip.scaleUnit)
                            ColumnLayout {
                                id: abilityTipCol
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.margins: Math.round(6 * tacticalRosterTip.scaleUnit)
                                spacing: Math.round(4 * tacticalRosterTip.scaleUnit)
                                Text {
                                    Layout.fillWidth: true
                                    text: "ABILITIES"
                                    color: "#e8c86a"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    font.letterSpacing: 0.7
                                }
                                Repeater {
                                    model: tacticalRosterTip.card && tacticalRosterTip.card.abilities && tacticalRosterTip.card.abilities.length > 0
                                        ? tacticalRosterTip.card.abilities
                                        : ["NO ACTIVE ABILITIES"]
                                    delegate: Text {
                                        Layout.fillWidth: true
                                        text: ">_ " + modelData
                                        color: modelData === "NO ACTIVE ABILITIES" ? "#64748b" : "#cbd5e1"
                                        font.family: root.fontDataFamily
                                        font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                                        wrapMode: Text.WordWrap
                                        maximumLineCount: 2
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            color: Qt.rgba(tacticalRosterTip.accentColor.r, tacticalRosterTip.accentColor.g, tacticalRosterTip.accentColor.b, 0.08)
                            border.width: 1
                            border.color: Qt.rgba(tacticalRosterTip.accentColor.r, tacticalRosterTip.accentColor.g, tacticalRosterTip.accentColor.b, 0.45)
                            radius: 0
                            implicitHeight: rangedTipCol.implicitHeight + Math.round(12 * tacticalRosterTip.scaleUnit)
                            ColumnLayout {
                                id: rangedTipCol
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.margins: Math.round(6 * tacticalRosterTip.scaleUnit)
                                spacing: Math.round(3 * tacticalRosterTip.scaleUnit)
                                Text {
                                    Layout.fillWidth: true
                                    text: "RANGED"
                                    color: "#8fb6e8"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(9 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    font.letterSpacing: 0.8
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: tacticalRosterTip.card && tacticalRosterTip.card.rangedName ? tacticalRosterTip.card.rangedName : "—"
                                    color: "#f8fafc"
                                    font.family: root.fontUiFamily
                                    font.pixelSize: Math.round(12 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    wrapMode: Text.WordWrap
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: tacticalRosterTip.card && tacticalRosterTip.card.rangedStatline ? tacticalRosterTip.card.rangedStatline : "—"
                                    color: "#cbd5e1"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(10 * tacticalRosterTip.scaleUnit)
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            color: Qt.rgba(tacticalRosterTip.secondaryAccentColor.r, tacticalRosterTip.secondaryAccentColor.g, tacticalRosterTip.secondaryAccentColor.b, 0.08)
                            border.width: 1
                            border.color: Qt.rgba(tacticalRosterTip.secondaryAccentColor.r, tacticalRosterTip.secondaryAccentColor.g, tacticalRosterTip.secondaryAccentColor.b, 0.45)
                            radius: 0
                            implicitHeight: meleeTipCol.implicitHeight + Math.round(12 * tacticalRosterTip.scaleUnit)
                            ColumnLayout {
                                id: meleeTipCol
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.margins: Math.round(6 * tacticalRosterTip.scaleUnit)
                                spacing: Math.round(3 * tacticalRosterTip.scaleUnit)
                                Text {
                                    Layout.fillWidth: true
                                    text: "MELEE"
                                    color: "#e8c86a"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(9 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    font.letterSpacing: 0.8
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: tacticalRosterTip.card && tacticalRosterTip.card.meleeName ? tacticalRosterTip.card.meleeName : "—"
                                    color: "#f8fafc"
                                    font.family: root.fontUiFamily
                                    font.pixelSize: Math.round(12 * tacticalRosterTip.scaleUnit)
                                    font.bold: true
                                    wrapMode: Text.WordWrap
                                }
                                Text {
                                    Layout.fillWidth: true
                                    text: tacticalRosterTip.card && tacticalRosterTip.card.meleeStatline ? tacticalRosterTip.card.meleeStatline : "—"
                                    color: "#cbd5e1"
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(10 * tacticalRosterTip.scaleUnit)
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: "SOURCE: ROSTER"
                        color: "#64748b"
                        font.family: root.fontDataFamily
                        font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                        font.bold: true
                        font.letterSpacing: 0.5
                    }
                    Item { Layout.fillWidth: true }
                    Text {
                        text: "DATA-SLATE"
                        color: tacticalRosterTip.accentColor
                        font.family: root.fontDataFamily
                        font.pixelSize: Math.round(8 * tacticalRosterTip.scaleUnit)
                        font.bold: true
                        font.letterSpacing: 0.5
                    }
                }
            }
        }
    }

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
            TacticalTabButton { text: "Лига" }
        }

        StackLayout {
            id: mainStack
            currentIndex: mainTabs.currentIndex
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: root.spacingLg
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
                                Text {
                                    text: controller.progressDetail
                                    visible: controller.progressDetail.length > 0
                                    color: root.uiTextMuted
                                    font.family: root.fontDataFamily
                                    font.pixelSize: Math.round(11 * root.uiScale)
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
                            property real smoothValue: controller.progressValue
                            value: smoothValue
                            Behavior on smoothValue {
                                NumberAnimation {
                                    duration: 600
                                    easing.type: Easing.OutCubic
                                }
                            }
                            Connections {
                                target: controller
                                function onProgressValueChanged() {
                                    trainingProgress.smoothValue = controller.progressValue
                                }
                            }
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

                    RowLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        // Первый ребёнок — правая статус-колонка; layoutDirection рисует рейку управления слева.
                        layoutDirection: Qt.RightToLeft
                        spacing: root.spacingMd

                        ScrollView {
                            id: mainStatusScroll
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true

                            ColumnLayout {
                                width: mainStatusScroll.availableWidth
                                spacing: root.spacingMd

                                DistTrainProgressPanel {
                                    Layout.fillWidth: true
                                    ctrl: controller
                                    uiScale: root.uiScale
                                    uiBorder: root.uiBorder
                                    uiTextMain: root.uiTextMain
                                    uiTextMuted: root.uiTextMuted
                                    fontUiFamily: root.fontUiFamily
                                    fontDataFamily: root.fontDataFamily
                                }

                                TelemetryStrip {
                                    Layout.fillWidth: true
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
                                                id: trainCtxMainCol
                                                Layout.fillWidth: true
                                                spacing: root.spacingXs
                                                readonly property bool trainCtxNarrow: trainCtxRoot.width < Math.round(520 * root.uiScale)

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
                                                    spacing: root.spacingSm
                                                    Rectangle {
                                                        Layout.fillWidth: true
                                                        implicitHeight: matchP1Col.implicitHeight + Math.round(16 * root.uiScale)
                                                        color: "#141b26"
                                                        border.width: 2
                                                        border.color: controller.learnerSide === "P1" ? root.p1Accent : root.uiBorder
                                                        ColumnLayout {
                                                            id: matchP1Col
                                                            anchors.left: parent.left
                                                            anchors.right: parent.right
                                                            anchors.top: parent.top
                                                            anchors.margins: Math.round(8 * root.uiScale)
                                                            spacing: Math.round(3 * root.uiScale)
                                                            RowLayout {
                                                                Layout.fillWidth: true
                                                                spacing: root.spacingXs
                                                                Image {
                                                                    source: controller.faction_icon_source(controller.trainRosterP1Faction)
                                                                    sourceSize.width: Math.min(root.factionIconSize, Math.round(22 * root.uiScale))
                                                                    sourceSize.height: Math.min(root.factionIconSize, Math.round(22 * root.uiScale))
                                                                    Layout.preferredWidth: sourceSize.width
                                                                    Layout.preferredHeight: sourceSize.height
                                                                    visible: source !== ""
                                                                    fillMode: Image.PreserveAspectFit
                                                                    smooth: true
                                                                }
                                                                Text {
                                                                    Layout.fillWidth: true
                                                                    text: "P1 · " + controller.trainRosterP1Faction
                                                                    color: root.uiTextMain
                                                                    font.family: root.fontUiFamily
                                                                    font.bold: true
                                                                    font.pixelSize: Math.round(11 * root.uiScale)
                                                                    elide: Text.ElideRight
                                                                }
                                                                Rectangle {
                                                                    implicitHeight: Math.round(18 * root.uiScale)
                                                                    implicitWidth: learnerBadgeP1.implicitWidth + Math.round(10 * root.uiScale)
                                                                    color: "#1a2332"
                                                                    border.width: 1
                                                                    border.color: controller.learnerSide === "P1" ? root.p1Accent : "#556276"
                                                                    Text {
                                                                        id: learnerBadgeP1
                                                                        anchors.centerIn: parent
                                                                        text: controller.learnerSide === "P1" ? "LEARNER" : "OPPONENT"
                                                                        color: root.uiTextMain
                                                                        font.family: root.fontDataFamily
                                                                        font.pixelSize: Math.round(9 * root.uiScale)
                                                                        font.bold: true
                                                                    }
                                                                }
                                                            }
                                                            Text {
                                                                Layout.fillWidth: true
                                                                text: (controller.learnerSide === "P1" ? "ОБУЧЕНИЕ" : "ОППОНЕНТ")
                                                                    + " · " + (controller.learnerSide === "P1"
                                                                        ? controller.trainContextLearnerAlgoShort
                                                                        : controller.trainContextOpponentAlgoShort)
                                                                color: root.uiTextMuted
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                                wrapMode: Text.Wrap
                                                            }
                                                        }
                                                    }
                                                    Rectangle {
                                                        Layout.fillWidth: true
                                                        implicitHeight: matchP2Col.implicitHeight + Math.round(16 * root.uiScale)
                                                        color: "#141b26"
                                                        border.width: 2
                                                        border.color: controller.learnerSide === "P2" ? root.p2Accent : "#6c3844"
                                                        ColumnLayout {
                                                            id: matchP2Col
                                                            anchors.left: parent.left
                                                            anchors.right: parent.right
                                                            anchors.top: parent.top
                                                            anchors.margins: Math.round(8 * root.uiScale)
                                                            spacing: Math.round(3 * root.uiScale)
                                                            RowLayout {
                                                                Layout.fillWidth: true
                                                                spacing: root.spacingXs
                                                                Image {
                                                                    source: controller.faction_icon_source(controller.trainRosterP2Faction)
                                                                    sourceSize.width: Math.min(root.factionIconSize, Math.round(22 * root.uiScale))
                                                                    sourceSize.height: Math.min(root.factionIconSize, Math.round(22 * root.uiScale))
                                                                    Layout.preferredWidth: sourceSize.width
                                                                    Layout.preferredHeight: sourceSize.height
                                                                    visible: source !== ""
                                                                    fillMode: Image.PreserveAspectFit
                                                                    smooth: true
                                                                }
                                                                Text {
                                                                    Layout.fillWidth: true
                                                                    text: "P2 · " + controller.trainRosterP2Faction
                                                                    color: root.uiTextMain
                                                                    font.family: root.fontUiFamily
                                                                    font.bold: true
                                                                    font.pixelSize: Math.round(11 * root.uiScale)
                                                                    elide: Text.ElideRight
                                                                }
                                                                Rectangle {
                                                                    implicitHeight: Math.round(18 * root.uiScale)
                                                                    implicitWidth: learnerBadgeP2.implicitWidth + Math.round(10 * root.uiScale)
                                                                    color: "#1a2332"
                                                                    border.width: 1
                                                                    border.color: controller.learnerSide === "P2" ? root.p2Accent : "#556276"
                                                                    Text {
                                                                        id: learnerBadgeP2
                                                                        anchors.centerIn: parent
                                                                        text: controller.learnerSide === "P2" ? "LEARNER" : "OPPONENT"
                                                                        color: root.uiTextMain
                                                                        font.family: root.fontDataFamily
                                                                        font.pixelSize: Math.round(9 * root.uiScale)
                                                                        font.bold: true
                                                                    }
                                                                }
                                                            }
                                                            Text {
                                                                Layout.fillWidth: true
                                                                text: (controller.learnerSide === "P2" ? "ОБУЧЕНИЕ" : "ОППОНЕНТ")
                                                                    + " · " + (controller.learnerSide === "P2"
                                                                        ? controller.trainContextLearnerAlgoShort
                                                                        : controller.trainContextOpponentAlgoShort)
                                                                color: root.uiTextMuted
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                                wrapMode: Text.Wrap
                                                            }
                                                        }
                                                    }
                                                }

                                                GridLayout {
                                                    Layout.fillWidth: true
                                                    columns: trainCtxMainCol.trainCtxNarrow ? 1 : 2
                                                    columnSpacing: root.spacingMd + Math.round(6 * root.uiScale)
                                                    rowSpacing: root.spacingSm
                                                    flow: GridLayout.LeftToRight

                                                    ColumnLayout {
                                                        Layout.fillWidth: true
                                                        Layout.minimumWidth: Math.round(160 * root.uiScale)
                                                        spacing: root.spacingXs
                                                        Label {
                                                            text: "Состав P1"
                                                            color: root.uiTextMuted
                                                            font.family: root.fontUiFamily
                                                            font.bold: true
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.capitalization: Font.AllUppercase
                                                        }
                                                        Label {
                                                            visible: controller.trainContextP1RosterCards.length === 0
                                                            Layout.fillWidth: true
                                                            text: "Пусто — задайте на вкладке «Ростер»."
                                                            color: root.uiTextMuted
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            wrapMode: Text.Wrap
                                                        }
                                                        Repeater {
                                                            model: controller.trainContextP1RosterCards
                                                            delegate: Rectangle {
                                                                property var card: modelData
                                                                Layout.fillWidth: true
                                                                implicitHeight: (card && card.kind === "more")
                                                                    ? Math.round(34 * root.uiScale)
                                                                    : Math.round(82 * root.uiScale)
                                                                color: "#141b26"
                                                                border.width: 1
                                                                border.color: "#35475c"

                                                                RowLayout {
                                                                    id: trainCardRowP1
                                                                    anchors.left: parent.left
                                                                    anchors.right: parent.right
                                                                    anchors.top: parent.top
                                                                    anchors.margins: Math.round(6 * root.uiScale)
                                                                    spacing: Math.round(8 * root.uiScale)
                                                                    visible: card && card.kind !== "more"

                                                                    Item {
                                                                        Layout.alignment: Qt.AlignTop
                                                                        implicitWidth: Math.round(54 * root.uiScale)
                                                                        implicitHeight: Math.round(54 * root.uiScale)
                                                                        Rectangle {
                                                                            anchors.fill: parent
                                                                            radius: Math.round(5 * root.uiScale)
                                                                            color: "#161f2e"
                                                                            border.width: 1
                                                                            border.color: "#3a5068"
                                                                            Rectangle {
                                                                                anchors.fill: parent
                                                                                anchors.margins: Math.round(3 * root.uiScale)
                                                                                radius: Math.round(3 * root.uiScale)
                                                                                color: "#0a0e14"
                                                                                border.width: 1
                                                                                border.color: "#1e2a38"
                                                                                Image {
                                                                                    id: p1UnitImg
                                                                                    anchors.fill: parent
                                                                                    anchors.margins: Math.round(2 * root.uiScale)
                                                                                    fillMode: Image.PreserveAspectFit
                                                                                    smooth: true
                                                                                    source: (card && card.unitIcon) ? card.unitIcon : ""
                                                                                    visible: source !== ""
                                                                                }
                                                                                Label {
                                                                                    anchors.centerIn: parent
                                                                                    visible: !p1UnitImg.visible && card && card.unitName
                                                                                    text: {
                                                                                        var n = card && card.unitName ? String(card.unitName) : ""
                                                                                        return n.length ? n.charAt(0).toUpperCase() : "?"
                                                                                    }
                                                                                    color: root.uiTextMuted
                                                                                    font.bold: true
                                                                                    font.pixelSize: Math.round(18 * root.uiScale)
                                                                                }
                                                                            }
                                                                        }
                                                                    }

                                                                    ColumnLayout {
                                                                        Layout.fillWidth: true
                                                                        spacing: Math.round(2 * root.uiScale)
                                                                        Text {
                                                                            Layout.fillWidth: true
                                                                            text: card && card.title ? String(card.title).toUpperCase() : ""
                                                                            color: root.uiTextMain
                                                                            font.family: root.fontUiFamily
                                                                            font.bold: true
                                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                                            font.letterSpacing: 0.5
                                                                            wrapMode: Text.Wrap
                                                                            maximumLineCount: 1
                                                                            elide: Text.ElideRight
                                                                        }
                                                                        Text {
                                                                            Layout.fillWidth: true
                                                                            visible: card && card.instanceId && String(card.instanceId).length > 0
                                                                            text: "SYS.REF: " + (card ? card.instanceId : "")
                                                                            color: "#5c6a7d"
                                                                            font.family: "Consolas"
                                                                            font.pixelSize: Math.round(8 * root.uiScale)
                                                                        }
                                                                        RowLayout {
                                                                            Layout.fillWidth: true
                                                                            spacing: Math.round(2 * root.uiScale)
                                                                            Item {
                                                                                Layout.preferredWidth: Math.round(32 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.preferredHeight: Math.round(24 * root.uiScale)
                                                                                Image {
                                                                                    anchors.centerIn: parent
                                                                                    anchors.verticalCenterOffset: -Math.round(1 * root.uiScale)
                                                                                    width: Math.round(24 * root.uiScale)
                                                                                    height: Math.round(24 * root.uiScale)
                                                                                    fillMode: Image.PreserveAspectFit
                                                                                    smooth: true
                                                                                    visible: card && card.rangedIcon && String(card.rangedIcon).length > 0
                                                                                    source: (card && card.rangedIcon) ? card.rangedIcon : ""
                                                                                }
                                                                            }
                                                                            Text {
                                                                                Layout.preferredWidth: Math.round(56 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: "RANGED:"
                                                                                color: "#6d7a8a"
                                                                                font.family: "Consolas"
                                                                                font.pixelSize: Math.round(9 * root.uiScale)
                                                                                font.bold: true
                                                                                horizontalAlignment: Text.AlignLeft
                                                                                verticalAlignment: Text.AlignVCenter
                                                                                elide: Text.ElideRight
                                                                            }
                                                                            Text {
                                                                                Layout.fillWidth: true
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: card && card.rangedName ? card.rangedName : "—"
                                                                                color: "#f0f4fc"
                                                                                font.family: root.fontDataFamily
                                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                                                elide: Text.ElideRight
                                                                            }
                                                                        }
                                                                        RowLayout {
                                                                            Layout.fillWidth: true
                                                                            spacing: Math.round(2 * root.uiScale)
                                                                            Item {
                                                                                Layout.preferredWidth: Math.round(32 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.preferredHeight: Math.round(24 * root.uiScale)
                                                                                Image {
                                                                                    anchors.centerIn: parent
                                                                                    anchors.verticalCenterOffset: -Math.round(1 * root.uiScale)
                                                                                    width: Math.round(24 * root.uiScale)
                                                                                    height: Math.round(24 * root.uiScale)
                                                                                    fillMode: Image.PreserveAspectFit
                                                                                    smooth: true
                                                                                    visible: card && card.meleeIcon && String(card.meleeIcon).length > 0
                                                                                    source: (card && card.meleeIcon) ? card.meleeIcon : ""
                                                                                }
                                                                            }
                                                                            Text {
                                                                                Layout.preferredWidth: Math.round(56 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: "MELEE:"
                                                                                color: "#6d7a8a"
                                                                                font.family: "Consolas"
                                                                                font.pixelSize: Math.round(9 * root.uiScale)
                                                                                font.bold: true
                                                                                horizontalAlignment: Text.AlignLeft
                                                                                verticalAlignment: Text.AlignVCenter
                                                                                elide: Text.ElideRight
                                                                            }
                                                                            Text {
                                                                                Layout.fillWidth: true
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: card && card.meleeName ? card.meleeName : "—"
                                                                                color: "#f0f4fc"
                                                                                font.family: root.fontDataFamily
                                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                                                elide: Text.ElideRight
                                                                            }
                                                                        }
                                                                    }
                                                                }

                                                                MouseArea {
                                                                    id: trainP1TipArea
                                                                    anchors.fill: parent
                                                                    acceptedButtons: Qt.NoButton
                                                                    hoverEnabled: true
                                                                    z: 1
                                                                }
                                                                TacticalRosterTip {
                                                                    card: modelData
                                                                    anchorItem: trainP1TipArea
                                                                    accentColor: "#2f6ed8"
                                                                    secondaryAccentColor: "#d97706"
                                                                }
                                                                Rectangle {
                                                                    visible: card && card.kind === "unit"
                                                                    anchors.right: parent.right
                                                                    anchors.top: parent.top
                                                                    anchors.margins: Math.round(5 * root.uiScale)
                                                                    implicitHeight: Math.round(16 * root.uiScale)
                                                                    implicitWidth: trainP1StatusTxt.contentWidth + Math.round(10 * root.uiScale)
                                                                    radius: Math.round(2 * root.uiScale)
                                                                    color: "#0a0e14"
                                                                    border.width: 1
                                                                    border.color: (card && card.rangedName && card.meleeName && card.rangedName !== "—" && card.meleeName !== "—")
                                                                        ? "#2d6a40" : "#7a6230"
                                                                    Text {
                                                                        id: trainP1StatusTxt
                                                                        anchors.centerIn: parent
                                                                        text: (card && card.rangedName && card.meleeName && card.rangedName !== "—" && card.meleeName !== "—")
                                                                            ? "[ OK ]" : "[ RDY ]"
                                                                        color: (card && card.rangedName && card.meleeName && card.rangedName !== "—" && card.meleeName !== "—")
                                                                            ? "#5ee86a" : "#e6b84d"
                                                                        font.family: "Consolas"
                                                                        font.pixelSize: Math.round(8 * root.uiScale)
                                                                        font.bold: true
                                                                    }
                                                                }

                                                                Text {
                                                                    anchors.centerIn: parent
                                                                    visible: card && card.kind === "more"
                                                                    text: card ? card.title : ""
                                                                    color: root.uiTextMuted
                                                                    font.family: root.fontDataFamily
                                                                    font.pixelSize: Math.round(10 * root.uiScale)
                                                                }
                                                            }
                                                        }
                                                    }

                                                    ColumnLayout {
                                                        Layout.fillWidth: true
                                                        Layout.minimumWidth: Math.round(160 * root.uiScale)
                                                        spacing: root.spacingXs
                                                        Label {
                                                            text: "Состав P2"
                                                            color: root.uiTextMuted
                                                            font.family: root.fontUiFamily
                                                            font.bold: true
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.capitalization: Font.AllUppercase
                                                        }
                                                        Label {
                                                            visible: controller.trainContextP2RosterCards.length === 0
                                                            Layout.fillWidth: true
                                                            text: "Пусто — задайте на вкладке «Ростер»."
                                                            color: root.uiTextMuted
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            wrapMode: Text.Wrap
                                                        }
                                                        Repeater {
                                                            model: controller.trainContextP2RosterCards
                                                            delegate: Rectangle {
                                                                property var card: modelData
                                                                Layout.fillWidth: true
                                                                implicitHeight: (card && card.kind === "more")
                                                                    ? Math.round(34 * root.uiScale)
                                                                    : Math.round(82 * root.uiScale)
                                                                color: "#141b26"
                                                                border.width: 1
                                                                border.color: "#35475c"

                                                                RowLayout {
                                                                    id: trainCardRowP2
                                                                    anchors.left: parent.left
                                                                    anchors.right: parent.right
                                                                    anchors.top: parent.top
                                                                    anchors.margins: Math.round(6 * root.uiScale)
                                                                    spacing: Math.round(8 * root.uiScale)
                                                                    visible: card && card.kind !== "more"

                                                                    Item {
                                                                        Layout.alignment: Qt.AlignTop
                                                                        implicitWidth: Math.round(54 * root.uiScale)
                                                                        implicitHeight: Math.round(54 * root.uiScale)
                                                                        Rectangle {
                                                                            anchors.fill: parent
                                                                            radius: Math.round(5 * root.uiScale)
                                                                            color: "#161f2e"
                                                                            border.width: 1
                                                                            border.color: "#3a5068"
                                                                            Rectangle {
                                                                                anchors.fill: parent
                                                                                anchors.margins: Math.round(3 * root.uiScale)
                                                                                radius: Math.round(3 * root.uiScale)
                                                                                color: "#0a0e14"
                                                                                border.width: 1
                                                                                border.color: "#1e2a38"
                                                                                Image {
                                                                                    id: p2UnitImg
                                                                                    anchors.fill: parent
                                                                                    anchors.margins: Math.round(2 * root.uiScale)
                                                                                    fillMode: Image.PreserveAspectFit
                                                                                    smooth: true
                                                                                    source: (card && card.unitIcon) ? card.unitIcon : ""
                                                                                    visible: source !== ""
                                                                                }
                                                                                Label {
                                                                                    anchors.centerIn: parent
                                                                                    visible: !p2UnitImg.visible && card && card.unitName
                                                                                    text: {
                                                                                        var n = card && card.unitName ? String(card.unitName) : ""
                                                                                        return n.length ? n.charAt(0).toUpperCase() : "?"
                                                                                    }
                                                                                    color: root.uiTextMuted
                                                                                    font.bold: true
                                                                                    font.pixelSize: Math.round(18 * root.uiScale)
                                                                                }
                                                                            }
                                                                        }
                                                                    }

                                                                    ColumnLayout {
                                                                        Layout.fillWidth: true
                                                                        spacing: Math.round(2 * root.uiScale)
                                                                        Text {
                                                                            Layout.fillWidth: true
                                                                            text: card && card.title ? String(card.title).toUpperCase() : ""
                                                                            color: root.uiTextMain
                                                                            font.family: root.fontUiFamily
                                                                            font.bold: true
                                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                                            font.letterSpacing: 0.5
                                                                            wrapMode: Text.Wrap
                                                                            maximumLineCount: 1
                                                                            elide: Text.ElideRight
                                                                        }
                                                                        Text {
                                                                            Layout.fillWidth: true
                                                                            visible: card && card.instanceId && String(card.instanceId).length > 0
                                                                            text: "SYS.REF: " + (card ? card.instanceId : "")
                                                                            color: "#5c6a7d"
                                                                            font.family: "Consolas"
                                                                            font.pixelSize: Math.round(8 * root.uiScale)
                                                                        }
                                                                        RowLayout {
                                                                            Layout.fillWidth: true
                                                                            spacing: Math.round(2 * root.uiScale)
                                                                            Item {
                                                                                Layout.preferredWidth: Math.round(32 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.preferredHeight: Math.round(24 * root.uiScale)
                                                                                Image {
                                                                                    anchors.centerIn: parent
                                                                                    anchors.verticalCenterOffset: -Math.round(1 * root.uiScale)
                                                                                    width: Math.round(24 * root.uiScale)
                                                                                    height: Math.round(24 * root.uiScale)
                                                                                    fillMode: Image.PreserveAspectFit
                                                                                    smooth: true
                                                                                    visible: card && card.rangedIcon && String(card.rangedIcon).length > 0
                                                                                    source: (card && card.rangedIcon) ? card.rangedIcon : ""
                                                                                }
                                                                            }
                                                                            Text {
                                                                                Layout.preferredWidth: Math.round(56 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: "RANGED:"
                                                                                color: "#6d7a8a"
                                                                                font.family: "Consolas"
                                                                                font.pixelSize: Math.round(9 * root.uiScale)
                                                                                font.bold: true
                                                                                horizontalAlignment: Text.AlignLeft
                                                                                verticalAlignment: Text.AlignVCenter
                                                                                elide: Text.ElideRight
                                                                            }
                                                                            Text {
                                                                                Layout.fillWidth: true
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: card && card.rangedName ? card.rangedName : "—"
                                                                                color: "#f0f4fc"
                                                                                font.family: root.fontDataFamily
                                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                                                elide: Text.ElideRight
                                                                            }
                                                                        }
                                                                        RowLayout {
                                                                            Layout.fillWidth: true
                                                                            spacing: Math.round(2 * root.uiScale)
                                                                            Item {
                                                                                Layout.preferredWidth: Math.round(32 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(32 * root.uiScale)
                                                                                Layout.preferredHeight: Math.round(24 * root.uiScale)
                                                                                Image {
                                                                                    anchors.centerIn: parent
                                                                                    anchors.verticalCenterOffset: -Math.round(1 * root.uiScale)
                                                                                    width: Math.round(24 * root.uiScale)
                                                                                    height: Math.round(24 * root.uiScale)
                                                                                    fillMode: Image.PreserveAspectFit
                                                                                    smooth: true
                                                                                    visible: card && card.meleeIcon && String(card.meleeIcon).length > 0
                                                                                    source: (card && card.meleeIcon) ? card.meleeIcon : ""
                                                                                }
                                                                            }
                                                                            Text {
                                                                                Layout.preferredWidth: Math.round(56 * root.uiScale)
                                                                                Layout.maximumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.minimumWidth: Math.round(56 * root.uiScale)
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: "MELEE:"
                                                                                color: "#6d7a8a"
                                                                                font.family: "Consolas"
                                                                                font.pixelSize: Math.round(9 * root.uiScale)
                                                                                font.bold: true
                                                                                horizontalAlignment: Text.AlignLeft
                                                                                verticalAlignment: Text.AlignVCenter
                                                                                elide: Text.ElideRight
                                                                            }
                                                                            Text {
                                                                                Layout.fillWidth: true
                                                                                Layout.alignment: Qt.AlignVCenter
                                                                                text: card && card.meleeName ? card.meleeName : "—"
                                                                                color: "#f0f4fc"
                                                                                font.family: root.fontDataFamily
                                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                                                elide: Text.ElideRight
                                                                            }
                                                                        }
                                                                    }
                                                                }

                                                                MouseArea {
                                                                    id: trainP2TipArea
                                                                    anchors.fill: parent
                                                                    acceptedButtons: Qt.NoButton
                                                                    hoverEnabled: true
                                                                    z: 1
                                                                }
                                                                TacticalRosterTip {
                                                                    card: modelData
                                                                    anchorItem: trainP2TipArea
                                                                    accentColor: "#a44848"
                                                                    secondaryAccentColor: "#d97706"
                                                                }
                                                                Rectangle {
                                                                    visible: card && card.kind === "unit"
                                                                    anchors.right: parent.right
                                                                    anchors.top: parent.top
                                                                    anchors.margins: Math.round(5 * root.uiScale)
                                                                    implicitHeight: Math.round(16 * root.uiScale)
                                                                    implicitWidth: trainP2StatusTxt.contentWidth + Math.round(10 * root.uiScale)
                                                                    radius: Math.round(2 * root.uiScale)
                                                                    color: "#0a0e14"
                                                                    border.width: 1
                                                                    border.color: (card && card.rangedName && card.meleeName && card.rangedName !== "—" && card.meleeName !== "—")
                                                                        ? "#2d6a40" : "#7a6230"
                                                                    Text {
                                                                        id: trainP2StatusTxt
                                                                        anchors.centerIn: parent
                                                                        text: (card && card.rangedName && card.meleeName && card.rangedName !== "—" && card.meleeName !== "—")
                                                                            ? "[ OK ]" : "[ RDY ]"
                                                                        color: (card && card.rangedName && card.meleeName && card.rangedName !== "—" && card.meleeName !== "—")
                                                                            ? "#5ee86a" : "#e6b84d"
                                                                        font.family: "Consolas"
                                                                        font.pixelSize: Math.round(8 * root.uiScale)
                                                                        font.bold: true
                                                                    }
                                                                }

                                                                Text {
                                                                    anchors.centerIn: parent
                                                                    visible: card && card.kind === "more"
                                                                    text: card ? card.title : ""
                                                                    color: root.uiTextMuted
                                                                    font.family: root.fontDataFamily
                                                                    font.pixelSize: Math.round(10 * root.uiScale)
                                                                }
                                                            }
                                                        }
                                                    }
                                                }

                                                Text {
                                                    Layout.fillWidth: true
                                                    text: "> INFO: Дроны и опции листа здесь не показаны. Цифры оружия — во всплывающей подсказке при наведении на карточку или на вкладке «Ростер»."
                                                    color: "#4d5666"
                                                    font.family: "Consolas"
                                                    font.pixelSize: Math.round(8 * root.uiScale)
                                                    wrapMode: Text.Wrap
                                                }
                                            }
                                        }

                                        Flow {
                                            Layout.fillWidth: true
                                            spacing: Math.round(8 * root.uiScale)
                                            Rectangle {
                                                implicitHeight: Math.round(22 * root.uiScale)
                                                implicitWidth: trainTermMissionTxt.contentWidth + Math.round(14 * root.uiScale)
                                                radius: Math.round(2 * root.uiScale)
                                                color: "#0e141c"
                                                border.width: 1
                                                border.color: "#3a4d62"
                                                Text {
                                                    id: trainTermMissionTxt
                                                    anchors.centerIn: parent
                                                    text: "[ " + controller.selectedMission.toUpperCase().replace("_", " ") + " ]"
                                                    font.family: "Consolas"
                                                    font.pixelSize: Math.round(9 * root.uiScale)
                                                    color: "#9db0c8"
                                                }
                                            }
                                            Text {
                                                text: "//"
                                                color: "#3d4a5c"
                                                font.family: "Consolas"
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Rectangle {
                                                implicitHeight: Math.round(22 * root.uiScale)
                                                implicitWidth: trainTermEpTxt.contentWidth + Math.round(14 * root.uiScale)
                                                radius: Math.round(2 * root.uiScale)
                                                color: "#0e141c"
                                                border.width: 1
                                                border.color: "#3a4d62"
                                                Text {
                                                    id: trainTermEpTxt
                                                    anchors.centerIn: parent
                                                    text: "[ " + controller.numGames + " EP ]"
                                                    font.family: "Consolas"
                                                    font.pixelSize: Math.round(9 * root.uiScale)
                                                    color: "#9db0c8"
                                                }
                                            }
                                            Text {
                                                text: "//"
                                                color: "#3d4a5c"
                                                font.family: "Consolas"
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Rectangle {
                                                implicitHeight: Math.round(22 * root.uiScale)
                                                implicitWidth: trainTermP1Txt.contentWidth + Math.round(14 * root.uiScale)
                                                radius: Math.round(2 * root.uiScale)
                                                color: "#0e141c"
                                                border.width: 1
                                                border.color: "#3a4d62"
                                                Text {
                                                    id: trainTermP1Txt
                                                    anchors.centerIn: parent
                                                    text: "[ P1: " + (controller.learnerSide === "P1" ? controller.trainContextLearnerAlgoTerminal : controller.trainContextOpponentAlgoTerminal) + " ]"
                                                    font.family: "Consolas"
                                                    font.pixelSize: Math.round(9 * root.uiScale)
                                                    color: "#9db0c8"
                                                }
                                            }
                                            Text {
                                                text: "//"
                                                color: "#3d4a5c"
                                                font.family: "Consolas"
                                                font.pixelSize: Math.round(9 * root.uiScale)
                                            }
                                            Rectangle {
                                                implicitHeight: Math.round(22 * root.uiScale)
                                                implicitWidth: trainTermP2Txt.contentWidth + Math.round(14 * root.uiScale)
                                                radius: Math.round(2 * root.uiScale)
                                                color: "#0e141c"
                                                border.width: 1
                                                border.color: "#3a4d62"
                                                Text {
                                                    id: trainTermP2Txt
                                                    anchors.centerIn: parent
                                                    text: "[ P2: " + (controller.learnerSide === "P2" ? controller.trainContextLearnerAlgoTerminal : controller.trainContextOpponentAlgoTerminal) + " ]"
                                                    font.family: "Consolas"
                                                    font.pixelSize: Math.round(9 * root.uiScale)
                                                    color: "#9db0c8"
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
                                                    onClicked: trainLog.clearAll()
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

                                        TrainLogView {
                                            id: trainLog
                                            Layout.fillWidth: true
                                            Layout.fillHeight: true
                                            visible: root.mainLogExpanded
                                            uiScale: root.uiScale
                                            fontDataFamily: root.fontDataFamily
                                            fontUiFamily: root.fontUiFamily
                                        }
                                    }
                                }
                            }
                        }

                        ColumnLayout {
                            Layout.preferredWidth: Math.round(380 * root.uiScale)
                            Layout.minimumWidth: Math.round(320 * root.uiScale)
                            Layout.maximumWidth: Math.round(420 * root.uiScale)
                            Layout.fillHeight: true
                            spacing: root.spacingMd

                            ScrollView {
                                id: mainRailScroll
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                clip: true

                                ColumnLayout {
                                    width: mainRailScroll.availableWidth
                                    spacing: root.spacingMd
                                    ChamferPanel {
                                        Layout.fillWidth: true
                                        Layout.minimumWidth: 0
                                        implicitHeight: missionPanelCol.implicitHeight + 2 * root.spacingMd
                                        fillColor: root.uiBgCard
                                        borderColor: root.uiBorder
                                        borderWidth: 1
                                        cutSize: Math.round(10 * root.uiScale)
                                        contentMargin: root.spacingMd

                                        ColumnLayout {
                                            id: missionPanelCol
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.top: parent.top
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
                                                    text: controller.selectedMission === "annihilation"
                                                          ? "ANNIHILATION / KILL POINTS"
                                                          : "ONLY WAR"
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
                                                    text: controller.selectedMission === "annihilation"
                                                          ? "точек нет (Kill Points)"
                                                          : "1, центр (30,20)"
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
                                                    text: controller.selectedMission === "annihilation"
                                                          ? "победа по уничтоженным юнитам врага"
                                                          : "roll-off определяет роли"
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
                                        implicitHeight: configPanelCol.implicitHeight + 2 * root.spacingMd
                                        fillColor: root.uiBgCard
                                        borderColor: root.uiBorder
                                        borderWidth: 1
                                        cutSize: Math.round(10 * root.uiScale)
                                        contentMargin: root.spacingMd

                                        ColumnLayout {
                                            id: configPanelCol
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.top: parent.top
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
                                                visible: controller.opponentSource !== "heuristic"
                                                Label {
                                                    text: "СНАПШОТ В РЕЕСТР"
                                                    font.bold: true
                                                    color: root.uiTextMuted
                                                    ToolTip.visible: hovered
                                                    ToolTip.text: "Как часто сохранять learner в реестр лиги (каждые N игр) и обновлять зеркало PPO self-play. В конце прогона — всегда финальный снапшот."
                                                    ToolTip.delay: 400
                                                }
                                                TextField {
                                                    id: selfPlaySnapshotEveryField
                                                    text: controller.selfPlaySnapshotEvery.toString()
                                                    validator: IntValidator { bottom: 1 }
                                                    Layout.preferredWidth: root.inputWidthMd
                                                    font.family: root.fontDataFamily
                                                    enabled: !controller.running
                                                    background: Rectangle {
                                                        radius: 0
                                                        color: parent.activeFocus ? "#1e2633" : "#141b26"
                                                        border.width: 1
                                                        border.color: parent.activeFocus ? "#b88a26" : "#2f3848"
                                                    }
                                                    onEditingFinished: {
                                                        var value = parseInt(text)
                                                        if (!isNaN(value)) {
                                                            controller.set_self_play_snapshot_every(value)
                                                        }
                                                    }
                                                }
                                                Label {
                                                    text: "игр"
                                                    color: root.uiTextMuted
                                                    font.pixelSize: root.evalCaptionSize
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
                                                        { value: "alphazero_tree", label: "ALPHAZERO TREE" },
                                                        { value: "alphazero_proxy", label: "ALPHAZERO PROXY" },
                                                        { value: "gumbel_muzero", label: "GUMBEL MUZERO" },
                                                        { value: "sampled_muzero", label: "SAMPLED MUZERO" },
                                                        { value: "gumbel_az", label: "GUMBEL ALPHAZERO" },
                                                        { value: "phoenix", label: "PHOENIX" }
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
                                                        { value: "specific_agent", label: "КОНКРЕТНЫЙ АГЕНТ" },
                                                        { value: "pool", label: "ПУЛ / ЛИГА (PFSP)" }
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
                                        implicitHeight: opsPanelCol.implicitHeight + 2 * root.spacingMd
                                        fillColor: root.uiBgCard
                                        borderColor: root.uiBorder
                                        borderWidth: 1
                                        cutSize: Math.round(10 * root.uiScale)
                                        contentMargin: root.spacingMd

                                        ColumnLayout {
                                            id: opsPanelCol
                                            anchors.left: parent.left
                                            anchors.right: parent.right
                                            anchors.top: parent.top
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
                                        }
                                    }
                                }
                            }

                            ChamferPanel {
                                Layout.fillWidth: true
                                fillColor: root.uiBgCard
                                borderColor: root.uiBorder
                                borderWidth: 1
                                cutSize: Math.round(10 * root.uiScale)
                                contentMargin: root.spacingMd
                                implicitHeight: mainActionsCol.implicitHeight + 2 * root.spacingMd

                                ColumnLayout {
                                    id: mainActionsCol
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    spacing: root.spacingSm

                                    Button {
                                        text: "ТРЕНИРОВКА 8X"
                                        enabled: !controller.running
                                        onClicked: controller.start_train_8x()
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(40 * root.uiScale)
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.enabled ? "#151102" : "#6a6347"
                                            font.bold: true
                                            font.family: root.fontUiFamily
                                            font.pixelSize: Math.round(13 * root.uiScale)
                                            font.letterSpacing: 1.0
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: ChamferPanel {
                                            cutSize: Math.round(8 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: parent.pressed ? "#d7a719" : (parent.hovered ? "#e8b932" : "#b88a26")
                                            borderWidth: 1
                                            borderColor: parent.hovered ? "#ffe08a" : "#8f6b1f"
                                        }
                                    }

                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: root.spacingSm
                                        Button {
                                            text: "ОЧИСТИТЬ КЭШ"
                                            enabled: !controller.running
                                            onClicked: clearCacheDialog.open()
                                            Layout.fillWidth: true
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.enabled ? "#d5b15a" : "#737b8a"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                elide: Text.ElideRight
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
                                            text: "TENSORBOARD"
                                            onClicked: tbWindow.openTensorboard()
                                            Layout.fillWidth: true
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.enabled ? "#d5b15a" : "#737b8a"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                elide: Text.ElideRight
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
                                            Layout.fillWidth: true
                                            contentItem: Text {
                                                text: parent.text
                                                color: parent.enabled ? "#d5b15a" : "#737b8a"
                                                font.bold: true
                                                font.pixelSize: root.evalCaptionSize
                                                elide: Text.ElideRight
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
                        Layout.preferredHeight: Math.round(188 * root.uiScale)
                        Layout.minimumHeight: Math.round(168 * root.uiScale)
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
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                Layout.preferredHeight: Math.round(138 * root.uiScale)
                                spacing: root.spacingMd

                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.minimumWidth: Math.round(160 * root.uiScale)
                                    implicitHeight: Math.round(136 * root.uiScale)
                                    color: "#151f33"
                                    border.width: 1
                                    border.color: "#2f6ed8"
                                    radius: 0
                                    clip: true
                                    Column {
                                        anchors.fill: parent
                                        anchors.margins: Math.round(8 * root.uiScale)
                                        spacing: Math.round(6 * root.uiScale)
                                        Text { width: parent.width; text: "P1 СВОДКА"; color: "#9eb6d4"; font.bold: true; font.family: root.fontUiFamily; font.pixelSize: Math.round(10 * root.uiScale); elide: Text.ElideRight }
                                        Text { width: parent.width; text: controller.rosterPointsP1; color: "#f2f6ff"; font.bold: true; font.family: "JetBrains Mono"; font.pixelSize: Math.round(18 * root.uiScale); elide: Text.ElideRight }
                                        Item {
                                            width: parent.width
                                            implicitHeight: kpiClusterP1.implicitHeight
                                            Row {
                                                id: kpiClusterP1
                                                anchors.left: parent.left
                                                spacing: Math.round(8 * root.uiScale)
                                                Repeater {
                                                    model: controller.rosterKpiP1Columns
                                                    delegate: Row {
                                                        property var col: modelData
                                                        spacing: Math.round(8 * root.uiScale)
                                                        Text {
                                                            text: "[ " + (col && col.h ? col.h : "—") + ": " + (col && col.v !== undefined ? col.v : "—") + " ]"
                                                            color: "#a8bdd4"
                                                            font.family: "JetBrains Mono"
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.bold: true
                                                        }
                                                        Text {
                                                            visible: index < 3
                                                            text: "//"
                                                            color: "#52657f"
                                                            font.family: "JetBrains Mono"
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.bold: true
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }

                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.minimumWidth: Math.round(160 * root.uiScale)
                                    implicitHeight: Math.round(136 * root.uiScale)
                                    color: "#151f33"
                                    border.width: 1
                                    border.color: "#7b4a4a"
                                    radius: 0
                                    clip: true
                                    Column {
                                        anchors.fill: parent
                                        anchors.margins: Math.round(8 * root.uiScale)
                                        spacing: Math.round(6 * root.uiScale)
                                        Text { width: parent.width; text: "P2 СВОДКА"; color: "#d4a69e"; font.bold: true; font.family: root.fontUiFamily; font.pixelSize: Math.round(10 * root.uiScale); elide: Text.ElideRight }
                                        Text { width: parent.width; text: controller.rosterPointsP2; color: "#f2f6ff"; font.bold: true; font.family: "JetBrains Mono"; font.pixelSize: Math.round(18 * root.uiScale); elide: Text.ElideRight }
                                        Item {
                                            width: parent.width
                                            implicitHeight: kpiClusterP2.implicitHeight
                                            Row {
                                                id: kpiClusterP2
                                                anchors.left: parent.left
                                                spacing: Math.round(8 * root.uiScale)
                                                Repeater {
                                                    model: controller.rosterKpiP2Columns
                                                    delegate: Row {
                                                        property var col: modelData
                                                        spacing: Math.round(8 * root.uiScale)
                                                        Text {
                                                            text: "[ " + (col && col.h ? col.h : "—") + ": " + (col && col.v !== undefined ? col.v : "—") + " ]"
                                                            color: "#d4c4c0"
                                                            font.family: "JetBrains Mono"
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.bold: true
                                                        }
                                                        Text {
                                                            visible: index < 3
                                                            text: "//"
                                                            color: "#6a5154"
                                                            font.family: "JetBrains Mono"
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.bold: true
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

                                    Connections {
                                        target: controller
                                        function onRosterWeaponsPreviewChanged() {
                                            var i = controller.rosterAvailableUnitListIndex
                                            if (i >= 0 && i < availableUnitsView.count)
                                                availableUnitsView.currentIndex = i
                                            else if (availableUnitsView.count > 0 && i < 0)
                                                availableUnitsView.currentIndex = 0
                                        }
                                    }
                                    Component.onCompleted: {
                                        var i = controller.rosterAvailableUnitListIndex
                                        if (i >= 0 && i < availableUnitsView.count)
                                            availableUnitsView.currentIndex = i
                                        else if (count > 0)
                                            availableUnitsView.currentIndex = 0
                                    }

                                    delegate: Rectangle {
                                        readonly property bool rowSel: ListView.view
                                            ? (ListView.view.currentIndex === index)
                                            : false
                                        width: ListView.view ? ListView.view.width : 0
                                        height: Math.max(unitNameAvailable.implicitHeight, unitIconAvailable.height) + root.spacingSm
                                        color: rowSel
                                            ? Qt.rgba(0.85, 0.47, 0.04, 0.14)
                                            : (unitRowMa.containsMouse ? Qt.rgba(1, 1, 1, 0.05) : "transparent")
                                        border.width: rowSel ? 1 : 0
                                        border.color: rowSel ? Qt.rgba(0.85, 0.47, 0.04, 0.45) : "transparent"
                                        Behavior on color { ColorAnimation { duration: 100 } }
                                        Behavior on border.color { ColorAnimation { duration: 100 } }
                                        Behavior on border.width { NumberAnimation { duration: 100 } }

                                        Rectangle {
                                            visible: rowSel
                                            anchors.left: parent.left
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            width: Math.round(4 * root.uiScale)
                                            color: "#d97706"
                                        }

                                        Image {
                                            id: unitIconAvailable
                                            source: controller.unit_icon_source(model.display)
                                            width: root.unitIconSize
                                            height: root.unitIconSize
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: parent.left
                                            anchors.leftMargin: root.spacingSm + (rowSel ? Math.round(4 * root.uiScale) : 0)
                                            fillMode: Image.PreserveAspectFit
                                            smooth: true
                                            visible: source !== ""
                                        }

                                        Text {
                                            id: unitNameAvailable
                                            text: model.display
                                            color: rowSel ? "#f8fafc" : "#94a3b8"
                                            font.bold: rowSel
                                            elide: Text.ElideRight
                                            anchors.verticalCenter: parent.verticalCenter
                                            anchors.left: unitIconAvailable.visible ? unitIconAvailable.right : parent.left
                                            anchors.leftMargin: unitIconAvailable.visible
                                                ? root.spacingSm
                                                : (root.spacingSm + (rowSel ? Math.round(4 * root.uiScale) : 0))
                                            font.family: root.fontUiFamily
                                        }

                                        MouseArea {
                                            id: unitRowMa
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            onClicked: controller.set_roster_available_preview_index(index)
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
                            Layout.minimumWidth: Math.round(230 * root.uiScale)
                            Layout.preferredWidth: Math.round(300 * root.uiScale)
                            Layout.maximumWidth: Math.round(360 * root.uiScale)
                            Layout.horizontalStretchFactor: 2

                            background: Rectangle {
                                color: root.bgElevated
                                border.width: 1
                                border.color: root.uiBorder
                            }

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: root.spacingXs
                                spacing: Math.round(6 * root.uiScale)

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
                                    text: controller.rosterWeaponsPreviewUnitName === "—" ? "Юнит не выбран" : controller.rosterWeaponsPreviewUnitName
                                    font.bold: true
                                    color: root.uiTextMain
                                    elide: Text.ElideRight
                                    Layout.fillWidth: true
                                    font.pixelSize: Math.round(13 * root.uiScale)
                                    font.family: root.fontUiFamily
                                }
                                Label {
                                    text: "Профили ниже — только шаблон для следующего добавления (кнопки «Добавить в P1/P2»). Уже в ростере отряды сохраняют своё оружие; разные отряды одного типа могут отличаться."
                                    color: "#8b95a8"
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                    font.family: root.fontUiFamily
                                    font.pixelSize: Math.round(10 * root.uiScale)
                                }
                                Rectangle {
                                    Layout.fillWidth: true
                                    implicitHeight: briefInner.implicitHeight + Math.round(14 * root.uiScale)
                                    color: "#080d14"
                                    border.width: 0
                                    radius: 0
                                    Rectangle {
                                        anchors.left: parent.left
                                        anchors.top: parent.top
                                        anchors.bottom: parent.bottom
                                        width: Math.round(3 * root.uiScale)
                                        color: "#6b5a32"
                                    }
                                    ColumnLayout {
                                        id: briefInner
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.top: parent.top
                                        anchors.leftMargin: Math.round(12 * root.uiScale)
                                        anchors.rightMargin: Math.round(8 * root.uiScale)
                                        anchors.topMargin: Math.round(8 * root.uiScale)
                                        anchors.bottomMargin: Math.round(8 * root.uiScale)
                                        spacing: Math.round(4 * root.uiScale)
                                        Text {
                                            text: "// LOADOUT.AUDIT"
                                            color: "#4a5566"
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(7 * root.uiScale)
                                        }
                                        Text {
                                            Layout.fillWidth: true
                                            text: "> ДАЛЬНИЙ: " + controller.rosterWeaponsSelectedRanged
                                            color: "#b8c8dc"
                                            wrapMode: Text.WordWrap
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                        }
                                        Text {
                                            Layout.fillWidth: true
                                            text: "> БЛИЖНИЙ: " + controller.rosterWeaponsSelectedMelee
                                            color: "#b8c8dc"
                                            wrapMode: Text.WordWrap
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                        }
                                        Text {
                                            readonly property bool ready: controller.rosterWeaponsPreviewUnitName !== "—"
                                                && controller.rosterWeaponsSelectedRanged !== "—"
                                                && controller.rosterWeaponsSelectedMelee !== "—"
                                            text: ready ? "STATUS: LOADOUT READY" : "STATUS: AWAITING SELECTION"
                                            color: ready ? "#7bc96f" : "#c9a227"
                                            font.family: root.fontDataFamily
                                            font.pixelSize: Math.round(9 * root.uiScale)
                                            font.bold: true
                                        }
                                    }
                                }

                                Text {
                                    Layout.fillWidth: true
                                    text: "> ДАЛЬНИЙ БОЙ  [ " + controller.rosterWeaponsPreviewRangedCount + " проф. ]"
                                    color: "#7d8a9c"
                                    font.family: root.fontUiFamily
                                    font.pixelSize: Math.round(11 * root.uiScale)
                                    font.capitalization: Font.AllUppercase
                                    font.letterSpacing: 0.7
                                }
                                Item {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: Math.round(6 * root.uiScale)
                                }
                                Repeater {
                                    model: controller.rosterWeaponsPreviewRanged
                                    delegate: Rectangle {
                                        readonly property string rwWeaponName: modelData
                                        readonly property bool rwSel: rwWeaponName === controller.rosterWeaponsSelectedRanged
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(90 * root.uiScale)
                                        color: "#0b1628"
                                        border.width: rwSel ? 2 : 1
                                        border.color: rwSel ? "#e8c86a" : "#334155"
                                        radius: 0
                                        Rectangle {
                                            anchors.fill: parent
                                            anchors.margins: 2
                                            color: "transparent"
                                            border.width: 1
                                            border.color: Qt.rgba(0, 0, 0, 0.35)
                                        }
                                        Rectangle {
                                            anchors.fill: parent
                                            gradient: Gradient {
                                                GradientStop { position: 0.0; color: Qt.rgba(0, 0, 0, 0.12) }
                                                GradientStop { position: 0.18; color: Qt.rgba(0, 0, 0, 0.02) }
                                                GradientStop { position: 0.82; color: "transparent" }
                                                GradientStop { position: 1.0; color: Qt.rgba(0, 0, 0, 0.2) }
                                            }
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                            anchors.margins: Math.round(8 * root.uiScale)
                                            spacing: root.spacingSm

                                            Item {
                                                Layout.preferredWidth: Math.round(16 * root.uiScale)
                                                Layout.preferredHeight: Math.round(16 * root.uiScale)
                                                Layout.alignment: Qt.AlignTop
                                                Layout.topMargin: Math.round(4 * root.uiScale)
                                                Rectangle {
                                                    anchors.fill: parent
                                                    radius: 0
                                                    color: "transparent"
                                                    border.width: rwSel ? 2 : 1
                                                    border.color: rwSel ? "#e8c86a" : "#4a5568"
                                                }
                                                Rectangle {
                                                    anchors.centerIn: parent
                                                    width: Math.round(6 * root.uiScale)
                                                    height: Math.round(6 * root.uiScale)
                                                    visible: rwSel
                                                    color: "#c79a32"
                                                    radius: 0
                                                }
                                            }

                                            Rectangle {
                                                Layout.preferredWidth: Math.round(44 * root.uiScale)
                                                Layout.preferredHeight: Math.round(44 * root.uiScale)
                                                Layout.alignment: Qt.AlignTop
                                                color: root.rosterSlateInstrumentBg
                                                border.width: 1
                                                border.color: "#323c4d"
                                                Image {
                                                    anchors.centerIn: parent
                                                    width: Math.round(36 * root.uiScale)
                                                    height: Math.round(36 * root.uiScale)
                                                    source: controller.roster_weapon_icon_source(rwWeaponName)
                                                    fillMode: Image.PreserveAspectFit
                                                    smooth: true
                                                    visible: source !== ""
                                                }
                                            }

                                            ColumnLayout {
                                                Layout.fillWidth: true
                                                spacing: Math.round(4 * root.uiScale)
                                                Text {
                                                    Layout.fillWidth: true
                                                    text: rwWeaponName
                                                    color: root.uiTextMain
                                                    font.bold: true
                                                    font.family: root.fontUiFamily
                                                    font.pixelSize: Math.round(12 * root.uiScale)
                                                    elide: Text.ElideRight
                                                }
                                                Row {
                                                    spacing: 0
                                                    Repeater {
                                                        model: 6
                                                        delegate: Column {
                                                            property int colIndex: index
                                                            width: root.rosterWeaponStatColWidths[colIndex]
                                                            spacing: Math.round(3 * root.uiScale)
                                                            Text {
                                                                width: parent.width
                                                                horizontalAlignment: Text.AlignHCenter
                                                                text: root.rosterWeaponStatHdrs[colIndex]
                                                                color: "#5c6678"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(7 * root.uiScale)
                                                                font.letterSpacing: 0.35
                                                            }
                                                            Text {
                                                                width: parent.width
                                                                horizontalAlignment: Text.AlignHCenter
                                                                text: controller.roster_weapon_stat_values_for_selected(rwWeaponName)[colIndex]
                                                                color: "#f4f7fc"
                                                                font.weight: Font.DemiBold
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }
                                                Flow {
                                                    Layout.fillWidth: true
                                                    spacing: root.rosterSlateGridStep
                                                    Repeater {
                                                        model: controller.roster_weapon_ability_badges_for_weapon(rwWeaponName)
                                                        delegate: Rectangle {
                                                            color: "#141b26"
                                                            border.width: 1
                                                            border.color: "#4a5c72"
                                                            radius: 0
                                                            implicitWidth: badgeRText.implicitWidth + Math.round(12 * root.uiScale)
                                                            implicitHeight: badgeRText.implicitHeight + Math.round(4 * root.uiScale)
                                                            Text {
                                                                id: badgeRText
                                                                anchors.centerIn: parent
                                                                text: modelData
                                                                color: "#b8c8dc"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: controller.set_selected_roster_ranged_weapon(rwWeaponName)
                                        }
                                    }
                                }

                                Text {
                                    Layout.fillWidth: true
                                    text: "> БЛИЖНИЙ БОЙ  [ " + controller.rosterWeaponsPreviewMeleeCount + " проф. ]"
                                    color: "#8a7d6a"
                                    font.family: root.fontUiFamily
                                    font.pixelSize: Math.round(11 * root.uiScale)
                                    font.capitalization: Font.AllUppercase
                                    font.letterSpacing: 0.7
                                }
                                Item {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: Math.round(6 * root.uiScale)
                                }
                                Repeater {
                                    model: controller.rosterWeaponsPreviewMelee
                                    delegate: Rectangle {
                                        readonly property string mwWeaponName: modelData
                                        readonly property bool mwSel: mwWeaponName === controller.rosterWeaponsSelectedMelee
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(90 * root.uiScale)
                                        color: "#0b1628"
                                        border.width: mwSel ? 2 : 1
                                        border.color: mwSel ? "#e8c86a" : "#334155"
                                        radius: 0
                                        Rectangle {
                                            anchors.fill: parent
                                            anchors.margins: 2
                                            color: "transparent"
                                            border.width: 1
                                            border.color: Qt.rgba(0, 0, 0, 0.35)
                                        }
                                        Rectangle {
                                            anchors.fill: parent
                                            gradient: Gradient {
                                                GradientStop { position: 0.0; color: Qt.rgba(0, 0, 0, 0.12) }
                                                GradientStop { position: 0.18; color: Qt.rgba(0, 0, 0, 0.02) }
                                                GradientStop { position: 0.82; color: "transparent" }
                                                GradientStop { position: 1.0; color: Qt.rgba(0, 0, 0, 0.2) }
                                            }
                                        }

                                        RowLayout {
                                            anchors.fill: parent
                                            anchors.margins: Math.round(8 * root.uiScale)
                                            spacing: root.spacingSm

                                            Item {
                                                Layout.preferredWidth: Math.round(16 * root.uiScale)
                                                Layout.preferredHeight: Math.round(16 * root.uiScale)
                                                Layout.alignment: Qt.AlignTop
                                                Layout.topMargin: Math.round(4 * root.uiScale)
                                                Rectangle {
                                                    anchors.fill: parent
                                                    radius: 0
                                                    color: "transparent"
                                                    border.width: mwSel ? 2 : 1
                                                    border.color: mwSel ? "#e8c86a" : "#4a5568"
                                                }
                                                Rectangle {
                                                    anchors.centerIn: parent
                                                    width: Math.round(6 * root.uiScale)
                                                    height: Math.round(6 * root.uiScale)
                                                    visible: mwSel
                                                    color: "#c79a32"
                                                    radius: 0
                                                }
                                            }

                                            Rectangle {
                                                Layout.preferredWidth: Math.round(44 * root.uiScale)
                                                Layout.preferredHeight: Math.round(44 * root.uiScale)
                                                Layout.alignment: Qt.AlignTop
                                                color: root.rosterSlateInstrumentBg
                                                border.width: 1
                                                border.color: "#323c4d"
                                                Image {
                                                    anchors.centerIn: parent
                                                    width: Math.round(36 * root.uiScale)
                                                    height: Math.round(36 * root.uiScale)
                                                    source: controller.roster_weapon_icon_source(mwWeaponName)
                                                    fillMode: Image.PreserveAspectFit
                                                    smooth: true
                                                    visible: source !== ""
                                                }
                                            }

                                            ColumnLayout {
                                                Layout.fillWidth: true
                                                spacing: Math.round(4 * root.uiScale)
                                                Text {
                                                    Layout.fillWidth: true
                                                    text: mwWeaponName
                                                    color: root.uiTextMain
                                                    font.bold: true
                                                    font.family: root.fontUiFamily
                                                    font.pixelSize: Math.round(12 * root.uiScale)
                                                    elide: Text.ElideRight
                                                }
                                                Row {
                                                    spacing: 0
                                                    Repeater {
                                                        model: 6
                                                        delegate: Column {
                                                            property int colIndex: index
                                                            width: root.rosterWeaponStatColWidths[colIndex]
                                                            spacing: Math.round(3 * root.uiScale)
                                                            Text {
                                                                width: parent.width
                                                                horizontalAlignment: Text.AlignHCenter
                                                                text: root.rosterWeaponStatHdrs[colIndex]
                                                                color: "#5c6678"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(7 * root.uiScale)
                                                                font.letterSpacing: 0.35
                                                            }
                                                            Text {
                                                                width: parent.width
                                                                horizontalAlignment: Text.AlignHCenter
                                                                text: controller.roster_weapon_stat_values_for_selected(mwWeaponName)[colIndex]
                                                                color: "#f4f7fc"
                                                                font.weight: Font.DemiBold
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(10 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }
                                                Flow {
                                                    Layout.fillWidth: true
                                                    spacing: root.rosterSlateGridStep
                                                    Repeater {
                                                        model: controller.roster_weapon_ability_badges_for_weapon(mwWeaponName)
                                                        delegate: Rectangle {
                                                            color: "#141b26"
                                                            border.width: 1
                                                            border.color: "#4a5c72"
                                                            radius: 0
                                                            implicitWidth: badgeMText.implicitWidth + Math.round(12 * root.uiScale)
                                                            implicitHeight: badgeMText.implicitHeight + Math.round(4 * root.uiScale)
                                                            Text {
                                                                id: badgeMText
                                                                anchors.centerIn: parent
                                                                text: modelData
                                                                color: "#b8c8dc"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        MouseArea {
                                            anchors.fill: parent
                                            onClicked: controller.set_selected_roster_melee_weapon(mwWeaponName)
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Layout.topMargin: Math.round(12 * root.uiScale)
                                    spacing: root.spacingSm
                                    Button {
                                        id: addP1WorkbenchBtn
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(46 * root.uiScale)
                                        text: "[ ДОБАВИТЬ В P1 ]"
                                        flat: true
                                        onClicked: controller.add_unit_to_player(availableUnitsView.currentIndex)
                                        background: ChamferPanel {
                                            cutSize: Math.round(10 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: addP1WorkbenchBtn.pressed ? "#152540"
                                                : (addP1WorkbenchBtn.hovered ? "#1a3150" : "#121824")
                                            borderWidth: 2
                                            borderColor: addP1WorkbenchBtn.hovered ? "#7eb0f0" : "#2f6ed8"
                                        }
                                        contentItem: Text {
                                            text: addP1WorkbenchBtn.text
                                            color: addP1WorkbenchBtn.pressed ? "#ffffff"
                                                : (addP1WorkbenchBtn.hovered ? "#e8f0ff" : "#c8d8f5")
                                            font.family: "JetBrains Mono"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                    Button {
                                        id: addP2WorkbenchBtn
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(46 * root.uiScale)
                                        text: "[ ДОБАВИТЬ В P2 ]"
                                        flat: true
                                        onClicked: controller.add_unit_to_model(availableUnitsView.currentIndex)
                                        background: ChamferPanel {
                                            cutSize: Math.round(10 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: addP2WorkbenchBtn.pressed ? "#301818"
                                                : (addP2WorkbenchBtn.hovered ? "#3a1e1e" : "#1a1214")
                                            borderWidth: 2
                                            borderColor: addP2WorkbenchBtn.hovered ? "#e08080" : "#a44848"
                                        }
                                        contentItem: Text {
                                            text: addP2WorkbenchBtn.text
                                            color: addP2WorkbenchBtn.pressed ? "#ffffff"
                                                : (addP2WorkbenchBtn.hovered ? "#ffe8e8" : "#f0c9c9")
                                            font.family: "JetBrains Mono"
                                            font.pixelSize: Math.round(11 * root.uiScale)
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
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

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    Layout.minimumHeight: 0
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
                                    Layout.fillHeight: false
                                    Layout.preferredHeight: Math.min(contentHeight, Math.round(430 * root.uiScale))
                                    Layout.minimumHeight: 0
                                    model: controller.playerRosterModel
                                    clip: true
                                    add: Transition {
                                        NumberAnimation { property: "opacity"; from: 0; to: 1; duration: 100; easing.type: Easing.OutQuad }
                                    }
                                    remove: Transition {
                                        NumberAnimation { property: "opacity"; from: 1; to: 0; duration: 90; easing.type: Easing.InQuad }
                                    }
                                    displaced: Transition {
                                        NumberAnimation { properties: "x,y"; duration: 100; easing.type: Easing.OutQuad }
                                    }
                                    // Data Slate P1 — при изменении зеркалить блок P2 ниже (keep in sync)
                                    delegate: Item {
                                        width: ListView.view ? ListView.view.width : 0
                                        implicitHeight: cardP1.implicitHeight
                                        height: implicitHeight

                                        readonly property bool isCurrent: ListView.view ? (ListView.view.currentIndex === index) : false

                                        Rectangle {
                                            id: cardP1
                                            z: 1
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            width: parent.width
                                            implicitHeight: Math.max(Math.round(124 * root.uiScale), slateP1.implicitHeight + 2 * root.spacingSm)
                                            height: implicitHeight
                                            clip: true
                                            color: controller.roster_entry_active("P1", index) ? "#1f2f45" : "#141b26"
                                            border.width: isCurrent ? 2 : 1
                                            border.color: controller.roster_entry_active("P1", index) ? "#d5b15a" : "#2f6ed8"
                                            radius: 0
                                            Behavior on color { ColorAnimation { duration: 100 } }
                                            Behavior on border.color { ColorAnimation { duration: 100 } }
                                            Behavior on border.width { NumberAnimation { duration: 100 } }

                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.top: parent.top
                                                width: Math.max(1, Math.round(1 * root.uiScale))
                                                height: parent.height
                                                color: controller.roster_entry_active("P1", index) ? "#d5b15a" : root.p1Accent
                                            }

                                            Column {
                                                id: slateP1
                                                anchors.left: parent.left
                                                anchors.right: parent.right
                                                anchors.top: parent.top
                                                anchors.margins: root.spacingSm
                                                spacing: 0
                                                width: parent.width - 2 * root.spacingSm

                                                RowLayout {
                                                    width: parent.width
                                                    spacing: root.spacingSm
                                                    Image {
                                                        Layout.alignment: Qt.AlignTop
                                                        source: controller.unit_icon_source(model.display)
                                                        width: root.unitIconSize
                                                        height: root.unitIconSize
                                                        fillMode: Image.PreserveAspectFit
                                                        smooth: true
                                                        visible: source !== ""
                                                    }
                                                    ColumnLayout {
                                                        Layout.fillWidth: true
                                                        spacing: Math.round(2 * root.uiScale)
                                                        RowLayout {
                                                            spacing: root.rosterSlateGridStep
                                                            Text {
                                                                Layout.fillWidth: true
                                                                text: controller.roster_entry_display_name("P1", index)
                                                                color: "#f2f6fc"
                                                                elide: Text.ElideRight
                                                                font.bold: true
                                                                font.family: root.fontUiFamily
                                                                font.pixelSize: Math.round(12 * root.uiScale)
                                                                font.capitalization: Font.AllUppercase
                                                            }
                                                            Text {
                                                                text: controller.roster_entry_count_label("P1", index)
                                                                color: "#6b8aab"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(9 * root.uiScale)
                                                            }
                                                        }
                                                        Rectangle {
                                                            Layout.fillWidth: true
                                                            height: 1
                                                            color: root.rosterTitleUnderline
                                                        }
                                                    }
                                                    Item { Layout.fillWidth: true }
                                                    Rectangle {
                                                        Layout.alignment: Qt.AlignTop
                                                        color: "#2a2210"
                                                        border.width: 1
                                                        border.color: "#c79a32"
                                                        radius: 0
                                                        implicitWidth: ptsP1Badge.implicitWidth + Math.round(20 * root.uiScale)
                                                        implicitHeight: ptsP1Badge.implicitHeight + Math.round(8 * root.uiScale)
                                                        Text {
                                                            id: ptsP1Badge
                                                            anchors.centerIn: parent
                                                            text: controller.roster_entry_pts_badge("P1", index)
                                                            color: "#f0e6c8"
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.bold: true
                                                            font.capitalization: Font.AllUppercase
                                                            horizontalAlignment: Text.AlignHCenter
                                                            verticalAlignment: Text.AlignVCenter
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Rectangle {
                                                    width: parent.width
                                                    color: root.rosterSlateInstrumentBg
                                                    implicitHeight: coreColP1.implicitHeight + 2 * root.rosterSlateGridStep
                                                    Column {
                                                        id: coreColP1
                                                        anchors.left: parent.left
                                                        anchors.right: parent.right
                                                        anchors.top: parent.top
                                                        anchors.margins: root.rosterSlateGridStep
                                                        spacing: Math.round(3 * root.uiScale)
                                                        Row {
                                                            spacing: 0
                                                            Repeater {
                                                                model: root.rosterCoreStatHdrs.length
                                                                Item {
                                                                    width: root.rosterCoreStatColWidths[index]
                                                                    implicitHeight: hdrCellP1.implicitHeight
                                                                    Text {
                                                                        id: hdrCellP1
                                                                        anchors.horizontalCenter: parent.horizontalCenter
                                                                        width: parent.width
                                                                        horizontalAlignment: Text.AlignHCenter
                                                                        text: root.rosterCoreStatHdrs[index]
                                                                        color: "#7a8a9e"
                                                                        font.weight: Font.Normal
                                                                        font.family: root.fontDataFamily
                                                                        font.pixelSize: Math.round(7 * root.uiScale)
                                                                        font.letterSpacing: 0.6
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        Row {
                                                            spacing: 0
                                                            Repeater {
                                                                model: controller.roster_entry_core_stat_values("P1", index)
                                                                Item {
                                                                    width: root.rosterCoreStatColWidths[index]
                                                                    implicitHeight: valCellP1.implicitHeight
                                                                    Text {
                                                                        id: valCellP1
                                                                        anchors.horizontalCenter: parent.horizontalCenter
                                                                        width: parent.width
                                                                        horizontalAlignment: Text.AlignHCenter
                                                                        text: modelData
                                                                        color: root.uiTextMain
                                                                        font.weight: Font.DemiBold
                                                                        font.family: root.fontDataFamily
                                                                        font.pixelSize: Math.round(10 * root.uiScale)
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Flow {
                                                    width: parent.width
                                                    spacing: root.rosterSlateGridStep
                                                    Repeater {
                                                        model: controller.roster_entry_keyword_tags("P1", index)
                                                        delegate: Rectangle {
                                                            color: kwP1Hover.hovered ? Qt.rgba(1, 1, 1, 0.08) : Qt.rgba(1, 1, 1, 0.05)
                                                            border.width: 1
                                                            border.color: kwP1Hover.hovered ? "#5e7494" : "#4a5c72"
                                                            radius: 0
                                                            implicitWidth: kwP1Chip.implicitWidth + Math.round(12 * root.uiScale)
                                                            implicitHeight: kwP1Chip.implicitHeight + Math.round(4 * root.uiScale)
                                                            Behavior on color { ColorAnimation { duration: 100 } }
                                                            Behavior on border.color { ColorAnimation { duration: 100 } }
                                                            HoverHandler {
                                                                id: kwP1Hover
                                                            }
                                                            ToolTip.visible: kwP1Hover.hovered
                                                            ToolTip.delay: 400
                                                            ToolTip.text: modelData
                                                            Text {
                                                                id: kwP1Chip
                                                                anchors.centerIn: parent
                                                                text: modelData
                                                                color: "#b8c8dc"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Column {
                                                    width: slateP1.width
                                                    spacing: Math.round(6 * root.uiScale)
                                                    Repeater {
                                                        model: controller.roster_entry_ability_lines("P1", index)
                                                        delegate: Text {
                                                            width: slateP1.width
                                                            wrapMode: Text.WordWrap
                                                            text: ">_ " + modelData
                                                            color: "#d5b15a"
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(9 * root.uiScale)
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Column {
                                                    width: parent.width
                                                    spacing: Math.round(8 * root.uiScale)
                                                    RowLayout {
                                                        width: parent.width
                                                        spacing: root.spacingXs
                                                        Item {
                                                            Layout.preferredWidth: Math.round(16 * root.uiScale)
                                                            Layout.fillHeight: true
                                                            Text {
                                                                anchors.verticalCenter: parent.verticalCenter
                                                                anchors.horizontalCenter: parent.horizontalCenter
                                                                text: "⌖"
                                                                color: root.uiTextMuted
                                                                font.pixelSize: Math.round(11 * root.uiScale)
                                                            }
                                                        }
                                                        Text {
                                                            Layout.fillWidth: true
                                                            Layout.alignment: Qt.AlignVCenter
                                                            text: controller.roster_entry_ranged_weapon("P1", index)
                                                            color: root.uiTextMain
                                                            wrapMode: Text.WordWrap
                                                            maximumLineCount: 2
                                                            elide: Text.ElideRight
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(9 * root.uiScale)
                                                        }
                                                    }
                                                    RowLayout {
                                                        width: parent.width
                                                        spacing: root.spacingXs
                                                        Item {
                                                            Layout.preferredWidth: Math.round(16 * root.uiScale)
                                                            Layout.fillHeight: true
                                                            Text {
                                                                anchors.verticalCenter: parent.verticalCenter
                                                                anchors.horizontalCenter: parent.horizontalCenter
                                                                text: "⚔"
                                                                color: root.uiTextMuted
                                                                font.pixelSize: Math.round(11 * root.uiScale)
                                                            }
                                                        }
                                                        Text {
                                                            Layout.fillWidth: true
                                                            Layout.alignment: Qt.AlignVCenter
                                                            text: controller.roster_entry_melee_weapon("P1", index)
                                                            color: "#c5d0de"
                                                            wrapMode: Text.WordWrap
                                                            maximumLineCount: 2
                                                            elide: Text.ElideRight
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(9 * root.uiScale)
                                                        }
                                                    }
                                                }
                                            }

                                            Canvas {
                                                z: 2
                                                anchors.top: parent.top
                                                anchors.right: parent.right
                                                width: Math.round(14 * root.uiScale)
                                                height: Math.round(14 * root.uiScale)
                                                onPaint: {
                                                    var ctx = getContext("2d")
                                                    ctx.reset()
                                                    ctx.beginPath()
                                                    ctx.moveTo(0, 0)
                                                    ctx.lineTo(width, 0)
                                                    ctx.lineTo(width, height)
                                                    ctx.closePath()
                                                    ctx.fillStyle = root.bgBase
                                                    ctx.fill()
                                                    ctx.strokeStyle = parent.border.color
                                                    ctx.lineWidth = 1
                                                    ctx.beginPath()
                                                    ctx.moveTo(0, 0)
                                                    ctx.lineTo(width, height)
                                                    ctx.stroke()
                                                }
                                            }

                                            MouseArea {
                                                z: 3
                                                anchors.fill: parent
                                                onClicked: playerRosterView.currentIndex = index
                                            }
                                        }

                                        Rectangle {
                                            id: selGlowP1
                                            visible: isCurrent
                                            z: -1
                                            anchors.centerIn: cardP1
                                            width: cardP1.width + 6
                                            height: cardP1.height + 6
                                            color: "transparent"
                                            border.width: 1
                                            border.color: Qt.rgba(0.42, 0.58, 0.88, 0.55)
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Layout.topMargin: Math.round(12 * root.uiScale)
                                    spacing: root.spacingSm
                                    Button {
                                        text: "[X] УДАЛИТЬ"
                                        enabled: playerRosterView.currentIndex >= 0
                                        onClicked: controller.remove_player_unit(playerRosterView.currentIndex)
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.enabled ? "#d2dbea" : "#6f7a8a"
                                            font.family: "JetBrains Mono"
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: Rectangle {
                                            radius: 0
                                            color: parent.down ? "#1f2632" : "#141b26"
                                            border.width: 1
                                            border.color: parent.hovered ? "#8fb6e8" : "#44536a"
                                        }
                                    }
                                    Button {
                                        text: "[!] ОЧИСТИТЬ РОСТЕР"
                                        onClicked: controller.clear_player_roster()
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.hovered ? "#f0d7d7" : "#d8b0b0"
                                            font.family: "JetBrains Mono"
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: Rectangle {
                                            radius: 0
                                            color: parent.down ? "#2b1d1d" : "#1a1518"
                                            border.width: 1
                                            border.color: parent.hovered ? "#c56e6e" : "#704848"
                                        }
                                    }
                                }

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    Layout.minimumHeight: 0
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
                                    Layout.fillHeight: false
                                    Layout.preferredHeight: Math.min(contentHeight, Math.round(430 * root.uiScale))
                                    Layout.minimumHeight: 0
                                    model: controller.modelRosterModel
                                    clip: true
                                    add: Transition {
                                        NumberAnimation { property: "opacity"; from: 0; to: 1; duration: 100; easing.type: Easing.OutQuad }
                                    }
                                    remove: Transition {
                                        NumberAnimation { property: "opacity"; from: 1; to: 0; duration: 90; easing.type: Easing.InQuad }
                                    }
                                    displaced: Transition {
                                        NumberAnimation { properties: "x,y"; duration: 100; easing.type: Easing.OutQuad }
                                    }
                                    // Data Slate P2 — синхронизировать с блоком P1 выше (keep in sync)
                                    delegate: Item {
                                        width: ListView.view ? ListView.view.width : 0
                                        implicitHeight: cardP2.implicitHeight
                                        height: implicitHeight

                                        readonly property bool isCurrent: ListView.view ? (ListView.view.currentIndex === index) : false

                                        Rectangle {
                                            id: cardP2
                                            z: 1
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            width: parent.width
                                            implicitHeight: Math.max(Math.round(124 * root.uiScale), slateP2.implicitHeight + 2 * root.spacingSm)
                                            height: implicitHeight
                                            clip: true
                                            color: controller.roster_entry_active("P2", index) ? "#3a2323" : "#141b26"
                                            border.width: isCurrent ? 2 : 1
                                            border.color: controller.roster_entry_active("P2", index) ? "#d5b15a" : "#a44848"
                                            radius: 0
                                            Behavior on color { ColorAnimation { duration: 100 } }
                                            Behavior on border.color { ColorAnimation { duration: 100 } }
                                            Behavior on border.width { NumberAnimation { duration: 100 } }

                                            Rectangle {
                                                anchors.left: parent.left
                                                anchors.top: parent.top
                                                width: Math.max(1, Math.round(1 * root.uiScale))
                                                height: parent.height
                                                color: controller.roster_entry_active("P2", index) ? "#d5b15a" : "#a44848"
                                            }

                                            Column {
                                                id: slateP2
                                                anchors.left: parent.left
                                                anchors.right: parent.right
                                                anchors.top: parent.top
                                                anchors.margins: root.spacingSm
                                                spacing: 0
                                                width: parent.width - 2 * root.spacingSm

                                                RowLayout {
                                                    width: parent.width
                                                    spacing: root.spacingSm
                                                    Image {
                                                        Layout.alignment: Qt.AlignTop
                                                        source: controller.unit_icon_source(model.display)
                                                        width: root.unitIconSize
                                                        height: root.unitIconSize
                                                        fillMode: Image.PreserveAspectFit
                                                        smooth: true
                                                        visible: source !== ""
                                                    }
                                                    ColumnLayout {
                                                        Layout.fillWidth: true
                                                        spacing: Math.round(2 * root.uiScale)
                                                        RowLayout {
                                                            spacing: root.rosterSlateGridStep
                                                            Text {
                                                                Layout.fillWidth: true
                                                                text: controller.roster_entry_display_name("P2", index)
                                                                color: "#f2f6fc"
                                                                elide: Text.ElideRight
                                                                font.bold: true
                                                                font.family: root.fontUiFamily
                                                                font.pixelSize: Math.round(12 * root.uiScale)
                                                                font.capitalization: Font.AllUppercase
                                                            }
                                                            Text {
                                                                text: controller.roster_entry_count_label("P2", index)
                                                                color: "#a87878"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(9 * root.uiScale)
                                                            }
                                                        }
                                                        Rectangle {
                                                            Layout.fillWidth: true
                                                            height: 1
                                                            color: root.rosterTitleUnderline
                                                        }
                                                    }
                                                    Item { Layout.fillWidth: true }
                                                    Rectangle {
                                                        Layout.alignment: Qt.AlignTop
                                                        color: "#2a2210"
                                                        border.width: 1
                                                        border.color: "#c79a32"
                                                        radius: 0
                                                        implicitWidth: ptsP2Badge.implicitWidth + Math.round(20 * root.uiScale)
                                                        implicitHeight: ptsP2Badge.implicitHeight + Math.round(8 * root.uiScale)
                                                        Text {
                                                            id: ptsP2Badge
                                                            anchors.centerIn: parent
                                                            text: controller.roster_entry_pts_badge("P2", index)
                                                            color: "#f0e6c8"
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(10 * root.uiScale)
                                                            font.bold: true
                                                            font.capitalization: Font.AllUppercase
                                                            horizontalAlignment: Text.AlignHCenter
                                                            verticalAlignment: Text.AlignVCenter
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Rectangle {
                                                    width: parent.width
                                                    color: root.rosterSlateInstrumentBg
                                                    implicitHeight: coreColP2.implicitHeight + 2 * root.rosterSlateGridStep
                                                    Column {
                                                        id: coreColP2
                                                        anchors.left: parent.left
                                                        anchors.right: parent.right
                                                        anchors.top: parent.top
                                                        anchors.margins: root.rosterSlateGridStep
                                                        spacing: Math.round(3 * root.uiScale)
                                                        Row {
                                                            spacing: 0
                                                            Repeater {
                                                                model: root.rosterCoreStatHdrs.length
                                                                Item {
                                                                    width: root.rosterCoreStatColWidths[index]
                                                                    implicitHeight: hdrCellP2.implicitHeight
                                                                    Text {
                                                                        id: hdrCellP2
                                                                        anchors.horizontalCenter: parent.horizontalCenter
                                                                        width: parent.width
                                                                        horizontalAlignment: Text.AlignHCenter
                                                                        text: root.rosterCoreStatHdrs[index]
                                                                        color: "#7a8a9e"
                                                                        font.weight: Font.Normal
                                                                        font.family: root.fontDataFamily
                                                                        font.pixelSize: Math.round(7 * root.uiScale)
                                                                        font.letterSpacing: 0.6
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        Row {
                                                            spacing: 0
                                                            Repeater {
                                                                model: controller.roster_entry_core_stat_values("P2", index)
                                                                Item {
                                                                    width: root.rosterCoreStatColWidths[index]
                                                                    implicitHeight: valCellP2.implicitHeight
                                                                    Text {
                                                                        id: valCellP2
                                                                        anchors.horizontalCenter: parent.horizontalCenter
                                                                        width: parent.width
                                                                        horizontalAlignment: Text.AlignHCenter
                                                                        text: modelData
                                                                        color: root.uiTextMain
                                                                        font.weight: Font.DemiBold
                                                                        font.family: root.fontDataFamily
                                                                        font.pixelSize: Math.round(10 * root.uiScale)
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Flow {
                                                    width: parent.width
                                                    spacing: root.rosterSlateGridStep
                                                    Repeater {
                                                        model: controller.roster_entry_keyword_tags("P2", index)
                                                        delegate: Rectangle {
                                                            color: kwP2Hover.hovered ? Qt.rgba(1, 1, 1, 0.08) : Qt.rgba(1, 1, 1, 0.05)
                                                            border.width: 1
                                                            border.color: kwP2Hover.hovered ? "#937070" : "#6a4a52"
                                                            radius: 0
                                                            implicitWidth: kwP2Chip.implicitWidth + Math.round(12 * root.uiScale)
                                                            implicitHeight: kwP2Chip.implicitHeight + Math.round(4 * root.uiScale)
                                                            Behavior on color { ColorAnimation { duration: 100 } }
                                                            Behavior on border.color { ColorAnimation { duration: 100 } }
                                                            HoverHandler {
                                                                id: kwP2Hover
                                                            }
                                                            ToolTip.visible: kwP2Hover.hovered
                                                            ToolTip.delay: 400
                                                            ToolTip.text: modelData
                                                            Text {
                                                                id: kwP2Chip
                                                                anchors.centerIn: parent
                                                                text: modelData
                                                                color: "#e8c4c0"
                                                                font.family: root.fontDataFamily
                                                                font.pixelSize: Math.round(8 * root.uiScale)
                                                            }
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Column {
                                                    width: slateP2.width
                                                    spacing: Math.round(6 * root.uiScale)
                                                    Repeater {
                                                        model: controller.roster_entry_ability_lines("P2", index)
                                                        delegate: Text {
                                                            width: slateP2.width
                                                            wrapMode: Text.WordWrap
                                                            text: ">_ " + modelData
                                                            color: "#d5b15a"
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(9 * root.uiScale)
                                                        }
                                                    }
                                                }

                                                Item {
                                                    width: parent.width
                                                    height: root.rosterSlateSectionGap
                                                }

                                                Column {
                                                    width: parent.width
                                                    spacing: Math.round(8 * root.uiScale)
                                                    RowLayout {
                                                        width: parent.width
                                                        spacing: root.spacingXs
                                                        Item {
                                                            Layout.preferredWidth: Math.round(16 * root.uiScale)
                                                            Layout.fillHeight: true
                                                            Text {
                                                                anchors.verticalCenter: parent.verticalCenter
                                                                anchors.horizontalCenter: parent.horizontalCenter
                                                                text: "⌖"
                                                                color: root.uiTextMuted
                                                                font.pixelSize: Math.round(11 * root.uiScale)
                                                            }
                                                        }
                                                        Text {
                                                            Layout.fillWidth: true
                                                            Layout.alignment: Qt.AlignVCenter
                                                            text: controller.roster_entry_ranged_weapon("P2", index)
                                                            color: root.uiTextMain
                                                            wrapMode: Text.WordWrap
                                                            maximumLineCount: 2
                                                            elide: Text.ElideRight
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(9 * root.uiScale)
                                                        }
                                                    }
                                                    RowLayout {
                                                        width: parent.width
                                                        spacing: root.spacingXs
                                                        Item {
                                                            Layout.preferredWidth: Math.round(16 * root.uiScale)
                                                            Layout.fillHeight: true
                                                            Text {
                                                                anchors.verticalCenter: parent.verticalCenter
                                                                anchors.horizontalCenter: parent.horizontalCenter
                                                                text: "⚔"
                                                                color: root.uiTextMuted
                                                                font.pixelSize: Math.round(11 * root.uiScale)
                                                            }
                                                        }
                                                        Text {
                                                            Layout.fillWidth: true
                                                            Layout.alignment: Qt.AlignVCenter
                                                            text: controller.roster_entry_melee_weapon("P2", index)
                                                            color: "#c5d0de"
                                                            wrapMode: Text.WordWrap
                                                            maximumLineCount: 2
                                                            elide: Text.ElideRight
                                                            font.family: root.fontDataFamily
                                                            font.pixelSize: Math.round(9 * root.uiScale)
                                                        }
                                                    }
                                                }
                                            }

                                            Canvas {
                                                z: 2
                                                anchors.top: parent.top
                                                anchors.right: parent.right
                                                width: Math.round(14 * root.uiScale)
                                                height: Math.round(14 * root.uiScale)
                                                onPaint: {
                                                    var ctx = getContext("2d")
                                                    ctx.reset()
                                                    ctx.beginPath()
                                                    ctx.moveTo(0, 0)
                                                    ctx.lineTo(width, 0)
                                                    ctx.lineTo(width, height)
                                                    ctx.closePath()
                                                    ctx.fillStyle = root.bgBase
                                                    ctx.fill()
                                                    ctx.strokeStyle = parent.border.color
                                                    ctx.lineWidth = 1
                                                    ctx.beginPath()
                                                    ctx.moveTo(0, 0)
                                                    ctx.lineTo(width, height)
                                                    ctx.stroke()
                                                }
                                            }

                                            MouseArea {
                                                z: 3
                                                anchors.fill: parent
                                                onClicked: modelRosterView.currentIndex = index
                                            }
                                        }

                                        Rectangle {
                                            id: selGlowP2
                                            visible: isCurrent
                                            z: -1
                                            anchors.centerIn: cardP2
                                            width: cardP2.width + 6
                                            height: cardP2.height + 6
                                            color: "transparent"
                                            border.width: 1
                                            border.color: Qt.rgba(0.92, 0.48, 0.48, 0.55)
                                        }
                                    }
                                }

                                RowLayout {
                                    Layout.fillWidth: true
                                    Layout.topMargin: Math.round(12 * root.uiScale)
                                    spacing: root.spacingSm
                                    Button {
                                        text: "[X] УДАЛИТЬ"
                                        enabled: modelRosterView.currentIndex >= 0
                                        onClicked: controller.remove_model_unit(modelRosterView.currentIndex)
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.enabled ? "#d2dbea" : "#6f7a8a"
                                            font.family: "JetBrains Mono"
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: Rectangle {
                                            radius: 0
                                            color: parent.down ? "#1f2632" : "#141b26"
                                            border.width: 1
                                            border.color: parent.hovered ? "#8fb6e8" : "#44536a"
                                        }
                                    }
                                    Button {
                                        text: "[!] ОЧИСТИТЬ РОСТЕР"
                                        onClicked: controller.clear_model_roster()
                                        contentItem: Text {
                                            text: parent.text
                                            color: parent.hovered ? "#f0d7d7" : "#d8b0b0"
                                            font.family: "JetBrains Mono"
                                            font.pixelSize: Math.round(10 * root.uiScale)
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        background: Rectangle {
                                            radius: 0
                                            color: parent.down ? "#2b1d1d" : "#1a1518"
                                            border.width: 1
                                            border.color: parent.hovered ? "#c56e6e" : "#704848"
                                        }
                                    }
                                }

                                Item {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    Layout.minimumHeight: 0
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

                        // Шапка: одна строка — заголовок + чипы модели + действия.
                        RowLayout {
                            width: parent.width
                            spacing: root.spacingMd

                            Text {
                                text: "Метрики модели"
                                font.pixelSize: Math.round(20 * root.uiScale)
                                font.bold: true
                                color: root.uiTextMain
                            }

                            // Иконка-подсказка ⓘ с описанием вкладки (текст не теряем).
                            Rectangle {
                                Layout.alignment: Qt.AlignVCenter
                                implicitWidth: Math.round(18 * root.uiScale)
                                implicitHeight: Math.round(18 * root.uiScale)
                                radius: width / 2
                                color: helpHover.hovered ? Qt.rgba(1, 1, 1, 0.06) : "transparent"
                                border.width: 1
                                border.color: helpHover.hovered ? root.uiTextMain : root.uiTextMuted

                                Text {
                                    anchors.centerIn: parent
                                    text: "i"
                                    font.bold: true
                                    font.italic: true
                                    font.pixelSize: Math.round(11 * root.uiScale)
                                    color: parent.border.color
                                }
                                HoverHandler { id: helpHover }
                                ToolTip.visible: helpHover.hovered
                                ToolTip.text: "Метрики тренировки: каждая точка — окно реальных тренировочных эпизодов (DET-прогоны удалены). Честное сравнение моделей — вкладка «Оценка»."
                            }

                            Item { Layout.fillWidth: true }

                            Label {
                                text: controller.metricsLabel
                                color: root.uiTextMuted
                                elide: Label.ElideLeft
                                Layout.maximumWidth: Math.round(260 * root.uiScale)
                            }
                            Button {
                                text: "Выбрать модель"
                                onClicked: metricsFileDialog.open()
                            }
                            Button {
                                text: "Последняя"
                                onClicked: controller.select_latest_metrics()
                            }
                        }

                        // Карточки «Модель» и «Оппонент» — на видном месте, сразу под шапкой.
                        RowLayout {
                            width: parent.width
                            spacing: root.spacingMd

                            // Карточка модели.
                            Item {
                                Layout.fillWidth: true
                                implicitHeight: Math.round(104 * root.uiScale)

                                ChamferPanel {
                                    anchors.fill: parent
                                    cutSize: Math.round(8 * root.uiScale)
                                    contentMargin: 0
                                    fillColor: root.bgElevated
                                    borderWidth: 1
                                    borderColor: root.borderMuted
                                }
                                Rectangle {
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.bottom: parent.bottom
                                    anchors.margins: Math.round(8 * root.uiScale)
                                    width: Math.round(3 * root.uiScale)
                                    radius: width / 2
                                    color: root.accentP1
                                }
                                Column {
                                    anchors.fill: parent
                                    anchors.leftMargin: Math.round(18 * root.uiScale)
                                    anchors.rightMargin: Math.round(12 * root.uiScale)
                                    anchors.topMargin: Math.round(10 * root.uiScale)
                                    anchors.bottomMargin: Math.round(10 * root.uiScale)
                                    spacing: Math.round(3 * root.uiScale)

                                    Text { text: "МОДЕЛЬ"; font.bold: true; font.pixelSize: Math.max(8, root.evalCaptionSize - 1); color: root.uiTextMuted }
                                    Text { text: "Алгоритм: " + controller.metricsAlgo; color: root.uiTextMain; font.bold: true }
                                    Text { text: "Режим: " + controller.metricsMode; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                                    Text {
                                        width: parent.width
                                        text: "Run ID: " + controller.metricsRunId
                                        color: root.uiTextMuted
                                        font.pixelSize: root.evalCaptionSize
                                        elide: Text.ElideRight
                                    }
                                }
                            }

                            // Карточка оппонента.
                            Item {
                                Layout.fillWidth: true
                                implicitHeight: Math.round(104 * root.uiScale)

                                ChamferPanel {
                                    anchors.fill: parent
                                    cutSize: Math.round(8 * root.uiScale)
                                    contentMargin: 0
                                    fillColor: root.bgElevated
                                    borderWidth: 1
                                    borderColor: root.borderMuted
                                }
                                Rectangle {
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.bottom: parent.bottom
                                    anchors.margins: Math.round(8 * root.uiScale)
                                    width: Math.round(3 * root.uiScale)
                                    radius: width / 2
                                    color: "#b88a26"
                                }
                                Column {
                                    anchors.fill: parent
                                    anchors.leftMargin: Math.round(18 * root.uiScale)
                                    anchors.rightMargin: Math.round(12 * root.uiScale)
                                    anchors.topMargin: Math.round(10 * root.uiScale)
                                    anchors.bottomMargin: Math.round(10 * root.uiScale)
                                    spacing: Math.round(3 * root.uiScale)

                                    Text { text: "ОППОНЕНТ"; font.bold: true; font.pixelSize: Math.max(8, root.evalCaptionSize - 1); color: root.uiTextMuted }
                                    Text { text: "Self-play: " + (controller.selfPlayEnabled ? "включён" : "выключен"); color: root.uiTextMain; font.bold: true }
                                    Text { text: "Источник: " + controller.opponentSource; color: root.uiTextMuted; font.pixelSize: root.evalCaptionSize }
                                    Text {
                                        width: parent.width
                                        text: "Алгоритм: " + controller.opponentAlgo + (controller.opponentId.length > 0 ? (" (id=" + controller.opponentId + ")") : "")
                                        color: root.uiTextMuted
                                        font.pixelSize: root.evalCaptionSize
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }

                        // --- Дашборд метрик тренировки: живые графики по окнам эпизодов ---
                        ColumnLayout {
                            id: metricsDash
                            width: parent.width
                            spacing: root.spacingMd

                            property var detData: ({ count: 0, episodes: [], series: {}, loss: { episodes: [], values: [] }, endReasons: {} })
                            function reloadDet() { detData = controller.detSeries() }
                            function _xsFor(spec) {
                                if (spec.src === "loss")
                                    return (detData.loss && detData.loss.episodes) ? detData.loss.episodes : []
                                return detData.episodes || []
                            }
                            function _seriesFor(spec) {
                                var out = []
                                for (var i = 0; i < spec.lines.length; i++) {
                                    var ln = spec.lines[i]
                                    var ys = []
                                    if (spec.src === "loss")
                                        ys = (detData.loss && detData.loss.values) ? detData.loss.values : []
                                    else if (spec.src === "end")
                                        ys = (detData.endReasons && detData.endReasons[ln.key]) ? detData.endReasons[ln.key] : []
                                    else
                                        ys = (detData.series && detData.series[ln.key]) ? detData.series[ln.key] : []
                                    out.push({ name: ln.name, color: ln.color, ys: ys })
                                }
                                return out
                            }

                            property var mainSpecs: [
                                { title: "Winrate", fmt: "pct", src: "series", lines: [{ key: "win_rate", name: "win", color: root.accentPrimaryAction }] },
                                { title: "Средняя награда", fmt: "num", src: "series", lines: [{ key: "reward_mean", name: "reward", color: root.accentP1 }] }
                            ]
                            property var restSpecs: [
                                { title: "Loss обучения", fmt: "num", src: "loss", lines: [{ key: "values", name: "loss", color: "#3fb950" }] },
                                { title: "Длина эпизода", fmt: "int", src: "series", lines: [{ key: "ep_len_mean", name: "ep_len", color: "#9b8cff" }] },
                                { title: "Avg VP (model vs enemy)", fmt: "num", src: "series", lines: [{ key: "model_vp_mean", name: "model", color: root.accentP1 }, { key: "enemy_vp_mean", name: "enemy", color: root.accentP2 }] },
                                { title: "HP diff", fmt: "num", src: "series", lines: [{ key: "hp_diff_mean", name: "hp_diff", color: root.accentP2 }] },
                                { title: "Kill diff", fmt: "num", src: "series", lines: [{ key: "kill_diff_mean", name: "kill_diff", color: root.accentPrimaryAction }] },
                                { title: "Причины завершения", fmt: "pct", src: "end", lines: [{ key: "wipeout_enemy_rate", name: "wipe enemy", color: root.accentP1 }, { key: "wipeout_model_rate", name: "wipe model", color: root.accentP2 }, { key: "turn_limit_rate", name: "turn limit", color: root.accentGhost }] }
                            ]

                            Connections {
                                target: controller
                                function onMetricsSummaryChanged() { metricsDash.reloadDet() }
                            }
                            Component.onCompleted: metricsDash.reloadDet()

                            // KPI-плитки: главное одним взглядом.
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingMd

                                Repeater {
                                    model: [
                                        { label: "WINRATE (ОКНО)", value: controller.detWinrateLast, accent: root.accentPrimaryAction },
                                        { label: "REWARD (ОКНО)", value: controller.detRewardLast, accent: root.accentP1 },
                                        { label: "ДЛИНА ЭПИЗОДА", value: controller.detEpLenLast, accent: "#9b8cff" },
                                        { label: "ЭПИЗОД-ЯКОРЬ", value: controller.detEpisodeLast, accent: root.accentGhost }
                                    ]
                                    delegate: Item {
                                        Layout.fillWidth: true
                                        implicitHeight: Math.round(64 * root.uiScale)

                                        ChamferPanel {
                                            anchors.fill: parent
                                            cutSize: Math.round(8 * root.uiScale)
                                            contentMargin: 0
                                            fillColor: root.bgElevated
                                            borderWidth: 1
                                            borderColor: root.borderMuted
                                        }
                                        Rectangle {
                                            anchors.left: parent.left
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            anchors.margins: Math.round(6 * root.uiScale)
                                            width: Math.round(3 * root.uiScale)
                                            radius: width / 2
                                            color: modelData.accent
                                        }
                                        ColumnLayout {
                                            anchors.fill: parent
                                            anchors.leftMargin: Math.round(16 * root.uiScale)
                                            anchors.rightMargin: Math.round(12 * root.uiScale)
                                            anchors.topMargin: Math.round(8 * root.uiScale)
                                            anchors.bottomMargin: Math.round(8 * root.uiScale)
                                            spacing: 0
                                            Text {
                                                text: modelData.label
                                                color: root.uiTextMuted
                                                font.pixelSize: Math.max(8, root.evalCaptionSize - 1)
                                                Layout.fillWidth: true
                                                elide: Text.ElideRight
                                            }
                                            Text {
                                                text: modelData.value
                                                color: root.uiTextMain
                                                font.bold: true
                                                font.pixelSize: root.evalSectionTitleSize + Math.round(3 * root.uiScale)
                                                Layout.fillWidth: true
                                                elide: Text.ElideRight
                                            }
                                        }
                                    }
                                }
                            }

                            // Панель действий: заголовок + переход в TensorBoard.
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: root.spacingMd

                                Text {
                                    text: "Главные кривые (окна эпизодов)"
                                    color: root.uiTextMain
                                    font.bold: true
                                    font.pixelSize: root.evalSectionTitleSize
                                    Layout.fillWidth: true
                                }
                                Button {
                                    text: "ОТКРЫТЬ В TENSORBOARD"
                                    onClicked: tbWindow.openTensorboard()
                                    Layout.preferredWidth: Math.round(210 * root.uiScale)
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

                            // Пустое состояние (нет DET-eval данных).
                            Item {
                                Layout.fillWidth: true
                                implicitHeight: Math.round(160 * root.uiScale)
                                visible: (metricsDash.detData.count || 0) === 0

                                ChamferPanel {
                                    anchors.fill: parent
                                    cutSize: Math.round(8 * root.uiScale)
                                    contentMargin: 0
                                    fillColor: root.bgElevated
                                    borderWidth: 1
                                    borderColor: root.borderMuted
                                }
                                ColumnLayout {
                                    anchors.centerIn: parent
                                    spacing: root.spacingSm
                                    Text {
                                        text: "Нет данных метрик"
                                        color: root.uiTextMain
                                        font.bold: true
                                        font.pixelSize: root.evalSectionTitleSize
                                        Layout.alignment: Qt.AlignHCenter
                                    }
                                    Text {
                                        text: "Запусти обучение — графики появятся после первого окна эпизодов."
                                        color: root.uiTextMuted
                                        font.pixelSize: root.evalCaptionSize
                                        Layout.alignment: Qt.AlignHCenter
                                    }
                                }
                            }

                            // Главные кривые: всегда крупно, 2 колонки.
                            GridLayout {
                                Layout.fillWidth: true
                                columns: 2
                                columnSpacing: root.spacingMd
                                rowSpacing: root.spacingMd
                                visible: (metricsDash.detData.count || 0) > 0

                                Repeater {
                                    model: metricsDash.mainSpecs
                                    delegate: MetricChart {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(258 * root.uiScale)
                                        uiScale: root.uiScale
                                        captionSize: root.evalCaptionSize
                                        textMain: root.uiTextMain
                                        textMuted: root.uiTextMuted
                                        panelFill: root.bgElevated
                                        panelBorder: root.borderMuted
                                        gridColor: root.borderMuted
                                        title: modelData.title
                                        fmt: modelData.fmt
                                        accent: modelData.lines[0].color
                                        xs: metricsDash._xsFor(modelData)
                                        series: metricsDash._seriesFor(modelData)
                                    }
                                }
                            }

                            // Остальные метрики: свёрнуто по умолчанию.
                            ExpanderSection {
                                Layout.fillWidth: true
                                Layout.preferredHeight: implicitHeight
                                visible: (metricsDash.detData.count || 0) > 0
                                title: "Остальные метрики"
                                expanded: false
                                uiScale: root.uiScale
                                captionSize: root.evalCaptionSize
                                textMain: root.uiTextMain
                                textMuted: root.uiTextMuted
                                panelFill: root.bgElevated
                                panelBorder: root.borderMuted

                                GridLayout {
                                    width: parent.width
                                    columns: 2
                                    columnSpacing: root.spacingMd
                                    rowSpacing: root.spacingMd

                                    Repeater {
                                        model: metricsDash.restSpecs
                                        delegate: MetricChart {
                                            Layout.fillWidth: true
                                            Layout.preferredHeight: Math.round(258 * root.uiScale)
                                            uiScale: root.uiScale
                                            captionSize: root.evalCaptionSize
                                            textMain: root.uiTextMain
                                            textMuted: root.uiTextMuted
                                            panelFill: root.bgElevated
                                            panelBorder: root.borderMuted
                                            gridColor: root.borderMuted
                                            title: modelData.title
                                            fmt: modelData.fmt
                                            accent: modelData.lines[0].color
                                            xs: metricsDash._xsFor(modelData)
                                            series: metricsDash._seriesFor(modelData)
                                        }
                                    }
                                }
                            }

                        }

                        // Model Info убрали: эта информация уже есть в верхней панели и карточке "Оппонент".
                    }
                }
            }

            HeurMetricsPanel {
                Layout.fillWidth: true
                Layout.fillHeight: true
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

                                    Label {
                                        visible: controller.playInferenceSearchSimsVisible
                                        text: controller.playInferenceSearchSimsLabel
                                        color: root.uiTextMuted
                                        font.capitalization: Font.AllUppercase
                                        font.letterSpacing: 0.8
                                    }

                                    TextField {
                                        visible: controller.playInferenceSearchSimsVisible
                                        Layout.preferredWidth: Math.round(72 * root.uiScale)
                                        enabled: !controller.running
                                        text: controller.playInferenceSearchSims
                                        placeholderText: "32"
                                        font.family: root.fontDataFamily
                                        onEditingFinished: controller.set_play_inference_search_sims(text)
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
                                        text: root.inferenceSearchHelpText
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

                        TrainingDeviceBanner {
                            rootUi: root
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
                                    Layout.fillWidth: true
                                    spacing: root.spacingSm
                                    Switch {
                                        checked: controller.hyperparamsBasicMode
                                        onToggled: controller.set_hyperparams_basic_mode(checked)
                                    }
                                    Label {
                                        text: "Базовый режим (только ключевые поля)"
                                        color: root.uiTextMuted
                                        Layout.fillWidth: true
                                    }
                                }

                                TabBar {
                                    id: algoHyperparamsTabs
                                    Layout.fillWidth: true
                                    TabButton { text: "DQN" }
                                    TabButton { text: "PHOENIX" }
                                    TabButton { text: "PPO" }
                                    TabButton { text: "AlphaZero Tree" }
                                    TabButton { text: "AlphaZero Proxy" }
                                    TabButton { text: "Gumbel MuZero" }
                                    TabButton { text: "Sampled MuZero" }
                                    TabButton { text: "Gumbel AlphaZero" }
                                }

                                StackLayout {
                                    id: algoHyperparamsStack
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: Math.round(640 * root.uiScale)
                                    currentIndex: algoHyperparamsTabs.currentIndex

                                    ScrollView {
                                        clip: true
                                        contentWidth: dqnHyperparamsColumn.width
                                        ColumnLayout {
                                            id: dqnHyperparamsColumn
                                            width: algoHyperparamsStack.width
                                            spacing: root.spacingSm

                                            DqnDistributedActorsPanel {
                                                rootUi: root
                                            }

                                            SectionHyperparamsEditor {
                                                Layout.fillWidth: true
                                                algoSection: "dqn"
                                                rootUi: root
                                            }
                                        }
                                    }
                                    ScrollView {
                                        clip: true
                                        contentWidth: phoenixHyperparamsColumn.width
                                        ColumnLayout {
                                            id: phoenixHyperparamsColumn
                                            width: algoHyperparamsStack.width
                                            spacing: root.spacingSm

                                            PhoenixDistributedActorsPanel {
                                                rootUi: root
                                            }

                                            SectionHyperparamsEditor {
                                                Layout.fillWidth: true
                                                algoSection: "phoenix"
                                                rootUi: root
                                            }
                                        }
                                    }
                                    ScrollView {
                                        clip: true
                                        SectionHyperparamsEditor {
                                            width: algoHyperparamsStack.width
                                            algoSection: "ppo"
                                            rootUi: root
                                        }
                                    }
                                    ScrollView {
                                        clip: true
                                        contentWidth: azTreeHyperparamsColumn.width
                                        ColumnLayout {
                                            id: azTreeHyperparamsColumn
                                            width: algoHyperparamsStack.width
                                            spacing: root.spacingSm

                                            AzInferenceServerPanel {
                                                rootUi: root
                                            }

                                            SectionHyperparamsEditor {
                                                Layout.fillWidth: true
                                                algoSection: "tree"
                                                rootUi: root
                                            }
                                        }
                                    }
                                    ScrollView {
                                        clip: true
                                        SectionHyperparamsEditor {
                                            width: algoHyperparamsStack.width
                                            algoSection: "proxy"
                                            rootUi: root
                                        }
                                    }
                                    ScrollView {
                                        clip: true
                                        contentWidth: gmzHyperparamsColumn.width
                                        ColumnLayout {
                                            id: gmzHyperparamsColumn
                                            width: algoHyperparamsStack.width
                                            spacing: root.spacingSm

                                            GmzInferenceServerPanel {
                                                rootUi: root
                                            }

                                            SectionHyperparamsEditor {
                                                Layout.fillWidth: true
                                                algoSection: "gmz"
                                                rootUi: root
                                            }
                                        }
                                    }
                                    ScrollView {
                                        clip: true
                                        contentWidth: smzHyperparamsColumn.width
                                        ColumnLayout {
                                            id: smzHyperparamsColumn
                                            width: algoHyperparamsStack.width
                                            spacing: root.spacingSm

                                            SmzInferenceServerPanel {
                                                rootUi: root
                                            }

                                            SectionHyperparamsEditor {
                                                Layout.fillWidth: true
                                                algoSection: "smz"
                                                rootUi: root
                                            }
                                        }
                                    }
                                    ScrollView {
                                        clip: true
                                        contentWidth: gazHyperparamsColumn.width
                                        ColumnLayout {
                                            id: gazHyperparamsColumn
                                            width: algoHyperparamsStack.width
                                            spacing: root.spacingSm

                                            GazInferenceServerPanel {
                                                rootUi: root
                                            }

                                            SectionHyperparamsEditor {
                                                Layout.fillWidth: true
                                                algoSection: "gaz"
                                                rootUi: root
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
                                RowLayout {
                                    spacing: root.spacingXs
                                    Label {
                                        text: "Воркеры:"
                                        font.bold: true
                                    }
                                    TextField {
                                        id: evalWorkersField
                                        text: controller.evalWorkers.toString()
                                        validator: IntValidator { bottom: 1 }
                                        Layout.preferredWidth: Math.round(86 * root.uiScale)
                                        enabled: !controller.running
                                        font.family: root.fontDataFamily
                                        ToolTip.visible: hovered
                                        ToolTip.text: "1 = последовательный eval; >1 = параллельные процессы, выше нагрузка на CPU/GPU."
                                        background: Rectangle {
                                            radius: 0
                                            color: parent.enabled ? "#253244" : "#202734"
                                            border.width: 1
                                            border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                        }
                                        onEditingFinished: {
                                            var value = parseInt(text)
                                            if (!isNaN(value)) {
                                                controller.set_eval_workers(value)
                                                text = controller.evalWorkers.toString()
                                            } else {
                                                text = controller.evalWorkers.toString()
                                            }
                                        }
                                    }
                                }
                                TacticalCheckBox {
                                    text: "ДЕТАЛЬНЫЙ ЛОГ"
                                    scaleRef: root.uiScale
                                    labelFontFamily: root.fontUiFamily
                                    labelFontSize: root.evalCaptionSize
                                    labelColorEnabled: root.uiTextMain
                                    checked: controller.evalActionTrace
                                    enabled: !controller.running
                                    onToggled: controller.set_eval_action_trace(checked)
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
                                                    text: controller.evalP1InferenceTemperatureLabel
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
                                                Label {
                                                    text: controller.evalP1InferenceSearchSimsLabel
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.8
                                                    color: root.uiTextMuted
                                                    opacity: controller.evalP1InferenceSearchSimsVisible ? 1.0 : 0.55
                                                }
                                                TextField {
                                                    Layout.preferredWidth: Math.round(72 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP1InferenceSearchSimsVisible
                                                    opacity: controller.evalP1InferenceSearchSimsVisible ? 1.0 : 0.55
                                                    text: controller.evalP1InferenceSearchSims
                                                    placeholderText: "32"
                                                    font.family: root.fontDataFamily
                                                    background: Rectangle {
                                                        radius: 0
                                                        color: parent.enabled ? "#253244" : "#202734"
                                                        border.width: 1
                                                        border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                                    }
                                                    onEditingFinished: {
                                                        if (controller.evalP1InferenceSearchSimsVisible) {
                                                            controller.set_eval_p1_inference_search_sims(text)
                                                        }
                                                    }
                                                }
                                                Button {
                                                    text: "ⓘ"
                                                    flat: true
                                                    font.bold: true
                                                    ToolTip.visible: hovered
                                                    ToolTip.text: root.inferenceSearchHelpText
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
                                                    text: controller.evalP2InferenceTemperatureLabel
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
                                                Label {
                                                    text: controller.evalP2InferenceSearchSimsLabel
                                                    font.capitalization: Font.AllUppercase
                                                    font.letterSpacing: 0.8
                                                    color: root.uiTextMuted
                                                    opacity: controller.evalP2InferenceSearchSimsVisible ? 1.0 : 0.55
                                                }
                                                TextField {
                                                    Layout.preferredWidth: Math.round(72 * root.uiScale)
                                                    enabled: !controller.running && controller.evalP2InferenceSearchSimsVisible
                                                    opacity: controller.evalP2InferenceSearchSimsVisible ? 1.0 : 0.55
                                                    text: controller.evalP2InferenceSearchSims
                                                    placeholderText: "32"
                                                    font.family: root.fontDataFamily
                                                    background: Rectangle {
                                                        radius: 0
                                                        color: parent.enabled ? "#253244" : "#202734"
                                                        border.width: 1
                                                        border.color: parent.activeFocus ? "#b88a26" : "#3a475b"
                                                    }
                                                    onEditingFinished: {
                                                        if (controller.evalP2InferenceSearchSimsVisible) {
                                                            controller.set_eval_p2_inference_search_sims(text)
                                                        }
                                                    }
                                                }
                                                Button {
                                                    text: "ⓘ"
                                                    flat: true
                                                    font.bold: true
                                                    ToolTip.visible: hovered
                                                    ToolTip.text: root.inferenceSearchHelpText
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
                                    text: controller.evalMissionText
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

            LeaguePanel {
                Layout.fillWidth: true
                Layout.fillHeight: true
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
            text: "Вы действительно хотите удалить все сохранённые модели, метрики "
                + "(включая heur_decisions), игровой лог response.txt и служебные логи?"
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

    TrainingAlgoHelpDialog {
        id: trainingAlgoHelpDialog
        rootUi: root
        initialAlgo: controller.trainingAlgo
    }

    // TensorBoard: запускаем локальный сервер и открываем во внешнем браузере.
    // QtWebEngine намеренно не импортируем: Chromium на части Windows/GPU шумит
    // GLES/GPUInfo ошибками даже при выключенном GPU-рендере.
    Window {
        id: tbWindow
        title: "TensorBoard — 40kAI"
        width: 560
        height: 180
        color: "#0F172A"
        modality: Qt.NonModal

        property string pendingUrl: ""

        function openTensorboard() {
            pendingUrl = controller.start_tensorboard()
            if (pendingUrl.length > 0)
                Qt.openUrlExternally(pendingUrl)
            show()
            raise()
            requestActivate()
        }

        onClosing: controller.stop_tensorboard()

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            RowLayout {
                Layout.fillWidth: true
                Layout.margins: 8
                spacing: 8

                Button {
                    text: "Открыть в браузере"
                    onClicked: {
                        if (tbWindow.pendingUrl.length > 0)
                            Qt.openUrlExternally(tbWindow.pendingUrl)
                    }
                }
                Button {
                    text: "Остановить сервер"
                    onClicked: {
                        controller.stop_tensorboard()
                        tbWindow.close()
                    }
                }
                Text {
                    Layout.fillWidth: true
                    text: tbWindow.pendingUrl.length > 0
                          ? tbWindow.pendingUrl
                          : "TensorBoard ещё не запущен"
                    color: "#98a4b8"
                    elide: Text.ElideRight
                    verticalAlignment: Text.AlignVCenter
                }
            }

            Text {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.margins: 12
                text: "TensorBoard открыт во внешнем браузере. Это отключает QtWebEngine внутри GUI и убирает Chromium/GPUInfo сообщения в консоли."
                color: "#cbd5e1"
                font.pixelSize: Math.round(13 * root.uiScale)
                wrapMode: Text.WordWrap
            }
        }
    }

    Connections {
        target: controller
        function onLogLine(message) {
            trainLog.appendLine(message)
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
        function onEvalWorkersChanged(value) {
            if (typeof evalWorkersField !== "undefined" && evalWorkersField) {
                evalWorkersField.text = value.toString()
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
