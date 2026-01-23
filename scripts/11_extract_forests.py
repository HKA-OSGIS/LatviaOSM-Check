#!/usr/bin/env python3
"""Extract forest areas from OSM PBF file"""

import osmium
import osmium.geom
import geopandas as gpd
from shapely import wkb
from shapely.geometry import Polygon
import pandas as pd

print("=" * 60)
print("Extracting Forests from OSM")
print("=" * 60)
print()

class ForestHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.forests = []
        self.count = 0
        # Create WKB factory for creating geometries
        self.wkb_factory = osmium.geom.WKBFactory()
        
    def way(self, w):
        """Process ways (closed ways can be forests)"""
        # Only process closed ways (polygons)
        if not w.is_closed():
            return
            
        tags = {tag.k: tag.v for tag in w.tags}
        
        # Check if it's a forest/wood
        if 'landuse' in tags and tags['landuse'] == 'forest':
            forest_type = 'forest'
        elif 'natural' in tags and tags['natural'] == 'wood':
            forest_type = 'wood'
        else:
            return
        
        # Try to extract geometry
        try:
            # Create WKB geometry from way
            wkb_geom = self.wkb_factory.create_linestring(w)
            geom = wkb.loads(wkb_geom, hex=True)
            
            # For closed ways, create polygon from linestring coordinates
            poly = Polygon(geom.coords)
            
            self.forests.append({
                'osm_id': w.id,
                'osm_type': 'way',
                'forest_type': forest_type,
                'name': tags.get('name', None),
                'geometry': poly
            })
            self.count += 1
            
            if self.count % 5000 == 0:
                print(f"  Processed {self.count:,} forests...")
        except Exception as e:
            # Skip problematic geometries
            pass

print("1/4 Reading OSM file...")
print("   This may take 10-15 minutes...")
handler = ForestHandler()
handler.apply_file('data/raw/latvia-latest.osm.pbf', locations=True)
print(f"✓ Found {len(handler.forests):,} forest areas")

print("\n2/4 Creating GeoDataFrame...")
if len(handler.forests) > 0:
    gdf = gpd.GeoDataFrame(handler.forests, crs='EPSG:4326')
    print(f"✓ Created GeoDataFrame")
else:
    print("✗ No forests found!")
    print("\nNote: Ensure the OSM file contains landuse=forest or natural=wood tags")
    exit(1)

print("\n3/4 Reprojecting to metric CRS...")
gdf = gdf.to_crs('EPSG:3035')
print("✓ Reprojected to EPSG:3035")

print("\n4/4 Calculating areas...")
gdf['area_km2'] = (gdf.geometry.area / 1_000_000).round(4)
gdf['area_ha'] = (gdf['area_km2'] * 100).round(2)
print("✓ Areas calculated")

# Save
print("\nSaving to file...")
gdf.to_file('data/processed/forests.geojson', driver='GeoJSON')
print(f"✓ Saved: data/processed/forests.geojson ({len(gdf):,} forests)")

# Statistics
print("\n" + "=" * 60)
print("Statistics:")
print(f"  Total forests: {len(gdf):,}")
print(f"  Total area: {gdf['area_km2'].sum():,.2f} km² ({gdf['area_ha'].sum():,.0f} ha)")
print(f"  Average area: {gdf['area_km2'].mean():.4f} km² ({gdf['area_ha'].mean():.2f} ha)")
print(f"\nForest type distribution:")
print(gdf['forest_type'].value_counts().to_string())
print("\nLargest 5 forests:")
print(gdf.nlargest(5, 'area_km2')[['name', 'forest_type', 'area_km2']].to_string(index=False))
print("=" * 60)
print()
