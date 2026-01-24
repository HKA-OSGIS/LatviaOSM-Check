# Usage Guide

Complete guide for using LatviaOSM-Check to analyze OpenStreetMap data quality in Latvia.

## Table of Contents

- [Getting Started](#getting-started)
- [Web Interface](#web-interface)
- [Data Analysis](#data-analysis)
- [API Usage](#api-usage)
- [Common Tasks](#common-tasks)
- [Advanced Usage](#advanced-usage)

---

## Getting Started

### Starting the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\Activate.ps1  # Windows

# Start the application
python app.py
```

The application will start on `http://localhost:5000`

### First Time Setup

If you haven't processed the data yet:

```powershell
# Windows - Run all pipelines
.\run_forest_pipeline.ps1
.\run_library_pipeline.ps1

# Or run individual scripts
python scripts/02_extract_roads.py
python scripts/11_extract_forests.py
python scripts/21_extract_libraries.py
```

---

## Web Interface

### Main Dashboard

Navigate to `http://localhost:5000` to access the main interface.

#### Features:

1. **Hierarchical Selector**
   - Select by Country → Region → Municipality → Feature Type
   - Multi-level filtering
   - Real-time map updates

2. **Interactive Map**
   - Color-coded municipalities
   - Zoom and pan
   - Click for details
   - Legend showing completeness ranges

3. **Statistics Panel**
   - Total roads (km)
   - Number of segments
   - Average completeness
   - Selected municipality count

### Navigation

#### Roads View
```
http://localhost:5000/roads
```
Shows road completeness analysis.

**What you'll see:**
- Road coverage by municipality
- Comparison with official statistics
- Missing road segments identification

#### Forests View
```
http://localhost:5000/forests
```
Shows forest mapping completeness.

**What you'll see:**
- Forest feature count by municipality
- OSM vs. official forest data
- Forest coverage visualization

#### Libraries View
```
http://localhost:5000/libraries
```
Shows library mapping completeness.

**What you'll see:**
- Library count per municipality
- Completeness percentages
- Gaps in library mapping

#### Combined View
```
http://localhost:5000/combined-map
```
Shows roads, forests, and libraries together on one interactive map with layer toggle.

**What you'll see:**
- **Default View**: Library completeness mapping (start here!)
- **Layer Selector**: Dropdown at top to switch between three layers:
  - 🛣️ Roads completeness
  - 🌲 Forest completeness  
  - 📚 Library completeness (default)
- **Color Coding**: 
  - Green (≥90%) = Excellent
  - Light Green (70-90%) = Good
  - Yellow (50-70%) = Fair
  - Orange (30-50%) = Poor
  - Red (<30%) = Critical
- **Interactive Features**: Click any municipality for detailed statistics

**How to Use:**
1. Open the Combined Map at `/combined-map`
2. Notice Libraries are shown by default
3. Use the dropdown selector at the top to switch to Roads or Forests
4. Click on any municipality boundary to see detailed analysis
5. The legend updates automatically with the selected layer

---

## Data Analysis

### Analyzing Completeness

#### Understanding Completeness Percentages

```
Completeness = (OSM Count / Official Count) × 100%
```

**Interpretation:**
- **> 100%**: OSM has MORE data than official statistics
- **= 100%**: Perfect match
- **< 100%**: OSM has LESS data (mapping gaps exist)
- **90-100%**: Excellent coverage
- **70-90%**: Good coverage
- **50-70%**: Fair coverage  
- **< 50%**: Poor coverage (needs improvement)

#### Color Coding on Maps

| Color | Completeness | Status |
|-------|--------------|--------|
| 🟢 Green | ≥ 90% | Excellent |
| 🟡 Yellow | 70-89% | Good |
| 🟠 Orange | 50-69% | Fair |
| 🔴 Red | < 50% | Poor |

### Identifying Mapping Gaps

#### Using the Web Interface

1. Open the roads/forests/libraries map
2. Look for orange or red municipalities
3. Click on a municipality to see details:
   - OSM count
   - Official count
   - Missing items

#### Using CSV Exports

```python
import pandas as pd

# Load completeness data
df = pd.read_csv('outputs/exports/completeness_municipalities.csv')

# Find municipalities with poor coverage
poor_coverage = df[df['completeness_pct'] < 50]
print(poor_coverage[['municipality_name', 'completeness_pct']].sort_values('completeness_pct'))

# Find municipalities with most missing roads
df['missing_km'] = df['official_road_km'] - df['osm_road_km']
needs_mapping = df.nlargest(10, 'missing_km')
print(needs_mapping[['municipality_name', 'missing_km']])
```

### Comparing Municipalities

#### In the Web Interface

1. Use the hierarchical selector
2. Check multiple municipalities
3. View comparison table
4. Compare statistics

#### Programmatically

```python
import requests
import pandas as pd

# Get data via API
response = requests.get('http://localhost:5000/api/csv-data')
df = pd.DataFrame(response.json())

# Compare specific municipalities
municipalities = ['Rīga', 'Daugavpils', 'Liepāja']
comparison = df[df['municipality_name'].isin(municipalities)]

print(comparison[['municipality_name', 'osm_road_km', 'official_road_km', 'completeness_pct']])
```

---

## API Usage

### Basic API Calls

#### Get All Municipality Data

```bash
curl http://localhost:5000/api/csv-data
```

```python
import requests
data = requests.get('http://localhost:5000/api/csv-data').json()
```

#### Get GeoJSON Data

```bash
curl http://localhost:5000/api/geojson-data > municipalities.geojson
```

```python
import requests
geojson = requests.get('http://localhost:5000/api/geojson-data').json()
```

#### Filter by Municipality

```bash
curl "http://localhost:5000/api/csv-data?municipality=Rīga"
```

### Python Examples

#### Analyze Top/Bottom Performers

```python
import requests
import pandas as pd

# Load data
response = requests.get('http://localhost:5000/api/csv-data')
df = pd.DataFrame(response.json())

# Top 10 by completeness
top10 = df.nlargest(10, 'completeness_pct')
print("Top 10 by completeness:")
print(top10[['municipality_name', 'completeness_pct']])

# Bottom 10 (needs improvement)
bottom10 = df.nsmallest(10, 'completeness_pct')
print("\nBottom 10 (needs improvement):")
print(bottom10[['municipality_name', 'completeness_pct']])
```

#### Generate Custom Report

```python
import requests
import pandas as pd

# Load all datasets
roads = pd.DataFrame(requests.get('http://localhost:5000/api/csv-data').json())
forests = pd.DataFrame(requests.get('http://localhost:5000/api/forest-data').json())
libraries = pd.DataFrame(requests.get('http://localhost:5000/api/library-data').json())

# Merge datasets
merged = roads.merge(forests, on='municipality_name', suffixes=('_roads', '_forests'))
merged = merged.merge(libraries, on='municipality_name')

# Calculate overall score
merged['overall_score'] = (
    merged['completeness_pct_roads'] * 0.5 +
    merged['completeness_pct_forests'] * 0.3 +
    merged['completeness_pct'] * 0.2
)

# Top performers
top_overall = merged.nlargest(10, 'overall_score')
print(top_overall[['municipality_name', 'overall_score']])

# Save report
merged.to_csv('custom_completeness_report.csv', index=False)
```

### JavaScript Examples

#### Display Data in Web Page

```html
<!DOCTYPE html>
<html>
<head>
    <title>Municipality Comparison</title>
</head>
<body>
    <h1>Municipality OSM Completeness</h1>
    <table id="data-table">
        <thead>
            <tr>
                <th>Municipality</th>
                <th>OSM Roads (km)</th>
                <th>Official Roads (km)</th>
                <th>Completeness (%)</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        fetch('http://localhost:5000/api/csv-data')
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('#data-table tbody');
                
                data.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${row.municipality_name}</td>
                        <td>${row.osm_road_km.toFixed(2)}</td>
                        <td>${row.official_road_km.toFixed(2)}</td>
                        <td>${row.completeness_pct.toFixed(1)}%</td>
                    `;
                    tbody.appendChild(tr);
                });
            });
    </script>
</body>
</html>
```

---

## Common Tasks

### Task 1: Find Areas Needing Mapping

**Goal:** Identify municipalities with poor OSM coverage.

```python
import pandas as pd

# Load data
df = pd.read_csv('outputs/exports/completeness_municipalities.csv')

# Filter for poor coverage
needs_work = df[df['completeness_pct'] < 70].sort_values('completeness_pct')

# Display results
print("Municipalities needing mapping work:")
for idx, row in needs_work.iterrows():
    print(f"- {row['municipality_name']}: {row['completeness_pct']:.1f}%")
    print(f"  Missing: {row['official_road_km'] - row['osm_road_km']:.1f} km of roads")
```

### Task 2: Export Data for JOSM

**Goal:** Create files for editing in JOSM.

```python
import geopandas as gpd

# Load municipality of interest
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
municipality = gdf[gdf['municipality_name'] == 'Rīga']

# Save for JOSM
municipality.to_file('riga_for_josm.geojson', driver='GeoJSON')
print("Saved to riga_for_josm.geojson")
print("Open in JOSM to start mapping!")
```

### Task 3: Generate Monthly Report

**Goal:** Create a progress report comparing this month vs. last month.

```python
import pandas as pd
from datetime import datetime

# Load current data
current = pd.read_csv('outputs/exports/completeness_municipalities.csv')
current['date'] = datetime.now().strftime('%Y-%m')

# Load previous month (if exists)
try:
    previous = pd.read_csv('reports/2024-12-completeness.csv')
    
    # Calculate improvements
    comparison = current.merge(previous, on='municipality_name', suffixes=('_current', '_previous'))
    comparison['improvement'] = comparison['completeness_pct_current'] - comparison['completeness_pct_previous']
    
    # Top improvers
    top_improvers = comparison.nlargest(10, 'improvement')
    print("Top 10 most improved municipalities:")
    print(top_improvers[['municipality_name', 'improvement']])
    
except FileNotFoundError:
    print("No previous month data available")

# Save current month report
current.to_csv(f'reports/{datetime.now().strftime("%Y-%m")}-completeness.csv', index=False)
```

### Task 4: Create Custom Map

**Goal:** Create a custom map showing specific municipalities.

```python
import folium
import geopandas as gpd

# Load data
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')

# Select municipalities of interest
municipalities = ['Rīga', 'Daugavpils', 'Liepāja', 'Jelgava']
selected = gdf[gdf['municipality_name'].isin(municipalities)]

# Create map
m = folium.Map(location=[56.9496, 24.1052], zoom_start=7)

# Add municipalities
for idx, row in selected.iterrows():
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x: {'fillColor': 'blue', 'color': 'black', 'weight': 2},
        tooltip=f"{row['municipality_name']}: {row['completeness_pct']:.1f}%"
    ).add_to(m)

# Save
m.save('custom_map.html')
print("Saved to custom_map.html")
```

---

## Advanced Usage

### Custom Analysis Scripts

#### Calculate Regional Statistics

```python
import pandas as pd
import geopandas as gpd

# Load data
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')

# Define regions (simplified)
regions = {
    'Rīga Region': ['Rīga', 'Jūrmala', 'Ādažu novads', 'Ķekavas novads', 'Mārupes novads'],
    'Kurzeme': ['Liepāja', 'Ventspils', 'Kuldīgas novads', 'Talsu novads'],
    'Vidzeme': ['Valmieras novads', 'Cēsu novads', 'Siguldas novads'],
    'Zemgale': ['Jelgava', 'Jelgavas novads', 'Bauskas novads'],
    'Latgale': ['Daugavpils', 'Rēzekne', 'Preiļu novads', 'Ludzas novads']
}

# Calculate regional stats
regional_stats = []
for region, municipalities in regions.items():
    region_data = gdf[gdf['municipality_name'].isin(municipalities)]
    
    stats = {
        'region': region,
        'municipalities': len(region_data),
        'total_osm_roads': region_data['osm_road_km'].sum(),
        'total_official_roads': region_data['official_road_km'].sum(),
        'avg_completeness': region_data['completeness_pct'].mean()
    }
    regional_stats.append(stats)

regional_df = pd.DataFrame(regional_stats)
print(regional_df)

# Save
regional_df.to_csv('regional_statistics.csv', index=False)
```

#### Time Series Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load historical data (if you've been saving monthly reports)
months = ['2024-09', '2024-10', '2024-11', '2024-12', '2025-01']
historical_data = []

for month in months:
    try:
        df = pd.read_csv(f'reports/{month}-completeness.csv')
        df['month'] = month
        historical_data.append(df)
    except FileNotFoundError:
        continue

if historical_data:
    combined = pd.concat(historical_data)
    
    # Plot trends for top municipalities
    top_munis = ['Rīga', 'Daugavpils', 'Liepāja', 'Jelgava']
    
    plt.figure(figsize=(12, 6))
    for muni in top_munis:
        muni_data = combined[combined['municipality_name'] == muni]
        plt.plot(muni_data['month'], muni_data['completeness_pct'], marker='o', label=muni)
    
    plt.xlabel('Month')
    plt.ylabel('Completeness (%)')
    plt.title('OSM Completeness Trends')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('completeness_trends.png')
    print("Saved to completeness_trends.png")
```

### Integration with Other Tools

#### Export for QGIS

```python
import geopandas as gpd

# Load data
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')

# Save in multiple formats for QGIS
gdf.to_file('outputs/exports/latvia_municipalities.shp')  # Shapefile
gdf.to_file('outputs/exports/latvia_municipalities.gpkg', driver='GPKG')  # GeoPackage
gdf.to_file('outputs/exports/latvia_municipalities.kml', driver='KML')  # KML

print("Exported in multiple formats for QGIS")
```

#### Generate Overpass Query

```python
def generate_overpass_query(municipality_name, bbox):
    """Generate Overpass query for a municipality."""
    query = f"""
    [out:json][timeout:25];
    (
      way["highway"]({bbox});
      way["natural"="forest"]({bbox});
      node["amenity"="library"]({bbox});
    );
    out geom;
    """
    return query

# Get bbox for a municipality
import geopandas as gpd
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
riga = gdf[gdf['municipality_name'] == 'Rīga'].iloc[0]

bbox = riga.geometry.bounds  # (minx, miny, maxx, maxy)
bbox_str = f"{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}"

query = generate_overpass_query('Rīga', bbox_str)
print(query)

# Save to file
with open('overpass_riga.txt', 'w') as f:
    f.write(query)
```

---

## Troubleshooting

### No Data Showing on Map

**Problem:** Map loads but shows no data.

**Solution:**
1. Check that pipeline has been run:
   ```bash
   ls outputs/exports/
   ```
2. Verify files exist:
   - `latvia_lau1.geojson`
   - `completeness_municipalities.csv`
3. Re-run pipeline if needed:
   ```bash
   python scripts/07_create_interactive_map.py
   ```

### API Returns Empty Response

**Problem:** API endpoint returns `[]` or empty data.

**Solution:**
1. Check file paths in `app.py`
2. Verify CSV files are not corrupted:
   ```python
   import pandas as pd
   df = pd.read_csv('outputs/exports/completeness_municipalities.csv')
   print(len(df))
   ```
3. Restart Flask application

### Completeness > 100%

**Problem:** Completeness shows over 100%.

**Explanation:** This is normal! It means OSM has MORE data than official statistics. This can happen because:
- OSM is more up-to-date
- OSM includes different road classifications
- Volunteers have mapped additional features

**Interpretation:** This is actually good news - it means OSM coverage is excellent!

---

## Next Steps

- **Contribute to OSM**: Use the identified gaps to improve mapping
- **Share Reports**: Export data and share with OSM community
- **Monitor Progress**: Set up monthly reporting
- **Customize**: Extend the tool for your specific needs

For more information:
- [API Documentation](API.md)
- [Development Guide](DEVELOPMENT.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
