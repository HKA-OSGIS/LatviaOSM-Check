# Forest Analysis - Quick Guide

## Overview
The forest analysis module compares OpenStreetMap forest/woodland data with official Latvian forest statistics for all 36 municipalities and major cities.

## Data Sources

### Official Statistics
- **Source**: Latvia Forest Inventory (2024)
- **File**: `data/raw/Forest.csv`
- **Coverage**: 36 municipalities + 10 cities
- **Metric**: Forest land area in hectares (ha)

### OSM Data
- **Tags**: `landuse=forest`, `natural=wood`
- **Source**: Same Latvia OSM extract used for roads
- **Extracted**: Forest polygons with area calculations

## Pipeline Scripts

### 1. Convert Official Statistics
```powershell
python scripts/10_convert_forest_stats.py
```
- Reads `Forest.csv` with official forest inventory data
- Filters to "Pavisam" (Total) category
- Converts hectares to km² for consistency
- Outputs: `data/raw/official_forest_stats.csv`

### 2. Extract Forests from OSM
```powershell
python scripts/11_extract_forests.py
```
- Extracts all forest areas from OSM PBF file
- Identifies forests using `landuse=forest` or `natural=wood`
- Calculates area for each forest polygon
- **Duration**: 10-15 minutes
- Outputs: `data/processed/forests.geojson`

### 3. Calculate Completeness
```powershell
python scripts/12_calculate_forest_completeness.py
```
- Performs spatial join of forests to municipalities
- Aggregates total forest area per municipality
- Compares OSM vs official statistics
- Calculates completeness percentage
- Outputs: `outputs/exports/completeness_forests.csv`

### 4. Create Interactive Map
```powershell
python scripts/13_create_forest_map.py
```
- Creates Folium map with color-coded completeness
- Green (≥90%), Yellow (50-70%), Red (<30%)
- Interactive popups with detailed statistics
- Outputs: `outputs/maps/forest_completeness_map.html`

## Run Complete Pipeline

### Windows PowerShell
```powershell
.\run_forest_pipeline.ps1
```

### Manual Execution
```powershell
python scripts/10_convert_forest_stats.py
python scripts/11_extract_forests.py
python scripts/12_calculate_forest_completeness.py
python scripts/13_create_forest_map.py
```

## View Results

### Start Flask Server
```powershell
python app.py
```

### Access Maps
- **Forest Map**: http://localhost:5000/forest-map
- **Roads Map**: http://localhost:5000/lau1-map

### API Endpoints
- **Forest Data**: `GET /api/forest-data` - JSON array of all municipalities
- **Roads Data**: `GET /api/csv-data` - JSON array of road completeness

## Output Files

### CSV Data
- `outputs/exports/completeness_forests.csv`
  - municipality_name
  - osm_forest_km2, osm_forest_ha
  - forest_area_km2, forest_area_ha (official)
  - completeness_pct
  - difference_ha, difference_km2
  - category (Low, Partial, Complete, Over-mapped)
  - num_forest_areas (count of forest polygons)

### Maps
- `outputs/maps/forest_completeness_map.html` - Standalone interactive map

### Processed Data
- `data/processed/forests.geojson` - All OSM forest geometries
- `data/raw/official_forest_stats.csv` - Cleaned official statistics

## Expected Results

### Coverage
- **36 municipalities**: All should have both OSM and official data
- **Cities**: Rīga, Daugavpils, Jelgava, Jūrmala, Liepāja, Rēzekne, Ventspils, Valmiera, Jēkabpils, Ogre

### Typical Completeness
- **High forest areas**: 30-70% (OSM typically has less forest data than official)
- **Urban areas**: May vary significantly
- **Rural municipalities**: Generally better coverage

## Troubleshooting

### Issue: No forests extracted
- **Check**: Ensure `data/raw/latvia-latest.osm.pbf` exists
- **Solution**: Re-download OSM data if needed

### Issue: Spatial join fails
- **Check**: Ensure `data/processed/municipalities.geojson` exists
- **Solution**: Run `python scripts/03_process_municipalities.py`

### Issue: Map not displaying
- **Check**: File size of HTML output
- **Solution**: Ensure completeness CSV has data

## Comparison with Roads

| Aspect | Roads | Forests |
|--------|-------|---------|
| OSM Tags | highway=* | landuse=forest, natural=wood |
| Metric | Length (km) | Area (km², ha) |
| Typical Completeness | 200%+ (over-mapped) | 30-70% (under-mapped) |
| Data Type | LineString | Polygon |
| Extract Time | 5-10 min | 10-15 min |

## Next Steps

After running the forest analysis:
1. Compare with road completeness patterns
2. Identify municipalities needing forest mapping
3. Use results for OSM improvement campaigns
4. Extend to other land use types (water, agricultural, urban)
