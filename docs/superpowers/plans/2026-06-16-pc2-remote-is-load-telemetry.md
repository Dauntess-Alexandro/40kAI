# ПК2 нагрузка (GPU+CPU) в телеметрии GUI для SMZ/GMZ remote IS — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Показать нагрузку ПК2 (удалённый inference-сервер) — GPU и CPU — в панели телеметрии Qt GUI при тренировке SMZ/GMZ с включённым LAN remote IS.

**Architecture:** Достраиваем два звена уже существующего конвейера «health_check → проба → карточки». (1) GMZ/SMZ серверы начинают слать системные CPU/RAM в health_check (как уже делает AZ). (2) GUI активирует пробу ПК2 для алго `sampled_muzero` (для `gumbel_muzero`/`alphazero_tree` гейты уже есть). QML и слой карточек (`cards.py`) не меняем — они уже рисуют «ПК2·GPU» и «ПК2·CPU».

**Tech Stack:** Python 3.12, PySide6 (Qt GUI), ZMQ (transport), psutil (CPU/RAM), pytest.

**Spec:** `docs/superpowers/specs/2026-06-16-pc2-remote-is-load-telemetry-design.md`

**Эталон:** AZ уже реализован — `tools/az_remote_inference_server.py:_handle_health` (сэмпл psutil) + `core/models/az_inference_protocol.build_health_response` (cpu/ram-поля). Приводим GMZ/SMZ к этому виду.

---

## File Structure

- **Modify** `core/telemetry/pc2_telemetry.py` — добавить общий хелпер `sample_cpu_ram_system()`; `sample_system_telemetry()` переиспользует его (DRY).
- **Modify** `tools/gmz_remote_inference_server.py` — кэш `self._cpu_name` в `__init__`; сэмпл CPU/RAM в `_handle_health_check`; cpu/ram-поля в `build_health_payload`.
- **Modify** `tools/smz_remote_inference_server.py` — те же три правки (структура идентична GMZ).
- **Modify** `app/gui_qt/main.py` — метод `_smz_remote_cfg_for_telemetry()` + включить его в цепочку `remote_cfg` в `set_context` (строка ~6660).
- **Modify** `tests/telemetry/test_pc2_telemetry.py` — тест нового хелпера.
- **Modify** `tests/telemetry/test_remote_health_payload.py` — cpu/ram в GMZ и SMZ payload.
- **Create** `tests/gui/test_smz_remote_cfg_telemetry.py` — гейт `_smz_remote_cfg_for_telemetry`.

Слой карточек (`app/gui_qt/telemetry/cards.py`) уже покрыт тестами на ПК2·GPU/CPU (`tests/telemetry/test_cards.py::test_pc2_cpu_card_present_and_ordered`) — не трогаем.

---

## Task 1: Общий хелпер системной CPU/RAM-телеметрии

**Files:**
- Modify: `core/telemetry/pc2_telemetry.py`
- Test: `tests/telemetry/test_pc2_telemetry.py`

- [ ] **Step 1: Написать падающий тест**

В конец `tests/telemetry/test_pc2_telemetry.py` добавить:

```python
def test_sample_cpu_ram_system_shape():
    from core.telemetry.pc2_telemetry import sample_cpu_ram_system

    s = sample_cpu_ram_system()
    assert set(s.keys()) == {"cpu_pct_system", "ram_pct_system", "ram_gb_system"}
    for v in s.values():
        assert v is None or isinstance(v, float)
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/telemetry/test_pc2_telemetry.py::test_sample_cpu_ram_system_shape -v`
Expected: FAIL — `ImportError: cannot import name 'sample_cpu_ram_system'`.

- [ ] **Step 3: Реализовать хелпер и переиспользовать его в `sample_system_telemetry`**

В `core/telemetry/pc2_telemetry.py` добавить функцию перед `sample_system_telemetry` (после `detect_cpu_name`):

```python
def sample_cpu_ram_system() -> dict[str, Any]:
    """Мгновенные системные CPU%/RAM% (psutil). Без имени CPU (его кэшируют отдельно).
    Все значения None, если psutil недоступен."""
    cpu_pct = None
    ram_pct = None
    ram_gb = None
    try:
        import psutil

        cpu_pct = float(psutil.cpu_percent(interval=None))
        vm = psutil.virtual_memory()
        ram_pct = float(vm.percent)
        ram_gb = round(float(vm.used) / (1024**3), 1)
    except Exception:
        pass
    return {
        "cpu_pct_system": cpu_pct,
        "ram_pct_system": ram_pct,
        "ram_gb_system": ram_gb,
    }
```

Затем в `sample_system_telemetry()` заменить inline-блок psutil (переменные `cpu_pct/ram_pct/ram_gb` с `try/except psutil`) на:

```python
    sys_cr = sample_cpu_ram_system()
    cpu_pct = sys_cr["cpu_pct_system"]
    ram_pct = sys_cr["ram_pct_system"]
    ram_gb = sys_cr["ram_gb_system"]
```

(Остальное тело `sample_system_telemetry` — GPU-часть и возвращаемый dict с ключами
`cpu_name/cpu_pct_system/ram_pct_system/ram_gb_system` — не меняем.)

- [ ] **Step 4: Запустить тесты — убедиться, что проходят**

Run: `python -m pytest tests/telemetry/test_pc2_telemetry.py -v`
Expected: PASS (новый тест + существующий `test_sample_system_telemetry_shape` не сломан).

- [ ] **Step 5: Коммит**

```bash
git add core/telemetry/pc2_telemetry.py tests/telemetry/test_pc2_telemetry.py
git commit -m "feat(telemetry): хелпер sample_cpu_ram_system для health_check ПК2"
```

---

## Task 2: GMZ-сервер — CPU/RAM в health_check

**Files:**
- Modify: `tools/gmz_remote_inference_server.py` (`build_health_payload` ~343, `__init__` ~162, `_handle_health_check` ~219)
- Test: `tests/telemetry/test_remote_health_payload.py`

- [ ] **Step 1: Написать падающий тест**

В `tests/telemetry/test_remote_health_payload.py` добавить:

```python
def test_gmz_build_health_payload_includes_cpu_ram():
    payload = build_health_payload(
        protocol_version=1, policy_version=7, gpu_name="RTX 2060 SUPER",
        queue_depth=0, uptime_s=5, avg_batch=None,
        gpu_util=10, gpu_mem_used_mb=512, gpu_mem_total_mb=8192, gpu_temp_c=44,
        cpu_name="Ryzen 5 1600", cpu_pct_system=38.0,
        ram_pct_system=31.0, ram_gb_system=5.0,
    )
    assert payload["cpu_name"] == "Ryzen 5 1600"
    assert payload["cpu_pct_system"] == 38.0
    assert payload["ram_pct_system"] == 31.0
    assert payload["ram_gb_system"] == 5.0


def test_gmz_build_health_payload_cpu_ram_default_none():
    payload = build_health_payload(
        protocol_version=1, policy_version=0, gpu_name="cpu",
        queue_depth=0, uptime_s=1, avg_batch=None,
        gpu_util=None, gpu_mem_used_mb=None, gpu_mem_total_mb=None, gpu_temp_c=None,
    )
    assert payload["cpu_pct_system"] is None
    assert payload["cpu_name"] is None
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/telemetry/test_remote_health_payload.py::test_gmz_build_health_payload_includes_cpu_ram -v`
Expected: FAIL — `TypeError: build_health_payload() got an unexpected keyword argument 'cpu_name'`.

- [ ] **Step 3: Расширить `build_health_payload`**

В `tools/gmz_remote_inference_server.py` заменить сигнатуру и тело `build_health_payload`:

```python
def build_health_payload(
    *,
    protocol_version: int,
    policy_version: int,
    gpu_name: str,
    queue_depth: int,
    uptime_s: int,
    avg_batch,
    gpu_util,
    gpu_mem_used_mb,
    gpu_mem_total_mb,
    gpu_temp_c,
    cpu_name: str | None = None,
    cpu_pct_system=None,
    ram_pct_system=None,
    ram_gb_system=None,
) -> dict:
    # cpu_*/ram_* — опциональны (телеметрия CPU/RAM ПК2). Старый ПК2 их не шлёт → None,
    # старый ПК1 (GUI) игнорирует. Обратная совместимость health_check сохраняется.
    return {
        "kind": "health_check",
        "status": "ok",
        "protocol_version": int(protocol_version),
        "policy_version": int(policy_version),
        "gpu_name": str(gpu_name),
        "queue_depth": int(queue_depth),
        "uptime_s": int(uptime_s),
        "avg_batch": (None if avg_batch is None else float(avg_batch)),
        "gpu_util": gpu_util,
        "gpu_mem_used_mb": gpu_mem_used_mb,
        "gpu_mem_total_mb": gpu_mem_total_mb,
        "gpu_temp_c": gpu_temp_c,
        "cpu_name": (None if cpu_name is None else str(cpu_name)),
        "cpu_pct_system": cpu_pct_system,
        "ram_pct_system": ram_pct_system,
        "ram_gb_system": ram_gb_system,
    }
```

- [ ] **Step 4: Кэшировать имя CPU в `__init__`**

В `tools/gmz_remote_inference_server.py` сразу после блока `self._gpu_name = (...)` (заканчивается на строке `else "cpu"\n        )`, добавить:

```python
        from core.telemetry.pc2_telemetry import detect_cpu_name

        self._cpu_name = detect_cpu_name()
```

- [ ] **Step 5: Сэмплить CPU/RAM в `_handle_health_check`**

В `_handle_health_check`, после блока GPU-сэмпла (`try/except` с `read_devices`), перед вызовом `resp = build_health_payload(`, добавить:

```python
        from core.telemetry.pc2_telemetry import sample_cpu_ram_system

        cpu = sample_cpu_ram_system()
```

и в самом вызове `build_health_payload(...)` после `gpu_temp_c=gpu_temp,` добавить:

```python
            cpu_name=self._cpu_name,
            cpu_pct_system=cpu["cpu_pct_system"],
            ram_pct_system=cpu["ram_pct_system"],
            ram_gb_system=cpu["ram_gb_system"],
```

- [ ] **Step 6: Запустить тесты — убедиться, что проходят**

Run: `python -m pytest tests/telemetry/test_remote_health_payload.py -v`
Expected: PASS (новые два теста + старые `test_build_health_payload_*`).

- [ ] **Step 7: Проверить синтаксис сервера**

Run: `python -m py_compile tools/gmz_remote_inference_server.py`
Expected: без вывода (успех).

- [ ] **Step 8: Коммит**

```bash
git add tools/gmz_remote_inference_server.py tests/telemetry/test_remote_health_payload.py
git commit -m "feat(gmz): CPU/RAM ПК2 в health_check inference-сервера"
```

---

## Task 3: SMZ-сервер — CPU/RAM в health_check

**Files:**
- Modify: `tools/smz_remote_inference_server.py` (`build_health_payload` ~357, `__init__` ~175, `_handle_health_check` ~233)
- Test: `tests/telemetry/test_remote_health_payload.py`

- [ ] **Step 1: Написать падающий тест**

В `tests/telemetry/test_remote_health_payload.py` добавить (новый импорт под алиасом, чтобы не путать с GMZ):

```python
def test_smz_build_health_payload_includes_cpu_ram():
    from tools.smz_remote_inference_server import build_health_payload as smz_payload

    payload = smz_payload(
        protocol_version=1, policy_version=7, gpu_name="RTX 2060 SUPER",
        queue_depth=0, uptime_s=5, avg_batch=None,
        gpu_util=10, gpu_mem_used_mb=512, gpu_mem_total_mb=8192, gpu_temp_c=44,
        cpu_name="Ryzen 5 1600", cpu_pct_system=38.0,
        ram_pct_system=31.0, ram_gb_system=5.0,
    )
    assert payload["cpu_pct_system"] == 38.0
    assert payload["cpu_name"] == "Ryzen 5 1600"
    assert payload["ram_pct_system"] == 31.0
    assert payload["ram_gb_system"] == 5.0
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/telemetry/test_remote_health_payload.py::test_smz_build_health_payload_includes_cpu_ram -v`
Expected: FAIL — `TypeError: build_health_payload() got an unexpected keyword argument 'cpu_name'`.

- [ ] **Step 3: Расширить SMZ `build_health_payload`**

В `tools/smz_remote_inference_server.py` заменить сигнатуру и тело `build_health_payload` точно так же, как в Task 2 Step 3 (та же сигнатура с `cpu_name/cpu_pct_system/ram_pct_system/ram_gb_system` и те же 4 ключа в возвращаемом dict).

- [ ] **Step 4: Кэшировать имя CPU в `__init__`**

В `tools/smz_remote_inference_server.py` сразу после блока `self._gpu_name = (...)` (строка `else "cpu"\n        )`), добавить:

```python
        from core.telemetry.pc2_telemetry import detect_cpu_name

        self._cpu_name = detect_cpu_name()
```

- [ ] **Step 5: Сэмплить CPU/RAM в `_handle_health_check`**

В `_handle_health_check`, после GPU-сэмпла (`try/except` с `read_devices`), перед `resp = build_health_payload(`, добавить:

```python
        from core.telemetry.pc2_telemetry import sample_cpu_ram_system

        cpu = sample_cpu_ram_system()
```

и в вызове `build_health_payload(...)` после `gpu_temp_c=gpu_temp,` добавить:

```python
            cpu_name=self._cpu_name,
            cpu_pct_system=cpu["cpu_pct_system"],
            ram_pct_system=cpu["ram_pct_system"],
            ram_gb_system=cpu["ram_gb_system"],
```

- [ ] **Step 6: Запустить тесты — убедиться, что проходят**

Run: `python -m pytest tests/telemetry/test_remote_health_payload.py -v`
Expected: PASS (включая новый SMZ-тест).

- [ ] **Step 7: Проверить синтаксис сервера**

Run: `python -m py_compile tools/smz_remote_inference_server.py`
Expected: без вывода (успех).

- [ ] **Step 8: Коммит**

```bash
git add tools/smz_remote_inference_server.py tests/telemetry/test_remote_health_payload.py
git commit -m "feat(smz): CPU/RAM ПК2 в health_check inference-сервера"
```

---

## Task 4: GUI — активировать пробу ПК2 для SMZ

**Files:**
- Modify: `app/gui_qt/main.py` (метод рядом с `_gmz_remote_cfg_for_telemetry` ~6665; `set_context` ~6660)
- Test: `tests/gui/test_smz_remote_cfg_telemetry.py` (create)

- [ ] **Step 1: Написать падающий тест**

Создать `tests/gui/test_smz_remote_cfg_telemetry.py`:

```python
import types

from app.gui_qt.main import GUIController


def _stub(algo, remote_is_smz):
    # Вызываем метод как несвязанную функцию с заглушкой — без QApplication.
    return types.SimpleNamespace(_training_algo=algo, _remote_is_smz=remote_is_smz)


def test_smz_cfg_returned_when_lan_active():
    stub = _stub("sampled_muzero", {
        "user_enabled_lan": True, "host": "192.168.0.101",
        "port": 5560, "auth_token": "",
    })
    cfg = GUIController._smz_remote_cfg_for_telemetry(stub)
    assert cfg == {
        "host": "192.168.0.101", "port": 5560,
        "auth_token": "", "transport": "gmz",
    }


def test_smz_cfg_none_when_lan_off():
    stub = _stub("sampled_muzero", {"user_enabled_lan": False, "host": "192.168.0.101", "port": 5560})
    assert GUIController._smz_remote_cfg_for_telemetry(stub) is None


def test_smz_cfg_none_for_other_algo():
    stub = _stub("gumbel_muzero", {"user_enabled_lan": True, "host": "192.168.0.101", "port": 5560})
    assert GUIController._smz_remote_cfg_for_telemetry(stub) is None
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/gui/test_smz_remote_cfg_telemetry.py -v`
Expected: FAIL — `AttributeError: type object 'GUIController' has no attribute '_smz_remote_cfg_for_telemetry'`.

- [ ] **Step 3: Реализовать метод**

В `app/gui_qt/main.py` сразу после метода `_gmz_remote_cfg_for_telemetry` (перед `_az_remote_cfg_for_telemetry`) добавить:

```python
    def _smz_remote_cfg_for_telemetry(self):
        # Remote IS (и карточка ПК2) для Sampled MuZero. SMZ ходит по GMZ-транспорту,
        # поэтому transport="gmz" (RemoteTelemetryProbe по умолчанию — gmz health_check).
        if str(self._training_algo) != "sampled_muzero":
            return None
        try:
            from app.gui_qt.remote_is_store import remote_is_lan_active
        except Exception:
            return None
        try:
            data = self._remote_is_smz
            if not remote_is_lan_active(data):
                return None
            return {
                "host": data.get("host", "127.0.0.1"),
                "port": int(data.get("port", 5560)),
                "auth_token": data.get("auth_token", ""),
                "transport": "gmz",
            }
        except Exception:
            return None
```

- [ ] **Step 4: Встроить в цепочку `remote_cfg`**

В `app/gui_qt/main.py`, в вызове `self._telemetry.set_context(` (строка ~6660), заменить строку:

```python
            remote_cfg=self._gmz_remote_cfg_for_telemetry() or self._az_remote_cfg_for_telemetry(),
```

на:

```python
            remote_cfg=(
                self._gmz_remote_cfg_for_telemetry()
                or self._smz_remote_cfg_for_telemetry()
                or self._az_remote_cfg_for_telemetry()
            ),
```

- [ ] **Step 5: Запустить тест — убедиться, что проходит**

Run: `python -m pytest tests/gui/test_smz_remote_cfg_telemetry.py -v`
Expected: PASS (все три теста).

- [ ] **Step 6: Проверить синтаксис GUI**

Run: `python -m py_compile app/gui_qt/main.py`
Expected: без вывода (успех).

- [ ] **Step 7: Коммит**

```bash
git add app/gui_qt/main.py tests/gui/test_smz_remote_cfg_telemetry.py
git commit -m "feat(gui): карточка нагрузки ПК2 для SMZ remote IS (гейт телеметрии)"
```

---

## Task 5: Регрессия и живая проверка

**Files:** —

- [ ] **Step 1: Прогнать весь телеметрический + затронутый набор**

Run: `python -m pytest tests/telemetry/ tests/gui/test_smz_remote_cfg_telemetry.py -v`
Expected: PASS (включая существующие `tests/telemetry/test_cards.py` — карточки ПК2·GPU/CPU).

- [ ] **Step 2: Живая проверка через Qt GUI (ручная, делает пользователь)**

На ПК2 перезапустить SMZ remote IS (`tools/pc2_remote_smz_is.bat`) — чтобы сервер с новым health_check поднялся.
На ПК1: запустить тренировку SMZ через Qt GUI с включённым LAN IS.
Ожидается: в панели телеметрии под карточками ПК1 появляются «ПК2 · <GPU>» (util %) и «ПК2 · <CPU>» (система %). При желании — нагрузить ПК2 и убедиться, что проценты растут.

- [ ] **Step 3 (если есть незакоммиченное от прошлых задач — не трогать).** Финальный статус:

Run: `git status --short`
Expected: чисто по затронутым файлам (служебные `runtime/state/*`, `hyperparams.json` — НЕ коммитить, это параллельная работа).

---

## Self-Review

- **Покрытие спеки:** Секция 1 (хелпер)→Task 1; Секция 2 (GMZ сервер)→Task 2; Секция 3 (SMZ сервер)→Task 3; Секция 4 (GUI-гейт)→Task 4; Секция 5 (QML без изменений)→подтверждено в File Structure (cards.py покрыт); Тестирование→Tasks 1–5. AZ — уже готов, изменений не требует (отмечено в шапке). ✓
- **Плейсхолдеры:** нет TBD/«добавить обработку ошибок» без кода — все шаги с конкретным кодом и командами. ✓
- **Согласованность типов:** `sample_cpu_ram_system()` возвращает ключи `cpu_pct_system/ram_pct_system/ram_gb_system` — те же читаются в `_handle_health_check` (Tasks 2/3) и кладутся в `build_health_payload`; `_smz_remote_cfg_for_telemetry` возвращает `{host,port,auth_token,transport}` — та же форма, что у `_gmz_remote_cfg_for_telemetry` и что ждёт `RemoteTelemetryProbe`. ✓
