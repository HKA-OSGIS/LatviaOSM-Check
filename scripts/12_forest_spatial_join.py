#!/usr/bin/env python3
"""Perform spatial join of forests with administrative boundaries"""

import geopandas as gpd
import pandas as pd
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Forest Spatial Join")
print("=" * 60)

# Load data
print("\n1/3 Loading data...")
forests = gpd.read_file('data/processed/forests.geojson')
admin = gpd.read_file('outputs/exports/latvia_lau1.geojson')

print(f"  ✓ Forests: {len(forests):,} features")
print(f"  ✓ Admin units: {len(admin):,} features")

# Ensure same CRS
print("\n2/3 Processing spatial join...")
forests = forests.to_crs('EPSG:3035')
admin = admin.to_crs('EPSG:3035')

# Calculate areas
forests['area_m2'] = forests.geometry.area
forests['area_km2'] = forests['area_m2'] / 1_000_000

# Spatial join
forests_with_admin = gpd.sjoin(forests, admin[['municipality_name', 'geometry']], 
                               how='left', predicate='intersects')

# Save joined data
forests_with_admin = forests_with_admin.to_crs('EPSG:4326')
forests_with_admin.to_file('data/processed/forests_by_novads.geojson', driver='GeoJSON')
print(f"  ✓ Saved: data/processed/forests_by_novads.geojson")

# Calculate statistics by LAU1
print("\n3/3 Calculating statistics...")
stats = forests_with_admin.groupby('municipality_name').agg({
    'area_km2': 'sum',
    'osm_id': 'count'
}).reset_index()
stats.columns = ['municipality_name', 'osm_forest_area_km2', 'forest_count']

# Round values
stats['osm_forest_area_km2'] = stats['osm_forest_area_km2'].round(2)

# Save statistics
stats.to_csv('outputs/exports/forest_stats_by_novads.csv', index=False)
print(f"  ✓ Saved: outputs/exports/forest_stats_by_novads.csv")

print("\n" + "=" * 60)
print("Summary:")
print(f"  Total forest area: {stats['osm_forest_area_km2'].sum():.2f} km²")
print(f"  Total forests: {stats['forest_count'].sum():,}")
print(f"  Administrative units: {len(stats)}")
print("=" * 60)
