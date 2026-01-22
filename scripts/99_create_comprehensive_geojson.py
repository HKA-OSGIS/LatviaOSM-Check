#!/usr/bin/env python3
"""
Create comprehensive Latvia GeoJSON with municipalities AND cities
Merges municipality completeness data with all 43 administrative boundaries
"""

import json
import csv

print("=" * 70)
print("Creating Comprehensive Latvia GeoJSON (Municipalities + Cities)")
print("=" * 70)
print()

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

# Step 3: Merge data and identify features
print("\n3/3 Processing and merging data...")
merged_count = 0
cities_without_data = []
municipalities_with_data = []

for feature in all_boundaries['features']:
    shape_name = feature['properties'].get('shapeName', '')
    
    # Add municipality_name for consistency
    feature['properties']['municipality_name'] = shape_name
    
    # Try to match with completeness data
    if shape_name in completeness:
        # Add completeness data with proper types
        comp_row = completeness[shape_name]
        feature['properties']['Municipality'] = comp_row['Municipality']
        
        # Handle missing values gracefully
        try:
            osm_km = float(comp_row['OSM_Roads_km']) if comp_row['OSM_Roads_km'] and str(comp_row['OSM_Roads_km']).lower() != 'nan' else None
            segments = int(float(comp_row['Segments'])) if comp_row['Segments'] and str(comp_row['Segments']).lower() != 'nan' else None
            official_km = float(comp_row['Official_Roads_km']) if comp_row['Official_Roads_km'] and str(comp_row['Official_Roads_km']).lower() != 'nan' else None
            completeness_pct = float(comp_row['Completeness_%']) if comp_row['Completeness_%'] and str(comp_row['Completeness_%']).lower() != 'nan' else None
            
            feature['properties']['OSM_Roads_km'] = osm_km
            feature['properties']['Segments'] = segments
            feature['properties']['Official_Roads_km'] = official_km
            feature['properties']['Completeness_%'] = completeness_pct
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
        cities_without_data.append(shape_name)

print(f"  Merged: {merged_count} features with completeness data")
print(f"  Cities/areas without data: {len(cities_without_data)}")
if cities_without_data:
    print(f"    {', '.join(cities_without_data[:10])}")

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
