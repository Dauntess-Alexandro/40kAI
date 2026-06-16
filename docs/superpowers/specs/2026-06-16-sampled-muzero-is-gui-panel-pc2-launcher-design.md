# Sampled MuZero — IS GUI-панель + ПК2-лаунчер (Design Spec)

**Дата:** 2026-06-16
**Статус:** утверждён пользователем (брейншторм), готов к плану.
**Автор:** AI-агент + ревью пользователя.

## Цель

Достроить паритет Sampled MuZero remote-IS с gmz/az по двум пунктам (оба отмечены как «отложено» в
`docs/superpowers/specs/2026-06-15-sampled-muzero-remote-is-design.md`):
1. **Выделенная GUI-панель «Inference Server»** во вкладке Sampled MuZero (как `GmzInferenceServerPanel.qml`):
   тумблер LAN + host/port/timeout/auth/weights_share, сохраняемые в `runtime/state/remote_is_smz.json`.
2. **ПК2-лаунчер**: пункт «Sampled MuZero inference server» в общем окне `Pc2Launcher.qml`, запускающий
   `tools/pc2_remote_smz_is.bat`.

По умолчанию LAN выкл (как у gmz: активен только при `user_enabled_lan`). Движок remote-IS (сервер/конфиг/
train.py/ПК2-bat) уже готов в прошлом цикле — это только GUI/лаунчер-обвязка.

## Контекст и решения брейншторма

- **Паритет с gmz/az** — копируем существующие паттерны, не изобретаем.
- **Стор — параметризовать `app/gui_qt/remote_is_store.py`** (добавить `filename="remote_is.json"`,
  обратносовместимо; sampled зовёт с `"remote_is_smz.json"`). DRY, без копии модуля. Утверждено пользователем.
- **ПК2-роль** добавляется в реестр `_ROLES` (`app/gui_qt/pc2_launcher_backend.py`) — окно рендерит роли из
  `pc2_roles()`, отдельный QML-код не нужен.

## Существующие точки (эталоны)

- `app/gui_qt/qml/components/GmzInferenceServerPanel.qml` — панель-образец.
- `app/gui_qt/remote_is_store.py` — стор `remote_is.json` (`DEFAULT_REMOTE_IS`, `normalize_remote_is`,
  `load_remote_is`/`save_remote_is`/`remote_is_config_path`/`remote_is_lan_active`,
  `apply_remote_is_to_qsettings`/`load_remote_is_from_qsettings`). Сейчас путь хардкодит `remote_is.json`.
- `app/gui_qt/main.py` — контроллер: `self._remote_is = load_remote_is(self._repo_root)` (стр. ~502),
  использование в train-launch (стр. ~6420), панель-биндинги для gmz.
- `app/gui_qt/qml/Main.qml` — где показывается `GmzInferenceServerPanel` во вкладке GMZ.
- `app/gui_qt/pc2_launcher_backend.py` — `Pc2Role(id,label,script,port,...)` + `_ROLES` (есть
  dqn_actors/az_actors/az_inference/gmz_inference); `pc2_roles()`/`resolve_role()`.

## Секция 1 — Параметризация стора

`remote_is_store.py`: во все функции, оперирующие путём, добавить аргумент `filename: str = "remote_is.json"`:
- `remote_is_config_path(repo_root, filename="remote_is.json")`.
- `load_remote_is(repo_root, filename="remote_is.json")`, `save_remote_is(repo_root, data, filename=...)`.
- `DEFAULT_REMOTE_IS["port"]` остаётся 5555 (gmz-дефолт); sampled-вызовы передают `port=5560` через данные/
  дефолт панели, НЕ меняя глобальный DEFAULT. Чтобы sampled имел корректный дефолт-порт, либо панель/контроллер
  задаёт 5560 при отсутствии файла, либо добавить тонкий хелпер `load_remote_is_smz(repo_root)` =
  `load_remote_is(repo_root, "remote_is_smz.json")` с пост-применением дефолт-порта 5560, если файла нет.
  Реализация — на усмотрение плана; ключевое: gmz-путь без аргумента не меняется (тест).
- `qsettings`-функции при необходимости получают префикс (`remote_is_smz/...`) — опционально; для v1 достаточно
  json-файла (gmz qsettings можно не дублировать, если sampled грузится только из json).

## Секция 2 — GUI-панель

`app/gui_qt/qml/components/SmzInferenceServerPanel.qml` — зеркало `GmzInferenceServerPanel.qml`, биндинги на
SMZ-свойства контроллера. `main.py`:
- `self._remote_is_smz = load_remote_is(self._repo_root, "remote_is_smz.json")` (с дефолт-портом 5560).
- Свойства/сигналы/слоты для панели (мирроры gmz: enabled/host/port/timeout/auth/weights_share + save).
- В train-launch (Task 8 уже читает `remote_is_smz.json` инлайн) — переключить на стор (`self._remote_is_smz`)
  для единообразия; host/port/auth берутся оттуда.
- `Main.qml` — вставить `SmzInferenceServerPanel` во вкладку Sampled MuZero (там же по структуре, где gmz-панель
  в своей вкладке).

## Секция 3 — ПК2-лаунчер

`app/gui_qt/pc2_launcher_backend.py` — в `_ROLES` добавить:
```python
Pc2Role(
    id="smz_inference",
    label="Sampled MuZero inference server",
    script="tools/pc2_remote_smz_is.bat",
    port=5560,
    ...  # остальные поля Pc2Role — как у gmz_inference
)
```
Сверить полный набор полей `Pc2Role` (dataclass) и заполнить по образцу `gmz_inference`.

## Секция 4 — Тесты

1. `tests/...` стор: `save_remote_is(root, {...}, "remote_is_smz.json")` → `load_remote_is(root, "remote_is_smz.json")`
   round-trip; `user_enabled_lan`-нормализация (enabled без флага → выкл); дефолт-порт 5560 для sampled-хелпера.
2. **Регресс gmz-стора:** `load_remote_is(root)` без аргумента всё ещё читает/пишет `remote_is.json` (дефолт не сломан).
3. ПК2-роль: `resolve_role("smz_inference")` → script=`tools/pc2_remote_smz_is.bat`, port=5560; присутствует в
   `pc2_roles()`.
4. QML: `pyside6-qmllint SmzInferenceServerPanel.qml` (только error/syntax); offscreen-импорт `app.gui_qt.main`.

## Секция 5 — Риски

- Параметризация стора ломает gmz → тест регресса дефолтного пути (Секция 4.2).
- Дубль чтения remote_is_smz.json (Task 8 инлайн + новый стор) → переключить Task-8-инлайн на стор, убрать дубль.
- Порт-дефолт: глобальный `DEFAULT_REMOTE_IS["port"]=5555` (gmz) — для sampled задать 5560 на уровне sampled-хелпера/
  панели, не меняя глобальный дефолт (иначе сломается gmz-дефолт).
- Секрет `auth_token` в `remote_is_smz.json` — файл уже в `.gitignore` (прошлый цикл).

## Критерий готовности

- Во вкладке Sampled MuZero есть панель «Inference Server»: тумблер LAN + поля host/port/auth, сохраняются в
  `remote_is_smz.json`; train-launch берёт их из стора.
- В окне ПК2-лаунчера есть пункт «Sampled MuZero inference server» → запускает `pc2_remote_smz_is.bat` (порт 5560).
- gmz-стор/панель не сломаны; тесты (Секция 4) зелёные; `pyside6-qmllint` чист; offscreen-импорт OK.
