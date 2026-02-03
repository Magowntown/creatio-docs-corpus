# RPT-005: Comprehensive Review Before Fix

**Date:** 2026-01-30
**Report:** "Customers did not buy over a period of time"
**IntExcelReport ID:** `1f65a56a-d7f4-4ce2-b517-c633872ea545`

---

## PROD OData Investigation Results (2026-01-30)

### IntExcelReport Configuration (PROD)

| Field | PROD Value | Status |
|-------|------------|--------|
| **IntName** | `Rpt CustomersDidNotBuyOverAPeriodOfTime` | ✅ Matches code check |
| **IntEntitySchemaNameId** | `00000000-0000-0000-0000-000000000000` (null) | ⚠️ Not set |
| **IntEntitySchemaId** | `d55e4a0b-b161-4dfb-a5ff-deb46016e90f` | ❌ Points to BGSalesByCustomerView |
| **IntEsq rootSchemaName** | `BGSalesByCustomerView` | ❌ **WRONG VIEW** |
| **IntSheetName** | `Data` | ✅ |
| **IntFiltersConfig** | Column does NOT exist in OData | N/A |
| **Created** | 2024-11-14 | Info |
| **Modified** | 2026-01-19 | Info |

### IntEsq JSON Analysis

The IntEsq field contains a complete ESQ definition with **wrong view** and **wrong columns**:

```json
{
  "rootSchemaName": "BGSalesByCustomerView",  // ❌ WRONG - should be BGCustomerDidNotBuyView
  "columns": {
    "BGStatus": {...},           // ❌ Sales column - not customer contact
    "BGCustomer": {...},         // ❌ Sales column
    "BGShipDate": {...},         // ❌ Sales column
    "BGInvoiceDate": {...},      // ❌ Sales column
    "BGAmount": {...},           // ❌ Sales column
    "BGPONumber": {...},         // ❌ Sales column
    "BGNumber": {...},           // ❌ Sales column
    "BGDeliveryDate": {...},     // ❌ Sales column
    "BGNumberInvoice": {...},    // ❌ Sales column
    "BGInvoiceNumber": {...},    // ❌ Sales column
    "BGSalesRep": {...},         // ❌ Sales column
    "BGSalesGroup": {...},       // ❌ Sales column
    "BGReportEndDate": {...},    // Filter column
    "BGReportStartDate": {...},  // Filter column
    "BGExecutionId": {...},      // Execution-based pattern
    "BGFilters": {...}           // Filter metadata
  }
}
```

### BGCustomerDidNotBuyView (PROD)

**Schema ID:** `10647dfc-f999-4cf7-a17c-52a070c36ee6`
**Exists:** ✅ Yes

**Actual Columns (from OData $top=1):**
| Column | Type | Purpose |
|--------|------|---------|
| `Id` | GUID | Primary key |
| `CreatedOn` | DateTime | System |
| `CreatedById` | GUID | System |
| `ModifiedOn` | DateTime | System |
| `ModifiedById` | GUID | System |
| `ProcessListeners` | Int | System |
| `BGPreviousOrderCount` | Int | Order history |
| `BGLastOrderId` | GUID | Order FK |
| `BGAccountId` | GUID | **Account FK** |
| `BGEmail` | String | Customer email |
| `BGFilters` | String | Filter metadata (e.g., "Created Date: 01/01/2025 to 01/31/2025") |
| `BGExecutionId` | GUID | **Execution-based pattern** |

**Sample Data:**
```json
{
  "BGAccountId": "0003020d-a49f-477f-ab52-3e222d7d57fa",
  "BGEmail": "jamie.rowley@fab.com",
  "BGPreviousOrderCount": 0,
  "BGFilters": "Created Date: 01/01/2025 to 01/31/2025",
  "BGExecutionId": "349f92e2-119f-4605-af46-4c72bf0beff0"
}
```

**Expanded Account (via $expand):**
```json
{
  "BGAccount": {
    "Id": "0003020d-a49f-477f-ab52-3e222d7d57fa",
    "Name": "FAB",
    "Phone": "",
    "Address": "95 Morton Street, 8th Floor.",
    "Zip": "10014"
  }
}
```

### BGSalesByCustomerView (PROD - for comparison)

**Actual Columns:**
- `Id`, `CreatedOn`, `CreatedById`, `ModifiedOn`, `ModifiedById`, `ProcessListeners`
- `BGStatus`, `BGCustomer`, `BGShipDate`, `BGInvoiceDate`, `BGAmount`
- `BGPONumber`, `BGNumber`, `BGDeliveryDate`, `BGNumberInvoice`, `BGInvoiceNumber`
- `BGSalesRep`, `BGSalesGroup`, `BGReportEndDate`, `BGReportStartDate`
- `BGExecutionId`, `BGFilters`

### BGReportExecution Records (PROD)

**Recent 20 records:** ALL are "Commission" reports
**"Customers did not buy" records:** NONE found in recent history

**Pattern Implication:** "Customers did not buy" may use:
1. A different execution pattern (not BGReportExecution-based), OR
2. Execution records exist but are older, OR
3. The report has never been successfully generated

---

## Root Cause Analysis

### The Core Problem

1. **IntExcelReport.IntEsq points to WRONG view:** `BGSalesByCustomerView`
2. **Backend routing works correctly** - it detects `Rpt CustomersDidNotBuyOverAPeriodOfTime` and routes to `GenerateCustomerDidNotBuyWithFilters()`
3. **Backend generator has WRONG column mapping:**

   Current backend expects these columns from `BGCustomerDidNotBuyView`:
   ```csharp
   Account, Address, City, State, ZIP, Email, Phone, LastOrderDate,
   LastOrderAmount, PreviousOrderCount, LastOrderSalesRep, LastOrderSalesGroup
   ```

   But the actual view only has:
   ```
   BGPreviousOrderCount, BGLastOrderId, BGAccountId, BGEmail, BGFilters, BGExecutionId
   ```

4. **Customer contact info must be JOINed from Account table** via `BGAccountId`

### Why Report Shows Wrong Columns

If the backend generator fails (columns not found), it may fall through to the default IntExcelExport library path which:
1. Uses the IntEsq JSON
2. Queries `BGSalesByCustomerView` (wrong view)
3. Returns sales columns instead of customer contact columns

---

## Correct Fix Strategy

### Option 1: Fix Backend Generator ESQ (Recommended)

Update `QueryCustomerDidNotBuyData()` in `UsrExcelReportService_Updated.cs` to use proper ESQ relationship columns:

```csharp
var columnMapping = new List<Tuple<string, string>>
{
    // Direct from view
    Tuple.Create("BGAccount.Name", "Account"),           // Column A: Customer name
    Tuple.Create("BGAccount.Address", "Address"),        // Column B: Address
    Tuple.Create("BGAccount.City.Name", "City"),         // Column C: City (lookup)
    Tuple.Create("BGAccount.Region.Name", "State"),      // Column D: State (lookup)
    Tuple.Create("BGAccount.Zip", "ZIP"),                // Column E: Zip Code
    Tuple.Create("BGEmail", "Email"),                    // Column F: Email (direct)
    Tuple.Create("BGAccount.Phone", "Phone"),            // Column G: Phone
    // Optional - if Excel template expects these:
    Tuple.Create("BGLastOrder.Date", "Last Order Date"), // Column H: Last Order Date
    Tuple.Create("BGLastOrder.Amount", "Last Order Amount"), // Column I: Amount
    Tuple.Create("BGPreviousOrderCount", "Previous Order Count"), // Column J: Count
};
```

**Key Changes:**
1. Use `BGAccount.` prefix for Account relationship columns
2. Use `BGAccount.City.Name` and `BGAccount.Region.Name` for lookup display values
3. Use `BGLastOrder.` prefix for Order relationship columns
4. Remove non-existent columns (Account, Address, City, State, ZIP, etc.)

### Option 2: Use Execution-Based Pattern (BGlobal's Original)

The view HAS `BGExecutionId` column, confirming it uses execution-based pattern:
1. The IntExcelExport library SHOULD:
   - Create `BGReportExecution` record with filters
   - Query view WHERE `BGExecutionId = @executionId`
   - The view's underlying SQL already does the JOINs
2. **BUT:** IntExcelReport.IntEsq points to WRONG view (BGSalesByCustomerView)
3. Fix requires updating IntEsq in PROD IntExcelReport record

### Option 3: Fix IntExcelReport Configuration (Long-term)

Update the PROD IntExcelReport record:
1. Change `IntEsq.rootSchemaName` to `BGCustomerDidNotBuyView`
2. Update `IntEsq.columns` to use relationship columns:
   ```json
   {
     "BGAccount.Name": {...},
     "BGAccount.Address": {...},
     "BGAccount.City.Name": {...},
     "BGAccount.Region.Name": {...},
     "BGAccount.Zip": {...},
     "BGEmail": {...},
     "BGAccount.Phone": {...}
   }
   ```
3. This would let IntExcelExport library work correctly

### Recommended Approach

**Short-term:** Fix Option 1 (Backend ESQ) - minimal risk, quick deploy
**Long-term:** Fix Option 3 (IntExcelReport config) - proper BGlobal pattern

## Verified PROD Data via OData $expand

**BGCustomerDidNotBuyView with $expand=BGAccount:**
```json
{
  "BGAccountId": "0003020d-a49f-477f-ab52-3e222d7d57fa",
  "BGEmail": "jamie.rowley@fab.com",
  "BGPreviousOrderCount": 0,
  "BGExecutionId": "349f92e2-119f-4605-af46-4c72bf0beff0",
  "BGFilters": "Created Date: 01/01/2025 to 01/31/2025",
  "BGAccount": {
    "Id": "0003020d-a49f-477f-ab52-3e222d7d57fa",
    "Name": "FAB",
    "Phone": "",
    "Address": "95 Morton Street, 8th Floor.",
    "Zip": "10014",
    "CityId": "24c7b5ed-446d-4608-8a1c-141fcce20953",
    "RegionId": "00b03270-f36b-1410-fd98-00155d043204"
  }
}
```

**Note:** City and Region are lookup IDs, not display values. ESQ must use `.Name` path.

---

## Updated Review Checklist

### 1. Packages Managing Report Pages

| Package | Role | Verified |
|---------|------|----------|
| **BGApp_eykaguu** | Child handler (UsrPage_ebkv9e8), Backend service (UsrExcelReportService) | ✅ Confirmed |
| **BGlobalLookerStudio** | Parent handler (UsrPage_ebkv9e8), UsrIframe component | ✅ Confirmed |
| **PampaBay** | Report views, BGIntExcelreportMixin, SQL scripts | ⏳ Need SQL review |
| **PampaBayQuickBooks** | Commission views, QB integration | N/A (different report) |
| **IntExcelExport** | Excel generation library (BGlobal) | ✅ Falls back to this |
| **Custom** | UsrReportesPampa entity extension | ⏳ |

### 2. Artifacts Verified

| Artifact Type | Item | Status | Finding |
|---------------|------|--------|---------|
| **IntExcelReport** | `1f65a56a-d7f4-4ce2-b517-c633872ea545` | ✅ | IntEsq points to WRONG view |
| **Entity Schema** | BGCustomerDidNotBuyView | ✅ | Has BGAccountId FK, uses execution pattern |
| **Entity Schema** | BGSalesByCustomerView | ✅ | Sales columns, not customer contact |
| **Source Code** | UsrExcelReportService | ✅ | Routing correct, column mapping WRONG |
| **BGReportExecution** | For this report | ❓ | None in recent history |

### 3. Questions Answered

| Question | Answer |
|----------|--------|
| What is the exact IntName in PROD? | ✅ `Rpt CustomersDidNotBuyOverAPeriodOfTime` |
| Does IntEntitySchemaName column exist? | ❌ No (IntEntitySchemaNameId is null GUID) |
| What columns does BGCustomerDidNotBuyView have? | ✅ See above (BGAccountId FK, BGEmail, BGPreviousOrderCount, BGExecutionId) |
| Is there a custom generator? | ✅ Yes, but column mapping is wrong |
| What filters should show? | Date filters (CreatedFrom/CreatedTo) |
| Conflict with Sales By Customer? | ⚠️ Yes - both may route to BGSalesByCustomerView fallback |

---

## BGlobal V7 Original SQL View Definition (Extracted)

The actual `BGCustomerDidNotBuyView` SQL was extracted from the PampaBay package:

**Key Design:**
1. **Type A (Execution-Based):** `JOIN "BGReportExecution" AS re ON true`
2. **Filters from BGReportExecution:** Uses `re."BGCreatedFrom"`, `re."BGCreatedTo"`
3. **NOT EXISTS logic:** Finds customers who have NO orders in the date range
4. **Only outputs Account ID:** Customer details (Name, Address, City) must come via ESQ relationship columns

**View Columns:**
| Column | Source | Notes |
|--------|--------|-------|
| `Id` | Account.Id | Primary key |
| `BGAccountId` | Account.Id | FK to Account |
| `BGLastOrderId` | Subquery | Most recent order before date range |
| `BGEmail` | Subquery | From AccountCommunication |
| `BGPreviousOrderCount` | Subquery | Count of orders before date range |
| `BGFilters` | Computed | Human-readable date string |
| `BGExecutionId` | BGReportExecution.Id | Execution-based filtering |

**Full SQL saved to:** `sql/BGCustomerDidNotBuyView_ORIGINAL.sql`

---

## Correct Fix: Use ESQ Relationship Columns

Based on BGlobal's original design, the backend must use **ESQ relationship columns** to get Account details:

```csharp
// Correct column mapping for QueryCustomerDidNotBuyData()
var columnMapping = new List<Tuple<string, string>>
{
    // Relationship columns (via BGAccountId FK)
    Tuple.Create("BGAccount.Name", "Account"),           // Column A
    Tuple.Create("BGAccount.Address", "Address"),        // Column B
    Tuple.Create("BGAccount.City.Name", "City"),         // Column C (lookup)
    Tuple.Create("BGAccount.Region.Name", "State"),      // Column D (lookup)
    Tuple.Create("BGAccount.Zip", "ZIP"),                // Column E
    Tuple.Create("BGAccount.Phone", "Phone"),            // Column F

    // Direct columns from view
    Tuple.Create("BGEmail", "Email"),                    // Column G
    Tuple.Create("BGPreviousOrderCount", "Previous Order Count"), // Column H
    Tuple.Create("BGLastOrder.Date", "Last Order Date"), // Column I (optional)
};

// Filter by BGExecutionId (Type A pattern)
esq.Filters.Add(esq.CreateFilterWithParameters(
    FilterComparisonType.Equal,
    "BGExecutionId",
    executionId
));
```

---

## Implementation Options

### Option A: Full BGlobal Pattern (Recommended)

Follow BGlobal's original execution-based pattern:

1. **Create BGReportExecution record:**
   ```csharp
   var execution = new BGReportExecution {
       BGReportName = "Customers Did Not Buy",
       BGCreatedFrom = request.CreatedFrom,
       BGCreatedTo = request.CreatedTo
   };
   execution.Save();
   var executionId = execution.Id;
   ```

2. **Query view with ESQ relationship columns:**
   ```csharp
   var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "BGCustomerDidNotBuyView");
   esq.AddColumn("BGAccount.Name");
   esq.AddColumn("BGAccount.Address");
   esq.AddColumn("BGAccount.City.Name");
   esq.AddColumn("BGAccount.Region.Name");
   esq.AddColumn("BGAccount.Zip");
   esq.AddColumn("BGEmail");
   esq.AddColumn("BGAccount.Phone");
   esq.AddColumn("BGPreviousOrderCount");
   esq.Filters.Add(esq.CreateFilterWithParameters(
       FilterComparisonType.Equal, "BGExecutionId", executionId));
   ```

3. **Map columns to Excel template**

### Option B: Direct ESQ Filter (Simpler)

Bypass execution pattern, filter directly (but loses audit trail):

1. **Query view with date filters:**
   ```csharp
   esq.Filters.Add(esq.CreateFilterWithParameters(
       FilterComparisonType.GreaterOrEqual, "BGCreatedFrom", request.CreatedFrom));
   ```

2. **Still use relationship columns for Account details**

### Option C: Fix IntExcelReport Configuration (Long-term)

Update PROD IntExcelReport record:
1. Change `IntEsq.rootSchemaName` to `BGCustomerDidNotBuyView`
2. Update `IntEsq.columns` to use relationship paths
3. Let IntExcelExport library handle it (preserves VBA macros)

---

## Next Steps

1. ✅ **SQL view definition extracted** - `sql/BGCustomerDidNotBuyView_ORIGINAL.sql`
2. ✅ **Architecture documented** - `docs/investigation/BGLOBAL_V7_ARCHITECTURE_COMPLETE.md`
3. **Fix backend code** - Update `QueryCustomerDidNotBuyData()` with ESQ relationship columns
4. **Test in PROD** - Verify report generates correct customer contact data
5. **Consider IntExcelReport fix** - Long-term: update IntEsq to correct view

---

## Files Reference

| File | Purpose |
|------|---------|
| `sql/BGCustomerDidNotBuyView_ORIGINAL.sql` | **Original BGlobal SQL view definition** |
| `docs/investigation/BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` | **Complete V7 architecture reference** |
| `source-code/UsrExcelReportService_Updated.cs` | Backend routing (lines 2222-2400) |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js` | Frontend handler |

---

*Investigation completed: 2026-01-30*
*BGlobal V7 architecture fully documented*
*PROD OData queries + PampaBay package extraction completed*
