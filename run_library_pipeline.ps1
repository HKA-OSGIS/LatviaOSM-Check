#!/usr/bin/env pwsh
# Library Analysis Pipeline for Latvia OSM Project

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "📚 LATVIA LIBRARY COMPLETENESS ANALYSIS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$ErrorActionPreference = "Stop"

# Step 1: Convert official library statistics
Write-Host "📊 Step 1/5: Converting official library statistics..." -ForegroundColor Yellow
python scripts/10_convert_library_stats.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Failed at Step 1" -ForegroundColor Red
    exit 1 
}

# Step 2: Extract libraries from OSM
Write-Host "`n📍 Step 2/5: Extracting libraries from OSM (this may take 2-3 minutes)..." -ForegroundColor Yellow
python scripts/21_extract_libraries.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Failed at Step 2" -ForegroundColor Red
    exit 1 
}

# Step 3: Spatial join with municipalities
Write-Host "`n🗺️  Step 3/5: Performing spatial join with municipalities..." -ForegroundColor Yellow
python scripts/22_library_spatial_join.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Failed at Step 3" -ForegroundColor Red
    exit 1 
}

# Step 4: Calculate completeness
Write-Host "`n📈 Step 4/5: Calculating library completeness..." -ForegroundColor Yellow
python scripts/23_calculate_library_completeness.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Failed at Step 4" -ForegroundColor Red
    exit 1 
}

# Step 5: Create interactive map
Write-Host "`n🗺️  Step 5/5: Creating interactive library map..." -ForegroundColor Yellow
python scripts/27_create_library_map.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Failed at Step 5" -ForegroundColor Red
    exit 1 
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "✅ LIBRARY PIPELINE COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`n📂 Output Files:" -ForegroundColor Cyan
Write-Host "   • data/raw/official_library_stats.csv" -ForegroundColor White
Write-Host "   • data/processed/libraries.geojson" -ForegroundColor White
Write-Host "   • data/processed/libraries_by_novads.geojson" -ForegroundColor White
Write-Host "   • outputs/exports/completeness_libraries.csv" -ForegroundColor White
Write-Host "   • outputs/maps/library_completeness_map.html" -ForegroundColor White

Write-Host "`n🌐 To view the map:" -ForegroundColor Cyan
Write-Host "   Open: outputs/maps/library_completeness_map.html" -ForegroundColor Yellow
Write-Host "   Or run: python app.py (then visit http://localhost:5000/library-map)" -ForegroundColor Yellow

Write-Host "`n"
