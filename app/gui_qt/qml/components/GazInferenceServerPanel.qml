import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

ChamferPanel {
    id: panel
    required property var rootUi

    readonly property var hp: controller.hpGazHyperparamsMap
    readonly property bool isEnabled: controller.gazInferenceServerEnabled || controller.gazRemoteIsEnabled
    readonly property bool localIsOn: controller.gazInferenceServerEnabled && !controller.gazRemoteIsEnabled

    function gazNum(k, d) {
        var v = hp[k]
        return (v === undefined || v === null || v === "") ? d : Number(v)
    }
    function setKey(k, v) { controller.set_gaz_hyperparam(k, String(v)) }

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
                color: controller.gazRemoteIsEnabled
                    ? Qt.rgba(0.25, 0.72, 0.95, 0.15)
                    : (panel.localIsOn
                        ? Qt.rgba(0.22, 0.72, 0.45, 0.15)
                        : Qt.rgba(0.5, 0.52, 0.56, 0.12))
                border.color: controller.gazRemoteIsEnabled
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
                    text: controller.gazRemoteIsEnabled
                        ? "LAN · ПК2"
                        : (panel.localIsOn ? "Local · B" : "Вариант A")
                    color: controller.gazRemoteIsEnabled ? "#7ee0ff"
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
            opacity: controller.gazRemoteIsEnabled ? 0.45 : 1.0
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
                tooltipText: "Local: GPU IS-процесс + CPU env-воркеры (GumbelAlphaZeroSearch) + learner на одном ПК. " +
                    "Сеть та же, что у AZ tree. Требуется CUDA. Дефолт выключен (вариант A — GPU-акторы)."
                active: !controller.gazRemoteIsEnabled
                switchChecked: panel.localIsOn
                switchEnabled: !controller.gazRemoteIsEnabled
                    && (controller.trainingCudaAvailable || panel.localIsOn)
                accentOn: "#3ecf8e"
                accentOff: "#4a5564"
                subtitle: controller.gazRemoteIsEnabled
                    ? "Выключено — используется LAN / ПК2"
                    : (!controller.trainingCudaAvailable
                        ? "Требуется CUDA"
                        : (panel.localIsOn
                            ? "CPU env workers + GPU IS + learner на этом ПК"
                            : "Вариант A: GPU-акторы"))
                onToggled: function(checked) {
                    if (controller.gazRemoteIsEnabled)
                        return
                    if (checked && !controller.trainingCudaAvailable)
                        return
                    controller.set_gaz_inference_server_mode(checked)
                }
            }
        }

        // --- LAN ---
        Rectangle {
            Layout.fillWidth: true
            radius: Math.round(10 * rootUi.uiScale)
            color: controller.gazRemoteIsEnabled
                ? Qt.rgba(0.15, 0.42, 0.62, 0.2)
                : Qt.rgba(0.35, 0.38, 0.42, 0.08)
            border.color: controller.gazRemoteIsEnabled
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
                    tooltipText: "LAN: net.infer уходит на GPU ПК2 (порт 5565). Дерево SH + env-rollout остаются на ПК1. " +
                        "Запуск на ПК2 — tools\\pc2_remote_gaz_is.bat. При включении Local выключается."
                    active: true
                    switchChecked: controller.gazRemoteIsEnabled
                    switchEnabled: !controller.running
                    accentOn: "#4eb8e8"
                    accentOff: "#4a5564"
                    subtitle: controller.gazRemoteIsEnabled
                        ? "Инференс на GPU ПК2 · tools\\pc2_remote_gaz_is.bat (порт 5565)"
                        : "Второй ПК в LAN · при включении Local выключается"
                    onToggled: function(checked) {
                        controller.setGazRemoteIsEnabled(checked)
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: rootUi.spacingSm
                    visible: controller.gazRemoteIsEnabled
                    opacity: controller.gazRemoteIsEnabled ? 1.0 : 0.0

                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: Qt.rgba(0.45, 0.75, 0.95, 0.25)
                    }

                    GmzIsToggleRow {
                        Layout.fillWidth: true
                        rootUi: panel.rootUi
                        title: "Distributed actors (ПК2)"
                        tooltipText: "Self-play на CPU ПК2: rollout → этот ПК (:5567). На ПК2 после train: " +
                            "tools\\pc2_remote_gaz_is.bat (IS + actors одной кнопкой)."
                        active: true
                        switchChecked: controller.gazDistributedActors
                        switchEnabled: !controller.running
                        accentOn: "#6eb8ff"
                        accentOff: "#4a5564"
                        subtitle: controller.gazDistributedActors
                            ? "Включено · на ПК2: pc2_remote_gaz_is.bat (IS + actors вместе)"
                            : "Выключено — только infer на ПК2, env только на этом ПК"
                        onToggled: function(checked) {
                            controller.setGazDistributedActors(checked)
                        }
                    }

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
                            text: controller.gazRemoteIsHost
                            placeholderText: "192.168.1.100"
                            onEditingFinished: controller.setGazRemoteIsHost(text)
                        }

                        Text { text: "Порт"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        SpinBox {
                            from: 1
                            to: 65535
                            value: controller.gazRemoteIsPort
                            // onValueModified — только ручное изменение (избегаем binding loop).
                            onValueModified: controller.setGazRemoteIsPort(value)
                        }

                        Text { text: "Таймаут, с"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.gazRemoteIsTimeout.toFixed(1)
                            inputMethodHints: Qt.ImhFormattedNumbersOnly
                            onEditingFinished: controller.setGazRemoteIsTimeout(parseFloat(text))
                        }

                        Text { text: "Auth token"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.gazRemoteIsAuthToken
                            echoMode: TextInput.Password
                            placeholderText: "опционально"
                            onEditingFinished: controller.setGazRemoteIsAuthToken(text)
                        }

                        Text { text: "Веса на ПК2"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.gazRemoteIsWeightsPath
                            placeholderText: "Z:/artifacts/.../latest_az_gumbel_az_policy.pth"
                            onEditingFinished: controller.setGazRemoteIsWeightsPath(text)
                        }

                        Text { text: "UNC (справка)"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
                        TextField {
                            Layout.fillWidth: true
                            text: controller.gazRemoteIsSmbUncHint
                            placeholderText: "\\\\PC1\\share\\..."
                            onEditingFinished: controller.setGazRemoteIsSmbUncHint(text)
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: rootUi.spacingSm
                        Button {
                            text: "Проверить соединение"
                            enabled: !controller.running
                            onClicked: controller.checkGazRemoteIsConnection()
                        }
                        Label {
                            text: controller.gazRemoteIsStatusText
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            color: controller.gazRemoteIsStatusText.indexOf("OK") >= 0 ? "#6ee7a0" : "#f0a0a0"
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        Label {
                            text: "RTT " + controller.gazRemoteIsLatencyText
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                    }
                }
            }
        }

        // --- Общие параметры (видны когда IS включён: local или LAN) ---
        GridLayout {
            Layout.fillWidth: true
            visible: panel.isEnabled
            columns: 2
            columnSpacing: rootUi.spacingMd
            rowSpacing: rootUi.spacingSm

            Text { text: "env workers"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
            SpinBox {
                from: 1; to: 64
                value: panel.gazNum("num_env_workers", 8)
                onValueModified: panel.setKey("num_env_workers", value)
            }
            Text { text: "batch size"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
            SpinBox {
                from: 1; to: 256
                value: panel.gazNum("inference_batch_size", 32)
                onValueModified: panel.setKey("inference_batch_size", value)
            }
            Text { text: "batch interval, мс"; color: rootUi.uiTextMuted; font.pixelSize: Math.round(11 * rootUi.uiScale) }
            SpinBox {
                from: 1; to: 200
                value: panel.gazNum("inference_batch_interval_ms", 10)
                onValueModified: panel.setKey("inference_batch_interval_ms", value)
            }
        }

        Label {
            visible: controller.gazRemoteIsEnabled
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: "Совет: для LAN рекомендуется max_depth=1 (меньше round-trip)."
            color: rootUi.uiTextMuted
            font.pixelSize: Math.round(10 * rootUi.uiScale)
            font.italic: true
        }

        Label {
            visible: panel.isEnabled
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: "Dist-акторы ПК2: Gumbel/hyperparams подтягиваются из SMB gaz_dist_train_context.json (ПК1 пишет при train) — git pull не нужен.\n" +
                  "inference batch size — на ПК1; remote IS: GAZ_REMOTE_BATCH_SIZE ≥ batch size (heavy ≈ 64) в pc2_remote_gaz_is_config.bat."
            color: rootUi.uiTextMuted
            font.pixelSize: Math.round(10 * rootUi.uiScale)
            font.italic: true
        }
    }
}
