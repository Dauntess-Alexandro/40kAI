# 40kAI

Симулятор и RL-песочница для настольной тактики в духе Warhammer 40k: обучение агентов (DQN, PPO, **AlphaZero Tree**, **AlphaZero Proxy**, Gumbel MuZero), оценка, просмотр партий в Viewer и управление всем через **Qt GUI (PySide6)**.

---

## О проекте (кратко)

- **Движок** — фазы хода, бой, миссии, ростер юнитов (`core/`).
- **Обучение** — `train.py` (self-play, чекпойнты в `artifacts/models/`).
- **Оценка** — `eval.py` или вкладка «Оценка» в GUI.
- **Игра / просмотр** — Viewer (`app/viewer/`), запуск из GUI.
- **Интерфейс** — `app/gui_qt/` (QML): старт train/eval, логи, настройки миссии и гиперпараметров.

Платформа: **Windows**, Python **3.12+**. Для GPU-обучения — видеокарта NVIDIA и драйвер с CUDA (PyTorch подбирается автоматически).

Подробнее для разработчиков: [docs/START_HERE.md](docs/START_HERE.md) · сборка установщика: [installer/README.md](installer/README.md)

---

## Установка (Windows)

### Способ 1 — Install.exe (рекомендуется)

Готовый установщик **не в Git** (файл >100 МБ, лимит GitHub). Варианты:

- **Releases** на GitHub — скачать `Install.exe` из последнего релиза (рекомендуется для друзей).
- **Собрать самому:** `scripts\build_installer.bat` → `installer\output\Install.exe`.
- Локально можно держать `Install.exe` в корне репо (в `.gitignore`).

**Другу / без Git:** достаточно **одного файла** `Install.exe` (Release, архив или флешка). Клонировать репозиторий не обязательно.

#### Что нужно на компьютере

| Требование | Зачем |
|------------|--------|
| Windows 10/11 (64-bit) | |
| **Python 3.12+** в PATH | После копирования файлов установщик качает библиотеки в `.venv` |
| **Интернет** | pip: torch, PySide6 и др. (CUDA-сборка torch — несколько ГБ) |
| ~0,5 ГБ под программу + **2–4+ ГБ** под `.venv` | Зависит от CPU/CUDA |

Установите Python с [python.org](https://www.python.org/downloads/) и отметьте **«Add python.exe to PATH»**.

#### Шаги

1. Запустите **`Install.exe`** (при необходимости — от имени администратора).
2. Выберите папку (по умолчанию `C:\Program Files\40kAI`).
3. По желанию включите **«Создать ярлык на рабочем столе»**.
4. Дождитесь окна **updater** (консоль): установка/обновление пакетов, строки `[SKIP]` / `[UPDATE]`.
5. В конце можно сразу запустить 40kAI.

**Запуск после установки:**

```text
C:\Program Files\40kAI\40kAI_GUI\40kAI_GUI.exe
```

или ярлык на рабочем столе.

**Лог установки зависимостей:**

```text
C:\Program Files\40kAI\runtime\logs\install.log
```

#### Что именно ставит Install.exe

- Копирует **рабочую копию приложения** (код `app/`, `core/`, `train.py`, GUI и т.д.) — **не** весь dev-репозиторий с `.git` / `tests`.
- **Не** включает готовый `.venv` — он создаётся при установке (скрипт-updater).
- Обученные модели в `artifacts/models/` появятся после вашего обучения.

Повторный запуск `Install.exe` или `install_deps.bat` в папке установки обновляет пакеты; уже актуальные помечаются **SKIP**.

---

### Способ 2 — из исходников (Git + bat)

Если клонировали репозиторий и хотите разрабатывать или не использовать `Install.exe`:

1. **Python 3.12+** в PATH.
2. Из корня репозитория:

```bat
installer\install_deps.bat
```

- Без аргументов — меню: авто GPU/CUDA или CPU (**Enter** = авто).
- Без меню: `installer\install_deps.bat -y`
- Принудительно: `installer\install_deps.bat cpu` или `installer\install_deps.bat cu128`

Создаётся `.venv` в корне репо, ставятся зависимости из `requirements_windows.txt`.

3. Запуск GUI:

```bat
.venv\Scripts\activate
python app\gui_qt\main.py
```

или

```bat
app\gui_qt\40k.bat
```

| Команда | Действие |
|---------|----------|
| `installer\install_deps.bat -y` | Только зависимости, авто CUDA/CPU |
| `train.bat` | Обучение из консоли |
| `scripts\viewer.bat` | Viewer |

---

## Обновление

Зависит от того, **как вы поставили 40kAI**.

### Поставили через Install.exe (`C:\Program Files\40kAI` и т.п.)

**Обновить только библиотеки (pip, torch)** — папку в мастере выбирать не нужно:

```bat
"C:\Program Files\40kAI\install_deps.bat" -y
```

Или: Пуск → 40kAI → **«Установить зависимости»**.

**Обновить саму программу** (новый GUI, код `app/`, `core/`):

1. Скачайте новый `Install.exe`.
2. Запустите его.
3. В шаге «Выбор папки» укажите **ту же папку**, куда ставили в прошлый раз (например `C:\Program Files\40kAI`) — установщик перезапишет файлы программы.
4. Снова дождитесь updater (зависимости: SKIP / UPDATE).

Модели в `artifacts\models\` и логи в `runtime\` при этом **обычно сохраняются** (если вы не удалили папку целиком).

### Работаете из папки с Git (`C:\40kAI` — клон репозитория)

1. Подтянуть код:
   ```bat
   git pull
   ```
2. Обновить зависимости:
   ```bat
   installer\install_deps.bat -y
   ```
3. GUI из исходников:
   ```bat
   python app\gui_qt\main.py
   ```

Папку «проекта» в Install.exe для этого сценария **не выбираете** — вы уже внутри репозитория.

### Что обновляет что

| Действие | Код программы | pip-пакеты (.venv) |
|----------|---------------|---------------------|
| `install_deps.bat -y` | нет | да |
| Новый `Install.exe` в **ту же** папку | да | да (updater в конце) |
| `git pull` | да (если в Git) | нет — нужен ещё `install_deps.bat -y` |

---

## Updater (зависимости)

Отдельного `Updater.exe` нет. Обновление пакетов — скрипт:

```text
scripts\updater\install_or_update.py
```

| Когда запускается | Как |
|-------------------|-----|
| При установке | `Install.exe` вызывает его сам |
| Вручную (репо) | `installer\install_deps.bat` |
| После установки в Program Files | `install_deps.bat -y` в каталоге 40kAI |

---

## Быстрый запуск (уже установлено)

| Сценарий | Команда |
|----------|---------|
| GUI | `40kAI_GUI\40kAI_GUI.exe` или `python app\gui_qt\main.py` |
| Обучение | Вкладка в GUI или `train.bat` |
| Оценка | Вкладка «Оценка» в GUI |
| Viewer | Кнопка в GUI или `scripts\viewer.bat` |

---

## Структура репозитория

```text
installer/output/Install.exe   # после сборки (в Git не коммитится)
installer/
  install_deps.bat       # ручная установка зависимостей из Git
  README.md              # как собрать Install.exe
app/gui_qt/              # Qt GUI
app/viewer/              # просмотр партии
core/                    # движок и RL
train.py, eval.py, play.py
requirements_windows.txt
docs/START_HERE.md
```

---

## Сборка Install.exe (для maintainer)

```bat
scripts\build_installer.bat
```

Нужны: Python 3.12+, [Inno Setup 6](https://jrsoftware.org/isdl.php).  
Результат обычно: `installer\output\Install.exe` (можно положить в корень как `Install.exe`).

---

## Лицензия

Уточните лицензию в репозитории при публикации на GitHub.
