# Library Completeness Analysis

This module analyzes the completeness of library mapping in OpenStreetMap (OSM) for Latvia by comparing OSM data with official library statistics from 2024.

## Overview

The library analysis pipeline follows the same pattern as the forest and road analyses:

1. **Convert official statistics** - Parse official library count data
2. **Extract OSM libraries** - Extract all `amenity=library` features from OSM
3. **Spatial join** - Match libraries to municipalities/cities
4. **Calculate completeness** - Compare OSM vs official counts
5. **Visualize results** - Create interactive map showing completeness

## Official Data Source

- **File**: `data/raw/Library.csv`
- **Source**: Latvian official statistics (2024)
- **Metric**: Number of public libraries (`Bibliotēku skaits`)
- **Coverage**: 7 cities + 36 municipalities (Madonas novads counted once)
- **Total**: 712 libraries nationwide (excluding Latvia total of 712)

### Official Library Counts by Type

**Cities (valstspilsētas)**:
- Rīga: 28 libraries
- Daugavpils: 8
- Jelgava: 4
- Jūrmala: 5
- Liepāja: 7
- Rēzekne: 4
- Ventspils: 5

**Municipalities (novads)**: Range from 2 (Ādažu novads) to 36 (Bauskas novads)

## OSM Data Extraction

### What is extracted:
- **Tag filter**: `amenity=library`
- **Geometry types**: Both nodes (points) and ways (buildings)
- **Attributes captured**:
  - OSM ID and type
  - Name (if available)
  - Operator
  - Access restrictions

### Expected OSM Coverage:
Libraries in OSM typically include:
- Public municipal libraries
- Academic/university libraries
- School libraries
- Private/special libraries

**Note**: Official statistics count only public libraries, so OSM counts may be higher if all library types are mapped.

## Pipeline Scripts

### 1. Convert Official Statistics
**Script**: `scripts/10_convert_library_stats.py`

Converts the raw CSV to clean format:
```csv
municipality_name,Area_Type,library_count
Rīga,City,28
Jelgava,City,4
Aizkraukles novads,Municipality,23
...
```

**Output**: `data/raw/official_library_stats.csv`

### 2. Extract Libraries from OSM
**Script**: `scripts/21_extract_libraries.py`

Extracts all libraries from the OSM PBF file:
- Searches for `amenity=library` tags
- Converts ways to points (using centroids)
- Creates GeoJSON with point geometries

**Expected time**: 2-3 minutes  
**Output**: `data/processed/libraries.geojson`

### 3. Spatial Join
**Script**: `scripts/22_library_spatial_join.py`

Joins libraries with administrative boundaries:
- Uses LAU1 municipalities from `outputs/exports/latvia_lau1.geojson`
- Assigns each library to its municipality
- Counts libraries per municipality

**Output**: 
- `data/processed/libraries_by_novads.geojson` - Libraries with municipality names
- `outputs/exports/library_stats_by_novads.csv` - Count statistics

### 4. Calculate Completeness
**Script**: `scripts/23_calculate_library_completeness.py`

Compares OSM vs. official counts:
- Merges OSM and official data
- Calculates completeness percentage: `(OSM_count / Official_count) × 100`
- Handles missing data (units with no OSM or official libraries)

**Output**: `outputs/exports/completeness_libraries.csv`

**Columns**:
- `municipality_name` - Name of municipality/city
- `Area_Type` - "City" or "Municipality"
- `osm_library_count` - Number of libraries in OSM
- `official_library_count` - Number in official statistics
- `completeness_%` - Percentage completeness

### 5. Create Interactive Map
**Script**: `scripts/27_create_library_map.py`

Creates a Folium-based interactive map:
- Color-coded by completeness percentage
- Clickable popups with detailed statistics
- Legend showing color scheme

**Output**: `outputs/maps/library_completeness_map.html`

**Color Scheme**:
- 🟢 Green (≥100%): Excellent coverage
- 🟠 Orange (75-99%): Good coverage
- 🟠 Dark Orange (50-74%): Fair coverage
- 🔴 Red (25-49%): Poor coverage
- 🔴 Dark Red (0-24%): Very poor coverage
- ⚫ Gray: No data

## Running the Pipeline

### Quick Start (All Steps)
```powershell
.\run_library_pipeline.ps1
```

### Individual Steps
```powershell
# Step 1: Convert official stats
python scripts/10_convert_library_stats.py

# Step 2: Extract from OSM (2-3 minutes)
python scripts/21_extract_libraries.py

# Step 3: Spatial join
python scripts/22_library_spatial_join.py

# Step 4: Calculate completeness
python scripts/23_calculate_library_completeness.py

# Step 5: Create map
python scripts/27_create_library_map.py
```

## Viewing Results

### Web Interface
```powershell
python app.py
```
Then open: `http://localhost:5000/library-map`

### Direct File Access
Open: `outputs/maps/library_completeness_map.html` in any browser

### Data Files
- **Completeness CSV**: `outputs/exports/completeness_libraries.csv`
- **Library locations**: `data/processed/libraries_by_novads.geojson`
- **Official stats**: `data/raw/official_library_stats.csv`

## Interpreting Results

### Completeness Percentage
- **< 50%**: Significant mapping needed
- **50-74%**: Moderate mapping needed  
- **75-99%**: Nearly complete
- **≥100%**: Complete or includes non-public libraries

### Over-mapping (>100%)
If OSM shows more libraries than official statistics, this could mean:
1. OSM includes academic, school, or private libraries
2. Official statistics only count public municipal libraries
3. Some libraries may be mapped multiple times (data quality issue)
4. New libraries opened after official statistics were compiled

## Integration with Other Analyses

The library analysis integrates with the existing project:
- Uses the same LAU1 municipality boundaries
- Follows the same completeness calculation methodology
- Can be combined with road and forest data for comprehensive OSM coverage assessment

## Future Enhancements

Potential improvements:
1. **Detailed classification**: Separate public vs academic libraries
2. **Combined map**: Show roads, forests, and libraries together
3. **API endpoints**: Add `/api/library-data` endpoint to app.py
4. **Temporal analysis**: Track library mapping progress over time
5. **Quality metrics**: Check for properly tagged names and operators
6. **Cross-validation**: Compare with other library databases

## Troubleshooting

**No libraries found in OSM**:
- Check if `data/raw/latvia-latest.osm.pbf` exists and is current
- Verify the file is not corrupted
- Confirm libraries are tagged as `amenity=library` in OSM

**Mismatched municipality names**:
- The script handles city name variations (e.g., "Jelgavas" → "Jelgava")
- Check `scripts/23_calculate_library_completeness.py` for name normalization

**Missing completeness data**:
- Ensure LAU1 boundaries exist: `outputs/exports/latvia_lau1.geojson`
- Verify official statistics have been converted
- Check that spatial join completed successfully

## Credits

- **Official Data**: Latvian Central Statistical Bureau
- **OSM Data**: OpenStreetMap contributors
- **Analysis Framework**: Follows the established pattern from road/forest analyses
