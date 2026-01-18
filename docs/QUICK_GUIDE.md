# Multi-Select Comparison Tool - Quick Guide

## What's New?

The tool has been updated with a powerful multi-select interface for comparing municipalities across Latvia.

## Key Features

### 1. **Multi-Select Checkboxes**
- Each municipality has a checkbox
- Click individual checkboxes to select/deselect
- **"Select All"** button - Choose all ~589 municipalities
- **"Clear All"** button - Deselect all municipalities
- **Default**: All municipalities are selected on page load

### 2. **Default Behavior**
- When you open http://localhost:5000, Latvia is pre-selected
- All municipalities are automatically checked
- The map displays all municipalities
- The comparison table shows all data

### 3. **Real-Time Statistics Dashboard**
```
Selected: 589           (count of checked municipalities)
Total Roads (OSM): 12,345.67 km   (sum of all selected)
Total Segments: 98,765    (sum of all segments)
Avg Completeness: 42.3%   (average of non-null values)
```

### 4. **Comparison Table**
Shows data for each selected municipality:
| Municipality | OSM Roads | Segments | Completeness |
|---|---|---|---|
| Rīga | 1,234.56 km | 5,678 | 78.5% |
| Jūrmala | 123.45 km | 567 | 65.3% |
| Daugavpils | 234.56 km | 890 | 52.1% |
| ... | ... | ... | ... |

### 5. **Interactive Map**
- Shows all selected municipalities highlighted in blue
- Map automatically fits to show all selected areas
- Updates instantly when you change selections
- Zoom and pan to explore details

## How to Use

### View All Municipalities (Default)
1. Open: http://localhost:5000
2. All municipalities are pre-selected
3. Map shows entire Latvia
4. Statistics show national totals

### Compare Specific Regions
1. Click "Clear All" to deselect everything
2. Select municipalities you want to compare by checking their boxes
3. Watch the map update in real-time
4. Review comparison statistics and table

### Quick Selection Options
- **Select All**: Check all municipalities at once
- **Clear All**: Uncheck all municipalities
- **Individual**: Click checkbox for each municipality

### Analyze Comparisons
- **View Top Municipalities**: Sort table by completeness
- **See Patterns**: Compare neighboring municipalities
- **Track Aggregates**: Monitor totals as you select/deselect

## API Endpoints for Developers

### Get All Data at Once
```bash
# Get all GeoJSON features
curl http://localhost:5000/api/geojson-data

# Get all statistics
curl http://localhost:5000/api/csv-data
```

### Programmatic Usage
```javascript
// Load all data
const geoData = await fetch('/api/geojson-data').then(r => r.json());
const csvData = await fetch('/api/csv-data').then(r => r.json());

// Build lookup
const stats = {};
csvData.forEach(row => stats[row.municipality_name] = row);

// Filter for specific municipalities
const selected = ['Rīga', 'Jūrmala'];
const features = geoData.features.filter(f => 
  selected.includes(f.properties.municipality_name)
);

// Calculate aggregates
const total = selected.reduce((sum, muni) => 
  sum + (stats[muni]?.osm_road_km || 0), 0);
```

## Performance Tips

- **Better Performance**: Select fewer municipalities to reduce map complexity
- **Fast Selections**: Use "Select All" / "Clear All" buttons for bulk operations
- **Smooth Updates**: All filtering happens in your browser (no server requests)

## Example Workflows

### Workflow 1: Compare Capital vs Other Cities
1. Click "Clear All"
2. Select: Rīga, Jūrmala, Daugavpils, Liepāja
3. View comparison statistics
4. Analyze road completeness patterns

### Workflow 2: Regional Analysis
1. Click "Clear All"
2. Select all municipalities in one region (e.g., Vidzeme region)
3. Compare with national average shown in stats
4. Export comparison data

### Workflow 3: Data Validation
1. Keep "Select All" checked
2. Review national statistics:
   - Total road kilometers
   - Average completeness
   - Segment counts
3. Spot-check individual municipalities for accuracy

## Troubleshooting

| Issue | Solution |
|---|---|
| Checkboxes not visible | Scroll left sidebar down |
| Map not updating | Check browser console for errors |
| No data showing | Verify GeoJSON and CSV files exist |
| Slow performance | Reduce selected municipalities |

## Next Steps

Future versions might add:
- **Filters**: By completeness category, road type, etc.
- **Export**: Download comparison as CSV or GeoJSON
- **Historical**: Compare data across different time periods
- **Regional**: Pre-grouped selections by administrative regions
