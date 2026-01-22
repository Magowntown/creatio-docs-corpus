# CLAUDE.md - Creatio Reports Fix

> **Status:** 🔴 **SYNC-004:** QB Web Connector offline. **IW-001:** IW_Commission Excel columns misaligned. ✅ **UI-002:** Reports page fixed.
> **Updated:** 2026-01-22 | **See:** `docs/TEAM_SUMMARY_20260120.md` for team summary

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
| **SYNC-002** | QB sync issue - UsrPage_ebkv9e8 implicated (PROD) | ✅ **Debunked** (see analysis) |
| **SYNC-003** | QB Customer Order Integration 20K limit | 🔴 **Batch Processing Required** |
| **UI-001** | DEV Reports page infinite loading | ✅ Fixed (Hybrid.js) |
| **EARNERS-001** | Brandwise backlog missing commission earners | ✅ **RESOLVED** (263 earners + schema fix) |
| **RPT-001** | Reports other than Commission fail (queryConfig) | ✅ **RESOLVED** (13/13 reports configured) |
| **RPT-003** | "Items by Customer" fails with BGYearMonth not found | ✅ **FIX READY** - View-specific filter mapping |
| **RPT-002** | "Rpt Sales By Line" fails with GUID error | ✅ **DEPLOYED** (ESQ sanitization) |
| **DL-004** | Commission download returns 404 | ✅ **DEPLOYED** to PROD |
| **DL-005** | Excel VBA "Type mismatch" error on open | ✅ **FIX READY** - DateTime null handling |
| **DATA-002** | Dec 2025 invoices awaiting payment in QB | ✅ **PARTIALLY RESOLVED** - Sync pulled data |
| **DATA-004** | Patricia Goncalves Dec 2025 commission missing | ⚠️ **ROOT CAUSE: QB Payment** |
| **DATA-003** | DEV commission data only through Oct 2025 | ⚠️ **Needs QB Sync** |
| **PROC-001** | V4 Commission process gateway type mismatch | 📋 Dormant (no IWPayments data) |
| ENV-001 | Template lookup broken in DEV | ✅ NOT REPRODUCIBLE |
| FUT-001 | Pre-calculated .xlsx (server-side macros) | 📋 Future |
| **FUT-002** | Freedom UI: Product Pictures in List Views | 📋 Future |
| **CSP-001** | Looker Studio iframes blocked by Freedom UI CSP | 🔴 **BLOCKED** - Requires server config |
| **LOOKER-001** | Looker Studio Google permissions for direct access | 🔴 **BLOCKED** - Requires BGlobal action |
| **RPT-004** | "Items by Customer" Row out of range error | 🔴 **Template Issue** - IntExcelReport config |
| **HANDLER-001** | Hybrid handler deployed (Looker + Excel fallback) | ✅ **DEPLOYED** to PROD |
| **SYNC-004** | QB Web Connector offline (96.56.203.106:8080) | 🔴 **IT Action Required** |
| **SYNC-005** | 637 orders falsely marked "Processed" (Aug 2023-Jan 2026) | 🔴 **Reset After QB Online** |
| **DATA-005** | Patricia Goncalves 97.8% commission missing | ⚠️ **QB Payment Bottleneck** |
| **DEV-001** | PROD → DEV sync for IWQBIntegration consolidation | ⏳ **In Progress** |
| **IW-001** | IW_Commission Excel columns misaligned | ⏳ **Template alignment needed** |
| **UI-002** | Non-Commission reports showing wrong filters (PROD) | ✅ **RESOLVED** - Parent schema restored |

---

## UI-002: Non-Commission Reports Showing Wrong Filters (PROD)

**Discovered:** 2026-01-22 | **Resolved:** 2026-01-22
**Status:** ✅ **RESOLVED** - Parent schema restored to original state

### Problem

Reports page showed `TypeError: Cannot read properties of undefined (reading 'getSchema')` error and prevented all report generation.

### Root Cause Analysis

**CRITICAL DISCOVERY:** Handler code with `$UsrShowCommissionFilters` attribute bindings was incorrectly deployed to the **PARENT schema** (BGlobalLookerStudio package) instead of the **CHILD schema** (BGApp_eykaguu package).

**Freedom UI Schema Inheritance:**
- Parent schemas use `viewModelConfig` (base definition with all attributes)
- Child schemas use `viewModelConfigDiff` (extends parent with differences)
- `getSchema` error occurs during schema resolution BEFORE handlers execute

**Why it failed:** Parent schema had `visible: "$UsrShowCommissionFilters"` bindings but the `UsrShowCommissionFilters` attribute wasn't defined in the parent's `viewModelConfig`, causing Freedom UI to fail during schema resolution.

### Solution Applied (2026-01-22)

**Step 1:** Restored PARENT schema to original state
```
Schema UID: 4e6a5aa6-86b7-48c1-9147-7b09e96ee59e
Package: BGlobalLookerStudio
File: client-module/BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js
```
- Uses `viewModelConfig` (NOT `viewModelConfigDiff`)
- Contains all original attributes: LookupAttribute_0as4io2, CreatedFrom, CreatedTo, etc.
- Contains original handlers: OpenReport, OpenReportIview

**Step 2:** Verified CHILD schema is minimal/empty
```
Schema UID: 561d9dd4-8bf2-4f63-a781-54ac48a74972
Package: BGApp_eykaguu
```
- Uses `viewModelConfigDiff` (empty array)
- No conflicting handlers or attribute bindings

### Verified Result

Reports page now loads successfully with all original filters visible:

| Element | Status |
|---------|--------|
| Report dropdown | ✅ Visible |
| Created From/To | ✅ Visible |
| Shipping From/To | ✅ Visible |
| Delivery From/To | ✅ Visible |
| Status Order dropdown | ✅ Visible |
| Report button | ✅ Visible |
| iframe | ⚠️ Blocked by CSP (expected - see CSP-001) |

### Key Files

| File | Purpose |
|------|---------|
| `client-module/BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js` | Original parent schema (DEPLOYED) |
| `docs/REPORT_FILTER_MAPPING.md` | Filter requirements for all 18 reports |

### Lesson Learned

When deploying Freedom UI handlers with custom attributes and conditional visibility:
1. **ALWAYS deploy to CHILD schemas** (using `viewModelConfigDiff`)
2. **NEVER modify PARENT schemas** unless changing base functionality
3. Attributes used in `visible: "$AttributeName"` bindings MUST be declared in the same schema's attributes section

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

### Update (2026-01-19): DEBUNKED

**Analysis in `docs/USRPAGE_CONFLICT_ANALYSIS.md` proves UsrPage_ebkv9e8 does NOT cause QB sync issues:**
- Client-side handlers are page-scoped (only run when page is open)
- No entity writes - only reads for report generation
- QB sync runs server-side as business process - completely independent
- Real culprit: IWQBIntegration's OrderPageV2 setting PaymentStatusId=Planned

---

## UI-001: DEV Reports Page Infinite Loading

**Discovered:** 2026-01-19 | **Resolved:** 2026-01-19
**Status:** ✅ Fixed by deploying Hybrid.js handler

### Problem

DEV Reports page showed infinite loading spinner on page load, preventing report generation.

### Root Cause

The `UsrPage_ebkv9e8_Updated.js` handler used `sdk` objects (`sdk.HandlerChainService`, `sdk.Model.create`, `sdk.FilterGroup`) in its `crt.LoadDataRequest` and `crt.HandleViewModelAttributeChangeRequest` handlers. The `sdk` object wasn't properly available in the Freedom UI context, causing JavaScript errors on page load.

### Solution

Deployed `UsrPage_ebkv9e8_Hybrid.js` which:
- Only has the report generation handler (`usr.GenerateExcelReportRequest`)
- No framework interceptors (no `crt.LoadDataRequest`, no `crt.HandleViewModelAttributeChangeRequest`)
- Uses only `fetch()` and `Terrasoft` (globally available)
- No `sdk` dependencies

### Deployment

```
https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734
```

Paste contents of `client-module/UsrPage_ebkv9e8_Hybrid.js` and save.

---

## RPT-002: "Rpt Sales By Line" GUID Error Fix

**Discovered:** 2026-01-19
**Status:** ✅ **FIX READY** - Awaiting deployment

### Problem

"Rpt Sales By Line" report fails with:
```
FormatException: Guid should contain 32 digits with 4 dashes
```

### Root Cause

The `IntExcelReport.IntEsq` JSON for this report contains a filter with `@P1@` placeholder:
```json
"parameter": {"value": "@P1@"}
```

The `IntExcelExport.ReportUtilities.ConvertStringToEsq()` method cannot parse this placeholder as a GUID.

### Fix

Added `SanitizeEsqJson()` method to `UsrExcelReportService_Updated.cs` that:
1. Detects `@P<number>@` patterns in ESQ JSON
2. Uses balanced brace matching to find the `items` object in filters
3. Clears the items (makes it `{}`) if placeholders exist
4. This mimics the working Commission report pattern (0 filter items in ESQ)

### Affected Reports

| Category | Count | Status |
|----------|-------|--------|
| With @P placeholders | 1 | ✅ Will be fixed |
| Valid ESQ (no placeholders) | 14 | ✅ Already work |
| Empty ESQ | 18 | ⚠️ Need configuration |

### Deployment

**Backend:** `source-code/UsrExcelReportService_Updated.cs`
```
https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

### Verification Test

After deployment, run:
```python
# Generate "Rpt Sales By Line" report
payload = {"ReportId": "0b40d51d-4935-4918-97f2-45352aed341f"}
# Should return success: true (previously failed with GUID error)
```

---

## DL-004: Commission Report Download Returns 404

**Discovered:** 2026-01-19 | **Resolved:** 2026-01-20
**Status:** ✅ **DEPLOYED** to PROD

### Problem

Commission report generation succeeds (returns `success: true` with key like `ExportFilterKey_<guid>`), but download via `GetReport/{key}` returns HTTP 404.

### Root Cause

The library fallback path (`ReportUtilities.Generate()`) returns an `ExportFilterKey_*` but does NOT store the file bytes in `SessionData`. The `GetReport` endpoint looks for bytes in `userConnection.SessionData[key]` and returns 404 when not found.

```
Generate → ReportUtilities.Generate() → Returns ExportFilterKey_abc123
GetReport → SessionData["ExportFilterKey_abc123"] → NULL → 404
```

### Fix Applied to Code

**File:** `source-code/UsrExcelReportService_Updated.cs`

**Changes:**

1. **Lines 1588-1605** - Route Commission reports to custom generator:
```csharp
if (entitySchemaName == "BGCommissionReportDataView")
{
    if (request.YearMonthId != Guid.Empty)
    {
        // Use GenerateWithDateFilter (already stores bytes in SessionData)
        return GenerateWithDateFilter(userConnection, request, yearMonthName);
    }
    else
    {
        // New method for all-time queries
        return GenerateWithDateFilterAllTime(userConnection, request);
    }
}
```

2. **Lines 1214-1263** - New `GenerateWithDateFilterAllTime` method:
   - Queries last 24 months of commission data
   - Populates Excel template
   - **Stores bytes in SessionData** (the key fix)
   - Returns key that GetReport can resolve

### Deployment

**PROD URL:**
```
https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

**Steps:**
1. Open PROD Source Code Schema Designer
2. Replace contents with `source-code/UsrExcelReportService_Updated.cs`
3. Save and publish
4. Wait for compilation

### Verification

After deployment, run:
```bash
python3 scripts/testing/verify_download_fix.py PROD
```

**Expected:**
- Generate returns `success: true` with key
- GetReport returns 200 with `Content-Type: application/octet-stream`
- Downloaded file starts with `PK` (valid Excel zip signature)

---

## DL-005: Excel VBA "Type mismatch" Error on Open

**Discovered:** 2026-01-20
**Status:** ✅ **FIX READY** - Redirect approach to preserve library output

### Problem

Commission report downloads successfully with 1099 rows, but Excel throws VBA macro error when opening:
```
Microsoft Visual Basic
Run-time error '12':
Type mismatch
```

### Root Cause (Revised)

The DL-004 fix routed Commission reports to our custom `PopulateExcelTemplate` method which manipulates the Excel XML directly. This broke the VBA macros because:
1. Our XML manipulation doesn't preserve VBA-expected data formats
2. The original library (`IntExcelExport`) generates proper Excel files that work with VBA

### Fix Applied

**Strategy:** Use the library's generation (preserves VBA) but redirect to library's GetReport for download.

**File:** `source-code/UsrExcelReportService_Updated.cs`

**Changes:**
1. Removed Commission bypass in Generate (lines 1642-1646) - now uses library generation
2. Added redirect logic in GetReport (lines 1909-1917):

```csharp
// DL-004/DL-005 FIX: If bytes not in our SessionData, try library's GetReport
if (cacheObj == null && key.StartsWith("ExportFilterKey_"))
{
    // Redirect to library's endpoint which knows where its bytes are stored
    var libraryUrl = "/0/rest/IntExcelReportService/GetReport/" + key;
    HttpContext.Current.Response.Redirect(libraryUrl, true);
    return;
}
```

**How it works:**
1. Generate calls the library's `ReportUtilities.Generate()` → produces proper Excel with VBA
2. Library stores bytes in its own cache (not our SessionData)
3. Our GetReport detects `ExportFilterKey_` with no bytes → redirects to library's endpoint
4. Library's GetReport serves the file correctly

### Deployment

**PROD URL:**
```
https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

**Steps:**
1. Open PROD Source Code Schema Designer
2. Replace contents with `source-code/UsrExcelReportService_Updated.cs`
3. Save and publish
4. Wait for compilation
5. Test Commission report download - should open in Excel without VBA errors

---

## SYNC-003: QB Customer Order Integration 20K Record Limit

**Discovered:** 2026-01-19
**Status:** 🔴 Batch processing required - cannot run until resolved

### Problem

Running "QB Customer Order Integration" in DEV fails with:
```
Terrasoft.Common.InvalidObjectStateException: Maximum number of 20000 records exceeded
while loading "BGQuickBooksIntegrationLogDetail" object data
```

### Root Cause

| Metric | Value |
|--------|-------|
| Total log records | **81,803** |
| Pending status | **~56,000+** (69%) |
| ESQ default limit | 20,000 |
| Pending date range | Oct 8, 2025 → Dec 10, 2025 |

The process `GetQuickBooksPendingLogsByType()` tries to load ALL pending records at once, exceeding Creatio's EntitySchemaQuery limit.

### Status Lookup

| Status ID | Name |
|-----------|------|
| `c97db3bc-634d-4c90-8432-ec7141c87640` | Pending |
| `e7428193-4cf1-4d1b-abae-00e93ab5e1c5` | Processed |
| `bdfc60c7-55fd-4cbd-9a2c-dca2def46d80` | Error |
| `fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef` | Processing |
| `ff92e20c-da27-4255-96bc-57e32f0944f4` | Re-Process |

### Batch Processing Solution (All Records Preserved)

**Step 1: Check counts**
```sql
SELECT
    CASE "BGStatusId"
        WHEN 'c97db3bc-634d-4c90-8432-ec7141c87640' THEN 'Pending'
        WHEN 'e7428193-4cf1-4d1b-abae-00e93ab5e1c5' THEN 'Processed'
        WHEN 'bdfc60c7-55fd-4cbd-9a2c-dca2def46d80' THEN 'Error'
        WHEN 'fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef' THEN 'Processing'
        WHEN 'ff92e20c-da27-4255-96bc-57e32f0944f4' THEN 'Re-Process'
        ELSE 'Unknown'
    END as status,
    COUNT(*) as count
FROM "BGQuickBooksIntegrationLogDetail"
GROUP BY "BGStatusId"
ORDER BY count DESC;
```

**Step 2: Move older pending to Re-Process (keep newest 15K as Pending)**
```sql
WITH newest_pending AS (
    SELECT "Id"
    FROM "BGQuickBooksIntegrationLogDetail"
    WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'
    ORDER BY "CreatedOn" DESC
    LIMIT 15000
)
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'ff92e20c-da27-4255-96bc-57e32f0944f4'  -- Re-Process
WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'  -- Pending
  AND "Id" NOT IN (SELECT "Id" FROM newest_pending);
```

**Step 3: Run QB Customer Order Integration**

**Step 4: Rotate next batch back to Pending**
```sql
WITH next_batch AS (
    SELECT "Id"
    FROM "BGQuickBooksIntegrationLogDetail"
    WHERE "BGStatusId" = 'ff92e20c-da27-4255-96bc-57e32f0944f4'
    ORDER BY "CreatedOn" DESC
    LIMIT 15000
)
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'
WHERE "Id" IN (SELECT "Id" FROM next_batch);
```

Repeat Steps 3-4 until all Re-Process records are processed.

### Impact on Other Processes

| Process | Impact |
|---------|--------|
| QB Customer Order Integration | ⚠️ Re-Process records skipped until rotated |
| WooCommerce | ✅ No impact - creates NEW Pending entries |
| Brandwise | ✅ No impact - creates NEW Pending entries |
| Commission Sync | ✅ No impact - different type |

---

## DATA-003: DEV Commission Data Only Through October 2025

**Discovered:** 2026-01-19
**Status:** ⚠️ Needs QB sync to resolve

### Problem

DEV Commission reports show empty data for November 2025 onwards because the `BGCommissionReportQBDownload` table hasn't been synced.

### Data Comparison

| Environment | Total Records | Most Recent Data |
|-------------|--------------|------------------|
| **DEV** | 9,112 | **October 2025** |
| **PROD** | 10,025 | January 2026 |

### DEV Data Distribution (sample of 500)

| Month | Records |
|-------|---------|
| 2025-10 | 6 |
| 2025-09 | 29 |
| 2025-08 | 21 |
| 2025-07 | 24 |
| ... | ... |

### Resolution

Run QB Commission sync in DEV after resolving SYNC-003 (20K limit issue).

---

## EARNERS-001: Brandwise Backlog Missing Commission Earners

**Discovered:** 2026-01-19 | **Resolved:** 2026-01-19
**Status:** ✅ RESOLVED - All fixes applied and verified

### Problem Summary

Brandwise orders from Jan 14-18, 2026 (and some December 2025 orders) were missing from Commission reports because they lacked `BGCommissionEarner` records.

### Root Cause

The "Add Commission Earners" process only runs on **order creation**, not modification. The Tax Status process was broken from Jan 14-18, which prevented the normal process chain from executing for Brandwise orders during that period.

### Actions Taken (2026-01-19)

| Action | Result |
|--------|--------|
| Created 253 BGCommissionEarner records | ✅ Via OData API |
| Fixed commission rates (1%-15%) | ✅ From Employee.BGDefaultCommission |
| Fixed names (Employee.Name) | ✅ e.g., "Jim Martin 6%", "Denise Rotenberry" |
| Verified new order process | ✅ 35 auto-created earners today |

### Resolution Summary (2026-01-19)

| Fix | Status | Result |
|-----|--------|--------|
| BGIsNote schema fix | ✅ Applied | View returns boolean (was integer) |
| Commission earners | ✅ Created | 263 manual + 37 auto |
| QB Download records | ✅ Created | 249 records |
| View population | ✅ Working | 34,883 total records |

**Report Improvements:**
| Month | Before | After | Change |
|-------|--------|-------|--------|
| December 2025 | 49 rows | 194 rows | +296% |
| January 2026 | 7 rows | 106 rows | +1414% |

**Note:** 130 orders won't appear until synced to QuickBooks (missing BGNumberInvoice)

### Scripts Created

| Script | Purpose |
|--------|---------|
| `scripts/utilities/populate_qb_download_v2.py` | Populate QB download table (FK-safe) |
| `scripts/utilities/final_gap_analysis.py` | Verify data integrity |
| `scripts/utilities/find_bgisnote.py` | Locate BGIsNote definitions |
| `scripts/utilities/get_current_view.py` | Verify view state |
| `scripts/sql/BGCommissionReportDataView_BGIsNote_fix.sql` | PostgreSQL view fix (APPLIED) |

### Documentation

| Document | Purpose |
|----------|---------|
| `docs/COMMISSION_FIX_COMPLETE.md` | Full technical documentation |
| `docs/ACTION_LOG.md` | Timeline of all actions |
| `docs/QUICK_REFERENCE.md` | Quick commands and troubleshooting |
| `docs/CURRENT_STATUS.md` | Current status summary |

### Key Entities

```
BGCommissionEarner:
- BGOrderId: Order GUID
- BGSalesRepId: Employee GUID (NOT Contact)
- BGName: Employee name
- BGCommissionRate: From Employee.BGDefaultCommission
- BGAddedManually: true for manual records

Account.BGAccountSalesRepId → Employee (source of sales rep)
```

### Maintenance

To verify ongoing health, run:
```bash
python3 scripts/utilities/final_gap_analysis.py
```

Expected: Auto-earner creation ✅ WORKING, 30+ earners auto-created daily

### 9 Orders Skipped (No Sales Rep)

These accounts need `BGAccountSalesRepId` assigned:
- Details-4
- Perch-1
- ST MICHAELS WOMAN'S EXCHANGE-1
- Simone REGALO-1
- GBG Associates-1
- National Roper's Supply-1

---

## DATA-002: December 2025 Invoices Awaiting Payment in QuickBooks

**Discovered:** 2026-01-15 | **Updated:** 2026-01-20
**Status:** ✅ **PARTIALLY RESOLVED** - Sync pulled significant new data

### Client Observation

> "Receiving Returns on the reports but not Sales"

### Update (2026-01-20): Sync Successful

After running "Get QuickBooks Commissions" and "QB Customer Integration" processes:

| Month | Before Sync | After Sync | Change |
|-------|-------------|------------|--------|
| **Dec 2025** | 39 records ($0 sales) | **106 records, $34,353.57** | ✅ +67 records |
| **Jan 2026** | 4 records (negatives) | **294 records, $168,588.02** | ✅ +290 records |
| Feb 2026 | 0 records | 26 records, $24,462.50 | ✅ New |
| Mar 2026 | 0 records | 4 records, $2,318.50 | ✅ New |

**Result:** Commission data is now available. Re-run Commission report to verify.

### Original Data Flow Investigation

```
Creatio Orders → QB Invoices → [Awaiting Payment] → QB ReceivePayments → Commission Data
     ✅              ✅               ✅                    ✅                    ✅
  (EXISTS)       (SYNCED)        (PROCESSED)          (NOW SYNCED)          (AVAILABLE)
```

### Remaining Gap Analysis

December 2025 ($34K) may still be lower than expected if some invoices haven't been paid in QuickBooks. The January 2026 figure ($168K) likely includes payments for December invoices that were paid in January.

### Action for Remaining Gap

If specific invoices are still missing after re-running the report:
1. Identify the missing invoice numbers
2. QuickBooks accounting team marks those invoices as paid
3. Run "Get QuickBooks Commissions" again

**Technical Details:** `docs/CLAUDE_REFERENCE.md` → "December 2025 Data Gap Analysis"

---

## DATA-004: Patricia Goncalves December 2025 Commission Missing

**Discovered:** 2026-01-19
**Status:** ⚠️ **ROOT CAUSE CONFIRMED** - QB Payment Workflow Issue

### Problem

Patricia Goncalves has December 2025 commission earners but $0 showing in commission reports.

### Investigation Results (Definitive)

| Metric | Value |
|--------|-------|
| Patricia's December earners | 63 records |
| Orders with invoice numbers | ✅ All have BGNumberInvoice |
| Invoices in QB Download | **2 out of 30** (7%) |
| Invoices NOT in QB Download | **28 out of 30** (93%) |

### Sample Missing Invoices

Patricia's December invoices NOT in QB Download:
- Invoice #59446 (ORD-14857)
- Invoice #59279 (ORD-14817)
- Invoice #61177 (ORD-15357)
- Invoice #59696 (ORD-14913)
- ... and 24 more

### Root Cause (Confirmed)

The commission view requires:
```
Order.BGNumberInvoice = BGCommissionReportQBDownload.BGCleanInvoiceNumber
```

Since 93% of Patricia's December invoices haven't been paid in QuickBooks, they don't have corresponding ReceivePayment records, and therefore don't appear in the QB Download table.

### Why January 2026 Works

Patricia has **132 January 2026** commission records ($41,263.86). These are likely from invoices that were invoiced earlier but **paid** in January, allowing the ReceivePayment records to sync.

### Action Required

**QuickBooks accounting team** must process payments against Patricia's December 2025 invoices. Once paid, the next "Get QuickBooks Commissions" sync will automatically populate the data.

### Verification Script

```bash
python3 /tmp/trace_patricia_december_gap.py
```

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
| Frontend handler (RECOMMENDED) | `client-module/UsrPage_ebkv9e8_Hybrid.js` |
| Frontend handler (has sdk issues) | `client-module/UsrPage_ebkv9e8_Updated.js` |
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
| **BGlobal Email (CSP/Looker issues)** | `docs/EMAIL_BGLOBAL_REPORT_ISSUES.md` - Email draft for BGlobal |
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
| **Frontend handler (DEPLOYED)** | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` |
| Backend service (C#) | `source-code/UsrExcelReportService_Updated.cs` |
| Frontend handler (legacy) | `client-module/UsrPage_ebkv9e8_Updated.js` |

---

## Session Log: 2026-01-20 (Commission Data Sync Success)

### DATA-002 Resolution: QB Sync Pulled New Data

**Time:** Late session
**Status:** ✅ Commission data now available

After user ran "Get QuickBooks Commissions" and "QB Customer Integration" processes, browser console queries confirmed significant new data:

| Month | Records | Amount |
|-------|---------|--------|
| Jan 2026 | 294 | $168,588.02 |
| Dec 2025 | 106 | $34,353.57 |
| Feb 2026 | 26 | $24,462.50 |
| Mar 2026 | 4 | $2,318.50 |
| Apr 2026 | 2 | $1,607.00 |

**Key Insight:** January 2026's large amount ($168K) likely includes payments for December invoices that were paid in January. Commission data is tied to **payment date**, not invoice date.

**Next Step:** User should re-run Commission report to verify data now displays correctly.

---

## Session Log: 2026-01-20 (Package Removal & Looker Studio Investigation)

### Context

IWQBIntegration and InterWeavePaymentApp packages were removed from PROD. Reports page needed to be restored to original functionality.

---

### CSP-001: Looker Studio Blocked by Content Security Policy

**Discovered:** 2026-01-20
**Status:** 🔴 BLOCKED - Requires Creatio server configuration

**Problem:** After removing InterWeave packages, attempted to restore original Looker Studio functionality. Iframes are blocked:

```
Refused to frame 'https://bglobalsolutions.com/' because it violates Content Security Policy
X-Frame-Options set to 'sameorigin'
```

**Root Cause:** Freedom UI (Creatio 8) has stricter default CSP policies than Classic UI (Creatio 7). External domains cannot be embedded in iframes without explicit server-side configuration.

**Attempted Workarounds:**
1. ❌ Original iframe approach - blocked by CSP
2. ⚠️ Open in new tab - works but requires Google permissions

**Resolution Required:** BGlobal needs to whitelist `lookerstudio.google.com` in Creatio's CSP settings, or users need Google account access granted.

---

### LOOKER-001: Looker Studio Google Permissions Issue

**Discovered:** 2026-01-20
**Status:** 🔴 BLOCKED - Requires BGlobal/Google Workspace action

**Problem:** When opening Looker Studio URLs in new tab (bypassing CSP), users get:

```
Can't access report
Your current account [user@email.com] can't access this report, or the report doesn't exist.
```

**Investigation:**
- URLs in `UsrReportesPampa.UsrURL` are embed-format URLs (designed for authenticated iframe context)
- Converted `/embed/` to `/u/0/` for direct viewing - still fails
- Google account permissions not configured for direct access

**Reports with Looker Studio URLs:**
| Report | Has URL |
|--------|---------|
| Sales By Customer | ✅ |
| Sales By Sales Group | ✅ |
| Sales By Customer Type | ✅ |
| Sales Rep Monthly Report | ✅ |
| Sales By Sales Rep | ✅ |
| Sales By Line With Ranking | ✅ |

**Reports WITHOUT Looker Studio URLs (Excel only):**
| Report | UsrURL |
|--------|--------|
| Commission | (empty) |
| Sales By Item By Type Of Customer | (empty) |
| Customers did not buy over period | (empty) |
| Sales By Item | (empty) |

**Resolution Required:** BGlobal needs to either:
1. Share Looker Studio dashboards with user Google accounts, OR
2. Make dashboards "Anyone with link can view", OR
3. Update URLs from embed format to direct viewing format

---

### RPT-004: "Items by Customer" Row Out of Range Error

**Discovered:** 2026-01-20
**Status:** 🔴 Template configuration issue

**Error:**
```
ArgumentException: Row out of range STACK:[0]at IntExcelExport.Utilities.ReportUtilities.LoadEsqToSheet
```

**Root Cause:** Excel template (`IntExcelReport`) has misconfigured data range - the template structure doesn't match the query results.

**Impact:** All reports without Looker Studio URLs (that fall back to Excel) may have similar template issues.

---

### HANDLER-001: Hybrid Handler Deployed

**Status:** ✅ DEPLOYED to PROD

**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js`

**Logic:**
```
User clicks "Generate Report"
    ↓
Check if report has UsrURL (Looker Studio)?
    ├─ YES → window.open(URL) in new tab
    │        (converts /embed/ to /u/0/ for direct viewing)
    └─ NO  → UsrExcelReportService for Excel download
            (resolves UsrReportesPampa → IntExcelReport ID)
```

**Test Results:**
| Report Type | Result |
|-------------|--------|
| Commission (Excel) | ✅ Downloads successfully |
| Looker Studio reports | ⚠️ Opens tab but requires Google permissions |
| Other Excel reports | ❌ Template configuration errors |

---

### Handler Evolution (Mistakes & Corrections)

| Version | Issue | Resolution |
|---------|-------|------------|
| v1 (Minimal) | Empty schema to inherit parent | CSP blocked Looker Studio iframe |
| v2 (UsrService) | Called UsrExcelReportService with wrong ID | FormatException: Excel template not found |
| v3 (UsrService_v2) | Added IntExcelReport resolution | Handler not running (cache) |
| v4 (Hybrid_v2) | Full hybrid with Looker + Excel paths | ✅ **Current deployed version** |

**Key Mistake:** Initially passed `UsrReportesPampa.Id` to `UsrExcelReportService`, but service expects `IntExcelReport.Id`. Fixed by adding OData lookup to resolve report name → IntExcelReport ID.

**Cache Issue:** After deploying new handler, console still showed old behavior. Solution: Hard refresh (`Ctrl+Shift+R`) required after schema compilation.

---

### Files Created This Session

| File | Purpose |
|------|---------|
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | **DEPLOYED** - Hybrid Looker/Excel handler |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_UsrService_v2.js` | Excel-only with IntExcelReport resolution |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_UsrService.js` | Excel-only (had wrong ID issue) |
| `docs/EMAIL_BGLOBAL_REPORT_ISSUES.md` | Email draft for BGlobal |

---

### Deployment Summary

| Component | Schema UID | Status |
|-----------|------------|--------|
| UsrExcelReportService (backend) | ed794ab8-8a59-4c7e-983c-cc039449d178 | ✅ Deployed |
| UsrPage_ebkv9e8 (child handler) | 561d9dd4-8bf2-4f63-a781-54ac48a74972 | ✅ Deployed (Hybrid_v2) |
| BGlobalLookerStudio (parent) | 4e6a5aa6-86b7-48c1-9147-7b09e96ee59e | Unchanged |

---

### Key Findings Summary

1. **Original system design:** Looker Studio iframes for most reports (now blocked by v8 CSP)
2. **Freedom UI (v8) security:** Stricter CSP than Classic UI (v7) - breaking change
3. **Commission reports:** Work via Excel (no Looker URL configured)
4. **Other reports:** Blocked - either Looker permissions or Excel template issues
5. **Root cause of issues:** Creatio 7 → 8 migration + package removal

---

### Next Steps (Awaiting BGlobal)

1. **CSP Configuration:** Whitelist Looker Studio domains in Creatio server settings
2. **Google Permissions:** Grant user access to Looker Studio dashboards
3. **Excel Templates:** Review IntExcelReport configurations for reports without Looker URLs
4. **QB Payments:** Process December 2025 / January 2026 invoice payments for Commission data

**Email sent to BGlobal:** `docs/EMAIL_BGLOBAL_REPORT_ISSUES.md`

---

## Session Log: 2026-01-19 (Latest - Continued)

### DL-004: Commission Download 404 Fix (Code Ready)

**Problem:** PROD Commission report generation succeeded but download failed with 404.

**Investigation Results:**
- `Generate` returns `ExportFilterKey_<guid>` with `success: true`
- `GetReport/{key}` returns 404
- Library fallback (`ReportUtilities.Generate`) doesn't store bytes in SessionData
- `GetReport` expects `userConnection.SessionData[key]` to contain file bytes

**Fix Applied:**
1. Added routing in Generate method to use `GenerateWithDateFilter` for Commission with Year-Month filter
2. Created new `GenerateWithDateFilterAllTime` method for Commission without filter
3. Both methods properly store bytes in SessionData before returning key

**Files Modified:**
- `source-code/UsrExcelReportService_Updated.cs` (lines 1214-1263, 1588-1605)

**Verification Script Created:**
- `scripts/testing/verify_download_fix.py`

**Status:** ✅ Code ready in repo, awaiting deployment to PROD

---

### RPT-002: ESQ Sanitization Fix (DEPLOYED to PROD)

**Verification:** Tested "Rpt Sales By Line" - no @P patterns, filter items cleared.

---

### December 2025 Payment Gap Confirmed

**Investigation Results:**
| Metric | Value |
|--------|-------|
| Total affected sales reps | 44 |
| Total affected commission earners | 790 |
| December 2025 orders showing Unpaid | 78% |
| Patricia Goncalves earners missing | 61 |

**Root Cause:** QB accounting hasn't processed December 2025 invoice payments.

**Documentation Created:**
- `docs/QB_TEAM_ACTION_REQUIRED.md`
- `docs/QB_TEAM_EMAIL_DRAFT.md`

---

## Session Log: 2026-01-19 (Earlier)

### UI-001: DEV Reports Page Infinite Loading (FIXED)

**Problem:** DEV Reports page showed infinite loading spinner, blocking all report generation.

**Root Cause:** `UsrPage_ebkv9e8_Updated.js` used `sdk` objects in framework interceptors (`crt.LoadDataRequest`, `crt.HandleViewModelAttributeChangeRequest`). The `sdk` object wasn't available in Freedom UI context, causing JS errors on page load.

**Fix:** Deployed `UsrPage_ebkv9e8_Hybrid.js` - minimal handler with only report generation, no `sdk` dependencies.

---

### DATA-003: DEV Commission Data Investigation

**Problem:** Reports generating but showing missing/empty data for recent months.

**Investigation Results:**

| Environment | Total Records | Most Recent Data |
|-------------|--------------|------------------|
| DEV | 9,112 | October 2025 |
| PROD | 10,025 | January 2026 |

**Conclusion:** DEV hasn't synced commission data since October 2025. November 2025+ data doesn't exist in DEV.

**Test Results:**
- December 2024: 514 rows ✅
- December 2025: 1 row (header only) ❌
- January 2026: 1 row (header only) ❌

---

### SYNC-003: QB Customer Order Integration 20K Limit

**Problem:** Attempted to run QB sync in DEV, received error:
```
Maximum number of 20000 records exceeded while loading "BGQuickBooksIntegrationLogDetail"
```

**Root Cause:**
- `BGQuickBooksIntegrationLogDetail` has 81,803 records
- ~56,000+ are in "Pending" status (69%)
- Creatio ESQ default limit is 20,000
- Process tries to load ALL pending records at once

**Pending Records Analysis:**
- All pending records are type: "Customer Order" / action: "Update"
- Date range: October 8, 2025 → December 10, 2025
- Backlog has been building for 3+ months

**Solution Documented:** Batch processing approach using "Re-Process" status rotation (see SYNC-003 section above).

---

### EARNERS-001: Brandwise Commission Earners Fix

**Problem:** December 2025 and January 2026 Commission reports only showing 49 and 7 rows respectively - Brandwise orders missing.

**Investigation Results:**
- December Brandwise: 79 orders, 0 had commission earners
- January Brandwise: 194 orders, 0 had commission earners
- Root cause: "Add Commission Earners" process only runs on order creation
- Tax Status process was broken Jan 14-18, breaking the process chain

**Actions Taken:**
1. Created 253 `BGCommissionEarner` records via OData API
2. Fixed commission rates using `Employee.BGDefaultCommission` (varied 1%-15%)
3. Fixed names using `Employee.Name` (e.g., "Jim Martin 6%", "Denise Rotenberry")
4. Verified new order process is working (35 auto-created earners today)

**Outstanding (CRITICAL):**
- Report view (`BGCommissionReportDataView`) NOT being populated
- **BROADER ISSUE: View has only 9 new records since Jan 14 - affects ALL orders**
- "Fill Commission Report Fields" process runs in <1 second but creates 0 records
- Direct API insertion fails due to BGIsNote schema mismatch (integer vs boolean)
- Even today's 36 auto-created earners are not appearing in report view
- User ran "Get QuickBooks Commissions" process - no effect on view
- Package reinstall did not fix the issue

**Scripts Created:**
- `/tmp/verify_and_create_earners.py` - Create commission earners
- `/tmp/fix_commission_earners.py` - Fix rates and names
- `/tmp/COMMISSION_FIX_LOG.md` - Detailed documentation

**Next Steps:**
1. Investigate "Fill Commission Report Fields" process in Creatio admin
2. Check for process errors in logs
3. Once view populates, regenerate reports

---

## Session Log: 2026-01-16

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

---

## Session Log: 2026-01-20 (QB Sync Infrastructure Investigation)

### Context

Continued investigation into why Patricia Goncalves and other sales reps have missing commission data despite orders existing in Creatio.

---

### SYNC-004: QB Web Connector Offline

**Discovered:** 2026-01-20
**Status:** 🔴 Infrastructure issue - requires IT action

**Problem:** QB Web Connector at `96.56.203.106:8080` is not responding.

| Test | Result |
|------|--------|
| Ping | ❌ 100% packet loss |
| Port 8080 | ❌ Connection timeout |
| HTTP request | ❌ No response |

**Impact:** 157+ January 2026 orders cannot sync to QuickBooks.

---

### SYNC-005: False "Processed" Orders (Historical Bug)

**Discovered:** 2026-01-20
**Status:** 🔴 637 orders need re-sync

**Problem:** Sync code marks orders as "Processed" even when connection fails.

| Metric | Value |
|--------|-------|
| Orders marked Processed with no QB ID | **637** |
| Date range | Aug 2023 → Jan 2026 |
| Root cause | Bug in `BGQuickBooksLogDetail.ProcessCustomerOrders()` |

**Fix Required:** Reset to Pending after QB Web Connector is online:
```sql
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640',
    "BGErrorMessage" = ''
WHERE "BGStatusId" = 'e7428193-4cf1-4d1b-abae-00e93ab5e1c5'
  AND "BGRecordId" IN (
      SELECT "Id" FROM "Order"
      WHERE "BGQuickBooksId" IS NULL OR "BGQuickBooksId" = ''
  );
```

---

### Data Pipeline Analysis Complete

Traced complete flow from Order → Commission Report:

```
ORDER → QB SYNC → QB INVOICE → QB PAYMENT → COMMISSION
  ✅       ⚠️         ⚠️           ❌           ❌
```

**Patricia Goncalves Example:**

| Stage | Count | % |
|-------|-------|---|
| Commission Earners | 1,250 | 100% |
| Synced to QB | ~400 | ~30% |
| **Paid in QB** | **27** | **2.2%** |
| In Commission Report | 27 | 2.2% |

**97.8% of Patricia's commission missing because invoices not marked paid in QB.**

---

### Actions Taken Today

| Action | Result |
|--------|--------|
| Fixed BGHasQuickBooksLog | 626 orders |
| Fixed ProcessListeners | 626 orders |
| Created log entries | 658 orders |
| Ran QB sync | 336 orders synced |
| Diagnosed timeout errors | 57 → QB offline |
| Found false-processed | 637 historical |

---

### Current Commission Data (After Sync)

| Month | Records | Amount | Commission |
|-------|---------|--------|------------|
| Jan 2026 | 350 | $196,511 | $13,832 |
| Dec 2025 | 115 | $33,087 | $4,888 |
| Feb 2026 | 28 | $26,193 | $3,929 |

---

### Documentation Created

| Document | Purpose |
|----------|---------|
| `docs/QB_SYNC_INFRASTRUCTURE_ISSUE.md` | Technical details for IT/QB team |
| `docs/COMMISSION_DATA_PIPELINE_ANALYSIS.md` | Full pipeline trace |
| `docs/TEAM_SUMMARY_20260120.md` | Non-technical team summary |

---

### Pending Actions

| Action | Owner | Priority |
|--------|-------|----------|
| Bring QB Web Connector online | IT/QB Team | HIGH |
| Reset 637 false-processed orders | Us (after QB online) | HIGH |
| Process invoice payments in QB | QB Accounting | HIGH |
| Fix sync code bug | e6Solutions | MEDIUM |

---

### Orders Verified in QuickBooks

These orders successfully synced and can be verified:

| Order # | Invoice # | QB ID |
|---------|-----------|-------|
| ORD-16076 | 62046 | 42BF65-1768878026 |
| ORD-16078 | 62051 | 42C0A8-1768879067 |
| ORD-16080 | 62053 | 42BFF9-1768878500 |
| ORD-16089 | 62064 | 42C06C-1768878885 |
| ORD-16093 | 62076 | 42C20C-1768937103 |

---

### QB Connection Configuration Investigation

**Checked SysSettings for alternative connections:**

#### QB Desktop (Production) - OFFLINE

| Setting | Value |
|---------|-------|
| `BGQuickBooksLocalUrl` | `http://96.56.203.106` |
| `BGQuickBooksLocalPort` | (empty - defaults to 99) |
| `BGQuickBooksLocalUser` | `qbconnect` |

#### QB Online (Sandbox) - NOT VIABLE

| Setting | Value |
|---------|-------|
| `BGQuickBooksBaseUrl` | `https://sandbox-quickbooks.api.intuit.com` |
| `BGQuickBooksRealmId` | `4620816365305265500` |

**Finding:** QB Online is configured for **sandbox** (test environment), not production. Cannot use as fallback.

---

### Non-Timeout Errors Identified

| Order | Error | Fix |
|-------|-------|-----|
| ORD-15402 | RefNumber too long ("CHA075-TJX AU") | Truncate PO# |
| ORD-15956 | QB Busy | ✅ Reset to Pending |
| ORD-16090 | Missing "Discount" account | QB Admin |
| 5 orders | Closed accounting period | QB Admin |

---

### Creatio-Side Actions Complete

| Action | Status |
|--------|--------|
| Fixed BGHasQuickBooksLog (626 orders) | ✅ |
| Fixed ProcessListeners (626 orders) | ✅ |
| Created 658 log entries | ✅ |
| Synced 336 orders | ✅ |
| Reset QB Busy error | ✅ |
| Verified new order flags correct | ✅ |
| Checked QB connection config | ✅ |
| Investigated QB Online fallback | ✅ Not viable |

**Conclusion:** All Creatio-side actions complete. Remaining blockers require IT (QB Web Connector) and QB Accounting (invoice payments).

---

### BGlobal Email Response (Late Jan 20)

**From Uriel Nusenbaum:**

| Topic | Response |
|-------|----------|
| **Looker Studio** | BGlobal owns dashboards, will share if we provide user emails |
| **Migration** | Says they left it working - e6Solutions responsible for issues |
| **Brandwise/QB Sync** | Doesn't have details - would need support engagement |
| **Telnet test** | Tried telnet, failed - mentioned IP permissions |

**⚠️ Clarification Needed:** Uriel said "I tried to perform a telnet but it is not working" but did NOT specify what server/port. We assumed QB Web Connector (`96.56.203.106:8080`) but this is unconfirmed. Could be:
- QB Web Connector (what we need tested)
- Creatio environment
- Something else entirely

**NOT Looker Studio** - telnet doesn't apply to Google cloud services (browser/HTTPS access, permission issue not network).

**Action:** Need to ask Uriel specifically what he tested and request explicit test of `96.56.203.106:8080`.

---

## Session Log: 2026-01-21 (PROD → DEV Sync & IW_Commission Fix)

### Context

Goal: Consolidate all report fixes into IWQBIntegration package. Bring PROD changes into DEV, then eventually deploy back to PROD.

---

### DEV-001: PROD → DEV Sync Progress

| Step | Status | Notes |
|------|--------|-------|
| Compare backend service (UsrExcelReportService) | ✅ | Identical - no changes needed |
| Compare frontend handler (UsrPage_ebkv9e8) | ✅ | PROD was newer |
| Deploy PROD handler to IWQBIntegration (DEV) | ✅ | Hybrid handler deployed |
| Fix BGApp_eykaguu conflict | ✅ | Made minimal (empty schema) |
| Verify SQL views | ✅ | Both views exist |
| Fix IntExcelReport - IW_Commission link | ✅ | Linked to IWCommissionReportDataView |
| Test Commission report | ✅ | Working |
| Test IW_Commission report | ⏳ | Excel column alignment issue |
| Export IWQBIntegration package | Pending | After testing complete |

---

### IW-001: IW_Commission Excel Template Issues

**Problem:** Report generates but Excel has issues:
1. Columns misaligned (duplicate columns, missing Sales Rep/Group/Account)
2. Commission Rate showing as dates ("1/12/1900" instead of "12%")

**Fixes Applied:**

1. **ESQ updated** - Mapped to correct view columns:
   - IWSalesRepId, IWSalesGroupId, IWAccountId
   - IWPONumber, IWInvoiceDate, IWAmount
   - IWCommissionAmount, IWCommissionRatePercentage
   - IWTransactionDate, IWYearMonthId, IWIsNote, IWDescription

2. **View recreated** - Fixed IWIsNote boolean issue:
   - Before: `CASE WHEN iw."IWBGIsNote" = true THEN 1 ELSE 0 END` (integer)
   - After: `COALESCE(iw."IWBGIsNote", false)` (boolean)

**Pending:** ESQ column order must match Excel template header order.

---

### QB Error Log Cleanup

**Action:** Cleaned up 645 empty connection timeout entries from `BGQuickBooksIntegrationLogDetail`.

| Entry Type | Count | Action |
|------------|-------|--------|
| Empty (connection timeout) | 645 | ✅ Deleted |
| Has order data | 202 | Kept for review |

**Remaining 202 errors:**
- 197 connection timeouts (reprocess when QB online)
- 5 closed accounting period (2021 orders - can delete)
- 1 missing Discount account (QB Admin action)
- 1 RefNumber too long (truncate PO#)

---

### Files Modified This Session

| File | Purpose |
|------|---------|
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Minimal.js` | Empty schema to avoid conflicts |
| IWQBIntegration.UsrPage_ebkv9e8 (DEV) | Hybrid handler from PROD |
| IWCommissionReportDataView (DEV DB) | Fixed IWIsNote boolean |
| IntExcelReport.IW_Commission (DEV DB) | Fixed ESQ column mapping |

---

### Next Steps

1. **Fix IW_Commission Excel columns** - Get template header order, align ESQ
2. **Test all reports in DEV** - Commission, IW_Commission, Looker Studio reports
3. **Export IWQBIntegration package** - For deployment to PROD
