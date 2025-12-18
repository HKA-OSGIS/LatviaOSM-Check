import geopandas as gpd
import pandas as pd

gdf = gpd.read_file('outputs/exports/latvia_official_only.geojson')
gdf['osm_road_km'] = pd.to_numeric(gdf['osm_road_km'], errors='coerce')
gdf['official_road_km'] = pd.to_numeric(gdf['official_road_km'], errors='coerce')
gdf['completeness_pct'] = pd.to_numeric(gdf['completeness_pct'], errors='coerce')

df = pd.DataFrame(gdf.drop(columns='geometry'))
df.to_csv('outputs/exports/completeness.csv', index=False, encoding='utf-8')

print(f'✓ Updated completeness.csv')
print(f'  Units: {len(df)}')
print(f'  OSM: {df["osm_road_km"].sum():.0f}km')
print(f'  Official: {df["official_road_km"].sum():.0f}km')
