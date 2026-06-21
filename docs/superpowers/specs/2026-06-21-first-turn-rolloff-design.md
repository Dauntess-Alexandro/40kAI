# Determine First Turn (второй roll-off) — design

Дата: 2026-06-21
Статус: согласован дизайн, ждёт ревью спеки → writing-plans
Область: `core/envs/warhamEnv.py`, `core/engine/`, драйверы `eval.py` / `train.py` / `game_controller.py` / `*_selfplay.py`

## 1. Контекст и проблема

В движке есть только **один** roll-off — `roll_off_attacker_defender` ([warhamEnv.py:298](../../../core/envs/warhamEnv.py)),
и его результат используется **только для зон/порядка деплоя** ([mission.py:871-887](../../../core/engine/mission.py)).
Кто ходит первым в боевом раунде — **захардкожено**: `turn_order = ["enemy","model"]` ([warhamEnv.py:1060](../../../core/envs/warhamEnv.py)),
`active_side = turn_order[0]` в `reset()` ([warhamEnv.py:7166](../../../core/envs/warhamEnv.py)). Нигде не переустанавливается по итогу roll-off.

По правилам 10e (Leviathan/Pariah Nexus, миссии типа Only War) после деплоя есть отдельный шаг
**Determine First Turn** — второй roll-off, победитель берёт первый ход. В коде его нет.

Последствия:
- Эвристика (env-сторона `enemy`) **всегда ходит первой**, learner (`model`) — всегда второй. Преимущество первого хода зашито в одну сторону.
- Метки P1/P2 косметические: настоящей оси «первый/второй игрок» нет → честная симметрия P1↔P2 недостижима.
- **Драйверы уже непоследовательны** по порядку: DQN/PPO/eval зовут `enemyTurn()` → `step(model)` (enemy-first),
  а AZ/MuZero self-play — `step(model)` → `enemyTurn()` (model-first). Из-за этого `_advance_turn_order`
  (закрывает раунд по `turn_order[-1]`) в AZ-пути закрывает раунд не на той половине — латентное расхождение счёта `battle_round`.

## 2. Цель и не-цели

**Цель.** Интегрировать шаг Determine First Turn: (1) второй roll-off, (2) очередь хода и `active_side`
определяются его итогом (не хардкод), (3) аудит и тесты, что VP/деплой/objective/счёт раундов не завязаны
неявно на «enemy первый». Сделать первый ход управляемым (override) для воспроизводимости и честного замера P1↔P2.

**Не-цели.** Глобальное сидирование RNG в `train.py` (отдельная задача). «Победитель выбирает первый/второй»
(берём упрощённое правило: победитель ходит первым). Изменение reward/эвристики стратагем.

## 3. Принятые решения

- **Семантика:** победитель второго roll-off ходит первым (без выбора первый/второй).
- **Default + override:** env-переменная `FIRST_TURN`:
  - `roll` (**default**) — честный D6-vs-D6 бросок (корректное правило 10e);
  - `model_first` — форс: learner первый;
  - `enemy_first` — форс: эвристика первая (**точный режим обратной совместимости** со старым поведением).
- **Охват:** все драйверы env — eval, train (DQN/PPO actor-learner), self-play (AlphaZero/Gumbel MuZero/Sampled MuZero), Viewer/play.
- **Фазирование (инженерное решение):** Phase 1 — стабильное ядро (env + хелпер + DQN/PPO/eval/play + регрессы);
  Phase 2 — AZ/MuZero MCTS (изолированно, свои тесты). Phase 2 не блокирует и не дестабилизирует Phase 1.
- **Архитектура:** Подход A — единый источник правды в env + общий хелпер последовательности половин хода.

## 4. Архитектура (Подход A)

Единый источник правды — `env.first_turn_side` (и производный `env.turn_order`). Один общий хелпер
прогоняет две половины боевого раунда в порядке `turn_order`. Каждый драйвер передаёт хелперу свои
замыкания для model-половины и enemy-половины. Это убирает дублирование «кто первый» и попутно
унифицирует счёт раундов (фикс латентного AZ-расхождения).

Поток на партию:
```
roll_off_attacker_defender()        # как сейчас → зоны деплоя
deploy_for_mission(...)             # как сейчас
first = resolve_first_turn_side()   # НОВОЕ: FIRST_TURN → roll|model_first|enemy_first
env.attacker_side / env.defender_side = ...   # как сейчас
env.first_turn_side = first         # НОВОЕ
env.reset(...)                      # turn_order = [first, other]; active_side = turn_order[0]
# далее цикл раундов через run_battle_round(env, run_model_half, run_enemy_half)
```

## 5. Компоненты

### 5.1 Определение первого хода (`core/envs/warhamEnv.py`)
- `roll_off_first_turn(manual_roll_allowed=False, log_fn=None) -> str` — зеркало `roll_off_attacker_defender`:
  D6 (enemy) vs D6 (model), ничья → переброс; enemy использует `player_dice` только при `MANUAL_DICE=1 and manual_roll_allowed`,
  model всегда `auto_dice`. Возвращает `"model"|"enemy"` — победитель (ходит первым).
- `resolve_first_turn_side(*, manual_roll_allowed=False, log_fn=None, env_value=None) -> str` — читает `FIRST_TURN`
  (`os.getenv`, lower-strip): `model_first→"model"`, `enemy_first→"enemy"`, иначе/`roll`/пусто → `roll_off_first_turn(...)`.
  Невалидное значение → лог-предупреждение в формате проекта (что/где/что делать) и фолбэк на `roll`.

### 5.2 Плоттинг в env (`reset` / round-counting)
- Убрать хардкод `turn_order` из `__init__` (или оставить как дефолт-плейсхолдер). В `reset()` **до** `active_side = turn_order[0]`:
  `first = getattr(self, "first_turn_side", None) or "enemy"`; `self.turn_order = [first, "model" if first == "enemy" else "enemy"]`.
  Фолбэк `"enemy"` сохраняет поведение для прямого конструирования env (тесты/утилиты) без драйвера.
- `step()` уже ставит `active_side="model"` ([warhamEnv.py:7711](../../../core/envs/warhamEnv.py)),
  `enemyTurn()` — `active_side="enemy"` ([warhamEnv.py:7238](../../../core/envs/warhamEnv.py)). `_advance_turn_order`
  закрывает раунд по `turn_order[-1]` ([warhamEnv.py:4684](../../../core/envs/warhamEnv.py)). **Не меняем** —
  корректность держится на инварианте: драйвер зовёт половины в порядке `turn_order` (см. 5.3).

### 5.3 Общий хелпер (`core/engine/turn_sequencing.py`, новый)
- `run_battle_round(env, *, run_model_half, run_enemy_half) -> None`:
  берёт `order = getattr(env_u, "turn_order", ["enemy","model"])`; для `side in order` вызывает
  соответствующее замыкание; после каждой половины — если `env_u.game_over`, прерывается.
- Контракт замыканий: `run_model_half()` инкапсулирует выбор действия + `env.step(...)` (или MCTS + step);
  `run_enemy_half()` — `env.enemyTurn(...)`. Хелпер не знает деталей алгоритма — только порядок и short-circuit.
- Юнит-тестируется на «скриптовом» env-дабле без реального движка.

### 5.4 Точки интеграции драйверов
- **Phase 1:**
  - `eval.run_episode` ([eval.py:588+](../../../eval.py)) — обернуть enemy/model половины в замыкания, цикл раунда через хелпер.
  - `train.py` DQN/PPO actor-learner: оба rollout-пути ([train.py:~5400/~5495](../../../train.py)) и det-eval ([train.py:3739/3761](../../../train.py)).
  - `game_controller` (Viewer/play, [game_controller.py:525+](../../../core/engine/game_controller.py)).
- **Phase 2:**
  - `alphazero_selfplay.play_episode_with_mcts`, `gumbel_muzero_selfplay`, `sampled_muzero_selfplay` — те же замыкания + раздел 5.5.

### 5.5 Особый случай AZ/MuZero (MCTS-prepend) — Phase 2
MCTS внутри симулирует ходы врага (`enemy_policy_fn`, `reset_options`) и предполагает структуру «model-ход → enemy-ход».
Когда **враг ходит первым**, его первую половину надо применить к корневому состоянию **до** входа в per-move MCTS-цикл
(«prepend» первой enemy-половины); далее цикл идёт как сегодня (model-MCTS, enemy). Симметрично при model-first — без prepend.
Реализуется в self-play драйверах через `run_battle_round`/явный prepend; покрывается отдельными тестами на оба порядка.
Если интеграция MCTS окажется неустойчивой — Phase 2 откатывается независимо от Phase 1.

## 6. Обработка ошибок и edge-кейсы
- Невалидный `FIRST_TURN` → предупреждение + фолбэк `roll` (не падать).
- `env.first_turn_side` не задан (прямое конструирование) → `reset()` фолбэк `"enemy"` (старое поведение).
- `manual_roll_allowed`/`MANUAL_DICE=1` — ручной бросок enemy, как у attacker/defender.
- Короткие партии: если `game_over` после первой половины — хелпер не зовёт вторую (short-circuit).

## 7. Обратная совместимость
- `FIRST_TURN=enemy_first` точно воспроизводит текущее поведение (enemy всегда первый).
- Default `roll` **меняет** поведение во всех путях (включая обучение): эвристика больше не всегда первая.
  Старые чекпойнты/бенчмарки несравнимы напрямую — это осознанный выбор ради корректности; смягчение —
  явный лог первого хода и возможность форса.

## 8. Тестирование (TDD — тест до кода)
- `roll_off_first_turn`: детерминизм при подменённых костях; корректный переброс при ничье; ветка `MANUAL_DICE`.
- `resolve_first_turn_side`: `roll`/`model_first`/`enemy_first`/пусто/мусор.
- `reset()`: `turn_order` и `active_side` собираются из `first_turn_side` для обоих значений; фолбэк `"enemy"`.
- round-counting: скриптовый прогон обоих порядков — `battle_round` инкрементируется ровно один раз за полный раунд,
  на второй половине; фикс латентного AZ-расхождения подтверждён тестом.
- `run_battle_round`: порядок вызовов = `turn_order`; short-circuit по `game_over`.
- Интеграционный smoke: 1–2 партии по одному драйверу из каждой группы (Phase 1: DQN/eval; Phase 2: один self-play) в обоих режимах форса.
- Перед коммитом — субагент `engine-regression-reviewer` по диффу движка.

## 9. Регрессионный чеклист (пункт 3)
Проверить отсутствие неявной завязки на «enemy первый»:
- CP: каждая `command_phase` даёт +1 обеим сторонам (порядко-независимо) — зафиксировать тестом.
- VP/objective: `score_end_of_command_phase`, `apply_end_of_battle` — симметрия по порядку.
- `battle_round`: корректность во всех драйверах и обоих порядках.
- Тайминг конца боя по лимиту раундов: кто ходит последним при разном первом ходе — задокументировать, проверить отсутствие систематического перекоса.
- eval-атрибуция победителя (`learner_side`-маппинг, [eval.py:1372-1405](../../../eval.py)) не зависит от первого хода.
- obs-фичи: нет скрытого кодирования «enemy первый».

## 10. Логирование/телеметрия
- `[FIRST_TURN] mode=<roll|model_first|enemy_first> winner=<model|enemy>` в TRAIN/EVAL/PLAY (RU-строка по формату проекта).
- Опционально (не блокер): счётчик winrate при ходе первым/вторым — для будущего замера преимущества первого хода.

## 11. Открытые риски
- AZ/MuZero MCTS-prepend (5.5) — самый тонкий момент; изолирован в Phase 2.
- Смена default-поведения (раздел 7) — широкий blast radius по обучению; смягчено форс-режимом и логом.
