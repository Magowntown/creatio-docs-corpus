# RPT-010: Backend Routing Order Fix

**Report:** Rpt Sales By Item (and related reports)
**Status:** ✅ FIXED
**Date:** 2026-01-30

---

## Problem

"Rpt Sales By Item" was generating with wrong columns - showing Items by Customer columns (7 columns including Customer) instead of the correct Sales By Item columns (7 columns including Line info).

---

## Root Cause

The backend routing in `UsrExcelReportService_Updated.cs` was checking `entitySchemaName` BEFORE checking the report name (`IntName`).

### The Issue

Some IntExcelReport records have outdated `IntEsq` JSON with `rootSchemaName` pointing to the wrong view:

```json
{
  "rootSchemaName": "BGSalesByItemView"  // <-- WRONG! Should be BGSalesByItemLineView
}
```

The routing code was:

```csharp
// OLD (WRONG) - checks entity schema first
if (entitySchemaName == "BGSalesByItemView")
{
    return GenerateSalesByItemWithFilters(...);  // Items by Customer handler
}
```

This meant "Rpt Sales By Item" (which should use BGSalesByItemLineView with different columns) was being routed to the "Items by Customer" handler.

---

## Fix

**Route by report name FIRST, then fall back to entity schema.**

### Updated Routing Code

```csharp
// ROUTE BY REPORT NAME FIRST (before view-based routing)
var reportName = GetReportName(userConnection, request.ReportId);

// SALES BY ITEM (7 columns - includes BGLine)
if (reportName == "Rpt Sales By Item")
{
    return GenerateSalesByItemReportWithFilters(userConnection, request);
}

// SALES BY ITEM BY TYPE OF CUSTOMER (6 columns)
if (reportName == "Rpt Sales By Item By Type Of Customer")
{
    return GenerateSalesByItemByTypeOfCustomerWithFilters(userConnection, request);
}

// ITEMS BY CUSTOMER (7 columns - includes BGCustomer) - fallback for BGSalesByItemView
if (reportName == "Items by Customer" ||
    entitySchemaName == "BGItemsByCustomerView" ||
    entitySchemaName == "BGSalesByItemView")
{
    return GenerateSalesByItemWithFilters(userConnection, request);
}
```

---

## New Handler: Sales By Item By Type Of Customer

A new handler was created for the 6-column "Sales By Item By Type Of Customer" report:

### Column Mapping

| # | ESQ Column | Output Key | Purpose |
|---|------------|------------|---------|
| 1 | BGItem | BGItem | Product name/code |
| 2 | BGDescription | Description | Product description |
| 3 | BGCustomerType | BGCustomerType | Customer type |
| 4 | BGQuantity | Qty | Quantity |
| 5 | BGAmount | Amount | Total amount |
| 6 | BGFilters | Filters | Filter description |

### Methods Added

- `GenerateSalesByItemByTypeOfCustomerWithFilters()` - Main generator
- `QuerySalesByItemByTypeOfCustomerData()` - ESQ query method

---

## File Modified

**File:** `source-code/UsrExcelReportService_Updated.cs`
**Location:** Lines ~3863-3925 (routing section)

---

## Key Lesson Learned

**Always check report name (`IntName`) BEFORE entity schema name when routing.**

IntEsq `rootSchemaName` can be:
- Outdated (legacy configurations)
- Wrong (misconfigured)
- Different from actual PROD behavior

The report name is the reliable identifier.

---

## Reports Affected by This Pattern

| Report | IntEsq rootSchemaName | Actual View | Status |
|--------|----------------------|-------------|--------|
| Items by Customer | BGSalesByItemView | BGItemsByCustomerView | ✅ Fixed (name-based) |
| Rpt Sales By Item | BGSalesByItemView | BGSalesByItemLineView | ✅ Fixed (name-based) |
| Rpt Sales By Item By Type | BGSalesByItemLineView | BGSalesByItemLineView | ✅ New handler |

---

## Verification

**Before fix:**
- "Rpt Sales By Item" → Items by Customer columns (wrong)

**After fix:**
- "Rpt Sales By Item" → Correct columns with BGLine info
- "Items by Customer" → Correct columns with BGCustomer
- "Sales By Item By Type" → Correct 6 columns

---

*Fixed: 2026-01-30*
*Analyst: Claude Code*
