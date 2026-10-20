# Start Antigravity PCB Annotator Local Server
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Starting Antigravity PCB Part Annotator & Calibrator... " -ForegroundColor Green
Write-Host "  URL: http://localhost:5180" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

Start-Process "http://localhost:5180"
python server.py
