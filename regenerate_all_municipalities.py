#!/usr/bin/env python3
"""
Regenerate completeness data for ALL municipalities (36-37)
This script expands from the current 30 to include all available municipalities
"""

import pandas as pd
import geopandas as gpd
import json
from pathlib import Path

print("=" * 70)
print("REGENERATING PROJECT FOR ALL MUNICIPALITIES (36-37)")
print("=" * 70)

# Step 1: Load official stats from TRS020
print("\n1. Loading official statistics from TRS020...")
trs020 = pd.read_csv('data/raw/TRS020_20251218-122746.csv', skiprows=1)
print(f"   Loaded {len(trs020)} municipalities")

# Clean up names
trs020['Municipality'] = (trs020['Territorial unit']
    .str.replace(' municipality', '', regex=False)
    .str.replace(' city', '', regex=False)
    .str.strip())

official_stats = trs020[['Municipality', '2024']].copy()
official_stats.columns = ['Municipality', 'Official_Roads_km']
print(f"   Columns: {official_stats.columns.tolist()}")
print(f"   Sample:\n{official_stats.head()}")

# Step 2: Load OSM data by municipality
print("\n2. Loading OSM road data...")
try:
    roads = gpd.read_file('data/processed/roads_by_municipality.geojson')
    osm_agg = roads.groupby('municipality_name').agg({
        'length_km': 'sum',
        'osm_id': 'count'
    }).reset_index()
    osm_agg.columns = ['Municipality', 'OSM_Roads_km', 'Segments']
    osm_agg['OSM_Roads_km'] = osm_agg['OSM_Roads_km'].round(2)
    print(f"   Found {len(osm_agg)} municipalities with OSM data")
except:
    print("   ⚠ OSM roads file not found, continuing with official data only")
    osm_agg = pd.DataFrame(columns=['Municipality', 'OSM_Roads_km', 'Segments'])

# Step 3: Merge data
print("\n3. Merging data...")
completeness = pd.merge(
    osm_agg,
    official_stats,
    on='Municipality',
    how='outer'
)

# Fill NaN values
completeness['OSM_Roads_km'] = completeness['OSM_Roads_km'].fillna(0)
completeness['Segments'] = completeness['Segments'].fillna(0).astype(int)
completeness['Official_Roads_km'] = completeness['Official_Roads_km'].fillna(0)

# Calculate completeness
completeness['Completeness_%'] = (
    completeness['OSM_Roads_km'] / completeness['Official_Roads_km'] * 100
).round(2)

# Handle division by zero
completeness['Completeness_%'] = completeness['Completeness_%'].replace([float('inf'), float('-inf')], 0)

# Sort by municipality name
completeness = completeness.sort_values('Municipality').reset_index(drop=True)

print(f"   Merged dataset: {len(completeness)} total records")
print(f"\n   With OSM data: {(completeness['OSM_Roads_km'] > 0).sum()}")
print(f"   Without OSM data: {(completeness['OSM_Roads_km'] == 0).sum()}")

# Step 4: Save to CSV
print("\n4. Saving completeness data...")
output_csv = 'outputs/exports/completeness_municipalities_all.csv'
completeness.to_csv(output_csv, index=False)
print(f"   ✓ Saved: {output_csv}")
print(f"   Total municipalities: {len(completeness)}")

# Step 5: Show summary statistics
print("\n5. Summary Statistics:")
if completeness['Official_Roads_km'].sum() > 0:
    total_osm = completeness['OSM_Roads_km'].sum()
    total_official = completeness['Official_Roads_km'].sum()
    avg_completeness = (total_osm / total_official * 100) if total_official > 0 else 0
    
    print(f"   Total OSM Roads: {total_osm:.2f} km")
    print(f"   Total Official Roads: {total_official:.2f} km")
    print(f"   Average Completeness: {avg_completeness:.2f}%")
    print(f"   Range: {completeness[completeness['Completeness_%'] > 0]['Completeness_%'].min():.1f}% - {completeness['Completeness_%'].max():.1f}%")

print(f"\n6. Municipalities ({len(completeness)} total):")
for idx, row in completeness.iterrows():
    osm_val = f"{row['OSM_Roads_km']:.0f}km" if row['OSM_Roads_km'] > 0 else "—"
    off_val = f"{row['Official_Roads_km']:.0f}km" if row['Official_Roads_km'] > 0 else "—"
    comp_val = f"{row['Completeness_%']:.1f}%" if row['Official_Roads_km'] > 0 else "—"
    print(f"   {idx+1:2d}. {row['Municipality']:25s} | OSM: {osm_val:8s} | Official: {off_val:8s} | Completeness: {comp_val:6s}")

print("\n" + "=" * 70)
print("✓ Regeneration complete!")
print("=" * 70)
