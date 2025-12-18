#!/usr/bin/env python3
"""Extract roads from OSM PBF file"""

import osmium
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd

print("=" * 60)
print("Extracting Roads from OSM")
print("=" * 60)
print()

class RoadHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.roads = []
        self.count = 0
        
    def way(self, w):
        if 'highway' in w.tags:
            highway_type = w.tags['highway']
            
            # Skip certain types
            if highway_type in ['proposed', 'construction', 'abandoned']:
                return
            
            # Extract coordinates
            try:
                coords = [(n.lon, n.lat) for n in w.nodes]
                if len(coords) >= 2:
                    self.roads.append({
                        'osm_id': w.id,
                        'highway': highway_type,
                        'name': w.tags.get('name', None),
                        'geometry': LineString(coords)
                    })
                    self.count += 1
                    
                    if self.count % 10000 == 0:
                        print(f"  Processed {self.count:,} roads...")
            except:
                pass

print("1/4 Reading OSM file...")
print("   This takes 5-10 minutes...")
handler = RoadHandler()
handler.apply_file('data/raw/latvia-latest.osm.pbf', locations=True)
print(f"✓ Found {len(handler.roads):,} roads")

print("\n2/4 Creating GeoDataFrame...")
gdf = gpd.GeoDataFrame(handler.roads, crs='EPSG:4326')
print(f"✓ Created GeoDataFrame")

print("\n3/4 Reprojecting to metric CRS...")
gdf = gdf.to_crs('EPSG:3035')
print("✓ Reprojected to EPSG:3035")

print("\n4/4 Calculating lengths...")
gdf['length_km'] = gdf.geometry.length / 1000.0
print("✓ Lengths calculated")

# Save
print("\nSaving to file...")
gdf.to_file('data/processed/roads.geojson', driver='GeoJSON')
print(f"✓ Saved: data/processed/roads.geojson ({len(gdf):,} roads)")

# Statistics
print("\n" + "=" * 60)
print("Statistics:")
print(f"  Total roads: {len(gdf):,}")
print(f"  Total length: {gdf['length_km'].sum():.2f} km")
print(f"  Average length: {gdf['length_km'].mean():.3f} km")
print("\nTop 5 road types:")
print(gdf['highway'].value_counts().head())
print("=" * 60)
print()