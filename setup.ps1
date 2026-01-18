#!/usr/bin/env pwsh
<# 
.SYNOPSIS
    LatviaOSM-Check - Setup Script
.DESCRIPTION
    Sets up the development environment for the LatviaOSM-Check project
.EXAMPLE
    .\setup.ps1
#>

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "LatviaOSM-Check - Project Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "✓ Python version: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Step 1/3: Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv .venv
    Write-Host "  ✓ Created .venv" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment and install dependencies
Write-Host "Step 2/3: Installing dependencies..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    & ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
    & ".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ requirements.txt not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Verify data files
Write-Host "Step 3/3: Verifying data files..." -ForegroundColor Cyan
$dataFiles = @{
    "data\raw\municipalities.geojson" = "Municipality boundaries"
    "data\raw\TRS020_20251218-165232.csv" = "Official road statistics"
    "data\processed\roads_by_novads.geojson" = "Road segments by novads"
    "outputs\exports\completeness_municipalities.csv" = "Completeness data"
    "outputs\exports\latvia_municipalities_36_only.geojson" = "36 novads GeoJSON"
}

$allFound = $true
foreach ($file in $dataFiles.Keys) {
    if (Test-Path $file) {
        Write-Host "  ✓ $($dataFiles[$file])" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Missing: $($dataFiles[$file]) - $file" -ForegroundColor Red
        $allFound = $false
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

if ($allFound) {
    Write-Host "Setup Complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run the application: .\run.ps1" -ForegroundColor White
    Write-Host "  2. Open browser: http://localhost:5000" -ForegroundColor White
} else {
    Write-Host "Setup completed with warnings" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Some data files are missing. You may need to:" -ForegroundColor Yellow
    Write-Host "  1. Run processing scripts in src/processing/" -ForegroundColor White
    Write-Host "  2. Or run the full pipeline: .\scripts\run_all.sh" -ForegroundColor White
}

Write-Host "============================================================" -ForegroundColor Cyan
