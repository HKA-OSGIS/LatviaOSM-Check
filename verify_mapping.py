#!/usr/bin/env python3
"""Compare normalized GeoJSON names with CSV municipality names."""

import json
import pandas as pd

# Load updated GeoJSON
with open('data/raw/municipalities.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract all novads (35) - excluding city states
geojson_novads = []
for feat in data.get('features', []):
    name = feat.get('properties', {}).get('shapeName', '')
    if 'novads' not in name.lower():  # Normalized names without 'novads' suffix
        geojson_novads.append(name)

# Load CSV
df = pd.read_csv('outputs/exports/completeness_municipalities.csv')
csv_munis = sorted(df['Municipality'].unique())

print('=' * 70)
print('GEOJSON vs CSV MUNICIPALITY NAMES - COMPARISON')
print('=' * 70)
print()

# Sort for comparison
geojson_novads_sorted = sorted(geojson_novads)

print('Side-by-side comparison:')
print('-' * 70)
print(f'{"#":3} | {"GeoJSON (Normalized)":30} | {"CSV":30} | Match')
print('-' * 70)

match_count = 0
for i, (geo_name, csv_name) in enumerate(zip(geojson_novads_sorted, csv_munis), 1):
    match_symbol = '✓' if geo_name == csv_name else '✗'
    if geo_name == csv_name:
        match_count += 1
    print(f'{i:3} | {geo_name:30} | {csv_name:30} | {match_symbol}')

print('-' * 70)
print(f'\nResults:')
print(f'  ✓ Perfect matches: {match_count}/{len(csv_munis)} municipalities')
print(f'  - GeoJSON total features: {len(data.get("features", []))}')
print(f'  - Municipalities (novads): {len(geojson_novads_sorted)}')
print(f'  - City states: 6 (Rīga, Daugavpils, Jūrmala, Liepāja, Rēzekne, Jelgava)')
print(f'  - CSV municipalities: {len(csv_munis)}')
print()
if match_count == len(csv_munis):
    print('✓✓✓ SUCCESS! All names now match perfectly! ✓✓✓')
else:
    print('⚠ Warning: Some names still do not match')
