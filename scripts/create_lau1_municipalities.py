import geopandas as gpd
import pandas as pd
import requests
import json

print("=" * 70)
print("Creating LAU-1 GeoJSON (36 Official Municipalities)")
print("=" * 70)

# Load official road data from CSV (this is our source of truth for LAU-1)
print("\n1. Loading official road data from CSV...")
df_csv = pd.read_csv('data/raw/TRS020_20251218-012055.csv', encoding='utf-8', skiprows=1)

# Extract municipalities from CSV (with " municipality" suffix)
mun_csv = df_csv[df_csv['Territorial unit'].str.contains('municipality', case=False, na=False)].copy()
mun_csv = mun_csv[mun_csv['Types of surface'] == 'Total'].copy()
mun_csv = mun_csv[mun_csv['Indicator'] == 'Total'].copy()
mun_csv['municipality_name'] = mun_csv['Territorial unit'].str.replace(' municipality', '', regex=False).str.strip()
official_data = mun_csv[['municipality_name', '2024']].copy()
official_data.columns = ['municipality_name', 'official_road_km']
official_data['official_road_km'] = pd.to_numeric(official_data['official_road_km'], errors='coerce')
official_data = official_data.drop_duplicates().reset_index(drop=True)
print(f"   ✓ Found {len(official_data)} official municipalities")
print(f"   Official municipalities: {', '.join(sorted(official_data['municipality_name'].tolist()))}")

# Load existing GeoJSON (contains both old and new municipalities)
print("\n2. Loading existing GeoJSON...")
gdf = gpd.read_file('outputs/exports/completeness_map.geojson')
print(f"   Current: {len(gdf)} features (includes old townships/parishes)")

# Filter GeoJSON to only municipalities that match the 36 official ones
print("\n3. Filtering GeoJSON to official LAU-1 municipalities...")
gdf_lau1 = gdf[gdf['municipality_name'].isin(official_data['municipality_name'])].copy()
print(f"   GeoJSON municipalities before filter: {gdf['municipality_name'].unique().tolist()[:5]}...")
print(f"   Official municipalities: {official_data['municipality_name'].unique().tolist()[:5]}...")
print(f"   ✓ Filtered to {len(gdf_lau1)} matched municipalities")

# Merge with official data
print("\n4. Merging with official road data...")
gdf_lau1 = gdf_lau1.merge(official_data, on='municipality_name', how='left')

# Calculate completeness based on official data
gdf_lau1['completeness_pct'] = (gdf_lau1['osm_road_km'] / gdf_lau1['official_road_km'] * 100).round(1)

# Save
output_file = 'outputs/exports/latvia_lau1.geojson'
gdf_lau1.to_file(output_file, driver='GeoJSON', encoding='utf-8')
print(f"\n✓ Saved: {output_file}")
print(f"   Features: {len(gdf_lau1)} LAU-1 municipalities")

print("\n" + "=" * 70)
print("36 Official LAU-1 Municipalities:")
print("=" * 70)
for idx, row in gdf_lau1.sort_values('municipality_name').iterrows():
    official_km = row['official_road_km']
    osm_km = row['osm_road_km']
    completeness = row['completeness_pct']
    print(f"  {row['municipality_name']:<25} Official: {official_km:>6.0f} km | OSM: {osm_km:>7.2f} km | Completeness: {completeness:>6.1f}%")

print(f"\nTotal: {len(gdf_lau1)} municipalities in LAU-1 GeoJSON")
