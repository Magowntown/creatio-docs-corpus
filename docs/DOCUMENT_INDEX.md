# Document Index

**Purpose:** Complete listing of all documentation with descriptions and relationships.
**Updated:** 2026-02-01
**Total Documents:** 112

---

## Entry Points (Start Here)

| Document | When to Use |
|----------|-------------|
| `CLAUDE.md` | **Always start here** - Current status, active issues, quick deploy |
| `docs/AI_NAVIGATION.md` | Scenario-based document lookup for AI assistants |
| `docs/DOCUMENT_INDEX.md` | This index - complete document listing |

---

## Investigation Documents

### IWQBIntegration Package (9 documents)

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `IWQBINTEGRATION_SUMMARY.md` | TL;DR | Quick overview, verdict, key findings |
| `IWQBINTEGRATION_MASTER_CATALOG.md` | **Complete Index** | 31 entities, 11 processes, 5 risks, all columns |
| `IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` | **Step-by-Step** | Import procedure with sign-off checklist |
| `IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md` | 13-Phase Checklist | Detailed verification queries, tests |
| `IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` | Risk Analysis | 5 critical risks, mitigation strategies |
| `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` | Root Causes | 26x cascade, race condition, version comparison |
| `IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md` | Agent Results | 6 parallel investigation findings |
| `IWQBINTEGRATION_NEXT_STEPS.md` | Recommendations | 5 improvements, suggested investigations |
| `IWQBINTEGRATION_INVESTIGATION_LOG.md` | Timeline | Full investigation methodology and status |

**Relationships:**
```
IWQBINTEGRATION_SUMMARY.md (quick read)
    └── IWQBINTEGRATION_MASTER_CATALOG.md (comprehensive index)
        ├── IWQBINTEGRATION_TEAM_INSTRUCTIONS.md (how to import)
        ├── IWQBINTEGRATION_CONFLICT_ASSESSMENT.md (risks)
        ├── IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md (root causes)
        └── IWQBINTEGRATION_NEXT_STEPS.md (what's next)
```

### BGlobal Architecture (4 documents)

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` | **Full Reference** | V7 execution patterns, entity relationships |
| `BGLOBAL_V7_EXECUTION_PATTERN.md` | Execution Flow | How reports execute in V7 |
| `INTEXCELREPORT_COMPLETE_ANALYSIS.md` | Report Configs | All 33 IntExcelReport records analyzed |
| `COMPREHENSIVE_INVESTIGATION_SUMMARY.md` | Investigation Overview | Summary of all report investigations |

### Report-Specific Investigations

| Document | Issue | Key Content |
|----------|-------|-------------|
| `RPT005_COMPREHENSIVE_REVIEW.md` | Customers Did Not Buy | Column mismatch analysis, fix strategy |
| `OPTION_A_IMPLEMENTATION_PLAN.md` | RPT-006 fix | Add BGProductDescription column |
| `OPTION_A_ENVIRONMENT_IMPACT.md` | RPT-006 impact | Risk assessment for Option A |

---

## Reference Documents

### Catalogs & Mappings

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `MASTER_CATALOG.md` | **All Reports/Views** | 33 reports, SQL views, configurations |
| `HANDLER_VERSION_HISTORY.md` | Frontend Versions | v1 through v54, what each changed |
| `REPORT_FILTER_REQUIREMENTS.md` | Filter Mapping | Which filters each report needs |
| `CLAUDE_REFERENCE.md` | Technical Reference | Creatio patterns, Freedom UI, ESQ |

### Workflow & Best Practices

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `CLAUDE_CODE_WORKFLOW.md` | How to Work | Boris Cherny method, Plan mode |

---

## Issue Documents

### Report Issues

| Document | Issues | Key Content |
|----------|--------|-------------|
| `RPT005_DEPLOYMENT_CHECKLIST.md` | RPT-005 | Deployment steps for Customers Did Not Buy |
| `RPT009_VBA_INFINITE_LOOP_FIX.md` | RPT-009 | VBA anchor variable fix for Sales By Item |
| `RPT010_ROUTING_ORDER_FIX.md` | RPT-010 | Backend routing order fix |
| `ITEMS_BY_CUSTOMER_FIX_20260128.md` | RPT-004,006,007 | Items by Customer comprehensive fix |
| `ITEMS_BY_CUSTOMER_VBA_FIX.md` | RPT-008 | VBA Type mismatch fix |
| `ITEMS_BY_CUSTOMER_COLUMN_INVESTIGATION.md` | RPT-006 | DESCRIPCION column investigation |

### Future Issues

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `FUTURE_ISSUES_TRACKING.md` | Backlog | Non-critical issues for later |

---

## Log Documents

### Session Logs

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `SESSION_LOG_20260201.md` | **Latest** | Comprehensive audit & shared understanding |
| `SESSION_LOG_20260130.md` | Previous | RPT-009/010 fixes, VBA fix |
| `SESSION_LOG_20260129.md` | Earlier | Report investigations |
| `SESSION_LOG_20260128.md` | Earlier | Items by Customer fixes |
| `SESSION_HISTORY.md` | Overview | Summary of all sessions |

### Other Logs

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `TEST_LOG.md` | Test Results | All API and browser test results |
| `IWQBINTEGRATION_INVESTIGATION_LOG.md` | Investigation Log | IWQBIntegration timeline |

---

## Deployment Documents

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `V19_DEPLOYMENT_GUIDE.md` | v19 Deploy | Handler v19 deployment steps |
| `REPORT_TESTING_CHECKLIST.md` | Testing | Post-deployment verification |

---

## Communication Documents

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `HANDOFF_E6SOLUTIONS.md` | Handoff | e6solutions team handoff doc |
| `EMAIL_BGLOBAL_REPORT_ISSUES.md` | Email Draft | BGlobal communication |
| `TEAM_SUMMARY_20260120.md` | Summary | Team status summary |

---

## QB Sync Documents

| Document | Purpose | Key Content |
|----------|---------|-------------|
| `QB_SYNC_AUTOMATION.md` | Sync Process | Commission sync automation |
| `QB_SYNC_INFRASTRUCTURE_ISSUE.md` | SYNC-004 | QB Web Connector offline issue |
| `SYNC_003_BATCH_PROCESSING.md` | SYNC-003 | Batch processing for large datasets (20K limit) |
| `COMMISSION_DATA_PIPELINE_ANALYSIS.md` | Pipeline | Full commission data flow analysis |
| `QB_TEAM_ACTION_REQUIRED.md` | Team Actions | Required actions for QB team |
| `IWQBINTEGRATION_CONSOLIDATION_PLAN.md` | Integration | IWQBIntegration consolidation strategy |

---

## Source Code Files

### Backend

| File | Purpose | Key Content |
|------|---------|-------------|
| `source-code/UsrExcelReportService_Updated.cs` | **Main Handler** | Report generation service |
| `source-code/UsrExcelReportService_ROLLBACK.cs` | Rollback | Previous version for rollback |

### Frontend

| File | Purpose | Key Content |
|------|---------|-------------|
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js` | **Current PROD** | v54 handler |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v51_StableDialog.js` | Stable Version | v51 with dialog pattern |
| `client-module/*.js` | All Versions | v19-v54 handler history |

### VBA

| File | Purpose | Key Content |
|------|---------|-------------|
| `vba/PMPSalesbySalesRep_FIXED_v2.bas` | VBA Fix | Infinite loop fix for Sales By Item |

### SQL

| File | Purpose | Key Content |
|------|---------|-------------|
| `sql/BGCustomerDidNotBuyView_ORIGINAL.sql` | View Definition | Original view from PampaBay |
| `sql/*.sql` | SQL Scripts | Various SQL scripts and views |

---

## Working Files

| Directory | Purpose |
|-----------|---------|
| `investigation/IWQBIntegration/` | Extracted package contents |
| `investigation/IWQBIntegration/full_content.txt` | Package strings |
| `investigation/IWQBIntegration/file_list.txt` | Package manifest |

---

## Document Naming Conventions

| Pattern | Meaning | Example |
|---------|---------|---------|
| `SESSION_LOG_YYYYMMDD.md` | Daily session log | `SESSION_LOG_20260130.md` |
| `{ISSUEID}_*.md` | Issue-specific doc | `RPT005_DEPLOYMENT_CHECKLIST.md` |
| `IWQBINTEGRATION_*.md` | IWQBIntegration docs | `IWQBINTEGRATION_MASTER_CATALOG.md` |
| `BGLOBAL_*.md` | BGlobal architecture | `BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` |
| `*_v{N}_*.js` | Handler version | `UsrPage_ebkv9e8_v54_FlatObject.js` |
| `EMAIL_*.md` | Email drafts | `EMAIL_BGLOBAL_REPORT_ISSUES.md` |

---

## Cross-Reference: Topic → Documents

| Topic | Primary Doc | Supporting Docs |
|-------|-------------|-----------------|
| **IWQBIntegration** | `IWQBINTEGRATION_MASTER_CATALOG.md` | All `IWQBINTEGRATION_*.md` |
| **Reports (general)** | `MASTER_CATALOG.md` | `REPORT_FILTER_REQUIREMENTS.md` |
| **V7 Architecture** | `BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` | `INTEXCELREPORT_COMPLETE_ANALYSIS.md` |
| **Commission** | `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` | `QB_SYNC_AUTOMATION.md` |
| **Frontend** | `HANDLER_VERSION_HISTORY.md` | `client-module/*.js` |
| **Backend** | `source-code/UsrExcelReportService_Updated.cs` | `BGLOBAL_V7_EXECUTION_PATTERN.md` |
| **QB Sync** | `QB_SYNC_AUTOMATION.md` | `SYNC_003_BATCH_PROCESSING.md` |

---

## Update Log

| Date | Change |
|------|--------|
| 2026-02-01 | Comprehensive audit, added SESSION_LOG_20260201, SHARED_UNDERSTANDING.md |
| 2026-02-01 | Added RPT009, RPT010 issue docs; QB sync docs |
| 2026-01-30 | Added IWQBIntegration docs (9), AI_NAVIGATION.md, DOCUMENT_INDEX.md |
| 2026-01-30 | Added BGLOBAL_V7_ARCHITECTURE_COMPLETE.md |
| 2026-01-29 | Added RPT005 docs |
| 2026-01-28 | Added ITEMS_BY_CUSTOMER docs |

---

*Document Index - Updated 2026-02-01*
