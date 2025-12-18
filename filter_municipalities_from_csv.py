#!/usr/bin/env python3
"""Filter GeoJSON to only municipalities from the new CSV"""

import geopandas as gpd
import pandas as pd

print("Filtering municipalities from CSV...")
print("=" * 70)

# Read the new CSV
csv_file = 'data/raw/TRS020_20251218-122746.csv'
df = pd.read_csv(csv_file, skiprows=2)  # Skip header rows

# Extract municipality names (all rows are municipalities)
municipalities_csv = df['Territorial unit'].unique()
municipalities_csv = [m.strip().replace(' municipality', '').replace(' city', '') for m in municipalities_csv]

print(f"Municipalities from CSV: {len(municipalities_csv)}")
print(f"Names: {sorted(municipalities_csv)}")
print()

# Read GeoJSON
gdf = gpd.read_file('outputs/exports/latvia_clean_33.geojson')
print(f"Features in GeoJSON: {len(gdf)}")

# Filter GeoJSON to only CSV municipalities
gdf_filtered = gdf[gdf['municipality_name'].isin(municipalities_csv)].copy()
print(f"After filtering: {len(gdf_filtered)} municipalities")
print()

# Merge official road lengths from CSV
official_roads_dict = {}
for _, row in df.iterrows():
    unit_original = row['Territorial unit'].strip()
    unit_clean = unit_original.replace(' municipality', '').replace(' city', '')
    if row['Indicator'] == 'Total':
        official_roads_dict[unit_clean] = float(row['2024'])

gdf_filtered['official_road_km'] = gdf_filtered['municipality_name'].map(official_roads_dict)

# Recalculate completeness
gdf_filtered['completeness_pct'] = (gdf_filtered['osm_road_km'] / gdf_filtered['official_road_km'] * 100).round(1)

# Save filtered GeoJSON
gdf_filtered.to_file('outputs/exports/latvia_municipalities_only.geojson', driver='GeoJSON', encoding='utf-8')
print(f"✓ Saved: outputs/exports/latvia_municipalities_only.geojson")

# Create CSV for Flask
csv_output = gdf_filtered[['municipality_name', 'osm_road_km', 'official_road_km', 'completeness_pct']].copy()
csv_output.columns = ['Municipality', 'OSM Roads (km)', 'Official Roads (km)', 'Completeness (%)']
csv_output = csv_output.sort_values('Municipality')

csv_output.to_csv('outputs/exports/completeness_municipalities.csv', index=False, encoding='utf-8')
print(f"✓ Saved: outputs/exports/completeness_municipalities.csv")
print()

print("Municipalities included:")
for name in sorted(gdf_filtered['municipality_name']):
    print(f"  - {name}")
