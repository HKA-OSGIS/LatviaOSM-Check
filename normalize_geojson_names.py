#!/usr/bin/env python3
"""Update municipalities.geojson to use normalized municipality names."""

import json

# Mapping from GeoJSON genitive/plural form to CSV nominative singular form
NOVADS_TO_MUNICIPALITY = {
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
    'Limbažu novads': 'Limbaži',
    'Ludzas novads': 'Ludza',
    'Līvānu novads': 'Līvāni',
    'Madonas novads': 'Madona',
    'Mārupes novads': 'Mārupe',
    'Ogres novads': 'Ogre',
    'Olaines novads': 'Olaine',
    'Preiļu novads': 'Preiļi',
    'Ropažu novads': 'Ropaži',
    'Rēzeknes novads': 'Rēzekne',
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
    'Ādažu novads': 'Ādaži',
    'Ķekavas novads': 'Ķekava',
}

# Load GeoJSON
input_file = 'data/raw/municipalities.geojson'
output_file = 'data/raw/municipalities.geojson'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update feature names
updated_count = 0
for feature in data.get('features', []):
    props = feature.get('properties', {})
    shape_name = props.get('shapeName', '')
    
    if shape_name in NOVADS_TO_MUNICIPALITY:
        new_name = NOVADS_TO_MUNICIPALITY[shape_name]
        props['shapeName'] = new_name
        updated_count += 1
        print(f"✓ {shape_name} -> {new_name}")

# Save updated GeoJSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Updated {updated_count} features")
print(f"✓ Saved to {output_file}")
