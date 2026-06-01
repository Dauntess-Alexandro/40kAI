import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

// Inference Server (вариант B) для AlphaZero tree.
// Полностью на AZ-гиперпараметрах (controller.hpAzTreeHyperparamsMap /
// controller.set_az_tree_hyperparam) — train.py читает их из hyperparams.json.
ChamferPanel {
    id: panel
    required property var rootUi

    readonly property var hp: controller.hpAzTreeHyperparamsMap
    readonly property bool isEnabled: azNum("inference_server_enabled", 0) === 1
    readonly property string mode: azStr("inference_server_mode", "local")
    readonly property bool localOn: isEnabled && mode === "local"
    readonly property bool lanOn: isEnabled && mode === "remote"

    function azNum(k, d) {
        var v = hp[k]
        return (v === undefined || v === null || v === "") ? d : Number(v)
    }
    function azStr(k, d) {
        var v = hp[k]
        return (v === undefined || v === null) ? d : String(v)
    }
    function setKey(k, v) { controller.set_az_tree_hyperparam(k, String(v)) }

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

        // --- Заголовок + бейдж режима ---
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
                color: panel.lanOn
                    ? Qt.rgba(0.25, 0.72, 0.95, 0.15)
                    : (panel.localOn ? Qt.rgba(0.22, 0.72, 0.45, 0.15) : Qt.rgba(0.5, 0.52, 0.56, 0.12))
                border.color: panel.lanOn
                    ? Qt.rgba(0.45, 0.85, 1.0, 0.45)
                    : (panel.localOn ? Qt.rgba(0.35, 0.85, 0.55, 0.4) : rootUi.uiBorder)
                border.width: 1
                implicitWidth: modeBadge.implicitWidth + rootUi.spacingSm * 2
                implicitHeight: modeBadge.implicitHeight + rootUi.spacingXs * 2
                Label {
                    id: modeBadge
                    anchors.centerIn: parent
                    text: panel.lanOn ? "LAN · ПК2" : (panel.localOn ? "Local · B" : "Вариант A")
                    color: panel.lanOn ? "#7ee0ff" : (panel.localOn ? "#6ee7a0" : rootUi.uiTextMuted)
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
            opacity: panel.lanOn ? 0.45 : 1.0
            color: panel.localOn ? Qt.rgba(0.18, 0.55, 0.38, 0.14) : Qt.rgba(0.35, 0.38, 0.42, 0.1)
            border.color: panel.localOn ? Qt.rgba(0.35, 0.85, 0.55, 0.5) : rootUi.uiBorder
            border.width: 1
            implicitHeight: localToggle.implicitHeight + rootUi.spacingMd * 2

            GmzIsToggleRow {
                id: localToggle
                anchors.fill: parent
                anchors.margins: rootUi.spacingMd
                rootUi: panel.rootUi
                title: "Local Inference server"
                tooltipText: "Вынести net.infer на GPU этого ПК. CPU env workers + GPU IS + learner. Требуется CUDA."
                active: !panel.lanOn
                switchChecked: panel.localOn
                switchEnabled: !panel.lanOn && !controller.running
                    && (controller.trainingCudaAvailable || panel.localOn)
                accentOn: "#3ecf8e"
                accentOff: "#4a5564"
                subtitle: panel.lanOn
                    ? "Выключено — используется LAN / ПК2"
                    : (!controller.trainingCudaAvailable
                        ? "Требуется CUDA"
                        : (panel.localOn
                            ? "CPU env workers + GPU inference server + learner на этом ПК"
                            : "Вариант A: CPU акторы с локальной сетью"))
                onToggled: function(checked) {
                    if (panel.lanOn) return
                    if (checked && !controller.trainingCudaAvailable) return
                    panel.setKey("inference_server_mode", "local")
                    panel.setKey("inference_server_enabled", checked ? "1" : "0")
                }
            }
        }

        // --- LAN ---
        Rectangle {
            Layout.fillWidth: true
            radius: Math.round(10 * rootUi.uiScale)
            color: panel.lanOn ? Qt.rgba(0.15, 0.42, 0.62, 0.2) : Qt.rgba(0.35, 0.38, 0.42, 0.08)
            border.color: panel.lanOn ? Qt.rgba(0.45, 0.75, 0.95, 0.55) : rootUi.uiBorder
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
                    tooltipText: "Инференс на GPU второго ПК (ПК2). MCTS+env остаются на этом ПК. Порт 5555."
                    active: true
                    switchChecked: panel.lanOn
                    switchEnabled: !controller.running
                    accentOn: "#4eb8e8"
                    accentOff: "#4a5564"
                    subtitle: panel.lanOn
                        ? "Инференс на GPU ПК2 · tools\\pc2_remote_az_is.bat"
                        : "Второй ПК в LAN · при включении Local выключается"
                    onToggled: function(checked) {
                        panel.setKey("inference_server_mode", checked ? "remote" : "local")
                        panel.setKey("inference_server_enabled", checked ? "1" : "0")
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: rootUi.spacingSm
                    visible: panel.lanOn

                    Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: Qt.rgba(0.45, 0.75, 0.95, 0.25) }

                    GridLayout {
                        columns: 2
                        columnSpacing: rootUi.spacingMd
                        rowSpacing: rootUi.spacingSm
                        Layout.fillWidth: true

                        Text { text: "Хост ПК2"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: panel.azStr("inference_remote_host", "127.0.0.1")
                            placeholderText: "192.168.1.100"
                            onEditingFinished: panel.setKey("inference_remote_host", text)
                        }

                        Text { text: "Порт"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        SpinBox {
                            from: 1; to: 65535
                            value: panel.azNum("inference_remote_port", 5555)
                            onValueModified: panel.setKey("inference_remote_port", value)
                        }

                        Text { text: "Таймаут, с"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: panel.azNum("inference_timeout", 5.0).toFixed(1)
                            inputMethodHints: Qt.ImhFormattedNumbersOnly
                            onEditingFinished: panel.setKey("inference_timeout", parseFloat(text))
                        }

                        Text { text: "Auth token"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: panel.azStr("inference_remote_auth_token", "")
                            echoMode: TextInput.Password
                            placeholderText: "опционально"
                            onEditingFinished: panel.setKey("inference_remote_auth_token", text)
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: rootUi.spacingSm
                        Button {
                            text: "Проверить соединение"
                            enabled: !controller.running
                            onClicked: controller.checkAzInferenceConnection()
                        }
                        Label {
                            text: controller.azInferenceStatusText
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            color: controller.azInferenceStatusText.indexOf("OK") >= 0 ? "#6ee7a0" : "#f0a0a0"
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        Label {
                            text: "RTT " + controller.azInferenceLatencyText
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                    }
                }
            }
        }

        // --- Общие параметры (видны когда IS включён) ---
        GridLayout {
            Layout.fillWidth: true
            visible: panel.isEnabled
            columns: 2
            columnSpacing: rootUi.spacingMd
            rowSpacing: rootUi.spacingSm

            Text { text: "env workers"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
            SpinBox {
                from: 1; to: 64
                value: panel.azNum("num_env_workers", 8)
                onValueModified: panel.setKey("num_env_workers", value)
            }
            Text { text: "batch size"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
            SpinBox {
                from: 1; to: 256
                value: panel.azNum("inference_batch_size", 32)
                onValueModified: panel.setKey("inference_batch_size", value)
            }
            Text { text: "batch interval, мс"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
            SpinBox {
                from: 1; to: 200
                value: panel.azNum("inference_batch_interval_ms", 10)
                onValueModified: panel.setKey("inference_batch_interval_ms", value)
            }
        }

        Label {
            visible: panel.lanOn
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: "Совет: для LAN рекомендуется mcts_max_depth=1 (меньше round-trip)."
            color: rootUi.uiTextMuted
            font.pixelSize: Math.round(10 * rootUi.uiScale)
            font.italic: true
        }
    }
}
