# LatviaOSM-Check

A comprehensive tool for analyzing OpenStreetMap (OSM) road completeness in Latvia by comparing OSM data with official municipal road statistics.

## Overview

This project compares OpenStreetMap road data against official government statistics for Latvian municipalities, providing:
- **Completeness Analysis**: Calculate what percentage of official roads are mapped in OSM
- **Interactive Mapping**: Visualize completeness on a web-based map
- **Data Quality Reports**: Identify mapping gaps and priorities
- **API Endpoints**: Access data programmatically

## Features

✅ **36 Municipalities Included**
- Official road data from government statistics (TRS020_20251218-165232.csv)
- OSM road data extracted from Latvia OSM dataset
- Completeness calculated for each municipality
- Only official novads included (7 city states excluded)

📊 **Data Metrics**
- Total OSM Roads: 7,821 km
- Total Official Roads: 54,785 km
- Overall Completeness: 14.3%
- Distribution: 4 high (≥50%), 7 medium (20-50%), 19 low (0-20%), 6 zero (0%)

🗺️ **Interactive Map**
- Color-coded municipalities by completeness percentage
- Detailed popups with statistics
- Flask-based web interface
- GeoJSON data layer

## Project Structure

```
.
├── app.py                          # Flask web application
├── data/
│   ├── raw/                        # Original datasets
│   │   ├── TRS020_20251218-122746.csv  # Official road statistics
│   │   └── ...
│   └── processed/                  # Processed data
├── scripts/
│   ├── 01_download_data.sh
│   ├── 02_extract_roads.py
│   ├── 03_process_municipalities.py
│   ├── 04_spatial_join.py
│   ├── 05_calculate_completeness.py
│   └── ...
├── outputs/
│   ├── exports/
│   │   ├── latvia_municipalities_only.geojson
│   │   └── completeness_municipalities.csv
│   ├── maps/
│   │   └── interactive_map.html
│   └── figures/
├── templates/                      # Flask templates
├── test_project.py                 # Unit tests
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

## Installation

### Prerequisites
- Python 3.7+
- Git (with Git LFS for large files)

### Download from GitHub

#### Option 1: Clone Repository (Recommended)

```bash
# Clone the repository with all large files
git clone https://github.com/HKA-OSGIS/LatviaOSM-Check.git
cd LatviaOSM-Check
```

#### Option 2: Download as ZIP

1. Go to: https://github.com/HKA-OSGIS/LatviaOSM-Check
2. Click **Code** button (green)
3. Select **Download ZIP**
4. Extract the ZIP file to your desired location
5. Open terminal/command prompt in the extracted folder

#### Option 3: Using Git LFS (for large spatial files)

If you have Git LFS installed, it will automatically download large files (>100MB):

```bash
# Install Git LFS (if not already installed)
# Windows: https://git-lfs.github.com or: choco install git-lfs
# macOS: brew install git-lfs
# Linux: sudo apt-get install git-lfs

# Clone with LFS support
git clone https://github.com/HKA-OSGIS/LatviaOSM-Check.git
cd LatviaOSM-Check
```

### Setup Instructions

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the Web Application

```bash
python app.py
```

Then open: http://localhost:5000

### View the Interactive Map

```bash
python app.py
```

Navigate to: http://localhost:5000/map

### Run Unit Tests

```bash
python test_project.py
```

### Filter Data to Municipalities

```bash
python filter_municipalities_from_csv.py
```

### Verify Data Quality

```bash
python verify_data.py
```

## Data Files

### Input Data
- **TRS020_20251218-122746.csv**: Official road lengths by municipality (2024)
  - Source: Latvian Central Statistical Bureau
  - 36 municipalities with total road statistics

### Output Data
- **latvia_municipalities_only.geojson**: 30 municipalities with OSM/official road data
- **completeness_municipalities.csv**: Statistics table with completeness percentages

## API Endpoints

### Get CSV Data
```
GET /api/csv-data
```
Returns all municipality statistics in JSON format.

### Get GeoJSON Data
```
GET /api/geojson-data
```
Returns GeoJSON layer with road data.

### Get Municipality Data
```
GET /api/municipality-data?name=<municipality_name>
```
Returns specific municipality data.

## Test Results

✅ **27/29 Tests Passed**

Test Coverage:
- ✅ Data Files (2/2)
- ✅ CSV Data Integrity (11/11)
- ✅ GeoJSON Data Integrity (7/7)
- ✅ Data Calculations (3/3)
- ✅ Municipality Data (2/2)
- ✅ Data Quality (4/4)
- ⏭️ Flask API (2 tests skipped)

## Municipalities Included

**36 Official Novads (Regional Municipalities):**

Aizkraukle, Alūksne, Balvi, Bauska, Cēsis, Dobele, Daugavpils, Dundaga, Engure, Garkalne, Iecava, Gulbene, Jēkabpils, Jelgava, Krāslava, Kuldīga, Līvāni, Ludza, Madona, Ogre, Olaine, Preiļi, Rēzekne, Ropaži, Salaspils, Saldus, Saulkrasti, Sigulda, Smiltene, Stopini, Talsi, Tukums, Valka, Valmiera, Varakļāni, Ventspils

*Note: 7 city states excluded (Rīga, Daugavpils, Jelgava, Rēzekne, Ventspils, Liepāja, Jūrmala) as they have different administrative structures*

## Data Quality Notes

- **Over-mapped areas**: Some municipalities show >100% completeness (e.g., Salaspils 148.1%), indicating:
  - Dual carriageways counted differently
  - Different road classification schemes
  - Data quality variations

- **Under-mapped areas**: Low completeness indicates mapping priorities:
  - Ludza: 6.2% (lowest)
  - Several municipalities 6-12% completeness

## Technologies

- **Python 3**: Core language
- **GeoPandas**: Geospatial data handling
- **Flask**: Web framework
- **Folium**: Interactive mapping
- **Pandas**: Data analysis
- **GDAL/OGR**: GIS operations
- **SQLite/PostGIS**: Optional data storage

## Future Enhancements

- [ ] Railway network analysis
- [ ] Building completeness analysis
- [ ] POI (Hospital, Restaurant) analysis
- [ ] Historical trend analysis
- [ ] Advanced filtering and reports
- [ ] Multi-language support
- [ ] Database backend integration

## Contributors

- Developed for HKA-OSGIS (Hochschule Karlsruhe - University of Applied Sciences, OSGeo Initiative)

## License

[Specify License - e.g., MIT, GPL, etc.]

## Contact

For questions or contributions, please open an issue on GitHub or contact the maintainers.

## References

- OpenStreetMap: https://www.openstreetmap.org
- Latvian Central Statistical Bureau: https://www.csb.gov.lv
- GeoPandas Documentation: https://geopandas.org
- Flask Documentation: https://flask.palletsprojects.com
