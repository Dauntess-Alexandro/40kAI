import QtQuick 2.15

Item {
    id: root
    property real pc1SegmentShare: 0.5
    property real pc1Fill: 0.0
    property real pc2Fill: 0.0
    property bool poolMode: false
    property bool waitingPc2: false
    property bool draining: false
    property color pc1Color: "#b88a26"
    property color pc2Color: "#3a6ea5"
    property color trackColor: "#16202f"
    property color borderColor: "#243650"
    property int barHeight: 10
    property real uiScale: 1.0

    implicitHeight: barHeight + Math.round(14 * uiScale)
    implicitWidth: 200

    readonly property real _pc1Share: Math.max(0.08, Math.min(0.92, pc1SegmentShare))

    Text {
        anchors.left: parent.left
        anchors.bottom: track.top
        anchors.bottomMargin: Math.round(3 * uiScale)
        text: "вклад в сбор"
        color: "#7d8ba0"
        font.pixelSize: Math.round(9 * uiScale)
        font.letterSpacing: 0.5
    }

    Row {
        id: legendRow
        anchors.right: parent.right
        anchors.bottom: track.top
        anchors.bottomMargin: Math.round(3 * uiScale)
        spacing: Math.round(10 * uiScale)

        Row {
            spacing: Math.round(4 * uiScale)
            Rectangle { width: 8; height: 8; radius: 2; color: pc1Color; anchors.verticalCenter: parent.verticalCenter }
            Text {
                text: poolMode ? "ПК1" : ("ПК1 " + Math.round(_pc1Share * 100) + "%")
                color: "#7d8ba0"
                font.pixelSize: Math.round(9 * uiScale)
            }
        }
        Row {
            spacing: Math.round(4 * uiScale)
            Rectangle { width: 8; height: 8; radius: 2; color: pc2Color; anchors.verticalCenter: parent.verticalCenter }
            Text {
                text: poolMode ? "ПК2" : ("ПК2 " + Math.round((1.0 - _pc1Share) * 100) + "%")
                color: "#7d8ba0"
                font.pixelSize: Math.round(9 * uiScale)
            }
        }
    }

    Item {
        id: track
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: root.barHeight

        Rectangle {
            anchors.fill: parent
            radius: Math.round(3 * uiScale)
            color: trackColor
            border.width: 1
            border.color: borderColor
        }

        Item {
            id: pc1Seg
            x: 0
            width: parent.width * _pc1Share
            height: parent.height
            clip: true

            Rectangle {
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: poolMode
                    ? parent.width
                    : parent.width * Math.max(0, Math.min(1, pc1Fill))
                radius: Math.round(3 * uiScale)
                color: pc1Color
                opacity: draining ? 0.55 : (waitingPc2 ? 0.45 : 1.0)
                Behavior on width {
                    NumberAnimation { duration: 450; easing.type: Easing.OutCubic }
                }
            }

            Rectangle {
                id: shimmerPc1
                visible: waitingPc2
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: Math.round(28 * uiScale)
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "transparent" }
                    GradientStop { position: 0.5; color: Qt.rgba(1, 1, 1, 0.22) }
                    GradientStop { position: 1.0; color: "transparent" }
                }
                SequentialAnimation on x {
                    running: waitingPc2 && root.visible
                    loops: Animation.Infinite
                    NumberAnimation {
                        from: -Math.round(28 * uiScale)
                        to: pc1Seg.width
                        duration: 1400
                        easing.type: Easing.InOutQuad
                    }
                }
            }
        }

        Rectangle {
            id: divider
            x: parent.width * _pc1Share - 0.5
            width: 1
            height: parent.height
            color: Qt.rgba(0, 0, 0, 0.45)
            visible: _pc1Share > 0.08 && _pc1Share < 0.92
        }

        Item {
            id: pc2Seg
            x: parent.width * _pc1Share
            width: parent.width * (1.0 - _pc1Share)
            height: parent.height
            clip: true

            Rectangle {
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: poolMode
                    ? parent.width
                    : parent.width * Math.max(0, Math.min(1, pc2Fill))
                radius: Math.round(3 * uiScale)
                color: pc2Color
                opacity: draining ? 0.55 : 1.0
                Behavior on width {
                    NumberAnimation { duration: 450; easing.type: Easing.OutCubic }
                }
            }

            Rectangle {
                id: shimmerPc2
                visible: waitingPc2
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: Math.round(28 * uiScale)
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0.0; color: "transparent" }
                    GradientStop { position: 0.5; color: Qt.rgba(1, 1, 1, 0.28) }
                    GradientStop { position: 1.0; color: "transparent" }
                }
                SequentialAnimation on x {
                    running: waitingPc2 && root.visible
                    loops: Animation.Infinite
                    NumberAnimation {
                        from: -Math.round(28 * uiScale)
                        to: pc2Seg.width
                        duration: 1100
                        easing.type: Easing.InOutQuad
                    }
                }
            }
        }
    }
}
