# ПК2 нагрузка (GPU + CPU) в телеметрии GUI для SMZ/GMZ remote IS

**Дата:** 2026-06-16
**Статус:** дизайн утверждён, ждёт спека-ревью
**Контекст:** при тренировке SMZ с включённым LAN remote IS (инференс на ПК2) панель
телеметрии в Qt GUI показывает только карточки ПК1 (GPU/CPU/RAM). Нагрузка ПК2
(удалённый inference-сервер) не видна вообще. Пользователь просит видеть GPU **и** CPU ПК2.

## Проблема (root cause)

Конвейер телеметрии «проба → карточки» уже построен и работает:
- `app/gui_qt/telemetry/controller.py` → `_collect_cards()`: если задан `remote_cfg`,
  запускает `RemoteTelemetryProbe(...).sample()` (health_check к ПК2) и строит карточки.
- `app/gui_qt/telemetry/remote_probe.py` уже читает из health_check поля
  `gpu_util/gpu_mem_*/gpu_temp_c` и `cpu_name/cpu_pct_system/ram_pct_system/ram_gb_system`.
- `app/gui_qt/telemetry/cards.py` рисует «ПК2 · GPU» (по `util`, строки 73–75)
  и «ПК2 · CPU» (по `cpu_pct_system`, строки 90–93).

Два звена не достроены для SMZ/GMZ:

- **Gap A (GUI, почему ПК2 не видно для SMZ).** В `main.py` при старте тренировки
  `set_context(remote_cfg=_gmz_remote_cfg_for_telemetry() or _az_remote_cfg_for_telemetry())`
  (строка ~6660). Для `gumbel_muzero` есть `_gmz_remote_cfg_for_telemetry`, для
  `alphazero_tree` — `_az_remote_cfg_for_telemetry`, **но для `sampled_muzero` гейта нет**.
  → `remote_cfg = None` → проба ПК2 не запускается → карточек ПК2 нет.

- **Gap B (сервер, GPU есть — CPU нет).** GMZ и SMZ inference-серверы в health_check
  отдают только GPU-поля (`tools/gmz_remote_inference_server.py:_handle_health_check`,
  `tools/smz_remote_inference_server.py:_handle_health_check` + их локальные
  `build_health_payload`). Системных `cpu_*`/`ram_*` нет → даже при активной пробе
  карточка «ПК2 · CPU» не рисуется.

**AZ — эталон, уже готов.** `core/models/az_inference_protocol.build_health_response`
уже принимает `cpu_name/cpu_pct_system/ram_pct_system/ram_gb_system`, а
`tools/az_remote_inference_server._handle_health` уже сэмплит psutil и шлёт их.
GUI-гейт `_az_remote_cfg_for_telemetry` тоже есть. AZ-карточки ПК2·GPU и ПК2·CPU
уже работают — приводим GMZ/SMZ к этому виду.

## Объём (утверждено: SMZ + GMZ + AZ)

- **SMZ:** серверная часть (CPU/RAM в health_check) + GUI-гейт.
- **GMZ:** серверная часть (CPU/RAM в health_check). GUI-гейт уже есть.
- **AZ:** уже реализовано — изменений по сути нет (только сверка/при желании DRY-рефактор
  на общий хелпер, без поведенческих изменений).

## Решение

### 1. Общий хелпер системной CPU/RAM-телеметрии
В `core/telemetry/pc2_telemetry.py` добавить лёгкую функцию:

```python
def sample_cpu_ram_system() -> dict[str, float | None]:
    """Системные CPU%/RAM% (psutil), без имени CPU. None при отсутствии psutil."""
    # -> {"cpu_pct_system", "ram_pct_system", "ram_gb_system"}
```

Имя CPU (`detect_cpu_name()`, реестр Windows — дорого) кэшируется в сервере один раз
при инициализации, как уже сделано в AZ (`self._cpu_label`). Перцентажи сэмплятся
каждый health-тик через `sample_cpu_ram_system()`.

Существующий `sample_system_telemetry()` остаётся (его использует DQN-distributed путь
`tools/pc2_dqn_actors.py`); по возможности переиспользует новый хелпер внутри.

### 2. GMZ-сервер: CPU/RAM в health_check
- `tools/gmz_remote_inference_server.py`:
  - в `__init__`: `self._cpu_name = detect_cpu_name()`.
  - в `_handle_health_check`: после GPU-сэмпла — `cpu = sample_cpu_ram_system()`.
  - расширить локальный `build_health_payload(...)` параметрами
    `cpu_name/cpu_pct_system/ram_pct_system/ram_gb_system` (опциональные, default None)
    и положить их в dict ответа.

### 3. SMZ-сервер: CPU/RAM в health_check
- `tools/smz_remote_inference_server.py`: те же три правки, что и в GMZ
  (`__init__` кэш имени, сэмпл в `_handle_health_check`, поля в `build_health_payload`).

### 4. GUI: гейт пробы ПК2 для SMZ
- `app/gui_qt/main.py`: добавить `_smz_remote_cfg_for_telemetry()` (зеркало
  `_gmz_remote_cfg_for_telemetry`):
  - только если `self._training_algo == "sampled_muzero"`;
  - если `remote_is_lan_active(self._remote_is_smz)` → вернуть
    `{"host": ..., "port": 5560, "auth_token": ..., "transport": "gmz"}`
    (SMZ ходит по GMZ-транспорту; `RemoteTelemetryProbe` по умолчанию — gmz health_check);
  - иначе None. Источник данных — уже загруженный в памяти `self._remote_is_smz`
    (живое состояние GUI), без перечитывания с диска.
- Встроить в цепочку (строка ~6660):
  `remote_cfg = self._gmz_remote_cfg_for_telemetry() or self._smz_remote_cfg_for_telemetry() or self._az_remote_cfg_for_telemetry()`.

### 5. QML — без изменений
`cards.py`/`cards_model`/QML уже рисуют ПК2·GPU и ПК2·CPU при наличии полей.

## Обратная совместимость
Все cpu/ram-поля опциональны. Старый ПК2 (без полей) → проба получает None →
карточка ПК2·CPU не рисуется (как и сейчас). Старый ПК1 игнорирует лишние поля.
Протокол health_check не ломается.

## Поток данных
```
ПК2 inference server (_handle_health_check)
  ├─ GpuBackend.read_devices() → gpu_util/mem/temp
  └─ sample_cpu_ram_system() (psutil) + self._cpu_name
        → build_health_payload(... + cpu_*/ram_*) → ZMQ reply
ПК1 GUI TelemetryController._tick (1/сек, в пуле потоков)
  └─ RemoteTelemetryProbe.sample() → health_check → dict
        → build_cards() → «ПК2 · GPU» + «ПК2 · CPU» → QML
```
GUI активирует пробу, только когда `_smz/_gmz/_az_remote_cfg_for_telemetry()` вернул cfg
(т.е. алго совпал и LAN-IS реально включён).

## Тестирование
1. `sample_cpu_ram_system()` возвращает ключи `cpu_pct_system/ram_pct_system/ram_gb_system`
   (типы float|None), не падает без psutil.
2. GMZ и SMZ `build_health_payload` содержат cpu/ram-поля (расширить
   `tests/telemetry/test_remote_health_payload.py`).
3. `_smz_remote_cfg_for_telemetry`: при `sampled_muzero` + активном LAN → cfg с port=5560
   transport="gmz"; иначе None (другой algo / LAN выкл).
4. Интеграция: `RemoteTelemetryProbe.sample()` + `build_cards()` на синтетическом
   SMZ health-ответе с cpu/ram → присутствуют карточки `pc2` (GPU) и `pc2_cpu`
   (расширить `tests/telemetry/test_cards.py` / `test_remote_probe.py`).

## Затронутые файлы
- `core/telemetry/pc2_telemetry.py` — новый хелпер.
- `tools/gmz_remote_inference_server.py` — health_check CPU/RAM.
- `tools/smz_remote_inference_server.py` — health_check CPU/RAM.
- `app/gui_qt/main.py` — `_smz_remote_cfg_for_telemetry` + цепочка remote_cfg.
- `tests/telemetry/test_remote_health_payload.py`, `test_cards.py` (и/или
  `test_remote_probe.py`) — регрессии.

## Не делаем (YAGNI)
- Отдельный telemetry-эндпоинт/сообщение (health_check достаточно).
- Изменения QML-вёрстки.
- Рефактор работающего AZ-пути (опционально, без поведенческих изменений).
- Исторические графики нагрузки ПК2 (сейчас — мгновенные карточки, как у ПК1).
