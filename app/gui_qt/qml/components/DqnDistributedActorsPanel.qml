import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

// Distributed actors (ПК2) для DQN — Ape-X: env-воркеры на ПК2 → общий PER-replay на ПК1.
ChamferPanel {
    id: panel
    required property var rootUi

    readonly property var hp: controller.hpDqnHyperparamsMap
    readonly property bool distOn: dqnNum("distributed_actors_enabled", 0) === 1

    function dqnNum(k, d) {
        var v = hp[k]
        return (v === undefined || v === null || v === "") ? d : Number(v)
    }
    function dqnStr(k, d) {
        var v = hp[k]
        return (v === undefined || v === null) ? d : String(v)
    }
    function setKey(k, v) { controller.set_dqn_hyperparam(k, String(v)) }

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
                text: "DISTRIBUTED ACTORS"
                font.bold: true
                font.pixelSize: Math.round(12 * rootUi.uiScale)
                font.family: rootUi.fontUiFamily
                font.letterSpacing: 1.2
                color: rootUi.uiTextMain
            }
            Item { Layout.fillWidth: true }
            Rectangle {
                radius: Math.round(10 * rootUi.uiScale)
                color: panel.distOn
                    ? Qt.rgba(0.25, 0.72, 0.95, 0.15)
                    : Qt.rgba(0.5, 0.52, 0.56, 0.12)
                border.color: panel.distOn
                    ? Qt.rgba(0.45, 0.85, 1.0, 0.45)
                    : rootUi.uiBorder
                border.width: 1
                implicitWidth: modeBadge.implicitWidth + rootUi.spacingSm * 2
                implicitHeight: modeBadge.implicitHeight + rootUi.spacingXs * 2
                Label {
                    id: modeBadge
                    anchors.centerIn: parent
                    text: panel.distOn ? "LAN · ПК2" : "Локально"
                    color: panel.distOn ? "#7ee0ff" : rootUi.uiTextMuted
                    font.pixelSize: Math.round(10 * rootUi.uiScale)
                    font.bold: true
                    font.letterSpacing: 0.6
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            radius: Math.round(10 * rootUi.uiScale)
            color: panel.distOn
                ? Qt.rgba(0.15, 0.42, 0.62, 0.2)
                : Qt.rgba(0.35, 0.38, 0.42, 0.08)
            border.color: panel.distOn
                ? Qt.rgba(0.45, 0.75, 0.95, 0.55)
                : rootUi.uiBorder
            border.width: 1
            implicitHeight: distCol.implicitHeight + rootUi.spacingMd * 2

            ColumnLayout {
                id: distCol
                anchors.fill: parent
                anchors.margins: rootUi.spacingMd
                spacing: rootUi.spacingMd

                GmzIsToggleRow {
                    Layout.fillWidth: true
                    rootUi: panel.rootUi
                    title: "Distributed actors (ПК2)"
                    tooltipText: controller.dqnDistActorsTooltip
                    active: true
                    switchChecked: panel.distOn
                    switchEnabled: !controller.running
                    accentOn: "#6eb8ff"
                    accentOff: "#4a5564"
                    subtitle: panel.distOn
                        ? "Включено · на ПК2 после старта train: tools\\pc2_dqn_actors.bat"
                        : "Выключено — опыт для обучения собирают только процессы на этом ПК"
                    onToggled: function(checked) {
                        panel.setKey("distributed_actors_enabled", checked ? "1" : "0")
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: rootUi.spacingSm
                    visible: panel.distOn

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 1
                        color: Qt.rgba(0.45, 0.75, 0.95, 0.25)
                    }

                    GridLayout {
                        columns: 2
                        columnSpacing: rootUi.spacingMd
                        rowSpacing: rootUi.spacingSm
                        Layout.fillWidth: true

                        Text {
                            text: "Порт приёма"
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        SpinBox {
                            from: 1
                            to: 65535
                            value: panel.dqnNum("distributed_rollout_port", 5558)
                            onValueModified: panel.setKey("distributed_rollout_port", value)
                        }

                        Text {
                            text: "Auth token"
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        TextField {
                            Layout.fillWidth: true
                            text: panel.dqnStr("distributed_auth_token", "")
                            echoMode: TextInput.Password
                            placeholderText: "опционально"
                            onEditingFinished: panel.setKey("distributed_auth_token", text)
                            onActiveFocusChanged: if (!activeFocus) panel.setKey("distributed_auth_token", text)
                        }

                        Text {
                            text: "Доля эпизодов ПК1"
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        SpinBox {
                            from: 5
                            to: 95
                            stepSize: 5
                            value: Math.round(panel.dqnNum("distributed_local_episode_fraction", 0.7) * 100)
                            onValueModified: panel.setKey("distributed_local_episode_fraction", (value / 100).toFixed(2))
                        }

                        Text {
                            text: "Воркеров на ПК2"
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        SpinBox {
                            from: 1
                            to: 32
                            value: panel.dqnNum("distributed_pc2_num_workers", 8)
                            onValueModified: panel.setKey("distributed_pc2_num_workers", value)
                        }

                        Text {
                            text: "Drain (сек)"
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        SpinBox {
                            from: 5
                            to: 300
                            stepSize: 5
                            value: panel.dqnNum("distributed_actors_drain_sec", 30)
                            onValueModified: panel.setKey("distributed_actors_drain_sec", value)
                        }

                        Text {
                            text: "Ожидание ПК2 (сек)"
                            color: rootUi.uiTextMuted
                            font.pixelSize: Math.round(11 * rootUi.uiScale)
                        }
                        SpinBox {
                            from: 0
                            to: 3600
                            stepSize: 30
                            value: panel.dqnNum("distributed_wait_pc2_timeout_sec", 600)
                            onValueModified: panel.setKey("distributed_wait_pc2_timeout_sec", value)
                        }
                    }

                    GmzIsToggleRow {
                        Layout.fillWidth: true
                        rootUi: panel.rootUi
                        title: "Ждать ПК2 перед стартом"
                        tooltipText: controller.dqnDistWaitPc2Tooltip
                        active: true
                        switchChecked: panel.dqnNum("distributed_wait_pc2", 0) === 1
                        switchEnabled: !controller.running
                        accentOn: "#6eb8ff"
                        accentOff: "#4a5564"
                        subtitle: panel.dqnNum("distributed_wait_pc2", 0) === 1
                            ? "Train не начнёт сбор эпизодов, пока не подключатся все воркеры ПК2"
                            : "Старт сразу (только ПК1), ПК2 может подключиться позже"
                        onToggled: function(checked) {
                            panel.setKey("distributed_wait_pc2", checked ? "1" : "0")
                        }
                    }
                }
            }
        }

        Label {
            visible: panel.distOn
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: "Порядок: 1) Старт train на ПК1 → 2) pc2_dqn_actors.bat на ПК2. " +
                  "При «Ждать ПК2» train встанет на waiting_pc2, пока не придут все hello. " +
                  "Порт 5558 (у AZ свой, :5557 — не мешают друг другу)."
            color: rootUi.uiTextMuted
            font.pixelSize: Math.round(10 * rootUi.uiScale)
            font.italic: true
        }
    }
}
