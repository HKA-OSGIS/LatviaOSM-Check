# Documentation Setup Guide

## GitHub Repository Configuration

This document explains how to configure the GitHub-related placeholders in the documentation.

### Placeholders to Replace

Throughout the documentation and configuration files, you'll find placeholder text that needs to be replaced with your actual GitHub repository information:

**Placeholder**: `<your-org>` / `<your-org>/latvia_osm_project`

**Description**: This is the GitHub repository URL path that needs to be replaced with your actual GitHub organization and repository name.

### Files with Placeholders

The following files contain `<your-org>` placeholders that should be replaced:

1. **README.md** (root level)
   - Clone URL examples
   - Repository links

2. **INSTALLATION.md**
   - Clone URL examples (multiple locations)
   - GitHub Issues link
   - GitHub Discussions link

3. **DEVELOPMENT.md**
   - Clone URL example

4. **API.md**
   - GitHub Issues link

5. **CONTRIBUTING.md** (if present)
   - Repository links

6. **CONTRIBUTORS.md**
   - Repository links

7. **pyproject.toml**
   - Repository URL
   - Homepage URL
   - Documentation URL

### How to Configure

#### Option 1: Manual Replacement

1. Determine your GitHub organization/repository path
   - Example: `latviaosm/latvia_osm_project`
   - Example: `my-org/latviaosm-check`

2. Use Find & Replace (Ctrl+H / Cmd+H in VS Code)
   - Find: `<your-org>`
   - Replace with: `your-organization-name`

3. Repeat for any other placeholder patterns

#### Option 2: Script-based Replacement

```bash
#!/bin/bash
# Replace placeholders in documentation

ORG_NAME="your-organization-name"
REPO_NAME="latvia_osm_project"

# Replace in all markdown files
find . -name "*.md" -type f -exec sed -i "s|<your-org>|$ORG_NAME|g" {} +

# Replace in pyproject.toml
sed -i "s|<your-org>|$ORG_NAME|g" pyproject.toml

# Replace in Python files
find . -name "*.py" -type f -exec sed -i "s|<your-org>|$ORG_NAME|g" {} +

echo "✓ All placeholders replaced with: $ORG_NAME"
```

#### Option 3: Python Script

```python
#!/usr/bin/env python3
"""
Replace GitHub placeholders in project files.
"""

from pathlib import Path
import re

def replace_placeholders(org_name):
    """Replace <your-org> placeholder with actual organization name."""
    
    # Files to update
    files_to_update = [
        'README.md',
        'pyproject.toml',
        'docs/README.md',
        'docs/INSTALLATION.md',
        'docs/DEVELOPMENT.md',
        'docs/API.md',
        'CONTRIBUTORS.md',
        'CONTRIBUTING.md'
    ]
    
    pattern = re.compile(r'<your-org>')
    updated_count = 0
    
    for file_path in files_to_update:
        path = Path(file_path)
        if path.exists():
            content = path.read_text()
            if pattern.search(content):
                new_content = pattern.sub(org_name, content)
                path.write_text(new_content)
                print(f"✓ Updated: {file_path}")
                updated_count += 1
    
    print(f"\n✓ Total files updated: {updated_count}")
    print(f"✓ All placeholders replaced with: {org_name}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python setup_docs.py <organization-name>")
        print("Example: python setup_docs.py my-org")
        sys.exit(1)
    
    org_name = sys.argv[1]
    replace_placeholders(org_name)
```

### Examples

**Before:**
```bash
git clone https://github.com/<your-org>/latvia_osm_project.git
```

**After:**
```bash
git clone https://github.com/my-geospatial-org/latvia_osm_project.git
```

---

## Other Configuration Items

### Docker Configuration (Coming Soon)

The README notes "Docker (Coming Soon)". When Docker support is ready:

1. Create `Dockerfile` in project root
2. Create `docker-compose.yml`
3. Update README.md to replace "Coming Soon" with Docker instructions
4. Add Docker section to INSTALLATION.md

Example Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Future Features (Coming Soon)

The codebase notes several "Coming Soon" features:

1. **Railways Analysis** - Train network data
2. **Buildings Analysis** - Building footprints
3. **POIs (Points of Interest)** - Hospitals, restaurants, etc.

To implement:

1. Create extraction scripts (e.g., `scripts/31_extract_railways.py`)
2. Add processing modules in `src/processing/`
3. Create visualization scripts
4. Add API endpoints
5. Update documentation

---

## Verification Checklist

After configuring all placeholders:

- [ ] All `<your-org>` references are replaced
- [ ] GitHub clone URLs point to correct repository
- [ ] GitHub Issues link is correct
- [ ] GitHub Discussions link is correct
- [ ] pyproject.toml repository URLs are correct
- [ ] README.md links are all valid
- [ ] INSTALLATION.md links work
- [ ] DEVELOPMENT.md links are correct

---

## Support

If you need help configuring these placeholders:

1. Check the specific file mentioned in the error/issue
2. Look for `<your-org>` text
3. Replace with your actual GitHub organization name
4. Test that the resulting URLs are valid

For example, if your org is `geomatics-team` and repo is `latvia-osm`, the URL should be:
```
https://github.com/geomatics-team/latvia-osm
```

---

**Note**: This configuration is a one-time setup. After replacing all placeholders, delete this file or keep it for reference.

**Status**: ✅ All documentation complete - Only placeholders need GitHub repository configuration
