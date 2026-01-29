param(
    [ValidateSet("Debug", "Release", "RelWithDebInfo", "MinSizeRel")]
    [string]$Configuration = "Release"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$guiDir = Join-Path $repoRoot "gui"
$buildDir = Join-Path $guiDir "build"

New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
Set-Location $buildDir

$toolchain = $null
if ($env:VCPKG_ROOT) {
    $toolchainCandidate = Join-Path $env:VCPKG_ROOT "scripts\buildsystems\vcpkg.cmake"
    if (Test-Path $toolchainCandidate) {
        $toolchain = $toolchainCandidate
    }
}

$cmakeArgs = @("-DCMAKE_BUILD_TYPE=$Configuration")
if ($toolchain) {
    $cmakeArgs += "-DCMAKE_TOOLCHAIN_FILE=$toolchain"
}

cmake .. @cmakeArgs
cmake --build . --config $Configuration

Write-Host "✅ GUI build finished: $buildDir"
