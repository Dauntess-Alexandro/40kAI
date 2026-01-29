param(
    [string]$Arg1 = "",
    [string]$Arg2 = "",
    [string]$Arg3 = "",
    [string]$Arg4 = "",
    [string]$Arg5 = ""
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (Test-Path ".venv\\Scripts\\Activate.ps1") {
    . ".venv\\Scripts\\Activate.ps1"
}

python -u gym_mod/gym_mod/engine/initFile.py $Arg1 $Arg2 $Arg3 $Arg4 $Arg5
