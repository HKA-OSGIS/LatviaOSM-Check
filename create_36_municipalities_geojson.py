#!/usr/bin/env python3
"""Filter GeoJSON to only include 36 municipalities with official data."""

import json
import pandas as pd

# Load the official municipalities from CSV
df_munis = pd.read_csv('outputs/exports/completeness_municipalities.csv')
official_munis = set(df_munis['Municipality'].unique())

print(f"Official municipalities to keep: {len(official_munis)}")

# Load the full GeoJSON
with open('data/raw/municipalities.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter features to only those in the official list
filtered_features = []
for feature in data.get('features', []):
    shape_name = feature.get('properties', {}).get('shapeName', '')
    
    # Check if this municipality is in our official list
    if shape_name in official_munis:
        filtered_features.append(feature)
        print(f"  ✓ {shape_name}")

print(f"\nFiltered features: {len(filtered_features)}")

# Create new GeoJSON with only the filtered features
filtered_geojson = {
    "type": "FeatureCollection",
    "features": filtered_features
}

# Save the filtered GeoJSON
output_file = 'outputs/exports/latvia_municipalities_36_only.geojson'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_geojson, f, ensure_ascii=False, indent=2)

print(f"✓ Saved filtered GeoJSON to {output_file}")
