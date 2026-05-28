# Гайд: поставить Remote Inference Server на второй ПК (ПК2)

Пошаговая инструкция для схемы **два компьютера**: обучение на **ПК1**, GPU-инференс (MCTS) на **ПК2**.

Полная документация: [`remote-inference-server-gmz.md`](remote-inference-server-gmz.md).

---

## Что получится в итоге

| Машина | Что работает |
|--------|----------------|
| **ПК1** | Qt GUI, `train` (learner на GPU), **6 CPU env workers** |
| **ПК2** | Только `tools\pc2_remote_is.bat` → inference server на GPU |
| **Связь** | ZMQ порт **5555**, веса через **общую папку SMB** |

На ПК2 **не нужны** Qt, train, play, eval.

---

## Перед началом (чеклист)

- [ ] Оба ПК в **одной сети** (лучше кабель Gigabit, не Wi‑Fi).
- [ ] На **ПК2**: Windows, **NVIDIA** (например RTX 2060 Super), `nvidia-smi` работает.
- [ ] На **ПК2**: **Python 3.12+** с галочкой **Add to PATH**.
- [ ] На **ПК2** лежит **тот же репозиторий 40kAI**, что на ПК1 (`git pull` на обеих — одна версия).
- [ ] На **ПК1** уже хотя бы раз запускали GMZ / есть checkpoint или `latest_gmz_policy.pth`.

Запишите IP ПК2: на ПК2 в cmd → `ipconfig` → **IPv4** (например `192.168.1.50`).

---

## Часть A — ПК2 (сервер инференса)

### Шаг 1. Скопировать репозиторий

```bat
cd C:\
git clone https://github.com/Dauntess-Alexandro/40kAI.git
cd 40kAI
git pull
```

Или скопируйте папку `C:\40kAI` с ПК1 на ПК2 (USB/сеть).

### Шаг 2. Первый запуск bat (создаст конфиг)

Двойной клик:

```text
C:\40kAI\tools\pc2_remote_is.bat
```

Или из cmd:

```bat
cd C:\40kAI
tools\pc2_remote_is.bat
```

Откроется **блокнот** с `runtime\state\pc2_remote_is_config.bat` — заполните и **сохраните** (шаг 3), затем запустите bat **ещё раз**.

### Шаг 3. Заполнить конфиг ПК2

Файл: `C:\40kAI\runtime\state\pc2_remote_is_config.bat`

| Переменная | Что указать |
|------------|-------------|
| `GMZ_REMOTE_WEIGHTS_PATH` | Путь к **SMB-файлу** весов, например `Z:\latest_gmz_policy.pth` (шаг 4) |
| `GMZ_REMOTE_SEARCH_CONFIG` | `C:\40kAI\runtime\state\gmz_remote_search_cfg.json` (шаг 5) |
| `GMZ_REMOTE_INIT_WEIGHTS` | Локальный checkpoint с ПК1, если на `Z:` ещё нет файла, например `C:\40kAI\artifacts\models\gumbel_muzero\checkpoint_ep1.pth` |
| `GMZ_REMOTE_PORT` | `5555` (как в GUI на ПК1) |
| `GMZ_REMOTE_DEVICE` | `cuda:0` |
| `GMZ_REMOTE_SETUP_FIREWALL` | `1` (добавить правило firewall) |

Для **RTX 2060 Super (8 GB)** оставьте по умолчанию: `GMZ_REMOTE_BATCH_SIZE=10`, `GMZ_REMOTE_COMPILE=1`.

### Шаг 4. Общая папка (SMB) с весами

**На ПК1:**

1. Убедитесь, что есть файл (или появится после train):  
   `C:\40kAI\artifacts\models\actor_sync\latest_gmz_policy.pth`
2. ПКМ по папке `actor_sync` → **Предоставить доступ** → пользователь с ПК2 (чтение).

**На ПК2:**

1. Проводник → **Подключить сетевой диск** → `\\ИМЯ-ПК1\actor_sync` (или ваш share).
2. Буква диска, например **`Z:`**.
3. Проверка: в cmd `dir Z:\latest_gmz_policy.pth` — файл виден.

В конфиге: `set "GMZ_REMOTE_WEIGHTS_PATH=Z:\latest_gmz_policy.pth"`.

### Шаг 5. Файл `gmz_remote_search_cfg.json`

Создайте `C:\40kAI\runtime\state\gmz_remote_search_cfg.json`.

**Важно:** `obs_dim`, `action_sizes`, `num_simulations` и остальное должны **совпадать с ПК1** (тот же ростер, preset GMZ).

Скопируйте готовый файл с ПК1 на ПК2 или создайте по образцу ниже.

### Актуальные значения для этого репозитория (май 2026)

Сверено с:

- ростер: `runtime/state/data.json` + `runtime/state/units.txt` (4× Necron Warriors по 10, миссия `only_war`, поле 60×40);
- GMZ hyperparams: `hyperparams.json` → секция `gumbel_muzero`.

```json
{
  "obs_dim": 17,
  "action_sizes": [5, 2, 2, 2, 5, 2, 24, 24],
  "latent_dim": 256,
  "hidden_dim": 256,
  "num_layers": 2,
  "action_embed_dim": 64,
  "num_simulations": 48,
  "root_top_k": 12,
  "discount": 0.997,
  "temperature": 0.15,
  "gumbel_scale": 1.0,
  "prior_weight": 0.25,
  "batch_recurrent": 1,
  "tree_reuse": 1
}
```

| Поле | Значение | Откуда |
|------|----------|--------|
| `obs_dim` | 17 | размер state env (зависит от ростера/миссии) |
| `action_sizes` | 8 чисел | action space env (головы move/attack/shoot/…) |
| `num_simulations` | 48 | hyperparams GMZ |
| `root_top_k` | 12 | hyperparams GMZ |

Если на ПК1 **смените ростер**, миссию или preset GMZ — пересчитайте `obs_dim` / `action_sizes` (и при необходимости sims) и обновите JSON на **обоих** ПК. Подробнее: [`remote-inference-server-gmz.md` §6](remote-inference-server-gmz.md#6-файл-search_cfgjson).

### Шаг 6. Установка зависимостей и запуск сервера

Снова:

```bat
cd C:\40kAI
tools\pc2_remote_is.bat
```

Первый полный прогон:

- вызовет `installer\install_deps.bat -y` (**5–20 мин**);
- поставит PyTorch+CUDA, **pyzmq**, **msgpack**;
- откроет firewall на порт 5555;
- запустит сервер.

**Успех** — в консоли:

```text
[GMZ][REMOTE_IS] listening on 0.0.0.0:5555 device=cuda
```

Окно **не закрывайте** — пока оно открыто, ПК2 принимает запросы. Остановка: **Ctrl+C**.

Проверка только окружения (без сервера):

```bat
tools\pc2_remote_is.bat check
```

Логи: `runtime\logs\gmz_remote_is_<дата>.log`.

---

## Часть B — ПК1 (обучение)

### Шаг 7. Обновить код и venv

```bat
cd C:\40kAI
git pull
.\.venv\Scripts\activate
python -m pip install -U pyzmq msgpack
```

(Или полный `installer\install_deps.bat -y`.)

### Шаг 8. Настройки GUI

1. Запустите Qt GUI.
2. **Настройки** → **Gumbel MuZero** → панель **Inference Server**.
3. Выключите **Local Inference server**.
4. Включите **LAN Inference server**.
5. **Хост ПК2** = IP из `ipconfig` на ПК2 (например `192.168.1.50`), **не** `127.0.0.1` (если ПК2 — другая машина).
6. **Порт** = `5555`.
7. **Веса на ПК2** = тот же SMB-путь, что видите с ПК1 (для справки).
8. **Проверить соединение** → должно быть **OK • GPU: ...**.
9. **Сохраните** hyperparams.

### Шаг 9. Запуск train

1. На ПК2 сервер **уже запущен** (`pc2_remote_is.bat`).
2. **Главная** → алгоритм **Gumbel MuZero** → **Тренировка**.

Если LAN включили случайно на одном ПК — в логе train будет подробная подсказка, что выключить LAN и включить Local.

---

## Быстрая проверка с ПК1 (без GUI)

```bat
cd C:\40kAI
.\.venv\Scripts\activate
python -c "from core.models.gmz_inference_transport import remote_health_check; print(remote_health_check(host='192.168.1.50', port=5555))"
```

Подставьте IP ПК2.

---

## Каждый день (коротко)

| ПК2 | ПК1 |
|-----|-----|
| `tools\pc2_remote_is.bat` | GUI → LAN ON → HealthCheck OK → Train |

---

## Частые проблемы

| Симптом | Решение |
|---------|---------|
| `Connection refused` | На ПК2 запущен bat? Firewall? Верный IP? |
| `search_cfg не найден` | Создайте JSON, путь в конфиге |
| `Нет файла весов` | SMB: `dir Z:\latest_gmz_policy.pth` с ПК2 |
| HealthCheck OK, train падает | Одна версия кода на ПК1 и ПК2 (`git pull`) |
| Один ПК, случайно LAN | Выключите LAN, включите Local |

---

## RTX 2060 Super на ПК2

- **VRAM 8 GB** — для remote IS (только inference, без learner) **достаточно**.
- Узкое место чаще **скорость GPU + LAN**, не память.
- Начните с preset **Balanced** на ПК1; при стабильности — Heavy.

---

## Ссылки

| Файл | Назначение |
|------|------------|
| `tools/pc2_remote_is.bat` | Запуск сервера на ПК2 |
| `runtime/state/pc2_remote_is_config.example.bat` | Шаблон конфига |
| `docs/remote-inference-server-gmz.md` | Полное руководство |
| `runtime/logs/LOGS_FOR_AGENTS_REMOTE_IS.md` | Логи для отладки (ПК2) |
