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

### Важно: текущий GUI написан под GTKmm 3
Код GUI использует API GTKmm 3 (GTK3). Если поставить GTKmm 4 (как в vcpkg), компиляция ломается
ошибками вида `ORIENTATION_HORIZONTAL не является членом Gtk`, `pack_start не найден`, `set_title не найден`.

**Рекомендуемый путь на Windows — MSYS2 + GTKmm 3.** Vcpkg сейчас ставит GTKmm 4, и это несовместимо.

### GTKmm 3 через MSYS2 (рекомендуемый путь)
Ниже — подробный сценарий установки.

1. **Установите MSYS2**:
   - Откройте страницу: https://www.msys2.org/
   - Скачайте установщик и установите MSYS2 (по умолчанию: `C:\msys64`).

2. **Обновите MSYS2 и установите пакеты GTKmm 3** (запускайте *MSYS2 MinGW x64*):
   ```bash
   pacman -Syu
   pacman -S --needed mingw-w64-x86_64-toolchain mingw-w64-x86_64-pkgconf mingw-w64-x86_64-gtkmm3 mingw-w64-x86_64-nlohmann-json mingw-w64-x86_64-cmake
   ```

3. **Сборка GUI из MSYS2 MinGW x64**:
   ```bash
   cd /c/путь/к/репозиторию/40kAI/gui
   mkdir -p build
   cd build
   cmake .. -G "MinGW Makefiles"
   cmake --build .
   ```

4. **Запуск GUI**:
   ```bash
   /c/путь/к/репозиторию/40kAI/gui/build/Application.exe
   ```

### GTKmm через vcpkg (НЕ рекомендуется для текущего кода)
vcpkg ставит GTKmm 4, а код проекта написан под GTKmm 3. Поэтому при использовании vcpkg возникнут ошибки
компиляции API‑несовместимости. Переход на GTKmm 4 возможен, но требует отдельного рефакторинга GUI.

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

4. **Установите GTKmm, nlohmann-json и pkgconf через vcpkg** (пример для x64 Windows):
   - Убедитесь, что PowerShell открыт **после** установки `VCPKG_ROOT`.
   - Перейдите в папку vcpkg (или используйте полный путь к vcpkg.exe):
     ```powershell
     cd C:\tools\vcpkg
     ```
   - Выполните установку:
     ```powershell
     .\vcpkg install gtkmm:x64-windows nlohmann-json:x64-windows pkgconf:x64-windows
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
.\build_gui.ps1 -Configuration Release -Triplet x64-windows
```

Что делает скрипт:
- создаёт папку `gui\build`, если её нет;
- вызывает CMake с `-DCMAKE_TOOLCHAIN_FILE` от vcpkg (если задан `VCPKG_ROOT`);
- запускает сборку в указанной конфигурации.

### Если сборка падает с ошибками `GTKMM_INCLUDE_DIRS-NOTFOUND`, `gtkmm.h: No such file` или `gtkmmConfig.cmake not found`
1. Проверьте, что vcpkg действительно установил пакеты:
   ```powershell
   cd C:\tools\vcpkg
   .\vcpkg list | Select-String -Pattern "gtkmm|nlohmann|pkgconf"
   ```
2. Проверьте переменную окружения:
   ```powershell
   echo $env:VCPKG_ROOT
   ```
   Должно быть: `C:\tools\vcpkg`.
3. Проверьте, что `PKG_CONFIG_PATH` указывает на vcpkg:
   ```powershell
   echo $env:PKG_CONFIG_PATH
   ```
   Ожидаемые пути (пример): `C:\tools\vcpkg\installed\x64-windows\lib\pkgconfig;C:\tools\vcpkg\installed\x64-windows\share\pkgconfig`.
4. Закройте PowerShell и откройте заново (чтобы подтянулась `VCPKG_ROOT`), затем выполните сборку ещё раз.

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
