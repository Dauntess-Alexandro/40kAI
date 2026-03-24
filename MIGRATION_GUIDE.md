# 40kAI Migration Guide (Side+Faction League)

## Что изменилось

Теперь проект поддерживает новую архитектуру обучения:

- отдельные агенты по стороне и фракции (`P1/P2 + faction`)
- хранение агентов в реестре `models/agents_registry.json`
- артефакты агента в `models/agents/<side>/<faction>/<agent_id>/`
- матчмейкер оппонента (`mirror`, `cross_faction`, `league`)
- проверка совместимости контрактов окружения перед матчем

Старый формат (`model-*.pickle` + `.pth`) все еще может читаться в части сценариев как legacy, но основной поток теперь через `agent_id`.

---

## 1) Быстрый старт (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
pip install -e gym_mod
```

Запуск GUI:

```powershell
python gui_qt\main.py
```

---

## 2) Обучение агента P1 (пример: Necrons)

### Через GUI

В `Главная -> Действия` выстави:

- `Сторона обучения`: `P1`
- `Фракция обучения`: `Necrons`
- `Политика оппонента`: `mirror` (для старта)

Нажми `Тренировка 8х` или `Самообучение`.

### Через терминал (без GUI)

```powershell
set LEARNER_SIDE=P1
set LEARNER_FACTION=Necrons
set OPPONENT_POLICY=mirror
set LEAGUE_ENABLE=1
python train.py
```

---

## 3) Обучение агента P2 (пример: Necrons)

```powershell
set LEARNER_SIDE=P2
set LEARNER_FACTION=Necrons
set OPPONENT_POLICY=mirror
set LEAGUE_ENABLE=1
python train.py
```

После тренировки будут новые записи в:

- `models/agents_registry.json`
- `models/agents/P2/Necrons/<agent_id>/...`

---

## 4) Где искать agent_id

### В реестре

Файл:

- `models/agents_registry.json`

Там у каждого агента есть:

- `agent_id`
- `side`
- `faction`
- `artifact_dir`

---

## 5) Запуск eval c новым форматом

## Вариант A: как раньше (legacy)

```powershell
python eval.py --games 50 --model path\to\model-xxx.pickle
```

## Вариант B: через новый `agent_id`

```powershell
python eval.py --games 50 --learner-agent-id P1_Necrons_only_war_v1_final_ep2000_20260323_120000
```

## Вариант C: с явным оппонентом (валидация совместимости)

```powershell
python eval.py --games 50 ^
  --learner-agent-id P1_Necrons_only_war_v1_final_ep2000_20260323_120000 ^
  --opponent-agent-id P2_Necrons_only_war_v1_final_ep2000_20260323_121500 ^
  --opponent-policy league
```

Примечание: в текущем eval оппонент остается эвристикой, но `opponent-agent-id` уже валидируется на совместимость контракта.

---

## 6) Запуск play через `agent_id`

```powershell
python play.py None False --agent-id P1_Necrons_only_war_v1_final_ep2000_20260323_120000
```

Где:

- `None` — legacy аргумент модели (можно оставить)
- `False` — играть не в GUI режиме play.py
- `--agent-id` — новый источник policy из реестра

---

## 7) Запуск viewer/game_controller через `agent_id`

Можно передать через env:

```powershell
set VIEWER_AGENT_ID=P1_Necrons_only_war_v1_final_ep2000_20260323_120000
python -m viewer
```

или через `model_path` формата `agent:<id>` в местах, где вызывается `GameController`.

---

## 8) Matchup метрики (league)

Файл:

- `models/matchups.json`

Что там хранится:

- `learner_agent_id`
- `opponent_agent_id`
- win/draw
- `vp_diff`
- причина завершения

GUI (блок состояния модели) показывает краткую сводку top-3 оппонентов по числу игр.

---

## 9) Контракт совместимости (очень важно)

Перед матчем проверяются:

- `ruleset_version`
- `obs_space_signature`
- `action_space_signature`

Если несовместимо, запуск прерывается с сообщением:

- что случилось
- где
- что делать дальше (выбрать совместимого агента или переобучить)

---

## 10) Рекомендуемый curriculum для новичка

1. Сначала `mirror`:
   - обучи `P1_Necrons`
   - обучи `P2_Necrons`
2. Потом `cross_faction`:
   - добавь новую фракцию и тренируй отдельно `P1/P2`
3. Потом `league`:
   - включай сложный пул оппонентов и сравнивай матчапы

---

## 11) Частые проблемы и решения

### Проблема: "несовместимый контракт"

Причина:

- разный `ruleset_version` или разная сигнатура spaces.

Что делать:

- убедиться, что оба агента обучены на одном контракте
- переобучить один из агентов с теми же параметрами миссии/окружения

### Проблема: агент не находится

Причина:

- неверный `agent_id`, нет записи в `models/agents_registry.json`.

Что делать:

- открыть реестр и скопировать точный `agent_id`

### Проблема: eval/play работают по-старому

Причина:

- не передан `--agent-id` / `--learner-agent-id`.

Что делать:

- явно передавать новые аргументы

---

## 12) Минимальный чек-лист после миграции

- `python gui_qt\main.py` запускается
- `train.py` пишет новые артефакты в `models/agents/...`
- `models/agents_registry.json` обновляется
- `models/matchups.json` создается и пополняется
- `eval.py --learner-agent-id ...` проходит
- `play.py ... --agent-id ...` запускается

