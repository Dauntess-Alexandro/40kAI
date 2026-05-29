# Live Telemetry Panel — Design

**Date:** 2026-05-29
**Status:** Approved (brainstorming) — pending implementation plan

## Goal

Добавить на вкладку «Главная» (Центр управления тренировкой) живую панель телеметрии: загрузка всех GPU (локальных + серверного ПК2, если активен), CPU и RAM **по процессу проекта**, плюс средний размер батча поиска. Цель — видеть реальную утилизацию железа во время тренировки и в один взгляд отвечать на вопрос «батчинг заработал? GPU загружен? нужна ли ещё карта?».

## Placement (decided: layout A)

Горизонтальная лента карточек во всю ширину **сразу под прогресс-баром**. Видна всегда; живые цифры во время тренировки, приглушённые «спеки» в простое.

Состав карточек слева направо:
1. **GPU0 (локальная, напр. 5060 Ti)** — util% карты целиком, VRAM процесса, температура.
2. **GPU ПК2 (напр. 2060 Super)** — только при активном LAN remote IS; появляется/исчезает динамически.
3. **CPU** — % по дереву процессов train.py.
4. **RAM** — % и ГБ по дереву процессов train.py.
5. **Батч поиска** — среднее значение `batch=` inference-сервера (`×N / batch_size`); **только для Gumbel MuZero** (для DQN/PPO скрыта).

## Key decision: что значит «загрузка GPU в проекте»

Windows/WDDM **не отдаёт надёжно per-process GPU compute%** (NVML per-process util на Windows обычно пуст/ноль). Поэтому:
- **GPU util% = загрузка карты целиком** (во время тренировки проект — практически единственный потребитель, так что это честно отражает работу).
- **GPU VRAM = по процессу** (NVML per-process memory по PID) — это доступно точно.
- CPU%/RAM — точно по дереву процессов через psutil.

## Data sources

| Метрика | Источник | Надёжность |
|---|---|---|
| CPU% / RAM проекта | `psutil`: train-процесс + дочерние, рекурсивно | точно |
| GPU0 util% / temp / clocks | `pynvml` (NVML), устройство целиком | точно |
| GPU0 VRAM проекта | NVML per-process memory по PID | точно |
| GPU ПК2 util/VRAM/temp/batch | расширенный `health_check` (ZMQ): ПК2 сам меряет через NVML | точно, пока ПК2 жив |
| Средний батч (локально) | парсинг строк `[GMZ][INF_SERVER] batch=N` из stdout | точно для GMZ |

Fallback: если pynvml не установлен/недоступен — парсинг `nvidia-smi --query-gpu=...`. Если и это недоступно — карточка GPU показывает «N/A», GUI не падает.

## Architecture (components)

Изолированные модули без Qt-зависимостей там, где можно (тестируемость):

1. **`app/gui_qt/telemetry/local_probe.py` — `LocalTelemetryProbe`**
   - Вход: PID train-процесса.
   - Выход: `{cpu_pct, ram_pct, ram_gb, gpus: [{idx, name, util, mem_used_mb, mem_total_mb, proc_mem_mb, temp_c}]}`.
   - Внутри: psutil (CPU/RAM по дереву) + pynvml (GPU device + per-process mem). NVML инициализируется один раз.
   - Без Qt.

2. **`app/gui_qt/telemetry/remote_probe.py` — `RemoteTelemetryProbe`**
   - Вход: host/port/auth_token.
   - Дёргает расширенный `health_check`, возвращает карточку ПК2 в том же формате, либо `None` если недоступен.
   - Переиспользует `remote_health_check` из `core/models/gmz_inference_transport.py`.

3. **`app/gui_qt/telemetry/batch_meter.py` — `BatchMeter`**
   - Скользящее среднее по строкам `batch=N` (последние ~30). Питается из существующего `_read_stdout`.
   - Без Qt.

4. **`app/gui_qt/telemetry/controller.py` — `TelemetryController(QObject)`**
   - Свой `QTimer` (~1с локально, ~2с для ПК2 — реже, по сети).
   - Локальный пробинг и удалённый — в `QThreadPool` (не блокировать UI-поток).
   - Сигнал `telemetryUpdated(dict)`.

5. **`app/gui_qt/telemetry/strip_widget.py` — `TelemetryStrip(QWidget)`**
   - Подписан на `telemetryUpdated`, перерисовывает карточки. Динамически добавляет/убирает карточку ПК2 и батч-карточку.

6. **Сторона ПК2:** `gmz_remote_inference_server.py::_handle_health_check` добавляет в payload поля GPU (NVML: util, mem_used/total, temp) и средний `batch`. Protocol payload расширяется обратносовместимо (новые ключи опциональны); версия протокола health_check инкрементируется.

### Data flow

```
train.py (subprocess) --stdout--> GUI._read_stdout --> BatchMeter (avg batch)
                                                          |
TelemetryController.QTimer(1s) --> QThreadPool:           |
   LocalTelemetryProbe(pid) --psutil+NVML--> local dict   |
   RemoteTelemetryProbe ----ZMQ health_check---> PC2 dict  |
        (PC2: NVML + server batch avg)                     |
                                                           v
              merge --> telemetryUpdated(dict) --> TelemetryStrip repaint
```

## Behavior

- **Тренировка идёт:** всё живое, обновление 1с (ПК2 ~2с).
- **Простой (IDLE):** карточки видны, но приглушены — имя GPU, общая VRAM/ядра/RAM как статические «спеки»; проектные % показаны прочерком `—` (без фейковых нулей).
- **Карточка ПК2:** показывается только когда `inference_server_mode=remote` и health_check отвечает. После N подряд неответов — состояние «нет связи» (красная рамка), затем скрытие.
- **Батч-карточка:** только при `train_algo == gumbel_muzero`.

## Visual spec

- Карточка: фон `#0d1521`, рамка `#243650` (ПК2 — `#3a6ea5`), радиус 6px.
- Внутри: инлайн-SVG иконка + короткий лейбл + число справа; крупное значение; тонкий прогресс-бар снизу.
- Цвета баров: GPU зелёный `#3fae6e`, CPU синий `#4a90d9`, RAM золотой `#d9a441`, темп оранжевый `#e06a4a`. При значении >90% бар краснеет (предупреждение).
- Иконки: аккуратные инлайн-SVG (видеокарта, чип CPU, планка RAM, сервер, молния-батч) — не эмодзи.
- Высота ленты ~64px, чтобы не давить блок «Контекст тренировки».
- Финальный стиль карточки дорабатывается визуально (browser) перед версткой.

## Dependencies

- `psutil`, `pynvml` (пакет `nvidia-ml-py`) — добавить в requirements/installer ПК1.
- На ПК2 — тоже `pynvml` (для health_check GPU-полей).
- Fallback на `nvidia-smi` парсинг, если pynvml недоступен.

## Error handling

- Любой сбой пробинга (NVML init fail, нет процесса, ZMQ timeout) → соответствующая карточка «N/A»/«нет связи», без исключений в UI-поток.
- NVML init один раз при старте контроллера, не на каждый тик.
- Удалённый пробинг полностью изолирован: недоступность ПК2 не влияет на локальные карточки.

## Testing

- Юнит `LocalTelemetryProbe`: мок psutil/pynvml → корректный dict, обработка отсутствия GPU.
- Юнит `BatchMeter`: поток строк лога → корректное скользящее среднее; строки без `batch=` игнорируются.
- Юнит `RemoteTelemetryProbe`: мок health_check payload (с GPU-полями и без — обратная совместимость) → карточка/None.
- Юнит расширенного `_handle_health_check` на ПК2: payload содержит GPU-поля при наличии NVML, и валиден без него.

## Out of scope (YAGNI)

- Исторические графики/тренды телеметрии (только мгновенные значения).
- Несколько удалённых ПК (только один ПК2, как сейчас).
- Per-process GPU compute% на Windows (технически ненадёжно — сознательно не делаем).
- Алерты/нотификации помимо красного бара при >90%.
