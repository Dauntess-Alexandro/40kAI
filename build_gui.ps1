$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Set-Location "$PWD\\gui"
New-Item -ItemType Directory -Force -Path "build" | Out-Null
Set-Location "build"

cmake ..
cmake --build . --config Release

Write-Host ""
Write-Host "✅ GUI build finished: $PWD"
Read-Host "Press Enter to close..."
