#!/usr/bin/env pwsh
<# 
.SYNOPSIS
    Run Forest Analysis Pipeline
.DESCRIPTION
    Executes all forest data processing scripts in sequence
.EXAMPLE
    .\run_forest_pipeline.ps1
#>

Write-Host "============================================================" -ForegroundColor Green
Write-Host "Latvia Forest Completeness - Full Pipeline" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

$START = Get-Date

Write-Host "[1/4] Converting official forest statistics..." -ForegroundColor Cyan
python scripts/10_convert_forest_stats.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in step 1" -ForegroundColor Red
    exit 1 
}

Write-Host ""
Write-Host "[2/4] Extracting forests from OSM (10-15 min)..." -ForegroundColor Cyan
python scripts/11_extract_forests.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in step 2" -ForegroundColor Red
    exit 1 
}

Write-Host ""
Write-Host "[3/4] Calculating forest completeness..." -ForegroundColor Cyan
python scripts/12_calculate_forest_completeness.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in step 3" -ForegroundColor Red
    exit 1 
}

Write-Host ""
Write-Host "[4/4] Creating interactive map..." -ForegroundColor Cyan
python scripts/13_create_forest_map.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Error in step 4" -ForegroundColor Red
    exit 1 
}

$END = Get-Date
$DURATION = ($END - $START).TotalSeconds
$MIN = [math]::Floor($DURATION / 60)
$SEC = [math]::Floor($DURATION % 60)

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✓ Forest Pipeline Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Processing time: ${MIN}m ${SEC}s" -ForegroundColor Yellow
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Cyan
Write-Host "  • Forest data: outputs/exports/completeness_forests.csv" -ForegroundColor White
Write-Host "  • Interactive map: outputs/maps/forest_completeness_map.html" -ForegroundColor White
Write-Host ""
Write-Host "To view the map:" -ForegroundColor Cyan
Write-Host "  1. Start Flask: python app.py" -ForegroundColor White
Write-Host "  2. Visit: http://localhost:5000/forest-map" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Green
