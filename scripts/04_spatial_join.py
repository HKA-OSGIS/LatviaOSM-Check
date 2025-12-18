#!/usr/bin/env python3
"""Spatial join roads to municipalities"""

import geopandas as gpd
import pandas as pd

print("=" * 60)
print("Spatial Join")
print("=" * 60)
print()

print("1/3 Loading data...")
roads = gpd.read_file('data/processed/roads.geojson')
municipalities = gpd.read_file('data/processed/municipalities.geojson')
print(f"✓ Loaded {len(roads):,} roads")
print(f"✓ Loaded {len(municipalities)} municipalities")

print("\n2/3 Performing spatial join...")
print("   This takes 2-5 minutes...")

# Spatial join
roads_with_muni = gpd.sjoin(
    roads,
    municipalities[['geometry', 'municipality_name', 'municipality_id']],
    how='left',
    predicate='intersects'
)
print("✓ Join complete")

print("\n3/3 Saving...")
roads_with_muni.to_file('data/processed/roads_by_municipality.geojson', driver='GeoJSON')
print(f"✓ Saved: data/processed/roads_by_municipality.geojson")

print("\n" + "=" * 60)
print("Statistics:")
print(f"  Roads assigned: {roads_with_muni['municipality_name'].notna().sum():,}")
print(f"  Unique municipalities: {roads_with_muni['municipality_name'].nunique()}")
print("=" * 60)
print()