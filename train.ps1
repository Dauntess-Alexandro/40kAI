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

python -u train.py
