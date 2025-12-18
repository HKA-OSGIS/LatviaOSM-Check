import pandas as pd

df = pd.read_csv('data/raw/TRS020_20251218-012055.csv', encoding='utf-8', skiprows=1)

# Count municipalities
mun = df[df['Territorial unit'].str.contains('municipality', case=False, na=False)]
mun = mun[(mun['Types of surface'] == 'Total') & (mun['Indicator'] == 'Total')]

# Count state cities  
city = df[~df['Territorial unit'].str.contains('municipality|region|statistical', case=False, na=False)]
city = city[(city['Types of surface'] == 'Total') & (city['Indicator'] == 'Total')]

print("=" * 60)
print("CSV CONTENTS (TRS020_20251218-012055.csv)")
print("=" * 60)
print(f"\nMunicipalities: {mun['Territorial unit'].nunique()}")
for i, name in enumerate(sorted(mun['Territorial unit'].unique()), 1):
    print(f"  {i}. {name}")

print(f"\nState Cities: {city['Territorial unit'].nunique()}")
for i, name in enumerate(sorted(city['Territorial unit'].unique()), 1):
    print(f"  {i}. {name}")

print(f"\nTOTAL: {mun['Territorial unit'].nunique() + city['Territorial unit'].nunique()} administrative units")
print("=" * 60)
