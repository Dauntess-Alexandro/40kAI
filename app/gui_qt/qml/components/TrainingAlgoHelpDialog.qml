import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dlg

    property var rootUi: null
    property string initialAlgo: ""

    property real uiScale: rootUi ? rootUi.uiScale : 1.0
    property color textMain: rootUi ? rootUi.uiTextMain : "#d7dde7"
    property color textMuted: rootUi ? rootUi.uiTextMuted : "#98a4b8"
    property int radiusMd: rootUi ? rootUi.radiusMd : 10
    property int spacingSm: rootUi ? rootUi.spacingSm : 8
    property int spacingMd: rootUi ? rootUi.spacingMd : 12

    readonly property var algoColors: ["#2563eb", "#0d9488", "#7c3aed", "#6366f1", "#d97706", "#0891b2"]
    readonly property var algoTabNames: ["DQN", "PPO", "AZ Tree", "AZ Proxy", "GMZ", "GAZ"]

    readonly property var dqnBadges: [
        { text: "Классика+",     bg: "#dbeafe", fg: "#1e40af" },
        { text: "Надёжный",      bg: "#e0e7ff", fg: "#3730a3" },
        { text: "Средний train", bg: "#dbeafe", fg: "#1e40af" },
        { text: "Q-оценки",      bg: "#e0e7ff", fg: "#3730a3" }
    ]
    readonly property var ppoBadges: [
        { text: "Рабочий дефолт", bg: "#ccfbf1", fg: "#115e59" },
        { text: "Стабильный",     bg: "#99f6e4", fg: "#134e4a" },
        { text: "Быстрый train",  bg: "#ccfbf1", fg: "#115e59" },
        { text: "Policy-RL",      bg: "#99f6e4", fg: "#134e4a" }
    ]
    readonly property var azTreeBadges: [
        { text: "Тактика+",                bg: "#ede9fe", fg: "#5b21b6" },
        { text: "Качество",                bg: "#ddd6fe", fg: "#4c1d95" },
        { text: "Super Very Compute-heavy",bg: "#ede9fe", fg: "#5b21b6" },
        { text: "MCTS",                    bg: "#ddd6fe", fg: "#4c1d95" }
    ]
    readonly property var azProxyBadges: [
        { text: "Тактика",       bg: "#e0e7ff", fg: "#3730a3" },
        { text: "Лёгкий MCTS",   bg: "#c7d2fe", fg: "#312e81" },
        { text: "Compute-light", bg: "#e0e7ff", fg: "#3730a3" },
        { text: "Proxy-поиск",   bg: "#c7d2fe", fg: "#312e81" }
    ]
    readonly property var gmzBadges: [
        { text: "Топ Качество",       bg: "#fef3c7", fg: "#92400e" },
        { text: "Тяжёлый режим",      bg: "#fde68a", fg: "#78350f" },
        { text: "Very Compute-heavy", bg: "#fef3c7", fg: "#92400e" },
        { text: "Search+",            bg: "#fde68a", fg: "#78350f" }
    ]
    readonly property var gazBadges: [
        { text: "Gumbel-план",    bg: "#cffafe", fg: "#155e75" },
        { text: "Малый бюджет",   bg: "#a5f3fc", fg: "#164e63" },
        { text: "Depth-1",        bg: "#cffafe", fg: "#155e75" },
        { text: "Policy-improve", bg: "#a5f3fc", fg: "#164e63" }
    ]

    readonly property var dqnSections: [
        { icon: "ⓘ", title: "Что это",
          text: "ИИ, который учится понимать, какой ход выгоднее в текущей ситуации. Для каждого действия он оценивает ожидаемую пользу и выбирает лучший вариант." },
        { icon: "▶", title: "Как учится",
          text: "Запоминает прошлые ситуации (состояние, действие, результат), потом на этих данных постепенно улучшает оценки действий. Со временем реже ошибается и лучше выбирает ходы в похожих сценариях." },
        { icon: "✓", title: "Сильные стороны",
          text: "• понятная логика выбора хода;\n• хорошее качество игры после обучения;\n• удобно сравнивать с PPO/AZ/GMZ;\n• обычно предсказуемое поведение в повторяющихся ситуациях;\n• подходит как надёжный базовый агент для тестов и долгих прогонов." },
        { icon: "⚠", title: "Ограничения",
          text: "• может учиться дольше PPO;\n• чувствителен к настройкам;\n• требует больше вычислений при тренировке;\n• качество сильно зависит от того, насколько удачно подобраны гиперпараметры;\n• в очень сложной тактике может хуже справляться, чем модели с полноценным поиском (MCTS/Search)." },
        { icon: "★", title: "Когда выбирать",
          text: "Когда нужен надёжный агент с понятным поведением и есть готовность подождать обучение ради качества итоговой модели." }
    ]
    readonly property var ppoSections: [
        { icon: "ⓘ", title: "Что это",
          text: "ИИ, который учится напрямую улучшать стратегию выбора действий. Он не просто оценивает отдельные ходы, а постепенно делает всю политику игры более качественной." },
        { icon: "▶", title: "Как учится",
          text: "Играет серии шагов (rollout), оценивает, какие решения были полезными, и обновляет стратегию небольшими безопасными шагами, чтобы не ломать уже выученное поведение." },
        { icon: "✓", title: "Сильные стороны",
          text: "• обычно стабильно обучается;\n• хороший баланс между скоростью обучения и качеством;\n• удобен как рабочий режим по умолчанию;\n• часто быстрее и предсказуемее в настройке, чем сложные search-модели;\n• подходит для длительных тренировок без сильных скачков поведения." },
        { icon: "⚠", title: "Ограничения",
          text: "• не использует поиск по дереву на каждом ходе;\n• в сложной тактике может уступать AZ/GMZ с MCTS/Search;\n• качество зависит от rollout/epoch/minibatch настроек;\n• иногда требует тонкой подстройки коэффициентов (clip, entropy, value loss)." },
        { icon: "★", title: "Когда выбирать",
          text: "Когда нужен надёжный универсальный агент с хорошим балансом скорость обучения / качество игры." }
    ]
    readonly property var azTreeSections: [
        { icon: "ⓘ", title: "Что это",
          text: "ИИ с настоящим поиском по дереву (MCTS): нейросеть даёт приоритеты и оценку позиции, а поиск прокручивает варианты вперёд (число симуляций и глубина реально влияют на силу хода)." },
        { icon: "▶", title: "Как учится",
          text: "Self-play: акторы играют партии, в позициях используется MCTS, сеть учится предсказывать политику и value так, как если бы играла с этим поиском." },
        { icon: "✓", title: "Сильные стороны",
          text: "• максимальная сила среди вариантов AZ в проекте;\n• лучше видит последствия на несколько ходов;\n• при росте mcts_simulations / mcts_max_depth обычно заметно крепче;\n• лучший выбор для eval/viewer, если важна сила, а не скорость хода." },
        { icon: "⚠", title: "Ограничения",
          text: "• самый тяжёлый AZ по CPU/GPU на каждом ходу;\n• чувствителен к search-настройкам (mcts_simulations, c_puct, mcts_max_depth, temperature);\n• при малом бюджете поиска преимущество над PPO/DQN может быть неочевидным." },
        { icon: "◆", title: "Режимы инференса",
          text: "• MCTS — рекомендуемый режим по умолчанию: сильнее, но медленнее;\n• Greedy — один проход сети, быстрый baseline без MCTS." },
        { icon: "✦", title: "Температура",
          text: "Только в режиме MCTS (в Greedy не используется)." },
        { icon: "★", title: "Когда выбирать",
          text: "Когда приоритет — качество решений и сила игры, есть ресурсы на обучение и на медленный инференс." }
    ]
    readonly property var azProxySections: [
        { icon: "ⓘ", title: "Что это",
          text: "То же семейство AlphaZero (policy + value, self-play, replay), но на ходу поиск упрощён: вместо полного MCTS — один проход сети и шум Dirichlet в корне. Компромисс «обучаемся как AZ, играем быстрее»." },
        { icon: "▶", title: "Как учится",
          text: "Так же через self-play и replay, но в акторах используется proxy-режим поиска (не разворачивается полное дерево, как в Tree)." },
        { icon: "✓", title: "Сильные стороны",
          text: "• быстрее Tree на инференсе и при большом числе акторов;\n• проще тюнить, если не хочется возиться с sims×depth;\n• удобен для длинных прогонов self-play, когда MCTS на каждом шаге слишком дорог;\n• промежуточный вариант между PPO и AZ Tree." },
        { icon: "⚠", title: "Ограничения",
          text: "• потолок силы ниже, чем у AZ Tree с нормальным MCTS;\n• mcts_simulations в Proxy не разворачивает полное дерево — на силу хода влияют сеть, mcts_top_k, Dirichlet, temperature;\n• для максимальной силы в Viewer обычно лучше Tree или GMZ." },
        { icon: "◆", title: "Режимы инференса",
          text: "• MCTS/Search — рекомендуемый режим по умолчанию, обычно сильнее Greedy;\n• Greedy — быстро, без search;\n• у Proxy это не полный Tree-MCTS: поведение ближе к search-lite." },
        { icon: "✦", title: "Температура",
          text: "Как у AZ: влияет в search-режиме, в Greedy — нет." },
        { icon: "★", title: "Когда выбирать",
          text: "Когда нужен пайплайн AlphaZero, но важнее скорость self-play / хода, чем абсолютный максимум тактики. Для «лучшего бота в турнире» — чаще Tree или GMZ." }
    ]
    readonly property var gmzSections: [
        { icon: "ⓘ", title: "Что это",
          text: "ИИ с поиском, который дополнительно использует внутреннюю модель динамики. Он не только выбирает ход, но и внутри модели проигрывает возможное будущее." },
        { icon: "▶", title: "Как учится",
          text: "Через self-play и unroll-обучение: representation/dynamics/prediction блоки совместно учатся лучше моделировать состояние, последствия действий и полезность решений." },
        { icon: "✓", title: "Сильные стороны",
          text: "• высокий потолок качества игры;\n• хорошо работает в сложных и длинных тактических сценариях;\n• search-режим часто даёт сильные решения в eval/viewer;\n• мощный инструмент, когда цель — выжать максимум качества." },
        { icon: "⚠", title: "Ограничения",
          text: "• самый тяжёлый режим по вычислениям;\n• дольше тренируется и сложнее в тюнинге;\n• чувствителен к параметрам search/replay/unroll;\n• при малом compute может не раскрывать потенциал полностью." },
        { icon: "◆", title: "Режимы инференса",
          text: "• Search — рекомендуемый режим по умолчанию: сильнее, но медленнее;\n• Greedy — быстрее, без search, для baseline/smoke-тестов." },
        { icon: "✦", title: "Температура",
          text: "Влияет только в Search (в Greedy не используется)." },
        { icon: "★", title: "Когда выбирать",
          text: "Когда нужен максимум силы модели и есть бюджет по времени/ресурсам для обучения и оценки." }
    ]
    readonly property var gazSections: [
        { icon: "ⓘ", title: "Что это",
          text: "AlphaZero с Gumbel-планированием: в корне берётся набор кандидатов (Gumbel top-k), Sequential Halving распределяет бюджет симуляций, а completed-Q даёт цель политики. Реальная модель среды (как у AlphaZero), без выученной динамики MuZero. Поиск — depth-1 (один ход вперёд + ответ врага)." },
        { icon: "▶", title: "Как учится",
          text: "Self-play тем же конвейером, что AlphaZero (replay, value/policy, чекпойнты). Отличается только бэкенд поиска у актёра: per-head Gumbel top-k + Sequential Halving вместо PUCT-MCTS." },
        { icon: "✓", title: "Сильные стороны",
          text: "• гарантирует улучшение политики даже при крошечном бюджете симуляций (16–64);\n• дешевле полного MCTS на ход;\n• сеть и чекпойнты полностью совместимы с AlphaZero;\n• в eval/play/Viewer теперь по умолчанию используется Search;\n• удобен для LAN/распределёнки (depth-1, мало симуляций)." },
        { icon: "⚠", title: "Ограничения",
          text: "• поиск только на 1 ход вперёд (depth-1, root-only), без глубокого дерева как у AZ Tree — это осознанный выбор режима, а не недоделка (глубже — отдельные будущие варианты за тем же алгоритмом);\n• при детерминированном ходе врага рост num_simulations почти не влияет — главный рычаг m (num_considered_actions);\n• потолок тактики ниже, чем у полного AZ Tree с большим MCTS." },
        { icon: "◆", title: "Режимы инференса",
          text: "• Search — Gumbel AlphaZero-поиск на инференсе, рекомендуемый режим по умолчанию;\n• Greedy — один проход сети без поиска, быстрее, но обычно слабее." },
        { icon: "✦", title: "Температура",
          text: "На дебюте ход сэмплится из улучшённой политики; дальше — детерминированный победитель Sequential Halving." },
        { icon: "★", title: "Когда выбирать",
          text: "Когда нужен AlphaZero-пайплайн с гарантией улучшения при малом бюджете поиска — особенно под LAN/распределённое self-play." }
    ]

    title: "Подсказка по моделям обучения"
    modal: true
    width: rootUi ? rootUi.dialogWidthXl : 900
    height: Math.round(720 * uiScale)
    anchors.centerIn: Overlay.overlay

    function tabIndexForAlgo(algo) {
        var a = String(algo || "")
        if (a === "ppo") return 1
        if (a === "alphazero_tree") return 2
        if (a === "alphazero_proxy") return 3
        if (a === "gumbel_muzero") return 4
        if (a === "gumbel_az") return 5
        return 0
    }

    onOpened: helpTabBar.currentIndex = tabIndexForAlgo(initialAlgo)

    contentItem: ColumnLayout {
        spacing: dlg.spacingSm

        RowLayout {
            Layout.fillWidth: true
            spacing: dlg.spacingSm

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: summarySpeedColumn.implicitHeight + Math.round(16 * dlg.uiScale)
                radius: dlg.radiusMd
                color: Qt.rgba(0.18, 0.45, 0.95, 0.12)
                border.color: Qt.rgba(0.35, 0.55, 0.95, 0.35)
                border.width: 1

                ColumnLayout {
                    id: summarySpeedColumn
                    anchors.fill: parent
                    anchors.margins: Math.round(10 * dlg.uiScale)
                    spacing: Math.round(4 * dlg.uiScale)

                    Label {
                        text: "Скорость и простота"
                        font.bold: true
                        font.pixelSize: Math.round(13 * dlg.uiScale)
                        color: "#93c5fd"
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    Label {
                        text: "DQN · PPO — быстрые итерации, удобный старт обучения."
                        wrapMode: Text.WordWrap
                        color: dlg.textMuted
                        Layout.fillWidth: true
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: summaryQualityColumn.implicitHeight + Math.round(16 * dlg.uiScale)
                radius: dlg.radiusMd
                color: Qt.rgba(0.55, 0.35, 0.95, 0.12)
                border.color: Qt.rgba(0.65, 0.45, 0.95, 0.35)
                border.width: 1

                ColumnLayout {
                    id: summaryQualityColumn
                    anchors.fill: parent
                    anchors.margins: Math.round(10 * dlg.uiScale)
                    spacing: Math.round(4 * dlg.uiScale)

                    Label {
                        text: "Качество и поиск"
                        font.bold: true
                        font.pixelSize: Math.round(13 * dlg.uiScale)
                        color: "#c4b5fd"
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    Label {
                        text: "AZ Tree · GMZ — просчёт вперёд, дороже по времени.\nAZ Proxy — self-play без полного MCTS, быстрее ход."
                        wrapMode: Text.WordWrap
                        color: dlg.textMuted
                        Layout.fillWidth: true
                    }
                }
            }
        }

        TabBar {
            id: helpTabBar
            Layout.fillWidth: true

            AlgoHelpTabButton { text: "DQN";       accentColor: dlg.algoColors[0]; rootUi: dlg.rootUi }
            AlgoHelpTabButton { text: "PPO";       accentColor: dlg.algoColors[1]; rootUi: dlg.rootUi }
            AlgoHelpTabButton { text: "AZ Tree";   accentColor: dlg.algoColors[2]; rootUi: dlg.rootUi }
            AlgoHelpTabButton { text: "AZ Proxy";  accentColor: dlg.algoColors[3]; rootUi: dlg.rootUi }
            AlgoHelpTabButton { text: "GMZ";       accentColor: dlg.algoColors[4]; rootUi: dlg.rootUi }
            AlgoHelpTabButton { text: "GAZ";       accentColor: dlg.algoColors[5]; rootUi: dlg.rootUi }
            AlgoHelpTabButton { text: "Сравнение"; accentColor: "#9ca3af";          rootUi: dlg.rootUi }
        }

        StackLayout {
            id: helpStack
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: helpTabBar.currentIndex

            ScrollView {
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                AlgoHelpCard {
                    width: helpStack.width
                    rootUi: dlg.rootUi
                    algoTitle: "DQN (Deep Q-Network)"
                    tldr: "Off-policy value-агент без поиска. Быстрый старт, надёжный базовый бот."
                    accentColor: dlg.algoColors[0]
                    badges: dlg.dqnBadges
                    sections: dlg.dqnSections
                }
            }
            ScrollView {
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                AlgoHelpCard {
                    width: helpStack.width
                    rootUi: dlg.rootUi
                    algoTitle: "PPO (Proximal Policy Optimization)"
                    tldr: "On-policy policy-агент. Стабильно учится, удобный дефолт для RL."
                    accentColor: dlg.algoColors[1]
                    badges: dlg.ppoBadges
                    sections: dlg.ppoSections
                }
            }
            ScrollView {
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                AlgoHelpCard {
                    width: helpStack.width
                    rootUi: dlg.rootUi
                    algoTitle: "AlphaZero Tree (AZ Tree)"
                    tldr: "Policy + Value с настоящим MCTS. Сильная тактика, дорогой инференс."
                    accentColor: dlg.algoColors[2]
                    badges: dlg.azTreeBadges
                    sections: dlg.azTreeSections
                }
            }
            ScrollView {
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                AlgoHelpCard {
                    width: helpStack.width
                    rootUi: dlg.rootUi
                    algoTitle: "AlphaZero Proxy (AZ Proxy)"
                    tldr: "Тот же AZ-пайплайн, на ходу без полного дерева. Быстрее, но потолок ниже."
                    accentColor: dlg.algoColors[3]
                    badges: dlg.azProxyBadges
                    sections: dlg.azProxySections
                }
            }
            ScrollView {
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                AlgoHelpCard {
                    width: helpStack.width
                    rootUi: dlg.rootUi
                    algoTitle: "Gumbel MuZero (GMZ)"
                    tldr: "MuZero с Gumbel-поиском и моделью динамики. Потолок качества, самый дорогой режим."
                    accentColor: dlg.algoColors[4]
                    badges: dlg.gmzBadges
                    sections: dlg.gmzSections
                }
            }
            ScrollView {
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                AlgoHelpCard {
                    width: helpStack.width
                    rootUi: dlg.rootUi
                    algoTitle: "Gumbel AlphaZero (GAZ)"
                    tldr: "AlphaZero с Gumbel-планированием (top-k + Sequential Halving, depth-1). Улучшение политики при малом бюджете симуляций."
                    accentColor: dlg.algoColors[5]
                    badges: dlg.gazBadges
                    sections: dlg.gazSections
                }
            }
            ScrollView {
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                AlgoCompareTable {
                    width: helpStack.width
                    rootUi: dlg.rootUi
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Button {
                text: "Закрыть"
                onClicked: dlg.close()
            }
        }
    }
}
