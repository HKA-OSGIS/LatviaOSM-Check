#!/usr/bin/env python3
"""
Quick fuzzy join without spatial operations (for testing)
"""

import pandas as pd
from difflib import SequenceMatcher

print("=" * 60)
print("Fuzzy Match Results (80% threshold)")
print("=" * 60)
print()

# Load GeoJSON names
import geopandas as gpd
gdf = gpd.read_file('data/raw/municipalities.geojson')
geojson_names = sorted(gdf['shapeName'].unique())

# Load TRS020
df_trs = pd.read_csv('data/raw/TRS020_20251218-165232.csv', skiprows=1)
df_trs['novads'] = df_trs['Teritoriālā vienība'].str.replace(' novads', '').str.strip()
df_trs = df_trs.rename(columns={'2024': 'Official_Roads_km'})
trs020_names = sorted(df_trs['novads'].unique())

# Fuzzy match
def fuzzy_ratio(s1, s2):
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

mapping = {}
for gname in geojson_names:
    best_match = None
    best_score = 0
    for tname in trs020_names:
        score = fuzzy_ratio(gname, tname)
        if score > best_score:
            best_score = score
            best_match = tname
    
    if best_score >= 0.80:
        mapping[gname] = best_match

# Create result table
results = []
for gname in sorted(mapping.keys()):
    tname = mapping[gname]
    official = df_trs[df_trs['novads'] == tname]['Official_Roads_km'].values[0]
    
    results.append({
        'GeoJSON_Name': gname,
        'TRS020_Name': tname,
        'Official_Roads_km': official,
        'Similarity_%': int(fuzzy_ratio(gname, tname) * 100)
    })

df_result = pd.DataFrame(results).sort_values('GeoJSON_Name').reset_index(drop=True)

# Save
df_result.to_csv('outputs/exports/novads_name_mapping_80percent.csv', index=False)

print(df_result.to_string(index=False))
print("\n" + "=" * 60)
print(f"✓ Matched {len(mapping)} novads")
print(f"✓ Saved mapping to: outputs/exports/novads_name_mapping_80percent.csv")
print("=" * 60)
