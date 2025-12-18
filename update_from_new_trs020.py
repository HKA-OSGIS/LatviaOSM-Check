#!/usr/bin/env python3
"""Process new TRS020 file and update completeness statistics."""

import pandas as pd
import json

# Load the new TRS020 file (skip first row which is a title)
trs020 = pd.read_csv('data/raw/TRS020_20251218-165232.csv', skiprows=1)

# Rename columns
trs020.columns = ['Territorial_unit', 'Indicator', 'Total_roads_km']

# Extract municipality name (remove " novads" suffix to match CSV format)
trs020['Municipality'] = trs020['Territorial_unit'].str.replace(' novads', '').str.strip()

# Keep only the total rows
trs020_totals = trs020[trs020['Indicator'] == 'Pavisam'].copy()

print("Official Road Data from TRS020_20251218-165232.csv:")
print(f"Total municipalities: {len(trs020_totals)}")
print(f"Total road km (sum): {trs020_totals['Total_roads_km'].sum():,}")
print("\nMunicipalities:")
for idx, row in trs020_totals.iterrows():
    print(f"  {row['Municipality']}: {row['Total_roads_km']} km")

# Load existing completeness data
df_completeness = pd.read_csv('outputs/exports/completeness_municipalities.csv')

print(f"\nCurrent CSV municipalities: {len(df_completeness)}")

# Update with new official road data
df_updated = df_completeness.copy()

for idx, row in trs020_totals.iterrows():
    muni = row['Municipality']
    official_km = row['Total_roads_km']
    
    # Find matching row in completeness data
    mask = df_updated['Municipality'] == muni
    if mask.any():
        df_updated.loc[mask, 'Official_Roads_km'] = official_km
        # Recalculate completeness
        osm_km = df_updated.loc[mask, 'OSM_Roads_km'].values[0]
        completeness = (osm_km / official_km * 100) if official_km > 0 else 0
        df_updated.loc[mask, 'Completeness_%'] = completeness

# Save updated CSV
df_updated.to_csv('outputs/exports/completeness_municipalities.csv', index=False)

print("\n✓ Updated completeness_municipalities.csv with new TRS020 data")

# Calculate new statistics
with_official = (df_updated['Official_Roads_km'] > 0).sum()
total_osm = df_updated['OSM_Roads_km'].sum()
total_official = df_updated[df_updated['Official_Roads_km'] > 0]['Official_Roads_km'].sum()

if with_official > 0:
    overall_completeness = (total_osm / total_official) * 100
    df_with = df_updated[df_updated['Official_Roads_km'] > 0].copy()
    high = (df_with['Completeness_%'] >= 50).sum()
    medium = ((df_with['Completeness_%'] >= 20) & (df_with['Completeness_%'] < 50)).sum()
    low = ((df_with['Completeness_%'] > 0) & (df_with['Completeness_%'] < 20)).sum()
    zero = (df_with['Completeness_%'] == 0).sum()
else:
    overall_completeness = 0
    high = medium = low = zero = 0

print(f"\n=== UPDATED STATISTICS ===")
print(f"Total municipalities: {len(df_updated)}")
print(f"Total OSM roads: {total_osm:,.0f} km")
print(f"Total official roads: {total_official:,.0f} km")
print(f"Overall completeness: {overall_completeness:.1f}%")
print(f"\nCompleteness breakdown:")
print(f"  High (≥50%): {high}")
print(f"  Medium (20-50%): {medium}")
print(f"  Low (0-20%): {low}")
print(f"  Zero (0%): {zero}")
