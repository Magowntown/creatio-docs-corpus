# Session Log - 2026-01-29

**Status:** SQL fix ready for deployment
**Next Action:** Apply `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql` in pgAdmin

---

## Session 3: Employee JOIN Investigation & Fix (Evening)

### Issue Discovered
- User reported "Items by Customer" showing 26x duplicate rows per order line
- Example: Sisters customer showing same item repeated 26 times with identical data

### Root Cause Analysis

**Problematic JOIN in BGSalesByItemView:**
```sql
JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId")
```

This joins the order to ALL employees in the sales group (26 employees), creating a Cartesian product.

**Correct Pattern (used by other views):**
```sql
LEFT JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")
```

This joins to the specific sales rep assigned to the order.

### Cross-View Investigation Results

| View | Employee JOIN Pattern | Has Duplicates? |
|------|----------------------|-----------------|
| **BGSalesByItemView** | `sg."Id" = e."BGSalesGroupLookupId"` | ⚠️ **BUG - 26x** |
| BGSalesByCustomerView | `o."BGSalesRepLookupId" = e."Id"` | ✅ Correct |
| BGSalesByItemLineView | `o."BGSalesRepLookupId" = e."Id"` | ✅ Correct |
| BGSalesBySalesGroupView | `o."BGSalesRepLookupId" = e."Id"` | ✅ Correct |
| BGCommissionReportDataView | Uses BGCommissionEarner | ✅ Correct |

**Key Finding:** ONLY BGSalesByItemView has this bug. All other views use the correct pattern.

### Reports Affected by Bug

1. **Items by Customer** - 26x duplicates
2. **Rpt Sales By Item** - 26x duplicates
3. **Rpt Sales By Item By Type** - 26x duplicates

### Reports NOT Affected (Correct Views)

- Customers Did Not Buy (BGSalesByCustomerView)
- Rpt Sales By Line (BGSalesByItemLineView)
- Rpt Sales By Sales Group (BGSalesBySalesGroupView)
- Rpt Commission (BGCommissionReportDataView)

### Files Created

| File | Purpose |
|------|---------|
| `sql/VwBGSalesByItemView_ORIGINAL.sql` | Archived buggy view definition |
| `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql` | **FIX** - Run in pgAdmin |
| `docs/investigation/DUPLICATE_ROWS_ANALYSIS.md` | Options analysis document |
| `docs/EXCEL_REPORTS_REVIEW.md` | All 8 Excel reports status |

### Documentation Updated

- `CLAUDE.md` - Added RPT-007 for duplicate rows issue
- `docs/EXCEL_REPORTS_REVIEW.md` - Updated with investigation results
- `docs/investigation/DUPLICATE_ROWS_ANALYSIS.md` - Added final findings

### Original BGSalesByItemView SQL (Buggy)

```sql
-- The problematic Employee JOIN:
JOIN "Employee" e ON ((sg."Id" = e."BGSalesGroupLookupId"))
-- This joins ALL employees in the sales group to each order
```

Full original saved to: `sql/VwBGSalesByItemView_ORIGINAL.sql`

### Fixed BGSalesByItemView SQL

```sql
-- The correct Employee JOIN:
LEFT JOIN "Employee" e ON ((o."BGSalesRepLookupId" = e."Id"))
-- This joins only the specific sales rep assigned to the order
```

Full fix saved to: `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql`

### Next Steps

1. ✅ **Run SQL fix in pgAdmin:** `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql` - APPLIED
2. **Test Items by Customer** - Verify no duplicate rows
3. **Test Rpt Sales By Item** - Verify no duplicate rows
4. **Test Rpt Sales By Item By Type** - Verify no duplicate rows

---

## Session 3b: PROD Report Configuration Discovery

### Critical Finding

User discovered PROD IntExcelReport configuration differs from documentation:

| Report | Documented View | Actual PROD View |
|--------|-----------------|------------------|
| Rpt Sales By Item | BGSalesByItemView | **BGSalesByItemLineView** |
| Rpt Sales By Item By Type Of Customer | BGSalesByItemView | **BGSalesByItemLineView** |
| Rpt Sales by Item Line | BGSalesByItemLineView | BGSalesByItemLineView |

### BGSalesByItemLineView Schema (PROD)

```
BGAmount          numeric
BGCustomer        character varying
BGCustomerType    character varying
BGDeliveryDate    date
BGDescription     text                      ← Product description (NOT BGProductDescription)
BGExecutionId     uuid                      ← Type A (Execution-Based) view
BGFilters         text
BGItem            character varying
BGLine            character varying
BGNumber          character varying
BGNumberInvoice   character varying
BGPONumber        character varying
BGPrice           numeric
BGQuantity        integer
BGReportEndDate   timestamp without time zone
BGReportStartDate timestamp without time zone
BGSalesGroup      character varying
BGSalesRep        character varying
BGShipDate        date
BGStatus          character varying
CreatedById       uuid
CreatedOn         timestamp without time zone
Id                uuid
ModifiedById      uuid
ModifiedOn        timestamp without time zone
ProcessListeners  integer
```

### Key Implications

1. **BGSalesByItemView fix may not affect these reports** - They use BGSalesByItemLineView
2. **Type A (Execution-Based) view** - Requires BGReportExecution records
3. **Different column name** - Uses `BGDescription` not `BGProductDescription`
4. **VBA Type mismatch** - Likely caused by execution-based filtering or column order

### Documentation Created

- `docs/investigation/BGSALESBYITEMLINEVIEW_SCHEMA.md`
- `docs/investigation/PROD_INTEXCELREPORT_CONFIGS.md`

---

## Session 3c: PROD IntExcelReport Deep Dive

### Critical Discovery

**ALL examined reports use Type A (Execution-Based) pattern with BGExecutionId filter!**

| Report | PROD View | Filter | Our Fix Applies? |
|--------|-----------|--------|------------------|
| Items by Customer | BGItemsByCustomerView | BGExecutionId = @P1@ | ❌ NO |
| Rpt Sales By Item | BGSalesByItemLineView | BGExecutionId = @P1@ | ❌ NO |
| Rpt Sales by Item Line | BGSalesByItemLineView | BGExecutionId = @P1@ | ❌ NO |
| Rpt Sales By Item By Type | BGSalesByItemLineView | BGExecutionId = @P1@ | ❌ NO |

### Documentation vs Reality Discrepancy

| Source | "Items by Customer" Config |
|--------|---------------------------|
| CLAUDE.md | BGSalesByItemView (changed) |
| PROD Screenshot | BGItemsByCustomerView (unchanged) |

**Explanation:** The IntExcelReport config was NEVER changed in PROD. Our custom generator bypasses it when filters are present.

### Why Reports Work Sometimes

```
WITH filters    → Custom generator → Queries BGSalesByItemView directly → Works ✅
WITHOUT filters → IntExcelExport → Uses BGItemsByCustomerView (empty) → FAILS ❌
```

This explains:
- 8,814 rows for Sisters (with filter) → Works
- VBA Type mismatch (no filters) → Fails

### The Real Problem

IntExcelExport is using execution-based views (BGItemsByCustomerView, BGSalesByItemLineView) that require BGReportExecution records, but:
1. BGItemsByCustomerView has **0 execution records**
2. Reports without filters fall back to IntExcelExport
3. IntExcelExport queries return empty/malformed data
4. VBA receives unexpected data → Type mismatch

### Options to Fix

**Option A:** Change IntExcelReport configs to use non-execution views
- Items by Customer → BGSalesByItemView (with proper filters)
- Rpt Sales By Item → BGSalesByItemView (with proper filters)

**Option B:** Make custom generators trigger always (not just with filters)
- Remove `if (hasFilter)` condition
- Add pagination/limits to prevent Excel row overflow

**Option C:** Fix the execution-based flow
- Create BGReportExecution records
- Complex, requires understanding BGlobal v7 pattern

---

## Session 2: DESCRIPCION Column Investigation (Afternoon)

### Issue Identified
- User reported "Items by Customer" DESCRIPCION column (D) shows order numbers instead of product descriptions
- Excel template expects product descriptions in Column D
- VBA macro reads Column D for DESCRIPCION

### Root Cause Analysis
- `BGSalesByItemView` has `BGItem` (product CODE) but NO product description column
- Backend `QuerySalesByItemData()` maps `BGNumber` (order number) to Column D "Product"
- Product entity HAS a `Description` column that can be joined via `Product.Code = BGItem`

### Investigation Completed
Ran 5 parallel subagent investigations with comprehensive findings:

| Investigation | Finding | Risk |
|--------------|---------|------|
| Environment Impact | View exists only in PampaBay package, no dependent views/triggers | LOW |
| UsrPage Frontend | Handler is decoupled from column structure | NONE |
| Backend Impact | Only 1 line change needed (line 1836) | LOW |
| Other Reports Impact | Only 3 reports use BGSalesByItemView | LOW |
| BGlobal v7 Pattern | "Items by Customer" was NEVER execution-based (0 records) | N/A |

### Documentation Created
- `docs/investigation/OPTION_A_ENVIRONMENT_IMPACT.md`
- `docs/investigation/OPTION_A_BACKEND_IMPACT.md`
- `docs/investigation/OPTION_A_USRPAGE_IMPACT.md`
- `docs/investigation/OPTION_A_OTHER_REPORTS_IMPACT.md`
- `docs/investigation/BGLOBAL_V7_EXECUTION_PATTERN.md`
- `docs/investigation/OPTION_A_IMPLEMENTATION_PLAN.md`

### Recommended Solution: Option A
1. **Modify BGSalesByItemView** to add `BGProductDescription` column (JOIN to Product entity)
2. **Update backend line 1836:** Change `BGNumber` to `BGProductDescription`

### Backend Deployment Issue (Earlier)
- Deployed UsrExcelReportService changes to PROD
- Environment became slow/unresponsive
- Created rollback file: `source-code/UsrExcelReportService_ROLLBACK.cs`
- After rollback applied, environment recovered
- May have been coincidental (app pool recycling), not the code

---

## Session 1: Original Tasks (Morning)

## Completed Today

### 1. Items by Customer Report - VBA Column Fix
- **Issue:** VBA macro reads columns by POSITION, not header name
- **Fix:** Reordered `QuerySalesByItemData()` column mapping to match VBA expectations
  - Column C = Amount (VBA sums this)
  - Column E = ProductCode (VBA groups by this)
- **File:** `source-code/UsrExcelReportService_Updated.cs` lines ~1826
- **Status:** ✅ Ready for deployment
- **PROD Test:** 8,814 rows for Sisters customer - working

### 2. Customers Did Not Buy - OutOfMemoryException Fix
- **Issue:** BGSalesByCustomerView queried without filters (millions of rows)
- **Root Cause:** IntExcelExport library doesn't inject date filters into ESQ
- **Fix:** Added custom generator that builds ESQ directly with filters
- **New Functions:**
  - `GenerateSalesByCustomerWithFilters()` - lines ~1966-2067
  - `QuerySalesByCustomerData()` - lines ~2068-2163
  - Updated `Generate()` routing - lines ~2507-2528
- **Status:** ✅ Ready for deployment

### 3. Extended BGSalesByItemView Generator
- **Change:** Now handles all reports using this view (Items by Customer, Sales By Item, Sales By Item By Type)
- **Routing:** Triggers when ANY filter is present (customer, dates, or status)
- **Status:** ✅ Ready for deployment

### 4. Documentation Created
- `docs/REPORT_FILTER_REQUIREMENTS.md` - Maps each report to required filters
- `docs/ITEMS_BY_CUSTOMER_VBA_FIX.md` - Documents VBA column order fix

### 5. Client Email Drafted
- Casual but informative email for Danlyn explaining:
  - Root cause (Creatio v7→v8 architectural change, not IWQBIntegration)
  - Why reverting wasn't an option
  - What's working vs. needs fine-tuning
  - Request for her help validating filters
  - Looker Studio access limitations
- **Status:** Draft ready, not sent

---

## Report-to-Generator Mapping (Final)

| Report | View Schema | Custom Generator | Required Filters |
|--------|-------------|------------------|------------------|
| Commission | BGCommissionReportDataView | Yes (ExecutionId) | YearMonth, SalesGroup |
| Items by Customer | BGSalesByItemView | ✅ Yes | Customer, Date, Status |
| Customers did not buy | BGSalesByCustomerView | ✅ Yes (NEW) | Date, Status |
| Sales By Item | BGSalesByItemView | ✅ Yes | Date, Status |
| Sales By Line | BGSalesByItemLineView | ⚠️ TBD | Date, Status |
| Sales By Item By Type | BGSalesByItemView | ✅ Yes | Date, Status |

---

## Pending Deployment

### Backend (UsrExcelReportService.cs)
**URL:** `https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178`

Copy from `source-code/UsrExcelReportService_Updated.cs`:
1. `GenerateSalesByCustomerWithFilters()` function (~lines 1966-2067)
2. `QuerySalesByCustomerData()` function (~lines 2068-2163)
3. Updated `Generate()` routing logic (~lines 2507-2528)
4. Updated `QuerySalesByItemData()` column order (~line 1826)

### Frontend (v54 - already correct)
- Customer ID extraction handles flat `{value: GUID}` format
- Filter visibility logic already in place
- No changes needed unless testing reveals issues

---

## Outstanding Items

| Item | Priority | Notes |
|------|----------|-------|
| Deploy backend to PROD | 🔴 High | Next session |
| Test "Customers did not buy" | 🔴 High | After deployment |
| Send email to Danlyn | 🟡 Medium | After deployment confirmed |
| Test Sales By Line | 🟡 Medium | May need BGSalesByItemLineView generator |
| Validate all report filters with client | 🟡 Medium | Coordinate with Danlyn |
| Looker Studio access | 🟢 Low | Requires BGlobal or client help |

---

## Key Learnings

1. **VBA macros are position-sensitive** - Always check Excel template expectations before changing column order
2. **IntExcelExport doesn't properly filter** - Custom generators required for large views
3. **IWQBIntegration was NOT the cause** - Confirmed after investigation; issue was v7→v8 framework incompatibility
4. **BGlobal packages affected:** `BGlobalLookerStudio`, `BGApp_eykaguu`

---

## Files Modified This Session

| File | Change |
|------|--------|
| `source-code/UsrExcelReportService_Updated.cs` | Added BGSalesByCustomerView generator, fixed column order, CreatedOn fix |
| `docs/REPORT_FILTER_REQUIREMENTS.md` | New - report filter mapping |
| `docs/ITEMS_BY_CUSTOMER_VBA_FIX.md` | New - VBA column fix documentation |
| `docs/SESSION_LOG_20260129.md` | New - this file |
| `sql/VwBGSalesByItemView_ORIGINAL.sql` | New - archived buggy view SQL |
| `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql` | New - **FIX** for Employee JOIN bug |
| `sql/VwBGSalesByItemView_REPLACE.sql` | New - single-line SQL for pgAdmin (includes BGProductDescription) |
| `docs/EXCEL_REPORTS_REVIEW.md` | New - comprehensive review of all 8 Excel reports |
| `docs/investigation/DUPLICATE_ROWS_ANALYSIS.md` | New - root cause analysis and options |
| `CLAUDE.md` | Updated - added RPT-007 (duplicate rows issue) |

---

## Session 4: Comprehensive Investigation & BGItemsByCustomerView Fix

### Deep Investigation Completed

Ran 5 parallel sub-agent investigations analyzing:
1. **Environment Impact** - BGSalesByItemView modification is LOW risk
2. **Frontend Impact** - NO changes needed (handler decoupled from columns)
3. **Backend Impact** - Single line change in routing logic
4. **Other Reports Impact** - Only 3 reports use BGSalesByItemView
5. **BGlobal v7 Execution Pattern** - Documents how Commission works vs. broken reports

### Critical Discovery

**PROD IntExcelReport configs differ from documentation:**

| Report | Documented View | Actual PROD View |
|--------|-----------------|------------------|
| Items by Customer | BGSalesByItemView | **BGItemsByCustomerView** |
| Rpt Sales By Item | BGSalesByItemView | **BGSalesByItemLineView** |

The SQL fix to BGSalesByItemView has **NO IMPACT** on these reports because they use different views!

### Root Cause of VBA Type Mismatch

- PROD uses `BGItemsByCustomerView` with `BGExecutionId = @P1@` filter
- **0 BGReportExecution records** exist for "Items by Customer"
- IntExcelExport returns empty/malformed data
- VBA receives unexpected structure → Type mismatch

### Fix Applied

**File:** `source-code/UsrExcelReportService_Updated.cs` lines 2512-2523

**Change:** Extended routing to include `BGItemsByCustomerView`:
```csharp
if (entitySchemaName == "BGSalesByItemView" || entitySchemaName == "BGItemsByCustomerView")
{
    // Always use custom generator - IntExcelExport fails for these views
    return GenerateSalesByItemWithFilters(userConnection, request);
}
```

**Impact:**
- "Items by Customer" will ALWAYS use custom generator
- Bypasses broken IntExcelExport flow (0 execution records)
- Works with or without filters

### Documentation Created

| File | Purpose |
|------|---------|
| `docs/investigation/OPTION_A_ENVIRONMENT_IMPACT.md` | View modification risk analysis |
| `docs/investigation/OPTION_A_USRPAGE_IMPACT.md` | Frontend impact (none) |
| `docs/investigation/OPTION_A_BACKEND_IMPACT.md` | Backend code analysis |
| `docs/investigation/OPTION_A_OTHER_REPORTS_IMPACT.md` | Other reports analysis |
| `docs/investigation/BGLOBAL_V7_EXECUTION_PATTERN.md` | BGExecutionId pattern explained |
| `docs/investigation/PROD_INTEXCELREPORT_CONFIGS.md` | PROD config screenshots |
| `docs/investigation/BGSALESBYITEMLINEVIEW_SCHEMA.md` | View schema documentation |
| `docs/COMPREHENSIVE_INVESTIGATION_SUMMARY.md` | All findings synthesized |
| `docs/investigation/REPORT_COLUMN_COMPATIBILITY_ANALYSIS.md` | Column structure comparison |

### Deployment & Verification

1. ✅ **Backend deployed to PROD** - Full UsrExcelReportService_Updated.cs
2. ✅ **Tested "Items by Customer" with customer only** - Downloaded successfully (Items+by+Customer (15).xlsm)
3. 🟡 **Test "Rpt Sales By Item"** - May need separate generator (different columns)

### Result: RPT-008 FIXED

"Items by Customer" now works with customer filter alone (no date filters required). VBA Type mismatch error resolved.

---

## Session 5: "Customers Did Not Buy" Column Mismatch Investigation

### Issue Discovered

User tested "Customers did not buy over a period of time" report. File downloaded but **columns are completely misaligned**.

**Rpt Sheet Output (wrong):**
```
Customer    Address    City    State    Zip Code    Email    Phone    Last Order Date...
Active      Cotton+Oak 46048   46048    46045       1252     DAL126   ORD-16351...
```

The VBA expects customer contact data but received order data with dates showing as Excel serial numbers.

### Root Cause: Wrong View in Backend

**PROD IntExcelReport Config (from screenshot):**
- **Entity Schema:** `BGCustomerDidNotBuyView` (NOT BGSalesByCustomerView!)
- **Filter:** `BGExecutionId = @P1@` (execution-based)

**Expected Columns:**
| Position | Column Name | Description |
|----------|-------------|-------------|
| A | Account | Customer name |
| B | Address | Customer address |
| C | City | City |
| D | State | State |
| E | ZIP | Zip code |
| F | Email | Customer email |
| G | Phone | Phone number |
| H | Last Order Date | Date |
| I | Last Order Amount | Amount |
| J | Previous Order Count | Count |
| K | Last Order Sales Rep | Sales rep name |
| L | Last Order Sales Group | Sales group name |

**Current Backend (`QuerySalesByCustomerData`):**
Queries `BGSalesByCustomerView` with order columns:
- BGStatus, BGCustomer, BGShipDate, BGInvoiceDate, BGDeliveryDate, BGAmount, BGPONumber, BGNumber, BGNumberInvoice, BGInvoiceNumber, BGSalesRep, BGSalesGroup

**Mismatch:** Backend queries wrong view with wrong columns!

### Fix Applied

**File:** `source-code/UsrExcelReportService_Updated.cs`

1. ✅ Added new routing for `BGCustomerDidNotBuyView` (lines ~2741-2748)
2. ✅ Created `GenerateCustomerDidNotBuyWithFilters()` function
3. ✅ Created `QueryCustomerDidNotBuyData()` function with correct columns:
   - Account, Address, City, State, ZIP, Email, Phone
   - Last Order Date, Last Order Amount, Previous Order Count
   - Last Order Sales Rep, Last Order Sales Group

**Deployment Required:** Copy full `UsrExcelReportService_Updated.cs` to PROD

---

## Session 6: ROOT CAUSE FOUND - IntEntitySchemaName Column Missing (2026-01-29)

### Problem: Routing Still Not Triggering

After deploying the BGCustomerDidNotBuyView routing, the report still showed wrong columns (BGSalesByCustomerView columns like BGStatus, BGCustomer, BGShipDate instead of Account, Address, City, State).

### Deep Investigation

Traced through documentation and code to find why `GetReportEntitySchemaName()` was not returning "BGCustomerDidNotBuyView".

**Critical Finding from MASTER_CATALOG.md (line 69):**
> `IntEntitySchemaName` column does NOT exist (schema different than assumed).

This explains everything!

### Root Cause Analysis

**The `GetReportEntitySchemaName()` function has 3 fallback levels:**
1. Try `IntEntitySchemaName.Name` lookup display name → **FAILS** (column doesn't exist!)
2. Try `IntEntitySchemaNameId` GUID via SysSchema lookup → **FAILS** (column doesn't exist!)
3. Parse `IntEsq` JSON for `rootSchemaName` → **SUCCEEDS** but returns **WRONG VALUE**

**The IntEsq JSON contains:**
```json
{
  "rootSchemaName": "BGSalesByCustomerView",
  ...
}
```

This was historically set when the report was created. The UI may show "BGCustomerDidNotBuyView" but the underlying IntEsq JSON contains "BGSalesByCustomerView".

### Code Flow

```
1. Report request comes in with ReportId = 1f65a56a-d7f4-4ce2-b517-c633872ea545
2. GetReportEntitySchemaName() is called
3. Tries IntEntitySchemaName → FAILS (column doesn't exist)
4. Tries IntEntitySchemaNameId → FAILS (column doesn't exist)
5. Parses IntEsq JSON → finds "rootSchemaName": "BGSalesByCustomerView"
6. Returns "BGSalesByCustomerView"
7. Routing check: entitySchemaName == "BGCustomerDidNotBuyView" → FALSE
8. Falls through to BGSalesByCustomerView routing with date filters
9. Calls GenerateSalesByCustomerWithFilters() which queries WRONG columns
```

### The Fix

**Solution: Route by report name (IntName) instead of schema name**

1. **Added `GetReportName()` helper function** (lines 675-686):
```csharp
private string GetReportName(UserConnection userConnection, Guid reportId)
{
    var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
    esq.AddColumn("IntName");
    var entity = esq.GetEntity(userConnection, reportId);
    if (entity == null) return null;
    return entity.GetTypedColumnValue<string>("IntName");
}
```

2. **Updated routing logic** (lines 2754-2766):
```csharp
// CUSTOMERS DID NOT BUY FIX: Route by report name (IntName)
// CRITICAL: IntEntitySchemaName column does NOT exist in IntExcelReport table
// GetReportEntitySchemaName() falls back to parsing IntEsq JSON for rootSchemaName
// IntEsq has rootSchemaName = "BGSalesByCustomerView" which is the WRONG view
var reportName = GetReportName(userConnection, request.ReportId);
if (reportName == "Rpt CustomersDidNotBuyOverAPeriodOfTime" ||
    entitySchemaName == "BGCustomerDidNotBuyView")
{
    return GenerateCustomerDidNotBuyWithFilters(userConnection, request);
}
```

### Files Changed

| File | Change |
|------|--------|
| `source-code/UsrExcelReportService_Updated.cs` | Added `GetReportName()` helper, updated routing to check by report name |

### Why This Wasn't Caught Earlier

1. Documentation said PROD IntExcelReport showed "Entity Schema: BGCustomerDidNotBuyView"
2. But this was the UI display, not the actual data in IntEsq JSON
3. The IntEntitySchemaName column simply doesn't exist in IntExcelReport schema
4. All routing relies on IntEsq.rootSchemaName which has the OLD value

### Lessons Learned

1. **Always verify column existence** before assuming lookup patterns will work
2. **IntEsq JSON is the source of truth** for entity schema name in BGlobal's IntExcelExport
3. **Route by report name** when schema name resolution is unreliable
4. **Documentation can be misleading** - UI display vs actual data structure

### Next Steps

**DEPLOY UPDATED FILE TO PROD:**
1. Copy full `UsrExcelReportService_Updated.cs` to PROD
2. Test "Customers did not buy" report with date filters
3. Expected: Columns should now be Account, Address, City, State, ZIP, etc.

---

*Session 6 completed: 2026-01-29*

---

## Session 7: Ralph Loop - Validation & Documentation (2026-01-29)

### Work Completed

1. **Code Review - PASSED**
   - Verified `GetReportName()` helper function (lines 675-686)
   - Verified routing logic update (lines 2754-2766)
   - Verified all three custom generators follow consistent pattern

2. **Documentation Created**
   - Created `docs/RPT005_DEPLOYMENT_CHECKLIST.md` with full deployment steps
   - Added risk documentation and rollback plan
   - Updated `CLAUDE.md` documentation index

3. **Code Consistency Verified**
   - All generators use same error handling pattern
   - Template file check, query with try/catch, empty data handling, row limit, Excel population

### Additional Finding: BGSalesByItemLineView Reports

**Potential Issue Identified:**
Three reports use `BGSalesByItemLineView` but have NO custom generator routing:
- Rpt Sales By Item
- Rpt Sales by Item Line
- Rpt Sales By Item By Type Of Customer

Per COMPREHENSIVE_INVESTIGATION_SUMMARY.md, "Sales By Item" has **0 BGReportExecution records**, which means it may fail the same way "Customers did not buy" was failing.

**Risk:** These reports may show similar column mismatch issues when tested.

**Recommendation:** After RPT-005 deployment is verified, investigate BGSalesByItemLineView reports and potentially add similar report-name-based routing.

**NOT fixing now:** Per user instruction to avoid breaking changes during this session.

---

*Session 7 (Ralph Loop) completed: 2026-01-29*

---

## Session 8: Post-Deployment Testing (2026-01-29)

### User Action
User deployed `UsrExcelReportService_Updated.cs` to PROD and requested testing.

### API Testing Attempted

**Test 1: DEV Environment**
```
CREATIO_URL: https://dev-pampabay.creatio.com
REPORT_ID: 1f65a56a-d7f4-4ce2-b517-c633872ea545
```

**DEV Response:**
```json
{
  "IntName": "Rpt Customer Did Not Buy",
  "IntEntitySchemaName": {
    "value": "10647dfc-f999-4cf7-a17c-52a070c36ee6",
    "displayValue": "BGCustomerDidNotBuyView"
  },
  "IntEsq length": 0
}
```

**Result:** Failed with IntExcelExport library error:
```
ArgumentNullOrEmptyException: Value for argument "queryConfig" must be specified.
```

**Analysis:**
- IntEntitySchemaName column EXISTS in DEV and returns `BGCustomerDidNotBuyView`
- IntEsq is EMPTY (length 0)
- Code is falling through to IntExcelExport library instead of our custom generator

### Critical Discovery: IntName Mismatch

| Source | IntName Value |
|--------|---------------|
| MASTER_CATALOG.md | `Rpt CustomersDidNotBuyOverAPeriodOfTime` |
| DEV API Response | `Rpt Customer Did Not Buy` |
| Our Routing Code | Checks for `Rpt CustomersDidNotBuyOverAPeriodOfTime` |

**Problem:** Our routing checks for `"Rpt CustomersDidNotBuyOverAPeriodOfTime"` but actual IntName in DEV is `"Rpt Customer Did Not Buy"`.

**Test 2: PROD Environment**
```
CREATIO_URL: https://pampabay.creatio.com
```

**Result:** 401 Unauthorized - API credentials don't work for PROD.

### Current Status

1. **Code Deployed to PROD:** ✅ User confirmed
2. **API Test DEV:** ❌ Failed - IntEsq empty, falls to library
3. **API Test PROD:** ❌ Cannot test - auth issue
4. **Manual Test PROD:** ⏳ Pending user verification

### Potential Issues Identified

**Issue 1: IntName Mismatch**
- Code checks: `reportName == "Rpt CustomersDidNotBuyOverAPeriodOfTime"`
- Actual value: `"Rpt Customer Did Not Buy"` (in DEV)
- **Fix Needed:** Update routing to check for actual IntName

**Issue 2: entitySchemaName Check May Fail**
- If `GetReportEntitySchemaName()` returns null (empty IntEsq, no IntEntitySchemaName lookup success)
- Then `entitySchemaName == "BGCustomerDidNotBuyView"` check fails
- Code falls through to IntExcelExport library

### Files Created This Session

| File | Purpose |
|------|---------|
| `docs/RPT005_DEPLOYMENT_CHECKLIST.md` | Deployment steps and verification checklist |
| `docs/FUTURE_ISSUES_TRACKING.md` | Tracking BGSalesByItemLineView reports for future fix |

### Files Updated This Session

| File | Changes |
|------|---------|
| `source-code/UsrExcelReportService_Updated.cs` | Added `GetReportName()`, updated routing |
| `docs/SESSION_LOG_20260129.md` | Session 6, 7, 8 documentation |
| `CLAUDE.md` | Updated status, documentation index |

### Recommended Next Steps

1. **Update routing to match actual IntName:**
   ```csharp
   if (reportName == "Rpt CustomersDidNotBuyOverAPeriodOfTime" ||
       reportName == "Rpt Customer Did Not Buy" ||  // ADD THIS
       entitySchemaName == "BGCustomerDidNotBuyView")
   ```

2. **Manual PROD Test:** User needs to test in browser:
   - Go to Pampa Reports > Customers did not buy
   - Set date filters
   - Generate report
   - Verify column headers: Account, Address, City, State, ZIP...

3. **Verify PROD IntName:** Confirm what the actual IntName is in PROD (may differ from DEV)

---

## Summary of All Work Done (Sessions 6-8)

### Session 6: Root Cause Discovery
- **Found:** `IntEntitySchemaName` column doesn't exist (per MASTER_CATALOG)
- **Found:** `GetReportEntitySchemaName()` falls back to IntEsq parsing
- **Found:** IntEsq has `rootSchemaName = "BGSalesByCustomerView"` (wrong)
- **Created:** `GetReportName()` helper function
- **Updated:** Routing to check by report IntName

### Session 7: Ralph Loop Validation
- **Verified:** Code consistency across all generators
- **Created:** `docs/RPT005_DEPLOYMENT_CHECKLIST.md`
- **Created:** `docs/FUTURE_ISSUES_TRACKING.md`
- **Identified:** BGSalesByItemLineView reports may have similar issues
- **Updated:** CLAUDE.md documentation index

### Session 8: Post-Deployment Testing
- **Tested:** DEV API - revealed IntName mismatch
- **Found:** Actual IntName is `"Rpt Customer Did Not Buy"` not `"Rpt CustomersDidNotBuyOverAPeriodOfTime"`
- **Found:** IntEntitySchemaName column DOES exist in DEV (contrary to MASTER_CATALOG)
- **Blocked:** PROD API test - auth credentials don't work
- **Pending:** Manual PROD verification by user

---

*Session 8 completed: 2026-01-29*

---

## Session 9: Documentation Restructure (2026-01-30)

### User Request
"log everything done. without removing anything. restructure our docs and logs and whatever else we are using to document all work, instructions, interactions, etc. claude.md needs to be the brain for AI instructions"

### Actions Taken

**1. Created New Directory Structure**
```
docs/
├── logs/           # Session logs, action logs, test logs (9 files)
├── issues/         # Issue-specific investigation & fixes (14 files)
├── investigation/  # Deep technical analysis (13 files)
├── reference/      # System knowledge & catalogs (20 files)
├── deployment/     # Deployment guides & checklists (7 files)
├── communication/  # Emails, meeting notes, summaries (8 files)
├── qb-sync/        # QuickBooks sync documentation (8 files)
└── archive/        # Older/completed docs (5 files)
```

**2. Reorganized 84 Markdown Files**

| Category | Files Moved | Purpose |
|----------|-------------|---------|
| logs/ | 9 | SESSION_LOG_*, TEST_LOG, ACTION_LOG, etc. |
| issues/ | 14 | ITEMS_BY_CUSTOMER_*, UI002_*, RPT005_*, etc. |
| investigation/ | 13 | COMPREHENSIVE_*, BGLOBAL_*, OPTION_A_* |
| reference/ | 20 | MASTER_CATALOG, HANDLER_VERSION_HISTORY, etc. |
| deployment/ | 7 | V19_*, PROD_DEPLOYMENT_PLAN, etc. |
| communication/ | 8 | EMAIL_*, TEAM_SUMMARY_*, etc. |
| qb-sync/ | 8 | QB_SYNC_*, SYNC_003_*, etc. |
| archive/ | 5 | CURRENT_STATUS, QUICK_REFERENCE, etc. |

**3. Rewrote CLAUDE.md as Central "Brain"**
- Reduced from ~360 lines to ~220 lines
- Added Quick Navigation table at top
- Consolidated issues into priority-ordered tables (🔴/🟡/✅)
- Added Documentation Structure tree view
- Kept AI Instructions, Rules, and Lessons Learned
- Collapsed resolved issues into expandable `<details>` sections

**4. Created README.md for Each Subdirectory**
- `docs/README.md` - Main index with directory structure
- `docs/logs/README.md` - Session log navigation
- `docs/issues/README.md` - Issue-specific index
- `docs/investigation/README.md` - Investigation index
- `docs/reference/README.md` - Reference documentation index
- `docs/deployment/README.md` - Deployment guide index
- `docs/communication/README.md` - Communication index
- `docs/qb-sync/README.md` - QB sync documentation index
- `docs/archive/README.md` - Archive index

### Files Created

| File | Purpose |
|------|---------|
| `docs/logs/README.md` | Session log navigation |
| `docs/issues/README.md` | Issue-specific index |
| `docs/investigation/README.md` | Investigation index |
| `docs/reference/README.md` | Reference documentation index |
| `docs/deployment/README.md` | Deployment guide index |
| `docs/communication/README.md` | Communication index |
| `docs/qb-sync/README.md` | QB sync documentation index |
| `docs/archive/README.md` | Archive index |

### Files Modified

| File | Changes |
|------|---------|
| `CLAUDE.md` | Complete rewrite as hub/brain |
| `docs/README.md` | Updated to reflect new structure |
| `docs/logs/SESSION_LOG_20260129.md` | Added Session 9 entry |

### Benefits of New Structure

1. **AI Context Loading:** Clear directory structure means AI can load only relevant docs
2. **Quick Navigation:** CLAUDE.md has table linking needs to locations
3. **Discoverability:** Each folder has README explaining contents
4. **Maintainability:** New docs go to obvious locations
5. **Nothing Removed:** All 84 files preserved, just reorganized

---

*Session 9 completed: 2026-01-30*

---

## Session 10: Workflow Prominence Update (2026-01-30)

### User Request
"ensure our workflow that we mentioned in the past is also on the forefront of claude.md"

### Actions Taken

**1. Added "🧠 Workflow (READ THIS FIRST)" Section**
- Moved to position #1 (right after status line)
- Added "The Three Pillars" table (Plan First, Verify Always, Update CLAUDE.md)
- Added "Session Start Checklist" for AI agents
- Added "Verification Commands" quick reference
- Added "When to Use Plan Mode" guidance

**2. Updated AI Instructions Section**
- Separated general rules from Creatio-specific rules
- Made rules more actionable

### New CLAUDE.md Structure

```
1. Status line
2. 🧠 Workflow (READ THIS FIRST)  ← NEW PROMINENT POSITION
   - The Three Pillars
   - Session Start Checklist
   - Verification Commands
   - When to Use Plan Mode
3. Quick Navigation
4. Active Issues
5. Quick Deploy
6. Documentation Structure
7. Key Files
8. AI Instructions
9. Reference Data
10. Scripts
```

### Key Workflow Elements Now Prominent

| Element | Description |
|---------|-------------|
| **Plan First** | Use Plan mode (`shift+tab` x2) for complex changes |
| **Verify Always** | Run tests before considering work complete |
| **Update CLAUDE.md** | Add lessons learned when Claude makes mistakes |
| **Session Start Checklist** | 4-step checklist for AI session startup |
| **When to Use Plan Mode** | Clear guidance on Plan vs direct implementation |

---

*Session 10 completed: 2026-01-30*

---

## Session 11: Project Direction Change - QB Integration Focus (2026-01-30)

### Email Received from Danlyn

> "Thank you! Now that it is clear that the reports broke due to Creatio pushing through the update, we can take this off your plate. We will need to rework these reports to make them workable with version 8. I will need to follow up with Rommel on what needs to be done.
>
> We really appreciate all your work on this. I'm sure we'll circle back when it is time to produce the commissions reports. Perhaps that is something that should be tackled with Rommel as he'll be working on updating the reports to make them suitable for version 8.
>
> In the meantime, Carlos would like to press forward with the QB integration. As I mentioned above, let's leave the commission reports for now and circle back. I will manually process them from QB this month.
>
> What are our next steps for the QB integration? I believe, the last time we spoke everything was in working order. Can we set a go-live date?"

### Key Takeaways

1. **Reports work handed off** - BGlobal/Rommel will handle v8 rework
2. **Commission reports** - Danlyn will process manually from QB this month
3. **Focus now: QB Integration** - Carlos wants to go-live
4. **Question:** What are next steps? Can we set go-live date?

### QB Integration Current Status

| Component | Status |
|-----------|--------|
| QB Web Connector | ✅ Online (was offline, now working) |
| Order Sync | ✅ 336 orders synced successfully |
| QB Customer Order Integration | ✅ Deployed to PROD |
| Commission Sync Process | ✅ Phase 1 deployed |

### Remaining Items

| Item | Priority | Blocking? |
|------|----------|-----------|
| SYNC-005: 637 false "Processed" orders | Low | No |
| SYNC-003: 20K batch limit (DEV only) | Low | No |
| Monitor stability (24-48 hours) | Medium | Recommended |

### Suggested Response Points

1. **QB Integration is ready** - Last tests showed everything working
2. **QB Web Connector is online** - Was down, now syncing successfully
3. **Go-live date** - Can set after 24-48 hour stability monitoring
4. **Cleanup items** - 637 false "Processed" orders can be reset post-go-live

### CLAUDE.md Updated

- Status changed to "REPORTS HANDED OFF | QB INTEGRATION FOCUS"
- Added QB Integration Go-Live Status section
- Moved reports issues to "Handed Off" section

---

*Session 11 in progress: 2026-01-30*
