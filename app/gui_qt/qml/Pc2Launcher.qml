pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 720
    height: 640
    visible: true
    title: qsTr("40kAI · ПК2 — запуск распределённого обучения")
    color: "#11151c"

    readonly property color accent: "#4aa3df"
    readonly property color panel: "#1b212b"
    readonly property color stroke: "#2c3542"
    property string selectedRole: ""

    function roleRequiresGpu(roleId) {
        for (let i = 0; i < controller.rolesModel.length; ++i)
            if (controller.rolesModel[i].id === roleId)
                return controller.rolesModel[i].requiresGpu;
        return false;
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 14

        Label {
            Layout.fillWidth: true
            text: qsTr("Один компьютер (ПК2) — одна общая папка с ПК1")
            color: "#e8eef6"
            font.pixelSize: 20
            font.bold: true
        }

        // --- Общая папка (SMB) ---
        Rectangle {
            Layout.fillWidth: true
            color: root.panel
            radius: 8
            border.color: root.stroke
            implicitHeight: shareCol.implicitHeight + 24

            ColumnLayout {
                id: shareCol
                anchors.fill: parent
                anchors.margins: 12
                spacing: 8

                Label {
                    text: qsTr("Общая папка ПК1 (40KAI_SHARE_ROOT)")
                    color: "#aebfd0"
                    font.pixelSize: 13
                }
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    TextField {
                        Layout.fillWidth: true
                        placeholderText: qsTr("\\\\PC1\\40kai_models  (или ...\\actor_sync)")
                        text: controller.shareRoot
                        color: "#e8eef6"
                        onTextEdited: controller.shareRoot = text
                        background: Rectangle {
                            color: "#0d1117"
                            radius: 6
                            border.color: root.stroke
                        }
                    }
                    Button {
                        text: qsTr("Проверить SMB")
                        onClicked: controller.checkSmb()
                    }
                }
                Label {
                    id: smbResult
                    Layout.fillWidth: true
                    wrapMode: Text.Wrap
                    text: qsTr("Укажите путь к общей папке ПК1 и нажмите «Проверить SMB».")
                    color: "#8aa0b6"
                    font.pixelSize: 12
                }
            }
        }

        // --- Выбор роли ---
        Label {
            text: qsTr("Что запустить на этом ПК2:")
            color: "#aebfd0"
            font.pixelSize: 13
        }
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 6
            Repeater {
                model: controller.rolesModel
                delegate: RadioButton {
                    id: roleDelegate
                    required property var modelData
                    Layout.fillWidth: true
                    enabled: !controller.running
                    checked: root.selectedRole === roleDelegate.modelData.id
                    onClicked: root.selectedRole = roleDelegate.modelData.id
                    contentItem: ColumnLayout {
                        spacing: 1
                        Label {
                            text: roleDelegate.modelData.label
                                  + (roleDelegate.modelData.requiresGpu ? qsTr("  · нужен GPU") : "")
                            color: "#e8eef6"
                            font.pixelSize: 14
                        }
                        Label {
                            text: roleDelegate.modelData.note
                            color: "#7e93a8"
                            font.pixelSize: 11
                            wrapMode: Text.Wrap
                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }

        // --- Управление ---
        RowLayout {
            Layout.fillWidth: true
            spacing: 10
            Button {
                text: controller.running ? qsTr("Запущено…") : qsTr("Старт")
                enabled: !controller.running && root.selectedRole !== ""
                onClicked: controller.start(root.selectedRole)
            }
            Button {
                text: qsTr("Стоп")
                enabled: controller.running
                onClicked: controller.stop()
            }
            Item { Layout.fillWidth: true }
            Label {
                text: controller.running ? qsTr("● работает: %1").arg(controller.activeRole)
                                          : qsTr("○ остановлено")
                color: controller.running ? "#5fd07a" : "#7e93a8"
                font.pixelSize: 12
            }
        }

        // --- Лог ---
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#0d1117"
            radius: 8
            border.color: root.stroke

            ScrollView {
                anchors.fill: parent
                anchors.margins: 8
                clip: true
                TextArea {
                    id: logView
                    readOnly: true
                    wrapMode: TextArea.Wrap
                    color: "#c3d2e2"
                    font.family: "Consolas"
                    font.pixelSize: 12
                    background: null
                }
            }
        }
    }

    Connections {
        target: controller
        function onLogLine(line) {
            logView.text += line + "\n";
            logView.cursorPosition = logView.length;
        }
        function onSmbChecked(ok, message) {
            smbResult.text = (ok ? "✓ " : "✗ ") + message;
            smbResult.color = ok ? "#5fd07a" : "#e06a5f";
        }
    }
}
