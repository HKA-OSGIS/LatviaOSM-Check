#!/usr/bin/env python3
import json
import urllib.request

data = json.load(urllib.request.urlopen('http://localhost:5000/api/geojson-data'))
print(f'Features in map: {len(data["features"])}')
print(f'First 3 municipalities:')
for feat in data["features"][:3]:
    print(f'  - {feat["properties"]["shapeName"]}')
