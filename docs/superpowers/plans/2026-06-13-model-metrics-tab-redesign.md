# Редизайн вкладки «Метрики модели» (вариант A) — план реализации

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Переверстать вкладку «Метрики модели» в `Main.qml` по варианту A «Одним взглядом»: компактная шапка-строка, 4 KPI, 2 главных графика, остальное — в свёрнутые секции; убрать дубли.

**Architecture:** Вводим переиспользуемый компонент `ExpanderSection.qml` (кликабельный заголовок + сворачиваемый контент). Внутри вкладки переставляем существующие элементы: KPI-плитки и `MetricChart` остаются, меняется их группировка. Источник данных (`controller.detSeries()`, `chartSpecs`, сигналы) не трогаем.

**Tech Stack:** PySide6 / Qt Quick (QML), компоненты `ChamferPanel`, `MetricChart`. Проверка — `qmllint.exe` из `.venv`, финальная — запуск Qt GUI.

**Спека:** `docs/superpowers/specs/2026-06-13-model-metrics-tab-redesign-design.md`

**Команда проверки QML (используется в каждой задаче):**
```
.venv/Scripts/qmllint.exe app/gui_qt/qml/Main.qml -I app/gui_qt/qml
```
Ожидаемо: предупреждения о неразрешённых типах/`controller` ДОПУСТИМЫ (qmllint не знает контекст PySide). Блокирующее — только синтаксические/parse-ошибки (`Error:` с указанием строки в правленом файле).

---

### Task 1: Компонент `ExpanderSection.qml`

Сворачиваемая секция: заголовок-строка с шевроном `▸/▾` + контейнер контента, который сворачивается по клику.

**Files:**
- Create: `app/gui_qt/qml/components/ExpanderSection.qml`

- [ ] **Step 1: Создать компонент**

```qml
import QtQuick
import QtQuick.Layouts
import ".."

// Сворачиваемая секция: кликабельная строка-заголовок (шеврон + текст) и контент,
// который показывается только когда expanded === true.
// Контент кладётся как дочерние элементы; каждый должен задавать width: parent.width.
Item {
    id: sec

    property string title: ""
    property bool expanded: false
    property real uiScale: 1.0
    property int captionSize: 11
    property color textMain: "#d7dde7"
    property color textMuted: "#98a4b8"
    property color panelFill: "#161f31"
    property color panelBorder: "#2f3d58"

    default property alias contentData: bodyHolder.data

    implicitHeight: headerBar.height
                    + (expanded ? bodyHolder.childrenRect.height + Math.round(8 * uiScale) : 0)

    ChamferPanel {
        id: headerBar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: Math.round(36 * sec.uiScale)
        cutSize: Math.round(6 * sec.uiScale)
        contentMargin: 0
        fillColor: sec.panelFill
        borderWidth: 1
        borderColor: sec.panelBorder
    }

    Row {
        anchors.left: headerBar.left
        anchors.leftMargin: Math.round(12 * sec.uiScale)
        anchors.verticalCenter: headerBar.verticalCenter
        spacing: Math.round(8 * sec.uiScale)

        Text {
            text: sec.expanded ? "▾" : "▸"   // ▾ / ▸
            color: sec.textMuted
            font.pixelSize: sec.captionSize + 2
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            text: sec.title
            color: sec.textMain
            font.bold: true
            font.pixelSize: sec.captionSize + 1
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    MouseArea {
        anchors.fill: headerBar
        cursorShape: Qt.PointingHandCursor
        onClicked: sec.expanded = !sec.expanded
    }

    Item {
        id: bodyHolder
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: headerBar.bottom
        anchors.topMargin: Math.round(8 * sec.uiScale)
        height: sec.expanded ? childrenRect.height : 0
        visible: sec.expanded
        clip: true
    }
}
```

- [ ] **Step 2: Проверить qmllint**

Run: `.venv/Scripts/qmllint.exe app/gui_qt/qml/components/ExpanderSection.qml -I app/gui_qt/qml`
Ожидаемо: нет `Error:` про синтаксис в `ExpanderSection.qml` (предупреждения о `ChamferPanel`/типах допустимы).

- [ ] **Step 3: Commit**

```bash
git add app/gui_qt/qml/components/ExpanderSection.qml
git commit -m "feat(gui): компонент ExpanderSection — сворачиваемая секция для вкладки метрик"
```

---

### Task 2: Шапка вкладки в одну строку + удаление дублей

Заменяем заголовок `Model Metrics` + длинный абзац + строку кнопок + три summary-карточки одной строкой-шапкой. Описание уезжает в тултип. Данные карточек «Модель»/«Оппонент» позже (Task 4) попадут в свёрнутую секцию — здесь просто удаляем их отсюда.

**Files:**
- Modify: `app/gui_qt/qml/Main.qml` (блок вкладки «Метрики модели», ориентировочно строки 3887–3985)

- [ ] **Step 1: Заменить заголовок+описание+кнопки+summary одной шапкой**

Найти блок, начинающийся с `Text { text: "Model Metrics" ...` и заканчивающийся закрывающей `}` summary-`RowLayout` (карточка «Оппонент»), т.е. участок от строки `Text { text: "Model Metrics"` до конца `RowLayout` с тремя `Rectangle`-карточками. Заменить его на:

```qml
                        // Шапка: одна строка — заголовок + чипы модели + действия.
                        RowLayout {
                            width: parent.width
                            spacing: root.spacingMd

                            Text {
                                text: "Метрики модели"
                                font.pixelSize: Math.round(20 * root.uiScale)
                                font.bold: true
                                color: root.uiTextMain
                            }

                            // Чип-подсказка с прежним описанием (текст не теряем).
                            Text {
                                text: "?"
                                color: root.uiTextMuted
                                font.bold: true
                                font.pixelSize: Math.round(14 * root.uiScale)
                                ToolTip.visible: helpHover.hovered
                                ToolTip.text: "Метрики тренировки: каждая точка — окно реальных тренировочных эпизодов (DET-прогоны удалены). Честное сравнение моделей — вкладка «Оценка»."
                                HoverHandler { id: helpHover }
                            }

                            Text {
                                text: controller.metricsAlgo
                                color: root.uiTextMuted
                                font.bold: true
                                visible: controller.metricsAlgo.length > 0
                            }
                            Text {
                                text: controller.selfPlayEnabled ? "selfplay" : "vs preset"
                                color: root.uiTextMuted
                            }

                            Item { Layout.fillWidth: true }

                            Label {
                                text: controller.metricsLabel
                                color: root.uiTextMuted
                                elide: Label.ElideLeft
                                Layout.maximumWidth: Math.round(260 * root.uiScale)
                            }
                            Button {
                                text: "Выбрать модель"
                                onClicked: metricsFileDialog.open()
                            }
                            Button {
                                text: "Последняя"
                                onClicked: controller.select_latest_metrics()
                            }
                        }
```

(«Открыть в TensorBoard» остаётся на своём месте ниже, в action-row внутри `metricsDash`, — его не трогаем.)

- [ ] **Step 2: Проверить qmllint**

Run: `.venv/Scripts/qmllint.exe app/gui_qt/qml/Main.qml -I app/gui_qt/qml`
Ожидаемо: нет новых `Error:` про синтаксис в районе правки.

- [ ] **Step 3: Commit**

```bash
git add app/gui_qt/qml/Main.qml
git commit -m "refactor(gui): шапка вкладки метрик в одну строку, удалены summary-дубли"
```

---

### Task 3: Разделить графики — 2 главных наверху, остальные в свёрнутую секцию

`chartSpecs` бьём на `mainSpecs` (Winrate, Reward) и `restSpecs` (остальные 6). Главные рендерим всегда крупной сеткой 2×1; остальные — внутри `ExpanderSection` (свёрнут по умолчанию).

**Files:**
- Modify: `app/gui_qt/qml/Main.qml` (внутри `ColumnLayout { id: metricsDash ... }`)

- [ ] **Step 1: Заменить единый `chartSpecs` на два массива**

Найти `property var chartSpecs: [ ... ]` (8 элементов) и заменить на:

```qml
                            property var mainSpecs: [
                                { title: "Winrate", fmt: "pct", src: "series", lines: [{ key: "win_rate", name: "win", color: root.accentPrimaryAction }] },
                                { title: "Средняя награда", fmt: "num", src: "series", lines: [{ key: "reward_mean", name: "reward", color: root.accentP1 }] }
                            ]
                            property var restSpecs: [
                                { title: "Loss обучения", fmt: "num", src: "loss", lines: [{ key: "values", name: "loss", color: "#3fb950" }] },
                                { title: "Длина эпизода", fmt: "int", src: "series", lines: [{ key: "ep_len_mean", name: "ep_len", color: "#9b8cff" }] },
                                { title: "Avg VP (model vs enemy)", fmt: "num", src: "series", lines: [{ key: "model_vp_mean", name: "model", color: root.accentP1 }, { key: "enemy_vp_mean", name: "enemy", color: root.accentP2 }] },
                                { title: "HP diff", fmt: "num", src: "series", lines: [{ key: "hp_diff_mean", name: "hp_diff", color: root.accentP2 }] },
                                { title: "Kill diff", fmt: "num", src: "series", lines: [{ key: "kill_diff_mean", name: "kill_diff", color: root.accentPrimaryAction }] },
                                { title: "Причины завершения", fmt: "pct", src: "end", lines: [{ key: "wipeout_enemy_rate", name: "wipe enemy", color: root.accentP1 }, { key: "wipeout_model_rate", name: "wipe model", color: root.accentP2 }, { key: "turn_limit_rate", name: "turn limit", color: root.accentGhost }] }
                            ]
```

- [ ] **Step 2: Заменить единый `GridLayout` графиков на «главные + секция»**

Найти `GridLayout { ... columns: 2 ... Repeater { model: metricsDash.chartSpecs ... } }` (сетка живых графиков, видимая при `count > 0`) и заменить весь этот `GridLayout` на:

```qml
                            // Главные кривые: всегда крупно, 2 колонки.
                            GridLayout {
                                Layout.fillWidth: true
                                columns: 2
                                columnSpacing: root.spacingMd
                                rowSpacing: root.spacingMd
                                visible: (metricsDash.detData.count || 0) > 0

                                Repeater {
                                    model: metricsDash.mainSpecs
                                    delegate: MetricChart {
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: Math.round(258 * root.uiScale)
                                        uiScale: root.uiScale
                                        captionSize: root.evalCaptionSize
                                        textMain: root.uiTextMain
                                        textMuted: root.uiTextMuted
                                        panelFill: root.bgElevated
                                        panelBorder: root.borderMuted
                                        gridColor: root.borderMuted
                                        title: modelData.title
                                        fmt: modelData.fmt
                                        accent: modelData.lines[0].color
                                        xs: metricsDash._xsFor(modelData)
                                        series: metricsDash._seriesFor(modelData)
                                    }
                                }
                            }

                            // Остальные метрики: свёрнуто по умолчанию.
                            ExpanderSection {
                                Layout.fillWidth: true
                                Layout.preferredHeight: implicitHeight
                                visible: (metricsDash.detData.count || 0) > 0
                                title: "Остальные метрики"
                                expanded: false
                                uiScale: root.uiScale
                                captionSize: root.evalCaptionSize
                                textMain: root.uiTextMain
                                textMuted: root.uiTextMuted
                                panelFill: root.bgElevated
                                panelBorder: root.borderMuted

                                GridLayout {
                                    width: parent.width
                                    columns: 2
                                    columnSpacing: root.spacingMd
                                    rowSpacing: root.spacingMd

                                    Repeater {
                                        model: metricsDash.restSpecs
                                        delegate: MetricChart {
                                            Layout.fillWidth: true
                                            Layout.preferredHeight: Math.round(258 * root.uiScale)
                                            uiScale: root.uiScale
                                            captionSize: root.evalCaptionSize
                                            textMain: root.uiTextMain
                                            textMuted: root.uiTextMuted
                                            panelFill: root.bgElevated
                                            panelBorder: root.borderMuted
                                            gridColor: root.borderMuted
                                            title: modelData.title
                                            fmt: modelData.fmt
                                            accent: modelData.lines[0].color
                                            xs: metricsDash._xsFor(modelData)
                                            series: metricsDash._seriesFor(modelData)
                                        }
                                    }
                                }
                            }
```

- [ ] **Step 3: Обновить заголовок action-row**

Найти `Text { text: "Графики тренировки (окна эпизодов)" ... }` и заменить текст на `"Главные кривые (окна эпизодов)"`.

- [ ] **Step 4: Проверить qmllint**

Run: `.venv/Scripts/qmllint.exe app/gui_qt/qml/Main.qml -I app/gui_qt/qml`
Ожидаемо: нет новых синтаксических `Error:`; `ExpanderSection` резолвится (лежит в `components/`, импорт `".."` уже есть в файле — компонент в той же папке `components`, доступен по имени).

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/qml/Main.qml
git commit -m "refactor(gui): метрики — 2 главных графика наверху, остальные в сворачиваемой секции"
```

---

### Task 4: Секция «Детали модели и оппонента» (свёрнута)

Возвращаем в свёрнутом виде справочные поля из удалённых карточек: модель (algo/mode/run id) и оппонент (self-play/источник/алгоритм).

**Files:**
- Modify: `app/gui_qt/qml/Main.qml` (внутри `metricsDash`, сразу после секции «Остальные метрики»)

- [ ] **Step 1: Добавить секцию деталей**

Сразу после закрывающей `}` блока `ExpanderSection { title: "Остальные метрики" ... }` добавить:

```qml
                            // Детали модели и оппонента: справочно, свёрнуто.
                            ExpanderSection {
                                Layout.fillWidth: true
                                Layout.preferredHeight: implicitHeight
                                title: "Детали модели и оппонента"
                                expanded: false
                                uiScale: root.uiScale
                                captionSize: root.evalCaptionSize
                                textMain: root.uiTextMain
                                textMuted: root.uiTextMuted
                                panelFill: root.bgElevated
                                panelBorder: root.borderMuted

                                RowLayout {
                                    width: parent.width
                                    spacing: root.spacingMd

                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 4
                                        Text { text: "Модель"; font.bold: true; color: root.uiTextMain }
                                        Text { text: "Алгоритм: " + controller.metricsAlgo; color: root.uiTextMuted }
                                        Text { text: "Режим: " + controller.metricsMode; color: root.uiTextMuted }
                                        Text { text: "Run ID: " + controller.metricsRunId; color: "#777777"; elide: Text.ElideRight; Layout.fillWidth: true }
                                    }
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 4
                                        Text { text: "Оппонент"; font.bold: true; color: root.uiTextMain }
                                        Text { text: "Self-play: " + (controller.selfPlayEnabled ? "включён" : "выключен"); color: root.uiTextMuted }
                                        Text { text: "Источник: " + controller.opponentSource; color: root.uiTextMuted }
                                        Text { text: "Алгоритм оппонента: " + controller.opponentAlgo + (controller.opponentId.length > 0 ? (" (id=" + controller.opponentId + ")") : ""); color: root.uiTextMuted; elide: Text.ElideRight; Layout.fillWidth: true }
                                    }
                                }
                            }
```

- [ ] **Step 2: Проверить qmllint**

Run: `.venv/Scripts/qmllint.exe app/gui_qt/qml/Main.qml -I app/gui_qt/qml`
Ожидаемо: нет новых синтаксических `Error:`.

- [ ] **Step 3: Commit**

```bash
git add app/gui_qt/qml/Main.qml
git commit -m "feat(gui): метрики — свёрнутая секция деталей модели и оппонента"
```

---

### Task 5: Финальная проверка в живом GUI

**Files:** (только запуск, без правок)

- [ ] **Step 1: Запустить Qt GUI**

Run: `python -m app.gui_qt` (или через skill `run-40kai`/`verify`).
Открыть вкладку «Метрики модели».

- [ ] **Step 2: Визуально проверить критерии готовности**

- Шапка — одна строка (заголовок + «?»-тултип + чипы + кнопки); нет англ. «Model Metrics» и абзаца-описания.
- Видны 4 KPI-плитки и 2 крупных графика (Winrate, Reward).
- Секции «Остальные метрики» и «Детали модели и оппонента» — свёрнуты; по клику раскрываются (6 графиков / справочные поля).
- Нет дублирующих числовых блоков.
- При отсутствии данных — прежнее пустое состояние «Нет данных метрик».
- Вкладки «Метрики эвристики» и «Играть» не сломаны.

- [ ] **Step 3: Commit (если были мелкие правки по итогам осмотра)**

```bash
git add -A
git commit -m "fix(gui): доводка вкладки метрик после визуальной проверки"
```

---

## Self-Review (выполнено при написании плана)

- **Покрытие спеки:** шапка-строка+тултип (T2) ✓; 4 KPI без дублей — KPI остаются, дубли удалены (T2) ✓; 2 главных графика (T3) ✓; «Остальные метрики» свёрнуто (T3) ✓; «Детали» свёрнуто (T4) ✓; удаление карточек-дублей (T2) ✓; не трогаем MetricChart/данные/пустое состояние/соседние вкладки ✓.
- **Плейсхолдеры:** нет — весь QML приведён целиком.
- **Согласованность имён:** `mainSpecs`/`restSpecs`, `_xsFor`/`_seriesFor`, `metricsDash.detData.count`, `ExpanderSection` (свойства `title/expanded/uiScale/captionSize/textMain/textMuted/panelFill/panelBorder` + дефолтный контент) — едины во всех задачах.
- **Примечание по KPI:** блок KPI-плиток (`Repeater` с 4 элементами) и пустое состояние в Task 2–3 НЕ удаляются — остаются как есть, между шапкой и графиками.
