#!/usr/bin/env python3
"""Perform spatial join of libraries with administrative boundaries"""

import geopandas as gpd
import pandas as pd
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Library Spatial Join")
print("=" * 60)

# Load data
print("\n1/3 Loading data...")
libraries = gpd.read_file('data/processed/libraries.geojson')
admin = gpd.read_file('outputs/exports/latvia_lau1.geojson')

print(f"  ✓ Libraries: {len(libraries):,} features")
print(f"  ✓ Admin units: {len(admin):,} features")

# Ensure same CRS
print("\n2/3 Processing spatial join...")
libraries = libraries.to_crs('EPSG:3035')
admin = admin.to_crs('EPSG:3035')

# Spatial join
libraries_with_admin = gpd.sjoin(libraries, admin[['municipality_name', 'Area_Type', 'geometry']], 
                                 how='left', predicate='within')

# Save joined data
libraries_with_admin = libraries_with_admin.to_crs('EPSG:4326')
libraries_with_admin.to_file('data/processed/libraries_by_novads.geojson', driver='GeoJSON')
print(f"  ✓ Saved: data/processed/libraries_by_novads.geojson")

# Calculate statistics by LAU1
print("\n3/3 Calculating statistics...")
stats = libraries_with_admin.groupby('municipality_name').agg({
    'osm_id': 'count',
    'Area_Type': 'first'
}).reset_index()
stats.columns = ['municipality_name', 'osm_library_count', 'Area_Type']

# Save statistics
stats.to_csv('outputs/exports/library_stats_by_novads.csv', index=False)
print(f"  ✓ Saved: outputs/exports/library_stats_by_novads.csv")

print("\n" + "=" * 60)
print("Summary:")
print(f"  Total libraries: {stats['osm_library_count'].sum():,}")
print(f"  Administrative units with libraries: {len(stats)}")
print("=" * 60)

print("\nTop 10 units by library count:")
print(stats.nlargest(10, 'osm_library_count')[['municipality_name', 'osm_library_count']].to_string(index=False))
