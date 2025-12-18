#!/usr/bin/env python3
"""Compare old and new TRS020 files."""

import pandas as pd

# Load both files
old = pd.read_csv('data/raw/TRS020_20251218-012055.csv', skiprows=1)
new = pd.read_csv('data/raw/TRS020_20251218-165232.csv', skiprows=1)

print('OLD file (012055):')
print(f'  Rows: {len(old)}')
print(f'  Columns: {old.columns.tolist()}')
print(f'  Unique municipalities: {old["Territorial unit"].nunique()}')

print('\nNEW file (165232):')
print(f'  Rows: {len(new)}')
print(f'  Columns: {new.columns.tolist()}')
print(f'  Unique municipalities: {new["Territorial unit"].nunique()}')

# Check if data is different
if old.equals(new):
    print('\n✓ Files are IDENTICAL')
else:
    print('\n✗ Files are DIFFERENT')
    
# Show total values
if '2024' in old.columns and '2024' in new.columns:
    old_total = old[old['Indicator'] == 'Total']['2024'].sum()
    new_total = new[new['Indicator'] == 'Total']['2024'].sum()
    print(f'\nOld total roads: {old_total:,} km')
    print(f'New total roads: {new_total:,} km')
    print(f'Difference: {new_total - old_total:,} km')
