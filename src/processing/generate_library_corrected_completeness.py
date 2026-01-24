#!/usr/bin/env python3
"""
Generate corrected library completeness using fuzzy mapping
Maps LAU1 names to Library.csv with 80% matching, then calculates OSM completeness
"""

import geopandas as gpd
import pandas as pd
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("CORRECTED LIBRARY COMPLETENESS: LAU1 → Library.csv → OSM")
print("=" * 70)
print()

# ============================================================
# STEP 1: Load the fuzzy mapping
# ============================================================
print("1/4 Loading fuzzy mapping (80% similarity)...")
df_mapping = pd.read_csv('outputs/exports/library_name_mapping_80percent.csv')
print(f"✓ Loaded {len(df_mapping)} municipality mappings")

# Create mapping dictionaries
lau1_to_official = dict(zip(df_mapping['LAU1_Name'], df_mapping['Official_Name']))
official_data = dict(zip(df_mapping['LAU1_Name'], df_mapping['Official_Library_Count']))

# ============================================================
# STEP 2: Load spatial join results (libraries by novads)
# ============================================================
print("\n2/4 Loading spatial join results...")
libraries_gdf = gpd.read_file('data/processed/libraries_by_novads.geojson')
print(f"✓ Loaded {len(libraries_gdf):,} libraries")

# ============================================================
# STEP 3: Calculate OSM completeness per municipality
# ============================================================
print("\n3/4 Calculating completeness for each municipality...")

completeness_data = []

for lau1_name in sorted(lau1_to_official.keys()):
    official_name = lau1_to_official[lau1_name]
    official_count = official_data[lau1_name]
    
    # Get libraries assigned to this municipality
    libs_in_municipality = libraries_gdf[libraries_gdf['novads'] == lau1_name]
    
    # Calculate OSM statistics
    osm_count = len(libs_in_municipality)
    
    # Calculate completeness percentage
    if official_count and official_count > 0:
        completeness_pct = (osm_count / official_count) * 100
    else:
        completeness_pct = 0.0
    
    # Determine area type
    area_type = 'City' if lau1_name in ['Rīga', 'Daugavpils', 'Jelgava', 'Jūrmala', 'Liepāja', 'Rēzekne', 'Ventspils'] else 'Municipality'
    
    completeness_data.append({
        'Municipality': lau1_name,
        'Official_Name': official_name,
        'OSM_Libraries': int(osm_count),
        'Official_Libraries': int(official_count),
        'Completeness_%': round(completeness_pct, 2),
        'Area_Type': area_type
    })
    
    print(f"  ✓ {lau1_name:25s} | OSM: {osm_count:3d} | Official: {official_count:3d} | {completeness_pct:6.1f}%")

df_completeness = pd.DataFrame(completeness_data).sort_values('Completeness_%', ascending=False).reset_index(drop=True)

# ============================================================
# STEP 4: Save results and create GeoJSON
# ============================================================
print("\n4/4 Saving results...")

# Save CSV
output_csv = 'outputs/exports/completeness_libraries_corrected.csv'
df_completeness.to_csv(output_csv, index=False)
print(f"✓ Saved to: {output_csv}")

# Load LAU1 geometries and merge
lau1 = gpd.read_file('outputs/exports/latvia_lau1.geojson')
lau1_with_libraries = lau1[['municipality_name', 'geometry']].merge(
    df_completeness,
    left_on='municipality_name',
    right_on='Municipality',
    how='left'
)

# Fill missing values
lau1_with_libraries['OSM_Libraries'] = lau1_with_libraries['OSM_Libraries'].fillna(0).astype(int)
lau1_with_libraries['Official_Libraries'] = lau1_with_libraries['Official_Libraries'].fillna(0).astype(int)
lau1_with_libraries['Completeness_%'] = lau1_with_libraries['Completeness_%'].fillna(0)
lau1_with_libraries['Area_Type'] = lau1_with_libraries['Area_Type'].fillna('Municipality')

# Save GeoJSON
output_geojson = 'outputs/exports/latvia_lau1_libraries_corrected.geojson'
lau1_with_libraries.to_file(output_geojson, driver='GeoJSON')
print(f"✓ Saved GeoJSON to: {output_geojson}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("LIBRARY COMPLETENESS SUMMARY")
print("=" * 70)
print()

# Display simple format
df_simple = df_completeness[['Municipality', 'OSM_Libraries', 'Official_Libraries', 'Completeness_%']].copy()
print(df_simple.to_string(index=False))

print("\n" + "=" * 70)
print("STATISTICS:")
print("=" * 70)
print(f"Total municipalities: {len(df_completeness)}")
print(f"Total OSM libraries: {df_completeness['OSM_Libraries'].sum():,}")
print(f"Total official libraries: {df_completeness['Official_Libraries'].sum():,}")
print(f"Average completeness: {df_completeness['Completeness_%'].mean():.1f}%")
print(f"Municipalities with >0% coverage: {len(df_completeness[df_completeness['Completeness_%'] > 0])}")
print("=" * 70)
