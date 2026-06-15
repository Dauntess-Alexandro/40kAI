# Гайд: поставить Remote Inference Server (Sampled MuZero) на второй ПК (ПК2)

Пошаговая инструкция для схемы **два компьютера**: обучение на **ПК1**, GPU-инференс (sampled-search) на **ПК2**.

Полная документация: [`remote-inference-server-smz.md`](remote-inference-server-smz.md).

---

## Что получится в итоге

| Машина | Что работает |
|--------|----------------|
| **ПК1** | Qt GUI, `train` (learner на GPU), CPU env workers |
| **ПК2** | Только `tools\pc2_remote_smz_is.bat` → inference server на GPU |
| **Связь** | ZMQ порт **5560**, веса через **общую папку SMB** |

На ПК2 **не нужны** Qt, train, play, eval.

> **Порт 5560** — у Sampled MuZero remote IS. У gmz/az remote IS — **5555**. Не запускайте два remote-сервера на одном ПК2 на одном и том же порту; если нужны оба одновременно, порты по умолчанию уже разнесены (5555 и 5560).

---

## Перед началом (чеклист)

- [ ] Оба ПК в **одной сети** (лучше кабель Gigabit, не Wi‑Fi).
- [ ] На **ПК2**: Windows, **NVIDIA** (например RTX 2060 Super), `nvidia-smi` работает.
- [ ] На **ПК2**: **Python 3.12+** с галочкой **Add to PATH**.
- [ ] На **ПК2** лежит **тот же репозиторий 40kAI**, что на ПК1 (`git pull` на обеих — одна версия).
- [ ] На **ПК1** уже хотя бы раз запускали Sampled MuZero / есть checkpoint или `latest_smz_policy.pth`.

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

### Шаг 2. Подключить `Z:` (SMB) — см. Шаг 4 ниже

Сначала общая папка и диск **`Z:`**, потом bat на ПК2.

### Шаг 3. Запуск bat на ПК2 (конфиг создаётся сам)

```bat
cd C:\40kAI
tools\pc2_remote_smz_is.bat
```

При **первом** запуске скрипт копирует шаблон `runtime\state\pc2_remote_smz_is_config.example.bat` в `runtime\state\pc2_remote_smz_is_config.bat` с готовыми значениями:

- `SMZ_REMOTE_PORT=5560`, `SMZ_REMOTE_DEVICE=cuda:0`, firewall и batch — из шаблона
- `SMZ_REMOTE_WEIGHTS_PATH` / `SMZ_REMOTE_SEARCH_CONFIG` — заполните путями на `Z:\`

Откроется блокнот — заполните минимум:

```bat
set "SMZ_REMOTE_WEIGHTS_PATH=Z:\latest_smz_policy.pth"
set "SMZ_REMOTE_SEARCH_CONFIG=Z:\smz_remote_search_cfg.json"
```

**Сохраните** и закройте блокнот, затем запустите bat снова.

Редактировать конфиг вручную позже:

```bat
tools\pc2_remote_smz_is.bat config
```

| Переменная | Когда менять |
|------------|----------------|
| `SMZ_REMOTE_INIT_WEIGHTS` | Только если на `Z:\` ещё нет `latest_smz_policy.pth` — путь к `.pth` на ПК2 |
| `SMZ_REMOTE_AUTH_TOKEN` | Если включили токен в GUI на ПК1 |
| `SMZ_REMOTE_WEIGHTS_PATH` / `SMZ_REMOTE_SEARCH_CONFIG` | Если буква диска не `Z:` |

Для **RTX 2060 Super (8 GB)**: `SMZ_REMOTE_BATCH_SIZE=10–20`, `SMZ_REMOTE_BATCH_INTERVAL_MS=5–20`, при проблемах с `torch.compile` — `SMZ_REMOTE_COMPILE=0`.

### Шаг 4. Общая папка (SMB) с весами

**На ПК1** (компьютер, где идёт train и пишутся веса):

1. Папка должна существовать (файл `latest_smz_policy.pth` появится после первого sync при train; до train можно расшарить пустую папку):
   ```
   C:\40kAI\artifacts\models\actor_sync\
   ```

2. **Расшарить папку (Windows 10/11)** — на ПК1, в проводнике, по папке `actor_sync`:
   - ПКМ по `actor_sync` → **Предоставить доступ к** → **Определённые люди…**
   - Выберите **Все** (Everyone), уровень прав **Чтение** → **Общий доступ**.
   - Скопируйте сетевой путь, например `\\DESKTOP-XXX\actor_sync`.

3. Узнайте имя/IP ПК1: `hostname` или `ipconfig` (IPv4).

**На ПК2** — подключить общую папку ПК1 как диск **`Z:`**:

```bat
net use Z: \\ИМЯ_ИЛИ_IP_ПК1\actor_sync /user:ИМЯ_ПК1\Логин ПАРОЛЬ_ПК1 /persistent:yes
```

Или через проводник: **Подключить сетевой диск** → буква `Z:` → путь `\\ИМЯ_ИЛИ_IP_ПК1\actor_sync`.

Проверка на ПК2:

```bat
dir Z:\
dir Z:\latest_smz_policy.pth
```

Если файла весов пока нет (train не запускали) — укажите `SMZ_REMOTE_INIT_WEIGHTS` (checkpoint с ПК1) для первого старта.

Подробнее по шарингу и устранению проблем с SMB: см. аналогичный раздел в [`pc2-remote-is-setup-guide.md`](pc2-remote-is-setup-guide.md#шаг-4-общая-папка-smb-с-весами) (gmz) — процедура идентична, меняются только имена файлов (`latest_smz_policy.pth` вместо `latest_gmz_policy.pth`).

### Шаг 5. Файл `smz_remote_search_cfg.json`

**На ПК1** подготовьте JSON с полями `obs_dim`, `action_sizes`, `latent_dim`, `hidden_dim`, `num_layers`, `action_embed_dim`, `num_samples`, `discount`, `temperature`, `sample_temperature`, `prior_weight`, `dedup` — значения соответствуют ростеру в `runtime/state/data.json` и `hyperparams.json` → `sampled_muzero` (см. пример в [`remote-inference-server-smz.md` §6](remote-inference-server-smz.md#6-файл-search_cfgjson)).

Положите файл в `artifacts\models\actor_sync\smz_remote_search_cfg.json` (та же SMB-папка, что и веса).

**На ПК2** в `pc2_remote_smz_is_config.bat`:

```bat
set "SMZ_REMOTE_SEARCH_CONFIG=Z:\smz_remote_search_cfg.json"
```

Проверка с ПК2: `dir Z:\smz_remote_search_cfg.json`

**Важно:** после смены ростера, миссии или гиперпараметров Sampled MuZero на ПК1 — пересоздайте JSON и перезапустите remote IS на ПК2.

### Шаг 6. Установка зависимостей и запуск сервера

Снова:

```bat
cd C:\40kAI
tools\pc2_remote_smz_is.bat
```

Первый полный прогон:

- вызовет `installer\install_deps.bat -y` (**5–20 мин**);
- поставит PyTorch+CUDA, **pyzmq**, **msgpack**;
- откроет firewall на порт 5560;
- запустит сервер.

**Успех** — в консоли:

```text
[SMZ][REMOTE_IS] listening on 0.0.0.0:5560 device=cuda
```

Окно **не закрывайте** — пока оно открыто, ПК2 принимает запросы. Остановка: **Ctrl+C**.

Проверка только окружения (без сервера):

```bat
tools\pc2_remote_smz_is.bat check
```

Логи: `runtime\logs\smz_remote_is_<дата>.log`.

---

## Часть B — ПК1 (обучение)

### Шаг 7. Обновить код и venv

```bat
cd C:\40kAI
git pull
.\.venv\Scripts\activate
python -m pip install -U pyzmq msgpack
```

### Шаг 8. Настройки GUI

1. Запустите Qt GUI.
2. **Настройки** → **Sampled MuZero** → панель **Inference Server**.
3. Выключите **Local Inference server**.
4. Включите **LAN Inference server**.
5. **Хост ПК2** = IP из `ipconfig` на ПК2 (например `192.168.1.50`), **не** `127.0.0.1` (если ПК2 — другая машина).
6. **Порт** = `5560`.
7. **Проверить соединение** → должно быть **OK • GPU: ...**.
8. **Сохраните** hyperparams.

### Шаг 9. Запуск train

1. На ПК2 сервер **уже запущен** (`pc2_remote_smz_is.bat`).
2. **Главная** → алгоритм **Sampled MuZero** → **Тренировка**.

---

## Быстрая проверка с ПК1 (без GUI)

```bat
cd C:\40kAI
.\.venv\Scripts\activate
python -c "from core.models.sampled_muzero_inference_transport import remote_health_check; print(remote_health_check(host='192.168.1.50', port=5560))"
```

Подставьте IP ПК2.

---

## Каждый день (коротко)

| ПК2 | ПК1 |
|-----|-----|
| `tools\pc2_remote_smz_is.bat` | GUI → LAN ON → HealthCheck OK → Train |

---

## Частые проблемы

| Симптом | Решение |
|---------|---------|
| Кракозябры в `install_deps.bat` (`╨Ъ╨╛╤А...`) | Нормально для старого **cmd.exe**: запустите `chcp 65001`, используйте **Windows Terminal**, или `installer\install_deps.bat -y` (меню на английском) |
| `Connection refused` | На ПК2 запущен bat? Firewall на порт 5560? Верный IP? |
| `search_cfg не найден` | Создайте JSON, путь в `SMZ_REMOTE_SEARCH_CONFIG` |
| `Нет файла весов` | SMB: `dir Z:\latest_smz_policy.pth` с ПК2 |
| `triton` not installed | Не ошибка: на Windows поставьте `SMZ_REMOTE_COMPILE=0` в конфиге |
| HealthCheck OK, train падает | Одна версия кода на ПК1 и ПК2 (`git pull`) |
| Один ПК, случайно LAN | Выключите LAN, включите Local |

---

## Ссылки

| Файл | Назначение |
|------|------------|
| `tools/pc2_remote_smz_is.bat` | Запуск сервера на ПК2 |
| `runtime/state/pc2_remote_smz_is_config.example.bat` | Шаблон конфига |
| `docs/remote-inference-server-smz.md` | Полное руководство |
| `runtime/logs/LOGS_FOR_AGENTS_REMOTE_IS.md` | Логи для отладки (ПК2) |
