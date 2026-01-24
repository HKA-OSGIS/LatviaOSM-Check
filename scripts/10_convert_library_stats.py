#!/usr/bin/env python3
"""Convert Library.csv to clean CSV format"""

import pandas as pd
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Converting Library Statistics to Clean Format")
print("=" * 60)

# Read the CSV (skip first row which is header description)
df = pd.read_csv('data/raw/Library.csv', skiprows=1, encoding='utf-8')

print(f"\n✓ Loaded {len(df)} rows")
print(f"  Columns: {df.columns.tolist()}")

# Rename columns
df.columns = ['indicator', 'municipality_name', 'library_count']

# Filter only library count rows (all are same indicator)
df = df[df['indicator'] == 'Bibliotēku skaits'].copy()

# Remove Latvia total
df = df[df['municipality_name'] != 'Latvija'].copy()

# Determine Area_Type based on municipality name
def get_area_type(name):
    """Determine if area is City or Municipality"""
    cities = ['Rīga', 'Daugavpils', 'Jelgava', 'Jūrmala', 'Liepāja', 'Rēzekne', 'Ventspils']
    if name in cities:
        return 'City'
    else:
        return 'Municipality'

df['Area_Type'] = df['municipality_name'].apply(get_area_type)

# Clean up special cases like "Madonas novads (no 01.07.2025.)"
df['municipality_name'] = df['municipality_name'].str.replace(r'\s*\(.*\)', '', regex=True)

# Select and reorder columns
output = df[['municipality_name', 'Area_Type', 'library_count']].copy()

# Sort by area type then name
output = output.sort_values(['Area_Type', 'municipality_name'])

# Save cleaned version
output.to_csv('data/raw/official_library_stats.csv', index=False, encoding='utf-8')
print(f"\n✓ Saved: data/raw/official_library_stats.csv")

# Display summary
print("\n" + "=" * 60)
print("Summary:")
print(f"  Cities: {len(output[output['Area_Type'] == 'City'])}")
print(f"  Municipalities: {len(output[output['Area_Type'] == 'Municipality'])}")
print(f"  Total libraries: {output['library_count'].sum():,}")
print("=" * 60)

print("\nSample data:")
print(output.head(10).to_string(index=False))
