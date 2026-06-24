# Remote IS: авто-republish cfg при obs-мисматче + понятная ошибка сервера — дизайн

Дата: 2026-06-24
Статус: согласован заказчиком

## Цель

Убрать ручную возню при изменении размера obs (напр. включили phase_obs → 17 стало 41):
1. **Авто-republish** `*_remote_search_cfg.json` на шару, если его `obs_dim` не совпадает с текущим
   env (вместо «ensure: создать только если нет» — из-за чего старый cfg переживал изменение).
   Заодно удалять устаревшие `latest_*_policy.pth` (несовпадающие по форме), чтобы сервер
   bootstrap'нул новые.
2. **Понятная ошибка сервера** вместо cryptic `mat1 and mat2 shapes cannot be multiplied
   (1x41 and 17x256)`: при несовпадении ширины входящего obs с obs_dim сети — RU-сообщение
   «obs_dim cfg=17 ≠ запрос=41 → перегенери search_cfg», сервер не падает.

## Контекст (факты из кода)

- `ensure_remote_search_cfg` (`core/models/remote_is_search_cfg_common.py:211`): если cfg есть и
  валиден (`is_valid_search_cfg`) → `action="found"` (используем как есть); иначе publish. **Нет
  сверки obs_dim** — старый cfg на шаре переживает изменение размера obs.
- Меры env: `measure_env_dims_from_roster(roster, build_units)` (`:154`) → `(obs_dim, action_sizes)`;
  учитывает phase_obs (строит env, читает PHASE_OBS_FEATURES). `publish_*_from_repo` уже это делает.
- Билдеры зовут общий ensure: `ensure_gmz_remote_search_cfg`/`smz`/`az`/`gaz` (gmz: `:189`).
- Standalone-сервер `tools/gmz_remote_inference_server.py`: строит net из cfg `obs_dim` (`:103-113`),
  `_process_and_reply` (`:313`) гоняет батч в try/except → `[GMZ][REMOTE_IS] batch_error: {exc}`
  (`:323`). `_send_error(identity, message)` (`:219`) уже есть. SMZ-сервер симметричен.
- Готовый стиль сообщения: `describe_obs_dim_mismatch` (`core/engine/phases/obs_features.py:62`).

## Решения заказчика

- При obs-мисматче republish: **да, авто-удалять старые bootstrap-веса** (полное само-лечение).
- Сервер при obs-мисматче запроса: **понятная ошибка + не падать** (лог + send_error клиенту).

## Архитектура

### Компонент 1 — ensure_remote_search_cfg (общий)

Сигнатура `ensure_remote_search_cfg(... , current_obs_dim_fn: Callable[[], int] | None = None)`.
В ветке «cfg найден & валиден» (`:220`):

```
if current_obs_dim_fn is not None:
    cur = current_obs_dim_fn()            # текущий obs_dim env (measure_env_dims_from_roster)
    cfg_obs = <obs_dim из существующего cfg>
    if cur > 0 and cfg_obs > 0 and cur != cfg_obs:
        log "[REMOTE_IS] obs_dim cfg=cfg_obs ≠ env=cur → перепубликую search_cfg"
        try: os.remove(paths.weights_path)   # устаревшие веса (форма не совпадёт)
        except OSError: pass
        <провалиться в publish ниже>   # не return found
    else: return found
else: return found
```

Билдеры передают `current_obs_dim_fn`:
- общий хелпер `current_env_obs_dim(sync_dir)` в common: резолв ростера (как в publish:
  TRAIN_DATA_PATH / `resolve_roster_path_on_share(sync_dir)`) → `measure_env_dims_from_roster` →
  `obs_dim`. Возвращает 0 при невозможности измерить (тогда сверка пропускается — safe).
- gmz/smz/az/gaz `ensure_*` оборачивают: `current_obs_dim_fn=lambda: current_env_obs_dim(<sync_dir>)`.

Ошибка измерения/удаления — не валит ensure: при любой проблеме поведение откатывается к
прежнему (found/republish), просто без авто-лечения.

### Компонент 2 — серверы (standalone GMZ + SMZ)

- Чистый хелпер `obs_dim_mismatch_message(expected: int, actual: int) -> str | None` (в
  `core/engine/phases/obs_features.py` рядом с `describe_obs_dim_mismatch`): None при совпадении,
  иначе RU-строка «[REMOTE_IS] obs_dim сети=expected ≠ запрос=actual. Перегенери search_cfg на ПК1
  (tools\write_*_remote_search_cfg.bat) и удали старые latest_*_policy.pth».
- Сервер: сохранить `self._obs_dim` из search_cfg. В `_process_and_reply` ДО инференса —
  для каждого запроса проверить ширину obs (`np.asarray(obs).shape[-1]`); при несовпадении:
  `_log(msg)` + `_send_error(identity, msg)` для этого клиента, исключить из батча; остальные —
  как обычно. Сервер продолжает работу.

## Поток (после фикса)

```
ПК1 GUI/ensure → cfg на шаре есть → measure env obs_dim → ≠ cfg → republish cfg(41) + rm weights
ПК2 сервер старт → cfg=41 → net(41) → весов нет → bootstrap 41 → ok
если всё же прилетел 41 на net=17 → сервер: лог+send_error «перегенери cfg», не падает
```

## Тестирование (TDD)

- `tests/models/test_remote_is_obs_mismatch.py`:
  - ensure: tmp share с cfg(obs_dim=17) + fake publish-callback (пишет cfg(41)) + `current_obs_dim_fn=lambda:41`
    → ветка republish: publish вызван, weights-файл удалён, action!="found".
  - ensure: cfg(41) + fn→41 → action=="found", publish НЕ вызван, weights на месте.
  - ensure: fn=None → "found" (back-compat).
- `tests/core/telemetry/` или `tests/engine/` для `obs_dim_mismatch_message`: совпадение→None;
  несовпадение→строка содержит оба числа и «search_cfg».

## Definition of Done

1. Тесты ensure-mismatch + message зелёные (TDD).
2. Существующие remote_search_cfg-тесты не сломаны (`tests/test_*_remote_search_cfg_builder.py`,
   `tests/test_remote_is_search_cfg_registry.py`).
3. ruff чист.
4. Серверы (gmz+smz) импортируются; проверка obs встроена в `_process_and_reply`.
5. Коммит только релевантного кода.

## Не-цели (YAGNI)

- In-process (local IS) сервер `core/models/*_inference_server.py` — не трогаем (боль в remote/standalone);
  при желании зеркалим позже.
- Авто-переобучение/конвертация весов под новый obs — нет (bootstrap генерит свежие).
- Изменение формата cfg/протокола — нет.

## Риски

- `current_obs_dim_fn` строит env (через roster) на каждом ensure — лёгкий оверхед, но ensure
  вызывается редко (старт remote IS), приемлемо. При ошибке измерения → откат к старому поведению.
- Удаление weights на шаре: только при подтверждённом obs-мисматче; safe-guard try/except.
