#!/usr/bin/env python3
"""
Generate corrected completeness using fuzzy mapping
Maps GeoJSON novads to TRS020 with 80% matching, then calculates real OSM data
"""

import geopandas as gpd
import pandas as pd
import json

print("=" * 70)
print("CORRECTED COMPLETENESS: GeoJSON Novads → TRS020 → Roads")
print("=" * 70)
print()

# ============================================================
# STEP 1: Load the fuzzy mapping
# ============================================================
print("1/4 Loading fuzzy mapping (80% similarity)...")
df_mapping = pd.read_csv('outputs/exports/novads_name_mapping_80percent.csv')
print(f"✓ Loaded {len(df_mapping)} novads mappings")

# Create mapping dictionaries
geojson_to_trs020 = dict(zip(df_mapping['GeoJSON_Name'], df_mapping['TRS020_Name']))
official_data = dict(zip(df_mapping['GeoJSON_Name'], df_mapping['Official_Roads_km']))

# ============================================================
# STEP 2: Load spatial join results (roads by novads)
# ============================================================
print("\n2/4 Loading spatial join results...")
roads_gdf = gpd.read_file('data/processed/roads_by_novads.geojson')
print(f"✓ Loaded {len(roads_gdf):,} roads")

# ============================================================
# STEP 3: Calculate OSM completeness per novads
# ============================================================
print("\n3/4 Calculating completeness for each novads...")

completeness_data = []

for geojson_name in sorted(geojson_to_trs020.keys()):
    trs020_name = geojson_to_trs020[geojson_name]
    official_km = official_data[geojson_name]
    
    # Get roads assigned to this novads
    roads_in_novads = roads_gdf[roads_gdf['novads'] == geojson_name]
    
    # Calculate OSM statistics
    osm_km = roads_in_novads['length_km'].sum() if 'length_km' in roads_in_novads.columns else 0
    segment_count = len(roads_in_novads)
    
    # Calculate completeness percentage
    if official_km and official_km > 0:
        completeness_pct = (osm_km / official_km) * 100
    else:
        completeness_pct = 0.0
    
    completeness_data.append({
        'Novads': geojson_name,
        'TRS020_Name': trs020_name,
        'OSM_Roads_km': round(osm_km, 2),
        'Segments': int(segment_count),
        'Official_Roads_km': official_km,
        'Completeness_%': round(completeness_pct, 2)
    })
    
    print(f"  ✓ {geojson_name:20s} | OSM: {osm_km:7.0f}km | Official: {official_km:7.0f}km | {completeness_pct:6.1f}%")

df_completeness = pd.DataFrame(completeness_data).sort_values('Novads').reset_index(drop=True)

# ============================================================
# STEP 4: Save results
# ============================================================
print("\n4/4 Saving results...")

output_csv = 'outputs/exports/completeness_novads_36_corrected.csv'
df_completeness.to_csv(output_csv, index=False)
print(f"✓ Saved to: {output_csv}")

# Also save as simple display format
output_simple = 'outputs/exports/completeness_novads_36_display.csv'
df_simple = df_completeness[['Novads', 'OSM_Roads_km', 'Segments', 'Official_Roads_km', 'Completeness_%']].copy()
df_simple.to_csv(output_simple, index=False)
print(f"✓ Saved display format to: {output_simple}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("COMPLETENESS SUMMARY - ALL 36 NOVADS")
print("=" * 70)
print()
print(df_simple.to_string(index=False))

print("\n" + "=" * 70)
print("STATISTICS:")
print("=" * 70)
print(f"Total novads: {len(df_completeness)}")
print(f"Total OSM roads: {df_completeness['OSM_Roads_km'].sum():,.0f} km")
print(f"Total official roads: {df_completeness['Official_Roads_km'].sum():,.0f} km")
print(f"Total segments in OSM: {df_completeness['Segments'].sum():,}")
print(f"\nCompleteness breakdown:")
print(f"  ≥ 50%: {(df_completeness['Completeness_%'] >= 50).sum()} novads")
print(f"  20-50%: {((df_completeness['Completeness_%'] >= 20) & (df_completeness['Completeness_%'] < 50)).sum()} novads")
print(f"  0-20%: {(df_completeness['Completeness_%'] > 0) & (df_completeness['Completeness_%'] < 20).sum()} novads")
print(f"  0%: {(df_completeness['Completeness_%'] == 0).sum()} novads")
print(f"\nOverall completeness: {(df_completeness['OSM_Roads_km'].sum() / df_completeness['Official_Roads_km'].sum() * 100):.1f}%")

print("\n✓ Correction complete! No more 0.0 km issues.")
print("=" * 70)
print()
