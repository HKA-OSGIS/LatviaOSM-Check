#!/usr/bin/env python3
import pandas as pd

df = pd.read_csv('outputs/exports/completeness_municipalities_all.csv')

# Total municipalities
total = len(df)

# Municipalities with official road data (non-zero)
with_official = (df['Official_Roads_km'] > 0).sum()

# Overall completeness
df_with_official = df[df['Official_Roads_km'] > 0].copy()
if len(df_with_official) > 0:
    overall_completeness = (df_with_official['OSM_Roads_km'].sum() / df_with_official['Official_Roads_km'].sum()) * 100
    high = (df_with_official['Completeness_%'] >= 50).sum()
    medium = ((df_with_official['Completeness_%'] >= 20) & (df_with_official['Completeness_%'] < 50)).sum()
    low = ((df_with_official['Completeness_%'] > 0) & (df_with_official['Completeness_%'] < 20)).sum()
    zero = (df_with_official['Completeness_%'] == 0).sum()
else:
    overall_completeness = 0
    high = medium = low = zero = 0

print(f'Total municipalities: {total}')
print(f'Municipalities with official data: {with_official}')
print(f'Overall completeness: {overall_completeness:.1f}%')
print(f'High (≥50%): {high}')
print(f'Medium (20-50%): {medium}')
print(f'Low (0-20%): {low}')
print(f'Zero (0%): {zero}')
