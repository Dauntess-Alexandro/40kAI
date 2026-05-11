import QtQuick 2.15

Item {
    id: root
    property color fillColor: "#1d2632"
    property color borderColor: "#2a3342"
    property int cutSize: 8
    property int borderWidth: 1
    property int contentMargin: 10
    default property alias contentData: content.data

    implicitWidth: content.implicitWidth + contentMargin * 2
    implicitHeight: content.implicitHeight + contentMargin * 2

    Canvas {
        id: frameCanvas
        anchors.fill: parent
        antialiasing: false
        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()
            var w = width
            var h = height
            var c = Math.max(0, Math.min(root.cutSize, Math.min(w, h) / 2))
            var offset = (root.borderWidth % 2 === 1) ? 0.5 : 0.0
            ctx.beginPath()
            ctx.moveTo(c + offset, 0 + offset)
            ctx.lineTo(w - offset, 0 + offset)
            ctx.lineTo(w - offset, h - c - offset)
            ctx.lineTo(w - c - offset, h - offset)
            ctx.lineTo(0 + offset, h - offset)
            ctx.lineTo(0 + offset, c + offset)
            ctx.closePath()
            ctx.fillStyle = root.fillColor
            ctx.fill()
            if (root.borderWidth > 0) {
                ctx.lineWidth = root.borderWidth
                ctx.strokeStyle = root.borderColor
                ctx.stroke()
            }
        }
    }

    Item {
        id: content
        anchors.fill: parent
        anchors.margins: root.contentMargin
    }

    onWidthChanged: frameCanvas.requestPaint()
    onHeightChanged: frameCanvas.requestPaint()
    onFillColorChanged: frameCanvas.requestPaint()
    onBorderColorChanged: frameCanvas.requestPaint()
    onCutSizeChanged: frameCanvas.requestPaint()
    onBorderWidthChanged: frameCanvas.requestPaint()
}
