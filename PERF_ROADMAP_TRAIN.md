# 40kAI: план ускорения тренировки (от лёгкого к сложному)

Цель: ускорить training throughput в **2–3x** (или максимально близко) без поломки игровой логики и с контролем качества.

---

## 0) База перед оптимизацией (обязательно)

### 0.1. Что меряем (единый baseline)
- Время на 1k env-шагов.
- Эпизодов/сек (it/s в GUI + фактический wall-clock).
- `[PERF]` метрики из train:
  - `action_ms`, `enemy_turn_ms`, `env_step_ms`,
  - `replay_sample_ms`, `train_fwd_ms`, `train_bwd_ms`,
  - `log_ms`.
- Утилизация CPU/GPU (минимум по `nvidia-smi`/Task Manager, если есть CUDA).

### 0.2. Условия честного сравнения
- Одинаковый roster/mission/NUM_ENVS/seed (где возможно).
- Один и тот же горизонт замера (например 10–20 минут или фиксированные 20k шагов).
- Отдельные прогоны для:
  - `train8` (subprocess env),
  - `selfplay` (без subprocess, как сейчас).

---

## 1) Лёгкие изменения (Quick wins, 0.5–1 день)

## 1.1. Speed-профиль логирования (уже частично готово)
**Что делаем**
- Для speed-режима жёстко:
  - `TRAIN_LOG_ENABLED=0`
  - `TRAIN_LOG_TO_CONSOLE=0`
  - `TRAIN_LOG_TO_FILE=0`
  - `REWARD_DEBUG=0`
  - `LOG_EVERY=1000+`

**Ожидаемый эффект**: +5–15%.

**Риск**: низкий (меньше диагностики в realtime).

---

## 1.2. CUDA-путь по умолчанию для speed
**Что делаем**
- Если доступна CUDA, включать:
  - `USE_AMP=1`
  - `USE_COMPILE=1` (с fallback)
  - `PREFETCH=1`
  - `PIN_MEMORY=1`

**Ожидаемый эффект**: +10–30% на train-части.

**Риск**: низкий/средний (стабильность `torch.compile` зависит от окружения).

---

## 1.3. Быстрый гиперпараметр-тюнинг под throughput
**Что делаем**
- Подобрать связку `NUM_ENVS` и `UPDATES_PER_STEP` так, чтобы `update_ratio` не был слишком низким.
- Для speed обычно:
  - `NUM_ENVS=10..16`,
  - `UPDATES_PER_STEP=8..12`,
  - `batch_size=256`.

**Ожидаемый эффект**: +10–25%.

**Риск**: низкий/средний (изменение шума обучения).

---

## 2) Средние по сложности (2–5 дней)

## 2.1. F — убрать IPC `sample_action` в epsilon-random
**Что делаем**
- Генерируем random action в train-процессе по форме action-space.
- В subprocess больше не вызываем `("sample_action", None)` на каждый env.

**Ожидаемый эффект**: +5–12% (особенно при высоком epsilon и большом NUM_ENVS).

**Риск**: низкий при корректном совпадении распределения с env sampler.

---

## 2.2. A — Lean info для train-mode
**Что делаем**
- В subprocess `step` возвращаем облегчённый `info` (только нужные train поля).
- Полный `info` оставляем для debug/eval/GUI-режимов.

**Минимальный состав train-info**
- `model health`, `player health`, `in attack`,
- `model VP`, `player VP`, `mission`,
- `end reason`, `winner`, `turn`.

**Ожидаемый эффект**: +10–25% в subprocess-режиме.

**Риск**: средний (важно не потерять поля, которые читает train-аналитика).

---

## 2.3. C — упрощение reward-heavy части step
**Что делаем**
- Разделить reward-компоненты на:
  - критичные (каждый шаг),
  - вторичные (реже/инкрементально).
- Уменьшить число дорогих повторных проверок в одном step.

**Ожидаемый эффект**: +8–20%.

**Риск**: средний (может измениться форма reward).

---

## 2.4. J — реальный async replay prefetch (поток)
**Что делаем**
- Не просто хранить “следующий sample”, а вынести подготовку следующего batch в фон.
- Основной поток забирает готовый batch из очереди.

**Ожидаемый эффект**: +5–20% на update-path.

**Риск**: средний (потокобезопасность replay и PER update).

---

## 3) Сложные архитектурные изменения (Deep changes)

## 3.1. D — PER sum-tree / segment-tree
**Что делаем**
- Полностью заменить текущее O(N) sampling на дерево префиксных сумм:
  - sample: O(log N),
  - update priority: O(log N).

**Ожидаемый эффект**: +10–30% (иногда выше на больших буферах).

**Риск**: средний/высокий (критично для стабильности PER).

---

## 3.2. B — кэш distance/target внутри env фаз
**Что делаем**
- Кэшировать distance-матрицы и доступные цели на фазу.
- Чёткая invalidation-схема после movement/charge/casualty.

**Ожидаемый эффект**: +15–40% на env-time.

**Риск**: высокий (устаревшие кэши = логические ошибки боя).

---

## 3.3. Опционально: Cython/Numba для hot loops
**Что делаем**
- Ускорить горячие участки distance/target scan.
- Выбирать только после стабилизации чисто-Python оптимизаций.

**Ожидаемый эффект**: +10–35% поверх B/C (зависит от профиля CPU).

**Риск**: высокий (поддержка сборки, переносимость Windows).

---

## 4) Порядок внедрения (рекомендуемый)
1. **Quick wins**: логи + CUDA flags + тюнинг env/update/batch.
2. **F + A**: убрать лишний IPC + облегчить payload.
3. **C**: безопасная оптимизация reward-step без изменения core-правил.
4. **D**: PER sum-tree.
5. **J**: async prefetch.
6. **B**: env cache (самая рискованная и самая “вкусная” по env-времени).
7. **Cython/Numba** только если после 1–6 всё ещё мало.

---

## 5) Контроль качества (чтобы не ускорить “в никуда”)

После каждого шага:
- Снимать `[PERF]` до/после (минимум 10–20 минут рантайма).
- Сравнивать:
  - средний reward,
  - winrate,
  - VP diff,
  - распределение end_reason.
- Если деградация качества > допустимого порога:
  - откат,
  - частичный rollback конкретной оптимизации.

Рекомендуемые пороги (можно уточнить):
- throughput: +10% минимум, иначе фича не окупилась;
- качество: падение winrate не более 2–4 п.п. на коротком прогоне.

---

## 6) Готовые целевые профили

## 6.1. Speed profile (максимум скорости)
- `NUM_ENVS=12`
- `USE_SUBPROC_ENVS=1` (кроме self-play)
- `UPDATES_PER_STEP=10`
- `batch_size=256`
- `warmup_steps=2000`
- `USE_AMP=1`
- `USE_COMPILE=1`
- `PREFETCH=1`
- `PIN_MEMORY=1`
- `TRAIN_LOG_ENABLED=0`
- `TRAIN_LOG_TO_CONSOLE=0`
- `TRAIN_LOG_TO_FILE=0`
- `LOG_EVERY=1000`

## 6.2. Balance profile (скорость + стабильность)
- `NUM_ENVS=8`
- `USE_SUBPROC_ENVS=1` (кроме self-play)
- `UPDATES_PER_STEP=6..8`
- `batch_size=320` (или 384, если GPU тянет)
- `warmup_steps=5000`
- `USE_AMP=1`
- `USE_COMPILE=0/1` по стабильности
- `PREFETCH=1`
- `PIN_MEMORY=1`
- `TRAIN_LOG_ENABLED=1`
- `TRAIN_LOG_TO_CONSOLE=0`
- `TRAIN_LOG_TO_FILE=0`
- `LOG_EVERY=300..500`

---

## 7) План задач в формате backlog

### Sprint 1 (быстрый прирост)
- [ ] Закрепить speed/balance профили в GUI/env overrides.
- [ ] Бенч baseline + бенч после quick wins.
- [ ] F: убрать `sample_action` IPC.
- [ ] A: lean-info для subprocess step.

### Sprint 2 (архитектурный)
- [ ] D: PER sum-tree + тесты корректности.
- [ ] J: async replay prefetch (с thread-safe доступом).

### Sprint 3 (env deep)
- [ ] B: кэш distance/targets + strict invalidation.
- [ ] C: оптимизация reward-heavy step логики.
- [ ] (опц.) Cython/Numba hot loops.

