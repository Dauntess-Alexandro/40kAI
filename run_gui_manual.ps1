$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvActivate = Join-Path $repoRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $venvActivate)) {
    throw "Не найдено виртуальное окружение: $venvActivate. Сначала выполните 'python -m venv .venv' и установите зависимости."
}

& $venvActivate

$env:PATH = "$repoRoot\.venv\Scripts;$env:PATH"
$env:PYTHONPATH = "$repoRoot\gym_mod;$env:PYTHONPATH"
$env:MANUAL_DICE = "1"

$guiBinary = Join-Path $repoRoot "gui\build\Application.exe"
if (-not (Test-Path $guiBinary)) {
    throw "Не найден GUI-бинарь: $guiBinary. Сначала выполните '.\build_gui.ps1'."
}

& $guiBinary
