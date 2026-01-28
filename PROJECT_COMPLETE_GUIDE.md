# LatviaOSM-Check: Complete Project Guide

**Date**: January 2026  
**Version**: 1.0  
**Purpose**: Comprehensive documentation of the LatviaOSM-Check project - architecture, components, data flow, and implementation details.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Data Pipeline](#data-pipeline)
5. [Components & Modules](#components--modules)
6. [Frontend-Backend Communication](#frontend-backend-communication)
7. [Data Files Structure](#data-files-structure)
8. [Running the Project](#running-the-project)
9. [Licensing](#licensing)
10. [Scalability & Performance](#scalability--performance)
11. [Common Workflows](#common-workflows)

---

## Project Overview

### What is LatviaOSM-Check?

LatviaOSM-Check is a geospatial data analysis platform that measures the **completeness of OpenStreetMap (OSM) data** in Latvia by comparing it against official government datasets. It analyzes three main categories:

- **Roads** - Road network coverage
- **Forests** - Forest area coverage
- **Libraries** - Public library locations

### Key Metrics

For each category, the system calculates:
- **Completeness (%)** = (OSM Count / Official Count) × 100
- Example: If OSM has 1,200 forests but official records show 1,000, completeness = 120%

### Purpose

- Track OSM data quality in Latvia
- Identify regions with incomplete mapping
- Support OSM community improvement efforts
- Provide interactive visualizations of data gaps
- Enable comparisons across municipalities and administrative regions (novads)

---

## Architecture

### 7-Layer Architecture Model

```
┌─────────────────────────────────────────────┐
│ 7. User Interface (Leaflet Maps, UI)       │
├─────────────────────────────────────────────┤
│ 6. Frontend (HTML, CSS, JavaScript, Bootstrap)│
├─────────────────────────────────────────────┤
│ 5. Web Application (Flask Routes & API)     │
├─────────────────────────────────────────────┤
│ 4. Data Output (GeoJSON, CSV, HTML Maps)   │
├─────────────────────────────────────────────┤
│ 3. Processing Modules (Fuzzy Matching, etc)│
├─────────────────────────────────────────────┤
│ 2. Processing Pipeline (20 Sequential Scripts)│
├─────────────────────────────────────────────┤
│ 1. Data Input (OSM PBF, CSV, GeoJSON)      │
└─────────────────────────────────────────────┘
```

### 6 Core Components

#### 1. **Data Input Layer**
- Raw OSM data (`latvia-latest.osm.pbf` ~200MB)
- Official statistics (CSV files: Forest.csv, Library.csv, Road.csv)
- Municipality boundaries (GeoJSON)
- Official government data files

**Location**: `data/raw/`

#### 2. **Processing Pipeline**
- 20 sequential numbered scripts that transform raw data
- Scripts organized in 5 stages: Extract → Standardize → Join → Calculate → Output

**Location**: `scripts/` (00-99 numbered Python files)

**Key Scripts**:
```
00_convert_official_stats.py      → Standardize official data format
02_extract_roads.py               → Extract roads from OSM
03_process_municipalities.py       → Clean municipality boundaries
04_spatial_join.py                → Link roads to municipalities
05_calculate_completeness.py      → Calculate road completeness
11_extract_forests.py             → Extract forests from OSM
21_extract_libraries.py           → Extract libraries from OSM
99_create_comprehensive_geojson.py → Merge all outputs
```

#### 3. **Processing Modules**
Reusable Python functions for common geospatial operations.

**Location**: `src/processing/`

**Key Modules**:
- `create_fuzzy_mapping.py` - Match Latvian municipality names (handle spelling variations)
- `generate_corrected_completeness.py` - Calculate completeness metrics
- `generate_quality_report.py` - Generate analysis reports
- `get_stats.py` - Aggregate statistics by region

#### 4. **Data Output Layer**
Generated processed data ready for web display.

**Location**: `data/processed/`

**Key Files**:
```
forests_by_novads.geojson      → Forest features grouped by administrative region
forests.geojson                → All forest features
libraries_by_novads.geojson    → Library features grouped by region
roads_by_municipality.geojson  → Road features by municipality
municipalities.geojson         → Administrative boundary polygons
```

**Properties in GeoJSON**:
```json
{
  "municipality_name": "Rīga",
  "osm_count": 1245,
  "official_count": 1089,
  "completeness_pct": 114.3,
  "data_source": "OSM",
  "last_updated": "2026-01-28"
}
```

#### 5. **Web Application (Flask Backend)**
HTTP server that serves data and renders templates.

**Location**: `app.py` (328 lines)

**Key Routes**:
```python
GET  /                          → Main roads completeness page
GET  /forests                   → Forest completeness page
GET  /libraries                 → Library completeness page
GET  /combined-map              → All features on one map
GET  /api/geojson-data          → JSON endpoint for roads
GET  /api/forest-data           → JSON endpoint for forests
GET  /api/library-data          → JSON endpoint for libraries
GET  /api/csv-data              → CSV statistics endpoint
```

**Caching System** (In-Memory Performance):
```python
_geojson_cache = None              # Roads GeoJSON cache
_dataframe_cache = None            # Roads DataFrame cache
_forest_dataframe_cache = None     # Forests DataFrame cache
_library_dataframe_cache = None    # Libraries DataFrame cache

def load_geojson():
    global _geojson_cache
    if _geojson_cache is None:     # Check if cached
        _geojson_cache = json.load(open('data/processed/roads.geojson'))
    return _geojson_cache           # Return from memory
```

#### 6. **Frontend (HTML/CSS/JavaScript)**
Interactive maps and user interface.

**Location**: `templates/`

**Key Templates**:
- `dynamic_map.html` - Main interactive map with Leaflet.js
- `with_dropdown.html` - Alternative UI with dropdown selectors

**Frontend Stack**:
- **Leaflet.js** - Interactive mapping library
- **Bootstrap 5** - Responsive CSS framework
- **jQuery** - JavaScript utilities
- **OpenStreetMap tiles** - Base map imagery

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.8+ | Core programming language |
| Flask | 2.3.3 | Web framework, routing, templating |
| GeoPandas | 0.13.2 | Geospatial data processing, spatial joins |
| Pandas | 1.5+ | Data manipulation and analysis |
| Shapely | 2.0+ | Geometric operations |
| FuzzyWuzzy | 0.18+ | String matching for municipality names |
| GDAL/OGR | 3.x | Geospatial data format conversion |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Leaflet.js | 1.9+ | Interactive mapping |
| Bootstrap | 5.x | Responsive design |
| jQuery | 3.x | DOM manipulation |
| OpenStreetMap | Latest | Base map tiles |
| HTML5 | - | Markup |
| CSS3 | - | Styling |

### Data Formats
| Format | Usage | Example |
|--------|-------|---------|
| GeoJSON | Spatial features + properties | `roads.geojson`, `forests_by_novads.geojson` |
| CSV | Tabular data | `Forest.csv`, `official_forest_stats.csv` |
| JSON | API responses | `/api/geojson-data` endpoint |
| GeoPackage | Optional spatial database | Not currently used |
| Shapefile | Legacy format support | Via GDAL/OGR |

### Coordinate Reference System (CRS)
- **Primary**: EPSG:4326 (WGS84) - latitude/longitude
- **Processing**: May use EPSG:3059 (LKS92) for accurate distance calculations
- **Conversion**: GeoPandas handles CRS transformations automatically

---

## Data Pipeline

### Complete Data Flow

```
Raw Data (OSM PBF + CSV)
         ↓
    [Extract]  ← Scripts 02, 11, 21
         ↓
Feature Data (Raw features)
         ↓
  [Standardize] ← Scripts 00, 03
         ↓
Clean Data (Consistent format)
         ↓
  [Spatial Join] ← Scripts 04, 12, 22
         ↓
Features + Boundaries (Roads in municipalities)
         ↓
[Calculate Metrics] ← Scripts 05, 13, 23
         ↓
Completeness Data (with percentages)
         ↓
  [Output Generation] ← Scripts 07-27, 99
         ↓
Final Outputs (GeoJSON, CSV, HTML maps)
         ↓
      app.py
         ↓
   Web Interface
         ↓
   User Views Map
```

### Stage Breakdown

#### Stage 1: Extract (Scripts 02, 11, 21)
**Purpose**: Parse raw data and extract features of interest

**Process**:
```python
# Script 02_extract_roads.py
import osmium
osm_data = osmium.OSMFile('data/raw/latvia-latest.osm.pbf')
roads = osm_data.get_ways_with_tag('highway')  # Filter to roads only
```

**Output**: Cleaned road GeoDataFrame with geometries

#### Stage 2: Standardize (Scripts 00, 03)
**Purpose**: Ensure consistent data format across sources

**Process**:
```python
# Script 00_convert_official_stats.py
official_df = pd.read_csv('data/raw/official_forest_stats.csv')
# Normalize column names: 'Forest Name' → 'name', 'Count' → 'osm_count'
official_df.columns = ['municipality', 'official_count', 'data_date']
```

**Output**: Standardized DataFrames with consistent schemas

#### Stage 3: Spatial Join (Scripts 04, 12, 22)
**Purpose**: Link features to administrative boundaries

**Process**:
```python
# Script 04_spatial_join.py
import geopandas as gpd
roads = gpd.read_file('data/processed/roads_raw.geojson')
municipalities = gpd.read_file('data/processed/municipalities.geojson')

# Link each road to its municipality
roads_with_municipality = gpd.sjoin(
    roads, municipalities, 
    how='left', 
    predicate='within'  # Road is within municipality polygon
)
```

**Output**: Features with municipality_id and municipality_name columns

#### Stage 4: Calculate Metrics (Scripts 05, 13, 23)
**Purpose**: Compute completeness percentages

**Process**:
```python
# Script 05_calculate_completeness.py
osm_count = roads_with_municipality.groupby('municipality_name').size()
official_count = official_df.set_index('municipality')['count']

completeness = (osm_count / official_count * 100).round(1)
# Result: {'Rīga': 114.3, 'Daugavpils': 91.0, ...}
```

**Output**: GeoJSON with completeness_pct property

#### Stage 5: Output Generation (Scripts 07-27, 99)
**Purpose**: Create maps and exports

**Process**:
```python
# Script 07_create_interactive_map.py
import folium
map_obj = folium.Map(location=[56.88, 24.60], zoom_start=8)
folium.GeoJson(roads_geojson).add_to(map_obj)
map_obj.save('outputs/maps/interactive_map.html')
```

**Output**: Interactive HTML maps, CSV exports, comprehensive GeoJSON

---

## Components & Modules

### Core Processing Modules (src/processing/)

#### create_fuzzy_mapping.py
**Purpose**: Handle Latvian municipality name variations

```python
from fuzzywuzzy import fuzz

def match_municipality_name(osm_name, official_names_list):
    """Find best match for municipality name"""
    best_match = None
    best_score = 0
    
    for official_name in official_names_list:
        score = fuzz.token_set_ratio(osm_name, official_name)
        if score > best_score:
            best_score = score
            best_match = official_name
    
    return best_match if best_score > 80 else None
```

**Usage**: Correct spelling variations in municipality names before joining

#### generate_corrected_completeness.py
**Purpose**: Calculate completeness with quality checks

```python
def calculate_completeness(osm_features, official_count, 
                          municipality_name):
    """
    Calculate completeness percentage with validation
    
    Args:
        osm_features: GeoDataFrame of OSM data
        official_count: Integer count from official records
        municipality_name: String municipality identifier
    
    Returns:
        float: Completeness percentage (can exceed 100%)
    """
    osm_count = len(osm_features)
    if official_count == 0:
        return None  # Cannot calculate with zero official records
    
    completeness = (osm_count / official_count) * 100
    return round(completeness, 1)
```

**Output**: Validated completeness metrics with quality flags

#### generate_quality_report.py
**Purpose**: Analyze data quality and generate reports

```python
def generate_report(geojson_path, output_path):
    """Generate markdown report of data quality"""
    gdf = gpd.read_file(geojson_path)
    
    report = f"""
    # Data Quality Report
    
    Total Features: {len(gdf)}
    CRS: {gdf.crs}
    Completeness Range: {gdf['completeness_pct'].min():.1f}% - {gdf['completeness_pct'].max():.1f}%
    Average Completeness: {gdf['completeness_pct'].mean():.1f}%
    
    ## Completeness by Municipality
    {gdf.groupby('municipality_name')['completeness_pct'].agg(['mean', 'min', 'max'])}
    """
    
    with open(output_path, 'w') as f:
        f.write(report)
```

#### get_stats.py
**Purpose**: Aggregate statistics across regions

```python
def aggregate_statistics(geojson_path, level='municipality'):
    """Aggregate stats by municipality or novads"""
    gdf = gpd.read_file(geojson_path)
    
    stats = gdf.groupby(f'{level}_name').agg({
        'osm_count': 'sum',
        'official_count': 'sum',
        'completeness_pct': 'mean'
    })
    
    stats['aggregated_completeness'] = (
        stats['osm_count'] / stats['official_count'] * 100
    )
    
    return stats.round(1)
```

---

## Frontend-Backend Communication

### Request-Response Cycle

#### Step 1: User Action
```javascript
// User clicks "View Forest Data" button or navigates to /forests
```

#### Step 2: Frontend HTTP Request
```javascript
// In templates/dynamic_map.html
async function loadForestData() {
    const response = await fetch('/api/forest-data');  // GET request
    return response.json();  // Parse JSON response
}
```

#### Step 3: Backend Route Handler
```python
# In app.py
@app.route('/api/forest-data')
def get_forest_data():
    """Return forest completeness data as GeoJSON."""
    data = load_forest_dataframe()  # Check cache first
    
    if data is None:
        return jsonify({'error': 'Data not found'}), 404
    
    # Convert GeoPandas to GeoJSON
    geojson = json.loads(data.to_json())
    return jsonify(geojson)
```

#### Step 4: Caching Check
```python
def load_forest_dataframe():
    global _forest_dataframe_cache
    
    # If data already in memory, return immediately (fast!)
    if _forest_dataframe_cache is not None:
        return _forest_dataframe_cache
    
    # Otherwise, load from disk
    forest_file = Path('data/processed/forests_by_novads.geojson')
    if forest_file.exists():
        _forest_dataframe_cache = gpd.read_file(forest_file)
        return _forest_dataframe_cache
    
    return None
```

#### Step 5: JSON Response
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "municipality_name": "Rīga",
        "osm_count": 1245,
        "official_count": 1089,
        "completeness_pct": 114.3
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[24.0, 56.9], [24.1, 56.9], ...]]
      }
    },
    // ... more features
  ]
}
```

#### Step 6: Frontend Rendering
```javascript
// Leaflet renders the GeoJSON on the map
L.geoJSON(data, {
    style: function(feature) {
        const completeness = feature.properties.completeness_pct;
        
        // Color based on completeness level
        if (completeness > 100) return {color: '#27ae60', weight: 2};  // Green
        if (completeness > 80) return {color: '#f39c12', weight: 2};   // Orange
        return {color: '#e74c3c', weight: 2};                          // Red
    },
    onEachFeature: function(feature, layer) {
        // Show popup on click
        const popup = `
            <b>${feature.properties.municipality_name}</b><br>
            OSM: ${feature.properties.osm_count}<br>
            Official: ${feature.properties.official_count}<br>
            Completeness: ${feature.properties.completeness_pct}%
        `;
        layer.bindPopup(popup);
    }
}).addTo(map);
```

#### Step 7: User Interaction
```javascript
// User clicks polygon → popup appears
// User hovers → highlight feature
// User zooms → Leaflet adjusts display
```

### Communication Endpoints Summary

| Endpoint | Method | Returns | Cache | Use Case |
|----------|--------|---------|-------|----------|
| `/api/geojson-data` | GET | GeoJSON | Yes | Road completeness map |
| `/api/forest-data` | GET | GeoJSON | Yes | Forest completeness map |
| `/api/library-data` | GET | GeoJSON | Yes | Library completeness map |
| `/api/csv-data` | GET | CSV | No | Download statistics |

### Performance Optimization

**Caching Strategy**:
- First request: Load file from disk (~100-500ms)
- Subsequent requests: Return from memory (~1ms)
- Cache cleared when app restarts

**JSON Compression**:
- GeoJSON files can be large (~5-10MB)
- Browsers automatically decompress with gzip
- Consider simplifying geometries for very large datasets

**AJAX Benefits**:
- Asynchronous loading (UI doesn't freeze)
- Partial data updates (load only needed features)
- Client-side rendering (server not overloaded)

---

## Data Files Structure

### Raw Data (`data/raw/`)

```
Forest.csv                      (2.3MB)
├─ municipality_name (Rīga, Daugavpils, ...)
├─ forest_count
├─ forest_area_hectares
└─ data_source (official government)

Library.csv                     (0.8MB)
├─ municipality_name
├─ library_count
├─ library_locations
└─ update_date

Road.csv                        (1.2MB)
├─ municipality_name
├─ road_length_km
├─ road_count
└─ classification (primary, secondary, tertiary)

latvia-latest.osm.pbf           (~200MB) *Not in git
├─ All OSM features for Latvia
├─ Ways: roads, buildings, natural areas
├─ Nodes: points of interest
├─ Relations: complex geometries
└─ Tags: metadata (highway=primary, natural=forest, etc.)

municipalities.geojson          (0.5MB)
├─ Feature: municipality boundaries
├─ Properties: name, population, area
└─ Geometry: Polygon boundaries

official_forest_stats.csv        (0.3MB)
├─ Official government forest statistics
├─ By municipality
└─ Used for completeness calculation
```

### Processed Data (`data/processed/`)

```
forests.geojson                 (2.1MB)
├─ Feature: Each forest polygon from OSM
├─ Properties: name, area, completeness_pct
└─ Geometry: Polygon (forest boundary)

forests_by_novads.geojson       (1.8MB)
├─ Feature: Aggregated by administrative region
├─ Properties: novads_name, osm_count, official_count, completeness_pct
└─ Used for regional analysis

roads_by_municipality.geojson   (3.4MB)
├─ Feature: Roads linked to municipalities
├─ Properties: road_type, municipality_name, completeness_pct
└─ Geometry: LineString (road path)

libraries_by_novads.geojson     (0.9MB)
├─ Feature: Libraries aggregated by region
├─ Properties: library_count, completeness_pct
└─ Geometry: Point (library location)

municipalities.geojson          (0.5MB)
├─ Administrative boundaries
├─ Used for spatial joins
└─ CRS: EPSG:4326
```

### Output Data (`outputs/`)

#### Exports (`outputs/exports/`)
```
completeness_municipalities.csv
├─ municipality_name, osm_count, official_count, completeness_pct
└─ One row per municipality

completeness_forests.csv
├─ Similar structure for forests
└─ Grouped by novads (administrative region)

completeness_libraries.csv
├─ Library completeness by region
└─ Used for analysis reports

latvia_lau1.geojson
├─ Administrative boundaries with completeness data
├─ LAU1 = Local Administrative Units level 1
└─ Complete dataset for all features

forest_completeness_full_report.txt
├─ Detailed analysis of forest completeness
├─ Statistics, trends, recommendations
└─ Generated by generate_quality_report.py
```

#### Maps (`outputs/maps/`)
```
interactive_map.html            (~8MB)
├─ Main interactive road completeness map
├─ Leaflet.js + Folium generated
├─ Standalone HTML file
└─ Open in browser to view

forest_completeness_map.html    (~6MB)
├─ Forest-specific map
├─ Color-coded by completeness percentage
└─ Includes legend and info boxes

library_completeness_map.html   (~4MB)
├─ Library coverage map
├─ Point-based visualization
└─ Popup statistics on click

combined_map.html               (~12MB)
├─ All three features on one map
├─ Layer toggle control
├─ Comprehensive overview
└─ Used for presentations
```

---

## Running the Project

### Prerequisites

```powershell
# Windows PowerShell (Administrator)
python --version  # Python 3.8+
pip --version

# Required system libraries (Windows)
# Already included in GDAL Python package
```

### Installation Steps

#### Option 1: PowerShell Scripts (Recommended)

```powershell
# 1. Navigate to project directory
cd d:\GeoMatics\OpenSourceGIS\latvia_osm_project

# 2. Run setup script (installs dependencies)
.\setup.ps1

# 3. Run complete pipeline
.\run.ps1

# 4. Or run specific pipelines
.\run_forest_pipeline.ps1   # Forests only
.\run_library_pipeline.ps1  # Libraries only
```

#### Option 2: Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run pipeline
python scripts/00_convert_official_stats.py
python scripts/02_extract_roads.py
# ... continue through script 99

# Start Flask app
python app.py
```

### Running the Web Application

```powershell
# Start Flask server
python app.py

# Output:
# WARNING: This is a development server. Do not use it in production.
# Running on http://127.0.0.1:5000

# Open browser to:
# http://localhost:5000/forests     # Forest completeness
# http://localhost:5000/roads       # Road completeness (default)
# http://localhost:5000/libraries   # Library completeness
# http://localhost:5000/combined-map # All features
```

### Pipeline Execution

#### Full Pipeline (Road + Forest + Library)
```bash
python run.ps1
# Executes all 20+ scripts in sequence
# Estimated time: 30-60 minutes first run (depends on OSM download)
# Subsequent runs: 5-10 minutes (cached data)
```

#### Forest Pipeline Only
```bash
python run_forest_pipeline.ps1
# Runs scripts: 00, 03, 10, 11, 12, 13, 17, 99
# Estimated time: 10-15 minutes
```

#### Library Pipeline Only
```bash
python run_library_pipeline.ps1
# Runs scripts: 00, 03, 21, 22, 23, 27, 99
# Estimated time: 8-12 minutes
```

### Development Workflow

```bash
# 1. Make changes to script (e.g., 05_calculate_completeness.py)
nano scripts/05_calculate_completeness.py

# 2. Run specific script to test
python scripts/05_calculate_completeness.py

# 3. Check output
ls data/processed/roads.geojson

# 4. If output correct, run full pipeline
python run.ps1

# 5. Start Flask app to see changes
python app.py
```

---

## Licensing

### Project License: MIT

The **LatviaOSM-Check code** itself is licensed under MIT (Massachusetts Institute of Technology) license.

**MIT Allows**:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

**MIT Requires**:
- ✅ License notice included
- ✅ Original copyright notice preserved

### Data Licenses (Important!)

The **data used in this project** comes from multiple sources with different licenses:

| Data Source | License | Usage |
|-------------|---------|-------|
| OpenStreetMap (OSM) | ODbL 1.0 | Must share derivative works |
| Official Latvian Statistics | Various (see below) | Government records |
| Municipality Boundaries | Public domain | Latvia state data |
| Library Data | CC-BY-4.0 | Attribution required |

### Dependency Licenses

| Package | License | Version |
|---------|---------|---------|
| Flask | BSD-3-Clause | 2.3.3 |
| GeoPandas | BSD-3-Clause | 0.13.2 |
| Leaflet.js | BSD-2-Clause | 1.9+ |
| Bootstrap | MIT | 5.x |
| jQuery | MIT | 3.x |
| Folium | MIT | Latest |
| Pandas | BSD-3-Clause | 1.5+ |
| Shapely | BSD-3-Clause | 2.0+ |

### Compliance Checklist

- [x] MIT license text included in LICENSE file
- [x] Copyright notice in source files (optional for MIT)
- [x] ODbL 1.0 statement in README (OSM data requirement)
- [x] Dependency licenses documented
- [x] No GPL v3 dependencies (would require entire project to be GPL)
- [x] Attribution given to OSM contributors in visualizations

### How to Distribute

If you distribute this project:
1. Include LICENSE file (MIT)
2. Include README mentioning OSM/ODbL
3. Include list of dependencies and their licenses
4. Inform users that data may have different license terms

---

## Scalability & Performance

### Current Performance Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| Flask startup | 2-3 seconds | Load Python + dependencies |
| First API request | 100-500ms | First load from disk (JSON parsing) |
| Subsequent API requests | 1-3ms | From memory cache |
| Full pipeline run | 30-60 min | First run with OSM download |
| Subsequent pipeline | 5-10 min | Using cached data |

### Bottlenecks & Solutions

#### Bottleneck 1: Large GeoJSON Files
**Problem**: `roads.geojson` can be 10-15MB, slow parsing

**Solution**: 
- Caching in memory (current approach)
- Pre-generate simplified geometries
- Use GeoPackage format (smaller, faster)

```python
# Simplify geometries for faster rendering
gdf.geometry = gdf.geometry.simplify(tolerance=0.001)
gdf.to_file('data/processed/roads_simplified.geojson', driver='GeoJSON')
```

#### Bottleneck 2: Spatial Joins on Large Datasets
**Problem**: `gpd.sjoin()` is slow with millions of features

**Solution**:
- Use spatial index (GeoPandas does this automatically)
- Pre-partition data by region
- Use PostGIS database for very large datasets

```python
# GeoPandas automatically creates spatial index
joined = gpd.sjoin(roads, municipalities, predicate='within')
# First join: slower (creates index)
# Subsequent joins: faster (index reused)
```

#### Bottleneck 3: Flask Single Process
**Problem**: One request blocks all others

**Solution**:
- Use Gunicorn with multiple workers
- Add load balancer (Nginx)
- Use caching proxy (Redis)

```bash
# Production deployment
gunicorn -w 4 -b 0.0.0.0:5000 app:app
# -w 4 = 4 worker processes (one per request)
```

### Scalability Scenarios

#### Small Scale (Current)
- **Users**: 1-10 concurrent
- **Deployment**: Single server
- **App Server**: Flask dev server
- **Cost**: ~$5-10/month (small VM)

```
User → Flask (Single Process) → GeoJSON Files
```

#### Medium Scale
- **Users**: 100-500 concurrent
- **Deployment**: Single or 2-3 servers
- **App Server**: Gunicorn + Nginx
- **Cache**: Redis (for session + data)

```
User → Load Balancer → Gunicorn (4-8 workers) → Cache (Redis) → GeoJSON Files
```

#### Large Scale
- **Users**: 1,000+ concurrent
- **Deployment**: Distributed servers
- **App Server**: Kubernetes + Gunicorn
- **Database**: PostGIS (not file-based)
- **Cache**: Redis cluster

```
Users → CDN → Load Balancer → Kubernetes Cluster → PostGIS Database → Redis
```

### Production Deployment Example

#### Using Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
# Build and run
docker build -t latvia-osm-check .
docker run -p 5000:5000 latvia-osm-check
```

#### Using Gunicorn + Nginx

```bash
# Start Gunicorn
gunicorn -w 4 \
    -b 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/gunicorn.log \
    --error-logfile /var/log/gunicorn-error.log \
    app:app

# Nginx configuration
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

---

## Common Workflows

### Workflow 1: Run Everything Fresh

```powershell
# 1. Ensure latest OSM data
# Download from: https://download.geofabrik.de/europe/latvia-latest.osm.pbf
# Save to: data/raw/latvia-latest.osm.pbf

# 2. Install dependencies
.\setup.ps1

# 3. Run complete pipeline
.\run.ps1

# 4. Start web server
python app.py

# 5. Open browser
# http://localhost:5000/forests
```

**Expected Output**:
- ✅ `data/processed/forests.geojson` created
- ✅ `outputs/maps/forest_completeness_map.html` generated
- ✅ Web interface shows forest coverage map

### Workflow 2: Modify Completeness Calculation

**Scenario**: Change completeness formula from percentage to ratio

```python
# 1. Edit script
nano scripts/05_calculate_completeness.py

# OLD
completeness = (osm_count / official_count * 100)

# NEW
completeness = osm_count / official_count  # Now a ratio (1.14 = 114%)

# 2. Test single script
python scripts/05_calculate_completeness.py

# 3. Verify output
python -c "import json; print(json.load(open('data/processed/roads.geojson'))['features'][0]['properties'])"

# 4. Update Flask app if needed
# In app.py, update color scheme to use ratio instead of percentage

# 5. Run full pipeline and test in browser
.\run.ps1
python app.py
```

### Workflow 3: Add New Feature Type (e.g., Schools)

```bash
# 1. Create new script following pattern
cp scripts/11_extract_forests.py scripts/31_extract_schools.py

# 2. Modify extraction logic
nano scripts/31_extract_schools.py
# Change: natural=forest → amenity=school

# 3. Create matching spatial join script
cp scripts/12_forest_spatial_join.py scripts/32_school_spatial_join.py
nano scripts/32_school_spatial_join.py

# 4. Create completeness script
cp scripts/13_calculate_forest_completeness.py scripts/33_calculate_school_completeness.py

# 5. Create map generation script
cp scripts/17_create_forest_map.py scripts/37_create_school_map.py

# 6. Update run.ps1 to include new scripts in correct order

# 7. Update app.py
# Add: @app.route('/schools')
# Add: @app.route('/api/school-data')
# Add: load_school_dataframe() function

# 8. Create new template
cp templates/dynamic_map.html templates/schools_map.html

# 9. Test
.\run.ps1
python app.py
# Visit: http://localhost:5000/schools
```

### Workflow 4: Generate Export Report

```bash
# 1. Run quality report generator
python src/processing/generate_quality_report.py \
    --input data/processed/forests.geojson \
    --output outputs/exports/forest_quality_report.txt

# 2. View report
type outputs/exports/forest_quality_report.txt

# 3. Export statistics
python src/processing/get_stats.py \
    --input data/processed/forests.geojson \
    --level novads \
    --output outputs/exports/forest_stats_by_novads.csv

# 4. Open in Excel/LibreOffice
start outputs/exports/forest_stats_by_novads.csv
```

### Workflow 5: Debug Data Quality Issue

**Scenario**: Forest completeness shows 0% in Rīga municipality

```bash
# 1. Check if raw data exists
ls data/raw/Forest.csv
ls data/processed/forests.geojson

# 2. Inspect raw forest count for Rīga
python -c "
import pandas as pd
df = pd.read_csv('data/raw/Forest.csv')
print(df[df['municipality_name'] == 'Rīga'])
"

# 3. Check processed data
python -c "
import geopandas as gpd
import json
gdf = gpd.read_file('data/processed/forests.geojson')
riga_forests = gdf[gdf['municipality_name'] == 'Rīga']
print(f'Count: {len(riga_forests)}')
print(f'Completeness: {riga_forests[\"completeness_pct\"].values}')
"

# 4. Check for spelling issues
python -c "
import geopandas as gpd
gdf = gpd.read_file('data/processed/forests.geojson')
print('Unique municipalities:', gdf['municipality_name'].unique())
"

# 5. If data looks correct, check calculation script
nano scripts/13_calculate_forest_completeness.py
# Verify: (osm_count / official_count) * 100

# 6. Re-run calculation
python scripts/13_calculate_forest_completeness.py

# 7. Verify fix
python -c "
import geopandas as gpd
gdf = gpd.read_file('data/processed/forests.geojson')
print(gdf[gdf['municipality_name'] == 'Rīga'][['municipality_name', 'osm_count', 'official_count', 'completeness_pct']])
"
```

---

## Quick Reference

### File Locations Cheat Sheet

```
Web Application   → app.py
Templates         → templates/*.html
Data Input        → data/raw/
Data Processed    → data/processed/
Scripts           → scripts/*.py
Modules           → src/processing/
Outputs           → outputs/maps/ and outputs/exports/
```

### Most Important Files

| File | Purpose |
|------|---------|
| `app.py` | Flask web server - START HERE |
| `scripts/99_create_comprehensive_geojson.py` | Final output generation |
| `data/processed/forests.geojson` | Forest data for web display |
| `templates/dynamic_map.html` | Interactive map UI |
| `src/processing/generate_corrected_completeness.py` | Core calculation logic |

### Useful Commands

```bash
# View completeness of all forests
python -c "import geopandas; gdf = geopandas.read_file('data/processed/forests.geojson'); print(gdf[['municipality_name', 'completeness_pct']].head(10))"

# Check CRS
python -c "import geopandas; gdf = geopandas.read_file('data/processed/forests.geojson'); print(gdf.crs)"

# Count features
python -c "import geopandas; gdf = geopandas.read_file('data/processed/forests.geojson'); print(f'Total forests: {len(gdf)}')"

# Export to CSV
python -c "import geopandas; gdf = geopandas.read_file('data/processed/forests.geojson'); gdf.to_csv('forests.csv')"

# Find municipality
python -c "import geopandas; gdf = geopandas.read_file('data/processed/forests.geojson'); print(gdf[gdf['municipality_name'].str.contains('Rīga', case=False)][['municipality_name', 'completeness_pct']])"
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError: No module named 'geopandas' | Run `pip install -r requirements.txt` |
| OSM PBF file not found | Download from https://download.geofabrik.de/europe/latvia-latest.osm.pbf |
| Port 5000 already in use | Change in app.py: `app.run(port=5001)` |
| Data not updating in browser | Clear Flask cache or restart app |
| Incomplete geometries | Check CRS transformation (should be EPSG:4326) |

---

## Summary

**LatviaOSM-Check** is a complete geospatial analysis platform that:

1. **Extracts** features (roads, forests, libraries) from OpenStreetMap
2. **Processes** data through a 20-script pipeline
3. **Calculates** completeness percentages by comparing OSM to official records
4. **Visualizes** results on interactive maps
5. **Exposes** data via REST API for external use

**Architecture**: 7 layers (Data Input → UI)  
**Frontend**: HTML + Leaflet.js + Bootstrap 5  
**Backend**: Flask + GeoPandas + Python 3.8+  
**Data**: GeoJSON + CSV + JSON  
**License**: MIT (code) + ODbL (OSM data)  

The project is production-ready and scalable from single-server deployments to Kubernetes clusters.

---

**Last Updated**: January 28, 2026  
**Maintained By**: LatviaOSM-Check Contributors  
**Contact**: See CONTRIBUTING.md
