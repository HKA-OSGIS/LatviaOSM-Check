# Installation Guide

Complete installation instructions for LatviaOSM-Check on different platforms.

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 2 GB free space
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)

### Recommended Requirements
- **Python**: 3.11 or higher
- **RAM**: 16 GB
- **Disk Space**: 5 GB free space
- **CPU**: Multi-core processor for faster data processing

---

## Installation Methods

### Method 1: Quick Setup (Recommended)

#### Windows (PowerShell)

```powershell
# 1. Clone the repository
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project

# 2. Run automated setup
.\setup.ps1

# 3. Start the application
.\run.ps1
```

The setup script will:
- Create a Python virtual environment
- Install all required dependencies
- Verify the installation
- Display setup status

#### macOS/Linux (Bash)

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project

# 2. Make scripts executable
chmod +x scripts/*.sh
chmod +x setup.sh run.sh

# 3. Run automated setup
./setup.sh

# 4. Start the application
./run.sh
```

---

### Method 2: Manual Setup

#### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify installation:
   ```powershell
   python --version
   ```

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Verify
python3 --version
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project
```

Or download ZIP from GitHub and extract.

#### Step 3: Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5: Verify Installation

```bash
python -c "import geopandas; import flask; print('Installation successful!')"
```

---

### Method 3: Docker Installation

#### Prerequisites
- Docker Desktop installed
- 4 GB RAM allocated to Docker

#### Using Docker

```bash
# 1. Clone repository
git clone https://github.com/<your-org>/latvia_osm_project.git
cd latvia_osm_project

# 2. Build Docker image
docker build -t latvia-osm-check .

# 3. Run container
docker run -p 5000:5000 -v $(pwd)/data:/app/data latvia-osm-check

# 4. Open browser
open http://localhost:5000
```

#### Docker Compose

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down
```

---

## Dependency Installation Details

### Core Dependencies

```bash
# Web framework
pip install flask==2.3.3

# Geospatial libraries
pip install geopandas==0.13.2
pip install shapely==2.0.1
pip install fiona==1.9.4
pip install pyogrio==0.7.2

# Data processing
pip install pandas==2.0.3

# Visualization
pip install folium==0.14.0

# HTTP requests
pip install requests==2.31.0
```

### Optional Dependencies

```bash
# For development
pip install pytest pytest-cov black flake8 mypy

# For Jupyter notebooks
pip install jupyter ipykernel

# For additional formats
pip install openpyxl xlrd
```

---

## Data Setup

### Download Required Data

#### 1. OSM Data for Latvia

```bash
# Download Latvia OSM extract (~300 MB)
cd data/raw
wget https://download.geofabrik.de/europe/latvia-latest.osm.pbf
```

Or download manually from: https://download.geofabrik.de/europe/latvia.html

#### 2. Municipality Boundaries

The project includes municipality boundaries. If you need to update:

```bash
# Download from official source
# Place in data/raw/municipalities.geojson
```

#### 3. Official Statistics

Official statistics are included in `data/raw/`. If updating:
- `Road.csv` - Road statistics
- `Forest.csv` - Forest statistics  
- `Library.csv` - Library statistics

---

## Running the Pipeline

### Full Data Processing Pipeline

#### Roads Analysis

```powershell
# Windows
.\run_road_pipeline.ps1

# Linux/macOS
./scripts/run_pipeline.sh roads
```

This will:
1. Convert official statistics
2. Extract roads from OSM
3. Process municipality boundaries
4. Perform spatial join
5. Calculate completeness
6. Generate interactive maps

#### Forests Analysis

```powershell
# Windows
.\run_forest_pipeline.ps1

# Linux/macOS
./scripts/run_pipeline.sh forests
```

#### Libraries Analysis

```powershell
# Windows
.\run_library_pipeline.ps1

# Linux/macOS
./scripts/run_pipeline.sh libraries
```

### Individual Scripts

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\Activate.ps1  # Windows

# Run individual scripts
python scripts/02_extract_roads.py
python scripts/11_extract_forests.py
python scripts/21_extract_libraries.py
```

---

## Starting the Web Application

### Development Server

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\Activate.ps1  # Windows

# Start Flask application
python app.py
```

The application will be available at:
- Main app: http://localhost:5000
- API docs: http://localhost:5000/api

### Production Deployment

#### Using Gunicorn (Linux/macOS)

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Waitress (Windows)

```powershell
# Install waitress
pip install waitress

# Run server
waitress-serve --port=5000 app:app
```

---

## Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError: No module named 'geopandas'`

**Solution:**
```bash
pip install --upgrade pip
pip install geopandas
```

If still failing, install system dependencies:

**Linux (Ubuntu):**
```bash
sudo apt install gdal-bin libgdal-dev
pip install GDAL==$(gdal-config --version)
```

**macOS:**
```bash
brew install gdal
pip install GDAL==$(gdal-config --version)
```

---

#### Issue: `fiona._env.DriverError`

**Solution:**
```bash
pip uninstall fiona
pip install --no-binary fiona fiona
```

---

#### Issue: Virtual environment activation fails

**Windows PowerShell:**
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Then retry:**
```powershell
.\venv\Scripts\Activate.ps1
```

---

#### Issue: Permission denied on Linux/macOS

**Solution:**
```bash
chmod +x setup.sh
chmod +x run.sh
chmod +x scripts/*.sh
```

---

#### Issue: Out of memory during processing

**Solution:**
1. Increase available RAM
2. Process data in chunks:
   ```python
   # In scripts, use chunksize parameter
   for chunk in pd.read_csv('large_file.csv', chunksize=10000):
       process(chunk)
   ```

---

#### Issue: Port 5000 already in use

**Solution:**
```bash
# Use different port
export FLASK_RUN_PORT=8080
python app.py
```

Or find and stop the conflicting process:

**Windows:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

**Linux/macOS:**
```bash
lsof -i :5000
kill -9 <process_id>
```

---

## Verifying Installation

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage report
pytest --cov=src tests/
```

### Check Data Pipeline

```bash
# Quick verification
python -c "
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Check data files exist
data_dir = Path('data/raw')
assert (data_dir / 'municipalities.geojson').exists()
assert (data_dir / 'Road.csv').exists()
assert (data_dir / 'Forest.csv').exists()
assert (data_dir / 'Library.csv').exists()

print('✓ All data files present')

# Check processed outputs
outputs_dir = Path('outputs/exports')
if outputs_dir.exists():
    print(f'✓ Found {len(list(outputs_dir.glob(\"*.geojson\")))} GeoJSON outputs')
    print(f'✓ Found {len(list(outputs_dir.glob(\"*.csv\")))} CSV outputs')
else:
    print('⚠ No outputs yet - run the pipeline')
"
```

---

## Updating

### Update Code

```bash
git pull origin main
```

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Update Data

Re-run the data pipeline:
```bash
.\run_forest_pipeline.ps1  # Windows
./scripts/run_pipeline.sh  # Linux/macOS
```

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove virtual environment
rm -rf venv/  # Linux/macOS
Remove-Item -Recurse -Force venv/  # Windows
```

### Remove Project

```bash
cd ..
rm -rf latvia_osm_project/  # Linux/macOS
Remove-Item -Recurse -Force latvia_osm_project/  # Windows
```

---

## Next Steps

After successful installation:

1. **Read the Quick Guide**: [QUICK_GUIDE.md](QUICK_GUIDE.md)
2. **Explore the API**: [API.md](API.md)
3. **Run the pipeline**: Process your first dataset
4. **Start the web app**: View interactive maps
5. **Contribute**: See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Getting Help

- **Documentation**: Check all docs in the `docs/` folder
- **Issues**: Report bugs on [GitHub Issues](https://github.com/<your-org>/latvia_osm_project/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/<your-org>/latvia_osm_project/discussions)
- **Email**: Contact maintainers (see [CONTRIBUTING.md](../CONTRIBUTING.md))
