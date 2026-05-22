import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: azEditor
    required property string section  // "tree" | "proxy"
    property var rootUi: null

    spacing: rootUi ? rootUi.spacingXs : 6
    Layout.fillWidth: true
    Layout.minimumWidth: Math.round(280 * (rootUi ? rootUi.uiScale : 1))

    property var hpMap: ({})
    function refreshMap() {
        if (typeof controller === "undefined" || controller === null) {
            hpMap = ({})
            return
        }
        hpMap = section === "tree" ? controller.hpAzTreeHyperparamsMap : controller.hpAzProxyHyperparamsMap
    }
    Component.onCompleted: refreshMap()
    Connections {
        target: controller
        function onTrainingHyperparamsChanged() { azEditor.refreshMap() }
    }

    function setKey(key, value) {
        if (!controller) return
        if (section === "tree") controller.set_az_tree_hyperparam(key, value)
        else controller.set_az_proxy_hyperparam(key, value)
    }

    function isIntKey(key) {
        var k = String(key)
        return k.indexOf("_size") >= 0 || k.indexOf("_steps") >= 0 || k.indexOf("_capacity") >= 0
            || k.indexOf("num_") === 0 || k.indexOf("mcts_simulations") >= 0 || k.indexOf("mcts_max_depth") >= 0
            || k.indexOf("mcts_top_k") >= 0 || k.indexOf("hidden_size") >= 0 || k.indexOf("num_layers") >= 0
            || k.indexOf("value_ensemble") >= 0 || k.indexOf("temperature_opening_moves") >= 0
            || k.indexOf("actor_") === 0 || k.indexOf("sync_") === 0 || k.indexOf("updates_per") >= 0
            || k.indexOf("replay_min") >= 0 || k.indexOf("max_policy") >= 0 || k.indexOf("outcome_only") >= 0
            || k.indexOf("mcts_eval_cache") >= 0 || k.indexOf("mcts_root_dirichlet") >= 0
            || k.indexOf("snapshot_opp") >= 0 || k.indexOf("lr_warmup") >= 0 || k.indexOf("lr_total") >= 0
    }

    function isStringKey(key) {
        var k = String(key)
        return k === "lr_scheduler" || k === "c_puct_schedule" || k === "mcts_mode"
    }

    RowLayout {
        Layout.fillWidth: true
        Label {
            text: section === "tree" ? "AlphaZero (Tree)" : "AlphaZero (Proxy)"
            font.bold: true
            Layout.fillWidth: true
        }
        Button {
            text: "Fast"
            onClicked: {
                if (section === "tree") controller.apply_az_tree_profile("fast")
                else controller.apply_az_proxy_profile("fast")
            }
        }
        Button {
            text: "Balanced"
            onClicked: {
                if (section === "tree") controller.apply_az_tree_profile("balanced")
                else controller.apply_az_proxy_profile("balanced")
            }
        }
        Button {
            text: "Heavy"
            onClicked: {
                if (section === "tree") controller.apply_az_tree_profile("heavy")
                else controller.apply_az_proxy_profile("heavy")
            }
        }
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: rootUi ? rootUi.spacingSm : 4

        Repeater {
            model: (typeof controller !== "undefined" && controller) ? controller.hpAzHyperparamKeys : []

            delegate: RowLayout {
                required property int index
                required property string modelData
                Layout.fillWidth: true

                Label {
                    text: modelData
                    Layout.preferredWidth: Math.round(200 * (rootUi ? rootUi.uiScale : 1))
                }

                TextField {
                    visible: azEditor.isStringKey(modelData)
                    readOnly: modelData === "mcts_mode"
                    text: String(azEditor.hpMap[modelData] ?? "")
                    Layout.fillWidth: true
                    Layout.preferredWidth: Math.round(180 * (rootUi ? rootUi.uiScale : 1))
                    onEditingFinished: if (!readOnly) azEditor.setKey(modelData, text)
                }

                SpinBox {
                    visible: !azEditor.isStringKey(modelData) && azEditor.isIntKey(modelData)
                    from: 0
                    to: 10000000
                    stepSize: 1
                    editable: true
                    value: parseInt(azEditor.hpMap[modelData] ?? 0)
                    Layout.preferredWidth: Math.round(180 * (rootUi ? rootUi.uiScale : 1))
                    onValueModified: azEditor.setKey(modelData, value.toString())
                }

                SpinBox {
                    visible: !azEditor.isStringKey(modelData) && !azEditor.isIntKey(modelData)
                    from: 0
                    to: 10000000
                    stepSize: 1
                    editable: true
                    property real factor: 1000000
                    value: Math.round(parseFloat(azEditor.hpMap[modelData] ?? 0) * factor)
                    Layout.preferredWidth: Math.round(180 * (rootUi ? rootUi.uiScale : 1))
                    textFromValue: function(v, locale) { return Number(v / factor).toLocaleString(locale, 'f', 6) }
                    valueFromText: function(t, locale) { return Math.round(Number.fromLocaleString(locale, t) * factor) }
                    onValueModified: azEditor.setKey(modelData, (value / factor).toString())
                }
            }
        }
    }
}
