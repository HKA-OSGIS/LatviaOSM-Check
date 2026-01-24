#!/usr/bin/env python3
"""Flask web application for OSM completeness analysis (Roads, Forests, Libraries) with interactive maps.

Provides interactive map views with hierarchical geographic filtering and comprehensive
comparison of OpenStreetMap data against official government statistics.
"""

from flask import Flask, send_file, jsonify, request, render_template, redirect
from pathlib import Path
import json
import pandas as pd

app = Flask(__name__, template_folder='templates')

ROOT = Path(__file__).resolve().parent
MAP_HTML = ROOT / 'outputs' / 'maps' / 'interactive_map.html'
LAU1_MAP_HTML = ROOT / 'outputs' / 'maps' / 'interactive_map.html'  # LAU1 map with municipalities and cities
FOREST_MAP_HTML = ROOT / 'outputs' / 'maps' / 'forest_completeness_map.html'  # Forest map
LIBRARY_MAP_HTML = ROOT / 'outputs' / 'maps' / 'library_completeness_map.html'  # Library map
COMBINED_MAP_HTML = ROOT / 'outputs' / 'maps' / 'combined_map.html'  # Combined roads, forests & libraries map
GEOJSON_FILE = ROOT / 'outputs' / 'exports' / 'latvia_lau1.geojson'  # Updated to use LAU1 GeoJSON
CSV_FILE = ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'
FOREST_CSV_FILE = ROOT / 'outputs' / 'exports' / 'completeness_forests.csv'
LIBRARY_CSV_FILE = ROOT / 'outputs' / 'exports' / 'completeness_libraries.csv'

# Cache for GeoJSON data and hierarchy
_geojson_cache = None
_hierarchy_cache = None
_dataframe_cache = None
_forest_dataframe_cache = None
_library_dataframe_cache = None


def clear_cache():
    """Clear all caches to force reload."""
    global _geojson_cache, _hierarchy_cache, _dataframe_cache, _forest_dataframe_cache, _library_dataframe_cache
    _geojson_cache = None
    _hierarchy_cache = None
    _dataframe_cache = None
    _forest_dataframe_cache = None
    _library_dataframe_cache = None


def load_geojson():
    """Load and cache GeoJSON data."""
    global _geojson_cache
    if _geojson_cache is None:
        if GEOJSON_FILE.exists():
            with open(GEOJSON_FILE, 'r', encoding='utf-8') as f:
                _geojson_cache = json.load(f)
    return _geojson_cache


def load_dataframe():
    """Load and cache CSV data."""
    global _dataframe_cache
    if _dataframe_cache is None:
        if CSV_FILE.exists():
            _dataframe_cache = pd.read_csv(CSV_FILE, encoding='utf-8')
    return _dataframe_cache


def load_forest_dataframe():
    """Load and cache forest CSV data."""
    global _forest_dataframe_cache
    if _forest_dataframe_cache is None:
        if FOREST_CSV_FILE.exists():
            _forest_dataframe_cache = pd.read_csv(FOREST_CSV_FILE, encoding='utf-8')
    return _forest_dataframe_cache


def load_library_dataframe():
    """Load and cache library CSV data."""
    global _library_dataframe_cache
    if _library_dataframe_cache is None:
        if LIBRARY_CSV_FILE.exists():
            _library_dataframe_cache = pd.read_csv(LIBRARY_CSV_FILE, encoding='utf-8')
    return _library_dataframe_cache


def build_hierarchy():
    """Build geographic hierarchy from data."""
    global _hierarchy_cache
    if _hierarchy_cache is None:
        geojson = load_geojson()
        if not geojson:
            return None
        
        # Extract municipalities from GeoJSON features
        municipalities = {}
        for feature in geojson.get('features', []):
            props = feature.get('properties', {})
            muni_name = props.get('municipality_name', '')
            if muni_name:
                municipalities[muni_name] = props
        
        # For now, group all municipalities under a single region called "All Regions"
        # since the data doesn't explicitly contain regional grouping
        _hierarchy_cache = {
            'countries': ['Latvia'],
            'regions': {
                'Latvia': ['All Regions']
            },
            'municipalities': {
                'Latvia': {
                    'All Regions': sorted(list(municipalities.keys()))
                }
            }
        }
    return _hierarchy_cache


@app.route('/')
def index():
    """Main page: redirect to combined map."""
    return redirect('/combined-map')


@app.route('/map')
def map_view():
    """Interactive map view with LAU1 municipalities and cities."""
    if not MAP_HTML.exists():
        return (
            'Map not found. Run: python scripts/08_create_lau1_map.py',
            500,
        )
    return send_file(MAP_HTML, mimetype='text/html')




@app.route('/combined-map')
def combined_map():
    """Interactive combined map with roads and forests toggle."""
    if not COMBINED_MAP_HTML.exists():
        return (
            'Combined map not found. Run: python scripts/18_create_combined_map.py',
            500,
        )
    return send_file(COMBINED_MAP_HTML, mimetype='text/html')


@app.route('/forest-map')
def forest_map():
    """Interactive forest completeness map."""
    if not FOREST_MAP_HTML.exists():
        return (
            'Forest map not found. Run: python scripts/13_create_forest_map.py',
            500,
        )
    return send_file(FOREST_MAP_HTML, mimetype='text/html')


@app.route('/library-map')
def library_map():
    """Interactive library completeness map."""
    if not LIBRARY_MAP_HTML.exists():
        return (
            'Library map not found. Run: python scripts/27_create_library_map.py',
            500,
        )
    return send_file(LIBRARY_MAP_HTML, mimetype='text/html')


@app.route('/lau1-map')
def lau1_map():
    """Interactive LAU1 map view with municipalities and cities."""
    if not LAU1_MAP_HTML.exists():
        return (
            'LAU1 map not found. Run: python scripts/08_create_lau1_map.py',
            500,
        )
    return send_file(LAU1_MAP_HTML, mimetype='text/html')


@app.route('/dynamic-map')
def dynamic_map():
    """Interactive map with dynamic data loading from API."""
    return render_template('dynamic_map.html')


@app.route('/api/hierarchy', methods=['GET'])
def api_hierarchy():
    """Get geographic hierarchy for selectors."""
    hierarchy = build_hierarchy()
    if not hierarchy:
        return jsonify({'error': 'Hierarchy data not available'}), 500
    return jsonify(hierarchy)


@app.route('/api/geojson-data', methods=['GET'])
def api_geojson_data():
    """Get full GeoJSON data for all municipalities."""
    geojson = load_geojson()
    if not geojson:
        return jsonify({'error': 'GeoJSON data not available'}), 500
    return jsonify(geojson)


@app.route('/api/csv-data', methods=['GET'])
def api_csv_data():
    """Get CSV data for all municipalities as array of objects."""
    df = load_dataframe()
    if df is None:
        return jsonify({'error': 'CSV data not available'}), 500
    
    # Rename columns to match the expected format
    df = df.rename(columns={
        'Municipality': 'municipality_name',
        'OSM_Roads_km': 'osm_road_km',
        'Official_Roads_km': 'official_road_km',
        'Completeness_%': 'completeness_pct',
        # Handle old format columns as well
        'OSM Roads (km)': 'osm_road_km',
        'Official Roads (km)': 'official_road_km',
        'Completeness (%)': 'completeness_pct'
    })
    
    # Convert to records and ensure NaN becomes None for JSON serialization
    records = json.loads(df.to_json(orient='records'))
    return jsonify(records)


@app.route('/api/municipality-data', methods=['GET'])
def api_municipality_data():
    """Get GeoJSON data for a specific municipality."""
    municipality = request.args.get('municipality', '')
    feature_type = request.args.get('feature', 'roads')
    
    if not municipality:
        return jsonify({'error': 'Municipality parameter required'}), 400
    
    geojson = load_geojson()
    if not geojson:
        return jsonify({'error': 'GeoJSON data not available'}), 500
    
    # Filter GeoJSON features to only the selected municipality
    filtered_features = []
    for feature in geojson.get('features', []):
        if feature.get('properties', {}).get('municipality_name') == municipality:
            filtered_features.append(feature)
    
    # Return as FeatureCollection
    result = {
        'type': 'FeatureCollection',
        'features': filtered_features
    }
    
    return jsonify(result)


@app.route('/api/data/<municipality>', methods=['GET'])
def api_data(municipality):
    """Get completeness data for a municipality."""
    df = load_dataframe()
    if df is None:
        return jsonify({'error': 'Data not available'}), 500
    
    # Find the municipality in the CSV
    muni_data = df[df['municipality_name'] == municipality]
    if muni_data.empty:
        return jsonify({'error': 'Municipality not found'}), 404
    
    # Convert to dict
    result = muni_data.iloc[0].to_dict()
    
    # Convert NaN to None for JSON serialization
    result = {k: (None if pd.isna(v) else v) for k, v in result.items()}
    
    return jsonify(result)


@app.route('/api/forest-data', methods=['GET'])
def api_forest_data():
    """Get forest completeness data for all municipalities as array of objects."""
    df = load_forest_dataframe()
    if df is None:
        return jsonify({'error': 'Forest data not available'}), 500
    
    # Convert to records and ensure NaN becomes None for JSON serialization
    records = json.loads(df.to_json(orient='records'))
    return jsonify(records)


if __name__ == '__main__':
    print("=" * 60)
    print("Starting LatviaOSM-Check Server")
    print("=" * 60)
    
    # Check files
    if not GEOJSON_FILE.exists():
        print("[X] GeoJSON not found:")
        print(f"  {GEOJSON_FILE}")
    else:
        print("[OK] GeoJSON found")
    
    if not CSV_FILE.exists():
        print("[X] CSV data not found:")
        print(f"  {CSV_FILE}")
    else:
        print("[OK] CSV data found")
    
    if not MAP_HTML.exists():
        print("[!] Legacy map not found (optional)")
    else:
        print("[OK] Legacy map available at /map")
    
    print("\n[MAIN] Maps available:")
    print("  - http://localhost:5000/combined-map (Roads, Forests & Libraries Combined) ⭐")
    print("  - http://localhost:5000/lau1-map (Roads Only)")
    print("  - http://localhost:5000/forest-map (Forests Only)")
    print("  - http://localhost:5000/library-map (Libraries Only)")
    print("\n[AVAILABLE TOPICS]")
    print("  [OK] Roads (OSM + 7 cities official data)")
    print("  [OK] Forests (OSM + official forest statistics)")
    print("  [OK] Libraries (OSM + official library statistics)")
    print("  [PENDING] Railways (Coming soon)")
    print("  [PENDING] Buildings (Coming soon)")
    print("  [PENDING] POIs - Hospitals, Restaurants (Coming soon)")
    print("\n[API] Endpoints:")
    print("  - GET /api/geojson-data - OSM roads GeoJSON")
    print("  - GET /api/csv-data - Roads completeness statistics")
    print("  - GET /api/forest-data - Forest completeness statistics")
    print("  - GET /api/hierarchy - Get geographic hierarchy")
    print("  - GET /api/municipality-data - Get GeoJSON for municipality\n")
    
    app.run(debug=True)
