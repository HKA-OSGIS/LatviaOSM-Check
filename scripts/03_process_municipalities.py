import geopandas as gpd

gdf = gpd.read_file("data/raw/municipalities.geojson")
gdf = gdf.to_crs("EPSG:3035")

gdf = gdf.rename(columns={
    "shapeName": "municipality_name",
    "shapeID": "municipality_id"
})

gdf["area_km2"] = gdf.area / 1_000_000
gdf.to_file("data/processed/municipalities.geojson", driver="GeoJSON")

print("Municipalities processed")
#!/usr/bin/env python3
"""Process municipality boundaries"""

import geopandas as gpd

print("=" * 60)
print("Processing Municipalities")
print("=" * 60)
print()

print("1/3 Loading municipalities...")
gdf = gpd.read_file('data/raw/municipalities.geojson')
print(f"✓ Loaded {len(gdf)} municipalities")

print("\n2/3 Reprojecting and cleaning...")
gdf = gdf.to_crs('EPSG:3035')
gdf = gdf.rename(columns={
    'shapeName': 'municipality_name',
    'shapeID': 'municipality_id'
})
gdf['area_km2'] = gdf.geometry.area / 1_000_000
print("✓ Cleaned and calculated areas")

print("\n3/3 Saving...")
gdf.to_file('data/processed/municipalities.geojson', driver='GeoJSON')
print(f"✓ Saved: data/processed/municipalities.geojson")

print("\n" + "=" * 60)
print(f"✓ Processed {len(gdf)} municipalities")
print("=" * 60)
print()