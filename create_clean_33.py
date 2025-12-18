#!/usr/bin/env python3
"""Create truly clean 33-unit GeoJSON by dissolving multi-part geometries"""

import geopandas as gpd
import pandas as pd

print("Creating clean 33-unit GeoJSON (dissolving scattered features)...")
print("=" * 70)

gdf = gpd.read_file('outputs/exports/latvia_official_only.geojson')

print(f"Before: {len(gdf)} features")
print(f"Geometry types: {gdf.geometry.type.unique()}")

# Use dissolve to merge all parts by municipality name
gdf_clean = gdf.dissolve(by='municipality_name', aggfunc='first')

print(f"After: {len(gdf_clean)} features (unified)")
print(f"Geometry types: {gdf_clean.geometry.type.unique()}")

# Save
gdf_clean.to_file('outputs/exports/latvia_clean_33.geojson', driver='GeoJSON', encoding='utf-8')
print("✓ Saved: outputs/exports/latvia_clean_33.geojson")

# Verify
print()
print("Final municipalities:")
for i, name in enumerate(sorted(gdf_clean['municipality_name']), 1):
    print(f"  {i}. {name}")
