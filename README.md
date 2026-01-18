# LatviaOSM-Check

A professional tool for analyzing OpenStreetMap (OSM) road completeness in Latvia by comparing OSM data with official municipal road statistics.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-Latest-orange.svg)](https://geopandas.org/)

## Overview

This project compares OpenStreetMap road data against official government statistics for 36 Latvian novads (municipalities), providing:

- **✅ Completeness Analysis**: Calculate what percentage of official roads are mapped in OSM
- **🗺️ Interactive Mapping**: Visualize completeness on a web-based map with color-coded regions
- **📊 Data Quality Reports**: Identify mapping gaps and priorities
- **🔌 RESTful API**: Access data programmatically via JSON endpoints
- **🎯 100% Data Matching**: Advanced fuzzy matching handles Latvian language variations

## Key Features

### 📍 **36 Latvian Novads (Municipalities)**
- Official road data from government statistics (TRS020)
- OSM road data from Latvia extract (456,381+ road segments)
- Completeness calculated for each municipality
- Advanced fuzzy name matching (80% threshold)

### 📈 **Data Quality**
- **Total OSM Roads**: 114,442 km
- **Total Official Roads**: 56,138 km  
- **Overall Completeness**: 203.9% (OSM has MORE data than official statistics)
- **Name Matching**: 100% (36/36 novads)
- **Zero Missing Values**: All municipalities have valid data

### 🎨 **Interactive Visualization**
- Color-coded municipalities: Green (≥90%), Yellow (70-90%), Orange (50-70%), Red (<50%)
- Detailed popups with statistics per municipality
- Flask-based responsive web interface
- GeoJSON data layers with Leaflet.js

## Quick Start

### Prerequisites
- Python 3.8 or higher
- 2 GB free disk space

### Installation

```powershell
# 1. Clone or download the repository
git clone <repository-url>
cd latvia_osm_project

# 2. Run setup (creates virtual environment and installs dependencies)
.\setup.ps1

# 3. Start the application
.\run.ps1

# 4. Open browser to http://localhost:5000
```

## Project Structure

```
latvia_osm_project/
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── setup.ps1                       # Environment setup script
├── run.ps1                         # Application launcher
├── CONTRIBUTING.md                 # Contribution guidelines
│
├── docs/                           # Documentation
│   ├── QUICK_GUIDE.md             # Quick start guide
│   └── IMPLEMENTATION_SUMMARY_NOVADS.md  # Technical implementation details
│
├── src/                            # Source code
│   ├── processing/                 # Data processing scripts
│   │   ├── create_fuzzy_mapping.py              # Fuzzy name matching (80% threshold)
│   │   ├── generate_corrected_completeness.py   # Completeness calculation
│   │   ├── generate_quality_report.py           # Data quality reports
│   │   └── get_stats.py                         # Statistics generation
│   └── utils/                      # Utility functions
│
├── scripts/                        # Full pipeline scripts
│   ├── 00_convert_official_stats.py  # Convert TRS020 format
│   ├── 02_extract_roads.py           # Extract roads from OSM
│   ├── 03_process_municipalities.py  # Process municipality boundaries
│   ├── 04_spatial_join.py            # Spatial join roads to municipalities
│   ├── 05_calculate_completeness.py  # Calculate completeness metrics
│   ├── 07_create_interactive_map.py  # Generate interactive map
│   └── 08_create_lau1_map.py         # Create LAU1 level map
│
├── templates/                      # Flask HTML templates
│   ├── dynamic_map.html           # Main interactive map
│   └── with_dropdown.html         # Map with dropdown selector
│
├── static/                         # Static assets (CSS, JS, images)
│
├── data/                           # Data files
│   ├── raw/                        # Original datasets
│   │   ├── latvia-latest.osm.pbf  # OSM data (700+ MB)
│   │   ├── municipalities.geojson  # Municipality boundaries
│   │   ├── TRS020_20251218-165232.csv  # Official road statistics
│   │   └── official_road_stats.csv     # Processed official stats
│   └── processed/                  # Processed datasets
│       ├── municipalities.geojson  # Processed boundaries
│       ├── roads.geojson          # All roads
│       └── roads_by_novads.geojson # Roads assigned to municipalities
│
└── outputs/                        # Generated outputs
    ├── exports/                    # Export files
    │   ├── completeness_municipalities.csv       # Final completeness data
    │   ├── completeness_novads_36_corrected.csv # Corrected version
    │   ├── latvia_municipalities_36_only.geojson # 36 novads boundaries
    │   └── novads_name_mapping_80percent.csv    # Name mapping reference
    └── maps/                       # Generated HTML maps
        └── interactive_map.html    # Standalone map
```

## Usage

### Running the Application

```powershell
# Quick start
.\run.ps1

# Or manually
python app.py
```

**Application will be available at:** http://localhost:5000

### Available Routes

- **`/`** - Homepage (redirects to dynamic map)
- **`/dynamic-map`** - Main interactive map with all 36 novads
- **`/map`** - Legacy standalone map
- **`/api/geojson-data?type=boundaries`** - Get municipality boundaries GeoJSON
- **`/api/geojson-data?type=roads`** - Get roads GeoJSON
- **`/api/csv-data`** - Get completeness statistics (JSON)
- **`/api/hierarchy`** - Get geographic hierarchy
- **`/api/municipality-data?name=<novads>`** - Get specific municipality data

### Processing Data

If you need to regenerate the completeness data:

```powershell
# Step 1: Create fuzzy name mapping (handles Latvian genitive case)
python src/processing/create_fuzzy_mapping.py

# Step 2: Generate corrected completeness metrics
python src/processing/generate_corrected_completeness.py

# Step 3: Generate quality report
python src/processing/generate_quality_report.py

# Step 4: Get statistics summary
python src/processing/get_stats.py
```

### Running Full Pipeline

To reprocess everything from scratch:

```bash
cd scripts
.\run_all.sh  # On Windows with Git Bash
# Or run scripts individually:
python 00_convert_official_stats.py
python 02_extract_roads.py
python 03_process_municipalities.py
python 04_spatial_join.py
python 05_calculate_completeness.py
python 07_create_interactive_map.py
python 08_create_lau1_map.py
```

## API Documentation

### GET /api/csv-data

Returns completeness statistics for all 36 municipalities.

**Response:**
```json
[
  {
    "Novads": "Aizkraukle",
    "OSM_Roads_km": 1234.56,
    "Official_Roads_km": 1500.00,
    "Completeness_%": 82.30,
    "Segments": 5432
  },
  ...
]
```

### GET /api/geojson-data?type=boundaries

Returns municipality boundaries as GeoJSON.

**Parameters:**
- `type` (required): `boundaries` or `roads`

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {...},
      "properties": {
        "shapeName": "Aizkraukle",
        "completeness": 82.30,
        ...
      }
    }
  ]
}
```

### GET /api/municipality-data?name={novads}

Returns specific municipality data including roads.

**Parameters:**
- `name` (required): Municipality name (e.g., "Aizkraukle")

**Response:** GeoJSON with roads for the specified municipality

## Data Sources

### Input Data Files

| File | Description | Size |
|------|-------------|------|
| `latvia-latest.osm.pbf` | OpenStreetMap data for Latvia | ~700 MB |
| `municipalities.geojson` | Official 36 novads boundaries | ~2 MB |
| `TRS020_20251218-165232.csv` | Official road statistics 2024 | ~10 KB |

### Generated Output Files

| File | Description |
|------|-------------|
| `completeness_municipalities.csv` | Final completeness data (36 rows) |
| `latvia_municipalities_36_only.geojson` | 36 novads with statistics |
| `novads_name_mapping_80percent.csv` | Name mapping reference |
| `roads_by_novads.geojson` | 456,381 road segments assigned to municipalities |

## Technical Details

### Data Processing Pipeline

1. **Fuzzy Name Matching** (80% threshold)
   - Handles Latvian language variations (nominative vs genitive case)
   - Example: "Aizkraukle" (GeoJSON) ↔ "Aizkraukles" (official stats)
   - Achieved 100% matching rate (36/36)

2. **Spatial Join**
   - Assigns 456,381 OSM road segments to municipalities
   - Uses `intersects` predicate
   - CRS: EPSG:3035 (European metric system)

3. **Completeness Calculation**
   - Formula: `(OSM_km / Official_km) * 100`
   - Handles edge cases (division by zero, missing data)

### Color Coding System

| Color | Range | Description |
|-------|-------|-------------|
| 🟢 Green | ≥90% | Excellent coverage |
| 🟡 Yellow | 70-90% | Good coverage |
| 🟠 Orange | 50-70% | Moderate coverage |
| 🔴 Red | <50% | Needs improvement |

## Troubleshooting

### Application won't start

```powershell
# Check Python version (requires 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check if port 5000 is in use
netstat -ano | findstr :5000
```

### Data files missing

```powershell
# Run setup again
.\setup.ps1

# Or regenerate from source data
python src/processing/create_fuzzy_mapping.py
python src/processing/generate_corrected_completeness.py
```

### Map not displaying

1. Clear browser cache (Ctrl+F5)
2. Check browser console for errors
3. Verify GeoJSON files exist in `outputs/exports/`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## Documentation

- **[Quick Guide](docs/QUICK_GUIDE.md)** - Fast introduction to the project
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY_NOVADS.md)** - Technical details and architecture

## License

This project is part of the LatviaOSM-Check initiative to improve OpenStreetMap coverage in Latvia.

## Acknowledgments

- **OpenStreetMap Contributors** - Road data
- **Latvian Central Statistical Bureau** - Official statistics (TRS020)
- **GeoPandas & Shapely** - Spatial processing
- **Flask & Leaflet.js** - Web interface

## Project Status

✅ **Production Ready**
- All 36 novads with valid data
- 100% name matching accuracy
- Zero NULL values
- 456,381 road segments processed
- Interactive web application deployed

---

**Last Updated**: January 18, 2026  
**Version**: 2.0  
**Python**: 3.8+
Returns specific municipality data.

## Test Results

✅ **27/29 Tests Passed**

Test Coverage:
- ✅ Data Files (2/2)
- ✅ CSV Data Integrity (11/11)
- ✅ GeoJSON Data Integrity (7/7)
- ✅ Data Calculations (3/3)
- ✅ Municipality Data (2/2)
- ✅ Data Quality (4/4)
- ⏭️ Flask API (2 tests skipped)

## Municipalities Included

**36 Official Novads (Regional Municipalities):**

Aizkraukle, Alūksne, Balvi, Bauska, Cēsis, Dobele, Daugavpils, Dundaga, Engure, Garkalne, Iecava, Gulbene, Jēkabpils, Jelgava, Krāslava, Kuldīga, Līvāni, Ludza, Madona, Ogre, Olaine, Preiļi, Rēzekne, Ropaži, Salaspils, Saldus, Saulkrasti, Sigulda, Smiltene, Stopini, Talsi, Tukums, Valka, Valmiera, Varakļāni, Ventspils

*Note: 7 city states excluded (Rīga, Daugavpils, Jelgava, Rēzekne, Ventspils, Liepāja, Jūrmala) as they have different administrative structures*

## Data Quality Notes

- **Over-mapped areas**: Some municipalities show >100% completeness (e.g., Salaspils 148.1%), indicating:
  - Dual carriageways counted differently
  - Different road classification schemes
  - Data quality variations

- **Under-mapped areas**: Low completeness indicates mapping priorities:
  - Ludza: 6.2% (lowest)
  - Several municipalities 6-12% completeness

## Technologies

- **Python 3**: Core language
- **GeoPandas**: Geospatial data handling
- **Flask**: Web framework
- **Folium**: Interactive mapping
- **Pandas**: Data analysis
- **GDAL/OGR**: GIS operations
- **SQLite/PostGIS**: Optional data storage

## Future Enhancements

- [ ] Railway network analysis
- [ ] Building completeness analysis
- [ ] POI (Hospital, Restaurant) analysis
- [ ] Historical trend analysis
- [ ] Advanced filtering and reports
- [ ] Multi-language support
- [ ] Database backend integration

## Contributors

- Developed for HKA-OSGIS (Hochschule Karlsruhe - University of Applied Sciences, OSGeo Initiative)

## License

[Specify License - e.g., MIT, GPL, etc.]

## Contact

For questions or contributions, please open an issue on GitHub or contact the maintainers.

## References

- OpenStreetMap: https://www.openstreetmap.org
- Latvian Central Statistical Bureau: https://www.csb.gov.lv
- GeoPandas Documentation: https://geopandas.org
- Flask Documentation: https://flask.palletsprojects.com
