# Changelog

All notable changes to LatviaOSM-Check will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Fuzzy name matching algorithm (80% threshold)
- Support for all 36 Latvian novads
- Advanced genitive case handling for Latvian names
- Corrected spatial join using proper administrative boundaries
- Interactive web map with Leaflet.js
- Flask RESTful API
- Color-coded completeness visualization

### Fixed
- Critical data integrity issue (6 novads showing 0.0 km)
- Language mismatch between GeoJSON and official statistics
- Wrong administrative division (587 parishes → 36 novads)
- Column header inconsistencies

### Technical Achievements
- 100% data matching accuracy (36/36 novads)
- 456,381 OSM road segments processed
- Zero NULL values in final dataset
- 203.9% overall completeness (OSM richer than official data)

