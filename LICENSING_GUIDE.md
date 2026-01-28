# Licenses for LatviaOSM-Check Project

**Date**: January 28, 2026  
**Purpose**: Comprehensive guide to licensing options for the LatviaOSM-Check project

---

## Current License

### MIT License (Currently Used)

**Status**: ✅ **ACTIVE** - Currently applied to this project

**License File**: [LICENSE](../LICENSE)

**Summary**:
```
MIT License
Copyright (c) 2026 LatviaOSM-Check Project Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

**Permissions**:
✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  
✅ Sublicensing  

**Limitations**:
❌ Liability (not liable for damages)  
❌ Warranty (provided as-is)  

**Conditions**:
⚠️ Must include copyright notice  
⚠️ Must include license text  

**Why MIT?**:
- Simple and permissive
- Business-friendly
- Well-recognized in open source
- No copyleft requirements
- Minimal restrictions
- Easy to use commercially

---

## Alternative Licenses for This Project

### 1. GPL v3 (GNU General Public License v3)

**Type**: Copyleft License

**Description**: Strong copyleft license requiring derivative works to be licensed under the same terms.

**Permissions**:
✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  
✅ Patent use  

**Limitations**:
❌ Liability (not liable)  
❌ Warranty (as-is)  
⚠️ Must disclose source code  
⚠️ State changes  
⚠️ Copyleft (derivatives must use same license)  

**When to Use**:
- Want to ensure open source contributions
- Building community-driven project
- Concerned about proprietary forks
- Want patent protection

**Issues for LatviaOSM-Check**:
- Too restrictive for commercial use
- Incompatible with some dependencies
- Complicated for mixed-use scenarios
- May discourage contributions

**Not Recommended** for this project (OSM is data-focused, not code-centric)

---

### 2. Apache License 2.0

**Type**: Permissive License

**Description**: Permissive license with explicit grant of patent rights.

**Permissions**:
✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  
✅ Patent use (explicit)  
✅ Sublicensing  

**Limitations**:
❌ Liability  
❌ Warranty  
⚠️ Trademark use (restricted)  

**Conditions**:
⚠️ Include copyright notice  
⚠️ Include license and notice of changes  
⚠️ State significant modifications  

**When to Use**:
- Patent-heavy project
- Large corporation backing
- Need explicit patent grant
- Software library with many users

**Advantages Over MIT**:
- Explicit patent protection
- Clearer terms
- More enterprise-friendly

**Issues for LatviaOSM-Check**:
- More verbose (longer license text)
- Overkill for academic/research project
- More complex for small projects
- MIT is simpler for same functionality

**Not Recommended** (MIT is simpler, equally permissive)

---

### 3. Creative Commons (CC0, CC-BY, CC-BY-SA)

**Type**: Data/Content License (NOT for software code)

**Variants**:

#### CC0 (Public Domain)
- No restrictions
- Complete public domain
- No attribution needed

#### CC-BY (Attribution)
- Must credit author
- Can use commercially
- Can modify

#### CC-BY-SA (Attribution-Share Alike)
- Must credit author
- Must use same license
- Can use commercially
- Copyleft for data

**When to Use**:
- For data/documentation, NOT code
- For datasets, maps, images
- For research publications

**Issues for LatviaOSM-Check**:
- ✅ Good for data (OSM, official statistics)
- ❌ Not for Python code
- ❌ License mixing required

**Recommendation for This Project**:
- Code: MIT License
- Data: ODbL (from OSM) + CC-BY (official stats)
- Documentation: CC-BY-SA or CC0

---

### 4. ODbL (Open Database License)

**Type**: Data License

**Description**: Reciprocal license for databases and data collections.

**Used By**: OpenStreetMap

**Permissions**:
✅ Copy database  
✅ Create derived databases  
✅ Distribute to public  
✅ Commercial use  

**Conditions**:
⚠️ Keep data open (copyleft for data)  
⚠️ Attribute ODbL/OSM  
⚠️ Derived data must use ODbL  
⚠️ Document all changes  

**Current Use in LatviaOSM-Check**:
- OSM data is under ODbL
- Municipality boundaries (from OSM) are ODbL
- Official statistics: Government/CC-BY

**License Stack**:
```
Software Code:        MIT License
├─ Flask, GeoPandas, etc.: Their licenses
└─ Our code: MIT

Data:
├─ OSM data: ODbL (OpenStreetMap)
├─ Municipality boundaries: ODbL
├─ Official statistics: Government/CC-BY
└─ Analysis output: ODbL (derived from OSM)

Documentation:
├─ README, guides: CC-BY-SA
└─ API docs: CC-BY
```

---

### 5. AGPL v3 (GNU Affero General Public License)

**Type**: Copyleft License (Network Copyleft)

**Description**: Like GPL v3 but extends to network use (cloud/SaaS).

**When to Use**:
- SaaS (Software as a Service) application
- Want to prevent closed-source forks
- Cloud-based deployment
- Community-driven platform

**Permissions**:
✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  
✅ Patent use  
✅ Network use (if you provide source)  

**Limitations**:
❌ Liability  
❌ Warranty  
⚠️ Copyleft (strong)  
⚠️ Must provide source to users  

**For LatviaOSM-Check**:
- Could work since it's deployed as web service
- But too restrictive for general use
- Users accessing API would need source
- Discourages deployment

**Not Recommended** (Over-complicated for this use case)

---

### 6. BSD Licenses (2-Clause or 3-Clause)

**Type**: Permissive License

**Description**: Simple permissive license, less popular than MIT.

#### BSD 2-Clause (Simplified)
```
Redistribution and use permitted with copyright notice and disclaimer
```

#### BSD 3-Clause
```
Same as 2-Clause, plus non-endorsement clause
```

**Comparison to MIT**:
- Similar permissions
- Slightly different wording
- 3-Clause adds non-endorsement clause
- MIT is preferred today

**Not Recommended** (MIT is more popular, simpler)

---

### 7. ISC License

**Type**: Permissive License

**Description**: Functionally equivalent to MIT, even simpler.

**Advantages**:
- Shorter, simpler text
- Functionally same as MIT
- Very clear and concise

**Not Recommended** (MIT is more recognized)

---

## Comparison Table

| License | Type | Copyleft | Patents | Commercial | Simple | 
|---------|------|----------|---------|------------|--------|
| **MIT** ✅ | Permissive | ❌ | ⚠️ | ✅ | ✅ |
| Apache 2.0 | Permissive | ❌ | ✅ | ✅ | ⚠️ |
| BSD 3-Clause | Permissive | ❌ | ⚠️ | ✅ | ✅ |
| ISC | Permissive | ❌ | ⚠️ | ✅ | ✅ |
| GPL v3 | Copyleft | ✅ | ✅ | ⚠️ | ❌ |
| AGPL v3 | Copyleft | ✅ | ✅ | ⚠️ | ❌ |
| ODbL | Data | ✅ | N/A | ✅ | ⚠️ |
| CC0 | Waiver | ❌ | N/A | ✅ | ✅ |
| CC-BY | Content | ❌ | N/A | ✅ | ✅ |

---

## Recommended License Stack for LatviaOSM-Check

### Current (✅ Recommended)

```
┌─────────────────────────────────────────┐
│        SOFTWARE CODE                    │
│        MIT License                      │
│  ✅ Permissive                          │
│  ✅ Commercial use allowed              │
│  ✅ Easy to understand                  │
│  ✅ Industry standard                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│        DATA & DATASETS                  │
│                                         │
│  OSM Data & Derivatives:                │
│  → ODbL (from OpenStreetMap)            │
│  → Reciprocal for derived data          │
│                                         │
│  Official Statistics:                   │
│  → Government license                   │
│  → CC-BY or ODbL acceptable             │
│                                         │
│  Generated Maps & Analysis:             │
│  → ODbL (derived from OSM)              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│        DOCUMENTATION                    │
│                                         │
│  README, Guides:                        │
│  → CC-BY-SA or CC-BY                    │
│  → Allows sharing/improvement           │
│                                         │
│  API Documentation:                     │
│  → CC-BY (attribution required)         │
│                                         │
│  Code Comments:                         │
│  → Same as code (MIT)                   │
└─────────────────────────────────────────┘
```

---

## License Change Process

### If You Want to Change from MIT to Another License

**Steps**:

1. **Update LICENSE file**
   ```bash
   # Replace LICENSE with new license text
   # Download from opensource.org
   ```

2. **Update pyproject.toml**
   ```toml
   license = "New License Name"
   # Update classifiers
   classifiers = [
       "License :: OSI Approved :: New License",
   ]
   ```

3. **Update README.md**
   ```markdown
   [![License: New](https://img.shields.io/badge/License-New-green.svg)]
   ```

4. **Add CHANGELOG entry**
   ```
   ## [X.X.X] - YYYY-MM-DD
   ### Changed
   - Changed license from MIT to New License
   ```

5. **Get contributor consent**
   - All contributors must agree
   - Retroactive changes require permission
   - Document decision in CONTRIBUTING.md

6. **Commit and tag**
   ```bash
   git add LICENSE pyproject.toml README.md CHANGELOG.md
   git commit -m "Change license from MIT to New License"
   git tag -a vX.X.X -m "License change: MIT → New License"
   ```

7. **Notify users**
   - GitHub release notes
   - Documentation update
   - Email to key users

**Note**: Once code is released under MIT, it cannot be revoked. Existing versions remain MIT.

---

## Compatibility Matrix

### Can I Use MIT Code in a Project Licensed Under...?

| Source License | Target License | Compatible? | Notes |
|---|---|---|---|
| MIT | MIT | ✅ Yes | Same license |
| MIT | Apache 2.0 | ✅ Yes | More permissive |
| MIT | GPL v3 | ✅ Yes | Can use MIT under GPL |
| MIT | AGPL v3 | ✅ Yes | Can use MIT under AGPL |
| MIT | Commercial | ✅ Yes | Fully compatible |
| GPL v3 | MIT | ❌ No | GPL code requires GPL |
| GPL v3 | Commercial | ❌ No | Cannot commercialize |
| ODbL | MIT | ⚠️ Complex | Data ≠ Code |

**Key Rule**: MIT code can be used under any other open-source license (one-way compatibility).

---

## Third-Party Dependencies & Their Licenses

### Python Package Licenses

```
Framework:
├─ Flask 2.3.3          → BSD 3-Clause
├─ Werkzeug             → BSD 3-Clause
└─ Jinja2               → BSD 3-Clause

Geospatial:
├─ GeoPandas 0.13.2     → BSD 3-Clause
├─ Shapely 2.0.1        → BSD 3-Clause
├─ Fiona 1.9.4          → MIT
└─ PyOGRIO 0.7.2        → MIT

Data Processing:
├─ Pandas 2.0.3         → BSD 3-Clause
└─ NumPy                → BSD 3-Clause

String Matching:
├─ FuzzyWuzzy           → GPL v2
└─ python-Levenshtein   → GPL v2 or proprietary

Utilities:
├─ Requests             → Apache 2.0
└─ Others               → Various (mostly MIT/BSD)

Frontend:
├─ Leaflet.js           → BSD 2-Clause
├─ Bootstrap 5          → MIT
├─ OpenStreetMap        → ODbL
└─ jQuery               → MIT
```

**License Conflict Risk**: ⚠️ FuzzyWuzzy is GPL v2 (weak copyleft)

### Handling GPL Dependencies

**Problem**: FuzzyWuzzy (GPL v2) is used in the project

**Solutions**:

1. **Keep Current Setup** (RECOMMENDED)
   - Distribution includes GPL code
   - Only applies if you distribute as executable
   - Web app (SaaS) not affected
   - Research/educational use: No problem

2. **Replace FuzzyWuzzy**
   - Use RapidFuzz (MIT licensed, faster)
   - Update scripts:
     ```python
     # Instead of:
     # from fuzzywuzzy import fuzz
     # Use:
     from rapidfuzz import fuzz
     ```
   - All GPL issues gone

3. **Add GPL Compliance**
   - Make source code available
   - Document GPL dependencies
   - Include license headers

**Recommendation**: Replace FuzzyWuzzy with RapidFuzz (MIT) for cleaner licensing.

---

## Best Practices for LatviaOSM-Check

### ✅ DO:

1. **Keep MIT License for Code**
   ```
   Simple, permissive, business-friendly
   ```

2. **Clearly Separate Data & Code**
   ```
   Data (ODbL) ≠ Code (MIT)
   Document both in LICENSE
   ```

3. **Include License Notices**
   - In README.md
   - In LICENSE file
   - In CONTRIBUTING.md

4. **Document Dependencies**
   - Include requirements.txt
   - Note their licenses
   - Identify any conflicts

5. **Use SPDX Identifiers**
   ```python
   # At top of each source file:
   # SPDX-License-Identifier: MIT
   ```

6. **Add Header Comments**
   ```python
   """
   LatviaOSM-Check - OpenStreetMap Data Quality Analysis
   
   SPDX-License-Identifier: MIT
   Copyright (c) 2026 LatviaOSM-Check Contributors
   """
   ```

### ❌ DON'T:

1. **Don't Mix GPL and Proprietary**
   - If using GPL code, must distribute source
   - Not suitable for closed-source products

2. **Don't Forget Attribution**
   - MIT requires copyright notice
   - ODbL requires OSM attribution
   - Official stats need government credit

3. **Don't Change Licenses Without Consensus**
   - Get contributor agreement
   - Can't retroactively change existing versions
   - Announce changes clearly

4. **Don't Ignore Dependencies' Licenses**
   - Check each package license
   - Ensure compatibility
   - Document in LICENSE

5. **Don't Remove License Text**
   - MIT requires full license inclusion
   - Keep LICENSE file in distribution
   - Include in source packages

---

## Resources

### Official License Resources

- **MIT License**: https://opensource.org/licenses/MIT
- **Apache 2.0**: https://opensource.org/licenses/Apache-2.0
- **GPL v3**: https://www.gnu.org/licenses/gpl-3.0.html
- **ODbL**: https://opendatacommons.org/licenses/odbl/
- **Creative Commons**: https://creativecommons.org/licenses/
- **SPDX License List**: https://spdx.org/licenses/
- **choosealicense.com**: https://choosealicense.com/

### Compatibility Tools

- **SPDX License Wizard**: https://spdx.org/licenses/
- **TLDRLegal**: https://tldrlegal.com/ (Simple summaries)
- **License Compatibility**: https://www.fsf.org/licensing/

### For This Project

- **LICENSE**: [MIT License](../LICENSE)
- **pyproject.toml**: License metadata
- **CONTRIBUTING.md**: License info for contributors
- **README.md**: License badge

---

## Summary

| Question | Answer |
|----------|--------|
| **Current License?** | MIT License ✅ |
| **Can I use commercially?** | Yes ✅ |
| **Can I modify?** | Yes ✅ |
| **Do I need to share changes?** | No (but appreciated) |
| **Do I need attribution?** | Yes (copyright notice) |
| **Can I use in GPL project?** | Yes ✅ |
| **What about OSM data?** | ODbL (separate from code) |
| **Should we change licenses?** | No, MIT is ideal |
| **GPL dependencies OK?** | Yes for research/SaaS, consider replacing for distribution |

---

**Conclusion**: MIT License is the **optimal choice** for LatviaOSM-Check - permissive, business-friendly, and well-recognized in the open-source community.

