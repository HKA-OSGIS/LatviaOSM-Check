#!/usr/bin/env python3
"""Calculate forest completeness percentages"""

import pandas as pd
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Forest Completeness Calculation")
print("=" * 60)

# Load OSM stats
osm_stats = pd.read_csv('outputs/exports/forest_stats_by_novads.csv')
print(f"\n✓ Loaded OSM statistics: {len(osm_stats)} units")

# Load official stats
official = pd.read_csv('data/raw/official_forest_stats.csv')
print(f"✓ Loaded official statistics: {len(official)} entries")

# Merge datasets
# First add Area_Type from LAU1 file
lau1 = pd.read_csv('outputs/exports/latvia_lau1.geojson', nrows=0)  # Just to check if available
# Load from LAU1 geojson
import geopandas as gpd
lau1_gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
area_types = lau1_gdf[['municipality_name', 'Area_Type']].copy()

# Merge with OSM stats to get Area_Type
osm_with_type = pd.merge(osm_stats, area_types, on='municipality_name', how='left')

# Normalize city names (remove possessive 's' suffix for cities)
# Only remove 's' if it creates a match in official data
official_city_names = set(official[official['Area_Type'] == 'City']['municipality_name'].values)

def normalize_city_name(row):
    if row['Area_Type'] != 'City':
        return row['municipality_name']
    
    name = row['municipality_name']
    # Try exact match first
    if name in official_city_names:
        return name
    # Try removing 's' suffix
    if name.endswith('s'):
        name_without_s = name[:-1]
        if name_without_s in official_city_names:
            return name_without_s
    return name

osm_with_type['match_name'] = osm_with_type.apply(normalize_city_name, axis=1)
official['match_name'] = official['municipality_name']

# Now merge with official data
merged = pd.merge(
    osm_with_type, 
    official[['match_name', 'forest_area_ha', 'Area_Type']], 
    on=['match_name', 'Area_Type'],
    how='left'
)

# Convert hectares to km²
merged['official_forest_km2'] = merged['forest_area_ha'] / 100

# Calculate completeness
merged['completeness_%'] = (merged['osm_forest_area_km2'] / merged['official_forest_km2'] * 100).round(2)

# Select output columns
output = merged[['municipality_name', 'Area_Type', 'osm_forest_area_km2', 'official_forest_km2', 'completeness_%', 'forest_count']]
output = output.sort_values('completeness_%', ascending=False)

# Save
output.to_csv('outputs/exports/completeness_forests.csv', index=False)
print(f"✓ Saved: outputs/exports/completeness_forests.csv")

print("\n" + "=" * 60)
print("Top 10 Most Complete:")
print(output.head(10)[['municipality_name', 'Area_Type', 'completeness_%']].to_string(index=False))

print("\n" + "=" * 60)
print("Summary Statistics:")
print(f"  Average completeness: {output['completeness_%'].mean():.2f}%")
print(f"  Median completeness: {output['completeness_%'].median():.2f}%")
print(f"  Total OSM forest land: {output['osm_forest_area_km2'].sum():.2f} km²")
print(f"  Total official forest land: {output['official_forest_km2'].sum():.2f} km²")
print(f"  Overall completeness: {(output['osm_forest_area_km2'].sum() / output['official_forest_km2'].sum() * 100):.2f}%")
print("=" * 60)
