#!/usr/bin/env python3
"""Generate Data Quality Analysis Report"""

import geopandas as gpd
import pandas as pd
import json

print("=" * 80)
print("LATVIA OSM ROAD DATA - QUALITY ANALYSIS REPORT")
print("=" * 80)
print()

# Load data
gdf = gpd.read_file('outputs/exports/latvia_official_only.geojson')
df = pd.DataFrame(gdf.drop(columns='geometry'))

# Convert to numeric types
df['osm_road_km'] = pd.to_numeric(df['osm_road_km'], errors='coerce')
df['official_road_km'] = pd.to_numeric(df['official_road_km'], errors='coerce')
df['completeness_pct'] = pd.to_numeric(df['completeness_pct'], errors='coerce')

print("1. DATA OVERVIEW")
print("-" * 80)
print(f"Total administrative units: {len(df)}")
print(f"Municipalities: {(df['municipality_name'].str.contains('municipality', case=False, na=False)).sum()}")
print(f"State cities: {(~df['municipality_name'].str.contains('municipality', case=False, na=False)).sum()}")
print(f"Total OSM road length: {df['osm_road_km'].sum():.0f} km")
print(f"Total official road length: {df['official_road_km'].sum():.0f} km")
print(f"Average completeness: {df['completeness_pct'].mean():.1f}%")
print()

print("2. DATA QUALITY ISSUES")
print("-" * 80)

# Over-mapped areas (>100% completeness)
print("\n🔵 OVER-MAPPED AREAS (OSM > Official data):")
print("  These areas have MORE roads in OSM than official statistics show")
print("  Possible reasons: Dual carriageways, mapper enthusiasm, classification differences")
overmapped = df[df['completeness_pct'] > 100].sort_values('completeness_pct', ascending=False)
for idx, row in overmapped.iterrows():
    print(f"    • {row['municipality_name']}: {row['completeness_pct']:.1f}% (OSM: {row['osm_road_km']:.0f}km vs Official: {row['official_road_km']:.0f}km)")

# Under-mapped areas (<50% completeness)
print("\n🔴 CRITICALLY UNDER-MAPPED AREAS (OSM < 50% of Official):")
print("  These areas need immediate OSM mapping attention")
print("  Missing ~50% or more of official roads")
undermapped = df[df['completeness_pct'] < 50].sort_values('completeness_pct')
for idx, row in undermapped.iterrows():
    missing_km = row['official_road_km'] - row['osm_road_km']
    print(f"    • {row['municipality_name']}: {row['completeness_pct']:.1f}% (Missing ~{missing_km:.0f}km of {row['official_road_km']:.0f}km)")

# Partial mapping (50-80%)
print("\n🟠 PARTIAL MAPPING (50-80% completeness):")
print("  These areas have good coverage but could be improved")
partial = df[(df['completeness_pct'] >= 50) & (df['completeness_pct'] < 80)].sort_values('completeness_pct')
for idx, row in partial.iterrows():
    missing_km = row['official_road_km'] - row['osm_road_km']
    print(f"    • {row['municipality_name']}: {row['completeness_pct']:.1f}% (Missing ~{missing_km:.0f}km)")

# Well-mapped areas (80-100%)
print("\n🟢 WELL-MAPPED AREAS (80-100% completeness):")
wellmapped = df[(df['completeness_pct'] >= 80) & (df['completeness_pct'] <= 100)].sort_values('completeness_pct', ascending=False)
for idx, row in wellmapped.iterrows():
    print(f"    • {row['municipality_name']}: {row['completeness_pct']:.1f}%")

print()
print("3. GEOGRAPHIC PATTERNS")
print("-" * 80)

# State cities analysis
print("\nSTATE CITIES vs MUNICIPALITIES:")
is_municipality = df['municipality_name'].str.contains('municipality', case=False, na=False)
mun_avg = df[is_municipality]['completeness_pct'].mean()
city_avg = df[~is_municipality]['completeness_pct'].mean()
print(f"  Municipalities average completeness: {mun_avg:.1f}%")
print(f"  State cities average completeness: {city_avg:.1f}%")
if city_avg > mun_avg:
    print(f"  → State cities are {city_avg - mun_avg:.1f}% better mapped (urban areas get more attention)")
else:
    print(f"  → Municipalities are {mun_avg - city_avg:.1f}% better mapped")

print()
print("4. PRIORITY RECOMMENDATIONS FOR OSM IMPROVEMENT")
print("-" * 80)
print()

# Priority 1: Critical gaps
critical = df[df['completeness_pct'] < 50].sort_values('completeness_pct')
if len(critical) > 0:
    print("🚨 PRIORITY 1 - CRITICAL MAPPING GAPS (Completeness < 50%):")
    total_missing = (critical['official_road_km'] - critical['osm_road_km']).sum()
    print(f"   {len(critical)} municipality/city with {total_missing:.0f}km of unmapped roads")
    for idx, row in critical.head(5).iterrows():
        pct_missing = ((row['official_road_km'] - row['osm_road_km']) / row['official_road_km'] * 100)
        print(f"   - {row['municipality_name']}: {pct_missing:.0f}% of roads missing ({row['official_road_km'] - row['osm_road_km']:.0f}km)")
else:
    print("✓ No critical mapping gaps")

print()

# Priority 2: Significant gaps
partial_gaps = df[(df['completeness_pct'] >= 50) & (df['completeness_pct'] < 80)].sort_values('completeness_pct')
if len(partial_gaps) > 0:
    print("⚠️  PRIORITY 2 - SIGNIFICANT GAPS (Completeness 50-80%):")
    total_missing = (partial_gaps['official_road_km'] - partial_gaps['osm_road_km']).sum()
    print(f"   {len(partial_gaps)} municipalities with {total_missing:.0f}km of unmapped roads")
    for idx, row in partial_gaps.iterrows():
        pct_missing = ((row['official_road_km'] - row['osm_road_km']) / row['official_road_km'] * 100)
        print(f"   - {row['municipality_name']}: {pct_missing:.0f}% of roads missing ({row['official_road_km'] - row['osm_road_km']:.0f}km)")
else:
    print("✓ No significant mapping gaps")

print()

# Priority 3: Quality check - over-mapped areas
if len(overmapped) > 0:
    print("🔍 PRIORITY 3 - DATA QUALITY CHECK (Over-mapped areas):")
    print(f"   {len(overmapped)} municipality/city with MORE roads than official data")
    print("   Need verification: Are these double-mapped routes, different road classifications, or mapping errors?")
    for idx, row in overmapped.head(3).iterrows():
        excess = row['osm_road_km'] - row['official_road_km']
        print(f"   - {row['municipality_name']}: +{excess:.0f}km excess ({row['completeness_pct']:.0f}%)")
else:
    print("✓ No over-mapped areas detected")

print()
print("5. SUMMARY STATISTICS")
print("-" * 80)
print(f"Well-mapped (≥80%):        {len(df[df['completeness_pct'] >= 80])} units ({len(df[df['completeness_pct'] >= 80])/len(df)*100:.0f}%)")
print(f"Partial (50-80%):          {len(df[(df['completeness_pct'] >= 50) & (df['completeness_pct'] < 80)])} units ({len(df[(df['completeness_pct'] >= 50) & (df['completeness_pct'] < 80)])/len(df)*100:.0f}%)")
print(f"Under-mapped (<50%):       {len(df[df['completeness_pct'] < 50])} units ({len(df[df['completeness_pct'] < 50])/len(df)*100:.0f}%)")
print(f"Over-mapped (>100%):       {len(overmapped)} units ({len(overmapped)/len(df)*100:.0f}%)")
print()

# Calculate total mapping effort needed
total_missing = (df['official_road_km'] - df['osm_road_km']).sum()
if total_missing > 0:
    print(f"Total OSM mapping effort needed: ~{total_missing:.0f}km")
    print(f"That's approximately {total_missing/50:.0f} mapper-weeks at 50km/week per mapper")
else:
    print("✓ All official roads are already well-mapped in OSM!")

print()
print("=" * 80)
print("Report generated:", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 80)
