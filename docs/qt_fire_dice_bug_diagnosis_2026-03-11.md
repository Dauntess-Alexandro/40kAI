# Диагностика бага Qt GUI (PySide6): залипание `Need: X dice` при смене цели после Cancel

## Что подтверждают свежие логи

- В `LOGS_FOR_AGENTS_PLAY.md` видно старт player shooting-запроса с валидными целями `Unit 11 -> [21, 22]`, затем запрос hit-кубов `20D6`.
- При этом в свежем куске логов **нет отдельной строки про Cancel/повторный выбор цели/пересчёт count**, из-за чего баг трудно восстановить по логам «по шагам UI».
- В `LOGS_FOR_AGENTS_TRAIN.md` рядом со временем сценария идут только `LOS_DEBUG` строки (Line of Sight), без событий UI-последовательности fire popover.

## Где в коде формируется `Need: X dice`

- Плашка `Need: ... dice` обновляется в `viewer/app.py::_update_shoot_popover_ui()`.
- Значение берётся напрямую из `self._pending_request.count`:
  - `dice_mode = getattr(request, "kind", "") == "dice"`
  - `count = int(getattr(request, "count", 0) or 0)`
  - затем `self.shoot_popover_step_summary.setText(f"Need: {count if dice_mode else '—'} dice")`

## Где хранится контекст цели/выстрела

Состояние fire-последовательности в UI держится в полях `ViewerApp`:

- `self._shoot_popover_target_id` — текущая цель поповера,
- `self._shoot_locked_target_id` — зафиксированная цель на этапе dice,
- `self._shoot_resolver_active`, `self._shoot_resolver_step`, `self._shoot_resolver_attacker_id`,
- `self._shoot_targets_valid` — разрешённые цели из target-request,
- и главное: `self._pending_request` — активный request от движка (target или dice).

## Что делает Cancel сейчас

`_close_shoot_popover()` делает только UI-сброс локального резолвера:

- очищает `_shoot_popover_target_id`,
- очищает `_shoot_locked_target_id`,
- сбрасывает `_shoot_resolver_active/_step/_attacker_id`,
- скрывает поповер.

Но **не меняет `self._pending_request`** (он остаётся тем же запросом от движка, нередко `kind="dice"` для уже выбранной прошлой цели).

## Корневая причина

Корень бага — рассинхронизация между UI state и engine request state:

1. На шаге `step==0` в `_shoot_step_action()` после выбора цели отправляется `_submit_answer(target)` и движок отдаёт dice-request с `count`, вычисленным для этой цели.
2. Пользователь нажимает Cancel → `_close_shoot_popover()` стирает `_shoot_locked_target_id` и локальный step, но **не отменяет/не переинициализирует pending dice-request**.
3. При повторном ПКМ по другой цели `_open_shoot_popover()` пропускает выбор, потому что защита от смены цели в dice-режиме работает только если `_shoot_locked_target_id` не `None`; после Cancel он уже `None`.
4. `_update_shoot_popover_ui()` показывает `Need` из старого `pending_request.count` (для предыдущей цели), но уже с новой визуально выбранной целью.

Итог: визуально «цель новая», а `Need: X dice` — от старой цели.

## Варианты фикса

### Вариант A (быстрый, минимальный)

**Идея:** не стирать lock при Cancel, если активен dice-request.

- В `_close_shoot_popover()` условно сохранять `_shoot_locked_target_id`, когда `self._is_shooting_dice_request(self._pending_request)`.
- Тогда `_open_shoot_popover()` не позволит открыть другую цель во время активного dice-request и выдаст понятный лог/подсказку.

**Плюсы:**
- Минимальный diff, быстро чинит конкретный симптом.

**Минусы:**
- Cancel перестаёт быть «полной отменой» шага выбора цели (скорее «закрыть окно»).

**Риск побочек:** низкий/средний (в UX может быть неожиданность у пользователя).

**Сложность:** низкая.

**Тесты:**
- выбрать цель A (rapid), дойти до dice-request, Cancel, ПКМ по цели B → должна появляться блокировка смены цели;
- `Need` должен оставаться согласованным с зафиксированной целью A.

### Вариант B (рекомендованный, более архитектурный)

**Идея:** разделить «закрыть popover» и «отменить fire-sequence».

- Оставить `_close_shoot_popover()` как чисто UI-hide.
- Добавить `_cancel_shoot_sequence()` для Esc/Cancel-кнопки в shooting flow:
  - если pending request = dice, принудительно завершать текущий shot как aborted и возвращаться к target-request (через контроллерный сигнал/служебный ответ),
  - сбрасывать lock + step + target только после подтверждённого rollback со стороны движка.

**Плюсы:**
- UI и движок снова синхронны по жизненному циклу запроса.
- Семантика Cancel становится однозначной.

**Минусы:**
- Нужен протокол отмены между Viewer и engine (`game_io`/request-loop).

**Риск побочек:** средний (затрагивается request-flow).

**Сложность:** средняя/высокая.

**Тесты:**
- интеграционно: target A -> dice -> Cancel -> target B -> новый dice-request с новым count;
- проверка, что в логе есть явные события `shoot_cancelled` и `shoot_retargeted`.

### Вариант C (с защитой от регрессий)

**Идея:** ввести runtime-инварианты и принудительную валидацию `Need` перед показом.

- В `_update_shoot_popover_ui()` добавлять guard:
  - если request `kind=dice`, но target в UI не совпадает с target, для которого был создан request, показывать ошибку состояния и блокировать кнопку Roll.
- Для этого хранить `request.meta["shooter_id"]` и `request.meta["target_id"]` (добавить в engine при генерации dice-request).
- При несоответствии — авто-сброс в безопасное состояние (закрыть popover + требовать повторного выбора цели).

**Плюсы:**
- Ловит не только текущий баг, но целый класс рассинхронов.

**Минусы:**
- Нужны изменения и в движке, и в UI.

**Риск побочек:** средний.

**Сложность:** средняя.

**Тесты:**
- unit-тест инварианта «dice-request всегда привязан к конкретной target_id»;
- UI-тест: искусственно подменить target во время dice-request → кнопка Roll должна блокироваться.

## Что тестировать обязательно (минимум)

1. `target A (rapid) -> Need=20 -> Cancel -> target B (out of rapid)`
   - ожидаем либо новый пересчёт `Need` (после реального re-request), либо явную блокировку смены цели.
2. Повторный Enter после Cancel не должен отправлять dice для «чужой» цели.
3. Логи должны явно фиксировать причину:
   - отмена выстрела,
   - фиксация/снятие lock цели,
   - источник `count` (для какой target_id посчитан).

## Рекомендация

Лучший путь: **Вариант B + один guard из Варианта C**.

- B убирает корневую проблему (рассинхрон UI ↔ engine state).
- Один защитный инвариант из C (привязка dice-request к target_id и проверка перед рендером `Need`) сильно снижает риск повторной регрессии.
- Если нужен hotfix «сегодня», можно сделать A как временный патч и сразу планировать B.
