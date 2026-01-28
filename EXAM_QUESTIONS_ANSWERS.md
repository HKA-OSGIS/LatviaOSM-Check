# LatviaOSM-Check - Exam Questions & Answers

**Created**: January 28, 2026  
**Purpose**: Comprehensive exam preparation for LatviaOSM-Check project

---

## Section 1: Project Overview & Purpose

### Q1: What is the primary purpose of LatviaOSM-Check?
**Answer:**
LatviaOSM-Check is an OpenStreetMap data quality analysis tool that:
- Compares OSM data against official government statistics for Latvia
- Analyzes completeness of 3 feature types: Roads, Forests, and Libraries
- Visualizes data quality using interactive web maps
- Provides RESTful API for programmatic data access
- Generates completeness metrics showing how comprehensive OSM coverage is compared to official data

**Key Formula**: Completeness % = (OSM Count / Official Count) × 100

---

### Q2: Which three geographic features are analyzed in LatviaOSM-Check?
**Answer:**
1. **Roads** - Road networks and transport infrastructure
2. **Forests** - Forest coverage and boundaries
3. **Libraries** - Public library locations and distribution

Each has its own:
- Extraction script
- Spatial join operations
- Completeness calculation
- Interactive map visualization
- API endpoints

---

### Q3: What is the current data coverage status?
**Answer:**
- **Total Features Analyzed**: 42 (36 municipalities + 6 cities)
- **Features with Complete Data**: 39
- **Completeness Rating**: 100% for available data
- **Average OSM Completeness**: 249.6% (very comprehensive)
- **Municipalities with Data**: 36/36 (100%)
- **Best Mapped Area**: Olaine (645.6% completeness)
- **Data Update**: January 2026

---

## Section 2: Architecture & Design

### Q4: Describe the layered architecture of LatviaOSM-Check
**Answer:**

**7-Layer Architecture:**

1. **Data Input Layer** - Raw OSM PBF files, official statistics CSV, boundary GeoJSON
2. **Processing Pipeline** - Numbered scripts (00-99) for sequential data transformation
3. **Processing Modules** - Reusable Python modules for fuzzy matching, spatial joins, calculations
4. **Data Output** - Processed GeoJSON, CSV exports, quality reports
5. **Web Application** - Flask app with routes, API endpoints, data caching
6. **Frontend** - Leaflet.js interactive maps, HTML/CSS UI
7. **External Libraries** - GeoPandas, Flask, Shapely, FuzzyWuzzy

**Data Flow**: Raw Data → Extraction → Processing → Calculation → Output → Web App → Browser Display

---

### Q5: What design patterns are used in the project?
**Answer:**

| Pattern | Purpose | Location |
|---------|---------|----------|
| **Pipeline** | Sequential data processing | scripts/ (00-99 numbered) |
| **Module** | Reusable processing logic | src/processing/ |
| **Caching** | Performance optimization | app.py in-memory cache |
| **Facade** | Simplified API interface | Flask routes |
| **MVC** | Web framework separation | Flask structure |
| **Repository** | Data abstraction | File-based storage |

---

### Q6: How is data caching implemented in the Flask application?
**Answer:**

```python
# Global cache variables
_geojson_cache = None
_dataframe_cache = None
_forest_dataframe_cache = None
_library_dataframe_cache = None

# Loading with cache check
def load_geojson():
    global _geojson_cache
    if _geojson_cache is None:
        # Load from disk only once
        with open(GEOJSON_FILE) as f:
            _geojson_cache = json.load(f)
    return _geojson_cache

# Cache clearing
def clear_cache():
    global _geojson_cache, _dataframe_cache, ...
    _geojson_cache = None
    _dataframe_cache = None
    ...
```

**Benefits:**
- Reduces disk I/O
- Faster API response times
- Improved performance for concurrent requests
- Data consistency throughout session

---

## Section 3: Data Processing Pipeline

### Q7: Explain the sequential steps in the data processing pipeline
**Answer:**

**Pipeline Workflow (Scripts 00-99):**

| Step | Script | Input | Output | Purpose |
|------|--------|-------|--------|---------|
| 0 | 00_convert_official_stats.py | CSV files | Standardized format | Normalize official data |
| 1 | 02_extract_roads.py | OSM PBF | roads.geojson | Extract road networks |
| 2 | 11_extract_forests.py | OSM PBF | forests.geojson | Extract forest areas |
| 3 | 21_extract_libraries.py | OSM PBF | libraries.geojson | Extract library points |
| 4 | 03_process_municipalities.py | GeoJSON | Processed boundaries | Validate & standardize CRS |
| 5 | 04_spatial_join.py | Features + boundaries | Features by municipality | Assign features to regions |
| 6 | 05_calculate_completeness.py | Joined + official | Completeness metrics | Calculate % coverage |
| 7 | 07-27_create_maps.py | Results + data | HTML maps | Generate visualizations |
| 8 | 99_create_comprehensive_geojson.py | All data | Final exports | Merge into final format |

**Key Operations:**
1. Extract features from OSM
2. Process boundaries
3. Perform spatial joins
4. Match names (fuzzy matching)
5. Calculate completeness metrics
6. Generate visualizations

---

### Q8: What is fuzzy matching and why is it used?
**Answer:**

**Definition**: Fuzzy matching finds similar strings even with spelling variations, capitalization differences, or slight misspellings.

**Why Used in LatviaOSM-Check:**
- OSM names differ from official statistics
- Latvian language supports multiple cases (nominative, genitive)
- Handles variations like "Riga" vs "Rīga"
- Matches despite spacing/punctuation differences

**Example:**
```
OSM Name          → Official Name      → Match Score
"Riga"            → "Rīga"             → 95%
"Daugavpils nova" → "Daugavpils novads" → 89%
"Jelgava city"    → "Jelgava"          → 82%
```

**Threshold**: 80% minimum match score required

**Implementation**: FuzzyWuzzy library with token_set_ratio algorithm

**Location**: `src/processing/create_fuzzy_mapping.py`

---

### Q9: Describe the spatial join operation in the pipeline
**Answer:**

**Purpose**: Assigns geographic features (roads, forests, libraries) to municipalities

**Process:**
```
Input:
  roads.geojson (point/line geometries)
  + municipalities.geojson (polygon geometries)

Operation:
  gpd.sjoin(roads, municipalities, 
            how='left', predicate='within')

Output:
  roads_by_municipality.geojson
  (each road has municipality_name attribute)
```

**Predicate Types:**
- `'within'` - Feature completely inside municipality
- `'intersects'` - Feature overlaps municipality boundary
- `'contains'` - Municipality contains feature

**Result:**
- Every road, forest, or library linked to a municipality
- Enables aggregation and statistics by region

---

## Section 4: Technical Concepts

### Q10: What is a Completeness Percentage and how is it calculated?
**Answer:**

**Formula:**
```
Completeness % = (OSM Data Count / Official Count) × 100
```

**Interpretation:**
- **> 100%** = OSM has MORE data than official statistics (over-mapped)
- **= 100%** = Perfect match
- **< 100%** = OSM has LESS data (under-mapped, needs improvement)
- **0-50%** = Critical gaps in mapping
- **50-70%** = Fair coverage
- **70-100%** = Good to excellent coverage

**Example:**
```
Official roads: 1,000 km
OSM roads: 2,496 km
Completeness: (2,496 / 1,000) × 100 = 249.6%
```

This means OSM has 2.5× more road data than official statistics.

---

### Q11: What is CRS (Coordinate Reference System) and why is it important?
**Answer:**

**Definition**: CRS defines how geographic coordinates (lat/lon) map to real-world locations

**Common CRS Values:**
- **EPSG:4326** = WGS84 (latitude/longitude, worldwide standard)
- **EPSG:3857** = Web Mercator (used in web maps like Google/OSM)
- **LKS92** = Latvian national grid

**Why Important in LatviaOSM-Check:**
1. All data must use same CRS for spatial operations
2. Different sources use different CRS
3. Mismatch causes errors in spatial joins
4. Standard practice: convert everything to EPSG:4326

**In Code:**
```python
roads = roads.to_crs('EPSG:4326')
municipalities = municipalities.to_crs('EPSG:4326')
# Now safe to perform spatial join
```

---

### Q12: What is a GeoJSON file and what does it contain?
**Answer:**

**Definition**: GeoJSON is a text format for encoding geographic data structures and their non-spatial attributes

**Structure:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lng, lat], ...]]
      },
      "properties": {
        "municipality_name": "Rīga",
        "osm_road_km": 1234.56,
        "official_road_km": 1100,
        "completeness_pct": 112.2
      }
    }
  ]
}
```

**In LatviaOSM-Check:**
- **latvia_lau1.geojson** - Municipal boundaries + completeness data
- **roads_by_municipality.geojson** - Road features with municipal assignments
- **forests.geojson** - Forest boundaries
- **libraries.geojson** - Library point locations

**Advantages:**
- Human-readable text format
- Web-friendly (used by Leaflet.js)
- Preserves both geometry and attributes
- Easy to export/share

---

## Section 5: Web Application & API

### Q13: List all API endpoints and their purposes
**Answer:**

| Endpoint | Method | Returns | Purpose |
|----------|--------|---------|---------|
| `/` | GET | HTML | Main interactive map |
| `/roads` | GET | HTML | Roads completeness map |
| `/forests` | GET | HTML | Forests completeness map |
| `/libraries` | GET | HTML | Libraries completeness map |
| `/combined-map` | GET | HTML | Multi-layer map (roads, forests, libraries) |
| `/api/geojson-data` | GET | GeoJSON | All features with boundaries |
| `/api/csv-data` | GET | JSON | Municipality statistics |
| `/api/forest-data` | GET | JSON | Forest statistics |
| `/api/library-data` | GET | JSON | Library statistics |

**Authentication**: None (public endpoints)

**Response Format**: 
- Maps return HTML
- API endpoints return JSON
- All responses include proper headers

---

### Q14: How would you call the API to get all municipality data in Python?
**Answer:**

```python
import requests
import pandas as pd

# Method 1: Get as JSON
response = requests.get('http://localhost:5000/api/csv-data')
data = response.json()
df = pd.DataFrame(data)

# Method 2: Get as GeoJSON
response = requests.get('http://localhost:5000/api/geojson-data')
geojson = response.json()

# Method 3: Get forest data
response = requests.get('http://localhost:5000/api/forest-data')
forest_stats = response.json()

# Example: Find municipalities with poor coverage
poor_coverage = df[df['completeness_pct'] < 70]
print(poor_coverage[['municipality_name', 'completeness_pct']])
```

**Error Handling:**
```python
try:
    response = requests.get('http://localhost:5000/api/csv-data')
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"API error: {e}")
```

---

### Q15: How would you call the API in JavaScript to fetch and display data?
**Answer:**

```javascript
// Fetch municipality data
fetch('http://localhost:5000/api/csv-data')
  .then(response => response.json())
  .then(data => {
    // Display data in table
    const table = document.querySelector('#data-table tbody');
    data.forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${row.municipality_name}</td>
        <td>${row.osm_road_km.toFixed(2)}</td>
        <td>${row.official_road_km.toFixed(2)}</td>
        <td>${row.completeness_pct.toFixed(1)}%</td>
      `;
      table.appendChild(tr);
    });
  })
  .catch(error => console.error('Error:', error));

// Fetch GeoJSON for map
fetch('http://localhost:5000/api/geojson-data')
  .then(res => res.json())
  .then(geojson => {
    // Add to Leaflet map
    L.geoJSON(geojson, {
      onEachFeature: function(feature, layer) {
        layer.bindPopup(`<b>${feature.properties.municipality_name}</b><br>
                        Completeness: ${feature.properties.completeness_pct}%`);
      }
    }).addTo(map);
  });
```

---

## Section 6: Installation & Deployment

### Q16: What are the system requirements for running LatviaOSM-Check?
**Answer:**

**Minimum Requirements:**
- Python 3.8 or higher
- RAM: 4 GB minimum
- Disk Space: 2 GB free
- OS: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)

**Recommended:**
- Python 3.11+
- RAM: 16 GB
- Disk Space: 5 GB
- CPU: Multi-core processor

**Additional Software:**
- Git (for version control)
- GDAL/OGR (for geospatial operations)
- Virtual environment (Python venv)

---

### Q17: Describe the installation process
**Answer:**

**Method 1: Automated (Recommended)**

Windows:
```powershell
.\setup.ps1
.\run.ps1
```

Linux/macOS:
```bash
./setup.sh
./run.sh
```

**Method 2: Manual Installation**

```bash
# Clone repository
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

**Access**: http://localhost:5000

---

### Q18: What dependencies are required and what does each do?
**Answer:**

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework for API & routes |
| GeoPandas | 0.13.2 | Geospatial data operations |
| Pandas | 2.0.3 | Data manipulation & analysis |
| Shapely | 2.0.1 | Geometric operations |
| Fiona | 1.9.4 | GeoJSON/Shapefile I/O |
| PyOGRIO | 0.7.2 | GDAL wrapper for data formats |
| Folium | 0.14.0 | Interactive map generation |
| Requests | 2.31.0 | HTTP client for API calls |
| FuzzyWuzzy | - | String matching (for names) |

**Install All:**
```bash
pip install -r requirements.txt
```

---

### Q19: How would you deploy LatviaOSM-Check to production?
**Answer:**

**Development Server** (Not for production):
```bash
python app.py
# Single process, debug mode enabled, not scalable
```

**Production Deployment Options:**

**Option 1: Gunicorn (Linux/macOS)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
# Runs 4 worker processes
```

**Option 2: Waitress (Windows)**
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

**Option 3: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t latvia-osm-check .
docker run -p 5000:5000 latvia-osm-check
```

**With Reverse Proxy (Nginx):**
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://localhost:5000;
    }
}
```

---

## Section 7: Features & Functionality

### Q20: What is the Multi-Select Comparison Tool?
**Answer:**

**Purpose**: Compare multiple municipalities simultaneously

**Features:**
- Checkboxes for each municipality
- "Select All" / "Clear All" buttons
- Real-time statistics update
- Interactive map highlighting
- Comparison table display

**Statistics Displayed:**
```
Selected: 589 (number checked)
Total Roads (OSM): 12,345.67 km
Total Segments: 98,765
Avg Completeness: 42.3%
```

**Use Cases:**
1. Compare neighboring municipalities
2. Analyze regional patterns
3. Identify top/bottom performers
4. Track improvements over time

---

### Q21: Describe the interactive map features
**Answer:**

**Main Map Features:**
- **Base Layer**: OpenStreetMap tiles
- **Features**: Municipality boundaries colored by completeness
- **Color Coding**:
  - 🟢 Green (≥90%) = Excellent
  - 🟡 Yellow (70-89%) = Good
  - 🟠 Orange (50-69%) = Fair
  - 🔴 Red (<50%) = Poor

**Interactions:**
- **Click**: Show municipality statistics in popup
  ```
  Municipality Name
  OSM Roads: 1,234.56 km
  Official Roads: 1,100 km
  Completeness: 112.2%
  ```
- **Zoom**: Navigate to detail level
- **Pan**: Move across map
- **Legend**: Shows completeness ranges

**Layer Toggle** (Combined Map):
- Switch between Roads/Forests/Libraries views
- Dynamic legend updates per layer

---

### Q22: What data analyses can be performed using LatviaOSM-Check?
**Answer:**

**Built-in Analyses:**

1. **Completeness Analysis**
   - Compare OSM vs official data
   - Calculate coverage percentages
   - Identify mapping gaps

2. **Geographic Analysis**
   - Regional comparisons
   - Municipality rankings
   - Spatial patterns

3. **Statistical Analysis**
   - Aggregates by region
   - Summary statistics
   - Distribution analysis

4. **Quality Assessment**
   - Data consistency checks
   - Error detection
   - Quality metrics

**Custom Analyses (Using API):**

```python
import pandas as pd
import requests

# Get all data
df = pd.DataFrame(requests.get('http://localhost:5000/api/csv-data').json())

# Find areas needing mapping
needs_work = df[df['completeness_pct'] < 70].sort_values('completeness_pct')

# Calculate total missing
total_missing = (df['official_road_km'] - df['osm_road_km']).sum()

# Find top performers
top_10 = df.nlargest(10, 'completeness_pct')
```

---

## Section 8: Development & Contribution

### Q23: What is the code structure and naming conventions?
**Answer:**

**Directory Structure:**
```
src/
├── __init__.py
└── processing/           # Data processing modules
    ├── create_fuzzy_mapping.py
    ├── generate_corrected_completeness.py
    ├── generate_quality_report.py
    └── get_stats.py

scripts/                  # Pipeline scripts
├── 00_convert_official_stats.py  # Data prep
├── 02_extract_roads.py           # Feature extraction
├── 04_spatial_join.py            # Spatial operations
├── 05_calculate_completeness.py  # Calculations
└── 99_create_comprehensive_geojson.py  # Final output

templates/               # Flask templates
├── dynamic_map.html
└── with_dropdown.html

data/
├── raw/                # Original data (not in git)
└── processed/          # Cleaned data

outputs/
├── exports/            # CSV, GeoJSON exports
└── maps/               # HTML interactive maps
```

**Naming Conventions:**

**Scripts**: `NN_descriptive_name.py`
- 00-09: Data preparation
- 10-19: Feature extraction
- 20-29: Spatial analysis
- 30-39: Future features
- 90-99: Utilities

**Functions**: `snake_case`
```python
def calculate_completeness(osm_data, official_data):
    pass
```

**Classes**: `PascalCase`
```python
class DataProcessor:
    pass
```

**Variables**: `snake_case`
```python
municipality_name = "Rīga"
```

---

### Q24: How should you contribute to the project?
**Answer:**

**Contribution Steps:**

1. **Setup Development Environment**
   ```bash
   git clone <repo>
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Code & Test**
   - Follow code style guidelines
   - Write/update tests
   - Test locally

4. **Commit Changes**
   ```bash
   git commit -m "Add feature description"
   ```

5. **Push & Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Create Pull Request on GitHub
   - Describe changes clearly
   - Link related issues

6. **Code Review**
   - Address review comments
   - Update as needed
   - Approval required before merge

**Guidelines:**
- Follow [Contributing.md](../CONTRIBUTING.md)
- Respect [Code of Conduct](../CODE_OF_CONDUCT.md)
- Write clear commit messages
- Keep PRs focused and manageable

---

### Q25: What are the code style guidelines?
**Answer:**

**Python Style (PEP 8):**

```python
# Line length: max 100 characters
# Indentation: 4 spaces
# Quotes: double quotes for strings

# Function documentation (Google style)
def calculate_completeness(
    osm_data: pd.DataFrame,
    official_data: pd.DataFrame
) -> pd.DataFrame:
    """Calculate OSM completeness by comparing with official data.
    
    Args:
        osm_data: OSM road data with geometry
        official_data: Official statistics data
        
    Returns:
        DataFrame with completeness metrics
        
    Raises:
        ValueError: If data is missing required columns
    """
    if osm_data.empty:
        raise ValueError("OSM data cannot be empty")
    return result

# Type hints required
from typing import List, Dict, Optional

def process_municipalities(
    names: List[str],
    threshold: float = 0.8
) -> Dict[str, float]:
    """Process municipality names."""
    pass

# Import order: stdlib, 3rd-party, local
import os
import sys
import pandas as pd
import geopandas as gpd
from src.processing import create_fuzzy_mapping
```

---

## Section 9: Geospatial Operations

### Q26: Explain the Spatial Join operation in detail
**Answer:**

**Purpose**: Associate point/line features with polygon boundaries

**Example: Roads → Municipalities**

```python
import geopandas as gpd

# Load data
roads = gpd.read_file('roads.geojson')
municipalities = gpd.read_file('municipalities.geojson')

# Ensure same CRS
roads = roads.to_crs('EPSG:4326')
municipalities = municipalities.to_crs('EPSG:4326')

# Spatial join
result = gpd.sjoin(
    roads,                      # Left GeoDataFrame
    municipalities,             # Right GeoDataFrame
    how='left',                # Keep all roads
    predicate='within'         # Road within municipality
)

# Result columns:
# - All columns from roads
# - All columns from municipalities
# - 'index_right': municipality index that contains road
```

**Predicates:**
- `'intersects'` - Any overlap
- `'within'` - Completely inside
- `'contains'` - Polygon contains feature
- `'crosses'` - Features cross

**Result Interpretation:**
```
Each road now has municipality_name attribute
↓
Enables aggregation: "Sum all roads in Rīga"
```

---

### Q27: What is Geometry Validation and why is it needed?
**Answer:**

**Common Geometry Problems:**
- Self-intersecting polygons
- Holes in boundaries
- Invalid rings
- Duplicate coordinates
- Topology errors

**Validation & Fixing:**

```python
import geopandas as gpd
from shapely.geometry import shape

# Load data
gdf = gpd.read_file('municipalities.geojson')

# Check validity
print(gdf.is_valid)  # Returns boolean array

# Fix invalid geometries
gdf['geometry'] = gdf['geometry'].buffer(0)

# Remove invalid geometries
valid_gdf = gdf[gdf.is_valid]

# Validate before spatial operations
assert gdf.is_valid.all(), "Invalid geometries found"
```

**Why Important:**
- Spatial joins fail on invalid geometries
- Can cause silent errors or wrong results
- Affects map visualization
- Essential preprocessing step

---

## Section 10: Real-World Scenarios

### Q28: How would you identify municipalities most in need of mapping improvement?
**Answer:**

**Step-by-Step Analysis:**

```python
import requests
import pandas as pd

# 1. Fetch data
response = requests.get('http://localhost:5000/api/csv-data')
df = pd.DataFrame(response.json())

# 2. Filter for low coverage
needs_improvement = df[df['completeness_pct'] < 70]

# 3. Calculate missing roads
needs_improvement['missing_km'] = (
    needs_improvement['official_road_km'] - 
    needs_improvement['osm_road_km']
)

# 4. Sort by most missing
priority = needs_improvement.sort_values(
    'missing_km', 
    ascending=False
)

# 5. Display results
print(priority[[
    'municipality_name',
    'completeness_pct',
    'missing_km'
]].head(10))
```

**Output Example:**
```
Municipality          Completeness  Missing (km)
─────────────────────────────────────────────────
Varakļāni                 45.2%        500.0
Preili                    52.1%        450.0
Ludza                     61.3%        350.0
```

**Next Steps:**
- Organize mapping events
- Contact OSM community
- Create import tasks
- Track improvements

---

### Q29: How would you create a custom regional analysis?
**Answer:**

**Example: Compare 3 regions**

```python
import pandas as pd
import requests

# Load data
df = pd.DataFrame(requests.get('http://localhost:5000/api/csv-data').json())

# Define regions
regions = {
    'Rīga Region': ['Rīga', 'Jūrmala', 'Ādažu novads', 'Ķekavas novads'],
    'Kurzeme': ['Liepāja', 'Ventspils', 'Kuldīgas novads'],
    'Latgale': ['Daugavpils', 'Rēzekne', 'Preiļu novads']
}

# Calculate regional stats
regional_stats = []
for region_name, municipalities in regions.items():
    region_data = df[df['municipality_name'].isin(municipalities)]
    
    stats = {
        'region': region_name,
        'municipalities': len(region_data),
        'total_osm_roads': region_data['osm_road_km'].sum(),
        'total_official_roads': region_data['official_road_km'].sum(),
        'avg_completeness': region_data['completeness_pct'].mean(),
        'min_completeness': region_data['completeness_pct'].min(),
        'max_completeness': region_data['completeness_pct'].max()
    }
    regional_stats.append(stats)

# Convert to DataFrame
regional_df = pd.DataFrame(regional_stats)

# Display
print(regional_df.to_string())

# Save
regional_df.to_csv('regional_analysis.csv', index=False)
```

---

### Q30: How would you integrate LatviaOSM-Check data with QGIS?
**Answer:**

**Method 1: Direct GeoJSON Import**

```
1. Open QGIS
2. Layer → Add Layer → Add Vector Layer
3. Source: outputs/exports/latvia_lau1.geojson
4. Click "Add"
5. Features now visible with all attributes
6. Right-click → Properties to style by completeness
```

**Method 2: Export for QGIS**

```python
import geopandas as gpd

# Load GeoJSON
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')

# Export in multiple formats
gdf.to_file('latvia.shp')      # Shapefile
gdf.to_file('latvia.gpkg',     # GeoPackage
            driver='GPKG')
gdf.to_file('latvia.kml',      # KML
            driver='KML')

# Use in QGIS: Layer → Add Layer → select file
```

**Method 3: API + Python QGIS Script**

```python
# In QGIS Python console
import requests
import geopandas as gpd
from io import StringIO

# Fetch data via API
response = requests.get('http://localhost:5000/api/geojson-data')
gdf = gpd.GeoDataFrame.from_features(response.json()['features'])

# Add to QGIS
layer = iface.addVectorLayer(
    "?crs=EPSG:4326&" + gdf.to_json(),
    "OSM Completeness", 
    "ogr"
)
```

**Styling in QGIS:**
1. Right-click layer → Properties
2. Symbology tab
3. Graduated colors by 'completeness_pct'
4. Color ramp: Green (high) to Red (low)
5. Apply

---

## Summary Table: Key Concepts

| Concept | Definition | Location |
|---------|-----------|----------|
| Completeness % | (OSM / Official) × 100 | Calculation module |
| Spatial Join | Link features to boundaries | scripts/04 |
| Fuzzy Match | String matching with tolerance | src/processing/ |
| CRS | Coordinate Reference System | Data processing |
| GeoJSON | Geographic data format | outputs/exports/ |
| Pipeline | Sequential data transformation | scripts/ (00-99) |
| API | RESTful endpoints | app.py |
| Cache | In-memory data storage | Flask app |
| Predicate | Geometric relationship type | GeoPandas sjoin |

---

## Answer Key Statistics

- **Total Questions**: 30
- **Difficulty Levels**:
  - Easy (Conceptual): Q1-Q5, Q20-Q22
  - Medium (Application): Q6-Q15, Q23-Q25
  - Hard (Analysis): Q16-Q19, Q26-Q30
- **Coverage Areas**: 10 sections
- **Project Understanding**: Comprehensive

---

**Good luck on your exam!**

*For more information, see [docs/README.md](../docs/README.md)*
