import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

// Журнал тренировки: ListView + модель вместо TextArea.text += (тот тормозит на
// длинных тренировках). Каждая строка при приёме классифицируется по маркеру
// ([AZ]/[DQN]/[PPO]/[GMZ]/[TRAIN]/[LEAGUE]/[TRACE]), красится по группе,
// голый служебный «ep=N/M» (дубль для прогресс-бара) скрывается.
ColumnLayout {
    id: logView

    property real uiScale: 1.0
    property string fontDataFamily: "Consolas"
    property string fontUiFamily: "Segoe UI"
    property int maxLines: 4000

    // all | episodes | train | actors | dist | warn
    property string activeFilter: "all"
    property int lineCount: 0
    readonly property int visibleCount: logModel.count
    property int hiddenNewCount: 0

    spacing: Math.round(6 * uiScale)

    // Палитра групп: dist — цвет ПК2 (#3a6ea5-семейство), train — янтарь обучения.
    readonly property var groupColors: ({
        "ep": "#e1be68",
        "actor": "#5b8def",
        "env": "#3fbfb0",
        "train": "#e0a93c",
        "dist": "#6fa8dc",
        "gui": "#8b95a8",
        "other": "#9aa3b2",
        "warn": "#e6914d"
    })

    property var _allLines: []
    property bool _appending: false

    ListModel { id: logModel }

    function _esc(s) {
        return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    }

    function _classify(line) {
        var sev = "info"
        if (line.indexOf("[WARN]") >= 0 || line.indexOf("[ERROR]") >= 0
                || line.indexOf("[ERR]") >= 0 || line.indexOf("[FALLBACK]") >= 0
                || line.indexOf("[ALERT]") >= 0) {
            sev = "warn"
        }

        // Итоги эпизодов: единый [TRAIN][EP] (все алгоритмы). Старые [AZ] ep= — совместимость.
        if (/^\[TRAIN\]\[EP\]/.test(line) || /^\[AZ\] ep=\d+/.test(line)) {
            return { group: "ep", sev: sev, kind: "ep" }
        }

        // Детальные трейсы действий ([TRACE][EP]/[TRACE][ACTIONS]/[TRAIN][ACTIONS]) — к акторам.
        if (line.indexOf("[TRACE]") === 0 || line.indexOf("[TRAIN][ACTIONS]") === 0) {
            return { group: "actor", sev: sev, kind: "line" }
        }

        // Общий словарь всех алгоритмов: второй маркер решает группу.
        var m = line.match(/^\[(AZ|DQN|PPO|GMZ|TRAIN|LEAGUE)\](?:\[([A-Z_0-9]+)\])?/)
        if (m) {
            var sub = m[2] || ""
            var group = "train" // UPDATE/CHECKPOINT/WAIT/RESUME/HONEST_EVAL/CONFIG/SAVE/BEST/… и LEAGUE
            if (sub === "ACTOR")
                group = "actor"
            else if (sub === "ENV_WORKER")
                group = "env"
            else if (sub === "DIST" || sub === "REMOTE_CLIENT" || sub === "REMOTE_IS"
                     || sub === "INF_SERVER" || sub === "INF_CLIENT" || sub === "LOCAL_TRANSPORT")
                group = "dist"
            else if (sub === "EP")
                group = "ep" // [PPO][EP] — старт сбора эпизода, без разделителя
            return { group: group, sev: sev, kind: "line" }
        }

        if (line.indexOf("[GUI]") === 0 || line.indexOf("[EVAL]") === 0
                || line.indexOf("[VIEWER]") === 0) {
            return { group: "gui", sev: sev, kind: "line" }
        }
        return { group: "other", sev: sev, kind: "line" }
    }

    function _matches(entry) {
        if (entry.sev !== "info")
            return true // WARN/ERROR не прячем никаким фильтром
        switch (activeFilter) {
        case "all": return true
        case "episodes": return entry.group === "ep"
        case "train": return entry.group === "train" || entry.group === "ep"
        case "actors": return entry.group === "actor" || entry.group === "env"
        case "dist": return entry.group === "dist"
        case "warn": return false
        }
        return true
    }

    function _renderHtml(line, meta, ts) {
        var m = line.match(/^((?:\[[^\]\n]*\])+)\s?([\s\S]*)$/)
        var tag = m ? m[1] : ""
        var rest = m ? m[2] : line
        var tagColor = meta.sev === "warn" ? groupColors["warn"]
                                           : (groupColors[meta.group] || groupColors["other"])
        // key=value: ключ приглушённый, значение яркое; result= красим по исходу.
        var restHtml = _esc(rest).replace(/([A-Za-z_][\w.]*)=([^\s]+)/g, function (all, k, v) {
            var vc = "#e7edf5"
            if (k === "result")
                vc = v === "win" ? "#5ee86a" : (v === "loss" ? "#e85d5d" : "#9aa3b2")
            return '<font color="#7d8ba0">' + k + '=</font><font color="' + vc + '">' + v + '</font>'
        })
        return '<font color="#5c6a7d">' + ts + '</font> '
                + '<font color="' + tagColor + '"><b>' + _esc(tag) + '</b></font> '
                + restHtml
    }

    function appendLine(message) {
        var line = String(message)
        if (line.length === 0)
            return
        if (/^ep=\d+\/\d+\s*$/.test(line))
            return // служебный дубль для прогресс-бара — полноценная строка в [TRAIN][EP]
        var meta = _classify(line)
        var entry = {
            html: _renderHtml(line, meta, Qt.formatTime(new Date(), "hh:mm:ss")),
            group: meta.group,
            sev: meta.sev,
            kind: meta.kind
        }
        _allLines.push(entry)
        if (_allLines.length > maxLines) {
            var dropped = _allLines.shift()
            // Модель — упорядоченное подмножество _allLines под текущим фильтром,
            // поэтому выпавшая видимая строка всегда первая в модели.
            if (_matches(dropped) && logModel.count > 0)
                logModel.remove(0)
        }
        lineCount = _allLines.length
        if (_matches(entry)) {
            _appending = true
            logModel.append(entry)
            if (list.follow) {
                Qt.callLater(function () {
                    list.positionViewAtEnd()
                    logView._appending = false
                })
            } else {
                hiddenNewCount += 1
                logView._appending = false
            }
        }
    }

    function clearAll() {
        _allLines = []
        logModel.clear()
        lineCount = 0
        hiddenNewCount = 0
        list.follow = true
    }

    onActiveFilterChanged: _rebuildModel()

    function _rebuildModel() {
        logModel.clear()
        for (var i = 0; i < _allLines.length; i++) {
            if (_matches(_allLines[i]))
                logModel.append(_allLines[i])
        }
        hiddenNewCount = 0
        list.follow = true
        Qt.callLater(function () { list.positionViewAtEnd() })
    }

    RowLayout {
        Layout.fillWidth: true
        spacing: Math.round(6 * logView.uiScale)

        Repeater {
            model: [
                { key: "all", label: "ВСЁ" },
                { key: "episodes", label: "ЭПИЗОДЫ" },
                { key: "train", label: "ОБУЧЕНИЕ" },
                { key: "actors", label: "АКТОРЫ" },
                { key: "dist", label: "DIST/ПК2" },
                { key: "warn", label: "WARN" }
            ]
            delegate: Rectangle {
                property bool active: logView.activeFilter === modelData.key
                implicitHeight: Math.round(22 * logView.uiScale)
                implicitWidth: chipText.implicitWidth + Math.round(16 * logView.uiScale)
                radius: Math.round(2 * logView.uiScale)
                color: active ? "#2a2410" : (chipArea.containsMouse ? "#1c2530" : "#141b26")
                border.width: 1
                border.color: active ? "#b88a26" : "#334052"
                Text {
                    id: chipText
                    anchors.centerIn: parent
                    text: modelData.label
                    color: parent.active ? "#e1be68" : "#9aa3b2"
                    font.family: logView.fontDataFamily
                    font.pixelSize: Math.round(9 * logView.uiScale)
                    font.bold: true
                    font.letterSpacing: 0.6
                }
                MouseArea {
                    id: chipArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: logView.activeFilter = modelData.key
                }
            }
        }

        Item { Layout.fillWidth: true }

        Text {
            text: logView.visibleCount === logView.lineCount
                  ? logView.lineCount + " строк"
                  : logView.visibleCount + " / " + logView.lineCount + " строк"
            color: "#5c6a7d"
            font.family: logView.fontDataFamily
            font.pixelSize: Math.round(9 * logView.uiScale)
        }
    }

    Item {
        Layout.fillWidth: true
        Layout.fillHeight: true

        Rectangle {
            anchors.fill: parent
            radius: 0
            color: "#111722"
            border.width: 1
            border.color: "#2e394d"
        }

        ListView {
            id: list
            anchors.fill: parent
            anchors.margins: Math.round(6 * logView.uiScale)
            clip: true
            model: logModel
            boundsBehavior: Flickable.StopAtBounds
            property bool follow: true

            ScrollBar.vertical: ScrollBar { }

            // Автоскролл с паузой: ушёл вверх — хвост не дёргается, внизу плашка «N новых».
            onAtYEndChanged: {
                if (atYEnd) {
                    follow = true
                    logView.hiddenNewCount = 0
                }
            }
            onContentYChanged: {
                if (!atYEnd && !logView._appending)
                    follow = false
            }

            delegate: Item {
                width: list.width
                height: lineText.implicitHeight + Math.round((model.kind === "ep" ? 8 : 2) * logView.uiScale)

                Rectangle {
                    anchors.fill: parent
                    color: model.sev === "warn" ? "#261a10"
                                                : (model.kind === "ep" ? "#18222f" : "transparent")
                }
                Rectangle {
                    visible: model.kind === "ep"
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 1
                    color: "#3a4a60"
                }
                Text {
                    id: lineText
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.leftMargin: Math.round(4 * logView.uiScale)
                    anchors.rightMargin: Math.round(4 * logView.uiScale)
                    textFormat: Text.StyledText
                    wrapMode: Text.Wrap
                    text: model.html
                    color: "#dfe6f0"
                    font.family: logView.fontDataFamily
                    font.pixelSize: Math.round(11 * logView.uiScale)
                }
            }

            Text {
                anchors.centerIn: parent
                visible: logModel.count === 0
                text: logView.lineCount === 0
                      ? "Журнал пуст — строки появятся при запуске тренировки."
                      : "Нет строк под текущим фильтром."
                color: "#4d5666"
                font.family: logView.fontDataFamily
                font.pixelSize: Math.round(10 * logView.uiScale)
            }
        }

        Rectangle {
            visible: logView.hiddenNewCount > 0
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: Math.round(10 * logView.uiScale)
            implicitHeight: Math.round(22 * logView.uiScale)
            implicitWidth: newPillText.implicitWidth + Math.round(18 * logView.uiScale)
            radius: Math.round(11 * logView.uiScale)
            color: "#1c2533"
            border.width: 1
            border.color: "#b88a26"
            Text {
                id: newPillText
                anchors.centerIn: parent
                text: "▼ " + logView.hiddenNewCount + " новых"
                color: "#e1be68"
                font.family: logView.fontDataFamily
                font.pixelSize: Math.round(9 * logView.uiScale)
                font.bold: true
            }
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    list.follow = true
                    list.positionViewAtEnd()
                    logView.hiddenNewCount = 0
                }
            }
        }
    }
}
