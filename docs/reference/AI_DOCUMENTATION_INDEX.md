# AI Documentation Index

**Purpose:** Quick reference guide for AI assistants working on the Creatio Reports Fix project.
**Last Updated:** 2026-01-23

---

## Quick Start for New AI Sessions

### 1. Read These First
| Priority | File | What You'll Learn |
|----------|------|-------------------|
| 1 | `CLAUDE.md` (root) | Current issues, status, active work |
| 2 | `docs/HANDLER_VERSION_HISTORY.md` | Handler iterations, current version (v18) |
| 3 | `docs/SESSION_LOG_20260123.md` | Latest session work and discoveries |

### 2. Current Production Files
| Component | File |
|-----------|------|
| Frontend handler | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v18_AttrBinding.js` |
| Backend service | `source-code/UsrExcelReportService_Updated.cs` |
| Parent schema | `client-module/BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js` |

### 3. Key Schema UIDs
| Schema | UID | Package |
|--------|-----|---------|
| Child (deploy here) | `561d9dd4-8bf2-4f63-a781-54ac48a74972` | BGApp_eykaguu |
| Parent (don't modify) | `4e6a5aa6-86b7-48c1-9147-7b09e96ee59e` | BGlobalLookerStudio |

---

## Documentation Categories

### Active Issues & Status
| File | Content |
|------|---------|
| `CLAUDE.md` | Master status file with all issues |
| `CURRENT_STATUS.md` | Condensed current state |
| `ACTION_PLAN.md` | Priority queue and next steps |

### Handler Development (UI-002)
| File | Content |
|------|---------|
| `HANDLER_VERSION_HISTORY.md` | All handler versions v10-v18 with issues/solutions |
| `SESSION_LOG_20260123.md` | v15→v18 development session |
| `REPORT_FILTER_MAPPING.md` | Which filters show for which reports |
| `UI002_FIX_CATALOG.md` | Previous fix attempts |
| `UI002_DEPLOYMENT_CHECKLIST.md` | Deployment steps |

### QuickBooks Sync Issues
| File | Content |
|------|---------|
| `QB_SYNC_INFRASTRUCTURE_ISSUE.md` | SYNC-004: QB Web Connector offline |
| `QB_SYNC_AUTOMATION.md` | Automated sync setup |
| `QB_TEAM_ACTION_REQUIRED.md` | Actions needed from QB team |
| `SYNC_003_BATCH_PROCESSING.md` | 20K record limit workaround |

### Commission Data Issues
| File | Content |
|------|---------|
| `COMMISSION_DATA_PIPELINE_ANALYSIS.md` | Full data flow trace |
| `COMMISSION_FIX_COMPLETE.md` | BGCommissionEarner fix |
| `CLIENT_COMMISSION_UPDATE_20260120.md` | Client-facing status |

### Technical Reference
| File | Content |
|------|---------|
| `CLAUDE_REFERENCE.md` | API patterns, entity schemas, deployment |
| `CREATIO_HANDLER_INSTRUCTIONS.md` | Freedom UI handler patterns |
| `CREATIO_REPORT_SYSTEM_ANALYSIS.md` | System architecture |
| `PACKAGE_COMPARISON.md` | IWQBIntegration vs PampaBayQuickBooks |

### Investigation Records
| File | Content |
|------|---------|
| `INVESTIGATION_PAYMENT_STATUS.md` | DATA-001: PaymentStatusId analysis |
| `USRPAGE_CONFLICT_ANALYSIS.md` | SYNC-002: Page handler vs QB sync |
| `REPORT_BUTTON_INVESTIGATION.md` | Report generation flow |

### Session Logs
| File | Content |
|------|---------|
| `SESSION_LOG_20260123.md` | Handler v15→v18, visibility fix |
| `INVESTIGATION_SUMMARY_20260119.md` | Commission earners fix |
| `TEAM_SUMMARY_20260120.md` | Non-technical team summary |

### External Communication
| File | Content |
|------|---------|
| `EMAIL_BGLOBAL_REPORT_ISSUES.md` | Email to BGlobal about CSP/Looker |
| `EMAIL_BGLOBAL_QB_CONNECTOR_20260120.md` | QB Connector status |
| `QB_TEAM_EMAIL_DRAFT.md` | QB team action request |
| `E6SOLUTIONS_MEETING_NOTES_20260120.md` | Meeting notes |

---

## Key Technical Patterns

### Freedom UI Dynamic Visibility (IMPORTANT)
**Problem:** Need to show/hide parent schema elements from child schema based on runtime conditions.

**Solution:** Attribute binding (NOT DOM manipulation)

```javascript
// In child schema viewModelConfigDiff:
"UsrShowFilters": { "value": false }

// Merge onto parent element:
{
    "operation": "merge",
    "name": "ParentGridContainer",
    "values": { "visible": "$UsrShowFilters" }
}

// Toggle in handler:
request.$context.UsrShowFilters = true;
```

**Why DOM manipulation fails:**
- `visible: false` = element not rendered to DOM
- Cannot find/manipulate elements that don't exist

### Report Type Detection
```javascript
const reportName = selectedReport.displayValue.toLowerCase();
const isCommissionReport = reportName.includes("commission");

// Check for Looker URL
const metaUrl = "/0/odata/UsrReportesPampa(" + id + ")?$select=UsrURL";
const meta = await fetch(metaUrl, {...}).then(r => r.json());
const isLookerReport = meta.UsrURL && meta.UsrURL.length > 0;
```

### Excel Template Resolution
```javascript
// UsrReportesPampa.Name → IntExcelReport.IntName
const odataUrl = "/0/odata/IntExcelReport?$filter=" +
    "(IntName eq '" + name + "' or IntName eq 'Rpt " + name + "')";
```

---

## Common Issues & Solutions

| Issue | Solution | Reference |
|-------|----------|-----------|
| Filters visible when should be hidden | Use attribute binding, not DOM | `HANDLER_VERSION_HISTORY.md` |
| Looker iframe blocked | Open in new tab | v18 handler |
| Excel download 404 | Check IntExcelReport template ID | `DL-004` in CLAUDE.md |
| Schema compilation error | Check attribute defined in viewModelConfigDiff | `UI-002` section |
| Report takes 60+ seconds | Normal for large datasets | `REPORT_TESTING_CHECKLIST.md` |

---

## Deployment Quick Reference

### Child Schema (Handler)
```
URL: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
File: client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v18_AttrBinding.js
After: Hard refresh (Ctrl+Shift+R)
```

### Backend Service
```
URL: https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
File: source-code/UsrExcelReportService_Updated.cs
```

---

## File Naming Conventions

| Pattern | Meaning |
|---------|---------|
| `*_v##_*.js` | Handler versions (v10-v18) |
| `SESSION_LOG_YYYYMMDD.md` | Daily session logs |
| `EMAIL_*.md` | External communication drafts |
| `*_INVESTIGATION.md` | Deep-dive analysis |
| `*_CHECKLIST.md` | Testing/deployment steps |

---

## Entity Quick Reference

| Entity | Purpose |
|--------|---------|
| `UsrReportesPampa` | Report definitions with UsrURL for Looker |
| `IntExcelReport` | Excel template configurations |
| `BGCommissionReportQBDownload` | QB commission sync data |
| `BGCommissionEarner` | Sales rep commission assignments |
| `BGYearMonth` | Year-month lookup for filtering |
| `BGSalesGroup` | Sales group lookup |

---

## Environment URLs

| Environment | URL |
|-------------|-----|
| PROD | `https://pampabay.creatio.com` |
| DEV | `https://dev-pampabay.creatio.com` |
