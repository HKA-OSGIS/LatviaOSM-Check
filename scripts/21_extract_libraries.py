#!/usr/bin/env python3
"""Extract libraries from OSM PBF file"""

import osmium
import osmium.geom
import geopandas as gpd
from shapely import wkb
from shapely.geometry import Point
import pandas as pd
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Extracting Libraries from OSM")
print("=" * 60)
print()

class LibraryHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.libraries = []
        self.count = 0
        # Create WKB factory for creating geometries
        self.wkb_factory = osmium.geom.WKBFactory()
        
    def node(self, n):
        """Process nodes (most libraries are nodes)"""
        tags = {tag.k: tag.v for tag in n.tags}
        
        # Check for library amenity
        if 'amenity' not in tags or tags['amenity'] != 'library':
            return
        
        # Try to extract geometry
        try:
            # Create point geometry
            wkb_geom = self.wkb_factory.create_point(n)
            geom = wkb.loads(wkb_geom, hex=True)
            
            self.libraries.append({
                'osm_id': n.id,
                'osm_type': 'node',
                'name': tags.get('name', None),
                'operator': tags.get('operator', None),
                'access': tags.get('access', None),
                'geometry': geom
            })
            self.count += 1
            
            if self.count % 100 == 0:
                print(f"  Processed {self.count} libraries...")
        except Exception as e:
            # Skip problematic geometries
            pass
    
    def way(self, w):
        """Process ways (some libraries are buildings)"""
        tags = {tag.k: tag.v for tag in w.tags}
        
        # Check for library amenity
        if 'amenity' not in tags or tags['amenity'] != 'library':
            return
        
        # Try to extract geometry (use centroid for ways)
        try:
            # Create linestring geometry
            wkb_geom = self.wkb_factory.create_linestring(w)
            geom = wkb.loads(wkb_geom, hex=True)
            
            # Use centroid for point location
            centroid = geom.centroid
            
            self.libraries.append({
                'osm_id': w.id,
                'osm_type': 'way',
                'name': tags.get('name', None),
                'operator': tags.get('operator', None),
                'access': tags.get('access', None),
                'geometry': centroid
            })
            self.count += 1
            
            if self.count % 100 == 0:
                print(f"  Processed {self.count} libraries...")
        except Exception as e:
            # Skip problematic geometries
            pass

print("1/3 Reading OSM file...")
print("   Searching for amenity=library...")
handler = LibraryHandler()
handler.apply_file('data/raw/latvia-latest.osm.pbf', locations=True)
print(f"✓ Found {len(handler.libraries):,} libraries")

print("\n2/3 Creating GeoDataFrame...")
if len(handler.libraries) > 0:
    gdf = gpd.GeoDataFrame(handler.libraries, crs='EPSG:4326')
    
    print(f"  ✓ Created GeoDataFrame with {len(gdf):,} features")
    
    print("\n3/3 Saving to GeoJSON...")
    gdf.to_file('data/processed/libraries.geojson', driver='GeoJSON')
    print(f"  ✓ Saved: data/processed/libraries.geojson")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Total libraries: {len(gdf):,}")
    print(f"  Named libraries: {gdf['name'].notna().sum():,}")
    print(f"  Unnamed libraries: {gdf['name'].isna().sum():,}")
    print("=" * 60)
else:
    print("⚠ No libraries found in OSM data")
    sys.exit(1)
