#!/usr/bin/env python3
"""Calculate library completeness percentages"""

import pandas as pd
import geopandas as gpd
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Library Completeness Calculation")
print("=" * 60)

# Load OSM stats
osm_stats = pd.read_csv('outputs/exports/library_stats_by_novads.csv')
print(f"\n✓ Loaded OSM statistics: {len(osm_stats)} units")

# Load official stats
official = pd.read_csv('data/raw/official_library_stats.csv')
print(f"✓ Loaded official statistics: {len(official)} entries")

# Normalize names for matching
def normalize_osm_name(row):
    """Normalize OSM names to match official format"""
    name = row['municipality_name']
    area_type = row['Area_Type']
    
    # For cities: remove possessive suffix (Jelgavas → Jelgava, Jūrmalas → Jūrmala)
    if area_type == 'City':
        if name == 'Jelgavas': return 'Jelgava'
        elif name == 'Jūrmalas': return 'Jūrmala'
        elif name == 'Liepājas': return 'Liepāja'
        elif name == 'Rēzeknes': return 'Rēzekne'
        return name  # Rīga, Daugavpils, Ventspils stay as-is
    
    # For municipalities: add " novads" suffix
    else:
        if name.endswith(' novads'):
            return name  # Already has suffix (e.g., Salaspils novads)
        
        # Direct mapping - add appropriate genitive + novads
        municipality_map = {
            'Ādaži': 'Ādažu novads',
            'Aizkraukle': 'Aizkraukles novads',
            'Alūksne': 'Alūksnes novads',
            'Augšdaugava': 'Augšdaugavas novads',
            'Balvi': 'Balvu novads',
            'Bauska': 'Bauskas novads',
            'Cēsis': 'Cēsu novads',
            'Dienvidkurzeme': 'Dienvidkurzemes novads',
            'Dobele': 'Dobeles novads',
            'Gulbene': 'Gulbenes novads',
            'Jelgava': 'Jelgavas novads',
            'Jēkabpils': 'Jēkabpils novads',
            'Ķekava': 'Ķekavas novads',
            'Krāslava': 'Krāslavas novads',
            'Kuldīga': 'Kuldīgas novads',
            'Limbaži': 'Limbažu novads',
            'Līvāni': 'Līvānu novads',
            'Ludza': 'Ludzas novads',
            'Madona': 'Madonas novads',
            'Mārupe': 'Mārupes novads',
            'Ogre': 'Ogres novads',
            'Olaine': 'Olaines novads',
            'Preiļi': 'Preiļu novads',
            'Rēzekne': 'Rēzeknes novads',
            'Ropaži': 'Ropažu novads',
            'Saldus': 'Saldus novads',
            'Saulkrasti': 'Saulkrastu novads',
            'Sigulda': 'Siguldas novads',
            'Smiltene': 'Smiltenes novads',
            'Talsi': 'Talsu novads',
            'Tukums': 'Tukuma novads',
            'Valka': 'Valkas novads',
            'Valmiera': 'Valmieras novads',
            'Varakļāni': 'Varakļānu novads',
            'Ventspils': 'Ventspils novads'
        }
        
        return municipality_map.get(name, name)

# Load OSM stats
osm_stats = pd.read_csv('outputs/exports/library_stats_by_novads.csv')
print(f"\n✓ Loaded OSM statistics: {len(osm_stats)} units")

# Load official stats
official = pd.read_csv('data/raw/official_library_stats.csv')
print(f"✓ Loaded official statistics: {len(official)} entries")

# Normalize OSM names to match official format
osm_stats['official_name'] = osm_stats.apply(normalize_osm_name, axis=1)

# Merge OSM with official data
merged = pd.merge(
    official,
    osm_stats[['official_name', 'osm_library_count']],
    left_on='municipality_name',
    right_on='official_name',
    how='left'
)

# Fill missing OSM counts with 0
merged['osm_library_count'] = merged['osm_library_count'].fillna(0).astype(int)

# Calculate completeness
merged['completeness_%'] = ((merged['osm_library_count'] / merged['library_count']) * 100).fillna(0).round(2)

# Handle division by zero (units with no official libraries)
merged.loc[merged['library_count'] == 0, 'completeness_%'] = 0

# Select output columns
output = merged[['municipality_name', 'Area_Type', 'osm_library_count', 'library_count']]
output.columns = ['municipality_name', 'Area_Type', 'osm_library_count', 'official_library_count']
output['completeness_%'] = merged['completeness_%']
output = output.sort_values('completeness_%', ascending=False)

# Save
output.to_csv('outputs/exports/completeness_libraries.csv', index=False)
print(f"✓ Saved: outputs/exports/completeness_libraries.csv")

print("\n" + "=" * 60)
print("Top 10 Most Complete:")
print(output[output['official_library_count'] > 0].head(10)[['municipality_name', 'Area_Type', 'osm_library_count', 'official_library_count', 'completeness_%']].to_string(index=False))

print("\n" + "=" * 60)
print("Bottom 10 (Least Complete with official libraries):")
print(output[output['official_library_count'] > 0].tail(10)[['municipality_name', 'Area_Type', 'osm_library_count', 'official_library_count', 'completeness_%']].to_string(index=False))

print("\n" + "=" * 60)
print("Summary Statistics:")
valid_data = output[output['official_library_count'] > 0]
print(f"  Units with libraries: {len(valid_data)}")
print(f"  Average completeness: {valid_data['completeness_%'].mean():.2f}%")
print(f"  Median completeness: {valid_data['completeness_%'].median():.2f}%")
print(f"  Total OSM libraries: {output['osm_library_count'].sum():,}")
print(f"  Total official libraries: {output['official_library_count'].sum():,}")
print(f"  Overall completeness: {(output['osm_library_count'].sum() / output['official_library_count'].sum() * 100):.2f}%")
print(f"  Units with 100% completeness: {len(output[output['completeness_%'] >= 100])}")
print(f"  Units with 0% completeness: {len(output[(output['completeness_%'] == 0) & (output['official_library_count'] > 0)])}")
print("=" * 60)
