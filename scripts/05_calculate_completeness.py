#!/usr/bin/env python3
"""Calculate road completeness"""

import geopandas as gpd
import pandas as pd

print("=" * 60)
print("Calculating Completeness")
print("=" * 60)
print()

print("1/4 Loading data...")
roads = gpd.read_file('data/processed/roads_by_municipality.geojson')
municipalities = gpd.read_file('data/processed/municipalities.geojson')
official = pd.read_csv('data/raw/official_road_stats.csv')
print("✓ Data loaded")

print("\n2/4 Aggregating OSM roads by municipality...")
osm_aggregated = roads.groupby('municipality_name').agg({
    'length_km': 'sum',
    'osm_id': 'count'
}).reset_index()
osm_aggregated.columns = ['municipality_name', 'osm_road_km', 'num_segments']
osm_aggregated['osm_road_km'] = osm_aggregated['osm_road_km'].round(2)
print(f"✓ Aggregated for {len(osm_aggregated)} municipalities")

print("\n3/4 Calculating completeness...")
completeness = pd.merge(
    osm_aggregated,
    official,
    on='municipality_name',
    how='outer'
)

completeness['completeness_pct'] = (
    completeness['osm_road_km'] / completeness['road_length_km'] * 100
).round(2)

def categorize(pct):
    if pd.isna(pct):
        return 'No data'
    elif pct < 70:
        return 'Low'
    elif pct < 90:
        return 'Partial'
    elif pct <= 110:
        return 'Complete'
    else:
        return 'Over-mapped'

completeness['category'] = completeness['completeness_pct'].apply(categorize)
completeness['difference_km'] = (completeness['osm_road_km'] - completeness['road_length_km']).round(2)
print("✓ Completeness calculated")

print("\n4/4 Creating final map dataset...")
completeness_map = municipalities.merge(
    completeness,
    on='municipality_name',
    how='left'
)
completeness_map['road_density_km_per_km2'] = (
    completeness_map['osm_road_km'] / completeness_map['area_km2']
).round(3)

# Convert back to WGS84 for web maps
completeness_map = completeness_map.to_crs('EPSG:4326')

# Save
completeness.to_csv('outputs/exports/completeness.csv', index=False)
completeness_map.to_file('outputs/exports/completeness_map.geojson', driver='GeoJSON')
print("✓ Saved results")

print("\n" + "=" * 60)
print("Summary:")
print(completeness['category'].value_counts().to_string())
print("\n" + "=" * 60)
print("✓ Completeness Analysis Complete!")
print("=" * 60)
print()