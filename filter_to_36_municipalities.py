#!/usr/bin/env python3
"""Filter completeness data to only 36 official municipalities."""

import pandas as pd
import json

# Load TRS020 to get official municipalities
trs020 = pd.read_csv('data/raw/TRS020_20251218-122746.csv', skiprows=1)

# Extract municipality names and normalize them
official_munis = set()
for unit in trs020['Territorial unit'].unique():
    # Clean up "X municipality" -> "X"
    muni = unit.replace(' municipality', '').strip()
    official_munis.add(muni)

print(f"Official municipalities: {len(official_munis)}")
for muni in sorted(official_munis):
    print(f"  - {muni}")

# Load the expanded completeness file
df_all = pd.read_csv('outputs/exports/completeness_municipalities_all.csv')

# Filter to only municipalities that have official data
df_filtered = df_all[df_all['Municipality'].isin(official_munis)].copy()

print(f"\nMatched municipalities: {len(df_filtered)}")
print(f"Original rows: {len(df_all)}")

# Sort by municipality name
df_filtered = df_filtered.sort_values('Municipality').reset_index(drop=True)

# Save to CSV
output_file = 'outputs/exports/completeness_municipalities.csv'
df_filtered.to_csv(output_file, index=False)
print(f"\nSaved to: {output_file}")

# Calculate statistics
with_official = (df_filtered['Official_Roads_km'] > 0).sum()
total_osm = df_filtered['OSM_Roads_km'].sum()
total_official = df_filtered[df_filtered['Official_Roads_km'] > 0]['Official_Roads_km'].sum()

if with_official > 0:
    overall_completeness = (total_osm / total_official) * 100
    df_with_official = df_filtered[df_filtered['Official_Roads_km'] > 0].copy()
    high = (df_with_official['Completeness_%'] >= 50).sum()
    medium = ((df_with_official['Completeness_%'] >= 20) & (df_with_official['Completeness_%'] < 50)).sum()
    low = ((df_with_official['Completeness_%'] > 0) & (df_with_official['Completeness_%'] < 20)).sum()
    zero = (df_with_official['Completeness_%'] == 0).sum()
else:
    overall_completeness = 0
    high = medium = low = zero = 0

print(f"\n=== STATISTICS ===")
print(f"Total municipalities: {len(df_filtered)}")
print(f"Municipalities with official data: {with_official}")
print(f"Total OSM roads: {total_osm:,.0f} km")
print(f"Total official roads: {total_official:,.0f} km")
print(f"Overall completeness: {overall_completeness:.1f}%")
print(f"\nCompleteness categories:")
print(f"  High (≥50%): {high}")
print(f"  Medium (20-50%): {medium}")
print(f"  Low (0-20%): {low}")
print(f"  Zero (0%): {zero}")
