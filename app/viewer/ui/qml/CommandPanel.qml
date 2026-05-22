import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "tokens.js" as Tokens

Rectangle {
    id: cmdRoot
    color: bgSurfaceColor
    implicitHeight: contentCol.implicitHeight + spacingMd * 2
    radius: radiusSm
    border.color: borderMutedColor

    readonly property bool hasCtrl: viewerController !== null && viewerController !== undefined
    readonly property string kind: hasCtrl ? viewerController.commandKind : "idle"
    readonly property bool confirmOk: hasCtrl && viewerController.commandConfirmEnabled

    component PrimaryButton: Button {
        property string hotkeySuffix: ""
        highlighted: true
        enabled: cmdRoot.confirmOk
        opacity: enabled ? 1.0 : 0.45
        Layout.fillWidth: true
        Layout.preferredHeight: 34
        contentItem: Label {
            text: parent.text + (parent.hotkeySuffix ? ("  " + parent.hotkeySuffix) : "")
            color: "#0F172A"
            font.bold: true
            font.pixelSize: fontMd
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        background: Rectangle {
            radius: radiusBtn
            color: parent.enabled ? accentPrimaryColor : bgElevatedColor
            border.color: borderMutedColor
        }
    }

    ColumnLayout {
        id: contentCol
        anchors.fill: parent
        anchors.margins: spacingSm
        spacing: spacingXs

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: Tokens.phaseIcon(hasCtrl ? viewerController.phaseRaw : "")
                font.pixelSize: fontLg
            }
            Label {
                Layout.fillWidth: true
                text: hasCtrl ? viewerController.commandPromptText : qsTr("Ожидаю команду…")
                color: textPrimaryColor
                font.pixelSize: bodyFontSize
                font.bold: true
                wrapMode: Text.Wrap
            }
        }

        Flow {
            Layout.fillWidth: true
            spacing: 4
            visible: kind === "text" || kind === "idle"
            Repeater {
                model: hasCtrl ? viewerController.commandHotkeys : []
                delegate: Rectangle {
                    required property var modelData
                    visible: modelData && modelData.secondary === true
                    radius: 4
                    color: bgElevatedColor
                    border.color: borderMutedColor
                    implicitHeight: chipTxt.implicitHeight + 6
                    implicitWidth: chipTxt.implicitWidth + 12
                    Label {
                        id: chipTxt
                        anchors.centerIn: parent
                        text: (modelData.label || "") + (modelData.key ? (" [" + modelData.key + "]") : "")
                        font.pixelSize: fontXs
                        color: textSecondaryColor
                    }
                }
            }
        }

        Label {
            Layout.fillWidth: true
            visible: hasCtrl && viewerController.commandHintText.length > 0
            text: hasCtrl ? viewerController.commandHintText : ""
            color: textSecondaryColor
            font.pixelSize: fontSm
            wrapMode: Text.Wrap
        }

        StackLayout {
            Layout.fillWidth: true
            currentIndex: {
                if (kind === "direction") return 1
                if (kind === "bool") return 2
                if (kind === "pace") return 3
                if (kind === "int") return 4
                if (kind === "choice") return 5
                if (kind === "move" || kind === "shoot") return 6
                return 0
            }

            ColumnLayout {
                spacing: spacingXs
                TextField {
                    id: cmdTextField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Введите команду…")
                    font.family: monoFontFamily
                    font.pixelSize: monoFontSize
                    onAccepted: if (hasCtrl) viewerController.submitText(text)
                }
                PrimaryButton {
                    text: qsTr("Отправить")
                    hotkeySuffix: "[Enter]"
                    onClicked: if (hasCtrl) viewerController.submitText(cmdTextField.text)
                }
            }

            GridLayout {
                columns: 3
                rowSpacing: 4
                columnSpacing: 4
                Button {
                    text: "↑"
                    Layout.preferredHeight: 34
                    onClicked: if (hasCtrl) viewerController.submitDirection("up")
                }
                Button {
                    text: "←"
                    Layout.preferredHeight: 34
                    onClicked: if (hasCtrl) viewerController.submitDirection("left")
                }
                Button {
                    text: "→"
                    Layout.preferredHeight: 34
                    onClicked: if (hasCtrl) viewerController.submitDirection("right")
                }
                Item { }
                Button {
                    text: "↓"
                    Layout.preferredHeight: 34
                    onClicked: if (hasCtrl) viewerController.submitDirection("down")
                }
                Item { }
                Button {
                    text: qsTr("Нет [0]")
                    Layout.columnSpan: 3
                    Layout.fillWidth: true
                    Layout.preferredHeight: 34
                    onClicked: if (hasCtrl) viewerController.submitDirection("none")
                }
            }

            RowLayout {
                PrimaryButton {
                    text: qsTr("Да")
                    hotkeySuffix: "[Y]"
                    onClicked: if (hasCtrl) viewerController.submitBool(true)
                }
                Button {
                    text: qsTr("Нет [N]")
                    Layout.fillWidth: true
                    Layout.preferredHeight: 34
                    onClicked: if (hasCtrl) viewerController.submitBool(false)
                }
            }

            PrimaryButton {
                text: qsTr("Далее")
                hotkeySuffix: "[Enter]"
                onClicked: if (hasCtrl) viewerController.submitPaceNext()
            }

            RowLayout {
                SpinBox {
                    id: intSpin
                    from: hasCtrl ? viewerController.intSpinMin : 0
                    to: hasCtrl ? viewerController.intSpinMax : 999
                    value: hasCtrl ? viewerController.intSpinValue : 0
                }
                PrimaryButton {
                    text: qsTr("ОК")
                    hotkeySuffix: "[Enter]"
                    Layout.preferredWidth: 120
                    onClicked: if (hasCtrl) viewerController.submitInt(intSpin.value)
                }
            }

            ColumnLayout {
                ComboBox {
                    id: choiceBox
                    Layout.fillWidth: true
                    model: hasCtrl ? viewerController.commandChoices : []
                    textRole: "label"
                }
                PrimaryButton {
                    text: qsTr("ОК")
                    hotkeySuffix: "[Enter]"
                    onClicked: {
                        if (!hasCtrl) return
                        viewerController.submitChoiceAtIndex(choiceBox.currentIndex)
                    }
                }
                Flow {
                    Layout.fillWidth: true
                    spacing: 6
                    Repeater {
                        model: commandLabelModel
                        delegate: Button {
                            required property int index
                            required property string modelData
                            text: modelData
                            onClicked: if (hasCtrl) viewerController.submitChoiceAtIndex(index)
                        }
                    }
                }
            }

            ColumnLayout {
                Label {
                    Layout.fillWidth: true
                    text: kind === "move"
                        ? qsTr("ЛКМ — клетка • ПКМ — идти • Backspace — stay")
                        : qsTr("ПКМ по врагу — Fire • Enter — Shoot • Esc — отмена")
                    color: textSecondaryColor
                    wrapMode: Text.Wrap
                    font.pixelSize: fontSm
                }
            }
        }
    }

    ShootPopover {
        parent: cmdRoot
    }
}
