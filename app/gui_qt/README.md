# 40kAI — второй GUI (Qt/PySide6)

Минимальный Qt/QML GUI для запуска `train.py` и `eval.py` как отдельных процессов с потоковыми логами.

## Быстрый старт (Windows)

```powershell
python -m venv .venv
\.venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements_windows.txt
python gui_qt\main.py
```

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

## Упаковка (черновик)
- Linux: `pyinstaller --onefile --windowed gui_qt/main.py` + AppImage через `linuxdeploy`.
- Windows: PyInstaller (EXE) + проверка Qt DLL.
