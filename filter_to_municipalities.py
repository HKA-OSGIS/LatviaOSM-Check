#!/usr/bin/env python3
"""Filter data to only include municipalities from the new CSV file"""

import geopandas as gpd
import pandas as pd

print("Filtering to municipalities from TRS020_20251218-122746.csv")
print("=" * 70)

# Read new CSV and extract municipalities
df_csv = pd.read_csv('data/raw/TRS020_20251218-122746.csv', skiprows=1)
print(f"CSV records: {len(df_csv)}")

# Extract municipality names (remove " municipality" suffix)
municipalities = df_csv['Territorial unit'].str.replace(' municipality', '').unique()
municipalities = [m.strip() for m in municipalities if m]
print(f"Unique municipalities in CSV: {len(municipalities)}")
print(f"Municipalities: {sorted(municipalities)}")

# Read current GeoJSON
gdf = gpd.read_file('outputs/exports/latvia_clean_33.geojson')
print(f"\nCurrent GeoJSON features: {len(gdf)}")

# Filter to only municipalities in CSV
gdf_filtered = gdf[gdf['municipality_name'].isin(municipalities)].copy()
print(f"After filtering: {len(gdf_filtered)} municipalities")

# Merge official road data from CSV
df_csv_for_merge = df_csv.copy()
df_csv_for_merge['municipality_name'] = df_csv_for_merge['Territorial unit'].str.replace(' municipality', '').str.strip()
df_csv_for_merge['official_road_km'] = pd.to_numeric(df_csv_for_merge['2024'], errors='coerce')
df_csv_for_merge = df_csv_for_merge[['municipality_name', 'official_road_km']].drop_duplicates(subset=['municipality_name'])

# Merge into GeoJSON
gdf_filtered = gdf_filtered.merge(
    df_csv_for_merge,
    on='municipality_name',
    how='left',
    suffixes=('_old', '')
)

# Recalculate completeness
gdf_filtered['osm_road_km'] = pd.to_numeric(gdf_filtered['osm_road_km'], errors='coerce')
gdf_filtered['official_road_km'] = pd.to_numeric(gdf_filtered['official_road_km'], errors='coerce')
gdf_filtered['completeness_pct'] = (gdf_filtered['osm_road_km'] / gdf_filtered['official_road_km'] * 100).round(1)

# Save filtered GeoJSON
gdf_filtered.to_file('outputs/exports/latvia_municipalities_only.geojson', driver='GeoJSON', encoding='utf-8')
print(f"\n✓ Saved: outputs/exports/latvia_municipalities_only.geojson ({len(gdf_filtered)} features)")

# Create completeness CSV
csv_data = gdf_filtered[['municipality_name', 'osm_road_km', 'official_road_km', 'completeness_pct']].copy()
csv_data.columns = ['municipality_name', 'osm_road_km', 'official_road_km', 'completeness_pct']
csv_data = csv_data.sort_values('municipality_name')

# Add totals row
totals = {
    'municipality_name': 'TOTAL',
    'osm_road_km': csv_data['osm_road_km'].sum(),
    'official_road_km': csv_data['official_road_km'].sum(),
    'completeness_pct': (csv_data['osm_road_km'].sum() / csv_data['official_road_km'].sum() * 100).round(1)
}
csv_data = pd.concat([csv_data, pd.DataFrame([totals])], ignore_index=True)

csv_data.to_csv('outputs/exports/completeness.csv', index=False, encoding='utf-8')
print(f"✓ Saved: outputs/exports/completeness.csv")

print(f"\nSummary:")
print(f"  Municipalities: {len(gdf_filtered)}")
print(f"  OSM Roads: {csv_data.iloc[-1]['osm_road_km']:,.0f} km")
print(f"  Official Roads: {csv_data.iloc[-1]['official_road_km']:,.0f} km")
print(f"  Average Completeness: {csv_data.iloc[-1]['completeness_pct']:.1f}%")
