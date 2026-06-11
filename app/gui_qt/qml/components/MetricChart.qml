import QtQuick
import QtQuick.Layouts
import ".."

// Карточка одной DET-метрики: заголовок + линейный график (рисуется на Canvas,
// без QtCharts — он нестабилен в текущей сборке) + чипы «Текущее/Среднее/Мин/Макс».
// Тема берётся из переданных токенов. Данные: xs (общая ось X) + series [{name,color,ys}].
Item {
    id: card

    // --- данные ---
    property string title: ""
    property string desc: ""
    property var xs: []
    property var series: []
    property string fmt: "num"          // num | pct | int

    // --- тема ---
    property color accent: "#2f6ed8"
    property color textMain: "#d7dde7"
    property color textMuted: "#98a4b8"
    property color panelFill: "#1E293B"
    property color panelBorder: "#334155"
    property color gridColor: "#27324a"
    property real uiScale: 1.0
    property int captionSize: 11

    implicitHeight: Math.round(258 * uiScale)

    property var statBox: _stats()

    function _stats() {
        var s = (series && series.length > 0) ? series[0].ys : []
        if (!s || s.length === 0)
            return { cur: NaN, avg: NaN, min: NaN, max: NaN }
        var sum = 0, mn = s[0], mx = s[0]
        for (var i = 0; i < s.length; i++) {
            sum += s[i]
            if (s[i] < mn) mn = s[i]
            if (s[i] > mx) mx = s[i]
        }
        return { cur: s[s.length - 1], avg: sum / s.length, min: mn, max: mx }
    }

    function _fmt(v) {
        if (v === undefined || v === null || isNaN(v)) return "—"
        if (fmt === "pct") return (v * 100).toFixed(1) + "%"
        if (fmt === "int") return Math.round(v).toString()
        return Math.abs(v) >= 100 ? v.toFixed(0) : v.toFixed(2)
    }

    onXsChanged: { statBox = _stats(); plot.requestPaint() }
    onSeriesChanged: { statBox = _stats(); plot.requestPaint() }

    // Фон карточки в стиле проекта.
    ChamferPanel {
        anchors.fill: parent
        cutSize: Math.round(8 * card.uiScale)
        contentMargin: 0
        fillColor: card.panelFill
        borderWidth: 1
        borderColor: card.panelBorder
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Math.round(12 * card.uiScale)
        spacing: Math.round(6 * card.uiScale)

        // Заголовок + легенда (для нескольких серий).
        RowLayout {
            Layout.fillWidth: true
            spacing: Math.round(8 * card.uiScale)

            Text {
                text: card.title
                color: card.textMain
                font.bold: true
                font.pixelSize: card.captionSize + 2
                Layout.fillWidth: true
                elide: Text.ElideRight
            }
            Repeater {
                model: card.series.length > 1 ? card.series : []
                delegate: RowLayout {
                    spacing: Math.round(3 * card.uiScale)
                    Rectangle {
                        implicitWidth: Math.round(8 * card.uiScale)
                        implicitHeight: Math.round(8 * card.uiScale)
                        radius: implicitWidth / 2
                        color: modelData.color || card.accent
                        Layout.alignment: Qt.AlignVCenter
                    }
                    Text {
                        text: modelData.name || ""
                        color: card.textMuted
                        font.pixelSize: card.captionSize
                    }
                }
            }
        }

        // График на Canvas.
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Canvas {
                id: plot
                anchors.fill: parent
                antialiasing: true
                onWidthChanged: requestPaint()
                onHeightChanged: requestPaint()

                onPaint: {
                    var ctx = getContext("2d")
                    ctx.reset()
                    ctx.clearRect(0, 0, width, height)

                    var hasData = card.xs && card.xs.length > 0 && card.series && card.series.length > 0
                    emptyLabel.visible = !hasData
                    if (!hasData)
                        return

                    var xs = card.xs
                    var xmin = xs[0], xmax = xs[xs.length - 1]
                    if (xmin === xmax) { xmin -= 1; xmax += 1 }

                    var ymin = Infinity, ymax = -Infinity
                    for (var si = 0; si < card.series.length; si++) {
                        var ys = card.series[si].ys || []
                        for (var i = 0; i < ys.length; i++) {
                            if (ys[i] < ymin) ymin = ys[i]
                            if (ys[i] > ymax) ymax = ys[i]
                        }
                    }
                    if (!isFinite(ymin)) { ymin = 0; ymax = 1 }
                    if (ymin === ymax) { ymin -= 1; ymax += 1 }
                    var pad = (ymax - ymin) * 0.10
                    ymin -= pad; ymax += pad

                    var padL = Math.round(40 * card.uiScale)
                    var padR = Math.round(8 * card.uiScale)
                    var padT = Math.round(6 * card.uiScale)
                    var padB = Math.round(18 * card.uiScale)
                    var pw = Math.max(1, width - padL - padR)
                    var ph = Math.max(1, height - padT - padB)
                    var fs = Math.max(8, card.captionSize - 1)
                    ctx.font = fs + "px sans-serif"
                    ctx.textBaseline = "middle"

                    function mapX(x) { return padL + (x - xmin) / (xmax - xmin) * pw }
                    function mapY(y) { return padT + (1 - (y - ymin) / (ymax - ymin)) * ph }

                    // Сетка + Y-подписи (4 линии).
                    ctx.strokeStyle = card.gridColor
                    ctx.fillStyle = card.textMuted
                    ctx.lineWidth = 1
                    var rows = 4
                    ctx.textAlign = "right"
                    for (var r = 0; r <= rows; r++) {
                        var gy = padT + ph * r / rows
                        ctx.globalAlpha = 0.6
                        ctx.beginPath()
                        ctx.moveTo(padL, gy)
                        ctx.lineTo(padL + pw, gy)
                        ctx.stroke()
                        ctx.globalAlpha = 1.0
                        var val = ymax - (ymax - ymin) * r / rows
                        ctx.fillText(card._fmt(val), padL - Math.round(4 * card.uiScale), gy)
                    }

                    // X-подписи (начало/конец).
                    ctx.textAlign = "left"
                    ctx.fillText(Math.round(xmin).toString(), padL, height - Math.round(8 * card.uiScale))
                    ctx.textAlign = "right"
                    ctx.fillText(Math.round(xmax).toString(), padL + pw, height - Math.round(8 * card.uiScale))

                    // Линии серий.
                    for (var k = 0; k < card.series.length; k++) {
                        var def = card.series[k]
                        var yy = def.ys || []
                        var n = Math.min(xs.length, yy.length)
                        if (n < 1) continue
                        ctx.strokeStyle = def.color || card.accent
                        ctx.lineWidth = Math.max(2, Math.round(2 * card.uiScale))
                        ctx.lineJoin = "round"
                        ctx.beginPath()
                        for (var j = 0; j < n; j++) {
                            var px = mapX(xs[j]), py = mapY(yy[j])
                            if (j === 0) ctx.moveTo(px, py)
                            else ctx.lineTo(px, py)
                        }
                        ctx.stroke()
                        // точки для коротких серий
                        if (n <= 40) {
                            ctx.fillStyle = def.color || card.accent
                            for (var d = 0; d < n; d++) {
                                ctx.beginPath()
                                ctx.arc(mapX(xs[d]), mapY(yy[d]), Math.max(1.5, 2 * card.uiScale), 0, 2 * Math.PI)
                                ctx.fill()
                            }
                        }
                    }
                }
            }

            Text {
                id: emptyLabel
                anchors.centerIn: parent
                text: "Нет данных метрик"
                color: card.textMuted
                font.pixelSize: card.captionSize
                visible: false
            }
        }

        // Чипы статистики.
        RowLayout {
            Layout.fillWidth: true
            spacing: Math.round(6 * card.uiScale)

            Repeater {
                model: [
                    { k: "Текущее", v: card._fmt(card.statBox.cur) },
                    { k: "Среднее", v: card._fmt(card.statBox.avg) },
                    { k: "Мин", v: card._fmt(card.statBox.min) },
                    { k: "Макс", v: card._fmt(card.statBox.max) }
                ]
                delegate: Rectangle {
                    Layout.fillWidth: true
                    radius: Math.round(4 * card.uiScale)
                    color: Qt.rgba(1, 1, 1, 0.04)
                    border.width: 1
                    border.color: card.panelBorder
                    implicitHeight: Math.round(34 * card.uiScale)

                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 0
                        Text {
                            text: modelData.k
                            color: card.textMuted
                            font.pixelSize: Math.max(8, card.captionSize - 1)
                            Layout.alignment: Qt.AlignHCenter
                        }
                        Text {
                            text: modelData.v
                            color: card.textMain
                            font.bold: true
                            font.pixelSize: card.captionSize
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
        }
    }
}
