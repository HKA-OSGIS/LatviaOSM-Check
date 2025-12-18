#!/usr/bin/env python3
"""Create interactive map with LAU-1 boundaries and official data"""

import geopandas as gpd
import folium
import pandas as pd

print("=" * 70)
print("Creating Interactive Map with LAU-1 Municipalities & Official Data")
print("=" * 70)
print()

# Load LAU-1 GeoJSON with merged data
print("1/3 Loading LAU-1 GeoJSON with municipality boundaries...")
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')
print(f"✓ Loaded {len(gdf)} LAU-1 municipalities")
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
    if completeness >= 100:
        return '#4575b4'  # Over-mapped (blue)
    elif completeness >= 80:
        return '#91cf60'  # Complete (green)
    elif completeness >= 50:
        return '#fc8d59'  # Partial (orange)
    else:
        return '#d73027'  # Low (red)

print("3/3 Adding municipality boundaries with popups...")

# Add GeoJSON features with popups
for idx, row in gdf.iterrows():
    mun_name = row['municipality_name']
    osm_km = float(row.get('osm_road_km', 0))
    
    # Handle official_road_km - could be string or numeric
    official_km = row.get('official_road_km', None)
    if official_km is not None:
        try:
            official_km = float(official_km)
        except (ValueError, TypeError):
            official_km = None
    
    completeness = row.get('completeness_pct', None)
    if completeness is not None:
        try:
            completeness = float(completeness)
        except (ValueError, TypeError):
            completeness = None
    
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
                    {f'{official_km:.2f}' if not pd.isna(official_km) else 'N/A'} km
                </td>
            </tr>
            <tr style="background-color: #f5f5f5;">
                <td style="padding: 6px; font-weight: bold;">Completeness:</td>
                <td style="padding: 6px; text-align: right; color: {get_color(completeness)}; font-weight: bold;">
                    {f'{completeness:.1f}%' if not pd.isna(completeness) else 'N/A'}
                </td>
            </tr>
        </table>
        
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 11px; color: #666;">
            <p style="margin: 0;">
                <strong>Interpretation:</strong><br>
                • &lt;50%: Low coverage<br>
                • 50-80%: Partial coverage<br>
                • 80-100%: Complete coverage<br>
                • &gt;100%: Over-mapped (OSM > official)
            </p>
        </div>
    </div>
    """
    
    # Determine color based on completeness
    color = get_color(completeness)
    
    # Add feature to map
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, color=color: {
            'fillColor': color,
            'color': '#333',
            'weight': 1,
            'opacity': 0.7,
            'fillOpacity': 0.6,
            'dashArray': '5, 5'
        },
        popup=folium.Popup(popup_html, max_width=400),
        tooltip=f"{mun_name}: {completeness:.1f}%" if not pd.isna(completeness) else mun_name
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; bottom: 50px; right: 10px; width: 240px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 15px; border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
    <h4 style="margin: 0 0 12px 0; color: #1976D2;">Road Completeness</h4>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #d73027; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Low (&lt;50%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #fc8d59; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Partial (50-80%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #91cf60; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Complete (80-100%)
    </p>
    <p style="margin: 0; font-size: 12px;">
        <i style="background-color: #4575b4; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; Over-mapped (&gt;100%)
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save map
output_path = 'outputs/maps/interactive_map.html'
m.save(output_path)
print(f"✓ Saved: {output_path}")
print()

# Summary statistics
print("=" * 70)
print("Summary Statistics:")
print("=" * 70)
print(f"Total municipalities: {len(gdf)}")
print(f"Municipalities with complete data: {gdf['official_road_km'].notna().sum()}")
print(f"Average completeness: {gdf['completeness_pct'].mean():.1f}%")
print(f"Min completeness: {gdf['completeness_pct'].min():.1f}%")
print(f"Max completeness: {gdf['completeness_pct'].max():.1f}%")
print()

# Show municipalities by completeness category
print("Completeness Categories:")
print("-" * 70)
low = (gdf['completeness_pct'] < 50).sum()
partial = ((gdf['completeness_pct'] >= 50) & (gdf['completeness_pct'] < 80)).sum()
complete = ((gdf['completeness_pct'] >= 80) & (gdf['completeness_pct'] <= 100)).sum()
overmapped = (gdf['completeness_pct'] > 100).sum()

print(f"  Low (<50%):            {low} municipalities")
print(f"  Partial (50-80%):      {partial} municipalities")
print(f"  Complete (80-100%):    {complete} municipalities")
print(f"  Over-mapped (>100%):   {overmapped} municipalities")
print()

# Top 5 best and worst
print("Top 5 Best Mapped (Highest Completeness):")
print("-" * 70)
top5 = gdf.nlargest(5, 'completeness_pct')[['municipality_name', 'completeness_pct']]
for idx, (_, row) in enumerate(top5.iterrows(), 1):
    print(f"  {idx}. {row['municipality_name']}: {row['completeness_pct']:.1f}%")
print()

print("Top 5 Least Mapped (Lowest Completeness):")
print("-" * 70)
bottom5 = gdf.nsmallest(5, 'completeness_pct')[['municipality_name', 'completeness_pct']]
for idx, (_, row) in enumerate(bottom5.iterrows(), 1):
    print(f"  {idx}. {row['municipality_name']}: {row['completeness_pct']:.1f}%")
print()

print("✓ Map generation completed successfully!")
print("=" * 70)
