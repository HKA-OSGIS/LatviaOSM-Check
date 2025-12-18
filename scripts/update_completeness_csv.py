#!/usr/bin/env python3
"""Generate completeness.csv from LAU-1 GeoJSON"""

import geopandas as gpd
import pandas as pd

# Load LAU-1 GeoJSON
gdf = gpd.read_file('outputs/exports/latvia_lau1.geojson')

# Drop geometry column for CSV export
df = pd.DataFrame(gdf.drop(columns='geometry'))

# Save to CSV
df.to_csv('outputs/exports/completeness.csv', index=False, encoding='utf-8')

print(f"✓ Generated completeness.csv with {len(df)} municipalities")
print(f"  Columns: {list(df.columns)}")
