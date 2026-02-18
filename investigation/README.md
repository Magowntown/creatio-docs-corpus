# Investigation Directory

> Package analysis and extracted data for deep investigation.

## Directory Structure

```
investigation/
└── IWQBIntegration/
    ├── IWQBIntegration        # Raw binary (5MB)
    ├── IWQBIntegration.gz     # Compressed (637KB)
    ├── file_list.txt          # Package manifest (43KB)
    └── full_content.txt       # Extracted JSON (4.4MB, 90,255 lines)
```

## IWQBIntegration Package Analysis

### Overview

The IWQBIntegration package was extracted and analyzed to understand its structure before importing to PROD.

### Key Files

| File | Size | Content |
|------|------|---------|
| `full_content.txt` | 4.4MB | Complete JSON configuration extracted from package |
| `file_list.txt` | 43KB | Manifest of all schemas, entities, processes |
| `IWQBIntegration` | 5MB | Original binary package |
| `IWQBIntegration.gz` | 637KB | Compressed for storage |

### Extracted Content

The `full_content.txt` contains:
- Package descriptor and metadata
- 19 package dependencies
- 31 entity definitions (10 extended, 21 created)
- 11 business process configurations
- 4 commission process versions
- 20 Order entity column definitions
- Filter expressions and relationships

### Key Discoveries

1. **Missing Dependency:** IWInterWeavePaymentApp must be imported first
2. **V3 Cascade Bug:** StartSignal4 monitors "any field" causing 26x duplicates
3. **Version Comparison:** PROD package (Sep 2025) has 19 deps vs D1 (Jul 2025) with 13

### Usage

```bash
# Search for specific entity
grep -i "IWPayments" IWQBIntegration/full_content.txt

# Find process configurations
grep -i "Process" IWQBIntegration/full_content.txt | head -50

# Count entities
grep -c "EntitySchemaName" IWQBIntegration/full_content.txt
```

## Related Documentation

- `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` - Complete package index
- `docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` - Import procedure
- `docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` - Root cause analysis
- `docs/investigation/IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` - Risk analysis
