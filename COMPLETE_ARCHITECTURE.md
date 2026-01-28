# Complete Architecture of LatviaOSM-Check Project

**Date**: January 28, 2026  
**Version**: 1.0 - Final

---

## Table of Contents

1. [High-Level System Architecture](#high-level-system-architecture)
2. [Layered Architecture](#layered-architecture)
3. [Component Architecture](#component-architecture)
4. [Data Flow Architecture](#data-flow-architecture)
5. [Processing Pipeline Architecture](#processing-pipeline-architecture)
6. [Web Application Architecture](#web-application-architecture)
7. [Directory Structure & Organization](#directory-structure--organization)
8. [Technology Stack](#technology-stack)
9. [Design Patterns](#design-patterns)
10. [Scalability & Deployment Architecture](#scalability--deployment-architecture)

---

## High-Level System Architecture

### System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    LatviaOSM-Check System                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  OpenStreetMap    Official Statistics    Municipality Boundaries │
│  (OSM PBF)        (CSV Files)           (GeoJSON)                │
│  ~200 MB          ~2 MB                 ~5 MB                    │
│                                                                   │
└────────────────┬──────────────────────┬──────────────────────────┘
                 │                      │
                 ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                               │
│  (Python Scripts + Processing Modules)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Extract Features → Standardize Data → Spatial Join             │
│  Calculate Completeness → Generate Outputs                      │
│                                                                  │
│  20 Pipeline Scripts (00-99)                                   │
│  6 Processing Modules (src/processing/)                         │
│                                                                  │
└────────────────┬──────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA PRODUCTS                                  │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  ┌────────┐ │
│  │   CSV       │  │  GeoJSON    │  │ Interactive  │  │ Flask  │ │
│  │   Files     │  │  Exports    │  │   HTML Maps  │  │  API   │ │
│  │  (Tabular)  │  │ (Spatial)   │  │  (Leaflet)   │  │(JSON)  │ │
│  └─────────────┘  └─────────────┘  └──────────────┘  └────────┘ │
│                                                                  │
│  outputs/exports/    outputs/exports/    outputs/maps/   app.py │
│                                                                  │
└────────────────┬──────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                  WEB APPLICATION (Flask)                         │
│                                                                  │
│  HTTP Routes ──→ Data Loading ──→ Caching ──→ Responses        │
│  /                                                               │
│  /roads         GeoJSON Loader  In-memory      JSON API        │
│  /forests       CSV Loader      Caching        HTML Pages      │
│  /libraries     Data Processing                Error Handling   │
│  /combined-map                                                   │
│  /api/*                                                          │
│                                                                  │
│  Templates: Leaflet.js + Bootstrap + HTML5                     │
│                                                                  │
└────────────────┬──────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    END USERS                                     │
│                                                                  │
│  Web Browser ──→ Interactive Maps ──→ API Clients              │
│  (Chrome, FF)    (GIS Visualization)  (Python, R, JS)          │
│  http://localhost:5000                Custom Applications       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layered Architecture

### 7-Layer Architecture Model

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 7: USER INTERFACE LAYER                              │
│  ├─ Web Browser (Leaflet.js Maps)                          │
│  ├─ API Consumers (Python, R, JavaScript)                  │
│  └─ GIS Applications (QGIS)                                │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ HTTP/JSON
┌─────────────────────────────────────────────────────────────┐
│  LAYER 6: PRESENTATION LAYER (Flask Templates)              │
│  ├─ HTML Templates (dynamic_map.html, with_dropdown.html)  │
│  ├─ Leaflet.js Integration (Interactive Maps)              │
│  ├─ Bootstrap Styling (Responsive Design)                  │
│  └─ Error Handling & Status Pages                          │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ Python Objects
┌─────────────────────────────────────────────────────────────┐
│  LAYER 5: APPLICATION LAYER (Flask Web App)                 │
│  ├─ Route Handlers (@app.route)                            │
│  ├─ RESTful API Endpoints (/api/*)                         │
│  ├─ Request Processing & Validation                        │
│  ├─ Response Formatting (JSON, HTML)                       │
│  └─ Error Handling & Logging                               │
│                                                             │
│  Key Components: app.py (328 lines)                        │
│  - / (main page)                                           │
│  - /roads, /forests, /libraries, /combined-map             │
│  - /api/geojson-data, /api/csv-data, etc.                 │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ Processed Data
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: CACHING & OPTIMIZATION LAYER                      │
│  ├─ In-Memory Caching (Global Variables)                   │
│  ├─ _geojson_cache (Geographic Features)                  │
│  ├─ _dataframe_cache (Tabular Data)                        │
│  ├─ _forest_dataframe_cache, _library_dataframe_cache     │
│  ├─ Cache Invalidation & Refresh Logic                     │
│  └─ Performance Optimization                               │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ Loaded Data
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: DATA LOADING & PROCESSING LAYER                   │
│  ├─ Data Loaders (load_geojson, load_dataframe, etc.)      │
│  ├─ GeoPandas Integration (Spatial Operations)             │
│  ├─ Pandas DataFrame Processing (Aggregation, Filtering)  │
│  ├─ File I/O (JSON, CSV)                                  │
│  ├─ Data Transformation & Enrichment                       │
│  └─ Processing Modules (src/processing/)                   │
│                                                             │
│  Key Modules:                                              │
│  - create_fuzzy_mapping.py (Latvian name matching)        │
│  - generate_corrected_completeness.py (Metrics)           │
│  - generate_quality_report.py (Analysis)                  │
│  - get_stats.py (Aggregation)                             │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ Raw/Processed Files
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: DATA STORAGE LAYER                                │
│  ├─ File-Based Storage                                     │
│  ├─ GeoJSON Files (Geography + Attributes)                 │
│  ├─ CSV Files (Tabular Data)                               │
│  ├─ HTML Maps (Pre-rendered Visualizations)                │
│  ├─ Directory Organization:                                │
│  │  data/raw/ (Original Data - 700+ MB)                   │
│  │  data/processed/ (Cleaned Data - 50 MB)                │
│  │  outputs/exports/ (Results - 20 MB)                    │
│  │  outputs/maps/ (Visualizations - HTML)                 │
│  └─ Metadata & Configuration                              │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ Source Data
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: DATA SOURCE LAYER                                 │
│  ├─ External Sources:                                       │
│  │  ├─ OpenStreetMap (PBF Format) - ~200 MB               │
│  │  ├─ Government Statistics (CSV) - ~2 MB                │
│  │  └─ Geographic Boundaries (GeoJSON) - ~5 MB            │
│  ├─ Data Quality:                                          │
│  │  ├─ OSM: Community-contributed, dynamic                │
│  │  ├─ Official: Authoritative reference data             │
│  │  └─ Boundaries: Official administrative divisions      │
│  └─ Update Frequency:                                      │
│     ├─ OSM: Real-time (updated continuously)              │
│     ├─ Official: Annual updates                           │
│     └─ Analysis: Monthly or on-demand                     │
└─────────────────────────────────────────────────────────────┘
```

### Layer Dependencies & Data Flow

```
User Interaction (Layer 7)
        ▼
Browser Request (HTTP)
        ▼
Flask Routes & Validation (Layer 5)
        ▼
Cache Check (Layer 4)
        ├─ Cache Hit → Return Cached Data
        └─ Cache Miss ↓
          Data Loader (Layer 3)
                ▼
          File System (Layer 2)
                ▼
          Process & Enrich Data (Layer 3)
                ▼
          Store in Cache (Layer 4)
                ▼
Format Response (Layer 5-6)
        ▼
Render/Serialize (Layer 6)
        ▼
Send to Browser (Layer 7)
        ▼
Display in UI
```

---

## Component Architecture

### Core Components

```
LatviaOSM-Check System Components
═════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────┐
│ 1. DATA ACQUISITION COMPONENT                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Responsibility: Fetch and validate data from external sources  │
│                                                                 │
│ Subcomponents:                                                 │
│  ├─ OSM Fetcher                                               │
│  │  ├─ Input: Bounding box for Latvia                        │
│  │  ├─ Source: OSM API / PBF downloads                       │
│  │  ├─ Format: PBF (Protocol Buffer Binary)                  │
│  │  └─ Output: romania-latest.osm.pbf (~200 MB)            │
│  │                                                             │
│  ├─ Statistics Loader                                         │
│  │  ├─ Input: CSV files from gov.lv                         │
│  │  ├─ Files: Road.csv, Forest.csv, Library.csv             │
│  │  └─ Output: Standardized statistics data                 │
│  │                                                             │
│  └─ Boundary Loader                                           │
│     ├─ Input: Municipality boundaries GeoJSON               │
│     ├─ Features: 42 administrative divisions                │
│     └─ Output: Validated boundary geometries                │
│                                                                 │
│ Technologies: requests, urllib, geopandas.read_file()        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ 2. DATA PROCESSING PIPELINE COMPONENT                          │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Responsibility: Transform raw data → analyzable information    │
│                                                                 │
│ 20 Sequential Processing Steps (Scripts 00-99):               │
│                                                                 │
│ Stage 1: Extraction (Scripts 02, 11, 21)                      │
│  ├─ Extract Roads from OSM                                   │
│  ├─ Extract Forests from OSM                                 │
│  └─ Extract Libraries from OSM                               │
│                                                                 │
│ Stage 2: Standardization (Scripts 00, 03)                    │
│  ├─ Convert Official Statistics format                       │
│  └─ Process Municipality Boundaries                          │
│                                                                 │
│ Stage 3: Spatial Operations (Scripts 04, 12, 22)             │
│  ├─ Spatial Join: Roads + Municipalities                     │
│  ├─ Spatial Join: Forests + Municipalities                   │
│  └─ Spatial Join: Libraries + Municipalities                 │
│                                                                 │
│ Stage 4: Completeness Calculation (Scripts 05, 13, 23)       │
│  ├─ Calculate Road Completeness (%)                          │
│  ├─ Calculate Forest Completeness (%)                        │
│  └─ Calculate Library Completeness (%)                       │
│                                                                 │
│ Stage 5: Output Generation (Scripts 07, 17, 27, 99)          │
│  ├─ Generate Interactive Maps (HTML)                         │
│  ├─ Export Data (CSV, GeoJSON)                              │
│  └─ Create Comprehensive Exports                             │
│                                                                 │
│ Processing Modules (src/processing/):                         │
│  ├─ create_fuzzy_mapping.py (Name matching)                 │
│  ├─ generate_corrected_completeness.py (Metrics)            │
│  ├─ generate_quality_report.py (Reports)                    │
│  └─ get_stats.py (Aggregations)                             │
│                                                                 │
│ Key Technologies:                                              │
│  ├─ GeoPandas 0.13.2 (Geospatial operations)                │
│  ├─ Shapely 2.0.1 (Geometry operations)                     │
│  ├─ Pandas 2.0.3 (Tabular data)                            │
│  ├─ Fiona 1.9.4 (GeoJSON I/O)                              │
│  └─ FuzzyWuzzy (String matching)                             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ 3. DATA STORAGE COMPONENT                                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Responsibility: Organize and store data at various stages      │
│                                                                 │
│ Storage Layers:                                                │
│                                                                 │
│ Raw Data Layer (data/raw/):                                   │
│  ├─ latvia-latest.osm.pbf (~200 MB) [.gitignore]            │
│  ├─ Road.csv, Forest.csv, Library.csv (~2 MB)              │
│  └─ municipalities.geojson (~5 MB)                          │
│                                                                 │
│ Processed Data Layer (data/processed/):                       │
│  ├─ roads.geojson (~30 MB)                                 │
│  ├─ forests.geojson (~10 MB)                               │
│  ├─ libraries.geojson (~5 MB)                              │
│  ├─ *_by_municipality.geojson                              │
│  └─ Cleaned, validated geometries                          │
│                                                                 │
│ Output Layer (outputs/):                                      │
│  ├─ Exports (outputs/exports/):                            │
│  │  ├─ completeness_*.csv (Metrics)                        │
│  │  ├─ latvia_lau1.geojson (Final spatial)                │
│  │  └─ *_stats_by_novads.csv (Regional analysis)          │
│  │                                                             │
│  └─ Maps (outputs/maps/):                                  │
│     ├─ combined_map.html (Multi-layer)                     │
│     ├─ library_completeness_map.html                       │
│     └─ interactive_map.html (Roads)                        │
│                                                                 │
│ File Formats:                                                  │
│  ├─ GeoJSON: Spatial data + attributes                      │
│  ├─ CSV: Tabular data for analysis                         │
│  ├─ HTML: Pre-rendered interactive maps                     │
│  └─ JSON: API responses                                     │
│                                                                 │
│ Storage Strategy:                                              │
│  ├─ Large files (.gitignore): data/raw/*.pbf               │
│  ├─ Medium files (git tracked): data/processed/             │
│  ├─ Outputs (build artifacts): outputs/                    │
│  └─ Version control: Git (.git/)                           │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ 4. WEB APPLICATION COMPONENT (Flask App)                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Responsibility: HTTP server, API endpoints, web interface      │
│                                                                 │
│ Entry Point: app.py (328 lines)                               │
│                                                                 │
│ Route Handlers:                                                │
│  ├─ GET / → Main interactive map (roads)                    │
│  ├─ GET /roads → Roads completeness map                     │
│  ├─ GET /forests → Forests completeness map                 │
│  ├─ GET /libraries → Libraries completeness map             │
│  └─ GET /combined-map → Multi-layer map                     │
│                                                                 │
│ API Endpoints:                                                 │
│  ├─ GET /api/geojson-data → GeoJSON features               │
│  ├─ GET /api/csv-data → Municipality statistics             │
│  ├─ GET /api/forest-data → Forest metrics                  │
│  ├─ GET /api/library-data → Library metrics                │
│  └─ POST /clear-cache → Cache invalidation                 │
│                                                                 │
│ Caching System:                                                │
│  ├─ _geojson_cache (GeoJSON data)                          │
│  ├─ _dataframe_cache (CSV data)                            │
│  ├─ _forest_dataframe_cache (Forest data)                  │
│  ├─ _library_dataframe_cache (Library data)                │
│  └─ _hierarchy_cache (Hierarchical data)                   │
│                                                                 │
│ Data Loading Functions:                                        │
│  ├─ load_geojson() → Cache or load from disk              │
│  ├─ load_dataframe() → Cache CSV data                     │
│  ├─ load_forest_dataframe()                                │
│  └─ load_library_dataframe()                               │
│                                                                 │
│ Response Formatting:                                           │
│  ├─ HTML: Render Leaflet maps via templates               │
│  ├─ JSON: API responses (application/json)                 │
│  ├─ Error Handling: 404, 500 status codes                  │
│  └─ Logging: Request tracking & debugging                  │
│                                                                 │
│ Technologies:                                                  │
│  ├─ Flask 2.3.3 (Web framework)                            │
│  ├─ Jinja2 (Template engine)                               │
│  ├─ Werkzeug (WSGI application)                            │
│  └─ Leaflet.js (Client-side maps)                          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ 5. FRONTEND VISUALIZATION COMPONENT                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Responsibility: Client-side rendering & user interaction       │
│                                                                 │
│ Technologies:                                                  │
│  ├─ HTML5 (Markup)                                           │
│  ├─ CSS3 (Styling) + Bootstrap (Responsive design)          │
│  ├─ JavaScript (Interactivity)                              │
│  └─ Leaflet.js (Interactive maps)                           │
│                                                                 │
│ Templates (Flask):                                             │
│  ├─ dynamic_map.html (Main map template)                    │
│  ├─ with_dropdown.html (Dropdown-enabled map)              │
│  └─ Base: Leaflet + OpenStreetMap tiles                     │
│                                                                 │
│ Map Features:                                                  │
│  ├─ Base Layer: OpenStreetMap tiles                        │
│  ├─ Feature Layers:                                         │
│  │  ├─ Municipality boundaries (colored by completeness)   │
│  │  ├─ Roads network                                       │
│  │  ├─ Forests polygons                                    │
│  │  └─ Library points                                      │
│  ├─ Color Coding:                                          │
│  │  ├─ 🟢 Green (≥90% completeness)                       │
│  │  ├─ 🟡 Yellow (70-89%)                                 │
│  │  ├─ 🟠 Orange (50-69%)                                 │
│  │  └─ 🔴 Red (<50%)                                       │
│  ├─ Interactivity:                                         │
│  │  ├─ Click → Show statistics popup                       │
│  │  ├─ Zoom/Pan → Navigate                                │
│  │  └─ Layer toggle → Switch views                        │
│  └─ Legend: Completeness ranges                            │
│                                                                 │
│ Data Binding:                                                  │
│  ├─ GeoJSON data from /api/geojson-data                   │
│  ├─ Styling functions (completeness-based coloring)        │
│  ├─ Popup content from feature properties                  │
│  └─ Real-time updates via API                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ 6. CONFIGURATION & DEPLOYMENT COMPONENT                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Responsibility: Environment setup, deployment configuration    │
│                                                                 │
│ Configuration Files:                                           │
│  ├─ pyproject.toml (Project metadata, dependencies)          │
│  ├─ requirements.txt (Python packages)                       │
│  ├─ .gitignore (Version control rules)                       │
│  └─ .vscode/settings.json (IDE configuration)               │
│                                                                 │
│ Setup Scripts:                                                 │
│  ├─ setup.ps1 (Windows setup automation)                    │
│  ├─ run.ps1 (Windows application launcher)                  │
│  ├─ run_forest_pipeline.ps1 (Forest analysis)              │
│  ├─ run_library_pipeline.ps1 (Library analysis)            │
│  └─ run_pipeline.sh (Unix pipeline runner)                 │
│                                                                 │
│ Deployment Targets:                                            │
│  ├─ Development: python app.py (Flask debug)               │
│  ├─ Production: gunicorn -w 4 -b 0.0.0.0:5000 app:app    │
│  ├─ Production (Windows): waitress-serve app:app           │
│  └─ Docker: Dockerfile (containerized deployment)          │
│                                                                 │
│ Environment Variables:                                         │
│  ├─ FLASK_APP=app.py                                        │
│  ├─ FLASK_ENV=production                                    │
│  ├─ PORT=5000 (default)                                    │
│  └─ DEBUG=False (production)                               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Architecture

### End-to-End Data Flow

```
User Request Flow:
══════════════════════════════════════════════════════════════════

1. USER INITIATES REQUEST
   └─ Opens browser → http://localhost:5000/roads
   
2. FLASK ROUTE HANDLER RECEIVES REQUEST
   └─ app.py: @app.route('/roads')
   
3. DATA LOADING & CACHE CHECK
   ├─ Check cache: Is data already in memory?
   │  ├─ Yes → Use cached data (fast)
   │  └─ No → Load from disk (slower, first time)
   │
   ├─ load_geojson():
   │  ├─ Check _geojson_cache
   │  ├─ If None, read outputs/exports/latvia_lau1.geojson
   │  └─ Store in _geojson_cache for future use
   │
   ├─ load_dataframe():
   │  ├─ Check _dataframe_cache
   │  ├─ If None, read outputs/exports/completeness_municipalities.csv
   │  └─ Store in _dataframe_cache
   │
   └─ Data ready in memory
   
4. DATA PROCESSING (if needed)
   ├─ Filter data based on query parameters
   ├─ Aggregate statistics
   ├─ Calculate summary metrics
   └─ Format response
   
5. RESPONSE FORMATTING
   ├─ For HTML request (browser):
   │  ├─ Render template (templates/dynamic_map.html)
   │  ├─ Inject data into Leaflet.js map
   │  ├─ Include CSS styling
   │  └─ Return complete HTML page
   │
   ├─ For API request (JSON):
   │  ├─ Convert data to JSON
   │  ├─ Set headers: Content-Type: application/json
   │  └─ Return JSON response
   │
   └─ Error responses (on failure):
      ├─ 400 Bad Request (invalid parameters)
      ├─ 404 Not Found (file missing)
      ├─ 500 Internal Server Error (processing error)
      └─ Error message with details
   
6. TRANSMISSION TO CLIENT
   ├─ HTTP response headers (status code, content type)
   ├─ Response body (HTML or JSON)
   └─ Compressed if needed (gzip)
   
7. CLIENT-SIDE RENDERING
   ├─ Browser receives HTML
   ├─ JavaScript parses GeoJSON data
   ├─ Leaflet.js renders map
   ├─ Apply color styling (by completeness %)
   ├─ Add popup event listeners
   └─ Display interactive map
   
8. USER INTERACTION
   ├─ Click on feature → Show popup with statistics
   ├─ Zoom/Pan → Navigate the map
   ├─ Layer toggle → Switch between feature types
   └─ Select municipality → Update statistics display

Processing Pipeline Data Flow:
═════════════════════════════════════════════════════════════════

Raw Data (External Sources)
    ↓
[Step 00] Convert Official Statistics
    ├─ Input: CSV files from government
    ├─ Output: Standardized CSV format
    ├─ Script: 00_convert_official_stats.py
    └─ Result: official_*.csv
    
[Step 02] Extract Roads from OSM
    ├─ Input: latvia-latest.osm.pbf (~200 MB)
    ├─ Filter: Features tagged as 'highway'
    ├─ Output: roads.geojson
    ├─ Script: 02_extract_roads.py
    └─ Result: ~98,765 road segments
    
[Step 11] Extract Forests from OSM
    ├─ Input: latvia-latest.osm.pbf
    ├─ Filter: Features tagged as 'landuse=forest'
    ├─ Output: forests.geojson
    ├─ Script: 11_extract_forests.py
    └─ Result: ~1,200 forest polygons
    
[Step 21] Extract Libraries from OSM
    ├─ Input: latvia-latest.osm.pbf
    ├─ Filter: Features tagged as 'amenity=library'
    ├─ Output: libraries.geojson
    ├─ Script: 21_extract_libraries.py
    └─ Result: ~728 library points
    
[Step 03] Process Municipality Boundaries
    ├─ Input: municipalities.geojson
    ├─ Operations:
    │  ├─ Validate geometries
    │  ├─ Convert to EPSG:4326 CRS
    │  ├─ Check for self-intersections
    │  └─ Remove invalid geometries
    ├─ Script: 03_process_municipalities.py
    └─ Output: Cleaned boundaries
    
[Steps 04, 12, 22] Spatial Joins
    ├─ [Step 04] Roads + Municipalities
    │  ├─ Input: roads.geojson + municipalities.geojson
    │  ├─ Operation: gpd.sjoin (predicate='within')
    │  ├─ Each road → municipality assignment
    │  └─ Output: roads_by_municipality.geojson
    │
    ├─ [Step 12] Forests + Municipalities
    │  ├─ Each forest → municipality assignment
    │  └─ Output: forests_by_municipality.geojson
    │
    └─ [Step 22] Libraries + Municipalities
       ├─ Each library → municipality assignment
       └─ Output: libraries_by_municipality.geojson
    
[Steps 05, 13, 23] Calculate Completeness
    ├─ [Step 05] Road Completeness
    │  ├─ Aggregate OSM roads by municipality
    │  ├─ Compare with official statistics
    │  ├─ Formula: (OSM / Official) × 100
    │  └─ Output: completeness_roads.csv
    │
    ├─ [Step 13] Forest Completeness
    │  ├─ Aggregate OSM forests by municipality
    │  ├─ Compare with official statistics
    │  └─ Output: completeness_forests.csv
    │
    └─ [Step 23] Library Completeness
       └─ Output: completeness_libraries.csv
    
[Steps 07, 17, 27] Generate Maps
    ├─ [Step 07] Create Roads Map
    │  ├─ Input: completeness_roads.csv + boundaries
    │  ├─ Technology: Folium + Leaflet.js
    │  ├─ Output: outputs/maps/interactive_map.html
    │  └─ Features: Color-coded by completeness
    │
    ├─ [Step 17] Create Forest Map
    │  └─ Output: outputs/maps/forest_completeness_map.html
    │
    └─ [Step 27] Create Library Map
       └─ Output: outputs/maps/library_completeness_map.html
    
[Step 99] Create Comprehensive Export
    ├─ Input: All processed data
    ├─ Operations:
    │  ├─ Merge all data (roads, forests, libraries)
    │  ├─ Create unified GeoJSON
    │  ├─ Create combined CSV exports
    │  └─ Combine all metrics
    ├─ Outputs:
    │  ├─ latvia_lau1.geojson (Final comprehensive spatial)
    │  ├─ completeness_municipalities.csv (Aggregated metrics)
    │  └─ Additional exports for analysis
    └─ Script: 99_create_comprehensive_geojson.py

Final Output Products
    ├─ outputs/exports/ (Data files)
    │  ├─ *.csv (Tabular analysis)
    │  ├─ *.geojson (Spatial data)
    │  └─ *_report.txt (Quality reports)
    │
    └─ outputs/maps/ (Visualizations)
       ├─ combined_map.html
       ├─ interactive_map.html
       └─ *_completeness_map.html
       
Available for:
    ├─ Web Application (Flask serving files)
    ├─ API Endpoints (JSON responses)
    ├─ GIS Software (QGIS import)
    └─ Data Analysis (Excel, R, Python)
```

---

## Processing Pipeline Architecture

### Pipeline Architecture Pattern

```
PROCESSING PIPELINE PATTERN
═════════════════════════════════════════════════════════════════

Type: Batch Processing Pipeline (ETL - Extract, Transform, Load)

Characteristics:
├─ Sequential execution (Step 0 → Step 99)
├─ Each step is independent (can run individually)
├─ Idempotent (safe to run multiple times)
├─ Modular (easy to add/remove steps)
├─ Traceable (clear input/output at each step)
└─ Reproducible (same input → same output)

Pipeline Stages:
═════════════════

STAGE 1: EXTRACT (Scripts 02, 11, 21)
└─ Extract relevant features from raw data
   ├─ Extract Points (libraries)
   ├─ Extract LineStrings (roads)
   ├─ Extract Polygons (forests)
   └─ Output: GeoJSON with clean geometries

STAGE 2: PREPARE (Scripts 00, 03)
└─ Prepare & standardize all input data
   ├─ Convert official statistics to standard format
   ├─ Validate & clean boundaries
   ├─ Standardize CRS (EPSG:4326)
   └─ Output: Cleaned, standardized data

STAGE 3: JOIN (Scripts 04, 12, 22)
└─ Link features to geographic regions
   ├─ Spatial join (features within municipalities)
   ├─ Attribute assignment
   ├─ Handle edge cases & duplicates
   └─ Output: Features with geographic context

STAGE 4: ANALYZE (Scripts 05, 13, 23)
└─ Calculate completeness metrics
   ├─ Aggregate by municipality
   ├─ Compare with official data
   ├─ Calculate percentages & ratios
   └─ Output: Completeness statistics

STAGE 5: OUTPUT (Scripts 07, 17, 27, 99)
└─ Generate final deliverables
   ├─ Create interactive maps
   ├─ Export to multiple formats
   ├─ Merge & aggregate results
   └─ Output: Maps, CSV, GeoJSON, HTML

Script Numbering Scheme:
═════════════════════════

00-09: Data Preparation
  └─ 00: Convert official stats
  
10-19: Extraction & Processing
  ├─ 02: Extract roads
  ├─ 03: Process municipalities
  ├─ 11: Extract forests
  └─ 21: Extract libraries
  
20-29: Spatial Analysis & Completeness
  ├─ 04: Spatial join (roads)
  ├─ 05: Calculate completeness (roads)
  ├─ 12: Spatial join (forests)
  ├─ 13: Calculate completeness (forests)
  ├─ 22: Spatial join (libraries)
  └─ 23: Calculate completeness (libraries)
  
30-39: Reserved for future features
  
40-89: Visualization & Reporting
  ├─ 07: Create roads map
  ├─ 17: Create forests map
  ├─ 27: Create libraries map
  └─ 18: Create combined map
  
90-99: Utilities & Comprehensive Exports
  └─ 99: Create comprehensive exports

Processing Order:
═════════════════

1. [00] Convert official stats
           ↓
2. [02] Extract roads
   [11] Extract forests        (parallel)
   [21] Extract libraries      (parallel)
           ↓
3. [03] Process municipalities
           ↓
4. [04] Spatial join roads
   [12] Spatial join forests   (parallel)
   [22] Spatial join libraries (parallel)
           ↓
5. [05] Calculate completeness (roads)
   [13] Calculate completeness (forests)  (parallel)
   [23] Calculate completeness (libraries) (parallel)
           ↓
6. [07] Create roads map
   [17] Create forests map     (parallel)
   [27] Create libraries map   (parallel)
   [18] Create combined map
           ↓
7. [99] Create comprehensive exports
           ↓
COMPLETE → Output ready for web app

Data Dependencies Graph:
═════════════════════════

OSM PBF ────→ [02] Extract Roads
            → [11] Extract Forests
            → [21] Extract Libraries
                        ↓
                  Combined with ↓
Boundaries ─────→ [03] Process Municipalities
                        ↓
                    [04, 12, 22] Spatial Joins
                        ↓
                    Feature datasets with
                    municipality context
                        ↓
Official Stats ─→ [05, 13, 23] Completeness Calc
                        ↓
                    Metrics with statistics
                        ↓
        [07, 17, 27, 18] Map Generation
        [99] Final Exports
                        ↓
        Outputs ready for web app/API
```

---

## Web Application Architecture

### Flask Application Structure

```
Flask Application Architecture
════════════════════════════════════════════════════════════════

app.py (328 lines) - Main Entry Point
├─ Imports
│  ├─ Flask framework
│  ├─ Data processing (pandas, geopandas)
│  ├─ File I/O (json, pathlib)
│  └─ Utils
│
├─ Configuration
│  ├─ ROOT = project root directory
│  ├─ MAP_HTML = path to map files
│  ├─ GEOJSON_FILE = path to geographic data
│  ├─ CSV_FILE = path to tabular data
│  └─ Similar for forest, library files
│
├─ Cache Layer
│  ├─ _geojson_cache
│  ├─ _hierarchy_cache
│  ├─ _dataframe_cache
│  ├─ _forest_dataframe_cache
│  ├─ _library_dataframe_cache
│  └─ clear_cache() function
│
├─ Data Loaders
│  ├─ load_geojson()
│  │  ├─ Check cache
│  │  ├─ Load from disk if needed
│  │  └─ Return geographic features
│  │
│  ├─ load_dataframe()
│  │  ├─ Load CSV file
│  │  ├─ Parse with pandas
│  │  └─ Cache for subsequent requests
│  │
│  ├─ load_forest_dataframe()
│  ├─ load_library_dataframe()
│  └─ Similar pattern
│
├─ Route Handlers
│  ├─ @app.route('/')
│  │  └─ Render main interactive map
│  │
│  ├─ @app.route('/roads')
│  │  └─ Render roads completeness map
│  │
│  ├─ @app.route('/forests')
│  │  └─ Render forests completeness map
│  │
│  ├─ @app.route('/libraries')
│  │  └─ Render libraries completeness map
│  │
│  └─ @app.route('/combined-map')
│     └─ Render multi-layer map
│
├─ API Endpoints
│  ├─ @app.route('/api/geojson-data', methods=['GET'])
│  │  ├─ Load GeoJSON
│  │  ├─ Return JSON response
│  │  └─ Status: 200 OK or error
│  │
│  ├─ @app.route('/api/csv-data', methods=['GET'])
│  │  ├─ Load CSV data
│  │  ├─ Convert to list of dicts
│  │  └─ Return as JSON
│  │
│  ├─ @app.route('/api/forest-data', methods=['GET'])
│  ├─ @app.route('/api/library-data', methods=['GET'])
│  └─ Similar pattern
│
├─ Utility Functions
│  ├─ get_summary_stats(data) - Aggregate statistics
│  ├─ format_response(data, format) - Format output
│  ├─ validate_input(params) - Input validation
│  └─ error_handler(error) - Error handling
│
└─ Error Handling
   ├─ @app.errorhandler(404) - File not found
   ├─ @app.errorhandler(500) - Server error
   ├─ Try-except blocks in loaders
   └─ Logging for debugging

Request Flow:
═════════════

User Browser Request
        ↓
Routed by Flask Router
        ↓
Match to Route Handler
        ↓
Execute Route Function
        ├─ Call data loaders
        ├─ Check cache
        ├─ Load from disk if needed
        ├─ Process data (if needed)
        ├─ Format response
        ├─ Set headers
        └─ Return response
        ↓
Flask sends HTTP response
        ↓
Browser receives & renders
        ↓
User sees interactive map/data

Response Types:
═══════════════

HTML Response (Routes):
├─ Content-Type: text/html
├─ Body: Complete HTML page
├─ Template rendering via Jinja2
└─ Includes embedded Leaflet.js map

JSON Response (API):
├─ Content-Type: application/json
├─ Body: JSON-serialized data
├─ Standard JSON structure
└─ Parseable by any client

Error Response:
├─ Status: 400, 404, 500, etc.
├─ Content-Type: application/json
├─ Body: Error message & details
└─ Stack trace (development mode)
```

---

## Directory Structure & Organization

### Complete Directory Tree with Roles

```
latvia_osm_project/
│
├── 📄 ROOT LEVEL DOCUMENTATION (4 files)
│   ├── README.md                      # Main project guide
│   ├── LICENSE                        # MIT License
│   ├── CHANGELOG.md                   # Version history
│   ├── CONTRIBUTING.md                # Contribution guidelines
│   ├── CONTRIBUTORS.md                # Author list
│   ├── CODE_OF_CONDUCT.md             # Community standards
│   └── [EXAM files created for studying]
│       ├── EXAM_QUESTIONS_ANSWERS.md
│       ├── DATA_FLOW_DIAGRAM_EXPLANATION.md
│       └── COMPLETE_ARCHITECTURE.md
│
├── 🎛️ CONFIGURATION FILES (5 files)
│   ├── app.py                         # Main Flask application (328 lines)
│   ├── pyproject.toml                 # Project metadata
│   ├── requirements.txt                # Python dependencies (20+ packages)
│   ├── .gitignore                     # Git ignore rules
│   └── .vscode/settings.json          # IDE configuration
│
├── 🚀 STARTUP SCRIPTS (4 files)
│   ├── setup.ps1                      # Windows setup automation
│   ├── run.ps1                        # Windows application launcher
│   ├── run_forest_pipeline.ps1        # Forest processing script
│   ├── run_library_pipeline.ps1       # Library processing script
│   └── run_pipeline.sh                # Unix pipeline runner
│
├── 📚 DOCUMENTATION (docs/ - 10 files)
│   ├── README.md                      # Docs overview
│   ├── INSTALLATION.md                # Setup instructions
│   ├── USAGE.md                       # User guide
│   ├── API.md                         # API documentation
│   ├── DEVELOPMENT.md                 # Developer guide
│   ├── PROJECT_STRUCTURE.md           # This file structure
│   ├── QUICK_GUIDE.md                 # 5-min quick start
│   ├── FINAL_STATUS.md                # Project status
│   ├── LIBRARY_ANALYSIS.md            # Library analysis docs
│   └── IMPLEMENTATION_SUMMARY_NOVADS.md
│
├── 🐍 SOURCE CODE (src/ - reusable modules)
│   ├── __init__.py
│   └── processing/
│       ├── create_fuzzy_mapping.py              # Fuzzy name matching
│       ├── create_library_fuzzy_mapping.py      # Library-specific matching
│       ├── generate_corrected_completeness.py   # Roads completeness
│       ├── generate_library_corrected_completeness.py  # Library completeness
│       ├── generate_forest_corrected_completeness.py   # Forest completeness
│       ├── generate_quality_report.py           # Quality reports
│       └── get_stats.py                         # Statistics aggregation
│
├── 🔧 PIPELINE SCRIPTS (scripts/ - 20 numbered files)
│   ├── 00_convert_official_stats.py             # [STEP 0] Standardize data
│   ├── 02_extract_roads.py                      # [STEP 2] Extract roads
│   ├── 03_process_municipalities.py             # [STEP 3] Process boundaries
│   ├── 04_spatial_join.py                       # [STEP 4] Join roads→municipalities
│   ├── 05_calculate_completeness.py             # [STEP 5] Calculate metrics
│   ├── 07_create_interactive_map.py             # [STEP 7] Generate maps
│   ├── 08_create_lau1_map.py                    # [STEP 8] LAU1 maps
│   ├── 10_convert_forest_stats.py               # [STEP 10] Convert forest stats
│   ├── 10_convert_library_stats.py              # [STEP 10] Convert library stats
│   ├── 11_extract_forests.py                    # [STEP 11] Extract forests
│   ├── 12_forest_spatial_join.py                # [STEP 12] Join forests
│   ├── 13_calculate_forest_completeness.py      # [STEP 13] Forest metrics
│   ├── 17_create_forest_map.py                  # [STEP 17] Forest maps
│   ├── 18_create_combined_map.py                # [STEP 18] Combined map
│   ├── 21_extract_libraries.py                  # [STEP 21] Extract libraries
│   ├── 22_library_spatial_join.py               # [STEP 22] Join libraries
│   ├── 23_calculate_library_completeness.py     # [STEP 23] Library metrics
│   ├── 27_create_library_map.py                 # [STEP 27] Library maps
│   ├── 99_create_comprehensive_geojson.py       # [STEP 99] Final exports
│   └── run_pipeline.sh                          # Unix runner
│
├── 🌐 TEMPLATES (templates/ - Flask HTML)
│   ├── dynamic_map.html                         # Interactive map template
│   ├── with_dropdown.html                       # Map with dropdown selector
│   └── Base: Leaflet.js + Bootstrap + HTML5
│
├── 📊 DATA (data/ - mostly .gitignore)
│   ├── raw/
│   │   ├── latvia-latest.osm.pbf               # OSM data (~200 MB) [.gitignore]
│   │   ├── municipalities.geojson              # 42 administrative boundaries
│   │   ├── Road.csv                            # Official road statistics
│   │   ├── Forest.csv                          # Official forest statistics
│   │   ├── Library.csv                         # Official library statistics
│   │   ├── official_road_stats.csv
│   │   ├── official_forest_stats.csv
│   │   ├── official_library_stats.csv
│   │   ├── railway_data.csv
│   │   └── TRS020_*.csv                        # Tax register data
│   │
│   └── processed/
│       ├── municipalities.geojson               # Cleaned boundaries
│       ├── roads.geojson                        # All roads (~30 MB) [.gitignore]
│       ├── roads_by_municipality.geojson        # Roads with municipality context
│       ├── roads_by_novads.geojson             # Roads by region
│       ├── forests.geojson                      # All forests (~10 MB) [.gitignore]
│       ├── forests_by_municipality.geojson     # Forests with context
│       ├── forests_by_novads.geojson          # Forests by region
│       ├── libraries.geojson                    # All libraries (~5 MB)
│       ├── libraries_by_municipality.geojson   # Libraries with context
│       └── libraries_by_novads.geojson        # Libraries by region
│
├── 📈 OUTPUTS (outputs/ - generated files)
│   ├── exports/
│   │   ├── latvia_lau1.geojson                 # Final spatial + data
│   │   ├── latvia_lau1_forests.geojson        # Forest data
│   │   ├── completeness_municipalities.csv     # Road completeness metrics
│   │   ├── completeness_forests.csv           # Forest metrics
│   │   ├── completeness_libraries.csv         # Library metrics
│   │   ├── forest_stats_by_novads.csv        # Regional forest stats
│   │   ├── library_stats_by_novads.csv       # Regional library stats
│   │   ├── forest_completeness_report.txt     # Analysis report
│   │   └── forest_completeness_full_report.txt # Detailed report
│   │
│   └── maps/
│       ├── combined_map.html                   # Roads + Forests + Libraries
│       ├── interactive_map.html                # Roads (main map)
│       ├── library_completeness_map.html      # Libraries visualization
│       └── forest_completeness_map.html       # Forests visualization
│
├── .git/                                        # Git version control
├── .venv/                                       # Python virtual environment
└── __pycache__/                                 # Python bytecode cache
```

### File Size Reference

```
Data Storage Summary:
════════════════════════════════════════════════════════════════

Raw Data (data/raw/):
  latvia-latest.osm.pbf           ~200 MB (not in git)
  municipalities.geojson            ~5 MB
  *.csv (Road, Forest, Library)      ~2 MB
  Other data files                   ~1 MB
  ─────────────────────────────────────
  Subtotal:                        ~208 MB

Processed Data (data/processed/):
  roads.geojson                    ~30 MB
  forests.geojson                  ~10 MB
  libraries.geojson                 ~5 MB
  *_by_municipality.geojson         ~3 MB
  ─────────────────────────────────────
  Subtotal:                         ~50 MB

Outputs (outputs/):
  *.csv files                        ~3 MB
  *.geojson exports                 ~5 MB
  HTML maps                          ~5 MB
  Reports & logs                     ~7 MB
  ─────────────────────────────────────
  Subtotal:                         ~20 MB

Codebase (src/, scripts/, templates/):
  Python scripts                     ~2 MB
  HTML templates                     ~0.2 MB
  Documentation                      ~3 MB
  ─────────────────────────────────────
  Subtotal:                         ~5.2 MB

TOTAL WITH EVERYTHING:           ~283+ MB
TOTAL IN GIT:                     ~83 MB (large files excluded)
```

---

## Technology Stack

### Complete Technology Stack

```
TECHNOLOGY STACK
════════════════════════════════════════════════════════════════

LANGUAGE
├─ Python 3.8+
│  ├─ Cross-platform support
│  ├─ Rich ecosystem for geospatial work
│  └─ Easy to learn & maintain
│
└─ JavaScript (Client-side)
   ├─ Leaflet.js map interactivity
   └─ HTML5/CSS3 rendering

WEB FRAMEWORK
├─ Flask 2.3.3
│  ├─ Lightweight WSGI framework
│  ├─ Perfect for small-to-medium projects
│  ├─ Built-in development server
│  ├─ Jinja2 template engine
│  └─ Blueprints for modularity
│
└─ Werkzeug (underlying WSGI server)

GEOSPATIAL PROCESSING
├─ GeoPandas 0.13.2
│  ├─ Geographic DataFrames
│  ├─ Spatial operations
│  ├─ Shapefile/GeoJSON I/O
│  └─ Coordinate transformations
│
├─ Shapely 2.0.1
│  ├─ Geometry objects
│  ├─ Geometric operations
│  ├─ WKT/WKB support
│  └─ Spatial predicates
│
├─ Fiona 1.9.4
│  ├─ GeoJSON/Shapefile I/O
│  ├─ OGR/GDAL wrapper
│  └─ Streaming data access
│
├─ PyOGRIO 0.7.2
│  ├─ Low-level GDAL wrapper
│  ├─ High-performance I/O
│  └─ Alternative to Fiona
│
└─ GDAL/OGR (system dependency)
   ├─ Geospatial data translation
   ├─ Raster & vector support
   └─ Format conversions

DATA PROCESSING
├─ Pandas 2.0.3
│  ├─ Tabular data manipulation
│  ├─ CSV reading/writing
│  ├─ DataFrame operations
│  ├─ Aggregation & grouping
│  └─ Statistical analysis
│
└─ NumPy (Pandas dependency)
   ├─ Numerical arrays
   ├─ Mathematical operations
   └─ Performance optimization

STRING MATCHING
├─ FuzzyWuzzy
│  ├─ Fuzzy string matching
│  ├─ Latvian language support
│  ├─ Similarity scoring
│  └─ Token-based matching
│
└─ python-Levenshtein (optional)
   ├─ Performance improvement
   └─ Distance calculations

FRONTEND VISUALIZATION
├─ Leaflet.js 1.9+
│  ├─ Interactive maps
│  ├─ Open-source mapping
│  ├─ GeoJSON rendering
│  ├─ Popups & tooltips
│  ├─ Layer control
│  └─ Lightweight & modular
│
├─ OpenStreetMap Tiles
│  ├─ Free base layer
│  ├─ Raster tiles
│  └─ World coverage
│
├─ Bootstrap 5
│  ├─ Responsive CSS framework
│  ├─ Mobile-friendly
│  └─ UI components
│
└─ HTML5 + CSS3
   ├─ Semantic markup
   └─ Modern styling

DATA FORMATS
├─ GeoJSON (RFC 7946)
│  ├─ Geographic features + attributes
│  ├─ JSON-based format
│  ├─ Web-friendly
│  └─ Text-based (editable)
│
├─ CSV (RFC 4180)
│  ├─ Tabular data
│  ├─ Spreadsheet-compatible
│  └─ Text-based (portable)
│
├─ OSM PBF
│  ├─ OpenStreetMap binary format
│  ├─ Compressed (~200 MB for Latvia)
│  └─ Efficient parsing
│
├─ Shapefile
│  ├─ Traditional GIS format
│  ├─ Binary + associated files
│  └─ Wide tool support
│
├─ JSON
│  ├─ API responses
│  ├─ Configuration files
│  └─ Human-readable
│
└─ HTML
   ├─ Map templates
   ├─ Web pages
   └─ Interactive content

DEVELOPMENT TOOLS
├─ Git
│  ├─ Version control
│  └─ Collaboration
│
├─ Virtual Environment (venv)
│  ├─ Python isolation
│  ├─ Dependency management
│  └─ Reproducible setup
│
├─ pip
│  ├─ Package management
│  └─ Dependency resolution
│
├─ VS Code
│  ├─ IDE/editor
│  ├─ Python extension
│  └─ Git integration
│
└─ Command Line Tools
   ├─ PowerShell (Windows)
   ├─ Bash (Unix/macOS)
   └─ GDAL utilities

DEPLOYMENT OPTIONS
├─ Development
│  └─ Flask development server
│
├─ Production (Gunicorn)
│  └─ Multi-worker WSGI
│
├─ Production (Waitress)
│  └─ Windows-friendly WSGI
│
├─ Docker
│  ├─ Containerization
│  └─ Environment isolation
│
├─ Cloud Platforms
│  ├─ Heroku
│  ├─ AWS (EC2, Lambda)
│  ├─ Azure
│  └─ Google Cloud
│
└─ Reverse Proxy
   └─ Nginx, Apache

TESTING (Optional)
├─ pytest
│  ├─ Testing framework
│  ├─ Fixture support
│  └─ Parametrization
│
├─ pytest-cov
│  ├─ Code coverage
│  └─ Coverage reports
│
└─ Mock libraries
   ├─ Unit testing
   └─ Dependency mocking

VERSION COMPATIBILITY
═════════════════════

Python:           3.8 - 3.12+
Flask:            2.3.3
GeoPandas:        0.13.2
Pandas:           2.0.3
Shapely:          2.0.1
Fiona:            1.9.4
Leaflet.js:       1.9+
Bootstrap:        5.x
```

---

## Design Patterns

### Architectural Patterns Used

```
DESIGN PATTERNS IN LatviaOSM-Check
═══════════════════════════════════════════════════════════════

1. PIPELINE PATTERN
   ├─ Use: Data processing flow
   ├─ Implementation: Scripts 00-99 (sequential processing)
   ├─ Benefit: Clear data transformation stages
   ├─ Example:
   │  OSM → Extract → Standardize → Join → Calculate → Output
   │
   └─ Code Location: scripts/ directory
       
2. REPOSITORY PATTERN
   ├─ Use: Data storage abstraction
   ├─ Implementation: data/ directory structure
   ├─ Benefits:
   │  ├─ Centralized data storage
   │  ├─ Easy to swap storage backends
   │  └─ Version control integration
   │
   └─ Files: data/raw/, data/processed/

3. CACHING PATTERN
   ├─ Use: Performance optimization
   ├─ Implementation: Global cache variables in app.py
   │  ├─ _geojson_cache
   │  ├─ _dataframe_cache
   │  └─ _*_cache variables
   │
   ├─ Benefits:
   │  ├─ Reduced disk I/O
   │  ├─ Faster API responses
   │  ├─ Lower memory overhead
   │  └─ Automatic invalidation
   │
   └─ Code:
       def load_geojson():
           global _geojson_cache
           if _geojson_cache is None:
               _geojson_cache = load_from_disk()
           return _geojson_cache

4. FACADE PATTERN
   ├─ Use: Simplify complex operations
   ├─ Implementation: Flask routes abstract complexity
   │  ├─ /api/geojson-data → Load + format + cache
   │  ├─ Route handles all complexity
   │  └─ Client sees simple interface
   │
   └─ Benefits:
       ├─ Reduced client complexity
       └─ Implementation hiding

5. MODULE PATTERN
   ├─ Use: Organize reusable code
   ├─ Implementation: src/processing/ modules
   │  ├─ create_fuzzy_mapping.py (specific purpose)
   │  ├─ generate_corrected_completeness.py
   │  ├─ generate_quality_report.py
   │  └─ get_stats.py
   │
   ├─ Benefits:
   │  ├─ Code reuse
   │  ├─ Single responsibility
   │  └─ Easy to test
   │
   └─ Import Pattern:
       from src.processing.create_fuzzy_mapping import \
           create_municipality_mapping

6. MVC PATTERN (Partial)
   ├─ Use: Web application structure
   ├─ Model: GeoJSON/CSV data files
   ├─ View: HTML templates (Flask Jinja2)
   ├─ Controller: Flask routes (app.py)
   │
   └─ Request Flow:
       Route Handler (C) → Load Data (M) → Render Template (V)

7. DECORATOR PATTERN
   ├─ Use: Flask route decoration
   ├─ Implementation: @app.route decorators
   │
   ├─ Example:
   │  @app.route('/api/geojson-data')
   │  def get_geojson():
   │      return jsonify(load_geojson())
   │
   └─ Benefits:
       ├─ Clean, readable code
       └─ Separation of concerns

8. LAZY LOADING PATTERN
   ├─ Use: Defer expensive operations
   ├─ Implementation: Cache loaders
   │
   ├─ Example:
   │  # Load only when first needed
   │  data = load_geojson()  # Loaded once
   │  # Subsequent calls return from cache
   │
   └─ Benefits:
       ├─ Faster startup time
       ├─ Reduced initial memory
       └─ On-demand loading

9. SINGLETON PATTERN
   ├─ Use: Ensure single instance
   ├─ Implementation: Flask app object
   │
   ├─ Code:
   │  app = Flask(__name__)  # Single instance
   │  # All requests use same app object
   │
   └─ Benefits:
       ├─ Consistent state
       └─ Global access

10. FILTER PATTERN
    ├─ Use: Data filtering & selection
    ├─ Implementation: API query parameters
    │
    ├─ Example:
    │  /api/geojson-data?municipality=Rīga&completeness>=70
    │
    └─ Benefits:
        ├─ Client-side customization
        └─ Reduced data transfer

Code Quality Patterns:
═══════════════════════

├─ DRY (Don't Repeat Yourself)
│  └─ Shared utility functions in src/processing/
│
├─ SOLID Principles
│  ├─ Single Responsibility (each script/module has one job)
│  ├─ Open/Closed (easy to extend, hard to break)
│  ├─ Liskov Substitution (consistent interfaces)
│  ├─ Interface Segregation (small focused APIs)
│  └─ Dependency Inversion (depend on abstractions)
│
├─ Clean Code Practices
│  ├─ Meaningful variable names
│  ├─ Function documentation strings
│  ├─ Error handling
│  └─ Consistent formatting
│
└─ Type Hints (Python 3.8+)
   ├─ Optional in codebase
   ├─ Improves code clarity
   └─ Enables IDE autocompletion
```

---

## Scalability & Deployment Architecture

### Scalability Patterns

```
CURRENT ARCHITECTURE (Single Server)
════════════════════════════════════════════════════════════════

┌─────────────────────────────────────┐
│      Single Server Instance          │
├─────────────────────────────────────┤
│                                      │
│  ┌─ Flask Application (4 processes) │
│  │  ├─ Process 1 (Worker)           │
│  │  ├─ Process 2 (Worker)           │
│  │  ├─ Process 3 (Worker)           │
│  │  └─ Process 4 (Worker)           │
│  │                                   │
│  ├─ Shared Cache (In-memory)        │
│  │  ├─ GeoJSON cache                │
│  │  ├─ CSV cache                    │
│  │  └─ Other data                   │
│  │                                   │
│  ├─ File System                     │
│  │  ├─ data/                        │
│  │  ├─ outputs/                     │
│  │  └─ templates/                   │
│  │                                   │
│  └─ Python Runtime                  │
│     ├─ GeoPandas, Pandas            │
│     ├─ Flask, Werkzeug              │
│     └─ Other dependencies           │
│                                      │
└─────────────────────────────────────┘

Characteristics:
├─ Single point of failure
├─ Suitable for: ~100-1000 concurrent users
├─ Deployment: Development or small production
└─ Cost: Low (one server)

Capacity:
├─ RAM: 4-16 GB
├─ CPU: 4-8 cores
├─ Disk: 500 GB (with raw OSM data)
└─ Network: 1 Mbps+ (typically more)

Performance:
├─ Response time: 50-200ms (cached)
├─ Peak requests/sec: 50-100
├─ Cache hit rate: >95%
└─ Throughput: 100-500 concurrent users


FUTURE ARCHITECTURE (Distributed)
════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────┐
│                Load Balancer (Nginx)                  │
└──────────────────────┬───────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Server 1      Server 2      Server N
    (Flask)       (Flask)       (Flask)
    
    Each Server:
    ├─ Multiple Flask workers
    ├─ Local cache
    └─ Connection to shared cache

Shared Components:
├─ Redis Cache (or similar)
│  └─ Distributed caching
│
├─ Database (Optional)
│  ├─ PostgreSQL + PostGIS
│  └─ Store metrics
│
├─ File Storage (Cloud)
│  ├─ S3-compatible storage
│  └─ Shared data access
│
└─ Message Queue (Optional)
   ├─ Celery + RabbitMQ
   └─ Async processing

Architecture Benefits:
├─ Horizontal scaling (add more servers)
├─ High availability (no single point of failure)
├─ Load distribution
├─ Independent cache updates
└─ Cloud-native deployment


DEPLOYMENT SCENARIOS
═════════════════════

Scenario 1: Development
├─ Setup: python app.py
├─ Server: Flask development server
├─ Port: 5000
├─ Debug: Enabled
├─ Suitable for: Development, testing
└─ Users: 1-5 developers

Scenario 2: Small Production
├─ Setup: gunicorn -w 4 -b 0.0.0.0:5000 app:app
├─ Server: Gunicorn WSGI
├─ Workers: 4-8 processes
├─ Port: 5000 (behind Nginx proxy)
├─ Reverse Proxy: Nginx on port 80/443
├─ Users: 100-500
└─ Cost: ~$20/month (small cloud server)

Scenario 3: Medium Production
├─ Setup: Multi-instance load balancer
├─ Servers: 3-5 instances
├─ Cache: Redis cluster
├─ Database: PostgreSQL (optional)
├─ CDN: CloudFlare or similar
├─ Users: 1,000-5,000
└─ Cost: ~$200-500/month

Scenario 4: Large Enterprise
├─ Setup: Kubernetes cluster
├─ Autoscaling: Dynamic pods
├─ Cache: Distributed cache
├─ Database: Managed database service
├─ Monitoring: Prometheus + Grafana
├─ Logging: ELK stack
├─ Users: 10,000+
└─ Cost: $1,000+/month


DEPLOYMENT TECHNOLOGIES
═════════════════════════

Container-based (Recommended):
├─ Docker
│  ├─ Dockerfile for app
│  ├─ Container images
│  └─ Easy deployment
│
└─ Docker Compose
   ├─ Multi-container orchestration
   ├─ Development & small production
   └─ Easy setup

Kubernetes (Enterprise):
├─ Pod orchestration
├─ Autoscaling
├─ Rolling deployments
├─ Self-healing
└─ Production-grade

Cloud Platforms:
├─ Heroku
│  ├─ PaaS (Platform as a Service)
│  ├─ Simple deployment
│  └─ Good for MVP
│
├─ AWS
│  ├─ EC2 (VMs)
│  ├─ RDS (Database)
│  ├─ S3 (Storage)
│  ├─ Lambda (Serverless)
│  └─ CloudFront (CDN)
│
├─ Azure
│  ├─ App Service
│  ├─ Database services
│  └─ Similar to AWS
│
└─ Google Cloud
   ├─ Compute Engine
   ├─ Cloud Storage
   └─ Cloud Functions


PERFORMANCE OPTIMIZATION
═════════════════════════

Current Optimizations:
├─ In-memory caching
├─ Lazy loading (load only on use)
├─ Static file caching
├─ Compressed responses (gzip)
└─ Efficient database queries

Potential Improvements:
├─ CDN for static assets
├─ HTTP caching headers
├─ Database indexing
├─ Query optimization
├─ Client-side caching
└─ Progressive loading (AJAX)

Monitoring & Metrics:
├─ Response time tracking
├─ Cache hit rates
├─ Error rates
├─ User traffic
├─ Resource utilization
└─ Uptime monitoring
```

---

## Summary: Architecture Overview

### Key Architectural Principles

```
1. LAYERED ARCHITECTURE
   └─ Data Input → Processing → Storage → Application → UI

2. SEPARATION OF CONCERNS
   ├─ Pipeline scripts (processing logic)
   ├─ Processing modules (reusable code)
   ├─ Flask app (web layer)
   └─ Templates (presentation)

3. MODULARITY
   ├─ Each script/module has single responsibility
   ├─ Easy to test individually
   └─ Simple to replace/upgrade

4. SCALABILITY
   ├─ Stateless application (scales horizontally)
   ├─ Caching layer (reduces load)
   └─ File-based storage (avoids DB complexity)

5. REPRODUCIBILITY
   ├─ Automated pipeline
   ├─ Clear data transformations
   ├─ Version control
   └─ Same input → same output

6. MAINTAINABILITY
   ├─ Clear naming conventions
   ├─ Comprehensive documentation
   ├─ Modular code
   └─ Easy debugging
```

### Architecture in One Diagram

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│            LatviaOSM-Check Architecture                 │
│                                                          │
│  DATA SOURCES                                           │
│  (OSM, Official Stats, Boundaries)                      │
│           ↓                                              │
│  PROCESSING PIPELINE                                    │
│  (20 scripts: Extract → Process → Join → Calculate)    │
│           ↓                                              │
│  DATA PRODUCTS                                          │
│  (GeoJSON, CSV, HTML)                                   │
│           ↓                                              │
│  FLASK APPLICATION                                      │
│  (Routes, API, Caching)                                 │
│           ↓                                              │
│  USER INTERFACE                                         │
│  (Web Browser, GIS Tools, API Clients)                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

**End of Architecture Documentation**

*For more information, see other documentation in /docs folder*
