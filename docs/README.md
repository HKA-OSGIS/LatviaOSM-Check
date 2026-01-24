# Documentation Index

Welcome to the LatviaOSM-Check documentation. This index will help you find the right documentation for your needs.

## 📚 Documentation Overview

### For Users

| Document | Description | When to Use |
|----------|-------------|-------------|
| [README](../README.md) | Project overview and quick start | First time learning about the project |
| [Installation Guide](INSTALLATION.md) | Detailed setup instructions | Setting up the project on your machine |
| [Quick Start Guide](QUICK_GUIDE.md) | Fast track to get running | When you want to start quickly |
| [Usage Guide](USAGE.md) | Complete user manual | Learning how to use all features |
| [API Documentation](API.md) | REST API reference | Integrating with the API programmatically |

### For Contributors

| Document | Description | When to Use |
|----------|-------------|-------------|
| [Contributing Guidelines](../CONTRIBUTING.md) | How to contribute | Before making your first contribution |
| [Development Guide](DEVELOPMENT.md) | Developer handbook | Writing code or adding features |
| [Project Structure](PROJECT_STRUCTURE.md) | Code organization | Understanding the codebase |
| [Code of Conduct](CODE_OF_CONDUCT.md) | Community guidelines | Participating in the community |

### Project Information

| Document | Description | When to Use |
|----------|-------------|-------------|
| [Changelog](../CHANGELOG.md) | Version history | Checking what's new or changed |
| [License](../LICENSE) | MIT License terms | Understanding usage rights |
| [Contributors](../CONTRIBUTORS.md) | Project contributors | Seeing who built this |
| [Final Status](FINAL_STATUS.md) | Current project status | Checking data coverage |

### Technical Documentation

| Document | Description | When to Use |
|----------|-------------|-------------|
| [Implementation Summary](IMPLEMENTATION_SUMMARY_NOVADS.md) | Technical implementation details | Deep dive into the technology |
| [Library Analysis](LIBRARY_ANALYSIS.md) | Library feature analysis | Understanding library data processing |

---

## 🚀 Getting Started Paths

### Path 1: "I want to use the tool"
1. Read [README](../README.md) - Understand what the project does
2. Follow [Installation Guide](INSTALLATION.md) - Set up the environment
3. Use [Quick Start Guide](QUICK_GUIDE.md) - Get running in 5 minutes
4. Refer to [Usage Guide](USAGE.md) - Learn all features

### Path 2: "I want to access the data programmatically"
1. Read [README](../README.md) - Project overview
2. Follow [Installation Guide](INSTALLATION.md) - Set up the server
3. Study [API Documentation](API.md) - Learn the API endpoints
4. Check [Usage Guide](USAGE.md) - See Python/JavaScript examples

### Path 3: "I want to contribute code"
1. Read [README](../README.md) - Understand the project
2. Review [Contributing Guidelines](../CONTRIBUTING.md) - Learn the process
3. Study [Development Guide](DEVELOPMENT.md) - Set up dev environment
4. Examine [Project Structure](PROJECT_STRUCTURE.md) - Understand the codebase
5. Check [Changelog](../CHANGELOG.md) - See recent changes

### Path 4: "I want to understand the methodology"
1. Read [README](../README.md) - Overview
2. Study [Implementation Summary](IMPLEMENTATION_SUMMARY_NOVADS.md) - Technical details
3. Review [Library Analysis](LIBRARY_ANALYSIS.md) - Example analysis
4. Check [Final Status](FINAL_STATUS.md) - Current data status

---

## 📖 Document Summaries

### [README.md](../README.md)
**Main project documentation**
- Project overview and features
- Quick installation steps
- Key features and statistics
- Basic usage examples
- Link to all other documentation

### [INSTALLATION.md](INSTALLATION.md)
**Complete setup guide**
- System requirements
- Multiple installation methods (automated, manual, Docker)
- Platform-specific instructions (Windows, macOS, Linux)
- Data download and setup
- Troubleshooting common issues
- Verification steps

### [USAGE.md](USAGE.md)
**User manual**
- Web interface guide
- Data analysis tutorials
- API usage examples (Python, JavaScript, R)
- Common tasks and workflows
- Advanced usage patterns
- Troubleshooting

### [API.md](API.md)
**REST API reference**
- All API endpoints documented
- Request/response formats
- Query parameters
- Code examples in multiple languages
- Error handling
- Rate limiting and CORS

### [DEVELOPMENT.md](DEVELOPMENT.md)
**Developer handbook**
- Development environment setup
- Project architecture explained
- Code style guidelines
- Testing procedures
- Adding new features
- Debugging tips
- Best practices

### [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
**Code organization**
- Complete directory tree
- File naming conventions
- Component descriptions
- Data flow diagrams
- Development workflow
- Extension guidelines

### [QUICK_GUIDE.md](QUICK_GUIDE.md)
**Fast track guide**
- Multi-select interface overview
- Key features summary
- Step-by-step usage
- API quick reference
- Common patterns

### [CONTRIBUTING.md](../CONTRIBUTING.md)
**Contribution guide**
- How to report bugs
- How to suggest features
- Pull request process
- Code review guidelines
- Community standards

### [CHANGELOG.md](../CHANGELOG.md)
**Version history**
- All releases documented
- New features by version
- Bug fixes and improvements
- Breaking changes
- Migration guides

### [IMPLEMENTATION_SUMMARY_NOVADS.md](IMPLEMENTATION_SUMMARY_NOVADS.md)
**Technical deep dive**
- Implementation methodology
- Data processing pipeline
- Fuzzy matching algorithm
- Spatial join techniques
- Quality assurance

### [LIBRARY_ANALYSIS.md](LIBRARY_ANALYSIS.md)
**Library feature analysis**
- Library data processing
- Completeness methodology
- Municipality-level analysis
- Results and findings

### [FINAL_STATUS.md](FINAL_STATUS.md)
**Current project status**
- Data coverage statistics
- Municipality completion status
- Known issues
- Future plans

---

## 🔍 Quick Reference

### Installation
```bash
# Quick install (Windows)
.\setup.ps1
.\run.ps1

# Quick install (Linux/macOS)
./setup.sh
./run.sh
```
See: [INSTALLATION.md](INSTALLATION.md)

### API Endpoints
```
GET /                    # Main map interface
GET /api/csv-data        # Municipality statistics
GET /api/geojson-data    # Geographic boundaries
GET /api/forest-data     # Forest statistics
GET /api/library-data    # Library statistics
```
See: [API.md](API.md)

### Common Tasks
```python
# Load data
import requests
data = requests.get('http://localhost:5000/api/csv-data').json()

# Analyze completeness
import pandas as pd
df = pd.DataFrame(data)
print(df['completeness_pct'].describe())
```
See: [USAGE.md](USAGE.md)

### Running Pipeline
```bash
# Process all data
.\run_forest_pipeline.ps1
.\run_library_pipeline.ps1

# Or individual scripts
python scripts/02_extract_roads.py
python scripts/11_extract_forests.py
```
See: [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 🆘 Getting Help

### Documentation Not Clear?
- Open an [Issue](https://github.com/<your-org>/latvia_osm_project/issues) labeled "documentation"
- Start a [Discussion](https://github.com/<your-org>/latvia_osm_project/discussions)

### Found a Bug?
- Check [FINAL_STATUS.md](FINAL_STATUS.md) for known issues
- Search existing [Issues](https://github.com/<your-org>/latvia_osm_project/issues)
- Create a new issue with detailed description

### Want to Contribute?
- Read [CONTRIBUTING.md](../CONTRIBUTING.md)
- Check open issues labeled "good first issue"
- Join discussions about new features

### Technical Questions?
- Review [DEVELOPMENT.md](DEVELOPMENT.md)
- Check [IMPLEMENTATION_SUMMARY_NOVADS.md](IMPLEMENTATION_SUMMARY_NOVADS.md)
- Ask in [Discussions](https://github.com/<your-org>/latvia_osm_project/discussions)

---

## 📝 Documentation Standards

All documentation in this project follows these standards:

- **Markdown Format**: All docs use GitHub Flavored Markdown
- **Clear Structure**: Headings, lists, and tables for easy scanning
- **Code Examples**: Practical examples for all code snippets
- **Cross-References**: Links between related documents
- **Versioning**: Updated with each release
- **Accessibility**: Clear language, no jargon when possible

---

## 🔄 Keeping Documentation Updated

Documentation is version-controlled alongside code. When making changes:

1. Update relevant documentation files
2. Update CHANGELOG.md with changes
3. Cross-check all references and links
4. Test all code examples
5. Submit as part of pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full process.

---

## 📬 Feedback

Documentation can always be improved! If you find:
- Unclear explanations
- Missing information
- Broken links
- Outdated content
- Typos or errors

Please open an issue or submit a pull request. We appreciate all feedback!

---

*Last updated: January 24, 2026*
