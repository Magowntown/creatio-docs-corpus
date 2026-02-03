# Report Column Compatibility Analysis

**Date:** 2026-01-29
**Purpose:** Determine if we can safely extend custom generator routing

---

## CRITICAL FINDING: Column Structures Are DIFFERENT

Each report has a different column structure. We CANNOT use one generator for all reports!

---

## Current Generator Output (QuerySalesByItemData)

**Queries:** BGSalesByItemView
**Output Columns (in VBA position order):**

| Position | Column Name | VBA Header | Data Type |
|----------|-------------|------------|-----------|
| A | BGCustomer | BGCustomer | varchar |
| B | CreatedOn | Created on | timestamp |
| C | BGAmount | Last Price | numeric |
| D | BGProductDescription | Product | text |
| E | BGItem | ProductCode | varchar |
| F | BGQuantity | Quantity | integer |
| G | BGPrice | Filters | numeric |

---

## PROD Report Column Requirements

### Items by Customer (BGItemsByCustomerView)

**IntExcelReport Columns:**
| Column | Expected |
|--------|----------|
| BGCustomer | ✅ |
| Created on | ✅ |
| Last Price | ✅ |
| Product | ✅ |
| ProductCode | ✅ |
| Quantity | ✅ |
| BGFilters | ✅ |

**Compatibility:** ✅ **MATCHES** our generator perfectly

---

### Rpt Sales By Item (BGSalesByItemLineView)

**IntExcelReport Columns:**
| Column | Our Generator Has? |
|--------|-------------------|
| BGItem | ✅ (but in position E, not A) |
| BGLine | ❌ NO |
| BGQuantity | ✅ (but in position F, not C) |
| BGAmount | ✅ (but in position C, not D) |
| BGReportStartDate | ❌ NO |
| BGReportEndDate | ❌ NO |
| Filters | ❌ Different meaning |

**Compatibility:** ❌ **DOES NOT MATCH** - Different column order AND missing columns

---

### Rpt Sales by Item Line (BGSalesByItemLineView)

**IntExcelReport Columns:**
| Column | Our Generator Has? |
|--------|-------------------|
| BGItem | ✅ |
| BGLine | ❌ NO |
| BGPONumber | ❌ NO |
| BGCustomer | ✅ |
| BGSalesRep | ❌ NO |
| BGSalesGroup | ❌ NO |
| BGShipDate | ❌ (we filter by it but don't output) |
| BGNumberInvoice | ❌ NO |
| BGQuantity | ✅ |
| BGPrice | ✅ |
| BGAmount | ✅ |
| BGReportStartDate | ❌ NO |
| BGReportEndDate | ❌ NO |
| Filters | ❌ Different |

**Compatibility:** ❌ **DOES NOT MATCH** - Many missing columns

---

### Rpt Sales By Item By Type Of Customer (BGSalesByItemLineView)

**IntExcelReport Columns:**
| Column | Our Generator Has? |
|--------|-------------------|
| BGItem | ✅ |
| Description | ✅ (as BGProductDescription) |
| BGCustomerType | ❌ NO |
| BGQuantity | ✅ |
| BGAmount | ✅ |
| Filters | ❌ Different |

**Compatibility:** ❌ **DOES NOT MATCH** - Missing BGCustomerType

---

## Risk Assessment

| Report | Use Our Generator? | Risk |
|--------|-------------------|------|
| **Items by Customer** | ✅ SAFE | Column structure matches |
| **Rpt Sales By Item** | ❌ DANGER | Wrong columns - VBA will fail |
| **Rpt Sales by Item Line** | ❌ DANGER | Many missing columns |
| **Rpt Sales By Item By Type** | ❌ DANGER | Missing BGCustomerType |

---

## SAFE CHANGE

**Only extend routing for BGItemsByCustomerView:**

```csharp
// SAFE: BGItemsByCustomerView has same column needs as BGSalesByItemView
if (entitySchemaName == "BGSalesByItemView" ||
    entitySchemaName == "BGItemsByCustomerView")
{
    // Both "Items by Customer" report types use same column structure
    bool hasFilter = ...;
    if (hasFilter)
    {
        return GenerateSalesByItemWithFilters(userConnection, request);
    }
}
```

---

## UNSAFE CHANGE (DO NOT DO)

```csharp
// DANGEROUS: BGSalesByItemLineView has DIFFERENT columns!
if (entitySchemaName == "BGSalesByItemView" ||
    entitySchemaName == "BGItemsByCustomerView" ||
    entitySchemaName == "BGSalesByItemLineView")  // ❌ WRONG - different structure
{
    return GenerateSalesByItemWithFilters(userConnection, request);
}
```

This would break "Rpt Sales By Item" because VBA expects different columns.

---

## To Fix Other Reports

Each report needs its OWN generator with correct column mapping:

### 1. Create QuerySalesByItemLineData() for BGSalesByItemLineView reports

```csharp
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGItem", "BGItem"),
    Tuple.Create("BGLine", "BGLine"),
    Tuple.Create("BGQuantity", "BGQuantity"),
    Tuple.Create("BGAmount", "BGAmount"),
    // etc.
};

var esq = new EntitySchemaQuery(..., "BGSalesByItemLineView");
```

### 2. Route each report to correct generator

```csharp
switch (entitySchemaName)
{
    case "BGSalesByItemView":
    case "BGItemsByCustomerView":
        return GenerateSalesByItemWithFilters(...);  // Items by Customer

    case "BGSalesByItemLineView":
        return GenerateSalesByItemLineWithFilters(...);  // Rpt Sales By Item, etc.

    case "BGSalesByCustomerView":
        return GenerateSalesByCustomerWithFilters(...);  // Customers Did Not Buy
}
```

---

## Recommendation

### Immediate (Safe)
1. ✅ Extend routing to catch `BGItemsByCustomerView` → use existing generator
2. ✅ This fixes "Items by Customer" without filters

### Later (Requires New Code)
1. Create `GenerateSalesByItemLineWithFilters()` with correct columns
2. Create `QuerySalesByItemLineData()` with BGSalesByItemLineView schema
3. Route BGSalesByItemLineView reports to new generator

---

## Summary

| Change | Safe? | Impact |
|--------|-------|--------|
| Add BGItemsByCustomerView to routing | ✅ YES | Fixes "Items by Customer" |
| Add BGSalesByItemLineView to routing | ❌ NO | Would break VBA with wrong columns |

**Only make the safe change. Other reports need dedicated generators.**

---

*Analysis completed: 2026-01-29*
