$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$venvActivate = Join-Path $repoRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $venvActivate)) {
    throw "Не найдено виртуальное окружение: $venvActivate. Сначала выполните 'python -m venv .venv' и установите зависимости."
}

& $venvActivate

Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

scrapy crawl data -o links.json
python -u addData.py
