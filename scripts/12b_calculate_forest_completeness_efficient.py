#!/usr/bin/env python3
"""Calculate forest completeness for LAU1 municipalities - optimized version"""

import geopandas as gpd
import pandas as pd
import json
from shapely.geometry import shape
from shapely.ops import unary_union

print("=" * 60)
print("Calculating Forest Completeness (Efficient)")
print("=" * 60)
print()

print("1/5 Loading municipalities...")
municipalities = gpd.read_file('data/raw/municipalities.geojson')
municipalities = municipalities.rename(columns={'shapeName': 'municipality_name'})
municipalities = municipalities.to_crs('EPSG:3035')  # Convert to meters for area calculation
print(f"✓ Loaded {len(municipalities)} LAU1 units")

print("\n2/5 Loading official forest statistics...")
official = pd.read_csv('data/raw/official_forest_stats.csv')
print(f"✓ Loaded {len(official)} entries")

print("\n3/5 Processing forest data from GeoJSON...")
print("  Reading forests (this will take 1-2 minutes)...")

osm_aggregated = []
batch_size = 5000
feature_count = 0

with open('data/processed/forests.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)
    total_features = len(data['features'])
    print(f"  Total forest features to process: {total_features:,}")
    
    # Process in batches
    for i in range(0, total_features, batch_size):
        batch = data['features'][i:i+batch_size]
        feature_count += len(batch)
        
        # Create GeoDataFrame from batch
        geometries = [shape(f['geometry']) for f in batch]
        properties = [f['properties'] for f in batch]
        gdf_batch = gpd.GeoDataFrame(properties, geometry=geometries, crs='EPSG:4326')
        gdf_batch = gdf_batch.to_crs('EPSG:3035')
        
        # Spatial join with municipalities
        joined = gpd.sjoin(gdf_batch, municipalities[['geometry', 'municipality_name']], 
                          how='left', predicate='intersects')
        
        # Aggregate by municipality for this batch
        batch_agg = joined.groupby('municipality_name').agg({
            'area_km2': 'sum',
            'area_ha': 'sum',
            'osm_id': 'count'
        }).reset_index()
        
        osm_aggregated.append(batch_agg)
        
        if (i + batch_size) % 10000 == 0 or (i + batch_size) >= total_features:
            print(f"  Processed {min(i + batch_size, total_features):,} / {total_features:,} features...")

# Combine all batches
osm_data = pd.concat(osm_aggregated, ignore_index=True)
osm_final = osm_data.groupby('municipality_name').agg({
    'area_km2': 'sum',
    'area_ha': 'sum',
    'osm_id': 'sum'
}).reset_index()
osm_final.columns = ['municipality_name', 'osm_forest_km2', 'osm_forest_ha', 'num_forest_areas']
print(f"✓ Aggregated for {len(osm_final)} municipalities")

print("\n4/5 Merging with official statistics...")
completeness = pd.merge(
    osm_final,
    official,
    on='municipality_name',
    how='outer'
)

# Calculate completeness
completeness['completeness_pct'] = (
    completeness['osm_forest_km2'] / completeness['forest_area_km2'] * 100
).round(2)

completeness['difference_ha'] = (completeness['osm_forest_ha'] - completeness['forest_area_ha']).round(2)
completeness['difference_km2'] = (completeness['osm_forest_km2'] - completeness['forest_area_km2']).round(2)

# Categorize
def categorize(pct):
    if pd.isna(pct):
        return 'No data'
    elif pct >= 90:
        return 'Complete'
    elif pct >= 70:
        return 'Good'
    elif pct >= 50:
        return 'Partial'
    elif pct >= 30:
        return 'Low'
    else:
        return 'Very Low'

completeness['category'] = completeness['completeness_pct'].apply(categorize)

# Handle over-mapped cases
completeness.loc[completeness['completeness_pct'] > 100, 'category'] = 'Over-mapped'

print("✓ Completeness calculated")

print("\n5/5 Saving results...")
completeness.to_csv('outputs/exports/completeness_forests.csv', index=False)
print("✓ Saved: outputs/exports/completeness_forests.csv")

print("\n" + "=" * 60)
print("Summary:")
print(completeness['category'].value_counts())
print()
print(f"Total municipalities/cities: {len(completeness)}")
print(f"With OSM data: {completeness['osm_forest_km2'].notna().sum()}")
print(f"With official data: {completeness['forest_area_km2'].notna().sum()}")
print()
print("Top 10 by completeness:")
print(completeness.nlargest(10, 'completeness_pct')[['municipality_name', 'completeness_pct', 'category']])
print("=" * 60)
