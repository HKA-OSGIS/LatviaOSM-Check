# Changelog

All notable changes to LatviaOSM-Check will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Automated data update pipeline
- Historical trend analysis
- Comparison with neighboring countries
- Mobile-responsive interface improvements
- Docker deployment support

## [2.1.1] - 2026-01-24

### Enhanced
- **Combined Map Update**
  - Added Library layer to combined map visualization
  - Libraries now default as primary view in combined map
  - Toggle between Roads, Forests, and Libraries layers
  - Improved map title and descriptions
  - Dynamic legend updates for each layer

## [2.1.0] - 2026-01-24

### Added
- **Comprehensive Documentation Suite**
  - [Installation Guide](docs/INSTALLATION.md) - Multi-platform setup instructions
  - [Usage Guide](docs/USAGE.md) - Complete user manual with examples
  - [API Documentation](docs/API.md) - Full REST API reference
  - [Development Guide](docs/DEVELOPMENT.md) - Developer handbook
- **Forest Analysis Module**
  - Forest feature extraction from OSM
  - Comparison with official forest statistics
  - Forest completeness visualization
  - Forest-specific API endpoints
- **Library Analysis Module**
  - Public library mapping analysis (712 libraries tracked)
  - Municipality-level library statistics
  - Library completeness metrics
  - Library-specific API endpoints
- **Combined Visualization**
  - Multi-layer map showing roads and forests together
  - Hierarchical geographic selector
  - Toggle between feature types
- **Enhanced API**
  - `/api/forest-data` - Forest statistics endpoint
  - `/api/library-data` - Library statistics endpoint
  - `/api/hierarchy` - Geographic hierarchy structure
  - `/api/statistics` - Aggregate statistics with filtering
- **Pipeline Scripts**
  - `run_forest_pipeline.ps1` - Automated forest analysis
  - `run_library_pipeline.ps1` - Automated library analysis
  - Individual extraction scripts for each feature type

### Changed
- Updated README with links to new documentation
- Enhanced project structure documentation
- Improved API response formats
- Extended GeoJSON properties with additional metadata

### Fixed
- Cache directory cleanup (__pycache__ removal)
- Debug script cleanup
- Improved error handling in API endpoints

## [2.0.0] - 2026-01-18

### Added
- Professional project structure with organized directories
- `src/processing/` directory for data processing scripts
- `docs/` directory for documentation
- `static/` directory for static assets
- Automated setup script (`setup.ps1`)
- Automated run script (`run.ps1`)
- Comprehensive CONTRIBUTING.md guide
- Professional README with badges and full documentation
- CHANGELOG.md for version tracking

### Changed
- Reorganized project structure to follow best practices
- Moved processing scripts from root to `src/processing/`
- Moved documentation to `docs/` folder
- Updated README with complete API documentation
- Improved project navigation and discoverability

### Removed
- Cleaned up 47+ obsolete/temporary files
- Removed redundant documentation files
- Removed diagnostic scripts (analyze_name_mismatch.py, diagnose_join.py, etc.)
- Removed obsolete processing scripts (duplicate/test versions)
- Removed category-specific completeness files
- Removed test templates
- Removed empty output directories

## [1.0.0] - 2025-12-18

### Added
- Initial release
- Fuzzy name matching algorithm (80% threshold)
- Support for all 36 Latvian novads
- Advanced genitive case handling for Latvian names
- Corrected spatial join using proper administrative boundaries
- Interactive web map with Leaflet.js
- Flask RESTful API
- Color-coded completeness visualization
- Road completeness analysis
- Municipality boundary processing

### Fixed
- Critical data integrity issue (6 novads showing 0.0 km)
- Language mismatch between GeoJSON and official statistics
- CRS projection inconsistencies
- Geometry validation errors
- Wrong administrative division (587 parishes → 36 novads)
- Column header inconsistencies

### Technical Achievements
- 100% data matching accuracy (36/36 novads)
- 456,381 OSM road segments processed
- Zero NULL values in final dataset
- 203.9% overall completeness (OSM richer than official data)

