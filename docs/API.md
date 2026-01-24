# API Documentation

## Overview

LatviaOSM-Check provides a RESTful API for accessing OpenStreetMap completeness data for Latvia. All endpoints return JSON data unless otherwise specified.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Endpoints

### Maps & Visualizations

#### GET `/`
Returns the main interactive map interface with hierarchical geographic selector.

**Response:** HTML page with interactive map

**Example:**
```bash
curl http://localhost:5000/
```

---

#### GET `/roads`
Returns the roads completeness map.

**Response:** HTML page with roads analysis

---

#### GET `/forests`
Returns the forests completeness map.

**Response:** HTML page with forests analysis

---

#### GET `/libraries`
Returns the libraries completeness map.

**Response:** HTML page with libraries analysis

---

#### GET `/combined-map`
Returns the combined interactive map with roads, forests, and libraries layers. Users can toggle between the three layers using the dropdown selector. Libraries are shown by default.

**Features:**
- Three feature layers: Roads, Forests, Libraries
- Dynamic legend that updates based on selected layer
- Color-coded completeness indicators
- Click on municipality for detailed statistics

**Response:** HTML page with combined multi-layer analysis

---

### Data APIs

#### GET `/api/geojson-data`
Returns all geographic features with municipality boundaries and metadata.

**Response Format:**
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
        "Area_Type": "City",
        "osm_road_km": 1234.56,
        "osm_segments": 5678,
        "completeness_pct": 78.5,
        "...": "..."
      }
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/geojson-data | jq '.features[0]'
```

**Python Example:**
```python
import requests
import geopandas as gpd

response = requests.get('http://localhost:5000/api/geojson-data')
gdf = gpd.GeoDataFrame.from_features(response.json()['features'])
print(gdf.head())
```

---

#### GET `/api/csv-data`
Returns statistical data for all municipalities in JSON format.

**Response Format:**
```json
[
  {
    "municipality_name": "Rīga",
    "Area_Type": "City",
    "osm_road_km": 1234.56,
    "osm_segments": 5678,
    "official_road_km": 1000.00,
    "completeness_pct": 123.5,
    "difference_km": 234.56
  }
]
```

**Query Parameters:**
- `municipality` (optional): Filter by municipality name
- `type` (optional): Filter by area type (`City` or `Municipality`)

**Examples:**
```bash
# Get all data
curl http://localhost:5000/api/csv-data

# Get specific municipality
curl "http://localhost:5000/api/csv-data?municipality=Rīga"

# Get only cities
curl "http://localhost:5000/api/csv-data?type=City"
```

**Python Example:**
```python
import requests
import pandas as pd

response = requests.get('http://localhost:5000/api/csv-data')
df = pd.DataFrame(response.json())
print(df.describe())
```

---

#### GET `/api/forest-data`
Returns forest completeness data.

**Response Format:**
```json
[
  {
    "municipality_name": "Aizkraukles novads",
    "Area_Type": "Municipality",
    "osm_forest_count": 245,
    "official_forest_count": 200,
    "completeness_pct": 122.5
  }
]
```

**Example:**
```bash
curl http://localhost:5000/api/forest-data
```

---

#### GET `/api/library-data`
Returns library completeness data.

**Response Format:**
```json
[
  {
    "municipality_name": "Rīga",
    "Area_Type": "City",
    "osm_library_count": 30,
    "official_library_count": 28,
    "completeness_pct": 107.1
  }
]
```

**Example:**
```bash
curl http://localhost:5000/api/library-data
```

---

#### GET `/api/hierarchy`
Returns the complete geographic hierarchy structure for the hierarchical selector.

**Response Format:**
```json
{
  "Latvia": {
    "Kurzeme": {
      "Dienvidkurzemes novads": {
        "Roads": {},
        "Forests": {},
        "Libraries": {}
      }
    },
    "Vidzeme": {},
    "Zemgale": {},
    "Latgale": {},
    "Cities": {
      "Rīga": {},
      "Daugavpils": {}
    }
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/hierarchy
```

---

#### GET `/api/statistics`
Returns aggregate statistics for selected municipalities.

**Query Parameters:**
- `municipalities` (required): Comma-separated list of municipality names

**Response Format:**
```json
{
  "total_municipalities": 5,
  "total_osm_roads_km": 5432.10,
  "total_osm_segments": 23456,
  "total_official_roads_km": 4321.00,
  "average_completeness_pct": 125.7,
  "min_completeness_pct": 85.3,
  "max_completeness_pct": 156.8
}
```

**Example:**
```bash
curl "http://localhost:5000/api/statistics?municipalities=Rīga,Jūrmala,Daugavpils"
```

**Python Example:**
```python
import requests

municipalities = ['Rīga', 'Jūrmala', 'Daugavpils']
params = {'municipalities': ','.join(municipalities)}

response = requests.get('http://localhost:5000/api/statistics', params=params)
stats = response.json()
print(f"Average completeness: {stats['average_completeness_pct']:.1f}%")
```

---

### File Downloads

#### GET `/api/download/geojson`
Downloads the complete GeoJSON file.

**Response:** GeoJSON file attachment

**Example:**
```bash
curl -O http://localhost:5000/api/download/geojson
```

---

#### GET `/api/download/csv`
Downloads the complete CSV statistics file.

**Response:** CSV file attachment

**Example:**
```bash
curl -O http://localhost:5000/api/download/csv
```

---

## Data Models

### Municipality Properties

| Field | Type | Description |
|-------|------|-------------|
| `municipality_name` | string | Official municipality name |
| `Area_Type` | string | Either "City" or "Municipality" |
| `osm_road_km` | float | Total road length from OSM (km) |
| `osm_segments` | integer | Number of road segments in OSM |
| `official_road_km` | float | Official road length from government data (km) |
| `completeness_pct` | float | OSM coverage percentage |
| `difference_km` | float | Difference between OSM and official (km) |
| `geometry` | GeoJSON | Municipality boundary polygon |

### Forest Properties

| Field | Type | Description |
|-------|------|-------------|
| `municipality_name` | string | Municipality name |
| `osm_forest_count` | integer | Number of forests in OSM |
| `official_forest_count` | integer | Official forest count |
| `completeness_pct` | float | Forest mapping completeness |

### Library Properties

| Field | Type | Description |
|-------|------|-------------|
| `municipality_name` | string | Municipality name |
| `osm_library_count` | integer | Number of libraries in OSM |
| `official_library_count` | integer | Official library count |
| `completeness_pct` | float | Library mapping completeness |

---

## Error Handling

### Error Response Format

```json
{
  "error": "Error message description",
  "status": 400
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, there are no rate limits implemented. However, please be considerate with API usage.

---

## CORS

CORS is enabled for all origins. You can make requests from any domain.

---

## Examples

### JavaScript (Fetch API)

```javascript
// Get all municipalities
fetch('http://localhost:5000/api/csv-data')
  .then(response => response.json())
  .then(data => {
    console.log(`Total municipalities: ${data.length}`);
    const topMunicipalities = data
      .sort((a, b) => b.completeness_pct - a.completeness_pct)
      .slice(0, 10);
    console.log('Top 10 by completeness:', topMunicipalities);
  });

// Get GeoJSON and display on map
fetch('http://localhost:5000/api/geojson-data')
  .then(response => response.json())
  .then(geojson => {
    L.geoJSON(geojson, {
      style: feature => ({
        fillColor: getColor(feature.properties.completeness_pct),
        weight: 1,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.7
      })
    }).addTo(map);
  });
```

### Python (Requests + Pandas)

```python
import requests
import pandas as pd

# Load data
response = requests.get('http://localhost:5000/api/csv-data')
df = pd.DataFrame(response.json())

# Analysis
print(f"Total municipalities: {len(df)}")
print(f"Average completeness: {df['completeness_pct'].mean():.1f}%")

# Filter cities only
cities = df[df['Area_Type'] == 'City']
print(f"\nCities: {len(cities)}")
print(cities[['municipality_name', 'completeness_pct']])

# Top 10 by road coverage
top10 = df.nlargest(10, 'osm_road_km')
print(f"\nTop 10 by total roads:")
print(top10[['municipality_name', 'osm_road_km']])
```

### R

```r
library(httr)
library(jsonlite)
library(dplyr)

# Get data
response <- GET("http://localhost:5000/api/csv-data")
data <- fromJSON(content(response, "text"))

# Convert to data frame
df <- as.data.frame(data)

# Summary statistics
summary(df$completeness_pct)

# Top municipalities
top_n(df, 10, completeness_pct)
```

---

## Changelog

### Version 2.0.0
- Added hierarchical geographic selector
- Added forest and library analysis endpoints
- Improved GeoJSON structure
- Added combined map view

### Version 1.0.0
- Initial API release
- Basic road completeness endpoints
- Interactive map interface

---

## Support

For issues, questions, or contributions, please visit:
- GitHub Issues: [Repository Issues](https://github.com/<your-org>/latvia_osm_project/issues)
- Documentation: [README.md](../README.md)
