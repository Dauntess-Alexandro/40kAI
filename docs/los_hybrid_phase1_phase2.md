# Hybrid LOS — Phase 1 и Phase 2 (внедрение)

## Что реализовано

### Phase 1: LOS-ядро
В `warhamEnv` добавлены функции:
- генерация сэмплов модели (`_build_model_samples`),
- трассировка луча по клеткам (`_line_cells_between_points`),
- проверка блокеров terrain/models (`_terrain_blocks_los`, `_models_blocking_los`, `_has_clear_los`),
- расчёт model-level LOS (`_check_model_los`),
- unit-level агрегация (`_check_unit_visibility`) через контракт `evaluate_unit_visibility`.

Текущая версия terrain-блокеров учитывает `self.terrain_blocks` (если доступно).
Если `terrain_blocks` не задан, блокировка terrain считается пустой (без падений).

### Phase 2: интеграция в боевые проверки
- `get_shoot_targets_for_unit(...)` теперь фильтрует цели по LOS после range-проверки.
- Overwatch-кандидаты теперь требуют одновременно range + LOS.
- Если LOS не проходит, пишется диагностическая строка с причинами и статистикой лучей.

## Логи для агентов
- Логи включены по умолчанию: `VERBOSE_LOGS=1`, если переменная не задана извне.
- Любое сообщение через `_log(...)` теперь пишется не только в активный IO, но и в оба файла:
  - `LOGS_FOR_AGENTS_TRAIN.md`
  - `LOGS_FOR_AGENTS_PLAY.md`

Это сделано для полной наблюдаемости train/play в едином формате timestamp + message.

## Ограничения текущего шага
- `UnitVisible`/`UnitFullyVisible` пока агрегируются на уровне пары `observer_unit -> target_unit` как минимум по модельной проверке для выбранной цели.
- Для более детального multi-model полного юнита потребуется расширение map `unit->models` в следующем шаге.
