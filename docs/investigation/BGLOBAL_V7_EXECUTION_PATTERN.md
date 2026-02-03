# BGlobal v7 Report Execution Pattern Investigation

**Date:** 2026-01-29
**Purpose:** Document how BGlobal originally set up Excel reports in Creatio v7, specifically the "BGExecutionId = @P1@" filter pattern

---

## Executive Summary

BGlobal's original v7 Excel report architecture used an **execution-based filtering pattern** for certain reports (Commission, Sales By Sales Group) where:

1. **User selects filters** on the Reports page (YearMonth, SalesGroup)
2. **BGReportExecution record is created** storing the filter values
3. **SQL View dynamically filters** data by joining to BGReportExecution using BGExecutionId
4. **IntExcelExport library queries** the view with `BGExecutionId = {execution_record_id}`
5. **View returns only matching rows** based on the execution context

This pattern was used for **Commission reports** but was **NOT implemented** for reports like "Items by Customer" which have 0 BGReportExecution records.

---

## The BGExecutionId Pattern Explained

### 1. What is BGExecutionId?

`BGExecutionId` is a GUID column present in certain SQL views (e.g., `BGCommissionReportDataView`) that references a `BGReportExecution` record. The view **JOINs** to the `BGReportExecution` table and **filters** data based on the filter values stored in that execution record.

### 2. How It Works (Commission Example)

**SQL View Definition** (from `sql/BGCommissionReportDataView.sql`):

```sql
CREATE OR REPLACE VIEW "BGCommissionReportDataView" AS
    SELECT
        -- ... many columns ...
        re."Id" AS "BGExecutionId",         -- The execution ID column
        re."BGYearMonthId"                  -- Year-Month from execution context
    FROM
        "BGCommissionReportQBDownload" qb
        JOIN "Order" so ON (...)
        JOIN "BGCommissionEarner" ce ON (...)
        JOIN "Employee" rep ON (...)
        -- KEY: Join to BGReportExecution
        JOIN "BGReportExecution" re ON (re."BGReportName" = 'Commission')
        LEFT JOIN "BGYearMonth" ym ON (ym."Id" = re."BGYearMonthId")
    WHERE
        -- Filter by SalesGroup from execution context
        (re."BGSalesGroupId" IS NULL OR re."BGSalesGroupId" = rep."BGSalesGroupLookupId")
        AND
        -- Filter by YearMonth from execution context
        (ym."Id" IS NULL OR (
            EXTRACT('month' FROM qb."BGTransactionDate") = EXTRACT('month' FROM ym."BGDateTime" + '1 day')
            AND EXTRACT('year' FROM qb."BGTransactionDate") = EXTRACT('year' FROM ym."BGDateTime" + '1 day')
        ))
```

**Key Insight:** The view doesn't take YearMonth/SalesGroup as parameters directly. Instead, it **JOINs to BGReportExecution** and **filters internally** based on the values stored in that execution record.

### 3. The Complete Flow (v7 Classic UI)

```
USER CLICKS REPORT BUTTON
        ↓
BGIntExcelreportMixin (Classic UI Mixin)
[Schema UID: a589d29b-9da7-4f66-836b-8e39fe0ca376]
        ↓
Creates BGReportExecution record:
  - BGReportName = "Commission"
  - BGYearMonthId = {selected YearMonth GUID}
  - BGSalesGroupId = {selected SalesGroup GUID}
        ↓
Triggers IntGenerateExcelReportUserTask business process
[GUID: 05c5265c-3f51-4114-9862-fc434abe1f6d]
        ↓
Business process builds ESQ with filter:
  WHERE BGExecutionId = {execution_record_id}
        ↓
ESQ queries BGCommissionReportDataView
  - View JOINs to BGReportExecution
  - Returns rows matching YearMonth + SalesGroup from execution record
        ↓
IntExcelExport library generates Excel bytes
        ↓
Stores bytes in SessionData[key]
        ↓
BGIntExcelReportService2.GetExportFilteredData(name, key)
        ↓
Downloads bytes from SessionData
        ↓
EXCEL FILE DOWNLOADS
```

---

## BGReportExecution Table Analysis

### Schema Definition

| Column | Type | Description |
|--------|------|-------------|
| **Id** | GUID | Primary key, becomes BGExecutionId in views |
| **BGReportName** | Text | "Commission", "Sales By Sales Group", etc. |
| **BGYearMonthId** | Lookup | Reference to BGYearMonth |
| **BGSalesGroupId** | Lookup | Reference to BGSalesGroup |
| **BGCustomerId** | Lookup | Reference to Account (for customer-based reports) |
| **BGCreatedFrom/To** | DateTime | Date range filters |
| **BGShippingFrom/To** | DateTime | Shipping date range |
| **BGDeliveryFrom/To** | DateTime | Delivery date range |
| **BGOrderStatusId** | Lookup | Order status filter |
| **BGUserId** | GUID | User who executed the report |

### Report Execution Record Counts

| Report Name | BGReportExecution Records | Pattern Used |
|-------------|--------------------------|--------------|
| Commission | 111 | ✅ Execution-based |
| Sales By Sales Group | 3 | ✅ Execution-based |
| Sales By Customer | 2 | ✅ Execution-based |
| Sales Rep Monthly Report | 1 | ✅ Execution-based |
| **Items by Customer** | **0** | ❌ NOT execution-based |
| **IW_Commission** | **0** | ❌ NOT execution-based |
| **Sales By Item** | **0** | ❌ NOT execution-based |
| **Sales By Line** | **0** | ❌ NOT execution-based |

**Critical Finding:** Reports with 0 BGReportExecution records were either:
1. **Never used** with the v7 original flow
2. **Designed differently** (using direct ESQ filters instead of execution-based views)
3. **Broken** from the start

---

## Two Distinct Report Architectures

### Type A: Execution-Based Views (Commission)

**Views:** `BGCommissionReportDataView`, `BGSalesBySalesGroupView`, `BGSalesByCustomerView`

**Characteristics:**
- View definition includes `JOIN "BGReportExecution" re`
- View has `re."Id" AS "BGExecutionId"` column
- Filters are embedded in view WHERE clause
- IntExcelReport.IntFiltersConfig = `"BGExecutionId = @P1@"`
- Requires BGReportExecution record creation before query

**IntEsq Filter Pattern:**
```json
{
  "filters": {
    "items": {
      "ExecutionFilter": {
        "filterType": 1,
        "comparisonType": 3,
        "leftExpression": {"columnPath": "BGExecutionId"},
        "rightExpression": {"parameter": {"value": "{execution_guid}"}}
      }
    }
  }
}
```

### Type B: Direct Views (Items by Customer)

**Views:** `BGSalesByItemView`, `BGSalesByLineView`, `BGItemsByCustomerView` (empty)

**Characteristics:**
- View is a simple SELECT without BGReportExecution JOIN
- No BGExecutionId column
- Filters must be applied in ESQ at query time
- IntExcelReport.IntFiltersConfig = empty or direct column filters
- No BGReportExecution record needed

**IntEsq Filter Pattern:**
```json
{
  "filters": {
    "items": {
      "CustomerFilter": {
        "filterType": 1,
        "comparisonType": 11,
        "leftExpression": {"columnPath": "BGCustomer"},
        "rightExpression": {"parameter": {"value": "Customer Name"}}
      },
      "DateFilter": {
        "filterType": 1,
        "comparisonType": 4,
        "leftExpression": {"columnPath": "CreatedOn"},
        "rightExpression": {"parameter": {"value": "2026-01-01"}}
      }
    }
  }
}
```

---

## "Items by Customer" - Historical Mystery

### Original Configuration (Incorrect)

| Field | Value |
|-------|-------|
| IntExcelReport.IntName | Items by Customer |
| IntEntitySchemaNameId | `01547449-50b0-4328-b51f-c742bdd3cccd` (BGItemsByCustomerView) |
| BGReportExecution records | **0** |
| BGItemsByCustomerView row count | **0** |

### The Mystery

`BGItemsByCustomerView` appears to be an **execution-based view** (similar to Commission pattern) but was **never populated**:

1. **No BGReportExecution records** exist for "Items by Customer"
2. **BGItemsByCustomerView is empty** (0 rows)
3. **No business process** populates this view
4. **No data source** feeds BGItemsByCustomerView

**Possible Explanations:**
1. **Incomplete Implementation:** BGlobal started building an execution-based "Items by Customer" but never finished
2. **Migration Gap:** The view was designed for a different data source that was never connected
3. **Configuration Error:** Wrong view was configured from the start

### The Fix (Our Implementation)

Changed IntExcelReport to use `BGSalesByItemView` instead:

| Field | Before | After |
|-------|--------|-------|
| IntEntitySchemaNameId | `01547449...` (BGItemsByCustomerView) | `5f969641...` (BGSalesByItemView) |
| Row count | 0 | 4,800,000+ |
| Custom generator | N/A | `GenerateSalesByItemWithFilters()` |

---

## SQL Scripts in Project

### `sql/BGCommissionReportDataView.sql`

Complete view definition showing the execution-based pattern:
- JOIN to BGReportExecution
- WHERE filters using execution context
- BGExecutionId output column

### `scripts/sql/BGCommissionReportDataView_fix_PROD.sql`

FLT-004 fix: Changed WHERE clause to filter on `so."BGInvoiceDate"` instead of `qb."BGTransactionDate"` to match output column.

### Other SQL Files

| File | Purpose |
|------|---------|
| `scripts/sql/IWCommissionReportDataView.sql` | IW_Commission view (not execution-based) |
| `scripts/sql/fix_yearmonth_data.sql` | BGYearMonth data fixes |

---

## IntExcelReport Configuration Table

### Reports Using Execution-Based Pattern

| Report | IntEntitySchemaName | IntFiltersConfig |
|--------|---------------------|------------------|
| Rpt Commission | BGCommissionReportDataView | BGExecutionId = @P1@ |
| Rpt Sales By Sales Group | BGSalesBySalesGroupView | BGExecutionId = @P1@ |
| Rpt Sales By Customer | BGSalesByCustomerView | BGExecutionId = @P1@ |

### Reports Using Direct Pattern

| Report | IntEntitySchemaName | IntFiltersConfig |
|--------|---------------------|------------------|
| Items by Customer | BGSalesByItemView (fixed) | (direct column filters) |
| Sales By Item | BGSalesByItemView | (direct column filters) |
| Sales By Line | BGSalesByLineView | (direct column filters) |

---

## Implications for Our Implementation

### What Works

1. **Commission reports** work because:
   - BGReportExecution record creation (via test script or frontend)
   - View filters by joining to execution record
   - IntExcelExport queries with BGExecutionId filter

2. **Items by Customer** works (after fix) because:
   - Changed to BGSalesByItemView (has data)
   - Custom generator applies filters directly
   - No BGReportExecution record needed

### What Needs Backend Deploy

1. **Customers did not buy** (`BGSalesByCustomerView`):
   - View is execution-based but has millions of rows
   - IntExcelExport causes OutOfMemoryException without proper filters
   - **Fix:** Custom generator `GenerateSalesByCustomerWithFilters()` in `UsrExcelReportService_Updated.cs`

### Architectural Decision

Our custom `UsrExcelReportService` bypasses the original execution-based pattern for most reports by:

1. **Building ESQ directly** with filter parameters from request
2. **Creating BGReportExecution records** when needed (for Commission)
3. **Using custom generators** for views with millions of rows

This is **necessary** because:
- Freedom UI can't use Classic UI mixins
- IntExcelExport library doesn't properly apply FiltersConfig for some views
- Large views need custom filtering to avoid OutOfMemoryException

---

## Reference Files

| Purpose | File Path |
|---------|-----------|
| BGCommissionReportDataView SQL | `sql/BGCommissionReportDataView.sql` |
| BGReportExecution schema docs | `docs/BGREPORTEXECUTION_SCHEMA.md` |
| Custom backend service | `source-code/UsrExcelReportService_Updated.cs` |
| Original handler reference | `client-module/UsrPage_ebkv9e8_ORIGINAL_INTEXCEL.js` |
| Architecture investigation | `docs/BGLOBAL_ARCHITECTURE_INVESTIGATION.md` |
| Items by Customer fix | `docs/ITEMS_BY_CUSTOMER_FIX_20260128.md` |
| Test script (execution flow) | `scripts/testing/test_commission_execution_filters.py` |

---

## Appendix: Key GUIDs

### IntExcelReport IDs

| Report | IntExcelReport.Id |
|--------|-------------------|
| Rpt Commission | `4ba4f203-7088-41dc-b86d-130c590b3594` |
| Items by Customer | `d213933b-093d-47fc-8da8-422c0d9bf715` |
| Rpt Sales By Line | `0b40d51d-4935-4918-97f2-45352aed341f` |
| Rpt Sales By Customer | `62d81c91-13d2-4edf-9827-1f9e35ce03d9` |
| Rpt Sales By Sales Group | `a935a791-e2ff-4693-9b50-38a8596a3667` |
| IW_Commission | `07c77859-b7e5-43f3-97c6-14113f6a1f6f` |

### Entity Schema IDs (IntEntitySchemaNameId)

| Schema | SysSchema.Id |
|--------|--------------|
| BGCommissionReportDataView | `e60e7a82-955e-4ea9-ae1a-203dd28a0e64` |
| BGSalesByItemView | `5f969641-af66-48bd-9fca-b532f479684f` |
| BGSalesByCustomerView | `c271da12-0ded-4154-b3eb-a9d97510314c` |
| BGSalesBySalesGroupView | `d88712a0-cb0d-48b3-abb1-bfd4f9d4ae64` |
| BGSalesByLineView | `28458bfc-078d-440e-ab86-27adea4d5a88` |
| BGItemsByCustomerView (empty) | `01547449-50b0-4328-b51f-c742bdd3cccd` |

### Process GUIDs

| Process | UId |
|---------|-----|
| IntGenerateExcelReportUserTask | `05c5265c-3f51-4114-9862-fc434abe1f6d` |
| BGBPGetQuickBooksCommissions | `7b1ac959-1726-4340-bc66-210b31f5f365` |

---

*Created: 2026-01-29*
*Investigation by: Claude Code*
