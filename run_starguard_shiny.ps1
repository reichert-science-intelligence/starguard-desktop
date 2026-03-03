# StarGuard Shiny (Production Desktop) - Start Script
# Run from starguard-shiny/ directory.
# Open http://localhost:8002 after starting.

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Starting StarGuard Shiny on http://localhost:8002 ..."
shiny run app.py --port 8002
