import QtQuick 2.15
import QtQuick.Controls 2.15

CheckBox {
    id: control

    property real scaleRef: 1.0
    property string labelFontFamily: "Rajdhani"
    property int labelFontSize: 11
    property color labelColorEnabled: "#d7dde7"
    property color labelColorDisabled: "#6b7280"

    padding: 0
    spacing: Math.round(10 * scaleRef)
    leftPadding: 0
    rightPadding: 0

    indicator: Rectangle {
        implicitWidth: Math.round(18 * scaleRef)
        implicitHeight: implicitWidth
        x: control.leftPadding
        y: control.height / 2 - height / 2
        radius: 0
        color: control.checked ? "#c79a32" : "#1a2230"
        border.width: 1
        border.color: control.checked
            ? "#e8c86a"
            : (control.hovered && control.enabled ? "#7a8496" : "#4f5a6b")

        Rectangle {
            anchors.centerIn: parent
            width: Math.round(8 * scaleRef)
            height: width
            radius: 0
            color: "#120f05"
            visible: control.checked
        }
    }

    contentItem: Text {
        text: control.text
        font.family: control.labelFontFamily
        font.pixelSize: control.labelFontSize
        font.bold: true
        opacity: control.enabled ? 1.0 : 0.45
        color: control.enabled ? control.labelColorEnabled : control.labelColorDisabled
        verticalAlignment: Text.AlignVCenter
        leftPadding: control.indicator.width + control.spacing
        rightPadding: 0
        elide: Text.ElideRight
    }

    background: Item {}
}
