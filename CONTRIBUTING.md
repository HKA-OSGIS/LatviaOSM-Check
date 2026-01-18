# LatviaOSM-Check Contributing Guide

Thank you for your interest in contributing to LatviaOSM-Check!

## Development Setup

1. **Clone the repository**
   ```powershell
   git clone <repository-url>
   cd latvia_osm_project
   ```

2. **Run setup**
   ```powershell
   .\setup.ps1
   ```

3. **Start development server**
   ```powershell
   .\run.ps1
   ```

## Project Structure

```
latvia_osm_project/
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── setup.ps1                       # Environment setup script
├── run.ps1                         # Application launcher
├── README.md                       # Main documentation
├── docs/                           # Documentation
│   ├── QUICK_GUIDE.md             # Quick start guide
│   └── IMPLEMENTATION_SUMMARY_NOVADS.md  # Technical details
├── src/                            # Source code
│   ├── processing/                 # Data processing scripts
│   │   ├── create_fuzzy_mapping.py
│   │   ├── generate_corrected_completeness.py
│   │   ├── generate_quality_report.py
│   │   └── get_stats.py
│   └── utils/                      # Utility functions
├── scripts/                        # Pipeline scripts
│   ├── 00_convert_official_stats.py
│   ├── 02_extract_roads.py
│   ├── 03_process_municipalities.py
│   ├── 04_spatial_join.py
│   ├── 05_calculate_completeness.py
│   ├── 07_create_interactive_map.py
│   └── 08_create_lau1_map.py
├── templates/                      # Flask HTML templates
│   ├── dynamic_map.html
│   └── with_dropdown.html
├── static/                         # Static assets (CSS, JS, images)
├── data/                           # Data files
│   ├── raw/                        # Original datasets
│   └── processed/                  # Processed datasets
└── outputs/                        # Generated outputs
    ├── exports/                    # Export files (CSV, GeoJSON)
    └── maps/                       # Generated maps

```

## Development Workflow

### Adding New Features

1. Create a new branch
   ```powershell
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test locally
   ```powershell
   .\run.ps1
   ```

4. Commit and push
   ```powershell
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

### Processing Pipeline

The data processing pipeline follows these steps:

1. **Fuzzy Name Matching** (`src/processing/create_fuzzy_mapping.py`)
   - Matches GeoJSON municipality names with official statistics
   - Uses 80% similarity threshold
   - Handles Latvian genitive case

2. **Completeness Calculation** (`src/processing/generate_corrected_completeness.py`)
   - Calculates OSM road completeness per municipality
   - Compares OSM data with official statistics

3. **Quality Reports** (`src/processing/generate_quality_report.py`)
   - Generates data quality metrics
   - Identifies data gaps

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic

### Testing

Before submitting:
1. Verify all 36 novads display correctly
2. Check data integrity (no NULL values)
3. Test map interactions
4. Verify API endpoints return correct data

## Adding New Data Sources

1. Place raw data in `data/raw/`
2. Create processing script in `src/processing/`
3. Output processed data to `data/processed/`
4. Update documentation

## Reporting Issues

When reporting issues, include:
- Description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (Python version, OS)

## Questions?

Open an issue or contact the maintainers.

## License

This project is part of the LatviaOSM-Check initiative to improve OpenStreetMap coverage in Latvia.
