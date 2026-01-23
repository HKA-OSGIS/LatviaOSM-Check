#!/usr/bin/env python3
"""Create simple forest map using Folium - minimal version"""
import folium
import json

print("Creating forest map...")

# Load forest GeoJSON
with open('outputs/exports/latvia_lau1_forests.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Create map
m = folium.Map(location=[56.8, 24.6], zoom_start=7, tiles='CartoDB positron')

# Color function
def get_color(pct):
    if not pct or pct == 'nan' or str(pct) == 'nan':
        return '#cccccc'
    pct = float(pct)
    if pct >= 90:
        return '#1a9850'
    elif pct >= 70:
        return '#91cf60'
    elif pct >= 50:
        return '#fee08b'
    elif pct >= 30:
        return '#fc8d59'
    else:
        return '#d73027'

# Add features
for feature in geojson_data['features']:
    props = feature['properties']
    name = props.get('Municipality', 'Unknown')
    osm = props.get('osm_forest_km2', 0)
    official = props.get('official_forest_km2', 0)
    completeness = props.get('forest_completeness_pct')
    
    popup_html = f"""
    <div style="width:250px">
        <h4>🌲 {name}</h4>
        <b>OSM Forest:</b> {osm:.1f} km²<br>
        <b>Official:</b> {official:.1f} km²<br>
        <b>Completeness:</b> {f'{completeness:.1f}%' if completeness and str(completeness) != 'nan' else 'N/A'}<br>
    </div>
    """
    
    folium.GeoJson(
        feature,
        style_function=lambda x, c=completeness: {
            'fillColor': get_color(c),
            'color': '#333',
            'weight': 1,
            'fillOpacity': 0.7
        },
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(m)

# Save
m.save('outputs/maps/forest_completeness_map.html')
print("✓ Saved: outputs/maps/forest_completeness_map.html")
print(f"  Features: {len(geojson_data['features'])}")
