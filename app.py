#!/usr/bin/env python3
"""Flask web application for OSM road completeness analysis with hierarchical selector.

Provides both a traditional map view and a new hierarchical geographic selector
for filtering by country, region, municipality, and feature type.
"""

from flask import Flask, send_file, jsonify, request, render_template
from pathlib import Path
import json
import geopandas as gpd
import pandas as pd

app = Flask(__name__, template_folder='templates')

ROOT = Path(__file__).resolve().parent
MAP_HTML = ROOT / 'outputs' / 'maps' / 'interactive_map.html'
GEOJSON_FILE = ROOT / 'outputs' / 'exports' / 'latvia_municipalities_36_only.geojson'
CSV_FILE = ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'

# Cache for GeoJSON data and hierarchy
_geojson_cache = None
_hierarchy_cache = None
_dataframe_cache = None


def clear_cache():
    """Clear all caches to force reload."""
    global _geojson_cache, _hierarchy_cache, _dataframe_cache
    _geojson_cache = None
    _hierarchy_cache = None
    _dataframe_cache = None


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
    """Main page: redirect to dynamic map."""
    from flask import redirect
    return redirect('/dynamic-map')


@app.route('/map')
def map_view():
    """Interactive map view (Folium - legacy)."""
    if not MAP_HTML.exists():
        return (
            'Map not found. Run: python scripts/07_create_interactive_map.py',
            500,
        )
    return send_file(MAP_HTML, mimetype='text/html')


@app.route('/dynamic-map')
def dynamic_map():
    """Interactive map with dynamic data loading from API."""
    return render_template('dynamic_map.html')


@app.route('/selector')
def selector():
    """Geographic selector with checkboxes and comparison."""
    return render_template('geographic_selector.html')


@app.route('/folium')
def folium_map():
    """Alias for the interactive map."""
    return map_view()


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


if __name__ == '__main__':
    print("=" * 60)
    print("Starting LatviaOSM-Check Server")
    print("=" * 60)
    
    # Check files
    if not GEOJSON_FILE.exists():
        print("❌ GeoJSON not found:")
        print(f"  {GEOJSON_FILE}")
    else:
        print("✓ GeoJSON found")
    
    if not CSV_FILE.exists():
        print("❌ CSV data not found:")
        print(f"  {CSV_FILE}")
    else:
        print("✓ CSV data found")
    
    if not MAP_HTML.exists():
        print("⚠ Legacy map not found (optional)")
    else:
        print("✓ Legacy map available at /map")
    
    print("\n[MAIN] Topic Selector at: http://localhost:5000")
    print("[AVAILABLE TOPICS]")
    print("  ✓ Roads (OSM + 20 cities official data)")
    print("  ⏳ Railways (Coming soon)")
    print("  ⏳ Buildings (Coming soon)")
    print("  ⏳ POIs - Hospitals, Restaurants (Coming soon)")
    print("  ⏳ Forests (Coming soon)")
    print("\n[API] Endpoints:")
    print("  - GET /api/geojson-data - OSM roads GeoJSON")
    print("  - GET /api/csv-data - Get all municipality statistics")
    print("  - GET /api/hierarchy - Get geographic hierarchy")
    print("  - GET /api/municipality-data - Get GeoJSON for municipality\n")
    
    app.run(debug=True)
