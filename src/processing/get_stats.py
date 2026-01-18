#!/usr/bin/env python3
"""Get statistics summary from completeness data."""

import pandas as pd
from pathlib import Path

# Use the correct CSV file
csv_file = Path('outputs/exports/completeness_municipalities.csv')

if not csv_file.exists():
    print(f"Error: {csv_file} not found")
    print("Run generate_corrected_completeness.py first")
    exit(1)

df = pd.read_csv(csv_file)

df = pd.read_csv(csv_file)

# Rename columns if needed (handle both old and new formats)
if 'Official_Roads_km' in df.columns:
    df = df.rename(columns={
        'Official_Roads_km': 'official_road_km',
        'OSM_Roads_km': 'osm_road_km',
        'Completeness_%': 'completeness_pct'
    })

# Total municipalities
total = len(df)

# Municipalities with official road data (non-zero)
with_official = (df['official_road_km'] > 0).sum()

# Overall completeness
df_with_official = df[df['official_road_km'] > 0].copy()
if len(df_with_official) > 0:
    overall_completeness = (df_with_official['osm_road_km'].sum() / df_with_official['official_road_km'].sum()) * 100
    high = (df_with_official['completeness_pct'] >= 50).sum()
    medium = ((df_with_official['completeness_pct'] >= 20) & (df_with_official['completeness_pct'] < 50)).sum()
    low = ((df_with_official['completeness_pct'] > 0) & (df_with_official['completeness_pct'] < 20)).sum()
    zero = (df_with_official['completeness_pct'] == 0).sum()
else:
    overall_completeness = 0
    high = medium = low = zero = 0

print('=' * 60)
print('LatviaOSM-Check - Statistics Summary')
print('=' * 60)
print(f'Total municipalities: {total}')
print(f'Municipalities with official data: {with_official}')
print(f'Overall completeness: {overall_completeness:.1f}%')
print(f'High (≥50%): {high}')
print(f'Medium (20-50%): {medium}')
print(f'Low (0-20%): {low}')
print(f'Zero (0%): {zero}')
print('=' * 60)
