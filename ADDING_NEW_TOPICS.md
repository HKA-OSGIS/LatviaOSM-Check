# How to Add New Topics (Railways, Buildings, POIs, Forests)

## Overview

The topic selector framework is ready for future topics. Currently, only **Roads** is implemented. This guide explains how to add new topics as they become available.

## Current Architecture

```
templates/topic_selector.html
├── Topic buttons (Roads, Railways, Buildings, POIs, Forests)
├── Map display
└── Statistics dashboard

Backend:
├── /api/geojson-data (roads GeoJSON)
├── /api/csv-data (roads statistics)
└── (Future: /api/railways-data, /api/buildings-data, etc.)
```

## Steps to Add a New Topic

### Step 1: Extract OSM Data

Create a new script in `scripts/` to extract the new data type from OSM.

**Example: `10_extract_railways.py`**

```python
#!/usr/bin/env python3
"""Extract railway data from OSM"""

import geopandas as gpd
from pathlib import Path

print("Extracting railways...")

# Read OSM data (PBF format)
railways = gpd.read_file('data/raw/latvia-latest.osm.pbf', layer='lines')

# Filter for railways
railways = railways[railways['railway'].notna()]

# Calculate length
railways['length_km'] = railways.geometry.length / 1000

# Group by municipality
rail_by_muni = railways.groupby('municipality').agg({
    'length_km': 'sum',
    'osm_id': 'count'
}).reset_index()
rail_by_muni.columns = ['municipality_name', 'railway_km', 'num_segments']

# Save
rail_by_muni.to_csv('outputs/exports/railways.csv', index=False)
print("✓ Saved railways.csv")
```

**Key Points:**
- Extract from `data/raw/latvia-latest.osm.pbf`
- Group by municipality
- Create: `num_km` and `num_segments` columns
- Save to `outputs/exports/{topic}.csv`

### Step 2: Create Backend Endpoint

Update `app.py` to serve the new data:

```python
@app.route('/api/railways-data', methods=['GET'])
def api_railways_data():
    """Get railway statistics."""
    railways_file = ROOT / 'outputs' / 'exports' / 'railways.csv'
    if railways_file.exists():
        df = pd.read_csv(railways_file, encoding='utf-8')
        records = json.loads(df.to_json(orient='records'))
        return jsonify(records)
    return jsonify({'error': 'Railway data not available'}), 500

@app.route('/api/railways-geojson', methods=['GET'])
def api_railways_geojson():
    """Get railway GeoJSON."""
    # Load from processed GeoJSON
    geojson_file = ROOT / 'outputs' / 'exports' / 'railways.geojson'
    if geojson_file.exists():
        with open(geojson_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Railway GeoJSON not available'}), 500
```

### Step 3: Update Frontend

Modify `templates/topic_selector.html` to enable the new topic:

```javascript
// Line ~10: Update topics array
const topics = [
    { id: 'roads', label: '🛣️ Roads', enabled: true, icon: '🛣️' },
    { id: 'railways', label: '🚂 Railways', enabled: true, icon: '🚂' },  // ← Change to true
    { id: 'buildings', label: '🏢 Buildings', enabled: false, comingSoon: true },
    { id: 'pois', label: '📍 POIs', enabled: false, comingSoon: true },
    { id: 'forests', label: '🌲 Forests', enabled: false, comingSoon: true }
];
```

Then add display function:

```javascript
// Add to loadTopicData() function
if (currentTopic === 'railways') {
    if (!allData.railways) {
        const response = await fetch('/api/railways-geojson');
        const csvResponse = await fetch('/api/railways-data');
        
        allData.railways = {
            geojson: await response.json(),
            csv: await csvResponse.json()
        };
    }
    
    displayRailways();
    statsBox.style.display = 'block';
}

// Add new display function
function displayRailways() {
    if (geojsonLayer) {
        map.removeLayer(geojsonLayer);
    }
    
    const data = allData.railways;
    if (!data) return;
    
    geojsonLayer = L.geoJSON(data.geojson, {
        style: {
            color: '#FF5722',  // Different color for railways
            weight: 3,
            opacity: 0.7
        },
        onEachFeature: function(feature, layer) {
            const props = feature.properties;
            const popup = `<strong>${props.municipality_name}</strong><br/>
                          🚂 ${props.railway_km} km of railways<br/>
                          📊 ${props.num_segments} segments`;
            layer.bindPopup(popup);
        }
    }).addTo(map);
    
    const bounds = geojsonLayer.getBounds();
    if (bounds.isValid()) {
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

// Update updateStats() to handle railways
if (currentTopic === 'railways') {
    // Similar logic but for railway_km instead of osm_road_km
    // ...
}
```

### Step 4: Test

```bash
# Run extraction script
python scripts/10_extract_railways.py

# Start Flask
python app.py

# Visit http://localhost:5000
# Click "Railways" button to see the data
```

## Data Source Guidelines

### For Each New Topic:

1. **Column Names (Required)**
   - `municipality_name` - Municipality identifier
   - `{topic}_km` - Total length in kilometers
   - `num_segments` - Number of features

2. **Optional Columns**
   - `completeness_pct` - If official statistics available
   - `category` - Classification (e.g., "major", "minor")
   - `density_per_km2` - Density metric

3. **File Locations**
   - CSV: `outputs/exports/{topic}.csv`
   - GeoJSON: `outputs/exports/{topic}.geojson`

### Data Sources for Future Topics:

**Railways:**
- OSM railway ways with `railway` tag
- Latvia Railways (LDz) official statistics (if available)

**Buildings:**
- OSM building polygons with `building` tag
- Group by municipality
- Count total and by type

**POIs (Points of Interest):**
- Hospitals: `amenity=hospital`
- Restaurants: `amenity=restaurant`
- Pharmacies: `amenity=pharmacy`

**Forests:**
- OSM landuse areas with `landuse=forest`
- Calculate total area
- Compare with official statistics

## Example: Full Implementation for Railways

### 1. Extract (scripts/10_extract_railways.py)

```python
#!/usr/bin/env python3
import geopandas as gpd
import pandas as pd

rails = gpd.read_file('data/raw/latvia-latest.osm.pbf', layer='lines')
rails = rails[rails['railway'].notna()]
rails['length_km'] = rails.geometry.length / 1000

result = rails.groupby('municipality').agg({
    'length_km': 'sum',
    'osm_id': 'count'
}).reset_index()
result.columns = ['municipality_name', 'railway_km', 'num_segments']
result.to_csv('outputs/exports/railways.csv', index=False)
```

### 2. Backend (app.py)

```python
@app.route('/api/railways-data')
def api_railways_data():
    df = pd.read_csv('outputs/exports/railways.csv')
    return jsonify(json.loads(df.to_json(orient='records')))
```

### 3. Frontend (topic_selector.html)

- Enable in `topics` array
- Add `displayRailways()` function
- Add stats logic in `updateStats()`
- Choose distinctive color (`#FF5722` for railways)

### 4. Run

```bash
python scripts/10_extract_railways.py
python app.py
# Click Railways button
```

## Quick Checklist for New Topics

- [ ] Create extraction script in `scripts/`
- [ ] Output CSV with `municipality_name`, `{topic}_km`, `num_segments`
- [ ] Create GeoJSON with same municipality_name in properties
- [ ] Add backend endpoint `/api/{topic}-data` and `/api/{topic}-geojson`
- [ ] Set `enabled: true` in topics array
- [ ] Add display function in frontend
- [ ] Add stats calculation logic
- [ ] Test on http://localhost:5000
- [ ] Update REQUIREMENTS_ASSESSMENT.md

## Troubleshooting

**API returns 500 error:**
- Check that CSV exists in `outputs/exports/`
- Verify column names match code

**Map not updating:**
- Check browser console (F12) for JavaScript errors
- Ensure GeoJSON has valid geometry

**Statistics show wrong numbers:**
- Verify column names in CSV
- Check that municipality_name matches between CSV and GeoJSON

## Questions?

Refer to existing roads implementation:
- `scripts/05_calculate_completeness.py` (extraction)
- `app.py` lines ~115-125 (API endpoints)
- `templates/topic_selector.html` lines ~160-210 (display logic)
