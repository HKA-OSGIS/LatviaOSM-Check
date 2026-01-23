#!/usr/bin/env python3
"""Create interactive forest completeness map"""

import geopandas as gpd
import pandas as pd
import folium
from folium import plugins
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Creating Forest Completeness Map")
print("=" * 60)

# Load data
print("\n1/2 Loading data...")
gdf = gpd.read_file('outputs/exports/latvia_lau1_forests.geojson')
gdf = gdf.to_crs('EPSG:4326')
print(f"  ✓ Loaded {len(gdf)} administrative units")

# Define color function based on completeness
def get_forest_color(completeness):
    """Return color based on completeness percentage"""
    if pd.isna(completeness):
        return '#cccccc'  # Gray for no data
    elif completeness < 40:
        return '#d73027'  # Red - Low
    elif completeness < 60:
        return '#fc8d59'  # Orange - Partial
    elif completeness < 80:
        return '#fee08b'  # Yellow - Good
    else:
        return '#1a9850'  # Green - Excellent
    
# Create map
print("\n2/2 Creating map...")
center = [56.8796, 24.6032]  # Latvia center
m = folium.Map(location=center, zoom_start=7, tiles='CartoDB positron')

# Create feature layer with popups
for _, row in gdf.iterrows():
    completeness = row['Forest_Completeness_%']
    osm_forest = row['OSM_Forest_km2']
    official_forest = row['Official_Forest_km2']
    forest_count = row['Forest_Count']
    
    # Format values
    comp_str = f"{completeness:.2f}%" if pd.notna(completeness) else "N/A"
    
    # Format with both km² and hectares
    if pd.notna(osm_forest):
        osm_ha = osm_forest * 100  # 1 km² = 100 ha
        osm_str = f"{osm_forest:.2f} km² ({osm_ha:,.0f} ha)"
    else:
        osm_str = "N/A"
    
    if pd.notna(official_forest):
        off_ha = official_forest * 100
        off_str = f"{official_forest:.2f} km² ({off_ha:,.0f} ha)"
    else:
        off_str = "N/A"
    
    count_str = f"{forest_count:,}" if pd.notna(forest_count) else "N/A"
    
    # Get color for this municipality
    fill_color = get_forest_color(completeness)
    
    # Create popup HTML
    popup_html = f"""
    <div style="font-family: Arial; min-width: 280px;">
        <h4 style="margin-bottom: 10px;">{row['municipality_name']}</h4>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td><b>Type:</b></td><td>{row['Area_Type']}</td></tr>
            <tr><td colspan="2"><hr style="margin: 5px 0;"></td></tr>
            <tr><td><b>OSM Forest:</b></td><td>{osm_str}</td></tr>
            <tr><td><b>Official Forest:</b></td><td>{off_str}</td></tr>
            <tr><td><b>Completeness:</b></td><td><b style="color: {fill_color};">{comp_str}</b></td></tr>
            <tr><td><b>Forest Features:</b></td><td>{count_str}</td></tr>
        </table>
    </div>
    """
    
    # Tooltip text
    tooltip_text = f"{row['municipality_name']}: {comp_str}"
    
    folium.GeoJson(
        row['geometry'].__geo_interface__,
        style_function=lambda x, color=fill_color: {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=tooltip_text,
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 240px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 10px; border-radius: 5px; font-size: 12px;">
    <p style="margin: 0; font-weight: bold; font-size: 14px; margin-bottom: 8px;">Municipalities - Forest Completeness</p>
    <p style="margin: 5px 0;">
        <span style="background: #d73027; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Low (&lt;40%)
    </p>
    <p style="margin: 5px 0;">
        <span style="background: #fc8d59; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Partial (40-60%)
    </p>
    <p style="margin: 5px 0;">
        <span style="background: #fee08b; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Good (60-80%)
    </p>
    <p style="margin: 5px 0;">
        <span style="background: #1a9850; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Excellent (≥80%)
    </p>
    <hr style="margin: 8px 0;">
    <p style="margin: 5px 0; font-size: 11px; font-style: italic;">
        <b>Interpretation:</b><br>
        • &lt;40%: Low coverage<br>
        • 40-60%: Partial coverage<br>
        • 60-80%: Good coverage<br>
        • ≥80%: Excellent coverage
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Add fullscreen button
plugins.Fullscreen().add_to(m)

# Save map
output_file = 'outputs/maps/forest_completeness_map.html'
m.save(output_file)
print(f"  ✓ Saved: {output_file}")

print("\n" + "=" * 60)
print("Map Statistics:")
print(f"  Total OSM forest land: {gdf['OSM_Forest_km2'].sum():.2f} km²")
print(f"  Total official forest land: {gdf['Official_Forest_km2'].sum():.2f} km²")
print(f"  Overall completeness: {(gdf['OSM_Forest_km2'].sum() / gdf['Official_Forest_km2'].sum() * 100):.2f}%")
print(f"  Average completeness: {gdf['Forest_Completeness_%'].mean():.2f}%")
print(f"  Median completeness: {gdf['Forest_Completeness_%'].median():.2f}%")
print("=" * 60)
