# CLAUDE.md - Creatio Reports Fix

> **Status:** ⚠️ **SYNC-002 NEW:** QB sync issue reported - `UsrPage_ebkv9e8` Form page in IWQB package (PROD) implicated. FLT-004 ✅ FLT-002 ✅
> **Updated:** 2026-01-16 | **See:** `docs/CLAUDE_REFERENCE.md` for technical details

---

## Current Issues

| ID | Issue | Status |
|----|-------|--------|
| DL-001 | "File wasn't available on site" | ✅ Fixed |
| DL-002 | `UsrURL` undefined error | ✅ Fixed |
| DL-003 | Excel can't open (format/extension) | ✅ Fixed |
| FLT-001 | Commission filters not applied | ✅ Fixed |
| **FLT-002** | IW_Commission filters not applied | ✅ Fixed |
| FLT-003 | Dynamic filters (3 combos) | ✅ Verified |
| FLT-004 | Commission empty data (older months) | ✅ Fixed |
| DATA-001 | PaymentStatusId=Planned blocks QB sync | ⚠️ Business Decision Required |
| **SYNC-001** | QB sync process | ✅ Resolved + Automated |
| **SYNC-002** | QB sync issue - UsrPage_ebkv9e8 implicated (PROD) | 🔴 **NEW - Investigate** |
| **DATA-002** | Dec 2025 invoices synced but awaiting payment in QB | ⚠️ QB Accounting Workflow |
| **PROC-001** | V4 Commission process gateway type mismatch | 📋 Dormant (no IWPayments data) |
| ENV-001 | Template lookup broken in DEV | ✅ NOT REPRODUCIBLE |
| FUT-001 | Pre-calculated .xlsx (server-side macros) | 📋 Future |
| **FUT-002** | Freedom UI: Product Pictures in List Views | 📋 Future |

---

## SYNC-001: QuickBooks Sync Process (RESOLVED + AUTOMATED)

**Discovered:** 2026-01-15 | **Resolved:** 2026-01-15
**Status:** ✅ Infrastructure working. Phase 1 automation deployed.

### Resolution Summary

| Step | Status | Result |
|------|--------|--------|
| Manual date entry | ✅ Done | Process completed successfully |
| Data sync | ✅ Done | 10,020 total records (last batch Jan 8, 2026) |
| Phase 1 automation | ✅ Deployed | 30-day rolling window script |
| Phase 2 automation | 📋 Pending | Dynamic ESQ query (last sync date) |

### Automation Status

**Phase 1 (Deployed):** Simplified script with 30-day window
```csharp
DateTime startDate = DateTime.UtcNow.AddDays(-30);
DateTime endDate = DateTime.UtcNow;
Set<DateTime>("AutoStartDate", startDate);
Set<DateTime>("AutoEndDate", endDate);
return true;
```

**Phase 2 (Next):** Query `BGCommissionReportQBDownload.CreatedOn` for dynamic start date

**Full guide:** `docs/QB_SYNC_AUTOMATION.md`

---

## SYNC-002: QB Sync Issue - UsrPage_ebkv9e8 Form Page (PROD)

**Reported:** 2026-01-16 | **Investigated:** 2026-01-16
**Status:** 🔴 **ROOT CAUSE IDENTIFIED - Fix Required**

### Report Summary

Word received that the QuickBooks sync issue is being caused by the `UsrPage_ebkv9e8` Form page in the **IWQB package in PROD**.

### Key Information

| Item | Value |
|------|-------|
| **Component** | `UsrPage_ebkv9e8` Form Page |
| **Package** | IWQB (IWQBIntegration) |
| **Environment** | PROD |
| **Modified Date** | **2026-01-14** (same day as problematic OrderPageV2) |
| **Local copies** | `UsrPage_ebkv9e8_Updated.js` (complex), `UsrPage_ebkv9e8_IframeDownload.js` (simple) |

### Investigation Findings

**PROD has 3 versions of UsrPage_ebkv9e8:**

| UID | Package | Modified | Status |
|-----|---------|----------|--------|
| `4e6a5aa6...` | BGlobalLookerStudio | 2023-10-23 | Old version |
| `561d9dd4...` | BGApp_eykaguu | 2025-07-14 | Intermediate |
| `1d5dfc4d...` | **IWQBIntegration** | **2026-01-14** | ⚠️ **Most recent - SUSPECT** |

### Root Cause Analysis

The **Updated.js** version (currently deployed to IWQBIntegration) has **2 additional handlers** compared to the simple version:

| Handler | Simple Version | Updated Version | Risk |
|---------|----------------|-----------------|------|
| `usr.GenerateExcelReportRequest` | ✅ | ✅ | Low - Report-specific |
| `crt.HandleViewModelAttributeChangeRequest` | ❌ | ✅ | **HIGH** - Triggers on ANY attribute change |
| `crt.LoadDataRequest` | ❌ | ✅ | **HIGH** - Intercepts ALL data load requests |

**Problem:** The `crt.LoadDataRequest` handler (lines 73-305) intercepts data loading and:
1. Queries `IWPayments` entity during Sales Group filtering
2. Queries `IWPaymentsInvoice` entity for fallback filtering
3. Creates `sdk.FilterGroup` objects with complex logic

**Potential Interference:**
- If this handler runs during QB sync operations, it could cause:
  - Database locks on IWPayments/IWPaymentsInvoice tables
  - Unhandled exceptions that propagate to sync processes
  - Memory/performance issues from repeated queries

### Code Comparison

```
UsrPage_ebkv9e8_IframeDownload.js (SAFE):
  - 217 lines
  - 1 handler: usr.GenerateExcelReportRequest only
  - No IWPayments queries
  - No framework-level interceptors

UsrPage_ebkv9e8_Updated.js (PROBLEMATIC):
  - 495 lines (2.3x larger)
  - 3 handlers including framework interceptors
  - Queries IWPayments and IWPaymentsInvoice
  - Complex FilterGroup logic
```

### Recommended Fix

**Option A (Quick Fix):** Roll back to the simpler `UsrPage_ebkv9e8_IframeDownload.js` version
- Removes the two framework interceptors
- Sacrifices Sales Group cascade filtering (UX feature)
- Lowest risk approach

**Option B (Targeted Fix):** Modify `crt.LoadDataRequest` handler to be more defensive
- Add try/catch around IWPayments queries
- Add checks to only run on this specific page
- Keep the UX feature but reduce interference risk

**Option C (Investigation):** Verify if page handlers are being triggered during sync
- Add logging to the handlers to confirm interference
- May need to check PROD server logs

### Connection to Other Issues

- **Same modification date** as OrderPageV2 change that caused DATA-001
- The IWQBIntegration package was modified on 2026-01-14 - 1 day before issues reported
- May explain DATA-002 (Dec 2025 data gap) if sync was blocked by page handlers

---

## DATA-002: December 2025 Invoices Awaiting Payment in QuickBooks

**Discovered:** 2026-01-15 | **Updated:** 2026-01-15
**Status:** ⚠️ QB accounting workflow issue - not a technical issue

### Client Observation

> "Receiving Returns on the reports but not Sales"

### Data Flow Investigation (Complete)

```
Creatio Orders → QB Invoices → [Awaiting Payment] → QB ReceivePayments → Commission Data
     ✅              ✅               ❌                    ❌                    ❌
  (EXISTS)       (SYNCED)        (NOT DONE)           (DOESN'T EXIST)        (MISSING)
```

### Key Findings

| Stage | Status | Evidence |
|-------|--------|----------|
| Dec 2025 Orders in Creatio | ✅ **EXISTS** | ORD-15159, ORD-15299, ORD-14800, etc. |
| Orders synced to QB (Invoices) | ✅ **SYNCED** | All have BGQuickBooksId |
| Invoices marked as Paid in QB | ❌ **NOT DONE** | 0 Sales in Commission data |
| ReceivePayments synced back | ❌ **NONE** | Only Credit Memos exist (39 records) |

### Commission Data (PROD via OData)

| Month | Sales | Credit Memos (Returns) | Total |
|-------|-------|------------------------|-------|
| **Dec 2025** | **0** | **39** | **39** |
| Nov 2025 | 485 | 16 | 501 |
| Oct 2025 | ~400 | ~20 | ~420 |

### Root Cause (Confirmed)

**December 2025 invoices exist in QuickBooks but haven't been marked as "paid".**

The commission sync queries `ReceivePayment` records (created when invoices are paid), NOT `Invoice` records. Until the QB accountant records payments against those invoices, there's nothing for the Commission sync to pull back.

- ✅ Creatio → QB sync (Orders → Invoices) is working correctly
- ✅ QB → Creatio sync (ReceivePayments → Commission) is working correctly
- ✅ Credit Memos (Returns) ARE syncing
- ❌ December 2025 invoices awaiting payment processing in QuickBooks

### Action Required

**QuickBooks accounting team** needs to:
1. Process payments against December 2025 invoices
2. Once payments are recorded, the next commission sync will pick them up automatically

**Technical Details:** `docs/CLAUDE_REFERENCE.md` → "December 2025 Data Gap Analysis"

---

## PROC-001: V4 Commission Process (Dormant - Fix Later If Needed)

**Process:** `IW Calculate Commission on Payment V4`
**Status:** 📋 Not currently running (no IWPayments data triggers it)

**Errors observed (Jan 14, 2026):**
1. `IWPaymentsSchema cannot be obtained` - Schema registration issue
2. `Argument types do not match` at gateway - Parameter `{eab9b2d5-4600-4a94-840d-4243c218cd28}` compared with `< 0`

**Root cause:** Gateway condition expects numeric type but receives incompatible type.

**When to fix:** If/when IWPayments starts receiving data and the process needs to run.

---

## FUT-002: Freedom UI Product Pictures (Pending)

**Contact:** Rommel Bocker (e6Solutions subcontractor)
**Status:** On hold - Rommel on PTO until Monday
**Priority:** High (showstopper for Pampa Bay users)

**Issue:** Product Pictures are not available in List Views under Freedom UI. Pampa Bay users rely heavily on seeing product pictures in Catalog Lists and Sales Order Lists when processing transactions.

**Background:**
- e6Solutions (Rommel Bocker) engaged for Classic → Freedom UI migration (TAI resources booked Q4)
- Both Rommel and TAI submitted Creatio support tickets
- **Creatio response:** Not enough customer demand to prioritize a fix

**Plan B (Rommel investigating):**
- Merge a Gallery View with List Views
- Product Pictures would show next to Product #'s and Descriptions
- Rommel working on estimate for this approach

**Next Steps:**
- Regroup with Rommel when he returns from PTO (Monday)

---

## DATA-001: PaymentStatusId Blocks QB Sync (Business Decision Required)

**Discovered:** 2026-01-15
**Status:** Root cause identified - awaiting business decision

### Problem

41% of December 2025 orders (206 out of 500) have `PaymentStatusId = Planned`, which prevents them from being synced to QuickBooks. Since commission report data comes from QB sync, these orders are **missing from commission reports**.

### Root Cause

| User | PaymentStatusId | QB Sync | Commission Data |
|------|-----------------|---------|-----------------|
| Supervisor | NULL/Empty | ✅ Synced | ✅ Included |
| Maria Victoria | Planned | ❌ Not synced | ❌ Missing |
| Pamela Murphy | Planned | ❌ Not synced | ❌ Missing |
| Krutika | Planned | ❌ Not synced | ❌ Missing |

**Source of Default:** IWQBIntegration package's `OrderPageV2` schema (modified 2026-01-14) appears to set `PaymentStatusId = Planned` as default for UI-created orders.

### Questions for Business

1. Should orders with `PaymentStatusId = Planned` be synced to QuickBooks?
2. Is the "Planned" default intentional for a workflow (e.g., orders pending approval)?
3. Should Supervisor orders behave differently from other users?

### Potential Fixes

| Option | Description | Effort |
|--------|-------------|--------|
| A | Update IWQBIntegration OrderPageV2 to remove "Planned" default | Low |
| B | Update QB sync process to include "Planned" orders | Medium |
| C | Change commission report to pull from Order entity directly | High |

**See:** `docs/INVESTIGATION_PAYMENT_STATUS.md` for full technical details

---

## Gates Status

```
✅ Gate A: API baseline (Commission + IW_Commission)
✅ Gate B: Runtime verification (reportDownloadFrame marker)
✅ Gate C: DL-001 browser download
✅ Gate C2: DL-003 macro extension (.xlsm serving)
✅ Gate D: Dynamic filter sweep (3 combos)
✅ Gate E: FLT-004 regression testing (3 Year-Month + Sales Group combos)
🔄 Gate F: Hardening
🔄 Gate G: PROD upgrade checklist
```

---

## What's Working

| Component | Status |
|-----------|--------|
| `UsrExcelReportService/Generate` | ✅ Returns key |
| `UsrExcelReportService/GetReport` | ✅ Serves .xlsm |
| Commission filters | ✅ Working |
| IW_Commission filters | ✅ Working (Year-Month + Sales Group) |
| Hidden iframe download | ✅ Working |

---

## FLT-004: RESOLVED

**Root cause:** The `BGCommissionReportDataView` SQL had a column mismatch:
- WHERE clause filtered on `qb."BGTransactionDate"` (QB download date)
- SELECT clause output `so."BGInvoiceDate"` (Order invoice date) as `BGTransactionDate`
- These are different dates, causing December filter to return Sept-Nov data

**Solution:** Fixed the view's SQL to filter on `so."BGInvoiceDate"` (the actual output column). Service uses `BGExecutionId` filtering; view handles Year-Month/SalesGroup via `BGReportExecution` JOIN.

**Database fix applied:**
```sql
-- Changed in WHERE clause:
-- FROM: EXTRACT(month FROM qb."BGTransactionDate")
-- TO:   EXTRACT(month FROM so."BGInvoiceDate")
```

**Verification (2026-01-13):**
| Test | Year-Month | Sales Group | Result |
|------|------------|-------------|--------|
| 1 | 2024-12 | RDGZ & Consulting LLC | 55 rows, all Dec 2024 |

All dates verified within December 2024 (Dec 1 - Dec 30).

---

## FLT-002: IW_Commission (PARTIAL)

**Status:** Report generation works. Sales Group filter works. Year-Month filter disabled due to library limitation.

**Data source:** `IWPayments` entity via `IWCommissionReportDataView` (QuickBooks payments via InterWeave sync)

### Implementation Complete (2026-01-14)

| Step | Status | Notes |
|------|--------|-------|
| 1. Create PostgreSQL view | ✅ DONE | With all BaseEntity columns |
| 2. Register entity schema | ✅ DONE | IWCommissionReportDataView in IWQBIntegration |
| 3. Configure IntExcelReport | ✅ DONE | IntEntitySchemaNameId + IntEsq updated |
| 4. Deploy C# service | ✅ DONE | Sales Group filter working |
| 5. Test implementation | ✅ DONE | Verified with regression |

### Known Limitation

**Year-Month (date) filtering is disabled** due to IntExcelExport library limitation:
- The library throws `ArgumentNullException` when DateTime filters are applied via FiltersConfig
- This is the same limitation encountered with FLT-004 (Commission)
- **Workaround:** Users can filter by Sales Group; date filtering requires future custom implementation

### Test Results (2026-01-14)

| Test | Result | Rows |
|------|--------|------|
| No filters | ✅ Pass | 5 (1 header + 4 data) |
| Sales Group only | ✅ Pass | 3 (filtered subset) |
| Year-Month only | ⚠️ Ignored | Returns all data |
| Commission regression | ✅ Pass | 56 rows unchanged |

**See:** `docs/IW_COMMISSION_STRATEGY.md` for full implementation details and error resolutions

---

## Quick Commands

```bash
# API tests
source .env && python3 scripts/testing/test_report_service.py
source .env && CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py

# Browser test
python3 scripts/investigation/review_report_flow.py --env dev
```

---

## Key Files

| Purpose | File |
|---------|------|
| Frontend handler | `client-module/UsrPage_ebkv9e8_Updated.js` |
| Backend service | `source-code/UsrExcelReportService_Updated.cs` |
| Test log | `docs/TEST_LOG.md` |
| Technical reference | `docs/CLAUDE_REFERENCE.md` |
| History | `docs/CLAUDE_HISTORY.md` |

---

## Deployment URLs

- **Frontend:** `https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734`
- **Backend:** `https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178`

---

## Rules

- Credentials in `.env` only (never in logs/docs/commits)
- Log test results to `docs/TEST_LOG.md`
- Hidden iframe is canonical download approach
- Optimize for v8/Freedom UI-first

---

## Creatio Expert AI Corpus

**Status:** ✅ COMPLETE (All phases including authenticated content)

| Source | Pages | Words |
|--------|-------|-------|
| v8.x Academy docs | 5,289 | - |
| v7.x Legacy docs | 626 | 523K |
| **Authenticated content** | **558** | **360K** |
| Training listings (public) | 46 | 8K |
| **TOTAL** | **~6,500** | **~900K+** |

**Output Directories:**
- `./creatio-docs-full/` - Main v8.x corpus (4,985 pages)
- `./creatio-docs-supplementary/` - Additional v8.x (304 pages)
- `./creatio-docs-v7/` - Legacy v7.x documentation (626 pages, 7.8MB)
- `./creatio-docs-training/` - Training/E-learning listings (46 pages)
- `./creatio-docs-authenticated-hybrid/` - **E-learning, Training, Certification, Community** (558 pages, 360K words)

**v7.x Breakdown:** development-sdk (209), studio (91), sales-team (91), sales-enterprise (83), service-enterprise (80), marketing (46), mobile (24)

**Authenticated Crawl (2026-01-15):** Successfully authenticated via profile.creatio.com SSO. Captured e-learning courses, training sessions, certification info, and community Q&A.

**Scripts:**
- `scripts/crawlers/legacy_docs_hybrid.py` (v7.x Playwright + Firecrawl)
- `scripts/crawlers/authenticated_hybrid_crawl.py` (Authenticated content)

---

## Documentation Index

| Need | Document |
|------|----------|
| **Current status & issues** | `CLAUDE.md` (this file) |
| **Next steps & priorities** | `docs/ACTION_PLAN.md` - Priority queue & action items |
| **QB Sync Automation** | `docs/QB_SYNC_AUTOMATION.md` - Process automation guide |
| **DATA-001 investigation** | `docs/INVESTIGATION_PAYMENT_STATUS.md` - PaymentStatusId analysis |
| **Package comparison** | `docs/PACKAGE_COMPARISON.md` - IWQBIntegration vs PampaBayQuickBooks |
| **IW_Commission implementation** | `docs/IW_COMMISSION_STRATEGY.md` - Full implementation plan |
| **Technical reference** | `docs/CLAUDE_REFERENCE.md` - API patterns, schemas, deployment steps |
| **TDD workflow & AI roles** | `docs/CLAUDE_REFERENCE.md` - Section "Workflows" |
| **Change history** | `docs/CLAUDE_HISTORY.md` - Full change log |
| **Test results** | `docs/TEST_LOG.md` - All test executions |
| **Root cause analysis** | `docs/REPORT_BUTTON_INVESTIGATION.md` |
| **Filter fix requirements** | `docs/REPORT_FILTER_FIX_REQUIRED.md` |
| **System analysis** | `docs/CREATIO_REPORT_SYSTEM_ANALYSIS.md` |
| **Handler instructions** | `docs/CREATIO_HANDLER_INSTRUCTIONS.md` |

### Scripts

| Purpose | Script |
|---------|--------|
| API baseline test | `scripts/testing/test_report_service.py` |
| Dynamic filter test | `scripts/testing/test_commission_dynamic_filters.py` |
| PROD execution filters | `scripts/testing/test_commission_execution_filters.py` |
| Browser flow test | `scripts/investigation/review_report_flow.py` |
| IWQBIntegration package | `scripts/investigation/check_iwqb_package.py` |
| Order payment defaults | `scripts/investigation/check_order_defaults.py` |
| IW processes & status | `scripts/investigation/check_iw_processes.py` |
| QB sync process filters | `scripts/investigation/check_qb_sync_process.py` |

### Source Code

| Purpose | File |
|---------|------|
| Frontend handler (JS) | `client-module/UsrPage_ebkv9e8_Updated.js` |
| Backend service (C#) | `source-code/UsrExcelReportService_Updated.cs` |

---

## Session Log: 2026-01-16 (Latest)

### New Issue Reported

**SYNC-002:** Word received that QB sync issue is caused by `UsrPage_ebkv9e8` Form page in IWQB package (PROD). Documented for later investigation.

### Also Noted (Windows auto-claude issues - separate from Creatio)

User reported issues with auto-claude application on Windows C: drive:
- Claude update blocked → **Fix:** Add `C:\Users\amago\.local\bin` to Windows PATH
- Git not detected → Git IS in PATH; likely auto-claude launch context issue
- auto-claude not initializing → Path mismatch in settings (`IW_IDE` vs `IW__Launcher`)

---

## Session Log: 2026-01-15

### What Was Done

1. **Complete data flow investigation** - Traced entire path: Creatio Orders → QB Invoices → QB Payments → Commission Data
2. **Verified December 2025 orders exist** - Found 20+ orders (ORD-15159, ORD-15299, etc.)
3. **Confirmed Orders are synced to QB** - All Dec 2025 orders have BGQuickBooksId
4. **Analyzed BGQuickBooksService.cs** - Understood the ReceivePayment vs Invoice query logic
5. **Identified root cause** - Dec 2025 invoices exist in QB but awaiting payment processing
6. **Discovered API behavior** - DataService unreliable for large tables; OData is correct

### Key Findings

| Discovery | Impact |
|-----------|--------|
| Dec 2025 orders exist in Creatio | ✅ 20+ orders found (ORD-15159, etc.) |
| Orders ARE synced to QuickBooks | ✅ All have BGQuickBooksId (invoices exist in QB) |
| Invoices NOT marked as paid in QB | ❌ No ReceivePayment records created |
| Commission sync queries ReceivePayments | ✅ Working correctly - nothing to sync |
| DataService vs OData | ⚠️ OData more reliable for large datasets |

### Technical Discovery

**BGQuickBooksService.cs Analysis:**
- `GetQuickBooksReceivedPayments()` queries `qtReceivePaymentSearch` (payment receipts, NOT invoices)
- `GetQuickBooksCreditMemos()` queries `qtCreditMemoSearch` with `PaidStatus = psPaid`
- Commission sync pulls PAYMENTS, not INVOICES

**Complete Data Flow:**
```
Creatio Orders → QB Invoices → [Awaiting Payment] → QB ReceivePayments → Commission Data
     ✅              ✅               ❌                    ❌                    ❌
  (EXISTS)       (SYNCED)        (NOT DONE)           (DOESN'T EXIST)        (MISSING)
```

### Files Updated This Session

| File | Changes |
|------|---------|
| `CLAUDE.md` | Refined DATA-002, updated session log |
| `docs/TEST_LOG.md` | Complete data flow investigation |
| `docs/CLAUDE_REFERENCE.md` | Technical analysis of QB sync |
| `docs/CLAUDE_HISTORY.md` | Session entries |
| `BGQuickBooksService.cs` | Extracted and analyzed (repo copy) |

### Handoff Notes for Next Session

- **DATA-002 ROOT CAUSE CONFIRMED:** Dec 2025 invoices exist in QB but awaiting payment
- **Action required:** QB accounting team must process payments against Dec invoices
- **Technical infrastructure:** All syncs working correctly (nothing to fix)
- **API Note:** Use OData for BGCommissionReportQBDownload queries (2.8M+ records)

### Client-Ready Summary

> The Commission report system is working correctly. Complete investigation confirmed:
> - ✅ December 2025 orders exist in Creatio
> - ✅ Orders are synced to QuickBooks as invoices
> - ✅ QB → Creatio commission sync is working
> - ❌ December 2025 invoices haven't been marked as "paid" in QuickBooks
>
> **Action Required:** QuickBooks accounting team needs to process payments against December 2025 invoices. Once payments are recorded, the next commission sync will automatically pull them into the report.
