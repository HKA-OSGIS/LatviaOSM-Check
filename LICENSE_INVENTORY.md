# License Inventory for LatviaOSM-Check Project

**Date**: January 28, 2026  
**Total Licenses Used**: **8+ licenses**

---

## License Summary Overview

```
LatviaOSM-Check Project License Stack:
═════════════════════════════════════════════════════════════════

TIER 1: PROJECT CODE (1 License)
├─ MIT License
└─ Our application code

TIER 2: DATA LAYERS (3 Licenses)
├─ ODbL (Open Database License) - OSM data
├─ CC-BY or Government License - Official statistics
└─ ODbL - Derived data/analysis

TIER 3: FRAMEWORK & CORE LIBRARIES (3 Licenses)
├─ BSD 3-Clause - Flask, Werkzeug, Jinja2, GeoPandas, Shapely, Pandas
├─ MIT - Fiona, PyOGRIO, Folium, Requests
└─ GPL v2 - FuzzyWuzzy (⚠️ Compatibility note)

TIER 4: FRONTEND LIBRARIES (2 Licenses)
├─ BSD 2-Clause - Leaflet.js
└─ MIT - Bootstrap 5, jQuery

TIER 5: DATA SOURCES (2 External)
├─ ODbL - OpenStreetMap content
└─ Government/CC-BY - Official statistics

TOTAL DISTINCT LICENSES: 8
```

---

## Detailed License Breakdown

### TIER 1: Project Code

#### 1. MIT License ✅ (PRIMARY)

**Applies To**: 
- app.py (328 lines)
- scripts/ (20 pipeline scripts)
- src/processing/ (6 modules)
- templates/ (2 HTML templates)

**Files**:
- LICENSE (root)
- Specified in pyproject.toml
- Badge in README.md

**Details**:
```
Copyright (c) 2026 LatviaOSM-Check Project Contributors
Permission: Commercial use, modification, distribution
Condition: Include copyright notice
Warranty: None (as-is)
```

**Total**: **1 project license**

---

### TIER 2: Data Layers

#### 2. ODbL (Open Database License) 📊

**Applies To**:
- OSM data (latvia-latest.osm.pbf)
- Municipality boundaries (from OSM)
- roads.geojson (extracted from OSM)
- forests.geojson (extracted from OSM)
- libraries.geojson (extracted from OSM)
- All *_by_municipality.geojson files
- All derived analysis data

**Source**: OpenStreetMap contributors

**Details**:
```
License: Open Data Commons Open Database License (ODbL) v1.0
URL: https://www.openstreetmap.org/copyright
Requirement: Attribution + Share-Alike (data)
Commercial: Allowed
```

**Attribution Required**:
```
© OpenStreetMap contributors
OpenStreetMap data is licensed under the 
Open Database License (ODbL)
```

**Total**: **1 data license (ODbL)**

---

#### 3. Government / CC-BY License 📈

**Applies To**:
- Road.csv (official road statistics)
- Forest.csv (official forest statistics)
- Library.csv (official library statistics)
- official_*_stats.csv files
- TRS020_*.csv (Tax register data)
- railway_data.csv

**Source**: Latvian Central Statistical Bureau (CSB)

**Details**:
```
License: Government of Latvia / CC-BY (attribution)
Source: Government open data portal (data.gov.lv)
Requirement: Attribution to source
Commercial: Allowed with attribution
```

**Attribution Format**:
```
Source: Latvian Central Statistical Bureau (CSB)
License: CC-BY / Government Open Data
```

**Total**: **1 government license**

---

### TIER 3: Python Dependencies (8 Packages)

#### Package Licenses Breakdown

```
Python Dependencies License Summary:
═══════════════════════════════════════════════════════════════

Package Name          Version    License            Type
─────────────────────────────────────────────────────────────
Flask                 2.3.3      BSD 3-Clause       🟢 Compatible
GeoPandas             0.13.2     BSD 3-Clause       🟢 Compatible
Pandas                2.0.3      BSD 3-Clause       🟢 Compatible
Folium                0.14.0     MIT                🟢 Compatible
Requests              2.31.0     Apache 2.0         🟢 Compatible
Shapely               2.0.1      BSD 3-Clause       🟢 Compatible
Fiona                 1.9.4      MIT                🟢 Compatible
PyOGRIO               0.7.2      MIT                🟢 Compatible
FuzzyWuzzy            (latest)   GPL v2             ⚠️  Note*
```

#### BSD 3-Clause License 🟢 (4 Packages)

**Applies To**:
1. **Flask 2.3.3** - Web framework
2. **GeoPandas 0.13.2** - Geospatial dataframes
3. **Pandas 2.0.3** - Data manipulation
4. **Shapely 2.0.1** - Geometric operations
5. Plus: Werkzeug (Flask dependency)
6. Plus: Jinja2 (Flask template engine)
7. Plus: NumPy (Pandas dependency)

**License**:
```
Redistribution and use permitted with:
- Copyright notice
- Disclaimer of warranty
- Non-endorsement clause (3-Clause)
```

**Count**: **4 direct + 3 transitive dependencies**

---

#### MIT License 🟢 (3 Packages)

**Applies To**:
1. **Fiona 1.9.4** - GeoJSON/Shapefile I/O
2. **PyOGRIO 0.7.2** - GDAL wrapper
3. **Folium 0.14.0** - Interactive maps
4. **Requests 2.31.0** - HTTP client

**License**:
```
Permissive open-source license
- Use, modify, distribute (commercial ok)
- Keep copyright notice
- No warranty
```

**Count**: **4 packages**

---

#### GPL v2 License ⚠️ (1 Package)

**Applies To**:
1. **FuzzyWuzzy** - Fuzzy string matching

**Details**:
```
License: GNU General Public License v2
Weak Copyleft: Requires source disclosure if distributed
Note: Only triggers if you distribute executable
      Not triggered for SaaS/web deployment
```

**Usage in Project**:
- Used in scripts for Latvian name matching
- `src/processing/create_fuzzy_mapping.py`
- `src/processing/create_library_fuzzy_mapping.py`

**Implications**:
- ✅ Fine for web application (SaaS)
- ✅ Fine for research/educational
- ⚠️ Need to handle for executable distribution
- 🔧 Can replace with RapidFuzz (MIT) if needed

**Count**: **1 package (with considerations)**

---

### TIER 4: Frontend Libraries (2 Licenses)

#### 4. BSD 2-Clause License 🟢 (1 Frontend)

**Applies To**:
- **Leaflet.js 1.9+** - Interactive map library

**Usage**:
```
<!-- In templates/ -->
<script src="https://cdn.leafr.../leaflet.js"></script>
```

**License**:
```
BSD 2-Clause (Simplified)
- Use, modify, distribute
- Include copyright notice
- No warranty
```

**Count**: **1 frontend library**

---

#### 5. MIT License 🟢 (Multiple Frontend)

**Applies To**:
- **Bootstrap 5.x** - CSS framework
- **jQuery** - JavaScript library (if used)
- **OpenStreetMap tiles** - Tile provider

**Usage**:
```
<!-- In templates/ -->
<link rel="stylesheet" href="bootstrap.css">
```

**License**:
```
MIT - Simple permissive license
```

**Count**: **2+ frontend libraries**

---

### TIER 5: Data Source Attributions (2 External)

#### OpenStreetMap 🗺️

**License**: ODbL (covered above)

**Attribution**:
```
© OpenStreetMap contributors
Licensed under ODbL v1.0
```

**URL**: https://www.openstreetmap.org/copyright

---

#### Latvian Government Data 🏛️

**License**: Government Open Data / CC-BY

**Attribution**:
```
Source: Republic of Latvia Government / CSB
Licensed under CC-BY
```

**URL**: https://data.gov.lv

---

## License Compatibility Analysis

### Cross-License Compatibility

```
Compatibility Matrix:
═════════════════════════════════════════════════════════════════

Can we use these licenses together in one project?

MIT (Project)
├─ ✅ + BSD 3-Clause (Flask, Pandas)
├─ ✅ + MIT (Fiona, Requests)
├─ ✅ + Apache 2.0 (Requests)
├─ ✅ + ODbL (OSM data)
└─ ⚠️ + GPL v2 (FuzzyWuzzy)
    └─ OK for: SaaS/research
    └─ Problem for: Executable distribution

Overall Compatibility: ✅ GOOD (with note on GPL)
```

---

## License File Locations

### In Project Repository

```
Project Root:
├── LICENSE                          # MIT License text
├── CONTRIBUTING.md                  # License info for contributors
├── README.md                        # License badge + data attribution
└── LICENSING_GUIDE.md              # This comprehensive guide

In Code:
├── app.py                          # MIT license identifier
├── pyproject.toml                  # License field: "MIT"
└── scripts/                        # Each script can include header

In Data:
├── data/raw/                       # Contains ODbL + Government data
│   └── README.md (should have)     # Attribution comments
└── outputs/exports/                # Derived data (ODbL)
    └── README.md (should have)     # Attribution comments
```

### Data Attribution Headers

**Recommended in data files**:

```python
# scripts/02_extract_roads.py
"""
OSM Road Extraction Script

Data Source: OpenStreetMap
License: ODbL (Open Database License)
Attribution: © OpenStreetMap contributors

This script processes OSM data licensed under ODbL.
Outputs are also licensed under ODbL.
"""
```

---

## Summary Table: All Licenses Used

| # | License | Type | Applies To | Required | Compatible |
|---|---------|------|-----------|----------|-----------|
| 1 | **MIT** | Code | Our code | ✅ | ✅ |
| 2 | **ODbL** | Data | OSM + derived | ✅ | ✅ |
| 3 | **CC-BY** | Data | Gov statistics | ✅ | ✅ |
| 4 | **BSD 3-Clause** | Code | Flask, Pandas | ✅ | ✅ |
| 5 | **MIT** | Code | Fiona, Requests | ✅ | ✅ |
| 6 | **GPL v2** | Code | FuzzyWuzzy | ⚠️ | ⚠️* |
| 7 | **BSD 2-Clause** | Code | Leaflet.js | ✅ | ✅ |
| 8 | **Apache 2.0** | Code | Various | ✅ | ✅ |

**Total Licenses**: 8 distinct licenses

**Status**: 
- ✅ All compatible for current use (web app)
- ⚠️ GPL v2 note: Only for SaaS deployment

---

## License Breakdown by Category

### By Type

```
Open Source Licenses:        8 total
├─ Permissive               7 (MIT, BSD, Apache)
└─ Copyleft                 1 (GPL v2)

Data Licenses:              2 total
├─ ODbL (Share-alike)       1
└─ CC-BY (Attribution)      1

By Permissiveness:
├─ Very Permissive         6 (MIT, BSD, Apache)
├─ Permissive + Share-alike 2 (ODbL, CC-BY)
└─ Copyleft                1 (GPL v2)
```

### By Layer

```
Application Layer:          3 licenses
├─ MIT (our code)
├─ BSD 3-Clause (Flask)
└─ MIT (Requests)

Data Processing:            3 licenses
├─ BSD 3-Clause (GeoPandas, Pandas)
├─ MIT (Fiona, PyOGRIO)
└─ GPL v2 (FuzzyWuzzy) ⚠️

Visualization:              2 licenses
├─ MIT (Folium)
├─ BSD 2-Clause (Leaflet)

Data Layer:                 2 licenses
├─ ODbL (OSM)
└─ CC-BY (Government)
```

---

## Compliance Checklist

### ✅ Are We Compliant?

- [x] MIT license properly documented (LICENSE file)
- [x] Project metadata updated (pyproject.toml)
- [x] License badge in README
- [x] Data attribution documented
- [x] Dependencies listed (requirements.txt)
- [x] No GPL code in proprietary parts
- [x] SaaS deployment OK with GPL v2
- [ ] Data README with attribution (should add)
- [ ] License headers in scripts (optional but recommended)
- [ ] CONTRIBUTING.md updated with license info

### Actions to Complete

1. **Add attribution to data files**
   ```
   # At top of data processing scripts
   # OSM data is licensed under ODbL
   # Government data is licensed under CC-BY
   ```

2. **Create data/README.md**
   ```markdown
   # Data Attribution
   
   ## OSM Data
   © OpenStreetMap contributors - ODbL v1.0
   
   ## Government Statistics
   Latvian Central Statistical Bureau - CC-BY
   ```

3. **Add SPDX identifiers to scripts** (optional)
   ```python
   # SPDX-License-Identifier: MIT
   ```

---

## Key Numbers

```
License Statistics:
═══════════════════════════════════════════════════════════════

Total Licenses Used:              8
├─ Primary project license:       1 (MIT)
├─ Data licenses:                 2 (ODbL, CC-BY)
├─ Framework licenses:            3 (BSD, MIT, Apache)
└─ Frontend licenses:             2 (BSD, MIT)

By Count:
├─ Permissive:                    7 ✅
├─ Copyleft (simple):             2
├─ Copyleft (restrictive):        1 ⚠️
└─ Incompatible:                  0

Compatibility:
├─ Fully compatible:              7/8 ✅
├─ Compatible with notes:         1/8 ⚠️
└─ Not compatible:                0/8

For Web Application (SaaS):       8/8 ✅ (all OK)
For Executable Distribution:      7/8 ✅ (avoid GPL v2)
For Proprietary Derivative:       6/8 ⚠️ (GPL v2 issue)
```

---

## Recommended Actions

### Short Term ✅

1. Keep current MIT license for code
2. Continue using ODbL for OSM data
3. Document CC-BY for government data
4. Maintain all attributions in README

### Medium Term 📋

1. Add data attribution headers to scripts
2. Create data/README.md with clear attribution
3. Add SPDX identifiers to code files
4. Update CONTRIBUTING.md with license info

### Long Term 🔄

1. Monitor GPL v2 requirements if distribution planned
2. Consider replacing FuzzyWuzzy with RapidFuzz (MIT) for cleaner licensing
3. Add license compliance checker to CI/CD
4. Document any future dependency changes

---

## References

### License Documentation
- MIT: https://opensource.org/licenses/MIT
- ODbL: https://opendatacommons.org/licenses/odbl/
- CC-BY: https://creativecommons.org/licenses/by/
- GPL v2: https://www.gnu.org/licenses/gpl-2.0.html
- BSD: https://opensource.org/licenses/

### Our Files
- [LICENSE](../LICENSE) - Full MIT license text
- [README.md](../README.md) - License badge
- [pyproject.toml](../pyproject.toml) - License metadata
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contributor guidelines

---

## Summary

**LatviaOSM-Check uses 8 distinct open-source licenses:**

1. ✅ **MIT** - Our application code (permissive)
2. ✅ **ODbL** - OSM data (share-alike for data)
3. ✅ **CC-BY** - Government statistics (attribution)
4. ✅ **BSD 3-Clause** - Flask, GeoPandas, Pandas (permissive)
5. ✅ **MIT** - Fiona, PyOGRIO, Folium, Requests (permissive)
6. ⚠️ **GPL v2** - FuzzyWuzzy (copyleft, OK for SaaS)
7. ✅ **BSD 2-Clause** - Leaflet.js (permissive)
8. ✅ **Apache 2.0** - Various packages (permissive)

**Bottom Line**: All licenses are compatible for current use. The project is fully compliant for:
- ✅ Web application (SaaS) deployment
- ✅ Research and educational use
- ✅ Open-source development
- ⚠️ Executable distribution (handle GPL v2)

