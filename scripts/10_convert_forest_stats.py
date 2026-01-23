#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert official forest statistics to standardized format
Processes Forest.csv with municipality and city forest area data
"""

import pandas as pd
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("Processing Official Forest Statistics (Forest Land Area)")
print("=" * 70)
print()

# Read the forest CSV
print("1/4 Reading forest statistics file...")
df = pd.read_csv('data/raw/Forest.csv', skiprows=1)
print(f"✓ Loaded {len(df)} rows")

# Show structure
print("\n2/4 Analyzing data structure...")
print(f"  Columns: {list(df.columns)}")
print(f"  Unique territories: {df['Teritoriālā vienība'].nunique()}")

# Filter to only "Pavisam" (Total) forest type for total forest area
print("\n3/4 Filtering to total forest land area...")
df_total = df[df['Meža īpašuma forma'] == 'Pavisam'].copy()
print(f"  Filtered from {len(df)} to {len(df_total)} rows (total forest only)")

# Rename columns
df_total = df_total.rename(columns={
    'Teritoriālā vienība': 'municipality_name',
    '2024': 'forest_area_ha'
})

# Keep only needed columns
df_total = df_total[['municipality_name', 'forest_area_ha']]

# Convert hectares to square kilometers (1 ha = 0.01 km²)
df_total['forest_area_km2'] = (df_total['forest_area_ha'] / 100).round(2)

# Remove rows with 0 area
df_total = df_total[df_total['forest_area_ha'] > 0].copy()

# Normalize municipality names to match LAU1 format
# Remove "novads" suffix and convert to nominative case where needed
name_mapping = {
    'Ādažu novads': 'Ādaži',
    'Aizkraukles novads': 'Aizkraukle',
    'Alūksnes novads': 'Alūksne',
    'Augšdaugavas novads': 'Augšdaugava',
    'Balvu novads': 'Balvi',
    'Bauskas novads': 'Bauska',
    'Cēsu novads': 'Cēsis',
    'Dienvidkurzemes novads': 'Dienvidkurzeme',
    'Dobeles novads': 'Dobele',
    'Gulbenes novads': 'Gulbene',
    'Jelgavas novads': 'Jelgava',
    'Jēkabpils novads': 'Jēkabpils',
    'Krāslavas novads': 'Krāslava',
    'Kuldīgas novads': 'Kuldīga',
    'Ķekavas novads': 'Ķekava',
    'Limbažu novads': 'Limbaži',
    'Līvānu novads': 'Līvāni',
    'Ludzas novads': 'Ludza',
    'Madonas novads': 'Madona',
    'Mārupes novads': 'Mārupe',
    'Ogres novads': 'Ogre',
    'Olaines novads': 'Olaine',
    'Preiļu novads': 'Preiļi',
    'Rēzeknes novads': 'Rēzekne',
    'Ropažu novads': 'Ropaži',
    'Salaspils novads': 'Salaspils novads',
    'Saldus novads': 'Saldus',
    'Saulkrastu novads': 'Saulkrasti',
    'Siguldas novads': 'Sigulda',
    'Smiltenes novads': 'Smiltene',
    'Talsu novads': 'Talsi',
    'Tukuma novads': 'Tukums',
    'Valkas novads': 'Valka',
    'Valmieras novads': 'Valmiera',
    'Varakļānu novads': 'Varakļāni',
    'Ventspils novads': 'Ventspils',
    # Cities (keep genitive for cities to match completeness_municipalities.csv)
    'Daugavpils pilsēta': 'Daugavpils',
    'Jelgavas pilsēta': 'Jelgavas',
    'Jūrmalas pilsēta': 'Jūrmalas',
    'Liepājas pilsēta': 'Liepājas',
    'Rēzeknes pilsēta': 'Rēzeknes',
    'Rīgas pilsēta': 'Rīga',
    'Ventspils pilsēta': 'Ventspils'
}

df_total['municipality_name'] = df_total['municipality_name'].replace(name_mapping)

print(f"✓ Processed {len(df_total)} municipalities and cities")

print("\n4/4 Saving processed data...")
df_total.to_csv('data/raw/official_forest_stats.csv', index=False)
print("✓ Saved: data/raw/official_forest_stats.csv")

# Show statistics
print("\n" + "=" * 70)
print("Statistics Summary:")
print(f"  Total entries: {len(df_total)}")
print(f"  Total forest area: {df_total['forest_area_ha'].sum():,.0f} ha ({df_total['forest_area_km2'].sum():,.2f} km²)")
print(f"  Average per area: {df_total['forest_area_ha'].mean():,.0f} ha ({df_total['forest_area_km2'].mean():,.2f} km²)")
print()
print("Top 10 municipalities by forest area:")
print(df_total.nlargest(10, 'forest_area_ha')[['municipality_name', 'forest_area_km2']].to_string(index=False))
print()
print("Cities:")
cities = df_total[df_total['municipality_name'].isin(['Rīga', 'Daugavpils', 'Jelgava', 'Jūrmala', 'Liepāja', 'Rēzekne', 'Ventspils', 'Valmiera', 'Jēkabpils', 'Ogre'])]
print(cities[['municipality_name', 'forest_area_km2']].to_string(index=False))
print("=" * 70)
