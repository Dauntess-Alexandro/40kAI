# Перенос GUI (GTKmm) на Windows

Этот документ описывает минимальный рабочий путь сборки GUI под Windows и запуск Python-части.

## 1) Зависимости

### Python
Ниже — подробный сценарий установки Python и зависимостей проекта.

1. **Скачайте Python 3.10+**:
   - Откройте страницу: https://www.python.org/downloads/windows/
   - Скачайте **Windows installer (64-bit)**.
   - В установщике обязательно включите галочку **Add Python to PATH**.

2. **Проверьте, что Python доступен в терминале**:
   ```powershell
   python --version
   ```

3. **Создайте виртуальное окружение в корне проекта**:
   ```powershell
   cd путь\к\репозиторию\40kAI
   python -m venv .venv
   ```

4. **Активируйте виртуальное окружение**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   Если PowerShell ругается на политику выполнения, выполните (один раз в текущем терминале):
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

5. **Установите зависимости Python**:
   ```powershell
   pip install -r requirements.txt
   ```

### GTKmm через vcpkg (рекомендуемый путь)
Ниже — максимально подробный путь установки.

1. **Скачайте и установите Visual Studio Build Tools** (обязательно нужен компилятор MSVC и Windows SDK):
   - Откройте страницу: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Скачайте установщик **Build Tools for Visual Studio**.
   - В установщике отметьте workload **Desktop development with C++**.
   - Убедитесь, что отмечены компоненты: **MSVC v143** (или новее) и **Windows 10/11 SDK**.

2. **Установите vcpkg отдельно от проекта** (это **не** Python-venv).
   - Откройте PowerShell и выполните:
     ```powershell
     cd C:\tools
     git clone https://github.com/microsoft/vcpkg.git
     cd vcpkg
     .\bootstrap-vcpkg.bat
     ```
   - После этого vcpkg готов к использованию.

3. **Задайте переменную окружения `VCPKG_ROOT`** на путь к папке vcpkg.
   Это нужно, чтобы скрипт сборки автоматически подхватил toolchain.
   ```powershell
   setx VCPKG_ROOT "C:\tools\vcpkg"
   ```
   После этого **закройте и заново откройте PowerShell**.
   Проверка, что переменная видна:
   ```powershell
   echo $env:VCPKG_ROOT
   ```
   Ожидаемый вывод: `C:\tools\vcpkg`.

4. **Установите GTKmm и nlohmann-json через vcpkg** (пример для x64 Windows):
   - Убедитесь, что PowerShell открыт **после** установки `VCPKG_ROOT`.
   - Перейдите в папку vcpkg (или используйте полный путь к vcpkg.exe):
     ```powershell
     cd C:\tools\vcpkg
     ```
   - Выполните установку:
     ```powershell
     .\vcpkg install gtkmm:x64-windows nlohmann-json:x64-windows
     ```
   - Для проверки списка установленных пакетов:
     ```powershell
     .\vcpkg list
     ```
   - Если пакеты установлены, но сборка всё равно не видит заголовки, убедитесь, что `VCPKG_ROOT` задан и вы запускаете `build_gui.ps1` в **новом** окне PowerShell.

## 2) Сборка GUI

Запуск из корня репозитория:

```powershell
cd путь\к\репозиторию\40kAI
.\build_gui.ps1 -Configuration Release
```

Что делает скрипт:
- создаёт папку `gui\build`, если её нет;
- вызывает CMake с `-DCMAKE_TOOLCHAIN_FILE` от vcpkg (если задан `VCPKG_ROOT`);
- запускает сборку в указанной конфигурации.

### Если сборка падает с ошибками `GTKMM_INCLUDE_DIRS-NOTFOUND` или `gtkmm.h: No such file`
1. Проверьте, что vcpkg действительно установил пакеты:
   ```powershell
   cd C:\tools\vcpkg
   .\vcpkg list | Select-String -Pattern "gtkmm|nlohmann"
   ```
2. Проверьте переменную окружения:
   ```powershell
   echo $env:VCPKG_ROOT
   ```
   Должно быть: `C:\tools\vcpkg`.
3. Закройте PowerShell и откройте заново (чтобы подтянулась `VCPKG_ROOT`), затем выполните сборку ещё раз.

## 3) Запуск GUI

```powershell
cd путь\к\репозиторию\40kAI
.\run_gui_manual.ps1
```

Если бинарь не найден, скрипт выведет понятное сообщение о том, где он ожидался и что делать дальше.

## 4) Запуск консольной игры

```powershell
cd путь\к\репозиторию\40kAI
.\play.ps1
```

## 5) Сбор данных (scrapy)

```powershell
cd путь\к\репозиторию\40kAI
.\data_collector\unit_data\scrape.ps1
```
