param(
    [string]$Model = "None"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$env:MANUAL_DICE = "1"
$env:VERBOSE_LOGS = "1"

$runCommand = "& '$PSScriptRoot\\play_terminal_manual.ps1' '$Model'"

if (Get-Command wt -ErrorAction SilentlyContinue) {
    Start-Process wt -ArgumentList "powershell", "-NoExit", "-Command", $runCommand
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $runCommand
}
