# Client Module - UsrPage_ebkv9e8 Handler Files

> **Last Updated:** 2026-01-20
> **Currently Deployed:** `BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js`

## Quick Reference

| Status | File | Purpose |
|--------|------|---------|
| ✅ **DEPLOYED** | `BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | Hybrid Looker Studio + Excel handler |
| 📋 Backup | `BGApp_eykaguu_UsrPage_ebkv9e8_UsrService_v2.js` | Excel-only with IntExcelReport resolution |
| 📋 Reference | `BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js` | Parent schema (fixed, not deployed) |
| ⚠️ Legacy | All other files | Historical versions, do not deploy |

## Deployment Information

**Child Schema (where handlers are deployed):**
- **Schema UID:** `561d9dd4-8bf2-4f63-a781-54ac48a74972`
- **Package:** BGApp_eykaguu
- **URL:** `https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972`

**Parent Schema (base schema, usually unchanged):**
- **Schema UID:** `4e6a5aa6-86b7-48c1-9147-7b09e96ee59e`
- **Package:** BGlobalLookerStudio

## Current Handler Logic (Hybrid_v2)

```
User clicks "Generate Report"
    ↓
Fetch report metadata from UsrReportesPampa
    ↓
Check if UsrURL exists?
    ├─ YES → Open Looker Studio in new tab (converts /embed/ to /u/0/)
    └─ NO  → Use UsrExcelReportService
              ↓
              Resolve UsrReportesPampa name → IntExcelReport ID
              ↓
              POST /0/rest/UsrExcelReportService/Generate
              ↓
              Download via hidden iframe
```

## File History (Chronological)

| Date | File | Change |
|------|------|--------|
| 2026-01-20 | `BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | **CURRENT** - Hybrid Looker + Excel |
| 2026-01-20 | `BGApp_eykaguu_UsrPage_ebkv9e8_UsrService_v2.js` | Excel-only with ID resolution |
| 2026-01-20 | `BGApp_eykaguu_UsrPage_ebkv9e8_UsrService.js` | Excel-only (wrong ID bug) |
| 2026-01-20 | `BGApp_eykaguu_UsrPage_ebkv9e8_Minimal.js` | Empty schema test |
| 2026-01-19 | `UsrPage_ebkv9e8_Hybrid.js` | Earlier hybrid attempt |
| Earlier | Other files | Various historical versions |

## Known Issues (2026-01-20)

1. **Looker Studio blocked** - CSP prevents iframes, new tab requires Google permissions
2. **Excel template errors** - Some reports have IntExcelReport configuration issues
3. **Commission data gap** - Dec 2025/Jan 2026 missing due to QB payment backlog

## Naming Convention

- `BGApp_eykaguu_*` = Intended for child schema (BGApp_eykaguu package)
- `BGlobalLookerStudio_*` = Intended for parent schema
- `UsrPage_ebkv9e8_*` = Generic/historical (no package prefix)

## Do Not Deploy

These files are historical or have known issues:
- `UsrPage_ebkv9e8_Updated.js` - Has sdk dependency issues in Freedom UI
- `UsrPage_ebkv9e8_IframeDownload.js` - Simple but lacks full functionality
- `UsrPage_ebkv9e8_Native.js` - Uses IntExcelReportService (404 bug)
- Any file not listed as "DEPLOYED" or "Backup" above
