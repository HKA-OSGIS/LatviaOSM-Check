#!/usr/bin/env python3
"""Create mapping between GeoJSON novads names and CSV municipality names."""

# Mapping from GeoJSON genitive/plural form to CSV nominative singular form
NOVADS_TO_MUNICIPALITY = {
    # Genitive/plural forms (from GeoJSON) -> Nominative singular (from CSV/TRS020)
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
    'Jēkabpils novads': 'Jēkabpils',  # This one might already match
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
    'Saldus novads': 'Saldus',  # Already matches
    'Saulkrastu novads': 'Saulkrasti',
    'Siguldas novads': 'Sigulda',
    'Smiltenes novads': 'Smiltene',
    'Talsu novads': 'Talsi',
    'Tukuma novads': 'Tukums',
    'Valkas novads': 'Valka',
    'Valmieras novads': 'Valmiera',
    'Varakļānu novads': 'Varakļāni',
    'Ventspils novads': 'Ventspils',  # Already matches
    'Ādažu novads': 'Ādaži',
    'Ķekavas novads': 'Ķekava',
}

print("Municipality Name Mapping (GeoJSON -> CSV)")
print("=" * 60)
for geojson_name, csv_name in sorted(NOVADS_TO_MUNICIPALITY.items()):
    print(f"{geojson_name:30} -> {csv_name}")

print(f"\nTotal mappings: {len(NOVADS_TO_MUNICIPALITY)}")
