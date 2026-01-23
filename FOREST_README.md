# 🌲 Forest Analysis - Ready to Run!

## What's Been Set Up

I've created a complete forest analysis pipeline for your Latvia OSM project, similar to the roads analysis. Here's what you have:

### ✅ Completed
1. **Official Statistics Processing** - Your Forest.csv has been converted
2. **Pipeline Scripts** - 4 new scripts ready to run
3. **Flask Integration** - Web app updated with forest map support
4. **Documentation** - Complete guides created

## Quick Start

### Run Everything at Once (Recommended)
```powershell
.\run_forest_pipeline.ps1
```
**Time**: 15-20 minutes total

### OR Run Step by Step
```powershell
# Step 1: Convert stats (DONE ✅)
python scripts/10_convert_forest_stats.py

# Step 2: Extract forests from OSM (10-15 min)
python scripts/11_extract_forests.py

# Step 3: Calculate completeness (2-5 min)
python scripts/12_calculate_forest_completeness.py

# Step 4: Create map (1 min)
python scripts/13_create_forest_map.py

# Step 5: View results
python app.py
# Visit: http://localhost:5000/forest-map
```

## What You'll Get

### 1. Forest Completeness Data
**File**: `outputs/exports/completeness_forests.csv`

Contains for each municipality:
- OSM forest area (km², ha)
- Official forest area (km², ha)
- Completeness percentage
- Number of forest areas
- Category (Low/Partial/Complete/Over-mapped)

### 2. Interactive Map
**File**: `outputs/maps/forest_completeness_map.html`
**URL**: http://localhost:5000/forest-map

Features:
- Color-coded by completeness (Green ≥90%, Yellow 50-70%, Red <30%)
- Click any municipality for detailed statistics
- Shows all 36 municipalities + 10 cities

### 3. API Access
```bash
# Get forest data
curl http://localhost:5000/api/forest-data

# Compare with roads
curl http://localhost:5000/api/csv-data
```

## Coverage

### Municipalities (36)
All administrative regions including:
- Ventspils novads (1,803 km² official forest)
- Talsu novads (1,779 km²)
- Dienvidkurzemes novads (1,776 km²)
- And 33 more...

### Cities (10)
- Rīga (55.77 km²)
- Jūrmala (48.11 km²)
- Daugavpils (15.91 km²)
- And 7 more...

## Expected Results

Unlike roads (which are over-mapped at 200%+), forests typically show:

- **30-70% completeness** - Forests are harder to map
- **Urban areas** - May have better coverage
- **Rural areas** - Larger forest blocks, easier to identify

### Why Lower Completeness?
1. Forest boundaries need aerial imagery
2. Smaller forest patches often not mapped
3. Private forests vs public forests
4. Seasonal changes make mapping harder

## Scripts Created

| Script | Purpose | Duration |
|--------|---------|----------|
| `10_convert_forest_stats.py` | Parse official data | 1 sec ✅ |
| `11_extract_forests.py` | Extract from OSM | 10-15 min |
| `12_calculate_forest_completeness.py` | Calculate metrics | 2-5 min |
| `13_create_forest_map.py` | Generate map | 1 min |
| `14_combined_analysis.py` | Compare roads+forests | 1 sec |

## Files Structure

```
latvia_osm_project/
├── data/
│   ├── raw/
│   │   ├── Forest.csv                  # Your uploaded file
│   │   └── official_forest_stats.csv   # ✅ Processed
│   └── processed/
│       └── forests.geojson             # ⏳ Will be created
│
├── outputs/
│   ├── exports/
│   │   ├── completeness_forests.csv    # ⏳ Final data
│   │   └── combined_roads_forests.csv  # ⏳ Comparison
│   └── maps/
│       └── forest_completeness_map.html # ⏳ Interactive map
│
├── scripts/
│   ├── 10_convert_forest_stats.py      # ✅ Done
│   ├── 11_extract_forests.py           # Ready
│   ├── 12_calculate_forest_completeness.py  # Ready
│   ├── 13_create_forest_map.py         # Ready
│   └── 14_combined_analysis.py         # Bonus!
│
├── docs/
│   └── FOREST_ANALYSIS_GUIDE.md        # Complete guide
│
├── run_forest_pipeline.ps1             # Run all steps
├── FOREST_IMPLEMENTATION.md            # This file
└── app.py                              # ✅ Updated with forest support
```

## Bonus: Combined Analysis

After running both pipelines, compare them:
```powershell
python scripts/14_combined_analysis.py
```

This creates:
- Side-by-side comparison
- Insights: "High roads, low forests"
- Combined CSV for further analysis

## Next Steps

1. **Run the pipeline**:
   ```powershell
   .\run_forest_pipeline.ps1
   ```

2. **Start Flask app**:
   ```powershell
   python app.py
   ```

3. **View maps**:
   - Roads: http://localhost:5000/lau1-map
   - Forests: http://localhost:5000/forest-map

4. **Run comparison**:
   ```powershell
   python scripts/14_combined_analysis.py
   ```

## Documentation

- **Quick Guide**: `docs/FOREST_ANALYSIS_GUIDE.md`
- **Implementation**: `FOREST_IMPLEMENTATION.md`
- **Main README**: `README.md` (should be updated)

## Troubleshooting

### "OSM file not found"
Ensure `data/raw/latvia-latest.osm.pbf` exists. This is the same file used for roads.

### "Municipalities not found"
Run: `python scripts/03_process_municipalities.py`

### "Out of memory"
The forest extraction is memory-intensive. Close other applications.

## What Makes This Different from Roads?

| Aspect | Roads | Forests |
|--------|-------|---------|
| **Data type** | Lines (LineString) | Areas (Polygons) |
| **Metric** | Length (km) | Area (km², ha) |
| **OSM tags** | highway=* | landuse=forest, natural=wood |
| **Completeness** | 200%+ (over) | 30-70% (under) |
| **Mapping difficulty** | Easy | Hard (needs imagery) |

## Ready to Go!

Everything is set up. Just run:
```powershell
.\run_forest_pipeline.ps1
```

Then visit:
- http://localhost:5000/forest-map

Enjoy exploring Latvia's forest coverage! 🌲🗺️
