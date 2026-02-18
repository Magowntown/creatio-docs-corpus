# CLAUDE.md - Creatio Reports Fix

> **Status:** ✅ **Reports Complete** | 🟡 **V6 Commission Process (Building)** | 🔴 **IWQBIntegration BLOCKED** | 🎯 **QB Go-Live Ready**
> **Updated:** 2026-02-11 evening | **Latest Log:** `docs/logs/SESSION_LOG_20260210.md` | **Audit:** `docs/investigation/COMMISSION_PROCESS_AUDIT_20260205.md`

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
| V6 Commission Process | `docs/investigation/V6_PROCESS_BUILDER_GUIDE.md` |
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
2. ✅ Check latest session log: `docs/logs/SESSION_LOG_20260203.md`
3. ✅ For deep understanding: Read `docs/SHARED_UNDERSTANDING.md`
4. ✅ Review the pre-deployment checklist: `docs/reference/RISK_CHECKLIST.md`
5. ✅ For complex changes: Enter Plan mode first
6. ✅ Before deploying: Verify with tests

### 🎯 Top Active Tasks (2026-02-11)

| Rank | Task | Priority | Status | Next Action |
|------|------|----------|--------|-------------|
| **1** | **V6 Combined Commission Process** | 🔴 HIGH | Plan Complete | Build in Process Designer → [Builder Guide](docs/investigation/V6_PROCESS_BUILDER_GUIDE.md) |
| **2** | IWQBIntegration PROD Import | 🔴 HIGH | Phase 0 ✅ | Export packages for PROD |
| **3** | QB Go-Live Confirmation | 🟡 HIGH | Ready | Monitor stability, confirm with Carlos |
| **4** | SYNC-005 Reset | 🟢 LOW | Pending | Wait for go-live, then SQL reset |

### 🟡 V6 Commission Process (2026-02-11)

**Plan:** Combine 3 broken processes into 1 combined `IWOrderandPaymentsSync`
**Builder Guide:** `docs/investigation/V6_PROCESS_BUILDER_GUIDE.md`
**Test Script:** `scripts/diagnostics/test_v6_process.py`
**Column Verification:** `scripts/diagnostics/verify_v6_columns.py`

| What | Details |
|------|---------|
| **Replaces** | V4 Calculator + Fill V2 Report Fields + Order Recalc V2 |
| **Signals** | 8 (IWPayments + Order + OrderProduct add/modify/delete) |
| **Paths** | A: Payment calculation, B1: Order→Pending, B2: OrderProduct→Pending, C: Order deleted |
| **Elements** | 36 total (8 signals, 7 reads, 6 changes, 4 gateways, 4 formulas, 7 terminators) |
| **Build order** | Path B1 first (tests ChangeData), then B2, C, A |

**Key Risk:** ChangeData may write null columns (known Creatio 8.3 bug). Path B1 is the canary test — if it writes null, switch to Script Task fallback.

**Test command:** `source .env && python3 scripts/diagnostics/test_v6_process.py`

### 🔴 Commission Process Bugs (2026-02-05 Audit)

**Audit:** `docs/investigation/COMMISSION_PROCESS_AUDIT_20260205.md`
**Steps:** `v3_restructure_steps_labeled.md` (Steps 11-12)

| # | Bug | Process | Fix | Status |
|---|-----|---------|-----|--------|
| 1 | V4 100x recursion | V4 | Remove "Payment Modified" signal (Step 11) | TODO |
| 2 | Fill V2 ↔ V4 ping-pong | Fill V2 + V4 | Remove Fill V2's Payment Modified signal (Step 12) | TODO |
| 3 | Fill V2 Order signal unfiltered | Fill V2 | Remove StartSignal4 from Fill V2 (Step 12) | TODO |
| 4 | V3 IsActiveVersion=True in package | V3 | Disable V3 before any PROD import | PENDING |
| 5 | **Order Recalc V2 never Published** | Order Recalc V2 | Open in Process Designer → **Publish** (not Compile All!) | TODO |
| 6 | Recalculation gap | V4 + Order Recalc V2 | Add Script Task to Order Recalc V2 (Option A) | DESIGN COMPLETE |
| 7 | V3 sets status as TEXT not GUID | V3 | Only matters if V3 activated (keep disabled) | N/A |

**Priority fix order:** 5 → 1 → 2+3 → test → 6

### V4 Commission Process Status (DEV)

| Process | Enabled | Actual | Status | Notes |
|---------|---------|--------|--------|-------|
| **V4** (Payment Calculator) | ✅ | ✅ | 🔴 Recursion bug | Remove "Payment Modified" signal |
| **Fill V2** (Report Fields) | ✅ | ✅ | 🔴 Ping-pong + unfiltered | Remove 2 signals |
| **Order Recalc V2** (Order→Pending) | ✅ | ✅ | 🔴 Never Published | Publish from Process Designer |
| V2 (Current) | ✅ | ❌ | Replaced by V4 | Won't execute |
| V1 (Original) | ✅ | ❌ | Superseded | Won't execute |

**Phase 0 Checklist (DEV Verification): ✅ COMPLETE**
- [x] Verify V2 commission active ✅ **API-VERIFIED 2026-02-05**
- [x] V1 processes not "Actual version" ✅ (V2 is Actual, V1 won't execute)
- [x] V3/V4 not found in DEV ✅ (V4 created during this session)
- [x] **Order Recalc V2 uses filtered trigger** ✅ **BROWSER-VERIFIED 2026-02-05**
  - Signal: "In any of the selected fields" (NOT "In any field")
  - Fields: Amount, Shipping Charge, Sub Total, Tax Amount, Total
- [x] Payment process triggers on IWPayments ✅ **BROWSER-VERIFIED**
- [ ] **Publish Order Recalc V2** from Process Designer (NOT Compile All!)
- [ ] Test commission in DEV (verify single execution) - Manual
- [ ] Export packages for PROD import - Manual

**📋 Key Documents (2026-02-05):**
- ✅ `docs/investigation/COMMISSION_PROCESS_AUDIT_20260205.md` - **4-agent audit results**
- ✅ `v3_restructure_steps_labeled.md` - **Steps 1-12 implementation guide**
- ✅ `docs/investigation/FILTERED_ORDER_TRIGGER_DESIGN.md` - Already implemented as V2
- ✅ `docs/investigation/COMMISSION_CALCULATION_INVESTIGATION.md` - Gap analysis complete

> **Reports work is HANDED OFF** to BGlobal/Rommel. Focus is now 100% on QB Integration.

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

## 📦 IWQBIntegration Package Import (2026-02-03)

**Status:** 🔴 **BLOCKED** - DEV verification required + Missing PROD dependency

### Current Blockers

| # | Blocker | Action Required | Status |
|---|---------|-----------------|--------|
| ~~1~~ | ~~DEV process configuration unverified~~ | ~~Verify V2 active, V3 disabled~~ | ✅ RESOLVED — API-verified 2026-02-05 |
| ~~2~~ | ~~System settings missing~~ | ~~Create IWEnableCommissionV3=false~~ | ✅ NOT NEEDED — V3 doesn't exist in DEV |
| 3 | **IWInterWeavePaymentApp not in PROD** | Export from DEV, import first |

### Package Status

| Package | DEV | PROD | Status |
|---------|-----|------|--------|
| PampaBay | ✅ | ✅ | OK |
| PampaBayQuickBooks | ✅ | ✅ | OK |
| **IWInterWeavePaymentApp** | ✅ | ❌ | **MISSING - Must import first!** |
| IWQBIntegration | ✅ | ❌ | Target (after dependency) |

### Required Steps (In Order)

**Phase 0: DEV Verification** ← CURRENT (API-VERIFIED ✅)
1. ✅ V2 commission processes are ACTIVE and set as Actual version
2. ✅ V1 processes enabled but NOT Actual version (won't execute)
3. ✅ V3/V4 NOT FOUND in DEV (no action needed)
4. [ ] Test commission calculation in DEV (verify single execution)
5. [ ] Export packages

**Phase 1-7: PROD Import** (after Phase 0)
1. Export IWInterWeavePaymentApp from DEV
2. Import to PROD, compile
3. Import IWQBIntegration to PROD
4. Verify V2 is Actual version in PROD
5. Compile and test

### Quick Summary (API-Verified 2026-02-05)

| Finding | Impact |
|---------|--------|
| NO breaking conflicts with UsrExcelReportService | ✅ Safe |
| **V3/V4 NOT FOUND in DEV** | No action needed for V3/V4 |
| **V2 is Actual version** | ✅ V1 won't execute (correct config) |
| **Order Recalc V2 EXISTS** | `IWRecalculateCommissionOnOrderChangeV2` already deployed! |
| Invoice race condition confirmed | Multiple processes write same fields |
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

### Process UIds (API-Verified 2026-02-05)

| Process | UId | Actual Ver | Executes |
|---------|-----|------------|----------|
| IWCalculateCommissiononPayment (V1) | c2623b8a-338e-4adb-afbe-cb76b68368d9 | ❌ | No |
| **IWCalculateCommissiononPaymentV2** | 8cdd4845-4b27-45cd-9907-e9cc478bc3c5 | ✅ | **Yes** |
| IWRecalculateCommissionOnOrderChange (V1) | 04e376c2-3452-4786-88d9-faf096c98ec6 | ❌ | No |
| **IWRecalculateCommissionOnOrderChangeV2** | 3c425afe-3ee8-4d38-baf2-a30de552bd94 | ✅ | **Yes** |

**Note:** V1 processes being "Enabled" doesn't matter - only Actual version executes.

| Setting | Required Value |
|---------|----------------|
| Commission Version | V2 is Actual ✅ |
| Order Recalc V2 | V2 is Actual ✅ |
| IWEnableCommissionV3 | Not needed (V3 doesn't exist) |
| IWEnableCommissionV4 | Not needed (V4 doesn't exist) |

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
14. **Process "Actual version" vs "Enabled" (2026-02-05):** In Creatio, a process can be Enabled but only the one marked as "Actual version" executes. Multiple versions can be Enabled simultaneously - only Actual version matters.
15. **"Publish" ≠ "Compile All" (2026-02-05):** "Publish" from Process Designer generates C# code, compiles, **registers start signals**, and clears NeedUpdate flags. "Compile All" from Configuration only recompiles existing generated code — does NOT generate new code or register signals. A process that was never Published will have NeedUpdateSourceCode=True, NeedUpdateStructure=True, NeedInstall=True and its signals won't fire.
16. **Unfiltered signals are dangerous (2026-02-05):** A signal with `DZ12=[]` (empty NewEntityChangedColumns) fires on ANY field change. Fill V2's Order signal has no filter — fires on every Order modification. Always verify signal column filters via metadata API.
17. **Creatio formula lookup syntax (2026-02-10):** In Process Designer conditional flow formulas, reference lookup values using `[#Lookup.EntityName.DisplayValue.GUID#]` format, NOT `Guid("...")`. Example: `[#Lookup.IW Commission Status.Pending.930bb1c6-ca67-4ac0-8f96-a5ea4018a366#]`. `Guid.Empty` and `||` are both valid.

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
| **V6 process test** | `scripts/diagnostics/test_v6_process.py` |
| **V6 column verify** | `scripts/diagnostics/verify_v6_columns.py` |
| API baseline | `scripts/testing/test_report_service.py` |
| Items by Customer | `scripts/testing/test_items_by_customer.py` |
| Dynamic filters | `scripts/testing/test_commission_dynamic_filters.py` |
| Browser flow | `scripts/investigation/review_report_flow.py` |
| IWQBIntegration | `scripts/investigation/check_iwqb_package.py` |
| QB sync filters | `scripts/investigation/check_qb_sync_process.py` |
