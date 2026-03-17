# Аудит движения модели (2026-03-17)

## Вердикт
- Статус: **Частично / ближе к "Нет" для Variant C/Cell-head**.
- По факту в play-ране модель двигалась по legacy `move`-направлению (`right`) с выбором reachable-клетки вдоль этого направления.
- Признаки Variant C / cell-head (`[MOVE][INTENT]`, `[MOVE][CELL_HEAD]`, `[MOVE][VARC]`) в логах отсутствуют.

## Хронология
1. Train стартовал с `USE_SUBPROC_ENVS=1`.
2. Viewer (play) запущен в greedy режиме (exploration=0), затем прошли деплой и ходы.
3. В movement phase у MODEL дважды выбран `right`, `advance=да`, `distance=6`.

## Ключевые доказательства
- `LOGS_FOR_AGENTS_TRAIN.md`: фиксируется только `USE_SUBPROC_ENVS=1` на старте.
- `LOGS_FOR_AGENTS_PLAY.md`: есть `[MOVE][DEBUG]` и `Выбор: right`, но нет `[MOVE][INTENT]`, `[MOVE][CELL_HEAD]`, `[MOVE][VARC]`.
- `results.txt`: есть агрегированный результат запуска, но без движения/флагов movement policy.

## Root cause (по коду)
- По умолчанию:
  - `MOVEMENT_ACTION_SCHEMA=legacy`
  - `MOVEMENT_POLICY_MODE=legacy`
  - `MOVEMENT_CELL_HEAD_MODE=off`
- В `gui_qt/main.py` при запуске play/train эти переменные не проставляются.
- Поэтому action-space не получает `move_intent_i/move_mode_i/move_cell_selector_i`, и ветка Variant C в `_pick_destination_from_overlay` не активируется.

## Что делать
1. Для проверки live-режима Variant D/Cell-head запускать с:
   - `MOVEMENT_ACTION_SCHEMA=variant_c`
   - `MOVEMENT_POLICY_MODE=variant_d_cell_live`
   - `MOVEMENT_CELL_HEAD_MODE=live`
   - `MOVEMENT_CELL_HEAD_TOPK=12`
2. В логах ожидать маркеры:
   - `[MOVE][VARC] mode=variant_d_cell_live ...`
   - `[MOVE][INTENT] ...`
   - `[MOVE][CELL_HEAD] mode=live selector=... topk=...`
3. Если нет — добавить явный runtime dump флагов в старт play/train.
