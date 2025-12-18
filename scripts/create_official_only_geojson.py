#!/usr/bin/env python3
"""Create filtered LAU-1 GeoJSON with ONLY municipalities that have official road data"""

import geopandas as gpd
import pandas as pd

print("Creating filtered LAU-1 GeoJSON (36 municipalities + 7 state cities)")
print("=" * 70)

# Load LAU-1 GeoJSON (78 features)
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
print(f"Original: {len(gdf)} features")

# Load official CSV data
df_csv = pd.read_csv('data/raw/TRS020_20251218-012055.csv', encoding='utf-8', skiprows=1)

# Extract official municipalities (with "municipality" in name)
mun_csv = df_csv[df_csv['Territorial unit'].str.contains('municipality', case=False, na=False)]
mun_csv = mun_csv[mun_csv['Types of surface'] == 'Total']
mun_csv = mun_csv[mun_csv['Indicator'] == 'Total']

# Clean municipality names
mun_csv['municipality_name'] = mun_csv['Territorial unit'].str.replace(' municipality', '', regex=False).str.strip()
official_municipalities = sorted(mun_csv['municipality_name'].unique())

print(f"Official municipalities in CSV: {len(official_municipalities)}")
for i, name in enumerate(official_municipalities, 1):
    print(f"  {i}. {name}")

# Extract state cities (Riga, Daugavpils, etc.)
city_csv = df_csv[~df_csv['Territorial unit'].str.contains('municipality|region|statistical', case=False, na=False)]
city_csv = city_csv[city_csv['Types of surface'] == 'Total']
city_csv = city_csv[city_csv['Indicator'] == 'Total']
state_cities = sorted(city_csv['Territorial unit'].unique())

print(f"\nState cities in CSV: {len(state_cities)}")
for i, name in enumerate(state_cities, 1):
    print(f"  {i}. {name}")

# Combine all official units
all_official = list(official_municipalities) + list(state_cities)

# Filter GeoJSON to only official units
gdf_filtered = gdf[gdf['municipality_name'].isin(all_official)].copy()

print(f"\nFiltered result: {len(gdf_filtered)} features")
print(f"  Municipalities: {(gdf_filtered['municipality_name'].isin(official_municipalities)).sum()}")
print(f"  State cities: {(gdf_filtered['municipality_name'].isin(state_cities)).sum()}")

# Save filtered GeoJSON
output_file = 'outputs/exports/latvia_official_only.geojson'
gdf_filtered.to_file(output_file, driver='GeoJSON', encoding='utf-8')
print(f"\n✓ Saved: {output_file}")

print("=" * 70)
