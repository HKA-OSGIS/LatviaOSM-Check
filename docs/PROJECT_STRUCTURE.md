# Project Structure

This document describes the organization of the LatviaOSM-Check project.

## Directory Structure

```
latvia_osm_project/
│
├── .git/                           # Git version control
├── .gitignore                      # Git ignore rules
├── .gitattributes                  # Git attributes configuration
├── .venv/                          # Python virtual environment (not in git)
├── .vscode/                        # VS Code settings
│   └── settings.json
│
├── app.py                          # Flask web application (main entry point)
├── pyproject.toml                  # Project metadata
├── requirements.txt                # Python dependencies
├── setup.ps1                       # Automated setup script (Windows)
├── run.ps1                         # Application launcher (Windows)
├── run_forest_pipeline.ps1         # Forest analysis pipeline
├── run_library_pipeline.ps1        # Library analysis pipeline
│
├── README.md                       # Main project documentation
├── LICENSE                         # MIT License
├── CHANGELOG.md                    # Version history and changes
├── CONTRIBUTING.md                 # Contribution guidelines
├── CONTRIBUTORS.md                 # List of contributors
│
├── docs/                           # 📚 Documentation
│   ├── API.md                      # REST API reference
│   ├── INSTALLATION.md             # Setup instructions
│   ├── USAGE.md                    # User guide
│   ├── DEVELOPMENT.md              # Developer guide
│   ├── QUICK_GUIDE.md              # Quick start guide
│   ├── IMPLEMENTATION_SUMMARY_NOVADS.md  # Technical implementation
│   ├── LIBRARY_ANALYSIS.md         # Library analysis documentation
│   └── FINAL_STATUS.md             # Project status report
│
├── src/                            # 🐍 Source code modules
│   ├── __init__.py
│   └── processing/                 # Data processing modules
│       ├── create_fuzzy_mapping.py              # Municipality name matching
│       ├── create_library_fuzzy_mapping.py      # Library-specific matching
│       ├── generate_corrected_completeness.py   # Roads completeness
│       ├── generate_library_corrected_completeness.py  # Library completeness
│       ├── generate_quality_report.py           # Data quality reports
│       └── get_stats.py                         # Statistics generation
│
├── scripts/                        # 🔧 Pipeline scripts (numbered workflow)
│   ├── 00_convert_official_stats.py     # Convert TRS020 format
│   ├── 02_extract_roads.py              # Extract OSM roads
│   ├── 03_process_municipalities.py     # Process boundaries
│   ├── 04_spatial_join.py               # Spatial join roads→municipalities
│   ├── 05_calculate_completeness.py     # Calculate road completeness
│   ├── 07_create_interactive_map.py     # Generate road map
│   ├── 08_create_lau1_map.py            # Create LAU1 level map
│   ├── 10_convert_forest_stats.py       # Convert forest statistics
│   ├── 10_convert_library_stats.py      # Convert library statistics
│   ├── 11_extract_forests.py            # Extract OSM forests
│   ├── 12_forest_spatial_join.py        # Spatial join forests
│   ├── 13_calculate_forest_completeness.py  # Calculate forest completeness
│   ├── 17_create_forest_map.py          # Generate forest map
│   ├── 18_create_combined_map.py        # Combined roads+forests map
│   ├── 21_extract_libraries.py          # Extract OSM libraries
│   ├── 22_library_spatial_join.py       # Spatial join libraries
│   ├── 23_calculate_library_completeness.py  # Calculate library completeness
│   ├── 27_create_library_map.py         # Generate library map
│   ├── 99_create_comprehensive_geojson.py  # Create comprehensive export
│   └── run_pipeline.sh                  # Unix pipeline runner
│
├── templates/                      # 🌐 Flask HTML templates
│   ├── dynamic_map.html            # Main interactive map
│   └── with_dropdown.html          # Map with dropdown selector
│
├── data/                           # 📊 Data files (mostly in .gitignore)
│   ├── raw/                        # Original source data
│   │   ├── latvia-latest.osm.pbf   # OSM data (~700 MB, not in git)
│   │   ├── municipalities.geojson  # Municipality boundaries
│   │   ├── Road.csv                # Official road statistics (2024)
│   │   ├── Forest.csv              # Official forest statistics (2024)
│   │   ├── Library.csv             # Official library statistics (2024)
│   │   ├── official_road_stats.csv
│   │   ├── official_forest_stats.csv
│   │   ├── official_library_stats.csv
│   │   ├── railway_data.csv
│   │   └── TRS020_20251218-165232.csv
│   │
│   └── processed/                  # Processed data files
│       ├── municipalities.geojson
│       ├── roads.geojson           # All roads (not in git - large)
│       ├── roads_by_municipality.geojson
│       ├── roads_by_novads.geojson
│       ├── forests.geojson
│       ├── forests_by_novads.geojson
│       ├── libraries.geojson
│       └── libraries_by_novads.geojson
│
└── outputs/                        # 📈 Generated outputs
    ├── exports/                    # Export files
    │   ├── latvia_lau1.geojson                    # LAU1 boundaries with data
    │   ├── latvia_lau1_forests.geojson            # Forests data
    │   ├── completeness_municipalities.csv        # Road completeness
    │   ├── completeness_forests.csv               # Forest completeness
    │   ├── completeness_libraries.csv             # Library completeness
    │   ├── forest_stats_by_novads.csv
    │   ├── library_stats_by_novads.csv
    │   ├── forest_completeness_report.txt
    │   └── forest_completeness_full_report.txt
    │
    └── maps/                       # Generated HTML maps
        ├── combined_map.html       # Roads + forests combined
        ├── library_completeness_map.html
        └── interactive_map.html    # Main map (roads)
```

## File Naming Conventions

### Scripts (numbered workflow)
- **00-09**: Data preparation and conversion
- **10-19**: Feature extraction and processing
  - 02: Roads extraction
  - 11: Forests extraction
  - 21: Libraries extraction
- **20-29**: Spatial analysis and completeness calculation
- **30-39**: Reserved for future features
- **90-99**: Utility and comprehensive exports

### Data Files
- **Raw data**: Original files from official sources
- **Processed data**: Cleaned and standardized files
- **Exports**: Final outputs for distribution

### Documentation
- **Uppercase .md files** (root): Project-level documentation
- **docs/*.md files**: Detailed guides and references

## Key Components

### 1. Web Application (`app.py`)
Main Flask application providing:
- Interactive web interface
- RESTful API endpoints
- Data caching and optimization
- Route handlers for all maps

### 2. Processing Modules (`src/processing/`)
Reusable Python modules for:
- Fuzzy name matching (Latvian language support)
- Completeness calculations
- Quality report generation
- Statistics aggregation

### 3. Pipeline Scripts (`scripts/`)
Standalone scripts that can be run individually or as a pipeline:
- Extract features from OSM
- Process municipality boundaries
- Perform spatial joins
- Calculate completeness metrics
- Generate visualizations

### 4. Templates (`templates/`)
HTML templates for Flask application:
- Leaflet.js based interactive maps
- Responsive design
- Hierarchical selectors

### 5. Documentation (`docs/`)
Comprehensive documentation:
- API reference
- Installation guides
- Usage tutorials
- Development guidelines

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. RAW DATA                                                 │
├─────────────────────────────────────────────────────────────┤
│ • latvia-latest.osm.pbf (OSM data)                          │
│ • municipalities.geojson (boundaries)                       │
│ • Road.csv, Forest.csv, Library.csv (official stats)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. EXTRACTION (scripts/0X_*, 1X_*, 2X_*)                   │
├─────────────────────────────────────────────────────────────┤
│ • Extract roads/forests/libraries from OSM PBF              │
│ • Convert official statistics to standard format            │
│ • Process municipality boundaries                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PROCESSING (scripts/XX_spatial_join, src/processing/)   │
├─────────────────────────────────────────────────────────────┤
│ • Spatial join features to municipalities                   │
│ • Fuzzy name matching (handle Latvian variations)           │
│ • Calculate completeness metrics                            │
│ • Generate quality reports                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. OUTPUTS (outputs/exports/, outputs/maps/)               │
├─────────────────────────────────────────────────────────────┤
│ • GeoJSON files with completeness data                      │
│ • CSV statistics files                                      │
│ • Interactive HTML maps                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. WEB APPLICATION (app.py)                                │
├─────────────────────────────────────────────────────────────┤
│ • Serve interactive maps                                    │
│ • Provide REST API                                          │
│ • Enable data downloads                                     │
└─────────────────────────────────────────────────────────────┘
```

## Git Workflow

### Tracked Files
- Source code (`.py`, `.html`)
- Documentation (`.md`)
- Configuration (`pyproject.toml`, `requirements.txt`, `.gitignore`)
- Small data files (`.csv` < 100MB)
- Municipality boundaries (`.geojson` if < 100MB)

### Ignored Files (`.gitignore`)
- Virtual environment (`venv/`, `.venv/`)
- Python cache (`__pycache__/`, `*.pyc`)
- Large OSM data (`*.pbf`)
- Large processed files (`data/processed/roads.geojson`)
- IDE settings (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Environment files (`.env`)

## Development Workflow

### 1. Initial Setup
```bash
git clone <repository>
cd latvia_osm_project
.\setup.ps1          # Creates venv and installs dependencies
```

### 2. Data Processing
```bash
.\run_forest_pipeline.ps1    # Process all features
.\run_library_pipeline.ps1
```

### 3. Development
```bash
# Activate environment
.\venv\Scripts\Activate.ps1

# Make changes to code
# Test changes

# Run application
python app.py
```

### 4. Testing
```bash
pytest tests/
```

### 5. Documentation
Update relevant `.md` files in `docs/`

### 6. Commit and Push
```bash
git add .
git commit -m "Description of changes"
git push
```

## Extending the Project

### Adding a New Feature Type (e.g., Railways)

1. **Create extraction script**: `scripts/31_extract_railways.py`
2. **Create spatial join**: `scripts/32_railway_spatial_join.py`
3. **Calculate completeness**: `scripts/33_calculate_railway_completeness.py`
4. **Generate map**: `scripts/37_create_railway_map.py`
5. **Add API endpoint**: Update `app.py`
6. **Update documentation**: Add to relevant `.md` files
7. **Create pipeline script**: `run_railway_pipeline.ps1`

### Adding a New Region/Country

1. Download OSM extract for region
2. Update municipality boundaries
3. Add official statistics
4. Modify fuzzy matching for local language
5. Update configuration in scripts
6. Run full pipeline

## Maintenance

### Regular Tasks
- Update OSM data: Download latest `latvia-latest.osm.pbf`
- Update official statistics: Replace `Road.csv`, `Forest.csv`, `Library.csv`
- Re-run pipelines: Process new data
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Review and merge pull requests
- Update changelog: Document changes in `CHANGELOG.md`

### Monthly
- Check for OSM data updates
- Review open issues
- Update documentation if needed

### Quarterly
- Major version updates
- Performance optimization
- Feature additions

## Best Practices

1. **Code Organization**: Keep related code together
2. **Documentation**: Update docs with code changes
3. **Testing**: Write tests for new features
4. **Version Control**: Commit frequently with clear messages
5. **Dependencies**: Keep `requirements.txt` updated
6. **Data Management**: Don't commit large files
7. **Configuration**: Use environment variables for secrets
8. **Error Handling**: Add try-catch blocks for robustness

## Resources

- **Main Documentation**: [README.md](../README.md)
- **API Reference**: [docs/API.md](API.md)
- **Development Guide**: [docs/DEVELOPMENT.md](DEVELOPMENT.md)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)
