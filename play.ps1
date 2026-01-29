param(
    [string]$Model = "None",
    [string]$UseManualDice = "False"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvActivate = Join-Path $repoRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $venvActivate)) {
    throw "Не найдено виртуальное окружение: $venvActivate. Сначала выполните 'python -m venv .venv' и установите зависимости."
}

& $venvActivate

$env:PYTHONPATH = "$repoRoot\gym_mod;$env:PYTHONPATH"

python -u (Join-Path $repoRoot "play.py") $Model $UseManualDice
