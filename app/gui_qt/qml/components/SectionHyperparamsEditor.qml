import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: hpEditor
    required property string algoSection  // dqn | ppo | tree | proxy | gmz
    property var rootUi: null

    spacing: rootUi ? rootUi.spacingSm : 8
    Layout.fillWidth: true

    property var hpMap: ({})
    property var defaultsMap: ({})
    property string searchText: ""

    function sectionTitle() {
        if (algoSection === "dqn") return "DQN"
        if (algoSection === "ppo") return "PPO"
        if (algoSection === "tree") return "AlphaZero (Tree)"
        if (algoSection === "proxy") return "AlphaZero (Proxy)"
        if (algoSection === "gmz") return "Gumbel MuZero"
        if (algoSection === "gaz") return "Gumbel AlphaZero"
        return algoSection
    }

    function groupsList() {
        if (typeof controller === "undefined" || !controller) return []
        if (algoSection === "dqn") return controller.hpDqnGroups
        if (algoSection === "ppo") return controller.hpPpoGroups
        if (algoSection === "tree" || algoSection === "proxy") return controller.hpAzGroups
        if (algoSection === "gmz") return controller.hpGmzGroups
        if (algoSection === "gaz") return controller.hpGazGroups
        return []
    }

    function basicKeysList() {
        if (typeof controller === "undefined" || !controller) return []
        if (algoSection === "dqn") return controller.hpDqnBasicKeys
        if (algoSection === "ppo") return controller.hpPpoBasicKeys
        if (algoSection === "tree") return controller.hpAzTreeBasicKeys
        if (algoSection === "proxy") return controller.hpAzProxyBasicKeys
        if (algoSection === "gmz") return controller.hpGmzBasicKeys
        if (algoSection === "gaz") return controller.hpGazBasicKeys
        return []
    }

    function displayGroups() {
        if (typeof controller !== "undefined" && controller && controller.hyperparamsBasicMode) {
            return [{
                "id": "basic",
                "title": "Базовый набор",
                "keys": basicKeysList(),
                "default_collapsed": false
            }]
        }
        return groupsList()
    }

    function refreshMaps() {
        if (typeof controller === "undefined" || !controller) {
            hpMap = ({})
            defaultsMap = ({})
            return
        }
        if (algoSection === "dqn") {
            hpMap = controller.hpDqnHyperparamsMap
            defaultsMap = controller.hpDqnDefaultsMap
        } else if (algoSection === "ppo") {
            hpMap = controller.hpPpoHyperparamsMap
            defaultsMap = controller.hpPpoDefaultsMap
        } else if (algoSection === "tree") {
            hpMap = controller.hpAzTreeHyperparamsMap
            defaultsMap = controller.hpAzTreeDefaultsMap
        } else if (algoSection === "proxy") {
            hpMap = controller.hpAzProxyHyperparamsMap
            defaultsMap = controller.hpAzProxyDefaultsMap
        } else if (algoSection === "gmz") {
            hpMap = controller.hpGmzHyperparamsMap
            defaultsMap = controller.hpGmzDefaultsMap
        } else if (algoSection === "gaz") {
            hpMap = controller.hpGazHyperparamsMap
            defaultsMap = controller.hpGazDefaultsMap
        } else {
            hpMap = ({})
            defaultsMap = ({})
        }
    }

    Component.onCompleted: refreshMaps()
    Connections {
        target: typeof controller !== "undefined" ? controller : null
        function onTrainingHyperparamsChanged() { hpEditor.refreshMaps() }
        function onHyperparamsBasicModeChanged() { hpEditor.refreshMaps() }
        function onTrainingDeviceInfoChanged() { hpEditor.refreshMaps() }
    }

    function setKey(key, value) {
        if (typeof controller === "undefined" || !controller) return
        if (algoSection === "dqn") controller.set_dqn_hyperparam(key, value)
        else if (algoSection === "ppo") controller.set_ppo_hyperparam(key, value)
        else if (algoSection === "tree") controller.set_az_tree_hyperparam(key, value)
        else if (algoSection === "proxy") controller.set_az_proxy_hyperparam(key, value)
        else if (algoSection === "gmz") controller.set_gmz_hyperparam(key, value)
        else if (algoSection === "gaz") controller.set_gaz_hyperparam(key, value)
    }

    function applyProfile(name) {
        if (typeof controller === "undefined" || !controller) return
        if (algoSection === "dqn") controller.apply_dqn_profile(name)
        else if (algoSection === "ppo") controller.apply_ppo_profile(name)
        else if (algoSection === "tree") controller.apply_az_tree_profile(name)
        else if (algoSection === "proxy") controller.apply_az_proxy_profile(name)
        else if (algoSection === "gmz") controller.apply_gmz_profile(name)
        else if (algoSection === "gaz") controller.apply_gaz_profile(name)
    }

    function presetLabel() {
        if (typeof controller === "undefined" || !controller) return "Custom"
        if (algoSection === "dqn") return controller.hpDqnPresetLabel
        if (algoSection === "ppo") return controller.hpPpoPresetLabel
        if (algoSection === "tree") return controller.hpAzTreePresetLabel
        if (algoSection === "proxy") return controller.hpAzProxyPresetLabel
        if (algoSection === "gmz") return controller.hpGmzPresetLabel
        if (algoSection === "gaz") return controller.hpGazPresetLabel
        return "Custom"
    }

    function presetKey() {
        var label = presetLabel()
        if (label === "Fast") return "fast"
        if (label === "Balanced") return "balanced"
        if (label === "Heavy") return "heavy"
        if (label === "Very Heavy") return "very_heavy"
        return "custom"
    }

    function presetColor() {
        return presetColorFor(presetKey())
    }

    function presetColorFor(name) {
        if (name === "fast") return "#2980b9"
        if (name === "balanced") return "#27ae60"
        if (name === "heavy") return "#e67e22"
        if (name === "very_heavy") return "#c0392b"
        return "#7f8c8d"
    }

    function presetLabelRu(name) {
        if (name === "fast") return "Fast"
        if (name === "balanced") return "Balanced"
        if (name === "heavy") return "Heavy"
        if (name === "very_heavy") return "Very Heavy"
        return "Custom"
    }

    function profilePreviewText(name) {
        if (typeof controller === "undefined" || !controller) return ""
        return controller.get_profile_preview_tooltip(hpEditor.algoSection, name)
    }

    function mutedColor() {
        return rootUi ? rootUi.uiTextMuted : "#9aa0a6"
    }

    function tooltipFor(key) {
        if (typeof controller === "undefined" || !controller) return ""
        var tips
        if (algoSection === "dqn") tips = controller.hpDqnFieldTooltips
        else if (algoSection === "ppo") tips = controller.hpPpoFieldTooltips
        else if (algoSection === "tree" || algoSection === "proxy") tips = controller.hpAzFieldTooltips
        else if (algoSection === "gmz") tips = controller.hpGmzFieldTooltips
        else if (algoSection === "gaz") tips = controller.hpGazFieldTooltips
        else return ""
        if (!tips) return ""
        var base = String(tips[key] ?? "")
        var raw = String(hpMap[key] ?? "")
        var cudaSuffix = controller.hyperparam_cuda_tooltip_suffix(algoSection, key, raw)
        return base + cudaSuffix
    }

    function cudaFieldState(key) {
        if (typeof controller === "undefined" || !controller) return 0
        return controller.hyperparam_cuda_field_state(
            hpEditor.algoSection, key, String(hpMap[key] ?? ""))
    }

    function cudaRowColor(key) {
        var st = cudaFieldState(key)
        if (st === 1) return Qt.rgba(0.22, 0.72, 0.45, 0.14)
        if (st === 2) return Qt.rgba(0.85, 0.28, 0.22, 0.16)
        return "transparent"
    }

    function cudaRowBorderColor(key) {
        var st = cudaFieldState(key)
        if (st === 1) return Qt.rgba(0.35, 0.85, 0.55, 0.55)
        if (st === 2) return Qt.rgba(0.92, 0.35, 0.28, 0.65)
        return "transparent"
    }

    function valuesEqual(a, b) {
        if (typeof a === "number" && typeof b === "number")
            return Math.abs(a - b) < 1e-9
        return String(a) === String(b)
    }

    function isModified(key) {
        return !valuesEqual(hpMap[key], defaultsMap[key])
    }

    function keyMatchesSearch(key) {
        if (!searchText || searchText.length === 0) return true
        return String(key).toLowerCase().indexOf(searchText) >= 0
    }

    function groupHasVisibleFields(keys) {
        if (!keys || keys.length === 0) return false
        for (var i = 0; i < keys.length; ++i) {
            if (keyMatchesSearch(keys[i])) return true
        }
        return false
    }

    function isIntKey(key) {
        var k = String(key)
        if (isStringKey(k)) return false
        return k.indexOf("_size") >= 0 || k.indexOf("_steps") >= 0 || k.indexOf("_capacity") >= 0
            || k.indexOf("num_") === 0 || k.indexOf("mcts_simulations") >= 0 || k.indexOf("mcts_max_depth") >= 0
            || k.indexOf("mcts_top_k") >= 0 || k.indexOf("hidden_size") >= 0 || k.indexOf("hidden_dim") >= 0
            || k.indexOf("latent_dim") >= 0 || k.indexOf("num_layers") >= 0
            || k.indexOf("ensemble") >= 0 || k.indexOf("value_ensemble") >= 0
            || k.indexOf("temperature_opening_moves") >= 0
            || k === "actor_batch_send" || k === "actor_queue_max" || k === "actor_max_cuda"
            || k === "actor_compile" || k === "learner_compile"
            || k.indexOf("sync_") === 0 || k.indexOf("updates_per") >= 0 || k.indexOf("replay_min") >= 0
            || k.indexOf("max_policy") >= 0 || k.indexOf("outcome_only") >= 0
            || k.indexOf("double_dqn") >= 0 || k.indexOf("dueling") >= 0
            || k.indexOf("adaptive_entropy") >= 0 || k.indexOf("noisy_disable") >= 0
            || k.indexOf("noisy_sigma_anneal") >= 0 || k.indexOf("iqn_n_") === 0
            || k.indexOf("rollout") >= 0 || k.indexOf("update_epochs") >= 0
            || k.indexOf("minibatch") >= 0
            || k.indexOf("det_eval") >= 0 || k.indexOf("mcts_eval") >= 0
            || k.indexOf("mcts_root") >= 0 || k.indexOf("snapshot_opp") >= 0
            || k === "batch_size" || k === "updates_per_step" || k === "warmup_steps"
            || k === "eps_decay" || k === "root_top_k" || k === "unroll_steps"
            || k.indexOf("action_embed") >= 0
    }

    function isStringKey(key) {
        var k = String(key)
        return k === "lr_scheduler" || k === "c_puct_schedule" || k === "mcts_mode"
            || k === "dist_type" || k === "eps_schedule"
            || k === "actor_device" || k === "atom_range"
    }

    Label {
        text: sectionTitle()
        font.bold: true
        font.pixelSize: rootUi ? Math.round(15 * rootUi.uiScale) : 15
        Layout.fillWidth: true
    }

    RowLayout {
        Layout.fillWidth: true
        spacing: rootUi ? rootUi.spacingSm : 8

        Label {
            text: "Пресеты"
            color: mutedColor()
            font.pixelSize: rootUi ? Math.round(11 * rootUi.uiScale) : 11
            Layout.alignment: Qt.AlignVCenter
        }

        Rectangle {
            Layout.fillWidth: true
            implicitHeight: presetBarRow.implicitHeight + 8
            radius: 8
            color: Qt.rgba(1, 1, 1, 0.04)
            border.color: Qt.rgba(1, 1, 1, 0.14)
            border.width: 1

            RowLayout {
                id: presetBarRow
                anchors.fill: parent
                anchors.margins: 4
                spacing: 4

                Repeater {
                    model: hpEditor.algoSection === "gmz"
                           ? ["fast", "balanced", "heavy", "very_heavy"]
                           : ["fast", "balanced", "heavy"]

                    delegate: Button {
                        id: presetBtn
                        required property string modelData
                        text: presetLabelRu(modelData)
                        flat: true
                        property bool isActive: hpEditor.presetKey() === modelData
                        implicitHeight: 30
                        implicitWidth: Math.max(72, implicitContentWidth + 20)

                        background: Rectangle {
                            radius: 6
                            color: {
                                if (presetBtn.isActive) return hpEditor.presetColorFor(modelData)
                                if (presetBtn.hovered) return Qt.rgba(1, 1, 1, 0.1)
                                return "transparent"
                            }
                            border.color: presetBtn.isActive ? presetBtn.palette.highlight : Qt.rgba(1, 1, 1, 0.18)
                            border.width: presetBtn.isActive ? 0 : 1
                        }

                        contentItem: Text {
                            text: presetBtn.text
                            font.bold: presetBtn.isActive
                            color: presetBtn.isActive ? "white" : (presetBtn.hovered ? "#e8eaed" : mutedColor())
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        ToolTip.visible: hovered
                        ToolTip.delay: 250
                        ToolTip.timeout: 12000
                        ToolTip.text: hpEditor.profilePreviewText(modelData)

                        onClicked: hpEditor.applyProfile(modelData)
                    }
                }
            }
        }

        RowLayout {
            spacing: 4
            visible: presetKey() === "custom"
            Layout.alignment: Qt.AlignVCenter

            Label {
                text: "сейчас"
                color: mutedColor()
                font.pixelSize: rootUi ? Math.round(10 * rootUi.uiScale) : 10
            }
            Rectangle {
                radius: 8
                color: presetColor()
                implicitHeight: 22
                implicitWidth: customChipLabel.implicitWidth + 14
                Label {
                    id: customChipLabel
                    anchors.centerIn: parent
                    text: "Custom"
                    color: "white"
                    font.bold: true
                    font.pixelSize: rootUi ? Math.round(10 * rootUi.uiScale) : 10
                }
            }
        }
    }

    TextField {
        Layout.fillWidth: true
        placeholderText: "Поиск поля…"
        onTextChanged: hpEditor.searchText = text.trim().toLowerCase()
    }

    Repeater {
        id: groupsRepeater
        model: {
            if (typeof controller === "undefined" || !controller) return []
            if (controller.hyperparamsBasicMode) {
                return [{
                    "id": "basic",
                    "title": "Базовый набор",
                    "keys": basicKeysList(),
                    "default_collapsed": false
                }]
            }
            return groupsList()
        }

        delegate: Frame {
            id: groupFrame
            required property int index
            required property var modelData
            Layout.fillWidth: true
            padding: rootUi ? rootUi.spacingXs : 4
            visible: hpEditor.groupHasVisibleFields(modelData.keys)

            property bool expanded: modelData.id === "basic" ? true : !(modelData.default_collapsed)

            background: Rectangle {
                color: Qt.rgba(1, 1, 1, 0.03)
                border.color: Qt.rgba(1, 1, 1, 0.08)
                radius: 6
            }

            ColumnLayout {
                anchors.fill: parent
                spacing: rootUi ? rootUi.spacingXs : 4

                RowLayout {
                    Layout.fillWidth: true
                    ToolButton {
                        text: groupFrame.expanded ? "▼" : "▶"
                        onClicked: groupFrame.expanded = !groupFrame.expanded
                    }
                    Label {
                        text: modelData.title
                        font.bold: true
                        Layout.fillWidth: true
                    }
                    ToolButton {
                        visible: modelData.id !== "basic"
                        text: "↺"
                        ToolTip.visible: hovered
                        ToolTip.text: "Сбросить группу к значениям по умолчанию"
                        onClicked: {
                            if (typeof controller !== "undefined" && controller)
                                controller.reset_algo_group(hpEditor.algoSection, modelData.id)
                        }
                    }
                }

                ColumnLayout {
                    visible: groupFrame.expanded
                    Layout.fillWidth: true
                    spacing: rootUi ? rootUi.spacingXs : 2

                    Repeater {
                        model: modelData.keys

                        delegate: Rectangle {
                            required property int index
                            required property var modelData
                            property string fieldKey: typeof modelData === "string" ? modelData : String(modelData)
                            Layout.fillWidth: true
                            Layout.maximumWidth: groupFrame.width - 16
                            implicitHeight: fieldRow.implicitHeight + 6
                            radius: 4
                            color: hpEditor.cudaRowColor(fieldKey)
                            border.color: hpEditor.cudaRowBorderColor(fieldKey)
                            border.width: hpEditor.cudaFieldState(fieldKey) === 0 ? 0 : 1
                            visible: hpEditor.keyMatchesSearch(fieldKey)

                            RowLayout {
                                id: fieldRow
                                anchors.fill: parent
                                anchors.margins: 3
                                spacing: rootUi ? rootUi.spacingSm : 8

                                Label {
                                    text: fieldKey
                                    Layout.preferredWidth: Math.round(210 * (rootUi ? rootUi.uiScale : 1))
                                    Layout.maximumWidth: Layout.preferredWidth
                                    elide: Text.ElideRight
                                    color: {
                                        var st = hpEditor.cudaFieldState(fieldKey)
                                        if (st === 1) return "#3ecf8e"
                                        if (st === 2) return "#e07a52"
                                        return mutedColor()
                                    }
                                    font.pixelSize: rootUi ? Math.round(12 * rootUi.uiScale) : 12
                                }

                                Rectangle {
                                    width: 6
                                    height: 6
                                    radius: 3
                                    color: "#f0b400"
                                    visible: hpEditor.isModified(fieldKey)
                                    ToolTip.visible: modifiedDotArea.containsMouse
                                    ToolTip.text: "Отличается от дефолта"

                                    MouseArea {
                                        id: modifiedDotArea
                                        anchors.fill: parent
                                        hoverEnabled: true
                                    }
                                }

                                TextField {
                                    visible: hpEditor.isStringKey(fieldKey)
                                    readOnly: fieldKey === "mcts_mode"
                                    text: String(hpEditor.hpMap[fieldKey] ?? "")
                                    Layout.preferredWidth: Math.round(168 * (rootUi ? rootUi.uiScale : 1))
                                    Layout.maximumWidth: Math.round(220 * (rootUi ? rootUi.uiScale : 1))
                                    horizontalAlignment: Text.AlignRight
                                    onEditingFinished: if (!readOnly) hpEditor.setKey(fieldKey, text)
                                    ToolTip.visible: hovered && hpEditor.tooltipFor(fieldKey).length > 0
                                    ToolTip.text: hpEditor.tooltipFor(fieldKey)
                                }

                                SpinBox {
                                    visible: !hpEditor.isStringKey(fieldKey) && hpEditor.isIntKey(fieldKey)
                                    from: 0
                                    to: 10000000
                                    stepSize: 1
                                    editable: true
                                    value: parseInt(hpEditor.hpMap[fieldKey] ?? 0)
                                    Layout.preferredWidth: Math.round(168 * (rootUi ? rootUi.uiScale : 1))
                                    Layout.maximumWidth: Math.round(220 * (rootUi ? rootUi.uiScale : 1))
                                    onValueModified: hpEditor.setKey(fieldKey, value.toString())
                                    ToolTip.visible: hovered && hpEditor.tooltipFor(fieldKey).length > 0
                                    ToolTip.text: hpEditor.tooltipFor(fieldKey)
                                }

                                SpinBox {
                                    visible: !hpEditor.isStringKey(fieldKey) && !hpEditor.isIntKey(fieldKey)
                                    from: 0
                                    to: 10000000
                                    stepSize: 1
                                    editable: true
                                    property real factor: 1000000
                                    value: Math.round(parseFloat(hpEditor.hpMap[fieldKey] ?? 0) * factor)
                                    Layout.preferredWidth: Math.round(168 * (rootUi ? rootUi.uiScale : 1))
                                    Layout.maximumWidth: Math.round(220 * (rootUi ? rootUi.uiScale : 1))
                                    textFromValue: function(v, locale) {
                                        return Number(v / factor).toLocaleString(locale, "f", 6)
                                    }
                                    valueFromText: function(t, locale) {
                                        return Math.round(Number.fromLocaleString(locale, t) * factor)
                                    }
                                    onValueModified: hpEditor.setKey(fieldKey, (value / factor).toString())
                                    ToolTip.visible: hovered && hpEditor.tooltipFor(fieldKey).length > 0
                                    ToolTip.text: hpEditor.tooltipFor(fieldKey)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
