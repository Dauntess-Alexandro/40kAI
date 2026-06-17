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

    readonly property var algoColors: ["#2563eb", "#0d9488", "#7c3aed", "#6366f1", "#d97706", "#be185d", "#0891b2"]
    readonly property var algoTabNames: ["DQN", "PPO", "AZ Tree", "AZ Proxy", "GMZ", "SMZ", "GAZ"]

    // --- стат-бары ---
    readonly property var dqnStats: [
        { label: qsTr("Скорость старта"), value: 4 },
        { label: qsTr("Сила тактики"),    value: 4 },
        { label: qsTr("Цена инференса"),  value: 1 },
        { label: qsTr("Сложность"),       value: 4 }
    ]
    readonly property var ppoStats: [
        { label: qsTr("Скорость старта"), value: 5 },
        { label: qsTr("Сила тактики"),    value: 2 },
        { label: qsTr("Цена инференса"),  value: 1 },
        { label: qsTr("Сложность"),       value: 3 }
    ]
    readonly property var azTreeStats: [
        { label: qsTr("Скорость старта"), value: 2 },
        { label: qsTr("Сила тактики"),    value: 5 },
        { label: qsTr("Цена инференса"),  value: 4 },
        { label: qsTr("Сложность"),       value: 4 }
    ]
    readonly property var azProxyStats: [
        { label: qsTr("Скорость старта"), value: 3 },
        { label: qsTr("Сила тактики"),    value: 3 },
        { label: qsTr("Цена инференса"),  value: 2 },
        { label: qsTr("Сложность"),       value: 3 }
    ]
    readonly property var gmzStats: [
        { label: qsTr("Скорость старта"), value: 1 },
        { label: qsTr("Сила тактики"),    value: 5 },
        { label: qsTr("Цена инференса"),  value: 5 },
        { label: qsTr("Сложность"),       value: 5 }
    ]
    readonly property var smzStats: [
        { label: qsTr("Скорость старта"), value: 2 },
        { label: qsTr("Сила тактики"),    value: 4 },
        { label: qsTr("Цена инференса"),  value: 3 },
        { label: qsTr("Сложность"),       value: 4 }
    ]
    readonly property var gazStats: [
        { label: qsTr("Скорость старта"), value: 2 },
        { label: qsTr("Сила тактики"),    value: 4 },
        { label: qsTr("Цена инференса"),  value: 4 },
        { label: qsTr("Сложность"),       value: 5 }
    ]

    // --- бейджи ---
    readonly property var dqnBadges: [
        { text: qsTr("Rainbow"),     bg: "#dbeafe", fg: "#1e40af" },
        { text: qsTr("IQN + Noisy"), bg: "#e0e7ff", fg: "#3730a3" },
        { text: qsTr("PER + n-step"),bg: "#dbeafe", fg: "#1e40af" },
        { text: qsTr("Q-оценки"),    bg: "#e0e7ff", fg: "#3730a3" }
    ]
    readonly property var ppoBadges: [
        { text: qsTr("Рабочий дефолт"), bg: "#ccfbf1", fg: "#115e59" },
        { text: qsTr("Стабильный"),     bg: "#99f6e4", fg: "#134e4a" },
        { text: qsTr("Быстрый train"),  bg: "#ccfbf1", fg: "#115e59" },
        { text: qsTr("Policy-RL"),      bg: "#99f6e4", fg: "#134e4a" }
    ]
    readonly property var azTreeBadges: [
        { text: qsTr("Тактика+"),                bg: "#ede9fe", fg: "#5b21b6" },
        { text: qsTr("Качество"),                bg: "#ddd6fe", fg: "#4c1d95" },
        { text: qsTr("Super Very Compute-heavy"),bg: "#ede9fe", fg: "#5b21b6" },
        { text: qsTr("MCTS"),                    bg: "#ddd6fe", fg: "#4c1d95" }
    ]
    readonly property var azProxyBadges: [
        { text: qsTr("Тактика"),       bg: "#e0e7ff", fg: "#3730a3" },
        { text: qsTr("Лёгкий MCTS"),   bg: "#c7d2fe", fg: "#312e81" },
        { text: qsTr("Compute-light"), bg: "#e0e7ff", fg: "#3730a3" },
        { text: qsTr("Proxy-поиск"),   bg: "#c7d2fe", fg: "#312e81" }
    ]
    readonly property var gmzBadges: [
        { text: qsTr("Топ Качество"),       bg: "#fef3c7", fg: "#92400e" },
        { text: qsTr("Тяжёлый режим"),      bg: "#fde68a", fg: "#78350f" },
        { text: qsTr("Very Compute-heavy"), bg: "#fef3c7", fg: "#92400e" },
        { text: qsTr("Search+"),            bg: "#fde68a", fg: "#78350f" }
    ]
    readonly property var smzBadges: [
        { text: qsTr("Сэмпл K ходов"),  bg: "#fce7f3", fg: "#831843" },
        { text: qsTr("Joint actions"),   bg: "#fbcfe8", fg: "#9d174d" },
        { text: qsTr("IS-коррекция"),    bg: "#fce7f3", fg: "#831843" },
        { text: qsTr("v1 одна машина"),  bg: "#fbcfe8", fg: "#9d174d" }
    ]
    readonly property var gazBadges: [
        { text: qsTr("Gumbel-план"),    bg: "#cffafe", fg: "#155e75" },
        { text: qsTr("Малый бюджет"),   bg: "#a5f3fc", fg: "#164e63" },
        { text: qsTr("Depth-1"),        bg: "#cffafe", fg: "#155e75" },
        { text: qsTr("Policy-improve"), bg: "#a5f3fc", fg: "#164e63" }
    ]

    // --- секции ---
    readonly property var dqnSections: [
        { icon: "ⓘ", title: qsTr("Что это"),
          text: qsTr("Не «ванильный» DQN, а Rainbow-набор: Double, Dueling, IQN, NoisyNet, n-step, PER. Off-policy value-агент без поиска.") },
        { icon: "▶", title: qsTr("Как учится"),
          text: qsTr("Запоминает прошлые ситуации в приоритетный replay (PER) и обновляет Q-распределение (IQN) с n-step возвратами. NoisyNet вместо ε-жадного exploration.") },
        { icon: "✓", title: qsTr("Сильные стороны"),
          text: qsTr("• сильный baseline без MCTS;\n• IQN даёт более точную оценку действий;\n• NoisyNet — стабильный exploration;\n• дешёвый инференс;\n• удобно сравнивать с PPO/AZ/GMZ.") },
        { icon: "⚠", title: qsTr("Ограничения"),
          text: qsTr("• без поиска может хуже видеть длинную тактику;\n• Rainbow-набор тянет больше настроек, чем чистый DQN;\n• качество сильно зависит от reward shaping.") },
        { icon: "★", title: qsTr("Когда выбирать"),
          text: qsTr("Первый запуск и проверка train/eval-потока — но уже как сильный baseline: часто его одного достаточно без MCTS.") }
    ]
    readonly property var ppoSections: [
        { icon: "ⓘ", title: qsTr("Что это"),
          text: qsTr("ИИ, который учится напрямую улучшать стратегию выбора действий. Не просто оценивает ходы, а делает всю политику более качественной.") },
        { icon: "▶", title: qsTr("Как учится"),
          text: qsTr("Играет серии шагов (rollout), оценивает, какие решения были полезными, и обновляет стратегию небольшими безопасными шагами, чтобы не ломать уже выученное поведение.") },
        { icon: "✓", title: qsTr("Сильные стороны"),
          text: qsTr("• обычно стабильно обучается;\n• хороший баланс скорость/качество;\n• удобен как рабочий режим по умолчанию;\n• быстрее и предсказуемее, чем сложные search-модели;\n• подходит для длительных тренировок без скачков.") },
        { icon: "⚠", title: qsTr("Ограничения"),
          text: qsTr("• не использует поиск по дереву;\n• в сложной тактике может уступать AZ/GMZ;\n• качество зависит от rollout/epoch/minibatch;\n• иногда требует тонкой подстройки (clip, entropy, value loss).") },
        { icon: "★", title: qsTr("Когда выбирать"),
          text: qsTr("Когда нужен on-policy взгляд: посмотреть, как policy-gradient ведёт себя на текущих наградах, и получить независимую от Q-обучения точку сравнения. Быстро запускается и почти не требует тяжёлых настроек.") }
    ]
    readonly property var azTreeSections: [
        { icon: "ⓘ", title: qsTr("Что это"),
          text: qsTr("ИИ с настоящим поиском по дереву (MCTS): нейросеть даёт приоритеты и оценку позиции, а поиск прокручивает варианты вперёд (число симуляций и глубина реально влияют на силу хода).") },
        { icon: "▶", title: qsTr("Как учится"),
          text: qsTr("Self-play: акторы играют партии, в позициях используется MCTS, сеть учится предсказывать политику и value так, как если бы играла с этим поиском.") },
        { icon: "✓", title: qsTr("Сильные стороны"),
          text: qsTr("• максимальная сила среди вариантов AZ;\n• лучше видит последствия на несколько ходов;\n• при росте mcts_simulations / mcts_max_depth заметно крепче;\n• лучший выбор для eval/viewer, если важна сила.") },
        { icon: "⚠", title: qsTr("Ограничения"),
          text: qsTr("• самый тяжёлый AZ по CPU/GPU на каждом ходу;\n• чувствителен к search-настройкам (mcts_simulations, c_puct, mcts_max_depth, temperature);\n• при малом бюджете поиска преимущество неочевидно.") },
        { icon: "◆", title: qsTr("Режимы инференса"),
          text: qsTr("• MCTS — рекомендуемый режим по умолчанию: сильнее, но медленнее;\n• Greedy — один проход сети, быстрый baseline без MCTS.") },
        { icon: "✦", title: qsTr("Температура"),
          text: qsTr("Только в режиме MCTS (в Greedy не используется).") },
        { icon: "★", title: qsTr("Когда выбирать"),
          text: qsTr("Когда приоритет — качество решений и сила игры, есть ресурсы на обучение и на медленный инференс.") }
    ]
    readonly property var azProxySections: [
        { icon: "ⓘ", title: qsTr("Что это"),
          text: qsTr("То же семейство AlphaZero (policy + value, self-play, replay), но на ходу поиск упрощён: вместо полного MCTS — один проход сети и шум Dirichlet в корне.") },
        { icon: "▶", title: qsTr("Как учится"),
          text: qsTr("Так же через self-play и replay, но в акторах используется proxy-режим поиска (не разворачивается полное дерево, как в Tree).") },
        { icon: "✓", title: qsTr("Сильные стороны"),
          text: qsTr("• быстрее Tree на инференсе и при большом числе акторов;\n• проще тюнить, если не хочется возиться с sims×depth;\n• удобен для длинных прогонов self-play;\n• промежуточный вариант между PPO и AZ Tree.") },
        { icon: "⚠", title: qsTr("Ограничения"),
          text: qsTr("• потолок силы ниже, чем у AZ Tree с нормальным MCTS;\n• mcts_simulations в Proxy не разворачивает полное дерево;\n• для максимальной силы в Viewer лучше Tree или GMZ.") },
        { icon: "◆", title: qsTr("Режимы инференса"),
          text: qsTr("• MCTS/Search — рекомендуемый режим по умолчанию;\n• Greedy — быстро, без search;\n• у Proxy это не полный Tree-MCTS: поведение ближе к search-lite.") },
        { icon: "✦", title: qsTr("Температура"),
          text: qsTr("Как у AZ: влияет в search-режиме, в Greedy — нет.") },
        { icon: "★", title: qsTr("Когда выбирать"),
          text: qsTr("Когда нужен пайплайн AlphaZero, но важнее скорость self-play / хода, чем абсолютный максимум тактики.") }
    ]
    readonly property var gmzSections: [
        { icon: "ⓘ", title: qsTr("Что это"),
          text: qsTr("ИИ с поиском, который дополнительно использует внутреннюю модель динамики. Он не только выбирает ход, но и внутри модели проигрывает возможное будущее.") },
        { icon: "▶", title: qsTr("Как учится"),
          text: qsTr("Через self-play и unroll-обучение: representation/dynamics/prediction блоки совместно учатся лучше моделировать состояние, последствия действий и полезность решений.") },
        { icon: "✓", title: qsTr("Сильные стороны"),
          text: qsTr("• высокий потолок качества игры;\n• хорошо работает в сложных и длинных тактических сценариях;\n• search-режим часто даёт сильные решения в eval/viewer;\n• мощный инструмент для максимума качества.") },
        { icon: "⚠", title: qsTr("Ограничения"),
          text: qsTr("• самый тяжёлый режим по вычислениям;\n• дольше тренируется и сложнее в тюнинге;\n• чувствителен к параметрам search/replay/unroll;\n• при малом compute может не раскрывать потенциал.") },
        { icon: "◆", title: qsTr("Режимы инференса"),
          text: qsTr("• Search — рекомендуемый режим по умолчанию: сильнее, но медленнее;\n• Greedy — быстрее, без search, для baseline/smoke-тестов.") },
        { icon: "✦", title: qsTr("Температура"),
          text: qsTr("Влияет только в Search (в Greedy не используется).") },
        { icon: "★", title: qsTr("Когда выбирать"),
          text: qsTr("Когда нужен максимум силы модели и есть бюджет по времени/ресурсам для обучения и оценки.") }
    ]
    readonly property var smzSections: [
        { icon: "ⓘ", title: qsTr("Что это"),
          text: qsTr("Sampled MuZero: сэмплирует K цельных (joint) ходов из приора, координирует действия юнитов через importance sampling. v1 — одна машина, без inference server.") },
        { icon: "▶", title: qsTr("Как учится"),
          text: qsTr("Self-play + replay: актор сэмплирует K joint-действий, оценивает их через модель динамики, обновляет policy с IS-коррекцией. Learner учится через unroll + V-trace.") },
        { icon: "✓", title: qsTr("Сильные стороны"),
          text: qsTr("• явная координация юнитов через joint sampling;\n• IS-коррекция смещения сэмплирования;\n• дедупликация повторных ходов (dedup);\n• совместим с V-trace и reanalyze.") },
        { icon: "⚠", title: qsTr("Ограничения"),
          text: qsTr("• только одна машина (v1);\n• при малом K поиск слабее GMZ;\n• нет inference server — акторы и learner делят ресурсы GPU.") },
        { icon: "◆", title: qsTr("Ключевые параметры"),
          text: qsTr("• num_samples (K) — число joint-ходов на шаг;\n• search_temperature — температура в поиске;\n• sample_temperature — температура сэмплирования из приора;\n• prior_weight — доля приора в политике (0 = только IS-цель).") },
        { icon: "★", title: qsTr("Когда выбирать"),
          text: qsTr("Когда нужна координация юнитов через совместные действия и есть желание экспериментировать с IS-based MuZero без распределённого inference.") }
    ]
    readonly property var gazSections: [
        { icon: "ⓘ", title: qsTr("Что это"),
          text: qsTr("AlphaZero с Gumbel-планированием: в корне берётся набор кандидатов (Gumbel top-k), Sequential Halving распределяет бюджет симуляций, а completed-Q даёт цель политики. Поиск — depth-1.") },
        { icon: "▶", title: qsTr("Как учится"),
          text: qsTr("Self-play тем же конвейером, что AlphaZero (replay, value/policy, чекпойнты). Отличается только бэкенд поиска у актёра: per-head Gumbel top-k + Sequential Halving вместо PUCT-MCTS.") },
        { icon: "✓", title: qsTr("Сильные стороны"),
          text: qsTr("• гарантирует улучшение политики даже при крошечном бюджете симуляций (16–64);\n• дешевле полного MCTS на ход;\n• сеть и чекпойнты совместимы с AlphaZero;\n• удобен для LAN/распределёнки (depth-1, мало симуляций).") },
        { icon: "⚠", title: qsTr("Ограничения"),
          text: qsTr("• поиск только на 1 ход вперёд (depth-1), без глубокого дерева как у AZ Tree;\n• при детерминированном ходе врага рост num_simulations почти не влияет;\n• потолок тактики ниже, чем у полного AZ Tree с большим MCTS.") },
        { icon: "◆", title: qsTr("Режимы инференса"),
          text: qsTr("• Search — Gumbel AlphaZero-поиск, рекомендуемый режим по умолчанию;\n• Greedy — один проход сети без поиска, быстрее, но обычно слабее.") },
        { icon: "✦", title: qsTr("Температура"),
          text: qsTr("На дебюте ход сэмплится из улучшённой политики; дальше — детерминированный победитель Sequential Halving.") },
        { icon: "★", title: qsTr("Когда выбирать"),
          text: qsTr("Когда нужен AlphaZero-пайплайн с гарантией улучшения при малом бюджете поиска — особенно под LAN/распределённое self-play.") }
    ]

    title: qsTr("Подсказка по моделям обучения")
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
        if (a === "sampled_muzero") return 5
        if (a === "gumbel_az") return 6
        return 0
    }

    onOpened: helpStack.currentIndex = tabIndexForAlgo(initialAlgo)

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
                        text: qsTr("Скорость и простота")
                        font.bold: true
                        font.pixelSize: Math.round(13 * dlg.uiScale)
                        color: "#93c5fd"
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    Label {
                        text: qsTr("DQN · PPO — быстрые итерации, удобный старт обучения.")
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
                        text: qsTr("Качество и поиск")
                        font.bold: true
                        font.pixelSize: Math.round(13 * dlg.uiScale)
                        color: "#c4b5fd"
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    Label {
                        text: qsTr("AZ Tree · GMZ — просчёт вперёд, дороже по времени.\nAZ Proxy — self-play без полного MCTS, быстрее ход.")
                        wrapMode: Text.WordWrap
                        color: dlg.textMuted
                        Layout.fillWidth: true
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            AlgoHelpSidebar {
                id: helpSidebar
                Layout.preferredWidth: Math.round(190 * dlg.uiScale)
                Layout.fillHeight: true
                currentIndex: helpStack.currentIndex
                rootUi: dlg.rootUi
                onIndexSelected: function(idx) { helpStack.currentIndex = idx }
            }

            StackLayout {
                id: helpStack
                Layout.fillWidth: true
                Layout.fillHeight: true

                ScrollView {
                    clip: true
                    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                    ScrollBar.vertical.policy: ScrollBar.AsNeeded

                    AlgoHelpCard {
                        width: helpStack.width
                        rootUi: dlg.rootUi
                        algoTitle: qsTr("DQN (Deep Q-Network)")
                        tldr: qsTr("Не «ванильный» DQN, а Rainbow-набор: Double, Dueling, IQN, NoisyNet, n-step, PER. Сильный value-агент без поиска.")
                        accentColor: dlg.algoColors[0]
                        abbr: "DQN"
                        role: qsTr("Rainbow-стрелок")
                        stats: dlg.dqnStats
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
                        algoTitle: qsTr("PPO (Proximal Policy Optimization)")
                        tldr: qsTr("On-policy policy-агент. Стабильно учится, удобный дефолт для RL.")
                        accentColor: dlg.algoColors[1]
                        abbr: "PPO"
                        role: qsTr("Линейный штурмовик")
                        stats: dlg.ppoStats
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
                        algoTitle: qsTr("AlphaZero Tree (AZ Tree)")
                        tldr: qsTr("Policy + Value с настоящим MCTS. Сильная тактика, дорогой инференс.")
                        accentColor: dlg.algoColors[2]
                        abbr: "AZ"
                        role: qsTr("Тактик-предиктор")
                        stats: dlg.azTreeStats
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
                        algoTitle: qsTr("AlphaZero Proxy (AZ Proxy)")
                        tldr: qsTr("Тот же AZ-пайплайн, на ходу без полного дерева. Быстрее, но потолок ниже.")
                        accentColor: dlg.algoColors[3]
                        abbr: "AZP"
                        role: qsTr("Лёгкий тактик")
                        stats: dlg.azProxyStats
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
                        algoTitle: qsTr("Gumbel MuZero (GMZ)")
                        tldr: qsTr("MuZero с Gumbel-поиском и моделью динамики. Потолок качества, самый дорогой режим.")
                        accentColor: dlg.algoColors[4]
                        abbr: "GMZ"
                        role: qsTr("Стратег-планировщик")
                        stats: dlg.gmzStats
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
                        algoTitle: qsTr("Sampled MuZero (SMZ)")
                        tldr: qsTr("MuZero с сэмплированием K joint-ходов и IS-коррекцией. Координация юнитов, v1 — одна машина.")
                        accentColor: dlg.algoColors[5]
                        abbr: "SMZ"
                        role: qsTr("Стратег-снайпер")
                        stats: dlg.smzStats
                        badges: dlg.smzBadges
                        sections: dlg.smzSections
                    }
                }
                ScrollView {
                    clip: true
                    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                    ScrollBar.vertical.policy: ScrollBar.AsNeeded

                    AlgoHelpCard {
                        width: helpStack.width
                        rootUi: dlg.rootUi
                        algoTitle: qsTr("Gumbel AlphaZero (GAZ)")
                        tldr: qsTr("AlphaZero с Gumbel-планированием (top-k + Sequential Halving, depth-1). Улучшение политики при малом бюджете симуляций.")
                        accentColor: dlg.algoColors[6]
                        abbr: "GAZ"
                        role: qsTr("Gumbel-тактик")
                        stats: dlg.gazStats
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
        }

        RowLayout {
            Layout.fillWidth: true
            Item { Layout.fillWidth: true }
            Button {
                text: qsTr("Закрыть")
                onClicked: dlg.close()
            }
        }
    }
}
