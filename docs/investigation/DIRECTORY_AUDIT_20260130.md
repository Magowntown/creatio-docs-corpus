# Comprehensive Directory Audit

**Date:** 2026-01-30
**Scope:** `/home/magown/creatio-report-fix` + `/home/magown/creatio-report-fix-archive` + related directories

---

## Executive Summary

| Category | Count | Status |
|----------|-------|--------|
| **Source Code Files (*.cs)** | 9 | 1 deployed, 8 legacy |
| **Client Module Files (*.js)** | 98 | 1 deployed (v54), 97 legacy/versions |
| **Package ZIPs** | 7 | Extracted, can archive |
| **Archive Directory** | 2 files | Unrelated JSON validation reports |
| **Other Creatio Directories** | 4 | Separate projects |

---

## 1. Source Code Files (`source-code/`)

### Currently Deployed

| File | Size | Status | Notes |
|------|------|--------|-------|
| `UsrExcelReportService_Updated.cs` | 145KB | **✅ DEPLOYED** | Main service with all fixes |

### Legacy Files (DO NOT DEPLOY)

| File | Size | Status | Notes |
|------|------|--------|-------|
| `UsrExcelReportService_ROLLBACK.cs` | 130KB | ⚠️ Backup | Original before fixes |
| `UsrExcelReportService_v2.cs` | 23KB | ❌ Legacy | Early iteration |
| `UsrExcelReportService_Fixed.cs` | 22KB | ❌ Legacy | Intermediate fix |
| `UsrExcelReportService_Standalone.cs` | 20KB | ❌ Legacy | Standalone attempt |
| `UsrExcelReportService_WithFilters.cs` | 13KB | ❌ Legacy | Filter testing |
| `BGIntExcelReportService2_updated.cs` | 10KB | ❌ Legacy | Built-in service mod |
| `UsrExcelReportService_Simple.cs` | 8KB | ❌ Legacy | Simplified version |
| `UsrExcelReportService_FIXED.cs` | 3KB | ❌ Legacy | Early fix attempt |

### Recommendation

**Keep:** `UsrExcelReportService_Updated.cs` (deployed) + `UsrExcelReportService_ROLLBACK.cs` (emergency)
**Archive:** Move other 7 files to `source-code/archive/`

---

## 2. Client Module Files (`client-module/`)

### Currently Deployed

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js` | v54 | **✅ PROD** | Customer ID value fix |

### Version History (98 total files)

| Range | Count | Description |
|-------|-------|-------------|
| v1-v9 | ~10 | Early development (Hybrid, UsrService) |
| v10-v18 | 9 | Initial production iterations |
| v19.x | 13 | Major development phase (Looker, filters) |
| v20-v39 | 20 | Architecture exploration |
| v40-v54 | 15 | Customer lookup iterations |
| Other | ~31 | Diagnostic, Original, Minimal, etc. |

### Key Versions

| Version | File | Purpose | Keep? |
|---------|------|---------|-------|
| **v54** | `_v54_FlatObject.js` | **DEPLOYED** - Customer fix | ✅ Yes |
| **v51** | `_v51_StableDialog.js` | Fixed infinite loading | ✅ Yes (backup) |
| **v19.13** | `_v19.13_ForcedReload.js` | Date filters working | ✅ Yes (reference) |
| v50 | `_v50_CorrectEmbedded.js` | BROKEN - caused infinite loading | ⚠️ Reference |
| ROLLBACK | `UsrPage_ebkv9e8_ORIGINAL_INTEXCEL.js` | Original BGlobal code | ✅ Yes (emergency) |

### Recommendation

**Keep:**
- v54 (deployed)
- v51, v50 (recent working/broken for reference)
- v19.13, v19.16 (working date filters)
- ORIGINAL_INTEXCEL (emergency rollback)
- DIAGNOSTIC, MINIMAL_HYBRID (debugging tools)

**Archive:** Move ~85 other versions to `client-module/archive/`

---

## 3. Package ZIP Files (Root Directory)

| File | Size | Date | Contents |
|------|------|------|----------|
| `PampaBay_2026-01-28_16.45.47.zip` | 2.2MB | Jan 28 | Main PROD package |
| `IntExcelExport_2026-01-28_16.46.12.zip` | 650KB | Jan 28 | Excel export library |
| `IWQBIntegration_2026-01-30_08.33.58.zip` | 632KB | Jan 30 | QB integration (latest) |
| `BGApp_eykaguu_2026-01-28_16.43.41.zip` | 207KB | Jan 28 | Custom app package |
| `BpmonlineCloudIntegration_2026-01-28_16.44.17.zip` | 86KB | Jan 28 | Cloud integration |
| `Custom_2026-01-28_16.46.28.zip` | 79KB | Jan 28 | Custom package |
| `BGlobalLookerStudio_2026-01-28_16.43.57.zip` | 63KB | Jan 28 | Looker integration |

### Recommendation

**Keep for reference:** All ZIPs (contain original BGlobal code for investigation)
**Organization:** Move to `packages/` subdirectory

---

## 4. Archive Directory (`creatio-report-fix-archive/`)

**Contents:** Only 2 files, unrelated to report fix:

| File | Date | Contents |
|------|------|----------|
| `json_syntax_summary.md` | Aug 4, 2025 | JSON validation tool docs |
| `json_validation_report.md` | Aug 4, 2025 | JSON validation results |

### Status

This archive contains old JSON validation work, **NOT** archived report fix code.

### Recommendation

Leave as-is or delete (not relevant to current work)

---

## 5. Documentation Structure (`docs/`)

### Current Structure

```
docs/
├── archive/          # Old status docs
├── communication/    # Emails, team summaries
├── deployment/       # Deployment guides
├── investigation/    # Technical deep-dives ← MOST ACTIVE
├── issues/           # Issue tracking
├── logs/             # Session logs
├── qb-sync/          # QuickBooks sync docs
└── reference/        # Reference materials
```

### Key Documents

| Directory | Key Files | Status |
|-----------|-----------|--------|
| `investigation/` | BGLOBAL_V7_ARCHITECTURE_COMPLETE.md | ✅ Current |
| `investigation/` | INTEXCELREPORT_COMPLETE_ANALYSIS.md | ✅ Current |
| `investigation/` | FIX_VS_V7_ARCHITECTURE_AUDIT.md | ✅ Current |
| `logs/` | SESSION_LOG_20260130.md | ✅ Active |
| `reference/` | HANDLER_VERSION_HISTORY.md | ✅ Reference |
| `reference/` | MASTER_CATALOG.md | ✅ Reference |

### Recommendation

Documentation structure is good. No changes needed.

---

## 6. Other Creatio Directories

### `/home/magown/creatio/`

**Contents:** Just `clio/` tool installation
**Status:** Keep - Creatio CLI tool

### `/home/magown/creatio_packages/`

**Contents:** IWQBIntegration package extracted
**Status:** Keep for QB sync work

### `/home/magown/creatio-ai-knowledge-hub/`

**Contents:** Separate AI knowledge base project
**Status:** Unrelated to report fix

### `/home/magown/creatio_screenshots/`

**Contents:** Browser screenshots
**Status:** Keep for debugging reference

---

## 7. Files in Home Directory

| File | Purpose | Action |
|------|---------|--------|
| `BGIntExcelreportMixin_fixed.js` | Fixed mixin from investigation | Move to repo |
| `BGIntExcelreportMixin_original.js` | Original mixin for reference | Move to repo |

---

## 8. Cleanup Recommendations

### High Priority (Do Now)

1. **Create archive directories:**
   ```bash
   mkdir -p /home/magown/creatio-report-fix/source-code/archive
   mkdir -p /home/magown/creatio-report-fix/client-module/archive
   mkdir -p /home/magown/creatio-report-fix/packages
   ```

2. **Move legacy source code:**
   ```bash
   mv source-code/UsrExcelReportService_v2.cs source-code/archive/
   mv source-code/UsrExcelReportService_Fixed.cs source-code/archive/
   mv source-code/UsrExcelReportService_Standalone.cs source-code/archive/
   mv source-code/UsrExcelReportService_WithFilters.cs source-code/archive/
   mv source-code/UsrExcelReportService_Simple.cs source-code/archive/
   mv source-code/UsrExcelReportService_FIXED.cs source-code/archive/
   mv source-code/BGIntExcelReportService2_updated.cs source-code/archive/
   ```

3. **Move package ZIPs:**
   ```bash
   mv *.zip packages/
   ```

4. **Move home directory files:**
   ```bash
   mv /home/magown/BGIntExcelreportMixin_*.js client-module/reference/
   ```

### Medium Priority (Later)

5. **Archive old client-module versions:**
   - Keep: v54, v51, v50, v19.13, v19.16, ORIGINAL, DIAGNOSTIC, MINIMAL
   - Archive: Everything else (~85 files)

### Low Priority (Optional)

6. **Delete archive directory contents:**
   - JSON validation files are from Aug 2025, unrelated

---

## 9. Verification: What's Actually Deployed

### PROD Backend

**Schema:** `UsrExcelReportService` (UID: ed794ab8-8a59-4c7e-983c-cc039449d178)
**Local File:** `source-code/UsrExcelReportService_Updated.cs`
**Status:** ✅ Matches (pending RPT-005 fix deployment)

### PROD Frontend

**Schema:** `BGApp_eykaguu_UsrPage_ebkv9e8` (UID: 873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2)
**Local File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js`
**Status:** ✅ Deployed (v54)

---

## 10. Summary

### Files to Keep (Essential)

| Type | File | Reason |
|------|------|--------|
| Backend | `UsrExcelReportService_Updated.cs` | Deployed |
| Backend | `UsrExcelReportService_ROLLBACK.cs` | Emergency rollback |
| Frontend | `_v54_FlatObject.js` | Deployed |
| Frontend | `_v51_StableDialog.js` | Recent working backup |
| Frontend | `_v19.13_ForcedReload.js` | Date filter reference |
| Frontend | `ORIGINAL_INTEXCEL.js` | Emergency rollback |

### Files to Archive (Move to archive/)

- 7 legacy backend files
- ~85 legacy frontend files

### Space Recovery

Moving legacy files to archive/ will clean up the main directories without losing history.

---

*Audit completed: 2026-01-30*
*Analyst: Claude Code*
