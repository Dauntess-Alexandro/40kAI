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
1. Установите [vcpkg](https://github.com/microsoft/vcpkg) отдельно от проекта (это **не** Python-venv). Проще всего — в `C:\tools\vcpkg` или любую папку без пробелов в пути.
   Затем задайте переменную окружения `VCPKG_ROOT` на путь к этой папке.
2. Установите пакеты GTKmm (пример для x64 Windows):

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
