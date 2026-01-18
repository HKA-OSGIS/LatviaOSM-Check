#!/bin/bash
# LatviaOSM-Check - Full Pipeline Runner
# Runs all processing scripts in sequence

set -e
cd "$(dirname "$0")/.."

echo "============================================================"
echo "LatviaOSM-Check - Full Data Processing Pipeline"
echo "============================================================"
echo ""

START=$(date +%s)

echo "[1/6] Extracting roads from OSM data (5-10 min)..."
python3 scripts/02_extract_roads.py

echo ""
echo "[2/6] Processing municipality boundaries..."
python3 scripts/03_process_municipalities.py

echo ""
echo "[3/6] Performing spatial join (2-5 min)..."
python3 scripts/04_spatial_join.py

echo ""
echo "[4/6] Calculating completeness metrics..."
python3 scripts/05_calculate_completeness.py

echo ""
echo "[5/6] Creating interactive map..."
python3 scripts/07_create_interactive_map.py

echo ""
echo "[6/6] Creating LAU1 level map..."
python3 scripts/08_create_lau1_map.py

END=$(date +%s)
DURATION=$((END - START))
MIN=$((DURATION / 60))
SEC=$((DURATION % 60))

echo ""
echo "============================================================"
echo "✓ Pipeline Complete!"
echo "============================================================"
echo "Processing time: ${MIN}m ${SEC}s"
echo ""
echo "Generated files:"
echo "  • Interactive map: outputs/maps/interactive_map.html"
echo "  • Completeness data: outputs/exports/completeness_municipalities.csv"
echo "  • GeoJSON: outputs/exports/latvia_municipalities_36_only.geojson"
echo ""
echo "To start the web app:"
echo "  python app.py"
echo "  Then open: http://localhost:5000"
echo ""
