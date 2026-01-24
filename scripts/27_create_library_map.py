#!/usr/bin/env python3
"""Create interactive map for library completeness"""

import geopandas as gpd
import pandas as pd
import folium
from folium import plugins
import json
import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Creating Library Completeness Map")
print("=" * 60)

# Load data
print("\n1/4 Loading data...")
completeness = pd.read_csv('outputs/exports/completeness_libraries.csv')
lau1 = gpd.read_file('outputs/exports/latvia_lau1.geojson')

print(f"  ✓ Completeness data: {len(completeness)} records")
print(f"  ✓ LAU1 boundaries: {len(lau1)} features")

# Normalize LAU1 names to match official format
def normalize_lau1_name(row):
    """Convert LAU1 names to official format for matching"""
    name = row['municipality_name']
    area_type = row['Area_Type']
    
    # For cities: remove possessive suffix
    if area_type == 'City':
        if name == 'Jelgavas': return 'Jelgava'
        elif name == 'Jūrmalas': return 'Jūrmala'
        elif name == 'Liepājas': return 'Liepāja'
        elif name == 'Rēzeknes': return 'Rēzekne'
        return name
    
    # For municipalities: add " novads" suffix
    else:
        if name.endswith(' novads'):
            return name
        
        # Mapping from LAU1 to official format
        municipality_map = {
            'Ādaži': 'Ādažu novads',
            'Aizkraukle': 'Aizkraukles novads',
            'Alūksne': 'Alūksnes novads',
            'Augšdaugava': 'Augšdaugavas novads',
            'Balvi': 'Balvu novads',
            'Bauska': 'Bauskas novads',
            'Cēsis': 'Cēsu novads',
            'Dienvidkurzeme': 'Dienvidkurzemes novads',
            'Dobele': 'Dobeles novads',
            'Gulbene': 'Gulbenes novads',
            'Jelgava': 'Jelgavas novads',
            'Jēkabpils': 'Jēkabpils novads',
            'Ķekava': 'Ķekavas novads',
            'Krāslava': 'Krāslavas novads',
            'Kuldīga': 'Kuldīgas novads',
            'Limbaži': 'Limbažu novads',
            'Līvāni': 'Līvānu novads',
            'Ludza': 'Ludzas novads',
            'Madona': 'Madonas novads',
            'Mārupe': 'Mārupes novads',
            'Ogre': 'Ogres novads',
            'Olaine': 'Olaines novads',
            'Preiļi': 'Preiļu novads',
            'Rēzekne': 'Rēzeknes novads',
            'Ropaži': 'Ropažu novads',
            'Saldus': 'Saldus novads',
            'Saulkrasti': 'Saulkrastu novads',
            'Sigulda': 'Siguldas novads',
            'Smiltene': 'Smiltenes novads',
            'Talsi': 'Talsu novads',
            'Tukums': 'Tukuma novads',
            'Valka': 'Valkas novads',
            'Valmiera': 'Valmieras novads',
            'Varakļāni': 'Varakļānu novads',
            'Ventspils': 'Ventspils novads'
        }
        
        return municipality_map.get(name, name)

lau1['official_name'] = lau1.apply(normalize_lau1_name, axis=1)

# Merge completeness with geometries
print("\n2/4 Merging data...")
lau1_with_data = lau1.merge(completeness, left_on='official_name', right_on='municipality_name', how='left', suffixes=('_lau1', '_official'))

# Use official_name for display
lau1_with_data['display_name'] = lau1_with_data['municipality_name_official'].fillna(lau1_with_data['municipality_name_lau1'])

# Define color function
def get_color(completeness):
    """Return color based on completeness percentage"""
    if pd.isna(completeness) or completeness == 0:
        return '#CCCCCC'  # Gray for no data
    elif completeness >= 100:
        return '#2ECC71'  # Green
    elif completeness >= 75:
        return '#F39C12'  # Orange
    elif completeness >= 50:
        return '#E67E22'  # Dark orange
    elif completeness >= 25:
        return '#E74C3C'  # Red
    else:
        return '#C0392B'  # Dark red

# Create map centered on Latvia
print("\n3/4 Creating map...")
m = folium.Map(
    location=[56.8796, 24.6032],
    zoom_start=7,
    tiles='OpenStreetMap'
)

# Add title
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50px; width: 400px; height: 90px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 10px">
<h4 style="margin:0">📚 Library OSM Completeness</h4>
<p style="margin:5px 0"><b>Latvia LAU1 Units</b></p>
<p style="margin:0; font-size:12px">Comparing OSM libraries vs. official statistics (2024)</p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Add choropleth layer
for idx, row in lau1_with_data.iterrows():
    completeness_val = row.get('completeness_%', 0)
    osm_count = row.get('osm_library_count', 0)
    official_count = row.get('official_library_count', 0)
    area_type_lau1 = row.get('Area_Type_lau1', 'Unknown')
    area_type_off = row.get('Area_Type_official', area_type_lau1)
    area_type = area_type_off if pd.notna(area_type_off) else area_type_lau1
    display_name = row.get('display_name', row.get('municipality_name_lau1', 'Unknown'))
    
    # Create popup
    popup_html = f"""
    <div style="font-family: Arial; width: 250px;">
        <h4 style="margin: 0 0 10px 0; color: #2C3E50;">{display_name}</h4>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 4px;"><b>Type:</b></td>
                <td style="padding: 4px;">{area_type}</td>
            </tr>
            <tr style="background-color: #ECF0F1;">
                <td style="padding: 4px;"><b>OSM Libraries:</b></td>
                <td style="padding: 4px;">{osm_count}</td>
            </tr>
            <tr>
                <td style="padding: 4px;"><b>Official Libraries:</b></td>
                <td style="padding: 4px;">{official_count}</td>
            </tr>
            <tr style="background-color: #ECF0F1;">
                <td style="padding: 4px;"><b>Completeness:</b></td>
                <td style="padding: 4px; color: {'green' if completeness_val >= 75 else 'red'};">
                    <b>{completeness_val:.1f}%</b>
                </td>
            </tr>
        </table>
    </div>
    """
    
    # Add polygon
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, comp=completeness_val: {
            'fillColor': get_color(comp),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        },
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 180px; height: 200px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 10px">
<p style="margin:0; font-weight: bold;">Completeness %</p>
<p style="margin:5px 0;"><span style="background-color:#2ECC71; width:20px; height:15px; display:inline-block; margin-right:5px;"></span>≥100%</p>
<p style="margin:5px 0;"><span style="background-color:#F39C12; width:20px; height:15px; display:inline-block; margin-right:5px;"></span>75-99%</p>
<p style="margin:5px 0;"><span style="background-color:#E67E22; width:20px; height:15px; display:inline-block; margin-right:5px;"></span>50-74%</p>
<p style="margin:5px 0;"><span style="background-color:#E74C3C; width:20px; height:15px; display:inline-block; margin-right:5px;"></span>25-49%</p>
<p style="margin:5px 0;"><span style="background-color:#C0392B; width:20px; height:15px; display:inline-block; margin-right:5px;"></span>0-24%</p>
<p style="margin:5px 0;"><span style="background-color:#CCCCCC; width:20px; height:15px; display:inline-block; margin-right:5px;"></span>No data</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save map
print("\n4/4 Saving map...")
output_file = 'outputs/maps/library_completeness_map.html'
m.save(output_file)
print(f"  ✓ Saved: {output_file}")

print("\n" + "=" * 60)
print("Map created successfully!")
print(f"  Open in browser: {output_file}")
print("=" * 60)
