import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: banner
    required property var rootUi

    Layout.fillWidth: true
    implicitHeight: bannerRow.implicitHeight + (rootUi ? rootUi.spacingMd : 12)
    radius: Math.round(10 * (rootUi ? rootUi.uiScale : 1))
    color: controller.trainingCudaAvailable
        ? Qt.rgba(0.18, 0.62, 0.42, 0.14)
        : Qt.rgba(0.75, 0.38, 0.22, 0.12)
    border.color: controller.trainingCudaAvailable
        ? Qt.rgba(0.35, 0.85, 0.55, 0.45)
        : Qt.rgba(0.9, 0.45, 0.3, 0.35)
    border.width: 1

    RowLayout {
        id: bannerRow
        anchors.fill: parent
        anchors.margins: rootUi ? rootUi.spacingMd : 12
        spacing: rootUi ? rootUi.spacingMd : 12

        Rectangle {
            width: Math.round(10 * (rootUi ? rootUi.uiScale : 1))
            height: width
            radius: width / 2
            color: controller.trainingCudaAvailable ? "#3ecf8e" : "#e07a52"
            Layout.alignment: Qt.AlignVCenter
        }

        ColumnLayout {
            spacing: Math.round(2 * (rootUi ? rootUi.uiScale : 1))
            Layout.fillWidth: true

            Label {
                text: controller.trainingCudaAvailable ? "CUDA доступна" : "CUDA недоступна"
                font.bold: true
                font.pixelSize: Math.round(14 * (rootUi ? rootUi.uiScale : 1))
                color: rootUi ? rootUi.uiTextMain : "#e8ecf4"
            }

            Label {
                text: controller.trainingDeviceSummary
                font.pixelSize: Math.round(12 * (rootUi ? rootUi.uiScale : 1))
                color: rootUi ? rootUi.uiTextMuted : "#98a4b8"
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
        }

        ToolButton {
            text: "↻"
            Layout.alignment: Qt.AlignTop
            ToolTip.visible: hovered
            ToolTip.text: "Обновить информацию о GPU / CUDA"
            onClicked: {
                if (typeof controller !== "undefined" && controller)
                    controller.refresh_training_device_info()
            }
        }
    }

    ToolTip.visible: bannerMouse.containsMouse && controller.trainingDeviceDetail.length > 0
    ToolTip.text: controller.trainingDeviceDetail
    ToolTip.delay: 400

    MouseArea {
        id: bannerMouse
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.NoButton
    }
}
