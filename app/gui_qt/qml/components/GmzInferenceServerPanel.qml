import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

ChamferPanel {
    id: panel
    required property var rootUi

    readonly property bool localIsOn: controller.gmzInferenceServerEnabled && !controller.remoteIsEnabled

    Layout.fillWidth: true
    fillColor: rootUi.uiBgBase
    borderColor: rootUi.uiBorder
    borderWidth: 1
    cutSize: Math.round(10 * rootUi.uiScale)
    contentMargin: rootUi.spacingMd
    implicitHeight: panelCol.implicitHeight + rootUi.spacingMd * 2

    ColumnLayout {
        id: panelCol
        width: parent.width
        spacing: rootUi.spacingMd

        RowLayout {
            Layout.fillWidth: true
            spacing: rootUi.spacingSm

            Text {
                text: "INFERENCE SERVER"
                font.bold: true
                font.pixelSize: Math.round(12 * rootUi.uiScale)
                font.family: rootUi.fontUiFamily
                font.letterSpacing: 1.2
                color: rootUi.uiTextMain
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                radius: Math.round(10 * rootUi.uiScale)
                color: controller.remoteIsEnabled
                    ? Qt.rgba(0.25, 0.72, 0.95, 0.15)
                    : (panel.localIsOn
                        ? Qt.rgba(0.22, 0.72, 0.45, 0.15)
                        : Qt.rgba(0.5, 0.52, 0.56, 0.12))
                border.color: controller.remoteIsEnabled
                    ? Qt.rgba(0.45, 0.85, 1.0, 0.45)
                    : (panel.localIsOn
                        ? Qt.rgba(0.35, 0.85, 0.55, 0.4)
                        : rootUi.uiBorder)
                border.width: 1
                implicitWidth: modeBadge.implicitWidth + rootUi.spacingSm * 2
                implicitHeight: modeBadge.implicitHeight + rootUi.spacingXs * 2

                Label {
                    id: modeBadge
                    anchors.centerIn: parent
                    text: controller.remoteIsEnabled
                        ? "LAN · ПК2"
                        : (panel.localIsOn ? "Local · B" : "Вариант A")
                    color: controller.remoteIsEnabled ? "#7ee0ff"
                        : (panel.localIsOn ? "#6ee7a0" : rootUi.uiTextMuted)
                    font.pixelSize: Math.round(10 * rootUi.uiScale)
                    font.bold: true
                    font.letterSpacing: 0.6
                }
            }
        }

        // --- Local ---
        Rectangle {
            Layout.fillWidth: true
            radius: Math.round(10 * rootUi.uiScale)
            opacity: controller.remoteIsEnabled ? 0.45 : 1.0
            color: panel.localIsOn
                ? Qt.rgba(0.18, 0.55, 0.38, 0.14)
                : Qt.rgba(0.35, 0.38, 0.42, 0.1)
            border.color: panel.localIsOn
                ? Qt.rgba(0.35, 0.85, 0.55, 0.5)
                : rootUi.uiBorder
            border.width: 1
            implicitHeight: localToggle.implicitHeight + rootUi.spacingMd * 2

            GmzIsToggleRow {
                id: localToggle
                anchors.fill: parent
                anchors.margins: rootUi.spacingMd
                rootUi: panel.rootUi
                title: "Local Inference server"
                tooltipText: controller.gmzLocalIsTooltip
                active: !controller.remoteIsEnabled
                switchChecked: panel.localIsOn
                switchEnabled: !controller.remoteIsEnabled
                    && (controller.trainingCudaAvailable || panel.localIsOn)
                accentOn: "#3ecf8e"
                accentOff: "#4a5564"
                subtitle: controller.remoteIsEnabled
                    ? "Выключено — используется LAN / ПК2"
                    : (!controller.trainingCudaAvailable
                        ? "Требуется CUDA"
                        : (panel.localIsOn
                            ? "6 CPU env workers + GPU IS + learner на этом ПК"
                            : "Вариант A: до 2 GPU-акторов"))
                onToggled: function(checked) {
                    if (controller.remoteIsEnabled)
                        return
                    if (checked && !controller.trainingCudaAvailable)
                        return
                    controller.set_gmz_inference_server_mode(checked)
                }
            }
        }

        // --- LAN ---
        Rectangle {
            Layout.fillWidth: true
            radius: Math.round(10 * rootUi.uiScale)
            color: controller.remoteIsEnabled
                ? Qt.rgba(0.15, 0.42, 0.62, 0.2)
                : Qt.rgba(0.35, 0.38, 0.42, 0.08)
            border.color: controller.remoteIsEnabled
                ? Qt.rgba(0.45, 0.75, 0.95, 0.55)
                : rootUi.uiBorder
            border.width: 1
            implicitHeight: lanCol.implicitHeight + rootUi.spacingMd * 2

            ColumnLayout {
                id: lanCol
                anchors.fill: parent
                anchors.margins: rootUi.spacingMd
                spacing: rootUi.spacingMd

                GmzIsToggleRow {
                    Layout.fillWidth: true
                    rootUi: panel.rootUi
                    title: "LAN Inference server"
                    tooltipText: controller.gmzLanIsTooltip
                    active: true
                    switchChecked: controller.remoteIsEnabled
                    switchEnabled: !controller.running
                    accentOn: "#4eb8e8"
                    accentOff: "#4a5564"
                    subtitle: controller.remoteIsEnabled
                        ? "Инференс на GPU ПК2 · tools\\pc2_remote_is.bat"
                        : "Второй ПК в LAN · при включении Local выключается"
                    onToggled: function(checked) {
                        controller.setRemoteIsEnabled(checked)
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: rootUi.spacingSm
                    visible: controller.remoteIsEnabled
                    opacity: controller.remoteIsEnabled ? 1.0 : 0.0

                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: Qt.rgba(0.45, 0.75, 0.95, 0.25)
                    }

                    GridLayout {
                        columns: 2
                        columnSpacing: rootUi.spacingMd
                        rowSpacing: rootUi.spacingSm
                        Layout.fillWidth: true

                        Text { text: "Хост ПК2"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.remoteIsHost
                            placeholderText: "192.168.1.100"
                            onEditingFinished: controller.setRemoteIsHost(text)
                        }

                        Text { text: "Порт"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        SpinBox {
                            from: 1
                            to: 65535
                            value: controller.remoteIsPort
                            // onValueModified — только ручное изменение; onValueChanged ловил бы и
                            // программный апдейт value из controller → binding loop.
                            onValueModified: controller.setRemoteIsPort(value)
                        }

                        Text { text: "Таймаут, с"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.remoteIsTimeout.toFixed(1)
                            inputMethodHints: Qt.ImhFormattedNumbersOnly
                            onEditingFinished: controller.setRemoteIsTimeout(parseFloat(text))
                        }

                        Text { text: "Auth token"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.remoteIsAuthToken
                            echoMode: TextInput.Password
                            placeholderText: "опционально"
                            onEditingFinished: controller.setRemoteIsAuthToken(text)
                        }

                        Text { text: "Веса на ПК2"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.remoteIsWeightsPath
                            placeholderText: "Z:/artifacts/.../latest_gmz_policy.pth"
                            onEditingFinished: controller.setRemoteIsWeightsPath(text)
                        }

                        Text { text: "UNC (справка)"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.remoteIsSmbUncHint
                            placeholderText: "\\\\PC1\\share\\..."
                            onEditingFinished: controller.setRemoteIsSmbUncHint(text)
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: rootUi.spacingSm
                        Button {
                            text: "Проверить соединение"
                            enabled: !controller.running
                            onClicked: controller.checkRemoteIsConnection()
                        }
                        Label {
                            text: controller.remoteIsStatusText
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            color: controller.remoteIsStatusText.indexOf("OK") >= 0 ? "#6ee7a0" : "#f0a0a0"
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        Label {
                            text: "RTT " + controller.remoteIsLatencyText
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                    }
                }
            }
        }
    }
}
