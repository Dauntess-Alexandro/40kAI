import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    width: 960
    height: 720
    visible: true
    title: "40kAI — второй GUI (Qt)"

    property string statusText: "Готово к запуску."

    Item {
        anchors.fill: parent
        anchors.margins: 16

        ColumnLayout {
            anchors.fill: parent
            spacing: 12

            Text {
                text: "40kAI: запуск тренировки и оценки"
                font.pixelSize: 22
                font.bold: true
            }

            RowLayout {
                spacing: 12

                Button {
                    text: "Запуск Train"
                    enabled: !controller.running
                    onClicked: controller.start_train()
                }

                Button {
                    text: "Запуск Eval"
                    enabled: !controller.running
                    onClicked: controller.start_eval()
                }

                Button {
                    text: "Остановить"
                    enabled: controller.running
                    onClicked: controller.stop_process()
                }
            }

            GroupBox {
                title: "Логи"
                Layout.fillWidth: true
                Layout.fillHeight: true

                ScrollView {
                    anchors.fill: parent

                    TextArea {
                        id: logArea
                        readOnly: true
                        wrapMode: TextArea.Wrap
                        text: ""
                    }
                }
            }

            Rectangle {
                color: "#1f1f1f"
                radius: 6
                Layout.fillWidth: true
                height: 36

                Text {
                    anchors.centerIn: parent
                    color: "#ffffff"
                    text: root.statusText
                }
            }
        }
    }

    Connections {
        target: controller
        function onLogLine(message) {
            logArea.text += message + "\n"
            logArea.cursorPosition = logArea.length
        }
        function onStatusChanged(message) {
            root.statusText = message
        }
    }
}
