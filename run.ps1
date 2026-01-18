#!/usr/bin/env pwsh
<# 
.SYNOPSIS
    LatviaOSM-Check - Run Script
.DESCRIPTION
    Starts the Flask web application for OSM road completeness analysis
.EXAMPLE
    .\run.ps1
#>

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "LatviaOSM-Check - Starting Application" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path ".venv") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment not found. Run setup.ps1 first" -ForegroundColor Yellow
}

# Check if required files exist
$requiredFiles = @(
    "app.py",
    "requirements.txt",
    "outputs\exports\completeness_municipalities.csv",
    "outputs\exports\latvia_municipalities_36_only.geojson"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "✗ Missing: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Starting Flask application..." -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the Flask app
python app.py
