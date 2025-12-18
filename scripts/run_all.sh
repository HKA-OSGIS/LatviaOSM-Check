#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "=========================================="
echo "Complete OSM Analysis (No Database)"
echo "=========================================="
echo ""

START=$(date +%s)

echo "[1/9] Downloading data..."
bash scripts/01_download_data.sh

echo ""
echo "[2/9] Extracting roads (5-10 min)..."
python3 scripts/02_extract_roads.py

echo ""
echo "[3/9] Processing municipalities..."
python3 scripts/03_process_municipalities.py

echo ""
echo "[4/9] Spatial join (2-5 min)..."
python3 scripts/04_spatial_join.py

echo ""
echo "[5/9] Calculating completeness..."
python3 scripts/05_calculate_completeness.py

echo ""
echo "[6/9] Creating static map..."
python3 scripts/06_create_static_map.py

echo ""
echo "[7/9] Creating interactive map..."
python3 scripts/07_create_interactive_map.py

echo ""
echo "[8/9] Creating charts..."
python3 scripts/08_create_charts.py

echo ""
echo "[9/9] Generating report..."
python3 scripts/09_generate_report.py

END=$(date +%s)
DURATION=$((END - START))
MIN=$((DURATION / 60))
SEC=$((DURATION % 60))

echo ""
echo "=========================================="
echo "✓ COMPLETE!"
echo "=========================================="
echo "Time: ${MIN}m ${SEC}s"
echo ""
echo "Outputs:"
echo "  Map: firefox outputs/maps/interactive_map.html"
echo "  PNG: eog outputs/figures/completeness_map.png"
echo "  Data: outputs/exports/completeness.csv"
echo "  Report: outputs/reports/report.md"
echo ""