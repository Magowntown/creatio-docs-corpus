# CLAUDE.md - Creatio Reports Fix

> **Status:** ✅ **RPT-009 & RPT-010 FIXED** | 📐 **BGlobal V7 Architecture Documented** | 🎯 **QB Go-Live Ready**
> **Updated:** 2026-02-01 | **Latest Log:** `docs/logs/SESSION_LOG_20260201.md`

---

## 🤖 AI Quick Start

**For any AI assistant:** This section enables quick context loading.

### Navigation Documents

| Document | Purpose |
|----------|---------|
| `docs/AI_NAVIGATION.md` | **Scenario → Document mapping** (use this first) |
| `docs/DOCUMENT_INDEX.md` | **Complete document listing** with relationships |
| `docs/SHARED_UNDERSTANDING.md` | **Complete system knowledge** in one place |
| `CLAUDE.md` | Current status, active issues, quick deploy |

### Scenario Quick Lookup

| User Request Type | Start With |
|-------------------|------------|
| IWQBIntegration / QB Package | `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` |
| Reports / Excel issues | `docs/reference/MASTER_CATALOG.md` |
| Deployment | This file → Quick Deploy section |
| Investigation | `docs/investigation/COMPREHENSIVE_INVESTIGATION_SUMMARY.md` |
| What's the status? | This file → Issue Tracker |

### AI Instructions

1. **Always load `CLAUDE.md` first** for current context
2. **Use `docs/AI_NAVIGATION.md`** to find documents by scenario
3. **Use `docs/DOCUMENT_INDEX.md`** for complete document listing
4. **Follow established patterns** in naming and structure
5. **Update documentation** when creating new docs
6. **Cross-reference** new docs in related existing docs

### 🔴 DEPLOY NOW: RPT-005 Backend Fix

**File:** `source-code/UsrExcelReportService_Updated.cs`
**Changed Methods:**
- `QueryCustomerDidNotBuyData()` - Rewritten with correct ESQ relationship columns
- `CreateReportExecution()` - New helper for Type A pattern
- `QueryCustomerDidNotBuyDataDirect()` - New fallback method

**Deploy URL:** https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178

### 📢 BGlobal V7 Architecture Reference (2026-01-30)

**New Documentation:** Complete understanding of how BGlobal designed V7 reports:
- `docs/investigation/BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` - Full architecture reference
- `docs/investigation/INTEXCELREPORT_COMPLETE_ANALYSIS.md` - All 33 report configurations analyzed
- `sql/BGCustomerDidNotBuyView_ORIGINAL.sql` - Original SQL view definition extracted from PampaBay

---

## 🧠 Workflow (READ THIS FIRST)

**Based on Boris Cherny's Claude Code Method** → Full guide: `docs/reference/CLAUDE_CODE_WORKFLOW.md`

### The Three Pillars

| Pillar | What It Means | How We Do It |
|--------|---------------|--------------|
| **1. Plan First** | Use Plan mode for complex changes. Iterate until plan is solid. | `shift+tab` (x2) to enter Plan mode |
| **2. Verify Always** | Give Claude a way to verify its work = 2-3x quality | Run tests, check browser, use CLI |
| **3. Update CLAUDE.md** | When Claude does something wrong, add correction here | Add to Lessons Learned section |

### Session Start Checklist

1. ✅ Read this CLAUDE.md (you're doing it now)
2. ✅ Check latest session log: `docs/logs/SESSION_LOG_20260201.md`
3. ✅ For deep understanding: Read `docs/SHARED_UNDERSTANDING.md`
4. ✅ For complex changes: Enter Plan mode first
5. ✅ Before deploying: Verify with tests

### Verification Commands

```bash
# API test (primary verification)
source .env && python3 scripts/testing/test_report_service.py

# Specific report test
source .env && CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py

# Browser flow test
python3 scripts/investigation/review_report_flow.py --env dev
```

### When to Use Plan Mode

- ✅ Any handler change (v19.x, v20.x, etc.)
- ✅ Backend service modifications
- ✅ SQL view changes
- ✅ Multi-file changes
- ❌ Simple doc updates
- ❌ Single-line fixes

---

## Quick Navigation

| Need | Go To |
|------|-------|
| **What's happening now** | [Active Issues](#active-issues) |
| **Deploy something** | [Quick Deploy](#quick-deploy) |
| **Run tests** | [Verification Commands](#verification-commands) |
| **Understand the system** | `docs/reference/` |
| **Review session history** | `docs/logs/` |
| **Find issue-specific docs** | `docs/issues/` |

---

## 🎯 QB Integration Go-Live Status

### Current State: ✅ READY (pending confirmation)

| Component | Status | Notes |
|-----------|--------|-------|
| **QB Web Connector** | ✅ Online | Was offline, now syncing |
| **Order Sync (PROD)** | ✅ Working | 336 orders synced successfully |
| **QB Customer Order Integration** | ✅ Deployed | Running in PROD |
| **Commission Sync Process** | ✅ Phase 1 deployed | `BGBPGetQuickBooksCommissions` |

### Blockers Cleared

| Issue | Status | Resolution |
|-------|--------|------------|
| SYNC-004 | ✅ Resolved | QB Web Connector back online |
| Connection timeouts | ✅ Resolved | Server responding |

### Remaining Items (Non-Blocking)

| Item | Priority | Notes |
|------|----------|-------|
| SYNC-005: Reset 637 false "Processed" | Low | Can reset after go-live |
| SYNC-003: 20K batch processing | Low | DEV environment only |
| Commission automation | Future | With Rommel later |

### Go-Live Checklist

- [ ] Confirm QB Web Connector stable (monitor 24-48 hours)
- [ ] Verify order sync completing without errors
- [ ] Set go-live date with Carlos
- [ ] Document any manual steps needed

---

## 📦 IWQBIntegration Package Investigation (2026-01-30)

**Status:** ✅ **INVESTIGATION COMPLETE** - Ready for PROD import with configuration

### Quick Summary

| Finding | Impact |
|---------|--------|
| NO breaking conflicts with UsrExcelReportService | ✅ Safe |
| V3 StartSignal4 causes 26x cascade | Set `IWEnableCommissionV3=false` |
| 4 commission versions exist | Only enable V2 |
| Invoice race condition confirmed | 3 processes write same fields |
| 31 entities (10 extended + 21 created) | Order is CRITICAL |

### Documents (Start Here)

| Document | Purpose |
|----------|---------|
| **[Master Catalog](docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md)** | Complete index of everything |
| **[Team Instructions](docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md)** | Step-by-step import procedure |
| [Investigation Log](docs/logs/IWQBINTEGRATION_INVESTIGATION_LOG.md) | Full timeline |
| [Conflict Assessment](docs/investigation/IWQBINTEGRATION_CONFLICT_ASSESSMENT.md) | Risk analysis |
| [Deep Dive Analysis](docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md) | Root cause of 26x |
| [Consolidated Findings](docs/investigation/IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md) | 6 agent results |
| [Next Steps](docs/investigation/IWQBINTEGRATION_NEXT_STEPS.md) | Recommendations |

### Key Configuration (Before Import)

```sql
-- Verify Order.SalesTax exists (user's concern)
SELECT column_name FROM information_schema.columns
WHERE table_name = 'Order' AND column_name LIKE '%SalesTax%';
```

| Setting | Required Value |
|---------|----------------|
| Commission Version | V2 only (disable V1, V3, V4) |
| Tax Process | V2 only (disable V1) |
| IWEnableCommissionV3 | **false** |
| IWEnableCommissionV4 | **false** |

---

## Active Issues (Reports - HANDED OFF)

> **Note:** Reports work handed to BGlobal/Rommel for v8 rework. Issues below are for reference only.

### 📋 Handed Off to BGlobal

| ID | Issue | Status |
|----|-------|--------|
| RPT-005 | "Customers did not buy" column mismatch | Handed off |
| RPT-006 | "Items by Customer" DESCRIPCION | Handed off |
| HANDLER-002 | "MainDS_Name" resource string | Handed off |
| IW-001 | IW_Commission columns | Handed off |

### 🔴 QB Integration (Our Focus)

| ID | Issue | Action | Doc |
|----|-------|--------|-----|
| **SYNC-005** | 637 orders falsely marked "Processed" | Reset after go-live confirmed | `docs/qb-sync/` |
| **SYNC-003** | QB Customer Order 20K limit (DEV) | Batch processing if needed | `docs/qb-sync/SYNC_003_BATCH_PROCESSING.md` |

### ✅ Recently Resolved

| ID | Issue | Resolution |
|----|-------|------------|
| **RPT-009** | "Sales By Item By Type Of Customer" VBA infinite loop | VBA anchor variable fix (v2) |
| **RPT-010** | "Rpt Sales By Item" showing wrong columns | Backend routing order fix |
| RPT-008 | "Items by Customer" VBA Type mismatch | BGItemsByCustomerView routing |
| RPT-007 | "Items by Customer" 26x duplicate rows | SQL Employee JOIN fix |
| RPT-006 | "Items by Customer" DESCRIPCION wrong | BGProductDescription added |
| UI-007 | Customer ID sent as "value" string | v54 flat object fix |
| UI-006 | PROD infinite loading (v50) | v51 deployed |
| RPT-004 | "Items by Customer" not generating | PROD WORKING (8,814 rows) |
| SYNC-004 | QB Web Connector offline | Resolved - syncing |

<details>
<summary>All Resolved Issues</summary>

| ID | Issue | Resolution |
|----|-------|------------|
| CSP-001 | Looker Studio iframes blocked | UsrIframe Shadow DOM |
| UI-003 | Customer filter missing | v19.13 (BGCustomer) |
| UI-004 | Sales Groups not filtered | v19.13 forced reload |
| LOOKER-002 | Looker reports missing URL params | v19.1 deployed |
| UI-002 | Non-Commission reports wrong filters | v19.1 deployed |
| HANDLER-001 | Hybrid handler (Looker + Excel) | Deployed |
| DL-001/002/003/004 | Download issues | All fixed |
| RPT-001/002/003 | Report config issues | All fixed |
| EARNERS-001 | Brandwise missing earners | 263 created |
| SYNC-001 | QB sync automation | Phase 1 deployed |

</details>

---

## Quick Deploy

### Backend (PROD)

**File:** `source-code/UsrExcelReportService_Updated.cs`
**URL:** https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178

### Frontend (PROD)

**Current:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js`
**URL:** https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2

### Test Commands

```bash
# API tests
source .env && python3 scripts/testing/test_report_service.py
source .env && CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py

# Browser test
python3 scripts/investigation/review_report_flow.py --env dev
```

---

## Documentation Structure

```
docs/
├── AI_NAVIGATION.md  ← **AI QUICK LOOKUP** (scenario → document mapping)
├── DOCUMENT_INDEX.md ← **COMPLETE INDEX** (all documents with relationships)
├── SHARED_UNDERSTANDING.md ← **COMPREHENSIVE REFERENCE** (system knowledge)
│
├── logs/           # Session logs, action logs, test logs
│   ├── SESSION_LOG_20260201.md  ← LATEST
│   ├── SESSION_HISTORY.md       ← Overview
│   ├── TEST_LOG.md              ← All test results
│   └── IWQBINTEGRATION_INVESTIGATION_LOG.md ← **Package investigation**
│
├── issues/         # Issue-specific investigation & fixes
│   ├── RPT005_DEPLOYMENT_CHECKLIST.md
│   ├── ITEMS_BY_CUSTOMER_*.md
│   ├── UI002_*.md
│   └── FUTURE_ISSUES_TRACKING.md
│
├── investigation/  # Deep technical analysis
│   ├── COMPREHENSIVE_INVESTIGATION_SUMMARY.md ← START HERE
│   ├── BGLOBAL_V7_ARCHITECTURE_COMPLETE.md ← Full V7 reference
│   ├── RPT005_COMPREHENSIVE_REVIEW.md      ← Customers Did Not Buy fix
│   ├── BGLOBAL_V7_EXECUTION_PATTERN.md
│   ├── OPTION_A_*.md
│   ├── IWQBINTEGRATION_MASTER_CATALOG.md   ← **IWQBIntegration index**
│   ├── IWQBINTEGRATION_TEAM_INSTRUCTIONS.md ← **Import procedure**
│   ├── IWQBINTEGRATION_CONFLICT_ASSESSMENT.md
│   ├── IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md
│   ├── IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md
│   ├── IWQBINTEGRATION_NEXT_STEPS.md
│   └── IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md
│
├── reference/      # System knowledge & catalogs
│   ├── MASTER_CATALOG.md        ← All reports/views/configs
│   ├── HANDLER_VERSION_HISTORY.md
│   ├── REPORT_FILTER_REQUIREMENTS.md
│   ├── CLAUDE_REFERENCE.md      ← Technical reference
│   └── CLAUDE_CODE_WORKFLOW.md  ← How to work
│
├── deployment/     # Deployment guides & checklists
│   ├── V19_DEPLOYMENT_GUIDE.md
│   └── REPORT_TESTING_CHECKLIST.md
│
├── communication/  # Emails, meeting notes, summaries
│   ├── EMAIL_*.md
│   └── TEAM_SUMMARY_*.md
│
├── qb-sync/        # QuickBooks sync documentation
│   ├── QB_SYNC_AUTOMATION.md
│   └── SYNC_003_BATCH_PROCESSING.md
│
└── archive/        # Older/completed docs
```

---

## Key Files

| Purpose | File |
|---------|------|
| Backend service | `source-code/UsrExcelReportService_Updated.cs` |
| Frontend handler | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js` |
| **VBA Fix (Sales By Item By Type)** | `vba/PMPSalesbySalesRep_FIXED_v2.bas` |
| All handler versions | `docs/reference/HANDLER_VERSION_HISTORY.md` |
| Report/view catalog | `docs/reference/MASTER_CATALOG.md` |
| Filter requirements | `docs/reference/REPORT_FILTER_REQUIREMENTS.md` |

---

## AI Instructions

### Rules

- Credentials in `.env` only (never in logs/docs/commits)
- Log test results to `docs/logs/TEST_LOG.md`
- Update session log daily in `docs/logs/SESSION_LOG_YYYYMMDD.md`
- Hidden iframe is canonical download approach for reports
- Optimize for v8/Freedom UI-first

### Creatio-Specific Rules

- **WCF date format required:** Backend expects `/Date(milliseconds)/` not ISO 8601
- **Customer MUST be LOOKUP:** Never use text input for customer filter
- **One data source per page:** Creatio Freedom UI limitation
- **UsrIframe (not crt.IFrame):** Use for Looker embedding

### Lessons Learned

<details>
<summary>Click to expand lessons learned</summary>

1. **Layered fixes cause new problems:** v20→v21→v22 each introduced new errors. Simpler is better.
2. **IntGenerateExcelReportUserTask EXISTS** (GUID: 05c5265c-3f51-4114-9862-fc434abe1f6d) - BGlobal's original flow.
3. **"Items by Customer" has 0 BGReportExecution records** - NEVER used execution-based pattern (Type A vs Type B).
4. **Parent-driven approach:** Use parent's `LookupAttribute_bsixu8a` dropdown. Parent business rules handle most filter visibility.
5. **Parent lacks Commission filters:** YearMonth and SalesGroup must be inserted by child handler.
6. **WCF date format required:** Backend expects `/Date(milliseconds)/` not ISO 8601.
7. **UsrIframe component (not crt.IFrame):** Use `UsrIframe` from BGlobalLookerStudio package for Looker embedding.
8. **Customer MUST be LOOKUP:** User explicitly rejected text input.
9. **Creatio only supports ONE data source per page:** embeddedModel and modelConfigDiff dataSources may not be officially supported.
10. **ComboBox CANNOT be programmatically populated:** Freedom UI ComboBox requires proper data source binding.
11. **IntName mismatch discovered (2026-01-29):** MASTER_CATALOG has different IntName values than actual database. Always verify via API.
12. **Route by report name FIRST (2026-01-30):** IntEsq rootSchemaName can be wrong (legacy data). Always check report name before entity schema when routing reports.
13. **VBA anchor variable pattern bug (2026-01-30):** BGlobal's nested While loops reset anchor variables inside the loop, causing infinite loops. Fix: move anchor reset BEFORE the While, remove resets inside loop.

</details>

---

## Reference Data

### Status IDs (QB Integration Log)

| Status | GUID |
|--------|------|
| Pending | `c97db3bc-634d-4c90-8432-ec7141c87640` |
| Processed | `e7428193-4cf1-4d1b-abae-00e93ab5e1c5` |
| Error | `bdfc60c7-55fd-4cbd-9a2c-dca2def46d80` |
| Processing | `fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef` |
| Re-Process | `ff92e20c-da27-4255-96bc-57e32f0944f4` |

### Data Pipeline

```
ORDER → QB SYNC → QB INVOICE → QB PAYMENT → COMMISSION REPORT
         ↑           ↑            ↑              ↑
     SYNC-004    SYNC-005    QB Accounting    Working
```

Most missing commission data is due to unpaid invoices in QuickBooks.

---

## Scripts

| Purpose | Script |
|---------|--------|
| API baseline | `scripts/testing/test_report_service.py` |
| Items by Customer | `scripts/testing/test_items_by_customer.py` |
| Dynamic filters | `scripts/testing/test_commission_dynamic_filters.py` |
| Browser flow | `scripts/investigation/review_report_flow.py` |
| IWQBIntegration | `scripts/investigation/check_iwqb_package.py` |
| QB sync filters | `scripts/investigation/check_qb_sync_process.py` |
