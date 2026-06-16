# Sampled MuZero — IS GUI-панель + ПК2-лаунчер Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Достроить паритет sampled remote-IS с gmz: выделенная GUI-панель «Inference Server» во вкладке Sampled MuZero (LAN host/port/auth → `remote_is_smz.json`) + пункт «Sampled MuZero inference server» в ПК2-лаунчере.

**Architecture:** Параметризуем общий стор `remote_is_store.py` (аргумент `filename`, дефолт сохраняет gmz). Контроллер в `main.py` получает параллельный набор sampled remote-IS свойств/слотов (backed `self._remote_is_smz`), check-connection реюзает общий `gmz_inference_transport.remote_health_check` (протокол shared). Панель `SmzInferenceServerPanel.qml` — зеркало gmz-панели с переименованными биндингами; ПК2-роль — запись в `_ROLES`.

**Tech Stack:** Python 3.12, PySide6/QML, pytest. Windows. Тесты на CPU/offscreen.

**Спека:** `docs/superpowers/specs/2026-06-16-sampled-muzero-is-gui-panel-pc2-launcher-design.md`.

---

## Файловая структура

**Создаём:**
- `app/gui_qt/qml/components/SmzInferenceServerPanel.qml` — панель (зеркало `GmzInferenceServerPanel.qml`).
- `tests/gui/test_remote_is_store_filename.py` — стор round-trip + gmz-регресс.
- `tests/gui/test_pc2_roles_smz.py` — ПК2-роль smz_inference.

**Модифицируем:**
- `app/gui_qt/remote_is_store.py` — параметр `filename="remote_is.json"`.
- `app/gui_qt/pc2_launcher_backend.py` — роль `smz_inference` в `_ROLES`.
- `app/gui_qt/main.py` — контроллер: sampled remote-IS свойства/слоты + `self._remote_is_smz`; переключить Task-8 инлайн-чтение remote на стор.
- `app/gui_qt/qml/Main.qml` — смонтировать `SmzInferenceServerPanel` во вкладке Sampled MuZero.

**Переиспользуем:** `GmzIsToggleRow.qml`, `ChamferPanel.qml` (generic), `core.models.gmz_inference_transport.remote_health_check` (протокол shared), `core.models.smz_remote_search_cfg_builder` (для подсказки путей весов).

---

## Task 1: Параметризация стора + тесты

**Files:**
- Modify: `app/gui_qt/remote_is_store.py`
- Create: `tests/gui/test_remote_is_store_filename.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/gui/test_remote_is_store_filename.py
from app.gui_qt.remote_is_store import (
    load_remote_is, save_remote_is, remote_is_config_path,
)


def test_filename_param_roundtrip_smz(tmp_path):
    data = {"user_enabled_lan": True, "host": "192.168.1.50", "port": 5560, "auth_token": "tok"}
    save_remote_is(tmp_path, data, filename="remote_is_smz.json")
    assert (tmp_path / "runtime" / "state" / "remote_is_smz.json").is_file()
    loaded = load_remote_is(tmp_path, filename="remote_is_smz.json")
    assert loaded["host"] == "192.168.1.50"
    assert loaded["port"] == 5560
    assert loaded["user_enabled_lan"] is True
    assert loaded["enabled"] is True


def test_gmz_default_filename_unchanged(tmp_path):
    # Регресс: без filename — прежний remote_is.json
    save_remote_is(tmp_path, {"user_enabled_lan": True, "host": "10.0.0.1"})
    assert (tmp_path / "runtime" / "state" / "remote_is.json").is_file()
    assert not (tmp_path / "runtime" / "state" / "remote_is_smz.json").is_file()
    assert load_remote_is(tmp_path)["host"] == "10.0.0.1"
    assert remote_is_config_path(tmp_path).name == "remote_is.json"


def test_config_path_filename(tmp_path):
    assert remote_is_config_path(tmp_path, filename="remote_is_smz.json").name == "remote_is_smz.json"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/gui/test_remote_is_store_filename.py -q`
Expected: FAIL — `TypeError: ... unexpected keyword argument 'filename'`.

- [ ] **Step 3: Add filename param to store**

В `app/gui_qt/remote_is_store.py` добавь параметр `filename` (дефолт сохраняет поведение gmz):

```python
def remote_is_config_path(repo_root: str | Path, filename: str = "remote_is.json") -> Path:
    return Path(repo_root) / "runtime" / "state" / str(filename)


def load_remote_is(repo_root: str | Path, filename: str = "remote_is.json") -> dict[str, Any]:
    path = remote_is_config_path(repo_root, filename)
    if not path.is_file():
        return normalize_remote_is({})
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return normalize_remote_is({})
    if not isinstance(raw, dict):
        return normalize_remote_is({})
    before = dict(raw)
    merged = normalize_remote_is(raw)
    if before.get("enabled") != merged.get("enabled") or before.get("user_enabled_lan") != merged.get(
        "user_enabled_lan"
    ):
        try:
            save_remote_is(repo_root, merged, filename)
        except OSError:
            pass
    return merged


def save_remote_is(repo_root: str | Path, data: dict[str, Any], filename: str = "remote_is.json") -> None:
    path = remote_is_config_path(repo_root, filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = normalize_remote_is(data)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
```

(`normalize_remote_is`/`remote_is_lan_active` не трогаем — они работают с dict.)

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/gui/test_remote_is_store_filename.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/remote_is_store.py tests/gui/test_remote_is_store_filename.py
git commit -m "feat(sampled_muzero): параметризация remote_is_store (filename) для remote_is_smz.json"
```

---

## Task 2: ПК2-роль smz_inference + тест

**Files:**
- Modify: `app/gui_qt/pc2_launcher_backend.py`
- Create: `tests/gui/test_pc2_roles_smz.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/gui/test_pc2_roles_smz.py
from app.gui_qt.pc2_launcher_backend import pc2_roles, resolve_role


def test_smz_inference_role_present():
    ids = [r.id for r in pc2_roles()]
    assert "smz_inference" in ids


def test_smz_inference_role_fields():
    r = resolve_role("smz_inference")
    assert r is not None
    assert r.script == "tools/pc2_remote_smz_is.bat"
    assert r.port == 5560
    assert r.requires_gpu is True


def test_gmz_role_still_present():
    assert resolve_role("gmz_inference") is not None  # регресс
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/gui/test_pc2_roles_smz.py -q`
Expected: FAIL — `assert "smz_inference" in ids`.

- [ ] **Step 3: Add role to _ROLES**

В `app/gui_qt/pc2_launcher_backend.py`, в кортеж `_ROLES` добавь (после `gmz_inference`):

```python
    Pc2Role(
        id="smz_inference",
        label="Sampled MuZero inference server",
        script="tools/pc2_remote_smz_is.bat",
        requires_gpu=True,
        port=5560,
        note="GPU inference :5560 (Sampled MuZero). Свой порт — можно вместе с gmz/az на разных портах.",
    ),
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/gui/test_pc2_roles_smz.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/pc2_launcher_backend.py tests/gui/test_pc2_roles_smz.py
git commit -m "feat(sampled_muzero): ПК2-лаунчер роль smz_inference (порт 5560)"
```

---

## Task 3: Контроллер sampled remote-IS в main.py

**Files:** Modify `app/gui_qt/main.py`

> Зеркало gmz remote-IS контроллер-членов. Изучи (Grep по main.py) ВСЕ gmz remote-IS свойства/слоты:
> `remoteIsEnabled`, `setRemoteIsEnabled`, `remoteIsHost`/`setRemoteIsHost`, `remoteIsPort`/`setRemoteIsPort`,
> `remoteIsTimeout`/`setRemoteIsTimeout`, `remoteIsAuthToken`/`setRemoteIsAuthToken`,
> `remoteIsWeightsPath`/`setRemoteIsWeightsPath`, `remoteIsSmbUncHint`/`setRemoteIsSmbUncHint`,
> `checkRemoteIsConnection`, `remoteIsStatusText`, `remoteIsLatencyText`, `gmzInferenceServerEnabled`,
> `set_gmz_inference_server_mode`, `gmzLocalIsTooltip`, `gmzLanIsTooltip`, и поле `self._remote_is`.
> Для КАЖДОГО заведи sampled-двойник с префиксом `smz`/`Smz`, backed `self._remote_is_smz`.

- [ ] **Step 1: Load sampled remote-IS state in __init__**

Рядом с `self._remote_is = load_remote_is(self._repo_root)` (~стр. 502) добавь:

```python
        self._remote_is_smz: dict = load_remote_is(self._repo_root, "remote_is_smz.json")
        if not (self._repo_root and (self._repo_root / "runtime" / "state" / "remote_is_smz.json").is_file()):
            self._remote_is_smz["port"] = 5560  # дефолт-порт sampled (gmz=5555)
```

- [ ] **Step 2: Mirror gmz remote-IS Qt properties/slots as smz**

Скопируй gmz remote-IS свойства/сигналы/слоты (найди их по грепу `remoteIs` в main.py) под именами smz*, заменив:
- backing-поле `self._remote_is` → `self._remote_is_smz`.
- имена Qt-свойств `remoteIsHost`→`smzRemoteIsHost`, `remoteIsPort`→`smzRemoteIsPort`, `remoteIsTimeout`→`smzRemoteIsTimeout`, `remoteIsAuthToken`→`smzRemoteIsAuthToken`, `remoteIsWeightsPath`→`smzRemoteIsWeightsPath`, `remoteIsSmbUncHint`→`smzRemoteIsSmbUncHint`, `remoteIsEnabled`→`smzRemoteIsEnabled`, `remoteIsStatusText`→`smzRemoteIsStatusText`, `remoteIsLatencyText`→`smzRemoteIsLatencyText`.
- слоты `setRemoteIsHost`→`setSmzRemoteIsHost` и т.д.; `setRemoteIsEnabled`→`setSmzRemoteIsEnabled`; `checkRemoteIsConnection`→`checkSmzRemoteIsConnection`.
- save: каждый setter пишет через `save_remote_is(self._repo_root, self._remote_is_smz, "remote_is_smz.json")`.
- `gmzInferenceServerEnabled`/`set_gmz_inference_server_mode` (Local toggle, читает/пишет hyperparam `inference_server_enabled`) → `smzInferenceServerEnabled`/`set_smz_inference_server_mode` (читает/пишет `self._smz_hyperparams["inference_server_enabled"]`).
- `gmzLocalIsTooltip`/`gmzLanIsTooltip` → `smzLocalIsTooltip`/`smzLanIsTooltip` (тексты RU про sampled; порт 5560, bat `pc2_remote_smz_is.bat`).
- `checkSmzRemoteIsConnection`: реюзай тот же транспорт-health-check, что gmz (найди, что вызывает `checkRemoteIsConnection` — обычно `from core.models.gmz_inference_transport import remote_health_check`; вызови с `self._remote_is_smz["host"/"port"/"auth_token"]`). Протокол общий — отдельного smz health-check НЕ нужно.
- mutual-exclusion Local↔LAN: повтори gmz-логику (включение LAN гасит Local и наоборот), но на smz-полях.

- [ ] **Step 3: Switch Task-8 inline remote read to the store**

Найди в train-launch ветке sampled (где Task 8 инлайн читал `remote_is_smz.json` через `json.loads`) — замени на использование `self._remote_is_smz` (или `load_remote_is(self._repo_root, "remote_is_smz.json")`) и `remote_is_lan_active`, чтобы не было дубля логики чтения. Экспорт env `SMZ_INFERENCE_REMOTE_HOST/PORT/AUTH_TOKEN` и `SMZ_INFERENCE_SERVER_MODE=remote` — из этого dict, когда `user_enabled_lan`.

- [ ] **Step 4: Verify**

Run: `set QT_QPA_PLATFORM=offscreen` (через env) и
`QT_QPA_PLATFORM=offscreen python -c "import app.gui_qt.main; print('main OK')"`
Expected: `main OK`.
Run: `python -c "import app.gui_qt.main as m; c=m.__dict__; print('has GuiController' , 'GuiController' in c or True)"` (sanity import).

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/main.py
git commit -m "feat(sampled_muzero): контроллер remote-IS (smz* свойства/слоты, remote_is_smz.json, check-connection)"
```

---

## Task 4: Панель SmzInferenceServerPanel.qml + монтаж в Main.qml

**Files:**
- Create: `app/gui_qt/qml/components/SmzInferenceServerPanel.qml`
- Modify: `app/gui_qt/qml/Main.qml`

- [ ] **Step 1: Mirror the panel**

Скопируй `app/gui_qt/qml/components/GmzInferenceServerPanel.qml` → `SmzInferenceServerPanel.qml` и замени биндинги контроллера gmz→smz (таблица):
- `controller.gmzInferenceServerEnabled` → `controller.smzInferenceServerEnabled`
- `controller.remoteIsEnabled` → `controller.smzRemoteIsEnabled`
- `controller.set_gmz_inference_server_mode` → `controller.set_smz_inference_server_mode`
- `controller.setRemoteIsEnabled` → `controller.setSmzRemoteIsEnabled`
- `controller.remoteIsHost`/`setRemoteIsHost` → `controller.smzRemoteIsHost`/`setSmzRemoteIsHost`
- `remoteIsPort`/`setRemoteIsPort` → `smzRemoteIsPort`/`setSmzRemoteIsPort`
- `remoteIsTimeout`/`setRemoteIsTimeout` → `smzRemoteIsTimeout`/`setSmzRemoteIsTimeout`
- `remoteIsAuthToken`/`setRemoteIsAuthToken` → `smzRemoteIsAuthToken`/`setSmzRemoteIsAuthToken`
- `remoteIsWeightsPath`/`setRemoteIsWeightsPath` → `smzRemoteIsWeightsPath`/`setSmzRemoteIsWeightsPath`
- `remoteIsSmbUncHint`/`setRemoteIsSmbUncHint` → `smzRemoteIsSmbUncHint`/`setSmzRemoteIsSmbUncHint`
- `checkRemoteIsConnection` → `checkSmzRemoteIsConnection`
- `remoteIsStatusText`/`remoteIsLatencyText` → `smzRemoteIsStatusText`/`smzRemoteIsLatencyText`
- `controller.gmzLocalIsTooltip`/`gmzLanIsTooltip` → `controller.smzLocalIsTooltip`/`smzLanIsTooltip`
- тексты-литералы: `pc2_remote_is.bat` → `pc2_remote_smz_is.bat`; `latest_gmz_policy.pth` → `latest_smz_policy.pth`; placeholder порт-намёки 5555→5560 если есть.
- `GmzIsToggleRow` — переиспользуй как есть (generic toggle-row).
- `ChamferPanel`/`rootUi`-биндинги — без изменений.

- [ ] **Step 2: Mount in Main.qml**

Найди в `Main.qml`, где для вкладки GMZ показывается `GmzInferenceServerPanel { rootUi: ... }` (грепни `GmzInferenceServerPanel`). В секции/вкладке Sampled MuZero (где сейчас `SectionHyperparamsEditor { algoSection: "smz" }`) добавь рядом:

```qml
SmzInferenceServerPanel {
    Layout.fillWidth: true
    rootUi: <тот же rootUi, что у gmz-панели>
}
```
(точное имя rootUi-объекта и контейнера — сверь с тем, как смонтирована GmzInferenceServerPanel в Main.qml, и повтори 1:1 в smz-вкладке.)

- [ ] **Step 3: Verify QML**

Run: `.venv/Scripts/pyside6-qmllint app/gui_qt/qml/components/SmzInferenceServerPanel.qml app/gui_qt/qml/Main.qml 2>&1 | grep -iE '\berror\b|syntax'`
Expected: пусто (unqualified-access warnings игнор).
Run: `QT_QPA_PLATFORM=offscreen python -c "import app.gui_qt.main; print('gui OK')"`
Expected: `gui OK`.

- [ ] **Step 4: Commit**

```bash
git add app/gui_qt/qml/components/SmzInferenceServerPanel.qml app/gui_qt/qml/Main.qml
git commit -m "feat(sampled_muzero): GUI-панель Inference Server во вкладке Sampled MuZero"
```

---

## Task 5: Сквозная проверка

- [ ] **Step 1: Run all new + regress tests**

Run: `python -m pytest tests/gui/test_remote_is_store_filename.py tests/gui/test_pc2_roles_smz.py tests/engine/test_smz_inference_server.py tests/train/test_sampled_muzero_actor_learner_smoke.py -q`
Expected: ALL PASS.

- [ ] **Step 2: Import + qmllint sweep**

Run: `QT_QPA_PLATFORM=offscreen python -c "import app.gui_qt.main, app.gui_qt.pc2_launcher_backend, app.gui_qt.remote_is_store; print('imports OK')"`
Run: `.venv/Scripts/pyside6-qmllint app/gui_qt/qml/components/SmzInferenceServerPanel.qml 2>&1 | grep -iE '\berror\b' || echo "qml clean"`

- [ ] **Step 3: gmz regress (не сломали стор/панель gmz)**

Run: `python -c "from app.gui_qt.remote_is_store import load_remote_is, remote_is_config_path; print(remote_is_config_path('.').name)"`
Expected: `remote_is.json` (gmz-дефолт цел).

- [ ] **Step 4: Manual GUI note**

Ручная приёмка (пользователь, по AGENTS.md): открыть Qt GUI → вкладка Sampled MuZero → панель «Inference Server» (тумблеры Local/LAN, поля host/port/auth, «Проверить соединение»); ПК2-лаунчер (`python tools/pc2_launcher.py`) → пункт «Sampled MuZero inference server».

- [ ] **Step 5: Final commit (если нужно)**

```bash
git add -A && git commit -m "chore(sampled_muzero): мелкие правки по сквозной проверке IS-панели" || echo "nothing to commit"
```

---

## Self-Review (выполнено при написании плана)

- **Покрытие спеки:** Секция 1 (стор) → Task 1. Секция 2 (панель) → Tasks 3 (контроллер) + 4 (QML/монтаж). Секция 3 (ПК2-роль) → Task 2. Секция 4 (тесты) → Tasks 1,2 + 5. Секция 5 (риски) → тест gmz-регресса (Task 1.2 `test_gmz_default_filename_unchanged`, Task 5.3), переключение Task-8 инлайн на стор (Task 3.3), порт-дефолт 5560 на уровне sampled (Task 3.1, не трогая глобальный DEFAULT_REMOTE_IS).
- **Заглушки:** Task 1/2 — полный код. Task 3 (контроллер) и Task 4 (QML) — точные таблицы замен gmz→smz + конкретные новые строки (load + mount). Это исполнимо (зеркало существующих gmz-членов).
- **Согласованность имён:** свойства `smzRemoteIs{Host,Port,Timeout,AuthToken,WeightsPath,SmbUncHint,Enabled,StatusText,LatencyText}`, `smzInferenceServerEnabled`, слоты `setSmzRemoteIs*`/`setSmzRemoteIsEnabled`/`set_smz_inference_server_mode`/`checkSmzRemoteIsConnection`, тултипы `smzLocalIsTooltip`/`smzLanIsTooltip`, стор `remote_is_smz.json`, роль `smz_inference`→`pc2_remote_smz_is.bat`:5560 — едины в Task 3 (main.py) и Task 4 (QML).
