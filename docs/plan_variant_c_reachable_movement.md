# План реализации Variant C: движение модели/эвристики через reachable-клетки (как у игрока)

## Контекст и цель
Сейчас у нас смешанный режим:
- игрок выбирает конкретную reachable-клетку в GUI,
- часть логики модели/эвристики всё ещё опирается на `move_dir` (up/down/left/right/stay).

Цель Variant C — перейти к двухэтапному выбору движения:
1) **Intent (намерение)**: куда/зачем двигаться (к objective, в cover, от угрозы, engage, stay),
2) **Concrete cell selection**: конкретная клетка из `move_cells/advance_cells/stay` с mask и score.

Это даст поведение ближе к игроку и снимет жёсткую привязку к 4 направлениям.

---

## Текущее состояние (как есть)

1. Reachable-клетки уже считаются и отдаются в overlay:
   - `get_unit_reachable_cells`,
   - `get_unit_movement_overlay` с `move_cells`/`advance_cells`.

2. Для model-ветки уже есть переход через `_pick_destination_from_overlay`, но с directional bias от `move_dir`.

3. Enemy heuristic уже выбирает из кандидатных reachable-клеток (`move+advance+stay`) по эвристике.

4. Enemy RL в одной ветке ещё делает осевой шаг через `move_dir`.

Итого: база для Variant C уже есть, но нужна унификация и новый action-contract.

---

## Целевой контракт действий (Variant C)

### 1) Action schema (движение)
Ввести (или подготовить) структуру:
- `move_intent` — дискретный класс намерения:
  - `0=to_objective`
  - `1=to_cover`
  - `2=threat_avoid`
  - `3=engage_target`
  - `4=stay`
- `move_mode_pref`:
  - `0=normal_only`
  - `1=allow_advance`
- `move_cell_selector`:
  - скаляр/вектор для ранжирования кандидатов (например, топ-1 по score сети или value-head по кандидатам).

### 2) Candidate set
Для каждого юнита строим:
- `C = move_cells ∪ advance_cells ∪ {stay_cell}`
- Для каждого кандидата считаем фичи:
  - dist к ближайшему objective,
  - dist к ближайшему врагу,
  - cover/exposure,
  - mode (normal/advance/stay),
  - distance-from-start.

### 3) Mask/validation
- Кандидаты только из reachable-списков.
- Если `move_mode_pref=normal_only`, advance-клетки можно штрафовать/отсекать.
- Если `intent=stay`, принудительный выбор stay (или очень высокий bias).

---

## Фазный план внедрения

## Фаза 0. Инструментация и флаги
1. Добавить feature-flag:
   - `MOVEMENT_POLICY_MODE=legacy|variant_c_shadow|variant_c_live`.
2. Добавить логи (без ломки формата):
   - `[MOVE][VARC] unit=... intent=... candidates=... chosen=(x,y,mode) ...`.
3. Добавить trace-поля в `movement_meta` для offline-сравнения.

**Результат:** можно безопасно включать shadow-режим и сравнивать решения.

## Фаза 1. Общий candidate-builder (переиспользуемый)
1. Вынести общую функцию построения кандидатов:
   - для model,
   - для enemy RL,
   - для enemy heuristic.
2. Унифицировать нормализацию фичей кандидатов.
3. Ввести единый scorer API:
   - `score_candidates(intent, features, context) -> best_candidate`.

**Результат:** единая точка выбора клетки по reachable для всех сторон.

## Фаза 2. Shadow inference (без влияния на геймплей)
1. В active run сохранять:
   - legacy-выбор,
   - variant_c-рекомендацию,
   - расхождение по клетке/метрикам.
2. В лог добавлять причину выбора:
   - objective delta,
   - threat/cover contribution,
   - mode penalty.
3. Собрать статистику на N игр:
   - частота stay,
   - средний прогресс к objective,
   - exposed_units,
   - winrate/VP.

**Результат:** видно, ухудшает/улучшает ли Variant C до переключения live.

## Фаза 3. Live для heuristic enemy
1. Перевести heuristic enemy полностью на общий candidate-builder + scorer.
2. Удалить осевую ветку для heuristic (где есть).
3. Проверить регрессии movement/overwatch/логов.

**Результат:** эвристика ходит как игрок (по reachable).

## Фаза 4. Live для model side (RL rollout)
1. Перевести model movement loop на Variant C scorer.
2. Оставить backward-совместимость action:
   - если старая модель отдаёт `move_dir`, маппить в intent через адаптер.
3. Ввести мягкие penalties:
   - over-advance без выгоды,
   - ухудшение threat/exposure,
   - бессмысленный stay.

**Результат:** модель ходит по reachable-клеткам без осевой привязки.

## Фаза 5. Обучение под новый контракт
1. Обновить action head:
   - intent head,
   - mode head,
   - candidate score head (или pointer-like score).
2. Обновить replay schema (версионирование).
3. Добавить curriculum:
   - сначала to_objective/to_cover,
   - потом full intents.
4. Сравнить с baseline на фиксированных сидов.

**Результат:** полноценный RL под Variant C.

---

## Изменения по модулям (когда начнём код)

## `gym_mod/gym_mod/envs/warhamEnv.py`
- Вынести `build_movement_candidates(side, idx)`.
- Вынести `score_movement_candidate(...)`.
- Добавить `select_movement_candidate_variant_c(...)`.
- Подключить в:
  - model movement loop,
  - enemy RL loop,
  - enemy heuristic loop.

## `viewer/app.py` / `viewer/opengl_view.py`
- UI почти не менять:
  - movement overlay уже работает по фактическому from/to.
- Опционально добавить debug-chip `intent=...` в лог-строки debug (не в основной формат).

## `tests/`
- Добавить регрессии:
  1) кандидат всегда из reachable,
  2) stay только при валидной причине,
  3) intent->клетка не ломает bounds/collision,
  4) parity с legacy в базовых сценариях.

---

## Риски и как гасим

1. **Риск деградации RL из-за смены action-space.**
   - Митигируем shadow-режимом + адаптером backward compatibility.

2. **Риск “дёрганого” поведения (частые бессмысленные advance).**
   - Добавляем penalties за advance без tactical gain.

3. **Риск шума в логах.**
   - Debug-логи только под флагом, базовый формат не ломаем.

4. **Риск роста вычислений при scoring всех кандидатов.**
   - Кэп на candidates + ранний pruning по intent.

---

## Критерии готовности (Definition of Done)

1. Все движения model/enemy(heur) выбираются из reachable-клеток.
2. Осевые смещения `move_dir` не используются напрямую в live-ветке.
3. Логи содержат объяснение выбора клетки в debug-режиме.
4. Регрессионные тесты movement проходят.
5. На контрольном наборе сидов не хуже baseline по ключевым метрикам:
   - VP delta,
   - winrate,
   - exposed_units,
   - objective progress.

---

## Рекомендуемый порядок запуска работ

1. Фаза 0 + Фаза 1 (инфраструктура + единый builder/scorer).
2. Фаза 2 (shadow) минимум на 100–300 матчей.
3. Фаза 3 (heuristic live).
4. Фаза 4 (model live через адаптер).
5. Фаза 5 (обновлённое обучение).

Этот порядок даёт минимальный риск и быстрый контроль качества.

---

## Статус реализации в коде (текущий шаг)

- ✅ Фаза 0 (базово):
  - добавлен feature-flag `MOVEMENT_POLICY_MODE=legacy|variant_c_shadow|variant_c_live`,
  - добавлен debug-лог формата `[MOVE][VARC] ...` через `_append_agent_log`.

- ✅ Фаза 1 (базово):
  - добавлен единый builder кандидатов `_build_movement_candidates(...)`,
  - добавлен scorer `_score_movement_candidate_variant_c(...)`,
  - добавлен selector `_select_movement_candidate_variant_c(...)`.

- ✅ Фаза 2 (shadow):
  - в `_pick_destination_from_overlay(...)` добавлен shadow-сравнитель legacy vs variant_c,
  - в `variant_c_shadow` поведение не меняется (только логируем сравнение),
- в `variant_c_live` подготовлен технический переключатель на variant_c-выбор.

- ✅ Фаза 3 (heuristic enemy live):
  - enemy heuristic теперь использует тот же variant_c-selector,
  - в `variant_c_shadow` логируется сравнение legacy vs variant_c,
  - в `variant_c_live` применяется variant_c-выбор клетки.

- ✅ Фаза 4 (model/enemy RL rollout):
  - enemy RL ветка переведена на `_pick_destination_from_overlay(...)` вместо прямого осевого шага,
  - это автоматически включает shadow/live Variant C через `MOVEMENT_POLICY_MODE`.

- ✅ Фаза 5 (schema/replay bootstrap, без полного retrain):
  - добавлены optional action-head ключи `move_intent_i` и `move_mode_i` (флаг `MOVEMENT_ACTION_SCHEMA=variant_c`),
  - model/enemy movement-loop умеют читать эти ключи как `intent_override`/`allow_advance_override`,
  - `train.py` собирает новые головы автоматически, если они присутствуют в `env.action_space`.

⚠️ Полный retrain и метрики parity по сидовому батчу остаются следующим шагом.

Дальше можно переходить к следующим шагам (расширение охвата на enemy RL/heur и более точные intent-score правила).
