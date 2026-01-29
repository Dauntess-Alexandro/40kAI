param(
    [string]$Model = "None"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (Test-Path ".venv\\Scripts\\Activate.ps1") {
    . ".venv\\Scripts\\Activate.ps1"
}

if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$PWD\\gym_mod;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = "$PWD\\gym_mod"
}

$env:MANUAL_DICE = "1"

$logDir = Join-Path $PWD "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir ("run_{0}.log" -f (Get-Date -Format "yyyy-MM-dd_HH-mm-ss"))

if ($env:VERBOSE_LOGS -eq "1") {
    python -u play.py $Model False 2>&1 | Tee-Object -FilePath $logFile
} else {
    python -u play.py $Model False
}
