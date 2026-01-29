param(
    [ValidateSet("Debug", "Release", "RelWithDebInfo", "MinSizeRel")]
    [string]$Configuration = "Release",
    [string]$Triplet = "x64-windows"
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

$pkgConfigPaths = @()
if ($env:VCPKG_ROOT) {
    $pkgConfigPaths += Join-Path $env:VCPKG_ROOT "installed\$Triplet\lib\pkgconfig"
    $pkgConfigPaths += Join-Path $env:VCPKG_ROOT "installed\$Triplet\share\pkgconfig"
    $env:PKG_CONFIG_PATH = ($pkgConfigPaths -join ";")
}

$cmakeArgs = @("-DCMAKE_BUILD_TYPE=$Configuration")
if ($toolchain) {
    $cmakeArgs += "-DCMAKE_TOOLCHAIN_FILE=$toolchain"
    $cmakeArgs += "-DVCPKG_TARGET_TRIPLET=$Triplet"
}

cmake .. @cmakeArgs
cmake --build . --config $Configuration

Write-Host "✅ GUI build finished: $buildDir"
