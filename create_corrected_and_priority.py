#!/usr/bin/env python3
"""Generate corrected dataset and mapping priority visualization"""

import geopandas as gpd
import pandas as pd
import folium

print("=" * 80)
print("CREATING CORRECTED DATASET & MAPPING PRIORITY MAP")
print("=" * 80)
print()

# Load data
gdf = gpd.read_file('outputs/exports/latvia_official_only.geojson')

# Convert to numeric types
gdf['osm_road_km'] = pd.to_numeric(gdf['osm_road_km'], errors='coerce')
gdf['official_road_km'] = pd.to_numeric(gdf['official_road_km'], errors='coerce')
gdf['completeness_pct'] = pd.to_numeric(gdf['completeness_pct'], errors='coerce')

# Fix NaN values - recalculate for entries with missing official_road_km
print("1. Fixing data quality issues...")
print(f"   Before: {gdf['official_road_km'].isna().sum()} NaN values in official_road_km")

# Recalculate completeness for rows with NaN
for idx, row in gdf.iterrows():
    if pd.isna(row['official_road_km']) and pd.notna(row['osm_road_km']):
        # If official data missing but OSM exists, mark as data_quality_issue
        gdf.at[idx, 'data_quality_flag'] = 'missing_official_data'
    elif pd.isna(row['completeness_pct']) and pd.notna(row['osm_road_km']) and pd.notna(row['official_road_km']):
        # Recalculate completeness if missing
        gdf.at[idx, 'completeness_pct'] = (row['osm_road_km'] / row['official_road_km'] * 100)

print(f"   After: {gdf['official_road_km'].isna().sum()} NaN values in official_road_km")

# Fill missing official_road_km with median for visualization
gdf_clean = gdf.copy()
median_official = gdf['official_road_km'].median()
gdf_clean['official_road_km'] = gdf_clean['official_road_km'].fillna(median_official)
gdf_clean['completeness_pct'] = gdf_clean['completeness_pct'].fillna(100)
gdf_clean['data_quality_flag'] = gdf_clean['data_quality_flag'].fillna('complete')

print()
print("2. Saving corrected dataset...")

# Save corrected GeoJSON
gdf_clean.to_file('outputs/exports/latvia_corrected.geojson', driver='GeoJSON', encoding='utf-8')
print("   ✓ Saved: outputs/exports/latvia_corrected.geojson")

# Save corrected CSV for analysis
df_clean = pd.DataFrame(gdf_clean.drop(columns='geometry'))
df_clean.to_csv('outputs/exports/latvia_corrected.csv', index=False, encoding='utf-8')
print("   ✓ Saved: outputs/exports/latvia_corrected.csv")

print()
print("3. Calculating mapping priorities...")

# Create priority classification
def get_priority(row):
    completeness = row['completeness_pct']
    if completeness < 50:
        return 'Critical'
    elif completeness < 80:
        return 'High'
    elif completeness < 100:
        return 'Medium'
    elif completeness <= 120:
        return 'Complete'
    else:
        return 'Over-mapped'

gdf_clean['priority'] = gdf_clean.apply(get_priority, axis=1)

# Calculate mapping effort needed
gdf_clean['km_to_map'] = (gdf_clean['official_road_km'] - gdf_clean['osm_road_km']).clip(lower=0)

priority_counts = gdf_clean['priority'].value_counts()
print("   Priority distribution:")
for priority in ['Critical', 'High', 'Medium', 'Complete', 'Over-mapped']:
    count = priority_counts.get(priority, 0)
    if count > 0:
        print(f"     {priority}: {count} units")

print()
print("4. Creating mapping priority map...")

# Create map
m = folium.Map(
    location=[56.8, 24.6],
    zoom_start=7,
    tiles='CartoDB positron'
)

# Color function by priority
def get_priority_color(priority):
    colors = {
        'Critical': '#d73027',      # Dark red
        'High': '#fc8d59',          # Orange
        'Medium': '#fee090',        # Yellow
        'Complete': '#91cf60',      # Green
        'Over-mapped': '#4575b4'    # Blue
    }
    return colors.get(priority, '#cccccc')

# Add features
for idx, row in gdf_clean.iterrows():
    priority = row['priority']
    municipality = row['municipality_name']
    osm_km = row['osm_road_km']
    official_km = row['official_road_km']
    completeness = row['completeness_pct']
    km_needed = row['km_to_map']
    
    # Create popup
    if priority == 'Critical':
        priority_text = '🚨 CRITICAL - Urgent mapping needed'
        explanation = f"Only {completeness:.1f}% of official roads are in OSM. Missing ~{km_needed:.0f}km out of {official_km:.0f}km"
    elif priority == 'High':
        priority_text = '⚠️ HIGH - Should be mapped'
        explanation = f"{completeness:.1f}% complete. Missing ~{km_needed:.0f}km"
    elif priority == 'Medium':
        priority_text = '📝 MEDIUM - Could be improved'
        explanation = f"{completeness:.1f}% complete. Missing ~{km_needed:.0f}km"
    elif priority == 'Complete':
        priority_text = '✅ COMPLETE - Well mapped'
        explanation = f"{completeness:.1f}% of official roads in OSM"
    else:
        priority_text = '🔍 OVER-MAPPED - Check for errors'
        explanation = f"{completeness:.1f}% - More OSM data than official statistics. May indicate double-mapping or classification differences"
    
    popup_html = f"""
    <div style="width: 280px; font-family: Arial; font-size: 12px;">
        <h4 style="margin: 0 0 10px 0; color: #1976D2; border-bottom: 2px solid #2196F3; padding-bottom: 8px;">
            {municipality}
        </h4>
        <p style="margin: 0 0 8px 0; font-weight: bold; color: {get_priority_color(priority)};">
            {priority_text}
        </p>
        <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
            <tr style="background-color: #f5f5f5;">
                <td style="padding: 5px; font-weight: bold;">OSM Roads:</td>
                <td style="padding: 5px; text-align: right;">{osm_km:.0f} km</td>
            </tr>
            <tr>
                <td style="padding: 5px; font-weight: bold;">Official Roads:</td>
                <td style="padding: 5px; text-align: right;">{official_km:.0f} km</td>
            </tr>
            <tr style="background-color: #f5f5f5;">
                <td style="padding: 5px; font-weight: bold;">Completeness:</td>
                <td style="padding: 5px; text-align: right; color: {get_priority_color(priority)}; font-weight: bold;">
                    {completeness:.1f}%
                </td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 8px; border-top: 1px solid #ddd; color: #666; font-size: 10px;">
                    {explanation}
                </td>
            </tr>
        </table>
    </div>
    """
    
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, color=get_priority_color(priority): {
            'fillColor': color,
            'color': '#333',
            'weight': 1,
            'opacity': 0.7,
            'fillOpacity': 0.6,
        },
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=f"{municipality}: {priority} ({completeness:.0f}%)"
    ).add_to(m)

# Add title
title_html = '''
<div style="position: fixed; top: 10px; left: 50px; width: 500px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 15px; border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
    <h3 style="margin: 0; color: #1976D2;">Latvia OSM Mapping Priority Map</h3>
    <p style="margin: 5px 0 0 0; font-size: 12px; color: #555;">
        Areas highlighted by urgency of OSM improvement needed
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Add legend
legend_html = '''
<div style="position: fixed; bottom: 50px; right: 10px; width: 260px;
     background-color: white; border: 2px solid grey; z-index: 9999;
     padding: 15px; border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
    <h4 style="margin: 0 0 12px 0; color: #1976D2;">Mapping Priority</h4>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #d73027; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; <b>Critical</b> (<50%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #fc8d59; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; <b>High</b> (50-80%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #fee090; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; <b>Medium</b> (80-100%)
    </p>
    <p style="margin: 0 0 8px 0; font-size: 12px;">
        <i style="background-color: #91cf60; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; <b>Complete</b> (≈100%)
    </p>
    <p style="margin: 0; font-size: 12px;">
        <i style="background-color: #4575b4; width: 20px; height: 15px; display: inline-block;"></i>
        &nbsp; <b>Over-mapped</b> (>100%)
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save map
m.save('outputs/maps/mapping_priority_map.html')
print("   ✓ Saved: outputs/maps/mapping_priority_map.html")

print()
print("5. Summary Statistics")
print("-" * 80)

critical = gdf_clean[gdf_clean['priority'] == 'Critical']
high = gdf_clean[gdf_clean['priority'] == 'High']
medium = gdf_clean[gdf_clean['priority'] == 'Medium']
complete = gdf_clean[gdf_clean['priority'] == 'Complete']
overmapped = gdf_clean[gdf_clean['priority'] == 'Over-mapped']

print(f"🚨 Critical (0-50%):          {len(critical)} units - {critical['km_to_map'].sum():.0f}km to map")
print(f"⚠️  High (50-80%):            {len(high)} units - {high['km_to_map'].sum():.0f}km to map")
print(f"📝 Medium (80-100%):          {len(medium)} units - {medium['km_to_map'].sum():.0f}km to map")
print(f"✅ Complete (~100%):          {len(complete)} units")
print(f"🔍 Over-mapped (>100%):       {len(overmapped)} units (needs verification)")
print()

total_to_map = gdf_clean['km_to_map'].sum()
print(f"Total OSM mapping effort needed: {total_to_map:.0f} km")
print(f"Estimated effort: {total_to_map/50:.0f} mapper-weeks (at 50km/week per mapper)")

print()
print("=" * 80)
print("✓ All files generated successfully!")
print("=" * 80)
