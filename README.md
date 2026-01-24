# LatviaOSM-Check

A professional tool for analyzing OpenStreetMap (OSM) completeness in Latvia by comparing OSM data with official government statistics for roads, forests, and libraries.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-Latest-orange.svg)](https://geopandas.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Table of Contents

- [Overview](#overview)
- [Documentation](#documentation)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

LatviaOSM-Check is a comprehensive geospatial analysis tool that evaluates OpenStreetMap data quality across Latvia by comparing OSM features with official government statistics. The tool provides:

- **✅ Multi-Feature Analysis**: Roads, forests, and libraries completeness metrics
- **🗺️ Interactive Mapping**: Web-based visualization with color-coded completeness indicators
- **📊 Quality Reports**: Identify mapping gaps and prioritize areas for improvement
- **🔌 RESTful API**: Programmatic access to all data via JSON endpoints
- **🎯 Advanced Matching**: Fuzzy name matching handles Latvian language variations
- **🌳 Environmental Data**: Forest coverage analysis
- **📚 Infrastructure Tracking**: Library and public amenity mapping status

## Documentation

📖 **[Complete Documentation Index](docs/README.md)** - Start here to find the right documentation for your needs

### Quick Links

| For Users | For Developers | Project Info |
|-----------|----------------|--------------|
| [Installation Guide](docs/INSTALLATION.md) | [Development Guide](docs/DEVELOPMENT.md) | [Changelog](CHANGELOG.md) |
| [Usage Guide](docs/USAGE.md) | [Project Structure](docs/PROJECT_STRUCTURE.md) | [Contributors](CONTRIBUTORS.md) |
| [Quick Start](docs/QUICK_GUIDE.md) | [Contributing](CONTRIBUTING.md) | [License](LICENSE) |
| [API Reference](docs/API.md) | [Implementation Details](docs/IMPLEMENTATION_SUMMARY_NOVADS.md) | [Final Status](docs/FINAL_STATUS.md) |

## Key Features

### 📍 **Comprehensive Geographic Coverage**
- **43 Administrative Divisions**: All Latvian municipalities (novads) and cities
- **Multi-Feature Analysis**: Roads, forests, libraries
- Official data from government statistics (CSB, TRS020)
- OSM data from Latvia extract (456,381+ road segments)
- Advanced fuzzy name matching (80% threshold) for Latvian language

### 📈 **Data Quality Metrics**

#### Roads
- **Total OSM Roads**: 114,442 km
- **Total Official Roads**: 56,138 km  
- **Overall Completeness**: 203.9% (OSM exceeds official statistics)

#### Forests
- **OSM Forest Features**: Tracked across all municipalities
- **Comparison with Official Data**: Forest inventory statistics
- **Coverage Analysis**: Identify unmapped forest areas

#### Libraries
- **712 Total Libraries** (Official count)
- **Municipal and City Libraries**: Public library network tracking
- **Completeness by Region**: Identify library mapping gaps

### 🎨 **Interactive Visualization**
- **Hierarchical Selector**: Country → Region → Municipality → Feature Type
- **Multi-Layer Maps**: Roads, forests, libraries, and combined views
- **Color-Coded Completeness**: 
  - 🟢 Green (≥90%) - Excellent
  - 🟡 Yellow (70-90%) - Good
  - 🟠 Orange (50-70%) - Fair
  - 🔴 Red (<50%) - Needs improvement
- **Detailed Popups**: Click any area for detailed statistics
- **Flask-Based Interface**: Responsive, modern web design
- **GeoJSON Data Layers**: Leaflet.js powered mapping

### 🔧 **Developer-Friendly**
- **RESTful API**: JSON endpoints for all data
- **Multiple Export Formats**: GeoJSON, CSV, Shapefile
- **Python SDK**: Easy integration with GeoPandas workflows
- **Extensible Architecture**: Add new feature types easily

## Quick Start

### Installation

```powershell
# Windows PowerShell
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project
.\setup.ps1
.\run.ps1
```

```bash
# Linux/macOS
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

Then open your browser to: **http://localhost:5000**

### What You Get

- **Roads Analysis**: `/roads` - Road network completeness
- **Forests Analysis**: `/forests` - Forest mapping coverage  
- **Libraries Analysis**: `/libraries` - Public library locations
- **Combined View**: `/combined` - Multi-layer visualization
- **API Access**: `/api/*` - Programmatic data access

For detailed installation instructions, see **[Installation Guide](docs/INSTALLATION.md)**.

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
bash run_pipeline.sh  # On Linux/Mac or Git Bash on Windows
# Or run scripts individually:
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

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for:

- 🐛 Reporting bugs
- 💡 Suggesting features
- 🔧 Submitting code
- 📝 Improving documentation
- 🧪 Writing tests

See also:
- [Contributors](CONTRIBUTORS.md) - List of project contributors
- [Development Guide](docs/DEVELOPMENT.md) - Technical details for developers
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Data Licenses

- **OpenStreetMap Data**: © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright)
- **Official Statistics**: © Central Statistical Bureau of Latvia (CSB)
- **Municipality Boundaries**: Open government data

## Support

### Getting Help

- 📖 Check the [Documentation Index](docs/README.md)
- 🔍 Search [existing issues](https://github.com/<your-org>/latvia_osm_project/issues)
- 💬 Start a [discussion](https://github.com/<your-org>/latvia_osm_project/discussions)
- 📧 Contact maintainers (see [CONTRIBUTORS.md](CONTRIBUTORS.md))

### Reporting Issues

Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Screenshots if applicable

### Feature Requests

Have an idea? We'd love to hear it! Create an issue describing:
- The feature you'd like
- Why it would be useful
- Any implementation ideas

## Acknowledgments

- **OpenStreetMap Community** - For creating and maintaining the OSM dataset
- **Central Statistical Bureau of Latvia** - For official statistics
- **GeoPandas Team** - For excellent geospatial tools
- **Flask Team** - For the web framework
- All contributors who have helped improve this project

## Citation

If you use this tool in your research or project, please cite:

```bibtex
@software{latvia_osm_check,
  title = {LatviaOSM-Check: OpenStreetMap Completeness Analysis Tool},
  author = {LatviaOSM-Check Contributors},
  year = {2026},
  url = {https://github.com/<your-org>/latvia_osm_project},
  version = {2.1.0}
}
```

---

**Made with ❤️ for the OpenStreetMap and Open Source GIS communities**

## License

[Specify License - e.g., MIT, GPL, etc.]

## Contact

For questions or contributions, please open an issue on GitHub or contact the maintainers.

## References

- OpenStreetMap: https://www.openstreetmap.org
- Latvian Central Statistical Bureau: https://www.csb.gov.lv
- GeoPandas Documentation: https://geopandas.org
- Flask Documentation: https://flask.palletsprojects.com
