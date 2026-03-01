# Hybrid LOS — Phase 0 (контракт и правила)

## Цель фазы 0

Зафиксировать единый контракт LOS до интеграции в `warhamEnv`:
- одинаковые термины (Model/Unit Visible + Fully Visible),
- единые флаги правил (кто "прозрачный" для LOS),
- единый формат результата для логов и UI.

Фаза 0 **не меняет текущее поведение игры**. Это подготовка API и правил.

## Что принято в контракте

### 1) Model Visible
Модель считается видимой, если есть хотя бы один успешный луч между сэмплами observer и target.

### 2) Unit Visible
Юнит считается видимым, если хотя бы одна его модель видима.

### 3) Model Fully Visible
Модель считается полностью видимой, если все обязательные фронтальные сэмплы цели доступны по LOS.

### 4) Unit Fully Visible
Юнит считается полностью видимым, если каждая его модель fully visible.

## Флаги правил (Wahapedia-aware)

- `see_through_observer_unit_models=True` — можно видеть сквозь другие модели своего юнита.
- `see_through_target_unit_models_for_full=True` — для проверки unit fully visible можно видеть сквозь модели наблюдаемого юнита.
- `block_by_terrain=True` — terrain блокирует LOS.
- `block_by_models=True` — прочие модели блокируют LOS.

## Формат результата

`LosCheckResult` возвращает:
- `visible: bool`
- `fully_visible: bool`
- `reason_codes: tuple[LosReason, ...]`
- `passed_rays: int`
- `total_rays: int`

Это позволяет объяснять игроку/логам, **почему** LOS есть/нет.

## Где лежит контракт

`gym_mod/gym_mod/engine/los_contract.py`

Ключевые сущности:
- `LosReason`
- `LosRuleFlags`
- `LosSamplingConfig`
- `LosCheckRequest`
- `LosCheckResult`
- `UnitLosSummary`
- `evaluate_unit_visibility(...)`

## Что будет в Phase 1

- генерация сэмплов (5–9 точек),
- raycast по сетке/террейну,
- выдача `LosCheckResult` для model->model,
- unit-агрегация через `evaluate_unit_visibility(...)`.
