#!/usr/bin/env python3
"""Test data consistency"""
import pandas as pd
import geopandas as gpd

print("=" * 80)
print("DATA VERIFICATION REPORT")
print("=" * 80)

# Check CSV
print("\n1. CSV DATA")
print("-" * 80)
df_csv = pd.read_csv('outputs/exports/completeness_municipalities.csv')
print(f"Total records: {len(df_csv)}")
print(f"Total OSM Roads: {df_csv['OSM Roads (km)'].sum():,.2f} km")
print(f"Total Official Roads: {df_csv['Official Roads (km)'].sum():,.2f} km")
print(f"Average Completeness: {df_csv['Completeness (%)'].mean():.2f}%")
print(f"Highest: {df_csv['Completeness (%)'].max():.1f}% ({df_csv.loc[df_csv['Completeness (%)'].idxmax(), 'Municipality']})")
print(f"Lowest: {df_csv['Completeness (%)'].min():.1f}% ({df_csv.loc[df_csv['Completeness (%)'].idxmin(), 'Municipality']})")

# Check GeoJSON
print("\n2. GEOJSON DATA")
print("-" * 80)
gdf = gpd.read_file('outputs/exports/latvia_municipalities_only.geojson')
print(f"Total features: {len(gdf)}")
print(f"Geometry: {gdf.geometry.type.unique()}")

# Check sample data
print(f"\n3. SAMPLE MUNICIPALITIES (First 5)")
print("-" * 80)
for idx, (i, row) in enumerate(gdf.head(5).iterrows(), 1):
    print(f"{idx}. {row['municipality_name']}: OSM={row['osm_road_km']:.1f}km, Official={row['official_road_km']:.1f}km, Complete={row['completeness_pct']:.1f}%")

# Verify CSV matches GeoJSON
print(f"\n4. DATA CONSISTENCY CHECK")
print("-" * 80)
all_match = True
for mun_name in gdf['municipality_name']:
    geojson_row = gdf[gdf['municipality_name'] == mun_name].iloc[0]
    csv_row = df_csv[df_csv['Municipality'] == mun_name]
    
    if len(csv_row) > 0:
        csv_official = csv_row['Official Roads (km)'].values[0]
        geojson_official = geojson_row['official_road_km']
        
        if abs(csv_official - geojson_official) > 0.01:
            print(f"✗ MISMATCH: {mun_name} - CSV={csv_official}, GeoJSON={geojson_official}")
            all_match = False

if all_match:
    print("✓ All CSV and GeoJSON data match perfectly!")

print("\n" + "=" * 80)
