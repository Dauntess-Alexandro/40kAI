import QtQuick 2.15

Item {
    id: root
    property color fillColor: "#2f6ed8"
    property color borderColor: "#6f95cf"
    property color textColor: "#ffffff"
    property string label: ""
    property int borderWidth: 1

    implicitWidth: 30
    implicitHeight: 30

    Canvas {
        id: hexCanvas
        anchors.fill: parent
        antialiasing: true
        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()
            var w = width
            var h = height
            ctx.beginPath()
            ctx.moveTo(w * 0.25, 0)
            ctx.lineTo(w * 0.75, 0)
            ctx.lineTo(w, h * 0.5)
            ctx.lineTo(w * 0.75, h)
            ctx.lineTo(w * 0.25, h)
            ctx.lineTo(0, h * 0.5)
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

    Text {
        anchors.centerIn: parent
        text: root.label
        color: root.textColor
        font.bold: true
        font.pixelSize: Math.round(parent.height * 0.33)
    }

    onWidthChanged: hexCanvas.requestPaint()
    onHeightChanged: hexCanvas.requestPaint()
    onFillColorChanged: hexCanvas.requestPaint()
    onBorderColorChanged: hexCanvas.requestPaint()
}
