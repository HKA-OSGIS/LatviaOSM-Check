#!/usr/bin/env python3
"""Create interactive web map"""

import geopandas as gpd
import folium

print("=" * 60)
print("Creating Interactive Map")
print("=" * 60)
print()

print("1/2 Loading data...")
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
print(f"✓ Loaded {len(gdf)} LAU-1 municipalities with official data")

print("\n2/2 Creating map...")

def get_color(category):
    colors = {
        'Low': '#d73027',
        'Partial': '#fc8d59',
        'Complete': '#91cf60',
        'Over-mapped': '#4575b4',
        'No data': '#cccccc'
    }
    return colors.get(category, '#cccccc')

m = folium.Map(location=[56.8, 24.6], zoom_start=7, tiles='CartoDB positron')

# Title
title_html = '''
<div style="position: fixed; top: 10px; left: 50px; width: 450px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 10px; border-radius: 5px;">

</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Add polygons
for _, row in gdf.iterrows():
    # Build comprehensive popup with ALL available information
    if row['category'] == 'No data':
        popup = f"""
        <div style="width: 320px; font-family: Arial; font-size: 11px;">
            <h4 style="margin: 0 0 12px 0; color: #1976D2; border-bottom: 2px solid #2196F3; padding-bottom: 8px;">
                {row['municipality_name']}
            </h4>
            
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 6px; border: 1px solid #ddd; font-weight: bold;">Municipality ID:</td>
                    <td style="padding: 6px; border: 1px solid #ddd;">{row['municipality_id']}</td>
                </tr>
                
                <tr style="background-color: #fff9c4;">
                    <td style="padding: 6px; border: 1px solid #ddd; font-weight: bold;">OSM Roads:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right; font-weight: bold; color: #2196F3;">{row['osm_road_km']:.2f} km</td>
                </tr>
                
                <tr>
                    <td style="padding: 6px; border: 1px solid #ddd;">Road Segments:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{int(row['num_segments'])}</td>
                </tr>
                
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 6px; border: 1px solid #ddd;">Municipality Area:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{row['area_km2']:.2f} km²</td>
                </tr>
                
                <tr>
                    <td style="padding: 6px; border: 1px solid #ddd;">Road Density:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{row['road_density_km_per_km2']:.3f} km/km²</td>
                </tr>
                
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 6px; border: 1px solid #ddd;">Shape Type:</td>
                    <td style="padding: 6px; border: 1px solid #ddd;">{row.get('shapeType', 'N/A')}</td>
                </tr>
                
                <tr>
                    <td style="padding: 6px; border: 1px solid #ddd;">Shape Group:</td>
                    <td style="padding: 6px; border: 1px solid #ddd;">{row.get('shapeGroup', 'N/A')}</td>
                </tr>
                
                <tr style="background-color: #fce4ec;">
                    <td colspan="2" style="padding: 8px; border: 1px solid #ddd; text-align: center; font-style: italic; color: #d32f2f;">
                        ⚠ Official road data not available
                    </td>
                </tr>
            </table>
        </div>
        """
        tooltip_text = f"{row['municipality_name']}: {row['osm_road_km']:.1f} km OSM"
    else:
        popup = f"""
        <div style="width: 340px; font-family: Arial; font-size: 11px;">
            <h4 style="margin: 0 0 12px 0; color: #1976D2; border-bottom: 2px solid #2196F3; padding-bottom: 8px;">
                {row['municipality_name']}
            </h4>
            
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #e8f5e9;">
                    <td style="padding: 6px; border: 1px solid #ddd; font-weight: bold;">Completeness:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right; font-weight: bold; font-size: 13px; color: #2e7d32;">
                        {row['completeness_pct']:.1f}%
                    </td>
                </tr>
                
                <tr>
                    <td style="padding: 6px; border: 1px solid #ddd; font-weight: bold;">Category:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">
                        <span style="padding: 2px 6px; background: #2196F3; color: white; border-radius: 3px; font-weight: bold;">
                            {row['category']}
                        </span>
                    </td>
                </tr>
                
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 6px; border: 1px solid #ddd;">Municipality ID:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{row['municipality_id']}</td>
                </tr>
                
                <tr style="background-color: #fff3e0;">
                    <td style="padding: 6px; border: 1px solid #ddd; font-weight: bold;">OSM Roads:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right; font-weight: bold; color: #e65100;">{row['osm_road_km']:.2f} km</td>
                </tr>
                
                <tr style="background-color: #fff3e0;">
                    <td style="padding: 6px; border: 1px solid #ddd; font-weight: bold;">Official Roads:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right; font-weight: bold; color: #e65100;">{row['road_length_km']:.2f} km</td>
                </tr>
                
                <tr style="background-color: #fff3e0;">
                    <td style="padding: 6px; border: 1px solid #ddd; font-weight: bold;">Difference:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right; font-weight: bold; color: {('#d32f2f' if row['difference_km'] >= 0 else '#1976D2')};">
                        {row['difference_km']:+.2f} km
                    </td>
                </tr>
                
                <tr>
                    <td style="padding: 6px; border: 1px solid #ddd;">Road Segments:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{int(row['num_segments'])}</td>
                </tr>
                
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 6px; border: 1px solid #ddd;">Municipality Area:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{row['area_km2']:.2f} km²</td>
                </tr>
                
                <tr>
                    <td style="padding: 6px; border: 1px solid #ddd;">Road Density:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{row['road_density_km_per_km2']:.3f} km/km²</td>
                </tr>
                
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 6px; border: 1px solid #ddd;">Shape Type:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{row.get('shapeType', 'N/A')}</td>
                </tr>
                
                <tr>
                    <td style="padding: 6px; border: 1px solid #ddd;">Shape Group:</td>
                    <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{row.get('shapeGroup', 'N/A')}</td>
                </tr>
            </table>
        </div>
        """
        tooltip_text = f"{row['municipality_name']}: {row['completeness_pct']:.1f}% complete ({row['osm_road_km']:.1f} km)"
    
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, c=row['category']: {
            'fillColor': get_color(c),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        popup=popup,
        tooltip=tooltip_text
    ).add_to(m)

# Legend
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 220px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 10px; border-radius: 5px; font-size: 12px;">
    <p style="margin: 0; font-weight: bold;">Road Completeness</p>
    <p style="margin: 5px 0;">
        <span style="background: #91cf60; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Complete (95-105%)
    </p>
    <p style="margin: 5px 0;">
        <span style="background: #fc8d59; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Partial (50-95%)
    </p>
    <p style="margin: 5px 0;">
        <span style="background: #d73027; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Low (&lt;50%)
    </p>
    <p style="margin: 5px 0;">
        <span style="background: #4575b4; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        Over-mapped (&gt;105%)
    </p>
    <p style="margin: 5px 0;">
        <span style="background: #cccccc; width: 20px; height: 15px; 
              display: inline-block; border: 1px solid black;"></span>
        No data
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

m.save('outputs/maps/interactive_map.html')
print("✓ Saved: outputs/maps/interactive_map.html")

print("\n" + "=" * 60)
print("✓ Interactive Map Created!")
print("=" * 60)
print()