#!/usr/bin/env python3
"""Create interactive combined map with roads and forests toggle"""

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
print("Creating Combined Road & Forest Completeness Map")
print("=" * 60)

# Load data
print("\n1/3 Loading data...")
roads_gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
forests_gdf = gpd.read_file('outputs/exports/latvia_lau1_forests.geojson')

roads_gdf = roads_gdf.to_crs('EPSG:4326')
forests_gdf = forests_gdf.to_crs('EPSG:4326')

print(f"  ✓ Loaded {len(roads_gdf)} road units")
print(f"  ✓ Loaded {len(forests_gdf)} forest units")

# Define color functions
def get_road_color(completeness):
    """Return color based on road completeness percentage"""
    if pd.isna(completeness):
        return '#cccccc'
    completeness = float(completeness)
    if completeness >= 90:
        return '#1a9850'  # Green
    elif completeness >= 70:
        return '#91cf60'  # Light green
    elif completeness >= 50:
        return '#fee08b'  # Yellow
    elif completeness >= 30:
        return '#fc8d59'  # Orange
    else:
        return '#d73027'  # Red

def get_forest_color(completeness):
    """Return color based on forest completeness percentage"""
    if pd.isna(completeness):
        return '#cccccc'
    elif completeness < 40:
        return '#d73027'  # Red
    elif completeness < 60:
        return '#fc8d59'  # Orange
    elif completeness < 80:
        return '#fee08b'  # Yellow
    else:
        return '#1a9850'  # Green

# Create map
print("\n2/3 Creating map...")
center = [56.8796, 24.6032]  # Latvia center
m = folium.Map(location=center, zoom_start=7, tiles='CartoDB positron')

# Create feature groups for layers (both visible initially, JS will control)
road_layer = folium.FeatureGroup(name='Roads')
forest_layer = folium.FeatureGroup(name='Forests')

# Add road polygons
print("  Adding road layer...")
for _, row in roads_gdf.iterrows():
    completeness = row.get('Completeness_%', None)
    osm_roads = row.get('OSM_Roads_km', None)
    official_roads = row.get('Official_Roads_km', None)
    
    comp_str = f"{completeness:.2f}%" if pd.notna(completeness) else "N/A"
    osm_str = f"{osm_roads:.2f} km" if pd.notna(osm_roads) else "N/A"
    off_str = f"{official_roads:.2f} km" if pd.notna(official_roads) else "N/A"
    
    fill_color = get_road_color(completeness)
    
    popup_html = f"""
    <div style="font-family: Arial; min-width: 280px;">
        <h4 style="margin-bottom: 10px; color: #1976D2;">🛣️ {row['municipality_name']}</h4>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td><b>Type:</b></td><td>{row.get('Area_Type', 'N/A')}</td></tr>
            <tr><td colspan="2"><hr style="margin: 5px 0;"></td></tr>
            <tr><td><b>OSM Roads:</b></td><td>{osm_str}</td></tr>
            <tr><td><b>Official Roads:</b></td><td>{off_str}</td></tr>
            <tr><td colspan="2"><hr style="margin: 5px 0;"></td></tr>
            <tr><td><b>Completeness:</b></td>
                <td style="color: {fill_color}; font-weight: bold;">{comp_str}</td></tr>
        </table>
    </div>
    """
    
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, fc=fill_color: {
            'fillColor': fc,
            'color': '#333333',
            'weight': 1,
            'fillOpacity': 0.6
        },
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(road_layer)

# Add forest polygons
print("  Adding forest layer...")
for _, row in forests_gdf.iterrows():
    completeness = row.get('Forest_Completeness_%', None)
    osm_forest = row.get('OSM_Forest_km2', None)
    official_forest = row.get('Official_Forest_km2', None)
    forest_count = row.get('Forest_Count', None)
    
    comp_str = f"{completeness:.2f}%" if pd.notna(completeness) else "N/A"
    
    if pd.notna(osm_forest):
        osm_ha = osm_forest * 100
        osm_str = f"{osm_forest:.2f} km² ({osm_ha:,.0f} ha)"
    else:
        osm_str = "N/A"
    
    if pd.notna(official_forest):
        off_ha = official_forest * 100
        off_str = f"{official_forest:.2f} km² ({off_ha:,.0f} ha)"
    else:
        off_str = "N/A"
    
    count_str = f"{forest_count:,}" if pd.notna(forest_count) else "N/A"
    fill_color = get_forest_color(completeness)
    
    popup_html = f"""
    <div style="font-family: Arial; min-width: 280px;">
        <h4 style="margin-bottom: 10px; color: #2e7d32;">🌲 {row['municipality_name']}</h4>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td><b>Type:</b></td><td>{row.get('Area_Type', 'N/A')}</td></tr>
            <tr><td colspan="2"><hr style="margin: 5px 0;"></td></tr>
            <tr><td><b>OSM Forest:</b></td><td>{osm_str}</td></tr>
            <tr><td><b>Official Forest:</b></td><td>{off_str}</td></tr>
            <tr><td><b>Forest Count:</b></td><td>{count_str}</td></tr>
            <tr><td colspan="2"><hr style="margin: 5px 0;"></td></tr>
            <tr><td><b>Completeness:</b></td>
                <td style="color: {fill_color}; font-weight: bold;">{comp_str}</td></tr>
        </table>
    </div>
    """
    
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, fc=fill_color: {
            'fillColor': fc,
            'color': '#333333',
            'weight': 1,
            'fillOpacity': 0.6
        },
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(forest_layer)

# Add layers to map
road_layer.add_to(m)
forest_layer.add_to(m)

# Add dropdown selector with dynamic legend
selector_html = '''
<div style="
    position: fixed;
    top: 80px;
    right: 10px;
    background: white;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    z-index: 9999;
    font-family: Arial;
">
    <label style="display: block; margin-bottom: 8px; font-weight: bold; font-size: 14px;">
        Select Map Type:
    </label>
    <select id="mapTypeSelector" onchange="switchMapType()" style="
        width: 100%;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 14px;
        cursor: pointer;
    ">
        <option value="roads">🛣️ Roads Completeness</option>
        <option value="forests" selected>🌲 Forest Completeness</option>
    </select>
</div>

<div id="dynamicLegend" style="
    position: fixed;
    bottom: 30px;
    right: 10px;
    background: white;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    z-index: 9999;
    font-family: Arial;
    max-width: 250px;
">
    <!-- Legend will be populated by JavaScript -->
</div>

<script>
function switchMapType() {
    var selector = document.getElementById('mapTypeSelector');
    if (!selector) return;
    
    var selectedType = selector.value;
    
    // Wait a bit for map to be fully loaded
    setTimeout(function() {
        // Get all path elements (Folium renders GeoJSON as SVG paths)
        var allPaths = document.querySelectorAll('.leaflet-overlay-pane path');
        
        if (allPaths.length === 0) return;
        
        // Split paths into two groups (first half = roads, second half = forests)
        var halfPoint = Math.floor(allPaths.length / 2);
        
        for (var i = 0; i < allPaths.length; i++) {
            if (selectedType === 'roads') {
                // Show first half (roads), hide second half (forests)
                allPaths[i].style.display = (i < halfPoint) ? 'block' : 'none';
            } else {
                // Show second half (forests), hide first half (roads)
                allPaths[i].style.display = (i >= halfPoint) ? 'block' : 'none';
            }
        }
        
        updateLegend(selectedType);
    }, 100);
}

function updateLegend(type) {
    var legendDiv = document.getElementById('dynamicLegend');
    if (!legendDiv) return;
    
    if (type === 'roads') {
        legendDiv.innerHTML = `
            <h4 style="margin: 0 0 10px 0; font-size: 14px; border-bottom: 2px solid #1976D2; padding-bottom: 5px;">
                🛣️ Road Completeness
            </h4>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #d73027; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">< 30% (Low)</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #fc8d59; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">30-50%</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #fee08b; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">50-70%</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #91cf60; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">70-90%</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #1a9850; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">≥ 90% (High)</span>
            </div>
        `;
    } else {
        legendDiv.innerHTML = `
            <h4 style="margin: 0 0 10px 0; font-size: 14px; border-bottom: 2px solid #2e7d32; padding-bottom: 5px;">
                🌲 Forest Completeness
            </h4>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #d73027; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">< 40% (Low)</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #fc8d59; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">40-60% (Partial)</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #fee08b; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">60-80% (Good)</span>
            </div>
            <div style="display: flex; align-items: center; margin: 5px 0;">
                <span style="background: #1a9850; width: 20px; height: 15px; display: inline-block; margin-right: 8px;"></span>
                <span style="font-size: 12px;">≥ 80% (Excellent)</span>
            </div>
        `;
    }
}

// Initialize with roads view on page load
window.addEventListener('load', function() {
    setTimeout(function() {
        switchMapType();
    }, 1000);
});
</script>
'''

m.get_root().html.add_child(folium.Element(selector_html))

# Add title
title_html = '''
<div style="
    position: fixed;
    top: 10px;
    left: 50px;
    background: white;
    padding: 15px 20px;
    border-radius: 5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    z-index: 9999;
    font-family: Arial;
">
    <h3 style="margin: 0; color: #1976D2;">Latvia OSM Completeness</h3>
    <p style="margin: 5px 0 0 0; font-size: 12px; color: #555;">
        Roads & Forests - LAU1 Administrative Units
    </p>
</div>
'''

m.get_root().html.add_child(folium.Element(title_html))

# Add fullscreen button
plugins.Fullscreen().add_to(m)

# Save map
output_path = 'outputs/maps/combined_map.html'
print(f"\n3/3 Saving map...")
m.save(output_path)
print(f"  ✓ Saved: {output_path}")

print("\n" + "=" * 60)
print("✓ Combined map created successfully!")
print("=" * 60)
