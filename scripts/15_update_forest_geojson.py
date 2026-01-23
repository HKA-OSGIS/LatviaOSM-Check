#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update latvia_lau1_forests.geojson with forest completeness data
Uses same structure as roads GeoJSON
"""

import json
import pandas as pd
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("Updating Forest GeoJSON with Completeness Data")
print("=" * 70)
print()

print("1/3 Loading template GeoJSON...")
with open('outputs/exports/latvia_lau1_forests.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)
print(f"✓ Loaded {len(geojson_data['features'])} features")

print("\n2/3 Loading forest completeness data...")
forest_data = pd.read_csv('outputs/exports/completeness_forests.csv')
print(f"✓ Loaded {len(forest_data)} forest completeness records")

# Load official data directly to handle duplicates
official_data = pd.read_csv('data/raw/official_forest_stats.csv')

# Create lookup dictionary for OSM data
osm_lookup = {}
for _, row in forest_data.iterrows():
    name = row['municipality_name']
    if pd.notna(row.get('osm_forest_km2')) and row.get('osm_forest_km2', 0) > 0:
        osm_lookup[name] = {
            'osm_forest_km2': row.get('osm_forest_km2', 0),
            'osm_forest_ha': row.get('osm_forest_ha', 0),
            'num_forest_areas': int(row.get('num_forest_areas', 0)) if pd.notna(row.get('num_forest_areas')) else 0
        }

# Create lookup for official data, handling duplicates
official_lookup = {}
for name in official_data['municipality_name'].unique():
    entries = official_data[official_data['municipality_name'] == name]
    if len(entries) > 1:
        # Has duplicates (city + novads) - store both
        official_lookup[name + '_city'] = entries.nsmallest(1, 'forest_area_km2').iloc[0]
        official_lookup[name + '_novads'] = entries.nlargest(1, 'forest_area_km2').iloc[0]
    else:
        official_lookup[name] = entries.iloc[0]

print("\n3/3 Updating GeoJSON properties...")
updated_count = 0
for feature in geojson_data['features']:
    mun_name = feature['properties'].get('Municipality') or feature['properties'].get('municipality_name')
    area_type = feature['properties'].get('Area_Type', 'Municipality')
    
    # Get OSM data
    osm_data = osm_lookup.get(mun_name, {})
    
    # Get official data - handle duplicates
    official_key = mun_name
    if area_type == 'City' and (mun_name + '_city') in official_lookup:
        official_row = official_lookup[mun_name + '_city']
    elif area_type == 'Municipality' and (mun_name + '_novads') in official_lookup:
        official_row = official_lookup[mun_name + '_novads']
    elif mun_name in official_lookup:
        official_row = official_lookup[mun_name]
    else:
        official_row = None
    
    # Build properties - convert all to native Python types
    props = {
        'osm_forest_km2': float(osm_data.get('osm_forest_km2', 0)) if osm_data.get('osm_forest_km2') else 0.0,
        'osm_forest_ha': float(osm_data.get('osm_forest_ha', 0)) if osm_data.get('osm_forest_ha') else 0.0,
        'num_forest_areas': int(osm_data.get('num_forest_areas', 0)) if osm_data.get('num_forest_areas') else 0
    }
    
    if official_row is not None:
        props['official_forest_km2'] = float(official_row['forest_area_km2']) if pd.notna(official_row['forest_area_km2']) else 0.0
        props['official_forest_ha'] = float(official_row['forest_area_ha']) if pd.notna(official_row['forest_area_ha']) else 0.0
        # Calculate completeness
        if props['official_forest_km2'] > 0 and props['osm_forest_km2'] > 0:
            props['forest_completeness_pct'] = round(float(props['osm_forest_km2']) / float(props['official_forest_km2']) * 100, 2)
        else:
            props['forest_completeness_pct'] = None
    else:
        props['official_forest_km2'] = 0.0
        props['official_forest_ha'] = 0.0
        props['forest_completeness_pct'] = None
    
    # Add category
    pct = props.get('forest_completeness_pct')
    if pct is None or pct == 0:
        props['forest_category'] = 'No data'
    elif pct >= 90:
        props['forest_category'] = 'Complete'
    elif pct >= 70:
        props['forest_category'] = 'Good'
    elif pct >= 50:
        props['forest_category'] = 'Partial'
    else:
        props['forest_category'] = 'Low'
    
    if pct and pct > 100:
        props['forest_category'] = 'Over-mapped'
    
    feature['properties'].update(props)
    updated_count += 1

print(f"✓ Updated {updated_count} features with forest data")

print("\n4/4 Saving updated GeoJSON...")
with open('outputs/exports/latvia_lau1_forests.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False)

file_size = len(open('outputs/exports/latvia_lau1_forests.geojson', 'rb').read()) / (1024 * 1024)
print(f"✓ Saved: outputs/exports/latvia_lau1_forests.geojson")
print(f"  File size: {file_size:.2f} MB")

print("\n" + "=" * 70)
print("✓ Forest GeoJSON ready!")
print("  Features with forest data: " + str(updated_count))
print("=" * 70)
