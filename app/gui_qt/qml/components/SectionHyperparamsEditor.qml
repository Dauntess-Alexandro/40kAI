import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: hpEditor
    required property string algoSection  // dqn | ppo | tree | proxy
    property var rootUi: null

    spacing: rootUi ? rootUi.spacingXs : 6
    Layout.fillWidth: true
    Layout.minimumWidth: Math.round(280 * (rootUi ? rootUi.uiScale : 1))

    property var hpMap: ({})

    function sectionTitle() {
        if (algoSection === "dqn") return "DQN"
        if (algoSection === "ppo") return "PPO"
        if (algoSection === "tree") return "AlphaZero (Tree)"
        if (algoSection === "proxy") return "AlphaZero (Proxy)"
        return algoSection
    }

    function keysList() {
        if (typeof controller === "undefined" || !controller) return []
        if (algoSection === "dqn") return controller.hpDqnHyperparamKeys
        if (algoSection === "ppo") return controller.hpPpoHyperparamKeys
        if (algoSection === "tree") return controller.hpAzHyperparamKeys
        if (algoSection === "proxy") return controller.hpAzHyperparamKeys
        return []
    }

    function refreshMap() {
        if (typeof controller === "undefined" || !controller) {
            hpMap = ({})
            return
        }
        if (algoSection === "dqn") hpMap = controller.hpDqnHyperparamsMap
        else if (algoSection === "ppo") hpMap = controller.hpPpoHyperparamsMap
        else if (algoSection === "tree") hpMap = controller.hpAzTreeHyperparamsMap
        else if (algoSection === "proxy") hpMap = controller.hpAzProxyHyperparamsMap
        else hpMap = ({})
    }

    Component.onCompleted: refreshMap()
    Connections {
        target: typeof controller !== "undefined" ? controller : null
        function onTrainingHyperparamsChanged() { hpEditor.refreshMap() }
    }

    function setKey(key, value) {
        if (typeof controller === "undefined" || !controller) return
        if (algoSection === "dqn") controller.set_dqn_hyperparam(key, value)
        else if (algoSection === "ppo") controller.set_ppo_hyperparam(key, value)
        else if (algoSection === "tree") controller.set_az_tree_hyperparam(key, value)
        else if (algoSection === "proxy") controller.set_az_proxy_hyperparam(key, value)
    }

    function applyProfile(name) {
        if (typeof controller === "undefined" || !controller) return
        if (algoSection === "dqn") controller.apply_dqn_profile(name)
        else if (algoSection === "ppo") controller.apply_ppo_profile(name)
        else if (algoSection === "tree") controller.apply_az_tree_profile(name)
        else if (algoSection === "proxy") controller.apply_az_proxy_profile(name)
    }

    function isIntKey(key) {
        var k = String(key)
        if (k === "lr_scheduler" || k === "c_puct_schedule" || k === "mcts_mode"
                || k === "dist_type" || k === "eps_schedule") return false
        return k.indexOf("_size") >= 0 || k.indexOf("_steps") >= 0 || k.indexOf("_capacity") >= 0
            || k.indexOf("num_") === 0 || k.indexOf("mcts_simulations") >= 0 || k.indexOf("mcts_max_depth") >= 0
            || k.indexOf("mcts_top_k") >= 0 || k.indexOf("hidden_size") >= 0 || k.indexOf("num_layers") >= 0
            || k.indexOf("ensemble") >= 0 || k.indexOf("value_ensemble") >= 0
            || k.indexOf("temperature_opening_moves") >= 0 || k.indexOf("actor_") === 0
            || k.indexOf("sync_") === 0 || k.indexOf("updates_per") >= 0 || k.indexOf("replay_min") >= 0
            || k.indexOf("max_policy") >= 0 || k.indexOf("outcome_only") >= 0
            || k.indexOf("double_dqn") >= 0 || k.indexOf("dueling") >= 0
            || k.indexOf("adaptive_entropy") >= 0 || k.indexOf("noisy_disable") >= 0
            || k.indexOf("noisy_sigma_anneal") >= 0 || k.indexOf("iqn_n_") === 0
            || k.indexOf("rollout") >= 0 || k.indexOf("update_epochs") >= 0
            || k.indexOf("minibatch") >= 0 || k.indexOf("replay_min") >= 0
            || k.indexOf("det_eval") >= 0 || k.indexOf("mcts_eval") >= 0
            || k.indexOf("mcts_root") >= 0 || k.indexOf("snapshot_opp") >= 0
            || k === "batch_size" || k === "updates_per_step" || k === "warmup_steps"
            || k === "eps_decay"
    }

    function isStringKey(key) {
        var k = String(key)
        return k === "lr_scheduler" || k === "c_puct_schedule" || k === "mcts_mode"
            || k === "dist_type" || k === "eps_schedule"
    }

    function presetLabel() {
        if (typeof controller === "undefined" || !controller) return "Custom"
        if (algoSection === "dqn") return controller.hpDqnPresetLabel
        if (algoSection === "ppo") return controller.hpPpoPresetLabel
        if (algoSection === "tree") return controller.hpAzTreePresetLabel
        if (algoSection === "proxy") return controller.hpAzProxyPresetLabel
        return "Custom"
    }

    RowLayout {
        Layout.fillWidth: true
        Label {
            text: sectionTitle()
            font.bold: true
            Layout.fillWidth: true
        }
        Button { text: "Fast"; onClicked: applyProfile("fast") }
        Button { text: "Balanced"; onClicked: applyProfile("balanced") }
        Button { text: "Heavy"; onClicked: applyProfile("heavy") }
    }

    Label {
        text: "Текущий пресет: " + presetLabel()
        color: palette.mid
        Layout.fillWidth: true
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: rootUi ? rootUi.spacingSm : 4

        Repeater {
            model: keysList()

            delegate: RowLayout {
                required property int index
                required property var modelData
                Layout.fillWidth: true

                Label {
                    text: typeof modelData === "string" ? modelData : String(modelData)
                    Layout.preferredWidth: Math.round(200 * (rootUi ? rootUi.uiScale : 1))
                }

                TextField {
                    visible: hpEditor.isStringKey(modelData)
                    readOnly: modelData === "mcts_mode"
                    text: String(hpEditor.hpMap[modelData] ?? "")
                    Layout.fillWidth: true
                    Layout.preferredWidth: Math.round(180 * (rootUi ? rootUi.uiScale : 1))
                    onEditingFinished: if (!readOnly) hpEditor.setKey(modelData, text)
                }

                SpinBox {
                    visible: !hpEditor.isStringKey(modelData) && hpEditor.isIntKey(modelData)
                    from: 0
                    to: 10000000
                    stepSize: 1
                    editable: true
                    value: parseInt(hpEditor.hpMap[modelData] ?? 0)
                    Layout.preferredWidth: Math.round(180 * (rootUi ? rootUi.uiScale : 1))
                    onValueModified: hpEditor.setKey(modelData, value.toString())
                }

                SpinBox {
                    visible: !hpEditor.isStringKey(modelData) && !hpEditor.isIntKey(modelData)
                    from: 0
                    to: 10000000
                    stepSize: 1
                    editable: true
                    property real factor: 1000000
                    value: Math.round(parseFloat(hpEditor.hpMap[modelData] ?? 0) * factor)
                    Layout.preferredWidth: Math.round(180 * (rootUi ? rootUi.uiScale : 1))
                    textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 6) }
                    valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                    onValueModified: hpEditor.setKey(modelData, (value / factor).toString())
                }
            }
        }
    }
}
