# SQL View Master Catalog - PampaBay Package

**Date:** 2026-01-29
**Source:** PampaBay package binary extraction
**Purpose:** Comprehensive catalog of all SQL views used by Excel reports

---

## Executive Summary

The PampaBay package contains **25+ SQL views** that power the Excel report system. These views follow **two distinct architectural patterns**:

| Pattern | Description | BGReportExecution | Example Views |
|---------|-------------|-------------------|---------------|
| **Type A: Execution-Based** | View JOINs to BGReportExecution table, filters internally | Yes (JOIN...ON true) | BGSalesByCustomerView, BGSalesByLineWithRankingView |
| **Type B: Direct** | View is a simple SELECT, filters applied via ESQ at query time | No | BGSalesByItemView, BGSalesByCustomerYearComparisonView |

**Critical Finding:** Views with `JOIN "BGReportExecution" re ON true` use the execution-based pattern where:
1. User selects filters on Reports page
2. BGReportExecution record is created with filter values
3. View dynamically filters based on execution context
4. IntExcelExport queries with `WHERE BGExecutionId = {guid}`

---

## Views by Pattern Type

### Type A: Execution-Based Views (Have BGExecutionId)

These views JOIN to `BGReportExecution` and filter data dynamically.

| View Name | BGExecutionId | BGReportExecution JOIN | Notes |
|-----------|---------------|------------------------|-------|
| BGCommissionReportDataView | ✅ | `JOIN ... ON BGReportName = 'Commission'` | Filters by YearMonth, SalesGroup |
| BGSalesByCustomerView | ✅ | `JOIN ... ON true` | Filters by date range |
| BGSalesByLineWithRankingView | ✅ | `INNER JOIN ... ON true` | Has BGProductDescription |
| BGSalesBySalesGroupView | ✅ | `JOIN ... ON BGReportName = ?` | Execution-based |
| BGSalesRepMonthlyReportView | ✅ | `JOIN ... ON true` | Monthly report |
| BGSalesByItemLineView | ✅ | `JOIN ... ON true` | Has p."Description" AS BGDescription |

### Type B: Direct Views (No BGExecutionId)

These views are simple SELECTs - filters must be applied externally.

| View Name | Product JOIN | Has Description | Notes |
|-----------|--------------|-----------------|-------|
| BGSalesByItemView | ✅ `JOIN "Product" p` | ✅ **ADDED** `BGProductDescription` | Fixed 2026-01-29 |
| BGSalesByItemByTypeOfCustomerView | ✅ `JOIN "Product" p` | ❌ Missing | Needs same fix |
| BGSalesByCustomerYearComparisonView | ❌ | ❌ | No product data |
| BGSalesByItemThemeView | ✅ | ❌ | Theme grouping |
| BGCatalogView | ✅ | ? | Product catalog |
| BGItemsByCustomerView | ? | ? | Empty view (broken) |

---

## Detailed View Analysis

### BGSalesByItemView (FIXED)

**Pattern:** Type B (Direct)
**Package:** PampaBay
**Status:** ✅ FIXED - BGProductDescription column added

```sql
SELECT
  o."Id",
  o."CreatedOn", o."CreatedById", o."ModifiedOn", o."ModifiedById",
  o."ProcessListeners",
  o."Number" AS "BGNumber",
  o."BGPONumber",
  o."BGShipDate",
  o."BGDeliveryDate",
  op."Price" AS "BGPrice",
  op."TotalAmount" AS "BGAmount",
  p."Name" AS "BGItem",
  p."Description" AS "BGProductDescription",  -- ADDED 2026-01-29
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep"
FROM
  "Order" o
  JOIN "Account" ac ON (o."AccountId" = ac."Id")
  JOIN "OrderStatus" os ON (o."StatusId" = os."Id")
  JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id")
  JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId")
  JOIN "OrderProduct" op ON (op."OrderId" = o."Id")
  JOIN "Product" p ON (p."Id" = op."ProductId")  -- Product already joined!
WHERE
  o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'::uuid
  AND sg.* IS NOT NULL
  AND os."Id" IN (...)
```

**Reports Using This View:**
- Items by Customer
- Rpt Sales By Item
- Rpt Sales By Item By Type Of Customer

---

### BGSalesByCustomerView (EXECUTION-BASED)

**Pattern:** Type A (Execution-Based)
**Package:** PampaBay
**BGExecutionId:** ✅ Yes
**Status:** Has OutOfMemoryException issue (RPT-005)

```sql
SELECT
  o."Number" AS "BGNumber",
  ... AS "BGAmount",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  ... AS "BGDeliveryDate",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep",
  ... AS "BGReportStartDate",
  ... AS "BGReportEndDate",
  re."Id" AS "BGExecutionId",  -- Execution-based!
  ... AS "BGFilters"
FROM
  "Order" o
  JOIN "Account" ac ON (...)
  JOIN "OrderStatus" os ON (...)
  JOIN "BGSalesGroup" sg ON (...)
  JOIN "Employee" e ON (...)
  JOIN "BGReportExecution" re ON true  -- Cross join to all executions!
  LEFT JOIN "UsrStatus" stat ON (...)
  LEFT JOIN "OrderStatus" status ON (...)
WHERE ...
```

**Problem:** The `JOIN "BGReportExecution" re ON true` creates a Cartesian product with ALL execution records, then filters. With millions of rows and 117+ execution records, this causes OutOfMemoryException.

**Fix:** Custom generator `GenerateSalesByCustomerWithFilters()` in UsrExcelReportService.cs

---

### BGSalesByItemLineView (HAS DESCRIPTION)

**Pattern:** Type A (Execution-Based)
**Package:** PampaBay
**BGExecutionId:** ✅ Yes
**Has Product Description:** ✅ Yes (`p."Description" AS "BGDescription"`)

```sql
SELECT
  o."Number" AS "BGNumber",
  op."Price" AS "BGPrice",
  op."TotalAmount" AS "BGAmount",
  p."Name" AS "BGItem",
  p."Description" AS "BGDescription",  -- Already has description!
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep",
  ct."Name" AS "BGCustomerType",
  lp."Name" AS "BGLine",
  ... AS "BGReportStartDate",
  ... AS "BGReportEndDate",
  re."Id" AS "BGExecutionId",
  ... AS "BGFilters"
FROM ...
```

**Reports Using This View:**
- Rpt Sales By Line
- Rpt Sales By Line With Ranking

---

### BGSalesByLineWithRankingView (HAS DESCRIPTION)

**Pattern:** Type A (Execution-Based)
**Package:** PampaBay
**Has Product Description:** ✅ Yes (`P."BGDescription" AS "BGProductDescription"`)

**Note:** This view explicitly uses `BGProductDescription` as the column name - the pattern we're now applying to BGSalesByItemView.

---

## Column Patterns Across Views

### Standard Columns (Most Views Have)

| Column | Source | Description |
|--------|--------|-------------|
| BGNumber | o."Number" | Order number |
| BGPONumber | o."BGPONumber" | PO number |
| BGDeliveryDate | o."BGDeliveryDate" | Delivery date |
| BGShipDate | o."BGShipDate" | Ship date |
| BGAmount | op."TotalAmount" or SUM | Line/order amount |
| BGPrice | op."Price" | Unit price |
| BGQuantity | op."Quantity" | Quantity |
| BGCustomer | ac."Name" | Account name |
| BGStatus | os."Name" | Order status |
| BGSalesGroup | sg."BGSalesGroupName" | Sales group |
| BGSalesRep | e."Name" | Employee name |

### Product-Related Columns

| Column | Source | Views That Have It |
|--------|--------|-------------------|
| BGItem | p."Name" | Most product views |
| BGDescription | p."Description" | BGSalesByItemLineView |
| BGProductDescription | p."Description" | BGSalesByLineWithRankingView, **BGSalesByItemView (added)** |
| BGLine | lp."Name" | Line views |
| BGCustomerType | ct."Name" | Type views |

### Execution-Based Columns

| Column | Source | Purpose |
|--------|--------|---------|
| BGExecutionId | re."Id" | Links to BGReportExecution record |
| BGReportStartDate | COALESCE(...) | Report date range start |
| BGReportEndDate | COALESCE(...) | Report date range end |
| BGFilters | Concatenated string | Human-readable filter description |

---

## IntExcelReport Mappings

| IntExcelReport Name | View Schema | Pattern | Custom Generator |
|--------------------|-------------|---------|------------------|
| Rpt Commission | BGCommissionReportDataView | Type A | Yes (ExecutionId) |
| Items by Customer | BGSalesByItemView | Type B | Yes (Filters) |
| Rpt Sales By Item | BGSalesByItemView | Type B | Yes (Filters) |
| Rpt Sales By Line | BGSalesByItemLineView | Type A | TBD |
| Customers did not buy | BGSalesByCustomerView | Type A | Yes (Filters) |
| Rpt Sales By Sales Group | BGSalesBySalesGroupView | Type A | TBD |
| Rpt Sales By Customer | BGSalesByCustomerView | Type A | TBD |
| Sales Rep Monthly | BGSalesRepMonthlyReportView | Type A | TBD |

---

## Recommendations

### Views Needing BGProductDescription

These views have Product JOINs but missing description column:

1. **BGSalesByItemByTypeOfCustomerView** - Same pattern as BGSalesByItemView, needs `p."Description" AS "BGProductDescription"`

### Views Needing Custom Generators

These execution-based views may cause OutOfMemory with large datasets:

1. **BGSalesByCustomerView** - ✅ Custom generator added (RPT-005)
2. **BGSalesBySalesGroupView** - May need custom generator
3. **BGSalesRepMonthlyReportView** - May need custom generator

### Architecture Considerations

1. **Type A views with ON true JOIN** create Cartesian products - performance risk
2. **Type B views** are safer but need proper ESQ filtering
3. **Product.Description** should be added to ALL product-related views for consistency

---

## SQL Scripts Created

| Script | Purpose | Status |
|--------|---------|--------|
| `sql/BGSalesByItemView_fix.sql` | Add BGProductDescription | ✅ Applied |
| `sql/BGCommissionReportDataView.sql` | Commission view reference | ✅ Documented |
| `scripts/sql/BGCommissionReportDataView_fix_PROD.sql` | FLT-004 date fix | ✅ Applied |

---

## Appendix: All Views in PampaBay Package

| View Name | Type | Has Product | Has Execution |
|-----------|------|-------------|---------------|
| BGCatalogView | B | ✅ | ❌ |
| BGCommissionReportDataView | A | ❌ | ✅ |
| BGCustomerDidNotBuyView | ? | ? | ? |
| BGItemsByCustomerView | B | ? | ❌ (empty) |
| BGMonthlyNewAndRepeatCustomerOrderView | ? | ? | ? |
| BGOrderProductTotalErrorCountView | ? | ? | ? |
| BGOrderTotalErrorCountView | ? | ? | ? |
| BGSalesByCustomerPrevYearComparisonView | B | ❌ | ❌ |
| BGSalesByCustomerTypeView | B | ? | ❌ |
| BGSalesByCustomerView | A | ❌ | ✅ |
| BGSalesByCustomerYearComparisonView | B | ❌ | ❌ |
| BGSalesByItemByTypeOfCustomerView | B | ✅ | ❌ |
| BGSalesByItemLineView | A | ✅ | ✅ |
| BGSalesByItemThemeView | B | ✅ | ❌ |
| BGSalesByItemView | B | ✅ | ❌ |
| BGSalesByLineByTypeOfCustomerView | B | ✅ | ❌ |
| BGSalesByLineWithRankingView | A | ✅ | ✅ |
| BGSalesBySalesGroupView | A | ? | ✅ |
| BGSalesBySalesRepView | B | ? | ❌ |
| BGSalesRepMonthlyReportView | A | ? | ✅ |
| BGTopSalesProductBySalesRepView | ? | ? | ? |
| BGVWProductInCatalog | ? | ✅ | ? |
| BGVWProductInOrder | ? | ✅ | ? |
| BGVwProductQuantityByOrder | ? | ✅ | ? |
| BGVwTopSalesReps | ? | ? | ? |
| BGVwTopSoldProducts | ? | ✅ | ? |

---

*Created: 2026-01-29*
*Source: PampaBay package binary extraction*
*Investigator: Claude Code*
