$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (Test-Path ".venv\\Scripts\\Activate.ps1") {
    . ".venv\\Scripts\\Activate.ps1"
}

$env:PATH = "$PWD\\.venv\\Scripts;$env:PATH"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$PWD\\gym_mod;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = "$PWD\\gym_mod"
}

$env:MANUAL_DICE = "1"

& "$PWD\\gui\\build\\Application.exe"
