# EXTENDING.md - How to Add New Data Sources to Latvia OSM Project

## Overview

This project analyzes OpenStreetMap completeness by comparing it with official statistics. Currently, it focuses on road networks, but the architecture is designed to support multiple topics (railways, hospitals, buildings, forests, etc.).

This guide explains how to add new data sources and topics to the project.

---

## Project Architecture

### Data Pipeline

```
data/raw/ (Input)
    ├─ Official statistics (CSV)
    ├─ Municipality boundaries (GeoJSON)
    └─ OSM data (PBF)
           ↓
scripts/ (Processing)
    ├─ 00_convert_* → Normalize official data
    ├─ 01_download_* → Get OSM/boundaries
    ├─ 02_extract_* → Extract OSM features
    ├─ 03_process_* → Process boundaries
    ├─ 04_spatial_join.py → Combine data
    └─ 05_calculate_* → Calculate completeness
           ↓
data/processed/ (Output)
    ├─ topic_data.geojson
    └─ topic_stats.csv
           ↓
outputs/exports/ (Final)
    ├─ completeness_map.geojson
    └─ completeness.csv
           ↓
app.py (Web Interface)
    └─ User selects topic → Map displays data
```

### Key Files

- **`app.py`** - Flask web application, API endpoints, metrics configuration
- **`scripts/`** - Data processing pipeline (numbered 00-09)
- **`data/raw/`** - Raw input data
- **`data/processed/`** - Processed intermediate data
- **`outputs/exports/`** - Final analysis results
- **`templates/`** - HTML templates for web interface

---

## Step-by-Step: Adding a New Topic

### Example: Adding Railway Completeness Analysis

Let's walk through adding railways as a new topic.

---

## Step 1: Prepare Your Official Statistics Data

### 1.1 Find and Download Data

**Where to find:**
- Central Statistical Bureau of Latvia: https://www.csb.gov.lv/
- For other countries, find equivalent national statistics offices
- Look for official data on:
  - Total kilometers of railways/bridges/etc.
  - Data by municipality or administrative division
  - Recent data (ideally current year)

**For railways in Latvia:** Some options:
- Rail company data (LDZ - Latvijas Dzelzceļš)
- CSB reports on transport infrastructure
- OpenData portals

### 1.2 Format Your Data

Save as: `data/raw/railways_statistics.csv`

Required columns:
- `municipality_name` - Must match municipalities in `data/raw/municipalities.geojson`
- `metric_value` - Your statistic (kilometers, count, area, etc.)
- Any additional columns you want to preserve

**Example for railways:**
```csv
municipality_name,railway_km,bridges_count
Rīga,47.2,12
Jūrmala,8.5,3
Ventspils,24.1,5
Salaspils,6.3,1
...
```

### 1.3 Verify Municipality Name Matching

**Critical:** Municipality names must exactly match the names in municipality boundaries GeoJSON.

**To find valid names:**
```python
import geopandas as gpd
gdf = gpd.read_file('data/raw/municipalities.geojson')
print(gdf['municipality_name'].unique())
```

---

## Step 2: Create a Data Conversion Script

### 2.1 Create Processing Script

**File:** `scripts/00_convert_railways.py`

This script converts raw data into a clean format. Use the roads script as a template.

```python
#!/usr/bin/env python3
"""Parse official Latvian railway statistics"""

import pandas as pd
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Processing Railway Statistics")
print("=" * 60)
print()

# Read raw data
print("1/3 Reading railway statistics...")
df = pd.read_csv('data/raw/railways_statistics.csv')
print(f"[OK] Loaded {len(df)} rows")

# Standardize columns
print()
print("2/3 Standardizing data format...")
df.columns = ['municipality_name', 'railway_km']

# Remove rows with missing data
df = df.dropna(subset=['railway_km'])
print(f"[OK] {len(df)} municipalities with data")

# Sort for readability
df = df.sort_values('railway_km', ascending=False).reset_index(drop=True)

# Display statistics
print()
print("Statistics:")
print(f"  Total municipalities: {len(df)}")
print(f"  Total railway km: {df['railway_km'].sum():.2f}")
print(f"  Average per municipality: {df['railway_km'].mean():.2f} km")

print()
print("3/3 Saving standardized data...")
df.to_csv('data/raw/official_railway_stats.csv', index=False)
print("[OK] Saved to data/raw/official_railway_stats.csv")

print()
print("=" * 60)
print("[OK] Conversion complete!")
print("=" * 60)
print()
print("Next: Run scripts/02_extract_railways.py")
```

---

## Step 3: Extract OSM Data

### 3.1 Create OSM Extraction Script

**File:** `scripts/02_extract_railways.py`

This script extracts relevant OSM features from the OSM data file.

```python
#!/usr/bin/env python3
"""Extract railway data from OSM"""

import geopandas as gpd
import osmium
from shapely.geometry import Point, LineString, MultiLineString
import pandas as pd
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Extracting Railways from OSM")
print("=" * 60)
print()

# Load municipality boundaries for spatial filtering
print("1/4 Loading municipality boundaries...")
gdf_munic = gpd.read_file('data/raw/municipalities.geojson')
bounds = gdf_munic.total_bounds
print(f"[OK] Loaded {len(gdf_munic)} municipalities")

# Extract railways from OSM
print()
print("2/4 Extracting railways from OSM...")

class RailwayHandler(osmium.SimpleHandler):
    def __init__(self):
        super(RailwayHandler, self).__init__()
        self.railways = []
    
    def way(self, w):
        # Extract railway lines
        if 'railway' in w.tags:
            try:
                coords = [(node.lon, node.lat) for node in w.nodes]
                if len(coords) > 1:
                    line = LineString(coords)
                    self.railways.append({
                        'osm_id': w.id,
                        'railway_type': w.tags.get('railway', 'unknown'),
                        'geometry': line,
                        'length_km': line.length * 111.0  # Approximate conversion
                    })
            except:
                pass

handler = RailwayHandler()
handler.apply_file('data/raw/latvia-latest.osm.pbf')

railways_gdf = gpd.GeoDataFrame(handler.railways, crs='EPSG:4326')
print(f"[OK] Extracted {len(railways_gdf)} railway ways")
print(f"     Total length: {railways_gdf['length_km'].sum():.2f} km")

# Spatial join with municipalities
print()
print("3/4 Joining railways to municipalities...")
railways_joined = gpd.sjoin(railways_gdf, gdf_munic, how='left')
railways_by_munic = railways_joined.groupby('municipality_name').agg({
    'length_km': 'sum'
}).reset_index()
railways_by_munic.columns = ['municipality_name', 'osm_railway_km']

print(f"[OK] {len(railways_by_munic)} municipalities with railways")

# Save output
print()
print("4/4 Saving processed railways...")
railways_by_munic.to_csv('data/processed/osm_railways.csv', index=False)
print("[OK] Saved to data/processed/osm_railways.csv")

print()
print("=" * 60)
print("[OK] Railway extraction complete!")
print("=" * 60)
```

**Note:** The exact method depends on what OSM features you're extracting and how you want to measure them.

---

## Step 4: Calculate Completeness

### 4.1 Create Completeness Script

**File:** `scripts/05_calculate_railways_completeness.py`

```python
#!/usr/bin/env python3
"""Calculate railway completeness for municipalities"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
import sys
import io

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Calculating Railway Completeness")
print("=" * 60)
print()

# Load data
print("1/4 Loading data...")
official_df = pd.read_csv('data/raw/official_railway_stats.csv')
osm_df = pd.read_csv('data/processed/osm_railways.csv')
gdf_munic = gpd.read_file('data/raw/municipalities.geojson')

print(f"[OK] Official: {len(official_df)} municipalities")
print(f"     OSM: {len(osm_df)} municipalities")

# Merge data
print()
print("2/4 Merging datasets...")
completeness_df = gdf_munic[['municipality_name', 'geometry']].copy()
completeness_df = completeness_df.merge(official_df, on='municipality_name', how='left')
completeness_df = completeness_df.merge(osm_df, on='municipality_name', how='left')

# Fill missing values
completeness_df['railway_km'] = completeness_df['railway_km'].fillna(0)
completeness_df['osm_railway_km'] = completeness_df['osm_railway_km'].fillna(0)

print(f"[OK] Combined {len(completeness_df)} municipalities")

# Calculate completeness
print()
print("3/4 Calculating completeness...")

def calculate_completeness(row):
    if row['railway_km'] == 0:
        return None  # No official data
    return (row['osm_railway_km'] / row['railway_km']) * 100

completeness_df['completeness_pct'] = completeness_df.apply(calculate_completeness, axis=1)

# Assign categories
def assign_category(completeness):
    if pd.isna(completeness):
        return 'No data'
    elif completeness >= 95 and completeness <= 105:
        return 'Complete'
    elif completeness >= 50 and completeness < 95:
        return 'Partial'
    elif completeness < 50:
        return 'Low'
    else:
        return 'Over-mapped'

completeness_df['category'] = completeness_df['completeness_pct'].apply(assign_category)

# Statistics
print()
print("Distribution:")
print(completeness_df['category'].value_counts().to_string())

# Save results
print()
print("4/4 Saving results...")
completeness_gdf = gpd.GeoDataFrame(completeness_df, crs='EPSG:4326')
completeness_gdf.to_file('data/processed/railways_completeness.geojson', driver='GeoJSON')

completeness_csv = completeness_df[[
    'municipality_name', 'railway_km', 'osm_railway_km', 
    'completeness_pct', 'category'
]]
completeness_csv.to_csv('data/processed/railways_completeness.csv', index=False)

print("[OK] Saved to data/processed/")

print()
print("=" * 60)
print("[OK] Railway completeness calculated!")
print("=" * 60)
```

---

## Step 5: Update Application Configuration

### 5.1 Add Topic to app.py

Edit `app.py` and update the `AVAILABLE_METRICS` dictionary:

```python
AVAILABLE_METRICS = {
    'roads': {
        'name': 'Road Network Completeness',
        'description': 'Analysis of OSM road mapping completeness compared to official statistics',
        'osm_field': 'osm_road_km',
        'official_field': 'road_length_km',
        'unit': 'km',
        'enabled': True,
        'data_file': 'data/processed/roads_completeness.geojson'
    },
    'railways': {
        'name': 'Railway Network Completeness',
        'description': 'Analysis of OSM railway mapping completeness compared to official statistics',
        'osm_field': 'osm_railway_km',
        'official_field': 'railway_km',
        'unit': 'km',
        'enabled': True,  # ← Change to True to activate
        'data_file': 'data/processed/railways_completeness.geojson'
    },
    # ... other topics
}
```

### 5.2 Update Data Loading (if using dynamic loading)

In `app.py`, ensure the `load_data()` function can handle multiple topics:

```python
def load_data(metric='roads'):
    """Load data for specified metric"""
    try:
        if metric in AVAILABLE_METRICS and AVAILABLE_METRICS[metric]['enabled']:
            metric_config = AVAILABLE_METRICS[metric]
            completeness_geojson = gpd.read_file(metric_config['data_file'])
            return completeness_geojson
    except Exception as e:
        print(f"Error loading {metric} data: {e}")
    return None
```

---

## Step 6: Update the Processing Pipeline

### 6.1 Add to run_all.sh

Add your new scripts to the automated pipeline:

```bash
#!/bin/bash

echo "Running complete analysis pipeline..."
echo ""

# New: Process railway data
echo "Processing railway statistics..."
python scripts/00_convert_railways.py

echo "Extracting railways from OSM..."
python scripts/02_extract_railways.py

echo "Calculating railway completeness..."
python scripts/05_calculate_railways_completeness.py

# ... existing scripts for roads ...

echo "All processing complete!"
```

---

## Step 7: Prepare Map Data Format

### 7.1 GeoJSON Properties

Your final GeoJSON should include these properties:

```json
{
  "type": "Feature",
  "geometry": {...},
  "properties": {
    "municipality_name": "Rīga",
    "osm_railway_km": 47.2,
    "railway_km": 45.0,
    "completeness_pct": 104.89,
    "category": "Over-mapped"
  }
}
```

### 7.2 Data Validation

Before using your data, validate it:

```python
import geopandas as gpd
gdf = gpd.read_file('data/processed/railways_completeness.geojson')

# Check all required fields exist
required_fields = ['municipality_name', 'osm_railway_km', 'railway_km', 'completeness_pct', 'category']
for field in required_fields:
    if field not in gdf.columns:
        raise ValueError(f"Missing required field: {field}")

# Check data types
assert gdf['completeness_pct'].dtype in ['float64', 'int64']

# Check completeness scores are reasonable
assert gdf['completeness_pct'].min() >= 0, "Completeness should be >= 0"

print("✓ Data validation passed!")
```

---

## Testing Your New Topic

### 1. Run Processing Scripts

```bash
python scripts/00_convert_railways.py
python scripts/02_extract_railways.py
python scripts/05_calculate_railways_completeness.py
```

### 2. Verify Output Files

```bash
ls data/processed/railways_*
# Should see:
# - railways_completeness.geojson
# - railways_completeness.csv
```

### 3. Check Data Quality

```python
import geopandas as gpd
gdf = gpd.read_file('data/processed/railways_completeness.geojson')
print(gdf.head())
print(gdf.describe())
print(gdf['category'].value_counts())
```

### 4. Start Web App

```bash
python app.py
```

Visit: `http://localhost:5000`

The railways option should now appear in the topic selector!

---

## Complete Checklist for Adding a New Topic

- [ ] **Data Preparation**
  - [ ] Find official statistics
  - [ ] Verify municipality name matching
  - [ ] Create `data/raw/your_data.csv`

- [ ] **Processing Scripts**
  - [ ] Create `scripts/00_convert_your_topic.py`
  - [ ] Create `scripts/02_extract_your_topic.py`
  - [ ] Create `scripts/05_calculate_your_topic_completeness.py`
  - [ ] Test each script individually

- [ ] **Data Validation**
  - [ ] Verify output GeoJSON format
  - [ ] Check all required fields present
  - [ ] Validate completeness percentages
  - [ ] Check municipality name matching

- [ ] **Application Integration**
  - [ ] Add to `AVAILABLE_METRICS` in `app.py`
  - [ ] Set `enabled: True`
  - [ ] Verify data file path is correct

- [ ] **Pipeline**
  - [ ] Add scripts to `scripts/run_all.sh`
  - [ ] Test full pipeline: `./scripts/run_all.sh`

- [ ] **Testing**
  - [ ] Run complete pipeline
  - [ ] Start web app: `python app.py`
  - [ ] Verify topic appears in web interface
  - [ ] Verify map displays correctly
  - [ ] Test topic selection

---

## Troubleshooting

### Issue: "Municipality names don't match"
**Solution:** Check exact names in GeoJSON:
```python
import geopandas as gpd
gdf = gpd.read_file('data/raw/municipalities.geojson')
print(sorted(gdf['municipality_name'].unique()))
```

### Issue: "Empty GeoJSON or no data shown"
**Solution:** Verify spatial join:
```python
import geopandas as gpd
gdf1 = gpd.read_file('data/processed/your_topic.geojson')
print(f"Rows: {len(gdf1)}")
print(f"Valid geometries: {gdf1.geometry.is_valid.sum()}")
print(gdf1.head())
```

### Issue: "Unicode/encoding errors"
**Solution:** Ensure UTF-8 encoding:
```python
df.to_csv('file.csv', encoding='utf-8')
gdf.to_file('file.geojson', driver='GeoJSON', encoding='utf-8')
```

---

## For Other Countries

The same architecture works for any country! Key changes:

1. **Find official statistics** for your country
2. **Identify municipality/region boundaries** (GeoJSON)
3. **Download OSM data** for your country (from geofabrik.de)
4. **Adjust scripts** for your country's naming conventions and data formats
5. **Test and validate** municipality name matching

Example OSM data download:
```bash
# Germany
wget https://download.geofabrik.de/europe/germany-latest.osm.pbf

# UK
wget https://download.geofabrik.de/europe/great-britain-latest.osm.pbf

# Or any country: https://download.geofabrik.de/
```

---

## Support and Questions

For issues or questions:
1. Check the script comments
2. Review the roads implementation as reference
3. Validate your data with Python/GeoPandas
4. Test each step individually before running full pipeline

---

Good luck adding new topics!
