#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create comprehensive Latvia GeoJSON with municipalities AND cities
Merges municipality completeness data with all 43 administrative boundaries
Uses fuzzy matching for automatic name matching
"""

import json
import csv
import sys
import io
from difflib import SequenceMatcher

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("Creating Comprehensive Latvia GeoJSON (Municipalities + Cities)")
print("Using Fuzzy Matching (50% threshold)")
print("=" * 70)
print()

def fuzzy_match_name(shape_name, csv_names, threshold=0.50):
    """
    Find best matching CSV municipality name using fuzzy matching
    Returns (matched_name, confidence) or (None, 0) if no good match
    """
    best_match = None
    best_ratio = 0.0
    
    for csv_name in csv_names:
        ratios = []
        
        # Strip " novads" from CSV for better base comparison
        csv_base = csv_name.replace(' novads', '').strip()
        
        # Direct comparison (full names)
        ratios.append(SequenceMatcher(None, shape_name.lower(), csv_name.lower()).ratio())
        
        # Compare without "novads" suffix (Tukums vs Tukuma)
        ratios.append(SequenceMatcher(None, shape_name.lower(), csv_base.lower()).ratio())
        
        # Try with " novads" added to shapeName
        ratios.append(SequenceMatcher(None, f"{shape_name} novads".lower(), csv_name.lower()).ratio())
        
        # Try possessive form: add 's' (Tukums -> Tukums + s)
        if not shape_name.endswith('s'):
            ratios.append(SequenceMatcher(None, f"{shape_name}s novads".lower(), csv_name.lower()).ratio())
            ratios.append(SequenceMatcher(None, f"{shape_name}s".lower(), csv_base.lower()).ratio())
        
        # Try genitive with 'a' suffix (Tukums -> Tukuma)
        if not shape_name.endswith('a'):
            ratios.append(SequenceMatcher(None, f"{shape_name}a".lower(), csv_base.lower()).ratio())
            ratios.append(SequenceMatcher(None, f"{shape_name}a novads".lower(), csv_name.lower()).ratio())
        
        ratio = max(ratios)
        
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = csv_name
    
    if best_ratio >= threshold:
        return best_match, best_ratio
    return None, 0.0

def normalize_to_novads(name):
    """Convert shapeName to match completeness Municipality format"""
    if not name:
        return name
    
    # Cities stay as-is (these match exactly in CSV)
    cities = ['Daugavpils', 'Jelgava', 'Rēzekne', 'Ventspils', 'Rīga']
    if name in cities:
        return name
    
    # Special cases where shapeName directly matches Municipality in CSV
    # (Salaspils is already "Salaspils novads" in both)
    if name == 'Salaspils novads':
        return name
    
    # Comprehensive manual mapping based on actual data
    # GeoJSON shapeName -> CSV Municipality
    name_mapping = {
        # Cities that end in 'as' genitive in GeoJSON
        'Jelgavas': 'Jelgavas novads',
        'Jūrmalas': 'Jūrmalas novads',  # Not in CSV, will be skipped
        'Liepājas': 'Liepājas novads',  # Not in CSV, will be skipped
        'Rēzeknes': 'Rēzeknes novads',
        
        # Municipalities - irregular possessives
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
        'Jēkabpils': 'Jēkabpils novads',
        'Ķekava': 'Ķekavas novads',  # Not in CSV
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
        'Ropaži': 'Ropažu novads',
        'Saldus': 'Saldus novads',
        'Saulkrasti': 'Saulkrastu novads',
        'Sigulda': 'Siguldas novads',
        'Smiltene': 'Smiltenes novads',
        'Talsi': 'Talsu novads',
        'Tukums': 'Tukuma novads',
        'Valka': 'Valkas novads',
        'Valmiera': 'Valmieras novads',  # Not in CSV
        'Varakļāni': 'Varakļānu novads',
    }
    
    if name in name_mapping:
        return name_mapping[name]
    
    # Fallback: return as-is
    return name

# Step 1: Load all raw boundaries (43 features = 36 novads + 7 cities)
print("1/3 Loading all administrative boundaries...")
with open('data/raw/municipalities.geojson', 'r', encoding='utf-8') as f:
    all_boundaries = json.load(f)
print(f"  Loaded {len(all_boundaries['features'])} total features (municipalities + cities)")

# Step 2: Load completeness data (37 records - 36 novads + maybe 1 city?)
print("\n2/3 Loading completeness data...")
completeness = {}
with open('outputs/exports/completeness_municipalities.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        mun_name = row['Municipality']
        completeness[mun_name] = row

print(f"  Loaded {len(completeness)} completeness records")

# Get list of CSV municipality names for fuzzy matching
csv_municipality_names = list(completeness.keys())

# Step 3: Merge data and identify features
print("\n3/3 Processing and merging data with fuzzy matching...")
merged_count = 0
fuzzy_matches = 0
cities_without_data = []
municipalities_with_data = []
match_log = []

for feature in all_boundaries['features']:
    shape_name = feature['properties'].get('shapeName', '')
    
    # Add municipality_name for consistency
    feature['properties']['municipality_name'] = shape_name
    
    # Try exact match first using normalization
    normalized_name = normalize_to_novads(shape_name)
    matched_name = None
    match_type = None
    confidence = 0.0
    
    if normalized_name in completeness:
        matched_name = normalized_name
        match_type = "exact"
        confidence = 1.0
    else:
        # Try fuzzy matching
        matched_name, confidence = fuzzy_match_name(shape_name, csv_municipality_names, threshold=0.50)
        if matched_name:
            match_type = "fuzzy"
            fuzzy_matches += 1
    
    # Log the match result
    if matched_name:
        match_log.append(f"  ✓ {shape_name:20} -> {matched_name:30} [{match_type} {confidence:.0%}]")
    else:
        match_log.append(f"  ✗ {shape_name:20} -> NO MATCH")
    
    # Try to match with completeness data
    if matched_name and matched_name in completeness:
        # Add completeness data with proper types
        comp_row = completeness[matched_name]
        feature['properties']['Municipality'] = comp_row['Municipality']
        
        # Handle missing values gracefully
        try:
            osm_km = float(comp_row['OSM_Roads_km']) if comp_row['OSM_Roads_km'] and str(comp_row['OSM_Roads_km']).lower() != 'nan' else None
            segments = int(float(comp_row['Segments'])) if comp_row['Segments'] and str(comp_row['Segments']).lower() != 'nan' else None
            official_km = float(comp_row['Official_Roads_km']) if comp_row['Official_Roads_km'] and str(comp_row['Official_Roads_km']).lower() != 'nan' else None
            completeness_pct = float(comp_row['Completeness_%']) if comp_row['Completeness_%'] and str(comp_row['Completeness_%']).lower() != 'nan' else None
            area_type = comp_row.get('Area_Type', 'Unknown') if comp_row.get('Area_Type') else 'Unknown'
            
            feature['properties']['OSM_Roads_km'] = osm_km
            feature['properties']['Segments'] = segments
            feature['properties']['Official_Roads_km'] = official_km
            feature['properties']['Completeness_%'] = completeness_pct
            feature['properties']['Area_Type'] = area_type
            feature['properties']['has_data'] = True
            merged_count += 1
            municipalities_with_data.append(shape_name)
        except (ValueError, TypeError):
            # If conversion fails, mark as incomplete data
            feature['properties']['has_data'] = False
            feature['properties']['Municipality'] = shape_name
            cities_without_data.append(shape_name)
    else:
        # No completeness data - mark as city or unmatched
        feature['properties']['has_data'] = False
        feature['properties']['Municipality'] = shape_name
        feature['properties']['Area_Type'] = 'Unknown'
        cities_without_data.append(shape_name)

# Print match results
print(f"\n  Match Results:")
print(f"  Total features: {len(all_boundaries['features'])}")
print(f"  Exact matches: {merged_count - fuzzy_matches}")
print(f"  Fuzzy matches: {fuzzy_matches}")
print(f"  Total matched: {merged_count}")
print(f"  Unmatched: {len(cities_without_data)}")

print(f"\n  Detailed Match Log:")
for log_entry in match_log:
    print(log_entry)

# Save comprehensive GeoJSON
output_file = 'outputs/exports/latvia_lau1.geojson'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_boundaries, f, ensure_ascii=False, indent=2)

print(f"\n[OK] Saved: {output_file}")
print(f"  Total features: {len(all_boundaries['features'])}")
print(f"  Features with data: {merged_count}")
print(f"  Features without data: {len(all_boundaries['features']) - merged_count}")

print("\n" + "=" * 70)
print("[OK] Comprehensive GeoJSON created successfully!")
print("=" * 70)
