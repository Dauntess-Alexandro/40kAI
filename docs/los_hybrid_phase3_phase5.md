# Hybrid LOS — Phase 3-5

## Phase 3: детальная наблюдаемость и причины

Добавлено единое лог-сообщение LOS-решений:
- формат `[LOS:<action>] accept/reject ...`
- поля: observer/target, `unit_visible`, `unit_fully_visible`, `reasons`, `rays`.

Логирование применяется в:
- подборе целей стрельбы,
- подборе кандидатов Overwatch.

Это убирает "тишину": теперь видно не только факт отказа, но и конкретную причину.

## Phase 4: LOS-данные в state payload для GUI

В `state_export` расширен payload юнита полем `los`.
Для каждого юнита формируется snapshot до ближайшей живой вражеской цели:
- `nearest_target`
- `visible`
- `fully_visible`
- `reasons`
- `rays_passed`
- `rays_total`

Это позволяет Qt GUI (или viewer/state) показывать LOS-статус без повторного пересчёта в UI.

## Phase 5: качество/производительность

1. **Юнит-агрегация по всем моделям цели**
   - `UnitVisible`: `any(model.visible)`
   - `UnitFullyVisible`: `all(model.fully_visible)`

2. **Тонкая настройка качества LOS через env**
   - `LOS_SAMPLE_COUNT` (default: 5)
   - `LOS_INCLUDE_DIAGONALS` (default: 0)
   - `LOS_FRONT_ARC_SAMPLES` (default: 3)

3. **Сохранена кэш-стратегия**
   - LOS-кэш сбрасывается вместе с инвалидацией target-кэша.

## Важно

`terrain_blocks` продолжает быть опциональным источником блокеров.
Если terrain-маска не задана, LOS не падает и работает только с model blockers.
