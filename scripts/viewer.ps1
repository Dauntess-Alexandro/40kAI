$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (Test-Path ".venv\\Scripts\\Activate.ps1") {
    . ".venv\\Scripts\\Activate.ps1"
}

if (-not $env:QT_QPA_PLATFORM -and -not $env:DISPLAY -and -not $env:WAYLAND_DISPLAY) {
    $env:QT_QPA_PLATFORM = "offscreen"
}

python -m viewer @args
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0 -and -not $env:QT_QPA_PLATFORM) {
    Write-Error "Viewer failed, retrying with QT_QPA_PLATFORM=offscreen..."
    $env:QT_QPA_PLATFORM = "offscreen"
    python -m viewer @args
    exit $LASTEXITCODE
}

exit $exitCode
