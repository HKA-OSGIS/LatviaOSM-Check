#!/usr/bin/env python3
"""Create a filtered interactive map showing only 36 municipalities."""

import folium
import geopandas as gpd
import json

# Load the filtered municipalities GeoJSON
with open('outputs/exports/latvia_municipalities_36_only.geojson', 'r', encoding='utf-8') as f:
    municipalities = json.load(f)

# Get bounds for map centering
bounds = []
for feature in municipalities['features']:
    coords = feature['geometry']['coordinates'][0]
    for lon, lat in coords:
        bounds.append([lat, lon])

if bounds:
    center_lat = sum(b[0] for b in bounds) / len(bounds)
    center_lon = sum(b[1] for b in bounds) / len(bounds)
else:
    center_lat = 56.5
    center_lon = 24.5

# Create the base map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=7,
    tiles='OpenStreetMap'
)

# Add the filtered municipalities as a GeoJSON layer
folium.GeoJson(
    municipalities,
    name='36 Official Municipalities',
    style_function=lambda x: {
        'fillColor': '#1f77b4',
        'color': '#1f77b4',
        'weight': 2,
        'fillOpacity': 0.3
    },
    popup=folium.GeoJsonPopup(fields=['shapeName']),
).add_to(m)

# Add a title
title_html = '''
             <div style="position: fixed; 
                     top: 10px; left: 50px; width: 300px; height: 60px; 
                     background-color: white; border:2px solid grey; z-index:9999; 
                     font-size:16px; padding:10px; border-radius: 5px;">
             <b>LatviaOSM-Check</b><br>
             36 Official Municipalities Only
             </div>
             '''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map
output_file = 'outputs/maps/interactive_map_36_municipalities.html'
m.save(output_file)
print(f"✓ Created filtered map: {output_file}")
print(f"  Features: {len(municipalities['features'])} municipalities")
