#!/usr/bin/env python3
"""Create interactive map with LAU-1 boundaries and official data"""

import json
import folium
import pandas as pd
from shapely.geometry import shape
import geopandas as gpd

print("=" * 70)
print("Creating Interactive Map with LAU-1 Municipalities & Official Data")
print("=" * 70)
print()

# Load LAU-1 GeoJSON directly with JSON (faster than geopandas)
print("1/3 Loading LAU-1 GeoJSON with municipality and city boundaries...")
with open('outputs/exports/latvia_lau1.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Convert to GeoDataFrame for easier handling
features = geojson_data['features']
print(f"  Loaded {len(features)} total features")

# Create list of feature data
data_list = []
for feature in features:
    row = feature['properties'].copy()
    row['geometry'] = shape(feature['geometry'])
    data_list.append(row)

gdf = gpd.GeoDataFrame(data_list, crs='EPSG:4326')
print(f"  Columns: {list(gdf.columns)}")
print()

# Create base map centered on Latvia
print("2/3 Creating base map...")
m = folium.Map(
    location=[56.8, 24.6],
    zoom_start=7,
    tiles='CartoDB positron'
)

# Add title
title_html = '''
<div style="position: fixed; top: 10px; left: 50px; width: 500px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 15px; border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
    <h3 style="margin: 0; color: #1976D2;">Latvia OSM Road Completeness</h3>
    <p style="margin: 5px 0 0 0; font-size: 12px; color: #555;">
        LAU-1 Municipalities: OSM vs Official Road Data
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Color function based on completeness
def get_color(completeness):
    if pd.isna(completeness):
        return '#cccccc'
    completeness = float(completeness)
    if completeness >= 90:
        return '#1a9850'  # Green: 90-110% or above
    elif completeness >= 70:
        return '#fee08b'  # Yellow: 70-90%
    elif completeness < 50:
        return '#d73027'  # Red: Below 50%
    else:
        return '#fc8d59'  # Orange: 50-70% (in-between)

print("3/3 Adding municipality and city boundaries with popups...")

# First pass: Add municipalities with data directly to map
municipalities = gdf[gdf['has_data'] == True]
for idx, row in municipalities.iterrows():
    mun_name = row['municipality_name']
    osm_km = float(row.get('OSM_Roads_km', 0))
    official_km = float(row.get('Official_Roads_km', None)) if row.get('Official_Roads_km') is not None else None
    completeness = float(row.get('Completeness_%', None)) if row.get('Completeness_%') is not None else None
    
    # Create popup with all available data
    popup_html = f"""
    <div style="width: 350px; font-family: Arial; font-size: 12px;">
        <h4 style="margin: 0 0 10px 0; color: #1976D2; border-bottom: 2px solid #2196F3; padding-bottom: 8px;">
            {mun_name}
        </h4>
        
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #f5f5f5;">
                <td style="padding: 6px; font-weight: bold; width: 50%;">OSM Road Length:</td>
                <td style="padding: 6px; text-align: right;">{osm_km:.2f} km</td>
            </tr>
            <tr>
                <td style="padding: 6px; font-weight: bold;">Official Road Length:</td>
                <td style="padding: 6px; text-align: right;">
                    {f'{official_km:.2f}' if official_km is not None else 'N/A'} km
                </td>
            </tr>
            <tr style="background-color: #f5f5f5;">
                <td style="padding: 6px; font-weight: bold;">Completeness:</td>
                <td style="padding: 6px; text-align: right; color: #2e7d32; font-weight: bold;">
                    {f'{completeness:.1f}%' if completeness is not None else 'N/A'}
                </td>
            </tr>
        </table>
        
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 11px; color: #666;">
            <p style="margin: 0;">
                <strong>Interpretation:</strong><br>
                • <50%: Low coverage<br>
                • 50-80%: Partial coverage<br>
                • 80-100%: Complete coverage<br>
                • >100%: Over-mapped (OSM > official)
            </p>
        </div>
    </div>
    """
    
    # Determine color based on completeness
    color = get_color(completeness)
    
    # Add municipality feature to map
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, color=color: {
            'fillColor': color,
            'color': '#333',
            'weight': 1.5,
            'opacity': 0.8,
            'fillOpacity': 0.7
        },
        popup=folium.Popup(popup_html, max_width=400),
        tooltip=f"{mun_name}: {completeness:.1f}%" if completeness is not None else mun_name
    ).add_to(m)

# Second pass: Add cities WITHOUT data directly to map
cities = gdf[gdf['has_data'] == False]
print(f"DEBUG: Found {len(cities)} cities to add")

for idx, row in cities.iterrows():
    mun_name = row['municipality_name']
    geom = row['geometry']
    print(f"  DEBUG: Adding city {mun_name}, geom type: {geom.geom_type}")
    
    # Create a single-feature GeoJSON for each city
    city_geojson = {
        "type": "Feature",
        "geometry": geom.__geo_interface__,
        "properties": {
            "name": mun_name,
            "city": True
        }
    }
    
    # Add city with explicit popup
    popup_text = f"<b>{mun_name}</b><br>City (no official data)"
    
    folium.GeoJson(
        city_geojson,
        style_function=lambda x: {
            'fillColor': '#ff6666',
            'color': '#cc0000',
            'weight': 3,
            'opacity': 1,
            'fillOpacity': 0.6
        },
        popup=folium.Popup(popup_text, max_width=200),
        tooltip=mun_name
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; bottom: 50px; right: 10px; width: 280px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 15px; border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
    <h4 style="margin: 0 0 12px 0; color: #1976D2;">Municipalities - Road Completeness</h4>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #d73027; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Low (&lt;50%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #fc8d59; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Partial (50-80%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #fee08b; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Good (70-90%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #1a9850; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Excellent (≥90%)
    </p>
    <hr style="margin: 10px 0; border: none; border-top: 1px solid #ccc;">
    <p style="margin: 0 0 0px 0; font-size: 12px; color: #666;">
        <i style="background-color: #ffcccc; width: 20px; height: 15px; display: inline-block; border: 2px dashed #cc0000;"></i>
        &nbsp; <strong>Cities</strong> (no data available)
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save map
output_path = 'outputs/maps/interactive_map.html'
m.save(output_path)
print(f"[OK] Saved: {output_path}")
print()

# Summary statistics
print("=" * 70)
print("Summary Statistics:")
print("=" * 70)
print(f"Total features: {len(gdf)}")
print(f"Features with data: {(gdf['has_data'] == True).sum()}")
print(f"Cities without data: {(gdf['has_data'] == False).sum()}")

# Only calculate statistics for features with data
gdf_with_data = gdf[gdf['has_data'] == True]
if len(gdf_with_data) > 0:
    print(f"\nMunicipality Statistics (with data):")
    print(f"Average completeness: {gdf_with_data['Completeness_%'].mean():.1f}%")
    print(f"Min completeness: {gdf_with_data['Completeness_%'].min():.1f}%")
    print(f"Max completeness: {gdf_with_data['Completeness_%'].max():.1f}%")
    print()

    # Show municipalities by completeness category
    print("Completeness Categories:")
    print("-" * 70)
    low = (gdf_with_data['Completeness_%'] < 50).sum()
    partial = ((gdf_with_data['Completeness_%'] >= 50) & (gdf_with_data['Completeness_%'] < 80)).sum()
    complete = ((gdf_with_data['Completeness_%'] >= 80) & (gdf_with_data['Completeness_%'] <= 100)).sum()
    overmapped = (gdf_with_data['Completeness_%'] > 100).sum()

    print(f"  Low (<50%):            {low} municipalities")
    print(f"  Partial (50-80%):      {partial} municipalities")
    print(f"  Complete (80-100%):    {complete} municipalities")
    print(f"  Over-mapped (>100%):   {overmapped} municipalities")
print()

# Top 5 best and worst
print("Top 5 Best Mapped (Highest Completeness):")
print("-" * 70)
top5 = gdf_with_data.nlargest(5, 'Completeness_%')[['municipality_name', 'Completeness_%']]
for idx, (_, row) in enumerate(top5.iterrows(), 1):
    print(f"  {idx}. {row['municipality_name']}: {row['Completeness_%']:.1f}%")
print()

print("Top 5 Least Mapped (Lowest Completeness):")
print("-" * 70)
bottom5 = gdf_with_data.nsmallest(5, 'Completeness_%')[['municipality_name', 'Completeness_%']]
for idx, (_, row) in enumerate(bottom5.iterrows(), 1):
    print(f"  {idx}. {row['municipality_name']}: {row['Completeness_%']:.1f}%")
print()

print("[OK] Map generation completed successfully!")
print("=" * 70)
