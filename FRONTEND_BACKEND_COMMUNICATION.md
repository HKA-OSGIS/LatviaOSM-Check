# Frontend & Backend Communication Architecture

**Date**: January 28, 2026  
**Topic**: How Frontend and Backend Components Communicate  
**Project**: LatviaOSM-Check

---

## System Overview

### Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│            USER'S WEB BROWSER                         │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌─────────────────────────────────────────────┐    │
│  │         FRONTEND (Client-Side)              │    │
│  ├─────────────────────────────────────────────┤    │
│  │                                              │    │
│  │  HTML          CSS           JavaScript     │    │
│  │  ┌────────┐  ┌─────────┐  ┌─────────────┐ │    │
│  │  │Content │  │ Styling │  │ Leaflet.js  │ │    │
│  │  │Layout  │  │Bootstrap│  │ Events      │ │    │
│  │  │        │  │         │  │ API Calls   │ │    │
│  │  └────────┘  └─────────┘  └─────────────┘ │    │
│  │                                              │    │
│  │  ┌──────────────────────────────────────┐  │    │
│  │  │ Leaflet.js Interactive Map           │  │    │
│  │  ├──────────────────────────────────────┤  │    │
│  │  │ - Draw polygons (municipalities)     │  │    │
│  │  │ - Color coding (by completeness)     │  │    │
│  │  │ - Handle clicks (show popups)        │  │    │
│  │  │ - Layer toggle (roads/forests/libs)  │  │    │
│  │  └──────────────────────────────────────┘  │    │
│  │                                              │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
└──────────────────────────────────────────────────────┘
        ▲                                  ▼
        │         HTTP REQUESTS           │
        │         (AJAX Calls)             │
        │         JSON Exchange            │
        │         XMLHttpRequest           │
        │         Fetch API                │
        │                                   │
        └───────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│              SERVER (Backend)                        │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────────────────────────────────────┐   │
│  │         FLASK WEB APPLICATION                │   │
│  │         (app.py - 328 lines)                 │   │
│  ├──────────────────────────────────────────────┤   │
│  │                                               │   │
│  │  ┌────────────────────────────────────────┐  │   │
│  │  │ Route Handlers                         │  │   │
│  │  ├────────────────────────────────────────┤  │   │
│  │  │ @app.route('/')                        │  │   │
│  │  │ @app.route('/roads')                   │  │   │
│  │  │ @app.route('/forests')                 │  │   │
│  │  │ @app.route('/libraries')               │  │   │
│  │  │ @app.route('/combined-map')            │  │   │
│  │  └────────────────────────────────────────┘  │   │
│  │                                               │   │
│  │  ┌────────────────────────────────────────┐  │   │
│  │  │ API Endpoints                          │  │   │
│  │  ├────────────────────────────────────────┤  │   │
│  │  │ /api/geojson-data → GeoJSON            │  │   │
│  │  │ /api/csv-data → Statistics             │  │   │
│  │  │ /api/forest-data → Forest metrics      │  │   │
│  │  │ /api/library-data → Library metrics    │  │   │
│  │  └────────────────────────────────────────┘  │   │
│  │                                               │   │
│  │  ┌────────────────────────────────────────┐  │   │
│  │  │ Data Processing Layer                  │  │   │
│  │  ├────────────────────────────────────────┤  │   │
│  │  │ load_geojson() → Cache GeoJSON         │  │   │
│  │  │ load_dataframe() → Cache CSV            │  │   │
│  │  │ Process & format data                  │  │   │
│  │  └────────────────────────────────────────┘  │   │
│  │                                               │   │
│  │  ┌────────────────────────────────────────┐  │   │
│  │  │ In-Memory Cache                        │  │   │
│  │  ├────────────────────────────────────────┤  │   │
│  │  │ _geojson_cache                         │  │   │
│  │  │ _dataframe_cache                       │  │   │
│  │  │ _forest_dataframe_cache                │  │   │
│  │  │ _library_dataframe_cache               │  │   │
│  │  └────────────────────────────────────────┘  │   │
│  │                                               │   │
│  └──────────────────────────────────────────────┘   │
│                                                       │
│  ┌──────────────────────────────────────────────┐   │
│  │         FILE SYSTEM (Data Storage)           │   │
│  ├──────────────────────────────────────────────┤   │
│  │                                               │   │
│  │  outputs/exports/                            │   │
│  │  ├─ latvia_lau1.geojson                     │   │
│  │  ├─ completeness_municipalities.csv          │   │
│  │  ├─ completeness_forests.csv                │   │
│  │  └─ completeness_libraries.csv              │   │
│  │                                               │   │
│  │  outputs/maps/                               │   │
│  │  ├─ interactive_map.html                    │   │
│  │  ├─ forest_completeness_map.html            │   │
│  │  ├─ library_completeness_map.html           │   │
│  │  └─ combined_map.html                       │   │
│  │                                               │   │
│  └──────────────────────────────────────────────┘   │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## Components Breakdown

### FRONTEND COMPONENTS

#### 1. **HTML Structure** (templates/)

**Files**:
- `templates/dynamic_map.html` - Main map template
- `templates/with_dropdown.html` - Dropdown selector template

**Responsibilities**:
```
<html>
├─ Head
│  ├─ Load Leaflet.js CSS
│  ├─ Load Bootstrap CSS
│  ├─ Load jQuery
│  └─ Custom CSS styles
│
├─ Body
│  ├─ Header (title, description)
│  ├─ Map container (div#map)
│  ├─ Legend (completeness ranges)
│  ├─ Info box (municipality info)
│  └─ Footer (credits)
│
└─ Scripts
   ├─ Leaflet.js initialization
   ├─ AJAX calls to backend
   ├─ Event handlers
   └─ Dynamic updates
```

**Key HTML Elements**:
```html
<!-- Map container -->
<div id="map" style="width: 100%; height: 100vh;"></div>

<!-- Legend -->
<div id="legend" class="legend">
  <div class="legend-item">
    <span class="legend-color" style="background: #2ecc71;"></span>
    <span>90-100%: Excellent</span>
  </div>
  <!-- More items... -->
</div>

<!-- Info popup -->
<div id="info" class="info-box">
  Municipality data and statistics
</div>
```

---

#### 2. **Leaflet.js** (Map Library)

**What It Does**:
```
JavaScript Library for Interactive Maps
├─ Display map tiles (OpenStreetMap)
├─ Render GeoJSON features (polygons, lines, points)
├─ Handle user interactions (click, zoom, pan)
├─ Show popups/tooltips
├─ Layer management
└─ Color-coded visualization
```

**Key JavaScript Code**:
```javascript
// Initialize map
const map = L.map('map').setView([56.88, 24.60], 8);

// Add base layer (OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Fetch GeoJSON from backend API
fetch('/api/geojson-data')
    .then(response => response.json())
    .then(geojson => {
        // Style by completeness percentage
        L.geoJSON(geojson, {
            style: function(feature) {
                const completeness = feature.properties.completeness_pct;
                let color;
                if (completeness >= 90) color = '#2ecc71'; // Green
                else if (completeness >= 70) color = '#f1c40f'; // Yellow
                else color = '#e74c3c'; // Red
                
                return { color: color, weight: 2, opacity: 0.7 };
            },
            onEachFeature: function(feature, layer) {
                // Show popup on click
                layer.bindPopup(`
                    <b>${feature.properties.municipality_name}</b><br>
                    Completeness: ${feature.properties.completeness_pct}%
                `);
            }
        }).addTo(map);
    });

// Handle click events
map.on('click', function(e) {
    console.log("Clicked at:", e.latlng);
});
```

**Responsibilities**:
- Render interactive maps
- Color-code by completeness
- Handle user interactions
- Display data dynamically
- Manage map layers

---

#### 3. **Bootstrap 5** (CSS Framework)

**What It Does**:
```
Responsive CSS Framework
├─ Responsive grid layout
├─ Styling components (buttons, cards, forms)
├─ Mobile-friendly design
├─ Pre-built components
└─ Consistent visual design
```

**Usage in Templates**:
```html
<!-- Responsive container -->
<div class="container-fluid">
  <div class="row">
    <div class="col-md-8">Map</div>
    <div class="col-md-4">Legend</div>
  </div>
</div>

<!-- Styled buttons -->
<button class="btn btn-primary">Load Data</button>

<!-- Alert messages -->
<div class="alert alert-info">Loading data...</div>
```

---

#### 4. **jQuery** (JavaScript Utility)

**Functions**:
```javascript
// AJAX calls to backend
$.ajax({
    url: '/api/csv-data',
    type: 'GET',
    success: function(data) {
        console.log("Data received:", data);
    }
});

// DOM manipulation
$('#legend').show();
$('#loading').hide();

// Event binding
$('#municipality-select').on('change', function() {
    const selected = $(this).val();
    loadMunicipalityData(selected);
});
```

---

### BACKEND COMPONENTS

#### 1. **Flask Application** (app.py)

**What It Does**:
```
Python Web Framework
├─ Handle HTTP requests from frontend
├─ Route requests to appropriate handlers
├─ Load data from disk
├─ Cache data in memory
├─ Format responses (HTML, JSON)
└─ Send responses back to client
```

**Structure**:
```python
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Configuration
ROOT = Path(__file__).resolve().parent
GEOJSON_FILE = ROOT / 'outputs' / 'exports' / 'latvia_lau1.geojson'
CSV_FILE = ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'

# Global caches
_geojson_cache = None
_dataframe_cache = None

# Route handlers
@app.route('/')
def index():
    return render_template('dynamic_map.html')

@app.route('/api/geojson-data')
def get_geojson():
    return jsonify(load_geojson())

@app.route('/api/csv-data')
def get_csv_data():
    df = load_dataframe()
    return jsonify(df.to_dict('records'))
```

---

#### 2. **Route Handlers**

**What They Do**:
```
Handle HTTP Requests and Return Responses

GET / 
├─ Return: HTML page (interactive map)
├─ Template: dynamic_map.html
└─ Purpose: Main interface

GET /roads, /forests, /libraries
├─ Return: HTML page (specific map)
├─ Purpose: Feature-specific view
└─ Template: dynamic_map.html

GET /combined-map
├─ Return: HTML page (multi-layer map)
└─ Purpose: View all features together
```

**Code Example**:
```python
@app.route('/')
def index():
    """Render main page with roads map."""
    return render_template('dynamic_map.html')

@app.route('/roads')
def roads_map():
    """Render roads completeness map."""
    return render_template('dynamic_map.html')

@app.route('/api/geojson-data')
def get_geojson():
    """Return GeoJSON data as JSON."""
    data = load_geojson()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Data not found'}), 404
```

---

#### 3. **API Endpoints**

**What They Do**:
```
Return Data in JSON Format (for JavaScript to use)

/api/geojson-data
├─ Returns: GeoJSON FeatureCollection
├─ Used by: Leaflet.js to draw map
├─ Content: Geography + attributes
└─ Size: ~5-20 MB

/api/csv-data
├─ Returns: Array of JSON objects
├─ Used by: Data tables, statistics
├─ Content: Municipality statistics
└─ Size: ~100 KB

/api/forest-data, /api/library-data
├─ Returns: Feature-specific data
├─ Used by: Alternative analysis
└─ Content: Forest/Library metrics
```

**API Response Examples**:

```json
// /api/geojson-data
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
        "osm_road_km": 2496,
        "official_road_km": 1000,
        "completeness_pct": 249.6
      }
    }
    // ... more features
  ]
}
```

```json
// /api/csv-data
[
  {
    "municipality_name": "Rīga",
    "osm_road_km": 2496,
    "official_road_km": 1000,
    "completeness_pct": 249.6
  },
  {
    "municipality_name": "Kuldīga",
    "osm_road_km": 234,
    "official_road_km": 200,
    "completeness_pct": 117.0
  }
  // ... more municipalities
]
```

---

#### 4. **Data Loading Functions**

**What They Do**:
```
Load Data from Disk & Cache in Memory

load_geojson()
├─ Check cache: Is data already loaded?
├─ If yes: Return cached data (fast)
├─ If no: Read from latvia_lau1.geojson
├─ Store in _geojson_cache
└─ Return data to API endpoint

load_dataframe()
├─ Check cache: Is CSV already loaded?
├─ If yes: Return cached data
├─ If no: Read completeness_municipalities.csv
├─ Parse with pandas
├─ Store in _dataframe_cache
└─ Return to API endpoint
```

**Code Example**:
```python
def load_geojson():
    """Load GeoJSON and cache it."""
    global _geojson_cache
    
    # Check if already cached
    if _geojson_cache is None:
        # Load from disk only first time
        if GEOJSON_FILE.exists():
            with open(GEOJSON_FILE, 'r', encoding='utf-8') as f:
                _geojson_cache = json.load(f)
    
    # Return cached data
    return _geojson_cache

def load_dataframe():
    """Load CSV and cache it."""
    global _dataframe_cache
    
    if _dataframe_cache is None:
        if CSV_FILE.exists():
            _dataframe_cache = pd.read_csv(CSV_FILE, encoding='utf-8')
    
    return _dataframe_cache
```

---

#### 5. **Caching System**

**Why Caching?**
```
Performance Optimization

Problem:
├─ Reading large GeoJSON from disk is slow
├─ Parsing CSV file takes time
├─ Every request loads data again
└─ → Slow response times

Solution: In-Memory Caching
├─ Load data once when app starts
├─ Store in memory (RAM)
├─ Reuse for all requests
├─ No disk I/O needed
└─ → Fast responses (50-200ms)

Cache Variables:
├─ _geojson_cache (GeoJSON data)
├─ _dataframe_cache (CSV data)
├─ _forest_dataframe_cache
├─ _library_dataframe_cache
└─ _hierarchy_cache
```

**Benefits**:
- ✅ 50-100x faster than disk reads
- ✅ Consistent response times
- ✅ Handles concurrent users
- ✅ Reduces server load

---

## Communication Flow: Request to Response

### Step-by-Step Communication

```
1. USER OPENS BROWSER
   └─ Navigates to http://localhost:5000/

2. BROWSER SENDS HTTP REQUEST
   ├─ Method: GET
   ├─ Path: /
   └─ Headers: Content-Type, User-Agent, etc.

3. FLASK RECEIVES REQUEST
   ├─ Routes to handler: @app.route('/')
   ├─ Executes: index() function
   └─ Returns: HTML template

4. FLASK RENDERS HTML TEMPLATE
   ├─ Load: templates/dynamic_map.html
   ├─ Inject: Dynamic variables (if any)
   └─ Returns: Complete HTML page

5. BROWSER RECEIVES RESPONSE
   ├─ Status: 200 OK
   ├─ Content-Type: text/html
   └─ Body: HTML document

6. BROWSER PARSES HTML
   ├─ Read HTML structure
   ├─ Load CSS stylesheets
   ├─ Load JavaScript files
   │  ├─ Leaflet.js
   │  ├─ jQuery
   │  ├─ Custom JavaScript
   │  └─ Bootstrap JS
   └─ Display page

7. PAGE LOADS (Leaflet.js Initializes)
   ├─ Create map object
   ├─ Display OpenStreetMap tiles
   ├─ Initialize event listeners
   └─ Wait for user interaction

8. JAVASCRIPT MAKES AJAX CALL
   ├─ Code: fetch('/api/geojson-data')
   ├─ Type: Asynchronous HTTP GET request
   ├─ Headers: Accept: application/json
   └─ Body: None

9. FLASK RECEIVES API REQUEST
   ├─ Routes to: @app.route('/api/geojson-data')
   ├─ Executes: get_geojson() function
   ├─ Calls: load_geojson()
   │  ├─ Check: _geojson_cache
   │  ├─ If None: Read from file
   │  └─ Return: GeoJSON object
   ├─ Calls: jsonify(geojson)
   │  └─ Convert: Python dict → JSON string
   └─ Returns: JSON response

10. BROWSER RECEIVES JSON RESPONSE
    ├─ Status: 200 OK
    ├─ Content-Type: application/json
    └─ Body: GeoJSON data

11. JAVASCRIPT PROCESSES DATA
    ├─ Parse: JSON string → JavaScript object
    ├─ Process: for each feature
    │  ├─ Extract: geometry & properties
    │  ├─ Calculate: completeness color
    │  └─ Create: Leaflet feature
    └─ Add to map: L.geoJSON(data)

12. LEAFLET RENDERS MAP
    ├─ Draw: All polygon boundaries
    ├─ Color: By completeness percentage
    │  ├─ Green: ≥90%
    │  ├─ Yellow: 70-89%
    │  ├─ Orange: 50-69%
    │  └─ Red: <50%
    ├─ Add: Popups on click
    └─ Display: Interactive map

13. USER SEES MAP
    └─ Interactive, fully functional map

14. USER CLICKS ON MUNICIPALITY
    ├─ Browser fires: click event
    ├─ Leaflet triggers: popup
    └─ Shows: Municipality statistics

15. USER INTERACTS
    ├─ Zoom/pan map
    ├─ Toggle layers
    ├─ Click features
    └─ View data
```

---

## Communication Protocols

### HTTP Protocol

```
REQUEST (Browser → Server):
═══════════════════════════════════════════════════════════════

GET /api/geojson-data HTTP/1.1
Host: localhost:5000
Accept: application/json
User-Agent: Mozilla/5.0
Content-Length: 0
Connection: keep-alive

[Empty body for GET]


RESPONSE (Server → Browser):
═══════════════════════════════════════════════════════════════

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 542301
Date: Wed, 28 Jan 2026 12:00:00 GMT
Connection: keep-alive
Cache-Control: max-age=3600

{
  "type": "FeatureCollection",
  "features": [
    { "type": "Feature", "geometry": {...}, "properties": {...} },
    { "type": "Feature", "geometry": {...}, "properties": {...} },
    ...
  ]
}
```

### JSON Data Format

```
JSON = JavaScript Object Notation
├─ Lightweight text format
├─ Humans can read
├─ Easy for machines to parse
├─ Supports: objects, arrays, strings, numbers, booleans
├─ Perfect for API responses
└─ Used for all communication
```

---

## Real Example: Complete Request-Response

### Scenario: User Clicks on Municipality

```
USER ACTION:
═══════════════════════════════════════════════════════════════
User clicks polygon for "Rīga" on map


BROWSER EVENT:
═══════════════════════════════════════════════════════════════
JavaScript onclick handler triggered
├─ Extracts: feature.properties.municipality_name = "Rīga"
├─ Creates: popup content
├─ Shows: "Rīga - Completeness: 249.6%"
└─ Optional: Makes API call for details


OPTIONAL API CALL:
═══════════════════════════════════════════════════════════════
fetch('/api/csv-data?municipality=Rīga')
  .then(res => res.json())
  .then(data => {
    // Update UI with detailed statistics
    updateStatistics(data);
  });


FLASK PROCESSING:
═══════════════════════════════════════════════════════════════
@app.route('/api/csv-data')
def get_csv_data():
    df = load_dataframe()  # Load from cache
    
    # Optionally filter by municipality
    municipality = request.args.get('municipality')
    if municipality:
        df = df[df['municipality_name'] == municipality]
    
    # Convert to JSON
    return jsonify(df.to_dict('records'))


RESPONSE:
═══════════════════════════════════════════════════════════════
{
  "municipality_name": "Rīga",
  "osm_road_km": 2496.0,
  "official_road_km": 1000,
  "road_count": 5400,
  "completeness_pct": 249.6
}


BROWSER UPDATE:
═══════════════════════════════════════════════════════════════
JavaScript receives response
├─ Extracts: statistics from JSON
├─ Updates: HTML elements with data
│  ├─ Municipality name
│  ├─ Road kilometers
│  ├─ Completeness percentage
│  └─ Road count
└─ User sees: Detailed popup with all data


RESULT:
═══════════════════════════════════════════════════════════════
Interactive popup appears showing:

  Rīga
  OSM Roads: 2,496 km
  Official Roads: 1,000 km
  Completeness: 249.6%
  Road Count: 5,400
```

---

## Data Flow Diagram

### Complete Data Movement

```
FILE SYSTEM (Disk)
├─ outputs/exports/latvia_lau1.geojson (20 MB)
├─ outputs/exports/completeness_municipalities.csv (500 KB)
└─ outputs/maps/interactive_map.html (pre-rendered)
       ↓
       │ (On app startup)
       ↓
FLASK APPLICATION (Server Memory)
├─ _geojson_cache (20 MB)
├─ _dataframe_cache (500 KB)
└─ _library_dataframe_cache, etc.
       ↓
       │ (HTTP API Response)
       ↓ (JSON Format)
       │
BROWSER (Client)
├─ JSON data in memory
└─ Display via Leaflet.js
       ↓
USER SEES:
└─ Interactive map with:
   ├─ Color-coded municipalities
   ├─ Popups with data
   ├─ Legend
   └─ Layer toggles
```

---

## Communication Methods

### 1. **Page Load (HTML)**
```
Browser requests:  GET /
Server returns:    HTML page
Purpose:           Initial page display
```

### 2. **AJAX (Asynchronous JavaScript)**
```javascript
fetch('/api/geojson-data')
    .then(res => res.json())
    .then(data => {
        // Use data without reloading page
        console.log(data);
    });
```

**Method**: Asynchronous  
**Purpose**: Load data without page reload  
**Speed**: No page flash, smooth UX  

### 3. **Event Listeners (User Interaction)**
```javascript
map.on('click', function(e) {
    // Handle map click
    // Fetch more data if needed
    // Update UI
});
```

**Triggered by**: User actions (click, zoom, etc.)  
**Purpose**: Responsive interactions  

### 4. **WebSocket (Real-Time) - Optional**
```javascript
// Not currently implemented
// Could use for real-time updates
const socket = new WebSocket('ws://localhost:5000/live');
```

**Future Enhancement**: For live data updates  

---

## Error Handling

### Frontend

```javascript
fetch('/api/geojson-data')
    .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    })
    .then(data => {
        if (!data.features) throw new Error('No features');
        renderMap(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Failed to load data');
    });
```

### Backend

```python
@app.route('/api/geojson-data')
def get_geojson():
    try:
        data = load_geojson()
        if data is None:
            return jsonify({'error': 'Data not found'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

---

## Performance Optimization

### Caching Strategy

```
First Request:
├─ User opens browser
├─ Flask reads file from disk (1-2 seconds)
├─ Store in _geojson_cache
└─ Send to browser

Subsequent Requests:
├─ Use cached data from memory
├─ No disk read needed
├─ Send to browser instantly (50-200ms)
└─ All users benefit from same cache

Cache Invalidation:
├─ Clear cache when data updates
├─ Manual: POST /clear-cache
├─ Or: Restart Flask app
└─ Automatic: Set expiry time
```

### Network Optimization

```
GeoJSON Size Reduction:
├─ Compression: gzip (reduces by 70%)
├─ Current: ~20 MB uncompressed
├─ Compressed: ~6 MB over network
├─ Transmission time: 1-2 seconds (1 Mbps)

Data Format Optimization:
├─ JSON is text (can be large)
├─ Could use: Protocol Buffers, MessagePack
├─ Current: Fine for this project size
└─ Future: Consider if data grows 10x
```

---

## Summary

### Frontend Role
```
Display Data & Handle User Interaction
├─ Render map (Leaflet.js)
├─ Color code by completeness
├─ Handle clicks/zooms
├─ Fetch data from API (AJAX)
└─ Update UI dynamically
```

### Backend Role
```
Store Data & Serve Requests
├─ Provide HTML pages
├─ Serve data via API endpoints
├─ Cache data in memory
├─ Process requests efficiently
└─ Return JSON responses
```

### Communication
```
HTTP Protocol
├─ RESTful API design
├─ GET requests for data
├─ JSON data format
├─ Asynchronous (AJAX)
└─ Error handling
```

---

## Technology Stack Summary

```
Frontend:
├─ HTML5 (markup)
├─ CSS3 + Bootstrap (styling)
├─ JavaScript (interactivity)
├─ Leaflet.js (maps)
├─ jQuery (utilities)
└─ AJAX (communication)

Backend:
├─ Python 3.8+
├─ Flask 2.3.3 (web framework)
├─ Pandas (data processing)
├─ Jinja2 (templates)
└─ JSON (data exchange)

Communication:
├─ HTTP (protocol)
├─ JSON (format)
├─ AJAX (method)
└─ REST (API style)
```

---

**In Short**: Frontend (HTML/JavaScript/Leaflet) displays the map and makes AJAX requests to Backend (Flask/Python) API, which loads cached data and returns JSON responses that Leaflet uses to render the interactive visualization.

