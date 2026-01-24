#!/usr/bin/env python3
"""
Create fuzzy mapping between LAU1 names and Library.csv names (80% threshold)
"""

import pandas as pd
import geopandas as gpd
from difflib import SequenceMatcher

print("=" * 60)
print("Library Fuzzy Match (80% threshold)")
print("=" * 60)
print()

# Load LAU1 GeoJSON names
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
lau1_names = sorted(gdf['municipality_name'].unique())

# Load Library.csv
df_lib = pd.read_csv('data/raw/Library.csv', skiprows=1)
df_lib = df_lib[df_lib['Rādītāji'] == 'Bibliotēku skaits'].copy()
df_lib = df_lib[df_lib['Teritoriālā vienība'] != 'Latvija']  # Exclude total row
df_lib['library_count'] = pd.to_numeric(df_lib['2024'], errors='coerce')
official_names = sorted(df_lib['Teritoriālā vienība'].unique())

# Fuzzy match function
def fuzzy_ratio(s1, s2):
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

# Perform fuzzy matching
mapping = {}
for lau1_name in lau1_names:
    best_match = None
    best_score = 0
    
    for official_name in official_names:
        score = fuzzy_ratio(lau1_name, official_name)
        if score > best_score:
            best_score = score
            best_match = official_name
    
    if best_score >= 0.80:
        mapping[lau1_name] = best_match

# Create result table
results = []
for lau1_name in sorted(mapping.keys()):
    official_name = mapping[lau1_name]
    library_count = df_lib[df_lib['Teritoriālā vienība'] == official_name]['library_count'].values[0]
    
    results.append({
        'LAU1_Name': lau1_name,
        'Official_Name': official_name,
        'Official_Library_Count': int(library_count),
        'Similarity_%': int(fuzzy_ratio(lau1_name, official_name) * 100)
    })

df_result = pd.DataFrame(results).sort_values('LAU1_Name').reset_index(drop=True)

# Save
output_path = 'outputs/exports/library_name_mapping_80percent.csv'
df_result.to_csv(output_path, index=False)

print(df_result.to_string(index=False))
print("\n" + "=" * 60)
print(f"✓ Matched {len(mapping)} municipalities")
print(f"✓ Total libraries matched: {df_result['Official_Library_Count'].sum()}")
print(f"✓ Saved mapping to: {output_path}")
print("=" * 60)
