#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse complete official Latvian road statistics (TRS020_20251218-012055.csv)
Converts the official data format to usable statistics by municipality and region
"""

import pandas as pd
import re
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("Processing Complete Official Road Statistics (TRS020 - Full 2024)")
print("=" * 70)
print()

# Read the official data
print("1/5 Reading complete official statistics file...")
df = pd.read_csv('data/raw/TRS020_20251218-012055.csv', skiprows=2)
print(f"[OK] Loaded {len(df)} rows")

# Show what we have
print()
print("2/5 Analyzing data structure...")
print(f"  Total rows: {len(df)}")
print(f"  Unique territories: {df['Territorial unit'].nunique()}")
print(f"  Sample territories:")
territories = df['Territorial unit'].unique()
for i, t in enumerate(territories[:10]):
    print(f"    {i+1}. {t}")

# Clean column names
df.columns = ['territorial_unit', 'surface_type', 'indicator', 'length_2024']
print(f"[OK] Columns: {list(df.columns)}")

print()
print("3/5 Cleaning and standardizing data...")

# Create municipality_name column with better parsing
df['municipality_name'] = df['territorial_unit'].str.strip()

# Filter to get only municipality/region data, not breakdowns
# We want total rows (where indicator is 'Total')
df_filtered = df[df['indicator'] == 'Total'].copy()
print(f"  Total rows: {len(df)} → Filtered to 'Total' indicator: {len(df_filtered)}")

# Further filter: keep only the aggregate rows (surface_type = 'Total')
df_final = df_filtered[df_filtered['surface_type'] == 'Total'].copy()
print(f"  With 'Total' surface type: {len(df_final)}")

# Handle missing values (represented as "…" or "-")
df_final['length_2024'] = pd.to_numeric(df_final['length_2024'], errors='coerce')

# Remove rows with no data
df_final = df_final.dropna(subset=['length_2024'])
print(f"  After removing missing values: {len(df_final)}")

# Clean territory names
def clean_territory_name(name):
    # Remove "statistical region" and date notes
    name = re.sub(r'\s*statistical region.*', '', name)
    name = re.sub(r'\s*\(before.*\)', '', name)
    name = re.sub(r'\s*\(from.*\)', '', name)
    name = re.sub(r'\s+', ' ', name)  # Remove extra spaces
    return name.strip()

df_final['municipality_name'] = df_final['municipality_name'].apply(clean_territory_name)

print()
print("4/5 Aggregating by territory...")

# Group by municipality and sum (in case there are duplicates after cleaning)
road_stats = df_final.groupby('municipality_name')['length_2024'].sum().reset_index()
road_stats.columns = ['municipality_name', 'road_length_km']
road_stats = road_stats.sort_values('road_length_km', ascending=False).reset_index(drop=True)

print(f"[OK] Aggregated to {len(road_stats)} unique territories")

# Show statistics
print()
print("Statistics of official road data:")
print(f"  Total territories with data: {len(road_stats)}")
print(f"  Total road length: {road_stats['road_length_km'].sum():.2f} km")
print(f"  Average per territory: {road_stats['road_length_km'].mean():.2f} km")
print(f"  Median: {road_stats['road_length_km'].median():.2f} km")
print(f"  Max: {road_stats['road_length_km'].max():.2f} km ({road_stats.iloc[0]['municipality_name']})")
print(f"  Min: {road_stats['road_length_km'].min():.2f} km ({road_stats.iloc[-1]['municipality_name']})")

# Special: check for Riga
riga_data = road_stats[road_stats['municipality_name'].str.contains('Riga', case=False, na=False)]
print()
print(f"[OK] Rīga found! Entries: {len(riga_data)}")
if len(riga_data) > 0:
    for idx, row in riga_data.iterrows():
        print(f"    {row['municipality_name']:40s} {row['road_length_km']:8.1f} km")

print()
print("5/5 Saving to official_road_stats.csv...")
road_stats.to_csv('data/raw/official_road_stats.csv', index=False)
print("[OK] Saved")

print()
print("=" * 70)
print("Top 15 territories by road length:")
print("=" * 70)
print()
top_15 = road_stats.head(15)
for idx, row in top_15.iterrows():
    print(f"  {row['municipality_name']:40s} {row['road_length_km']:8.1f} km")

print()
print("=" * 70)
print("[OK] Conversion complete!")
print("=" * 70)
print()
print("Next steps:")
print("  1. Run: python scripts/05_calculate_completeness.py")
print("  2. Start: python app.py")
print("  3. Open: http://localhost:5000")
