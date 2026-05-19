# 40kAI (Qt/PySide6)

Минимальный Qt/QML GUI для запуска `train.py` и `eval.py` как отдельных процессов с потоковыми логами.

## Быстрый старт (Windows)

```powershell
# из корня репозитория:
.\installer\install_deps.bat          # авто GPU/CUDA + меню; Enter = авто
.\installer\install_deps.bat -y       # авто без меню
\.venv\Scripts\activate
python app\gui_qt\main.py
```

`installer\install_deps.bat` сам выбирает PyTorch: CUDA при NVIDIA GPU, иначе CPU. Меню: `1` авто, `2` CPU, `3–6` cu128/cu126/cu124/cu121.

## Как это работает
- GUI запускает `train.py`/`eval.py` через `QProcess`.
- stdout/stderr попадают в лог-панель.
- Статусная строка показывает состояние процесса.

## Примечания
- Если процесс не стартует, проверьте зависимости Python и наличие всех пакетов из `requirements_windows.txt`.
- Для вывода логов в консоль используются переменные окружения:
  - `TRAIN_LOG_ENABLED=1`
  - `TRAIN_LOG_TO_CONSOLE=1`
  - `TRAIN_LOG_TO_FILE=1`

## Установщик Windows (Install.exe)

Сборка (нужны Python 3.12+, Inno Setup 6):

```bat
scripts\build_installer.bat
```

Результат: `installer\output\Install.exe`

- Копирует приложение + `40kAI_GUI.exe`
- Онлайн-установка зависимостей в `.venv` (`scripts/updater/install_or_update.py`)
- Галочка **ярлык на рабочем столе**
- Train/eval запускаются через `.venv\Scripts\python.exe` (не из GUI bundle)

Только GUI exe: `scripts\build_gui_exe.bat` → `dist\40kAI_GUI\40kAI_GUI.exe`

Подробнее: [installer/README.md](../../installer/README.md)
