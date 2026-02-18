# AI Navigation Guide

**Purpose:** Enable any AI assistant to quickly locate relevant documentation based on user requests.
**Updated:** 2026-02-05

---

## 🎯 Quick Reference Card

> **Ultra-compact navigation** - Use this section for instant lookup. Detailed scenarios below.

### By Task (One-Line Lookup)

| Task | Start Here |
|------|------------|
| **What's the status?** | `/CLAUDE.md` |
| **IWQBIntegration import** | `investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` |
| **Report issues** | `reference/MASTER_CATALOG.md` |
| **QB sync issues** | `qb-sync/QB_SYNC_AUTOMATION.md` |
| **Frontend/SDK** | `reference/CREATIO_SDK_REFERENCE.md` |
| **Find a file** | `reference/RESOURCE_INVENTORY.md` |
| **Deploy something** | `/CLAUDE.md` → Quick Deploy section |
| **Session history** | `logs/SESSION_LOG_20260203.md` |

### Key SDK Patterns (Copy-Paste Ready)

```typescript
// Module bootstrap
bootstrapCrtModule('pkg', AppModule, { resolveDependency: t => injector.get(t) });

// View element
@CrtViewElement({ selector: 'usr-my', type: 'usr.My' })

// Data access
const model = await sdk.Model.create('Contact');
const items = await model.load({ Name: 'John' });
```

### Critical Gotchas

| Gotcha | Rule |
|--------|------|
| WCF dates | Use `/Date(ms)/` not ISO 8601 |
| Customer filter | Must be LOOKUP, never text |
| Data sources | Only ONE per Freedom UI page |
| V3 commission | Keep DISABLED (26x cascade bug) |

### File Locations

| Resource | Path |
|----------|------|
| Backend service | `source-code/UsrExcelReportService_Updated.cs` |
| Frontend handler | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js` |
| SDK types | `node_modules/@creatio-devkit/common/index.d.ts` |
| Freedom UI template | `FreedomUIProjectTemplate_v5/` |
| Academy code examples | `creatio-docs-full/code/` (1,496 dirs) |
| Package analysis | `investigation/IWQBIntegration/full_content.txt` |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | **Entry point** - current status, issues, quick deploy |
| `docs/AI_NAVIGATION.md` | **This document** - scenario-based lookup |
| `docs/DOCUMENT_INDEX.md` | **Complete listing** - all documents with relationships |
| `docs/SHARED_UNDERSTANDING.md` | **Comprehensive reference** - complete system knowledge |

---

## How to Use This Document

1. **Identify the scenario** from user's request
2. **Find matching category** below
3. **Load recommended documents** in order listed
4. **Follow action guidance** for that scenario
5. **For complete document listing**, see `docs/DOCUMENT_INDEX.md`

---

## Scenario → Document Mapping

### 🔧 IWQBIntegration / QuickBooks Package

| User Might Say | Load These Documents (in order) |
|----------------|--------------------------------|
| "Import IWQBIntegration to PROD" | `docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` → `IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md` |
| "What's in the IWQBIntegration package?" | `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` |
| "IWQBIntegration risks" / "conflicts" | `docs/investigation/IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` → `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` |
| "26x duplicate" / "cascade issue" | `docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` (Deep Dive #2) |
| "Commission process versions" | `docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` (Deep Dive #1) |
| "Invoice race condition" | `docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` (Deep Dive #3) |
| "Order columns" / "PCI data" | `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` (Order Entity Column Catalog) |
| "IWQBIntegration summary" | `docs/investigation/IWQBINTEGRATION_SUMMARY.md` |
| "What to do next for IWQB" | `docs/investigation/IWQBINTEGRATION_NEXT_STEPS.md` |

### 📊 Reports / Excel Generation

| User Might Say | Load These Documents (in order) |
|----------------|--------------------------------|
| "Report not working" / "report error" | `CLAUDE.md` (Active Issues) → `docs/reference/MASTER_CATALOG.md` |
| "Customers did not buy" / "RPT-005" | `docs/investigation/RPT005_COMPREHENSIVE_REVIEW.md` → `docs/issues/RPT005_DEPLOYMENT_CHECKLIST.md` |
| "Items by Customer" / "RPT-004/006/008" | `docs/issues/ITEMS_BY_CUSTOMER_FIX_20260128.md` → `docs/issues/ITEMS_BY_CUSTOMER_VBA_FIX.md` |
| "Report filters" / "filter mapping" | `docs/reference/REPORT_FILTER_REQUIREMENTS.md` |
| "All reports" / "report catalog" | `docs/reference/MASTER_CATALOG.md` |
| "BGlobal architecture" / "V7 pattern" | `docs/investigation/BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` |
| "UsrExcelReportService" / "backend handler" | `source-code/UsrExcelReportService_Updated.cs` |
| "Frontend handler" / "client module" | `docs/reference/HANDLER_VERSION_HISTORY.md` |
| "VBA macro" / "Excel macro fix" | `vba/PMPSalesbySalesRep_FIXED_v2.bas` |

### 🔄 QuickBooks Sync

| User Might Say | Load These Documents (in order) |
|----------------|--------------------------------|
| "QB sync" / "QuickBooks sync" | `docs/qb-sync/QB_SYNC_AUTOMATION.md` |
| "20K limit" / "SYNC-003" | `docs/qb-sync/SYNC_003_BATCH_PROCESSING.md` |
| "QB Web Connector" / "SYNC-004" | `CLAUDE.md` (QB Integration Go-Live Status) |
| "False processed orders" / "SYNC-005" | `CLAUDE.md` (SYNC-005 section) |
| "Commission sync" | `docs/qb-sync/QB_SYNC_AUTOMATION.md` |

### 🖥️ Frontend / UI / SDK

| User Might Say | Load These Documents (in order) |
|----------------|--------------------------------|
| "Frontend handler" / "page handler" | `docs/reference/HANDLER_VERSION_HISTORY.md` → `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js` |
| "Infinite loading" / "UI-006" | `CLAUDE.md` (UI-006 section) |
| "Customer filter" / "lookup" | `docs/reference/HANDLER_VERSION_HISTORY.md` (v54) |
| "Looker Studio" / "iframe" | `CLAUDE.md` (CSP-001) |
| "Freedom UI" | `docs/reference/CLAUDE_REFERENCE.md` → `docs/reference/CREATIO_SDK_REFERENCE.md` |
| "TypeScript SDK" / "@creatio-devkit" | `docs/reference/CREATIO_SDK_REFERENCE.md` |
| "CrtModule" / "CrtViewElement" | `docs/reference/CREATIO_SDK_REFERENCE.md` (Decorators section) |
| "Model service" / "data access" | `docs/reference/CREATIO_SDK_REFERENCE.md` (Model section) |
| "Custom component" / "Angular component" | `docs/reference/CREATIO_SDK_REFERENCE.md` → `FreedomUIProjectTemplate_v5.zip` |
| "Request handler" / "handler chain" | `docs/reference/CREATIO_SDK_REFERENCE.md` (Handler Chain Pattern) |
| "Creatio architecture" / "how Creatio works" | `docs/reference/CREATIO_ARCHITECTURE_DEEP_DIVE.md` |

### 📋 Deployment

| User Might Say | Load These Documents (in order) |
|----------------|--------------------------------|
| "Deploy backend" | `CLAUDE.md` (Quick Deploy section) |
| "Deploy frontend" | `CLAUDE.md` (Quick Deploy section) → `docs/reference/HANDLER_VERSION_HISTORY.md` |
| "Deploy to PROD" | `CLAUDE.md` → specific issue docs |
| "Test deployment" | `docs/deployment/REPORT_TESTING_CHECKLIST.md` |
| "Rollback" | Relevant issue doc (each has rollback section) |

### 🔍 Investigation / Debugging

| User Might Say | Load These Documents (in order) |
|----------------|--------------------------------|
| "Investigate" / "debug" / "find issue" | `CLAUDE.md` → `docs/investigation/COMPREHENSIVE_INVESTIGATION_SUMMARY.md` |
| "Session history" / "what happened" | `docs/logs/SESSION_LOG_20260203.md` → `docs/logs/SESSION_HISTORY.md` |
| "Test results" | `docs/logs/TEST_LOG.md` |
| "All issues" / "issue tracker" | `CLAUDE.md` (Issue Tracker section) |

### 📝 Communication / Handoff

| User Might Say | Load These Documents (in order) |
|----------------|--------------------------------|
| "Email" / "draft email" | `docs/communication/EMAIL_*.md` |
| "Handoff" / "e6solutions" | `docs/HANDOFF_E6SOLUTIONS.md` |
| "Team summary" | `docs/communication/TEAM_SUMMARY_*.md` |
| "BGlobal" | `docs/communication/EMAIL_BGLOBAL_*.md` |

---

## Document Priority by Context

### When User Starts New Session

Load in this order:
1. `CLAUDE.md` - Current status, active issues, quick deploy
2. Latest session log - `docs/logs/SESSION_LOG_20260203.md`
3. Specific docs based on user's first request

### When User Asks About Specific Issue

Pattern: `docs/issues/{ISSUE_ID}_*.md` or `docs/investigation/{TOPIC}_*.md`

### When User Wants to Deploy

1. `CLAUDE.md` (Quick Deploy section)
2. Relevant issue checklist
3. `docs/logs/TEST_LOG.md` for verification

### When User Asks "What's the status?"

1. `CLAUDE.md` (Issue Tracker + Go-Live Status)
2. Latest session log

---

## File Path Patterns

| Pattern | Contains |
|---------|----------|
| `docs/investigation/IWQBINTEGRATION_*.md` | IWQBIntegration package analysis (9 docs) |
| `docs/investigation/BGLOBAL_*.md` | BGlobal architecture & patterns |
| `docs/investigation/RPT*_*.md` | Report-specific investigations |
| `docs/investigation/OPTION_*.md` | Implementation options analysis |
| `docs/issues/*.md` | Issue-specific fixes & checklists |
| `docs/logs/SESSION_LOG_*.md` | Daily session logs |
| `docs/reference/*.md` | Catalogs, mappings, technical reference |
| `docs/qb-sync/*.md` | QuickBooks sync documentation |
| `docs/deployment/*.md` | Deployment guides & checklists |
| `docs/communication/*.md` | Emails, summaries, handoffs |
| `source-code/*.cs` | Backend C# code |
| `client-module/*.js` | Frontend JavaScript handlers |
| `vba/*.bas` | Excel VBA macros |
| `sql/*.sql` | SQL scripts & views |

---

## Key Document Relationships

```
CLAUDE.md (entry point)
├── docs/investigation/
│   ├── COMPREHENSIVE_INVESTIGATION_SUMMARY.md (reports overview)
│   ├── BGLOBAL_V7_ARCHITECTURE_COMPLETE.md (V7 system)
│   └── IWQBINTEGRATION_MASTER_CATALOG.md (QB package index)
│       ├── IWQBINTEGRATION_TEAM_INSTRUCTIONS.md (HOW TO)
│       ├── IWQBINTEGRATION_CONFLICT_ASSESSMENT.md (RISKS)
│       ├── IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md (ROOT CAUSES)
│       └── IWQBINTEGRATION_NEXT_STEPS.md (WHAT'S NEXT)
├── docs/reference/
│   ├── MASTER_CATALOG.md (all reports/views)
│   ├── HANDLER_VERSION_HISTORY.md (frontend versions)
│   └── REPORT_FILTER_REQUIREMENTS.md (filter mapping)
├── docs/issues/
│   └── {ISSUE_ID}_*.md (per-issue docs)
└── docs/logs/
    ├── SESSION_LOG_YYYYMMDD.md (daily logs)
    └── IWQBINTEGRATION_INVESTIGATION_LOG.md (package log)
```

---

## Quick Reference: Document by ID

### Issue IDs → Documents

| ID | Primary Document |
|----|------------------|
| RPT-004 | `docs/issues/ITEMS_BY_CUSTOMER_FIX_20260128.md` |
| RPT-005 | `docs/investigation/RPT005_COMPREHENSIVE_REVIEW.md` |
| RPT-006 | `docs/issues/ITEMS_BY_CUSTOMER_FIX_20260128.md` |
| RPT-007 | `docs/issues/ITEMS_BY_CUSTOMER_FIX_20260128.md` |
| RPT-008 | `docs/issues/ITEMS_BY_CUSTOMER_VBA_FIX.md` |
| RPT-009 | `vba/PMPSalesbySalesRep_FIXED_v2.bas` |
| RPT-010 | `source-code/UsrExcelReportService_Updated.cs` |
| UI-006 | `CLAUDE.md` (UI-006 section) |
| UI-007 | `docs/reference/HANDLER_VERSION_HISTORY.md` (v54) |
| SYNC-003 | `docs/qb-sync/SYNC_003_BATCH_PROCESSING.md` |
| SYNC-004 | `CLAUDE.md` (QB Integration section) |
| SYNC-005 | `CLAUDE.md` (SYNC-005 section) |

### Package Names → Documents

| Package | Primary Document |
|---------|------------------|
| IWQBIntegration | `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` |
| BGApp_eykaguu | `docs/reference/HANDLER_VERSION_HISTORY.md` |
| PampaBay | `docs/reference/MASTER_CATALOG.md` |
| IntExcelExport | `docs/investigation/INTEXCELREPORT_COMPLETE_ANALYSIS.md` |

---

## AI Action Guidance

### For Investigation Tasks

1. Load `CLAUDE.md` for context
2. Load specific investigation docs
3. Use Ralph Loop pattern with parallel agents if complex
4. Log findings to `docs/logs/` or `docs/investigation/`

### For Deployment Tasks

1. Load `CLAUDE.md` Quick Deploy section
2. Load relevant checklist/instructions
3. Verify with test commands before confirming
4. Update issue status in `CLAUDE.md` after deploy

### For Documentation Tasks

1. Check existing docs in relevant `docs/` subdirectory
2. Follow established naming patterns
3. Cross-reference in `CLAUDE.md` and related docs
4. Update `AI_NAVIGATION.md` if new category created

### For Debugging Tasks

1. Load `CLAUDE.md` for known issues
2. Check `docs/logs/TEST_LOG.md` for previous results
3. Check session logs for context
4. Document findings in appropriate location

---

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Session logs | `SESSION_LOG_YYYYMMDD.md` | `SESSION_LOG_20260130.md` |
| Issue docs | `{ISSUE_ID}_*.md` | `RPT005_DEPLOYMENT_CHECKLIST.md` |
| Investigation | `{TOPIC}_*.md` | `IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` |
| Handler versions | `*_v{N}_*.js` | `UsrPage_ebkv9e8_v54_FlatObject.js` |
| SQL files | `{ViewName}_*.sql` | `BGCustomerDidNotBuyView_ORIGINAL.sql` |

---

*AI Navigation Guide - Updated 2026-02-05*
