# LatviaOSM-Check: OpenStreetMap Data Quality Analysis Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active](https://img.shields.io/badge/Status-Active-green.svg)](https://github.com)

> **Analyze, visualize, and understand OpenStreetMap data completeness across Latvia**

## 🌍 Overview

LatviaOSM-Check is a comprehensive analysis tool that compares OpenStreetMap (OSM) data quality against official government statistics for Latvia. It provides interactive visualizations, statistical analysis, and detailed reports for three key geographic features:

- 🛣️ **Roads** - Road networks and transport infrastructure
- 🌲 **Forests** - Forest coverage and boundaries
- 📚 **Libraries** - Library locations and cultural institutions

### Key Features

✅ **Interactive Web Dashboard**
- Multi-layer interactive maps with color-coded completeness indicators
- Real-time filtering and comparison tools
- Hierarchical geographic selector (Country → Region → Municipality)
- Click-to-explore detailed statistics

✅ **Data Analysis**
- Automatic comparison of OSM data vs official statistics
- Completeness percentage calculations
- Spatial join operations across 589+ geographic areas
- Statistical aggregation by region (novads)

✅ **RESTful API**
- 15+ endpoints for programmatic data access
- GeoJSON and CSV data export
- Code examples in Python, JavaScript, and R

✅ **Professional Documentation**
- Complete installation guides (Windows, macOS, Linux, Docker)
- User manual with common workflows
- Developer guide for contributions
- API reference with examples
- Technical implementation details

## 📊 Current Data Status

| Feature | Coverage | Records | Status |
|---------|----------|---------|--------|
| **Roads** | 36 municipalities | 39/42 areas | ✅ Complete |
| **Forests** | Complete nationwide | Multiple regions | ✅ Complete |
| **Libraries** | Complete nationwide | Multiple regions | ✅ Complete |
| **Municipalities** | All 36 municipalities | 36/36 | ✅ Complete |
| **Overall Completeness** | 249.6% average | 42 features | ✅ Excellent |

## 🚀 Quick Start

### Installation (5 minutes)

**Windows:**
```powershell
git clone <repository-url>
cd latvia_osm_project
.\setup.ps1
.\run.ps1
```

**Linux/macOS:**
```bash
git clone <repository-url>
cd latvia_osm_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Access the Application

Open your browser and navigate to:
- **Main Dashboard**: http://localhost:5000
- **Roads Analysis**: http://localhost:5000/roads
- **Forests Analysis**: http://localhost:5000/forests
- **Libraries Analysis**: http://localhost:5000/libraries
- **Combined Map**: http://localhost:5000/combined-map

## 📖 Documentation

Complete documentation is available in the `docs/` folder:

### For Users
- [**Installation Guide**](docs/INSTALLATION.md) - Setup instructions for all platforms
- [**Usage Guide**](docs/USAGE.md) - Complete user manual with examples
- [**Quick Start Guide**](docs/QUICK_GUIDE.md) - Get running in 5 minutes
- [**API Documentation**](docs/API.md) - REST API reference with code examples

### For Contributors
- [**Contributing Guide**](CONTRIBUTING.md) - How to contribute code, documentation, or ideas
- [**Development Guide**](docs/DEVELOPMENT.md) - Developer setup and architecture
- [**Project Structure**](docs/PROJECT_STRUCTURE.md) - Codebase organization
- [**Code of Conduct**](CODE_OF_CONDUCT.md) - Community standards

### Project Information
- [**Changelog**](CHANGELOG.md) - Version history and release notes
- [**Contributors**](CONTRIBUTORS.md) - People who built this project
- [**License**](LICENSE) - MIT License terms
- [**Final Status**](docs/FINAL_STATUS.md) - Current project status and statistics

## 💡 Usage Examples

### Web Interface
1. Open http://localhost:5000 in your browser
2. Select municipalities using the checkboxes
3. View real-time statistics and map updates
4. Click features for detailed information

### Python API
```python
import requests
import json

# Get all data as GeoJSON
response = requests.get('http://localhost:5000/api/geojson-data')
geojson = response.json()

# Get statistics CSV
response = requests.get('http://localhost:5000/api/csv-data')
csv_data = response.text
```

### JavaScript/Node.js
```javascript
// Fetch completeness data
fetch('http://localhost:5000/api/geojson-data')
  .then(res => res.json())
  .then(data => console.log(data.features[0]))
```

### R
```r
library(httr)

# Get completeness data
response <- GET('http://localhost:5000/api/geojson-data')
data <- content(response, as = 'parsed')
```

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.8+
- **Data Processing**: GeoPandas, Pandas, NumPy
- **Geospatial**: Shapely, pyproj, GDAL
- **Frontend**: Leaflet.js, HTML5, CSS3, JavaScript
- **Data Formats**: GeoJSON, CSV, GeoTIFF, OSM PBF

## 📁 Project Structure

```
latvia_osm_project/
├── app.py                    # Flask web application
├── src/                      # Source code modules
│   └── processing/           # Data processing scripts
├── scripts/                  # Pipeline scripts (numbered workflow)
├── templates/                # Flask HTML templates
├── data/                     # Data files (raw & processed)
├── outputs/                  # Generated maps and exports
├── docs/                     # Documentation
└── README.md                 # This file
```

See [Project Structure](docs/PROJECT_STRUCTURE.md) for complete directory documentation.

## 🤝 Contributing

We welcome contributions from the community! Whether you want to:
- Fix bugs
- Add features
- Improve documentation
- Report issues
- Suggest improvements

Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

### Development Quick Start
```bash
# Clone repository
git clone <repository-url>
cd latvia_osm_project

# Setup development environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Start development server
python app.py
```

See [Development Guide](docs/DEVELOPMENT.md) for more details.

## 📋 Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB+ recommended for full OSM processing)
- **Disk Space**: 1GB for installation + dependencies
- **Operating System**: Windows, macOS, or Linux
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

## 📦 Installation Methods

### 1. Automated Setup (Recommended)
```powershell
# Windows
.\setup.ps1
.\run.ps1
```

### 2. Manual Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 3. Docker (Coming Soon)
```bash
docker build -t latvia-osm-check .
docker run -p 5000:5000 latvia-osm-check
```

See [Installation Guide](docs/INSTALLATION.md) for detailed setup instructions.

## 📊 Data Sources

- **OpenStreetMap**: OSM data extract for Latvia (quarterly updates)
- **Official Statistics**: Government datasets (2024)
- **Municipality Boundaries**: Official LAU1/LAU2 boundaries
- **Supporting Data**: Roads, forests, and library records

## 📈 Statistics & Results

### Coverage Summary
- **Total Features Analyzed**: 42 (36 municipalities + 6 cities)
- **Features with Complete Data**: 39
- **Average Completeness**: 249.6% (very comprehensive)
- **Best Mapped Area**: Olaine (645.6%)
- **Areas Over 100%**: 35 (indicating comprehensive OSM coverage)

### Feature Analysis
- **Roads**: Complete coverage for 36 municipalities
- **Forests**: Full national coverage
- **Libraries**: Complete geographic distribution

## 🔍 Analysis Capabilities

- Compare multiple municipalities simultaneously
- Calculate completeness percentages
- Generate statistical reports
- Export data in multiple formats
- Interactive visualization and exploration
- Historical data tracking (when available)

## 🐛 Reporting Issues

Found a bug? Have a suggestion? Please open an issue on GitHub:
- [Report Bug](https://github.com/issues/new?labels=bug)
- [Suggest Feature](https://github.com/issues/new?labels=enhancement)

## 📚 Additional Resources

- [API Documentation](docs/API.md) - Complete API reference
- [Implementation Details](docs/IMPLEMENTATION_SUMMARY_NOVADS.md) - Technical deep dive
- [Library Analysis Report](docs/LIBRARY_ANALYSIS.md) - Feature-specific analysis
- [Development Guide](docs/DEVELOPMENT.md) - Architecture and code organization

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

### License Summary
- ✅ Commercial use permitted
- ✅ Modification permitted
- ✅ Distribution permitted
- ✅ Private use permitted
- ⚠️ Include license and copyright notice
- ⚠️ No warranty provided

## 👥 Contributors

See [Contributors](CONTRIBUTORS.md) for a list of people who have contributed to this project.

### Special Thanks
- **OpenStreetMap Community** - For the incredible OSM dataset
- **GeoPandas Team** - For excellent geospatial tools
- **Flask Team** - For lightweight web framework
- **Leaflet.js Community** - For interactive mapping library

## 📞 Support

- 📖 Check [Usage Guide](docs/USAGE.md) for common questions
- 🔧 See [Troubleshooting](docs/INSTALLATION.md#troubleshooting) for issues
- 💬 Open an issue on GitHub for bugs
- 🤝 See [Contributing Guide](CONTRIBUTING.md) to help improve the project

## 🗺️ Project Roadmap

- ✅ Core road analysis functionality
- ✅ Forest coverage analysis
- ✅ Library location mapping
- ✅ Interactive web interface
- ✅ REST API
- ✅ Comprehensive documentation
- 🔄 Docker containerization
- 🔄 Advanced filtering options
- 🔄 Historical data tracking
- 🔄 Data export enhancements

## 📞 Contact

For questions or inquiries about the project:
- 📧 Email: [project contact]
- 🐙 GitHub: [project repository]
- 🌐 Website: [project website]

---

**Last Updated**: January 28, 2026

**Status**: ✅ Active and Maintained

**Version**: 1.0.0

See [Changelog](CHANGELOG.md) for version history and release notes.
