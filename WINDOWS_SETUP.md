# Перенос GUI (GTKmm) на Windows

Этот документ описывает минимальный рабочий путь сборки GUI под Windows и запуск Python-части.

## 1) Зависимости

### Python
Установите Python 3.10+ и создайте виртуальное окружение в корне проекта:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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

3. **Задайте переменную окружения `VCPKG_ROOT`** на путь к папке vcpkg:
   ```powershell
   setx VCPKG_ROOT "C:\tools\vcpkg"
   ```
   Закройте и заново откройте PowerShell, чтобы переменная подтянулась.

4. **Установите GTKmm через vcpkg** (пример для x64 Windows):
   ```powershell
   vcpkg install gtkmm:x64-windows
   ```

## 2) Сборка GUI

Запуск из корня репозитория:

```powershell
.\build_gui.ps1 -Configuration Release
```

Если `VCPKG_ROOT` задан, скрипт автоматически подключит toolchain.

## 3) Запуск GUI

```powershell
.\run_gui_manual.ps1
```

Если бинарь не найден, скрипт выведет понятное сообщение о том, где он ожидался и что делать дальше.

## 4) Запуск консольной игры

```powershell
.\play.ps1
```

## 5) Сбор данных (scrapy)

```powershell
.\data_collector\unit_data\scrape.ps1
```
