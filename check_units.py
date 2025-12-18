import geopandas as gpd

gdf = gpd.read_file('outputs/exports/latvia_clean_33.geojson')
print(f"Total features: {len(gdf)}")
print("\nMunicipalities:")
for name in sorted(gdf['municipality_name']):
    print(f"  {name}")
