# Development Guide

Guide for developers who want to contribute to or extend LatviaOSM-Check.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Architecture](#project-architecture)
- [Code Style](#code-style)
- [Testing](#testing)
- [Adding New Features](#adding-new-features)
- [Data Pipeline](#data-pipeline)
- [Web Application](#web-application)
- [Debugging](#debugging)

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- IDE (VS Code, PyCharm recommended)
- Basic knowledge of Python, Flask, GeoPandas

### Initial Setup

```bash
# Clone repository
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies including dev tools
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Development Dependencies

Create `requirements-dev.txt`:

```txt
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1

# Code quality
black>=23.7.0
flake8>=6.1.0
mypy>=1.5.0
pylint>=2.17.5

# Documentation
sphinx>=7.1.2
sphinx-rtd-theme>=1.3.0

# Development tools
ipython>=8.14.0
jupyter>=1.0.0
pre-commit>=3.3.3
```

---

## Project Architecture

### Directory Structure

```
latvia_osm_project/
├── app.py                    # Flask application entry point
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── processing/           # Data processing modules
│   │   ├── create_fuzzy_mapping.py
│   │   ├── generate_corrected_completeness.py
│   │   └── generate_quality_report.py
│   └── utils/                # Utility functions
│       ├── geo_utils.py      # Geospatial utilities
│       ├── data_loader.py    # Data loading functions
│       └── validators.py     # Data validation
├── scripts/                  # Pipeline scripts
│   ├── 00_convert_official_stats.py
│   ├── 02_extract_roads.py
│   └── ...
├── templates/                # Flask HTML templates
├── static/                   # Static assets (CSS, JS)
├── data/                     # Data files
│   ├── raw/                  # Original data
│   └── processed/            # Processed data
├── outputs/                  # Generated outputs
│   ├── exports/              # Export files
│   └── maps/                 # Generated maps
├── tests/                    # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── docs/                     # Documentation
```

### Code Organization

#### `app.py`
Main Flask application with routes and API endpoints.

**Key Components:**
- Route handlers (`@app.route`)
- API endpoints (`/api/*`)
- Data caching
- Error handling

#### `src/processing/`
Data processing and analysis modules.

**Modules:**
- `create_fuzzy_mapping.py`: Municipality name matching
- `generate_corrected_completeness.py`: Completeness calculations
- `generate_quality_report.py`: Quality metrics
- `get_stats.py`: Statistics generation

#### `scripts/`
Standalone processing scripts for the data pipeline.

**Naming Convention:**
- `00-09`: Data preparation
- `10-19`: Feature extraction
- `20-29`: Spatial analysis
- `30-39`: Visualization

---

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Maximum line length: 100 characters
# Use 4 spaces for indentation
# Use double quotes for strings

# Good
def calculate_completeness(osm_data: pd.DataFrame, 
                          official_data: pd.DataFrame) -> pd.DataFrame:
    """Calculate OSM completeness by comparing with official data.
    
    Args:
        osm_data: OSM road data with geometry
        official_data: Official statistics data
        
    Returns:
        DataFrame with completeness metrics
    """
    pass

# Bad
def calc_comp(osm,off):
    pass
```

### Import Order

```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party packages
import pandas as pd
import geopandas as gpd
from flask import Flask, jsonify

# 3. Local modules
from src.processing import create_fuzzy_mapping
from src.utils import geo_utils
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Dict, Optional, Tuple
import pandas as pd
import geopandas as gpd

def process_municipalities(
    gdf: gpd.GeoDataFrame,
    stats: pd.DataFrame,
    threshold: float = 0.8
) -> Tuple[gpd.GeoDataFrame, List[str]]:
    """Process municipality data with fuzzy matching."""
    pass
```

### Documentation

Use Google-style docstrings:

```python
def spatial_join_roads(
    roads: gpd.GeoDataFrame,
    municipalities: gpd.GeoDataFrame,
    how: str = "inner"
) -> gpd.GeoDataFrame:
    """Perform spatial join between roads and municipalities.
    
    Args:
        roads: GeoDataFrame containing road geometries
        municipalities: GeoDataFrame containing municipality boundaries
        how: Join type ('inner', 'left', 'right')
        
    Returns:
        GeoDataFrame with joined data
        
    Raises:
        ValueError: If CRS do not match
        
    Example:
        >>> roads = gpd.read_file('roads.geojson')
        >>> munis = gpd.read_file('municipalities.geojson')
        >>> result = spatial_join_roads(roads, munis)
    """
    if roads.crs != municipalities.crs:
        raise ValueError("CRS must match")
        
    return gpd.sjoin(roads, municipalities, how=how, predicate="within")
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_fuzzy_matching.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_fuzzy_matching.py::test_exact_match
```

### Writing Tests

#### Unit Test Example

```python
# tests/unit/test_fuzzy_matching.py
import pytest
import pandas as pd
from src.processing.create_fuzzy_mapping import fuzzy_match_names

def test_exact_match():
    """Test exact name matching."""
    osm_names = ["Rīga", "Daugavpils", "Jelgava"]
    official_names = ["Rīga", "Daugavpils", "Jelgava"]
    
    result = fuzzy_match_names(osm_names, official_names)
    
    assert len(result) == 3
    assert all(result["match_score"] == 100)

def test_fuzzy_match():
    """Test fuzzy matching with slight variations."""
    osm_names = ["Riga", "Daugavpils novads"]
    official_names = ["Rīga", "Daugavpils"]
    
    result = fuzzy_match_names(osm_names, official_names, threshold=0.8)
    
    assert len(result) == 2
    assert all(result["match_score"] >= 80)

def test_no_match():
    """Test when no match is found."""
    osm_names = ["Unknown City"]
    official_names = ["Rīga", "Daugavpils"]
    
    result = fuzzy_match_names(osm_names, official_names)
    
    assert len(result) == 0
```

#### Integration Test Example

```python
# tests/integration/test_pipeline.py
import pytest
from pathlib import Path
import geopandas as gpd

def test_full_road_pipeline():
    """Test complete road processing pipeline."""
    # This would run the full pipeline
    from scripts import extract_roads, spatial_join, calculate_completeness
    
    # Extract roads
    roads = extract_roads.process()
    assert len(roads) > 0
    
    # Spatial join
    joined = spatial_join.process(roads)
    assert "municipality_name" in joined.columns
    
    # Calculate completeness
    completeness = calculate_completeness.process(joined)
    assert "completeness_pct" in completeness.columns
```

#### Fixture Example

```python
# tests/conftest.py
import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

@pytest.fixture
def sample_municipalities():
    """Create sample municipality data."""
    data = {
        "municipality_name": ["Rīga", "Daugavpils"],
        "Area_Type": ["City", "City"],
        "geometry": [
            Polygon([(24, 56), (24, 57), (25, 57), (25, 56)]),
            Polygon([(26, 55), (26, 56), (27, 56), (27, 55)])
        ]
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")

@pytest.fixture
def sample_roads():
    """Create sample road data."""
    data = {
        "road_id": [1, 2, 3],
        "road_name": ["A1", "A2", "A3"],
        "length_km": [10.5, 8.3, 15.2],
        "geometry": [
            Point(24.5, 56.5),
            Point(24.6, 56.6),
            Point(26.5, 55.5)
        ]
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")
```

---

## Adding New Features

### Adding a New Data Source

#### 1. Create Extraction Script

```python
# scripts/31_extract_railways.py
"""Extract railway data from OSM."""

import geopandas as gpd
from pathlib import Path

def extract_railways():
    """Extract railway features from OSM PBF file."""
    input_file = Path("data/raw/latvia-latest.osm.pbf")
    output_file = Path("data/processed/railways.geojson")
    
    # Use ogr2ogr or geopandas to extract
    # Filter for railway features
    railways = gpd.read_file(
        input_file,
        layer="lines",
        where="railway IS NOT NULL"
    )
    
    # Save
    railways.to_file(output_file, driver="GeoJSON")
    print(f"Extracted {len(railways)} railways")

if __name__ == "__main__":
    extract_railways()
```

#### 2. Add Processing Module

```python
# src/processing/process_railways.py
"""Process railway data."""

import pandas as pd
import geopandas as gpd

def calculate_railway_completeness(
    osm_railways: gpd.GeoDataFrame,
    official_railways: pd.DataFrame
) -> pd.DataFrame:
    """Calculate railway completeness metrics."""
    # Implementation
    pass
```

#### 3. Add API Endpoint

```python
# In app.py
@app.route('/api/railway-data')
def get_railway_data():
    """Get railway completeness data."""
    try:
        railway_file = ROOT / 'outputs' / 'exports' / 'railway_stats.csv'
        df = pd.read_csv(railway_file)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/railways')
def railways_map():
    """Display railways map."""
    map_file = ROOT / 'outputs' / 'maps' / 'railway_map.html'
    if map_file.exists():
        return send_file(map_file)
    return "Railways map not available", 404
```

#### 4. Update Documentation

Add to [README.md](../README.md) and [API.md](API.md).

---

## Data Pipeline

### Pipeline Workflow

```
┌─────────────────┐
│  Raw OSM Data   │
│  (PBF format)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Feature │ ← scripts/02_extract_roads.py
│   (GeoJSON)     │   scripts/11_extract_forests.py
└────────┬────────┘   scripts/21_extract_libraries.py
         │
         ▼
┌─────────────────┐
│ Spatial Join    │ ← scripts/04_spatial_join.py
│  with Munis     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fuzzy Matching  │ ← src/processing/create_fuzzy_mapping.py
│  Municipality   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Completeness   │ ← src/processing/generate_corrected_completeness.py
│   Calculation   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualization  │ ← scripts/07_create_interactive_map.py
│  (HTML Maps)    │
└─────────────────┘
```

### Creating a New Pipeline Script

```python
#!/usr/bin/env python3
"""
Script: 32_railway_spatial_join.py
Purpose: Spatially join railways with municipalities
"""

import sys
from pathlib import Path
import geopandas as gpd
import pandas as pd

# Add src to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.geo_utils import ensure_crs, validate_geometries

def main():
    """Main processing function."""
    print("=" * 70)
    print("Railway Spatial Join")
    print("=" * 70)
    
    # Load data
    print("\n1. Loading data...")
    railways = gpd.read_file(ROOT / "data" / "processed" / "railways.geojson")
    munis = gpd.read_file(ROOT / "data" / "processed" / "municipalities.geojson")
    
    print(f"   Railways: {len(railways):,}")
    print(f"   Municipalities: {len(munis):,}")
    
    # Ensure same CRS
    print("\n2. Ensuring consistent CRS...")
    railways = ensure_crs(railways, "EPSG:4326")
    munis = ensure_crs(munis, "EPSG:4326")
    
    # Validate geometries
    print("\n3. Validating geometries...")
    railways = validate_geometries(railways)
    
    # Spatial join
    print("\n4. Performing spatial join...")
    joined = gpd.sjoin(railways, munis, how="left", predicate="within")
    
    # Aggregate by municipality
    print("\n5. Aggregating by municipality...")
    stats = joined.groupby("municipality_name").agg({
        "length_km": "sum",
        "railway": "count"
    }).rename(columns={"railway": "railway_count"})
    
    # Save
    output_file = ROOT / "data" / "processed" / "railways_by_municipality.geojson"
    print(f"\n6. Saving to {output_file}...")
    joined.to_file(output_file, driver="GeoJSON")
    
    stats_file = ROOT / "outputs" / "exports" / "railway_stats.csv"
    stats.to_csv(stats_file)
    
    print("\n✓ Complete!")
    print(f"   Output: {output_file}")
    print(f"   Stats: {stats_file}")

if __name__ == "__main__":
    main()
```

---

## Web Application

### Flask Application Structure

```python
# app.py
from flask import Flask, render_template, jsonify, send_file
from pathlib import Path
import json

app = Flask(__name__)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Cache
_data_cache = {}

def load_geojson(file_path):
    """Load and cache GeoJSON data."""
    if file_path not in _data_cache:
        with open(file_path) as f:
            _data_cache[file_path] = json.load(f)
    return _data_cache[file_path]

@app.route('/')
def index():
    """Main page with interactive map."""
    return render_template('dynamic_map.html')

@app.route('/api/data')
def api_data():
    """API endpoint for data."""
    try:
        data = load_geojson('outputs/exports/data.geojson')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Adding New Templates

```html
<!-- templates/new_feature.html -->
<!DOCTYPE html>
<html>
<head>
    <title>New Feature - LatviaOSM-Check</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map { height: 600px; }
    </style>
</head>
<body>
    <h1>New Feature Visualization</h1>
    <div id="map"></div>
    
    <script>
        // Initialize map
        const map = L.map('map').setView([56.9496, 24.1052], 7);
        
        // Add base layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Load data
        fetch('/api/new-feature-data')
            .then(response => response.json())
            .then(data => {
                L.geoJSON(data, {
                    onEachFeature: function(feature, layer) {
                        layer.bindPopup(`<b>${feature.properties.name}</b>`);
                    }
                }).addTo(map);
            });
    </script>
</body>
</html>
```

---

## Debugging

### Debugging Tips

#### 1. Enable Flask Debug Mode

```python
# app.py
if __name__ == '__main__':
    app.run(debug=True)  # Auto-reload on code changes
```

#### 2. Add Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def process_data():
    logger.debug("Starting data processing")
    logger.info("Processing 1000 records")
    logger.warning("Low memory")
    logger.error("Failed to load file")
```

#### 3. Use IPython for Interactive Debugging

```python
# Insert breakpoint
import IPython; IPython.embed()
```

#### 4. Profile Performance

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
process_large_dataset()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest functions
```

---

## Best Practices

### 1. Error Handling

```python
def safe_load_data(file_path: Path) -> Optional[gpd.GeoDataFrame]:
    """Safely load geodata with error handling."""
    try:
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None
            
        gdf = gpd.read_file(file_path)
        
        if len(gdf) == 0:
            logger.warning(f"Empty dataset: {file_path}")
            return None
            
        return gdf
        
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}")
        return None
```

### 2. Memory Management

```python
# Process large files in chunks
import pandas as pd

for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process_chunk(chunk)
    del chunk  # Free memory
```

### 3. Code Reusability

```python
# src/utils/geo_utils.py
def ensure_crs(gdf: gpd.GeoDataFrame, target_crs: str) -> gpd.GeoDataFrame:
    """Ensure GeoDataFrame has target CRS."""
    if gdf.crs != target_crs:
        return gdf.to_crs(target_crs)
    return gdf

def validate_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Fix invalid geometries."""
    gdf['geometry'] = gdf['geometry'].buffer(0)
    return gdf
```

---

## Resources

- **GeoPandas Documentation**: https://geopandas.org
- **Flask Documentation**: https://flask.palletsprojects.com
- **Shapely Documentation**: https://shapely.readthedocs.io
- **OSM Wiki**: https://wiki.openstreetmap.org

---

## Getting Help

- Open an issue on GitHub
- Check existing documentation
- Ask in discussions
- Contact maintainers
