# PROD IntExcelReport Configurations

**Date:** 2026-01-29
**Source:** PROD screenshots from Pampa Reports → Excel reports

---

## Executive Summary

**ALL examined reports are Type A (Execution-Based)**, using `BGExecutionId = @P1@` filter.

The SQL fix applied to BGSalesByItemView does NOT affect any of these reports.

---

## Report Configurations

### 1. Items by Customer

| Property | Value |
|----------|-------|
| Name | Items by Customer |
| Entity Schema | **BGItemsByCustomerView** |
| Report Type | Custom report |
| Template | Items by Customer.xlsx |
| Filter | BGExecutionId = @P1@ |

**Columns:**
| Column | Sort |
|--------|------|
| BGCustomer | No sorting |
| Created on | No sorting |
| Last Price | No sorting |
| Product | No sorting |
| ProductCode | No sorting |
| Quantity | No sorting |
| BGFilters | No sorting |

---

### 2. Rpt Sales By Item

| Property | Value |
|----------|-------|
| Name | Rpt Sales By Item |
| Entity Schema | **BGSalesByItemLineView** |
| Report Type | Custom report |
| Template | Rpt Sales By Item.xlsx |
| Filter | BGExecutionId = @P1@ |

**Columns:**
| Column | Sort |
|--------|------|
| BGItem | No sorting |
| BGLine | No sorting |
| BGQuantity | No sorting |
| BGAmount | No sorting |
| BGReportStartDate | No sorting |
| BGReportEndDate | No sorting |
| Filters | No sorting |

---

### 3. Rpt Sales by Item Line

| Property | Value |
|----------|-------|
| Name | Rpt Sales by Item Line |
| Entity Schema | **BGSalesByItemLineView** |
| Report Type | Custom report |
| Template | Rpt Sales by Item Line.xlsx |
| Filter | BGExecutionId = @P1@ |

**Columns:**
| Column | Sort |
|--------|------|
| BGItem | No sorting |
| BGLine | No sorting |
| BGPONumber | No sorting |
| BGCustomer | No sorting |
| BGSalesRep | No sorting |
| BGSalesGroup | No sorting |
| BGShipDate | No sorting |
| BGNumberInvoice | No sorting |
| BGQuantity | No sorting |
| BGPrice | No sorting |
| BGAmount | No sorting |
| BGReportStartDate | No sorting |
| BGReportEndDate | No sorting |
| Filters | No sorting |

---

### 4. Rpt Sales By Item By Type Of Customer

| Property | Value |
|----------|-------|
| Name | Rpt Sales By Item By Type Of Customer |
| Entity Schema | **BGSalesByItemLineView** |
| Report Type | Custom report |
| Template | Rpt Sales By Item By Type Of Customer.xlsx |
| Filter | BGExecutionId = @P1@ |

**Columns:**
| Column | Sort |
|--------|------|
| BGItem | No sorting |
| Description | No sorting |
| BGCustomerType | No sorting |
| BGQuantity | No sorting |
| BGAmount | No sorting |
| Filters | No sorting |

---

## View Usage Summary

| View | Reports Using It | Type |
|------|------------------|------|
| **BGItemsByCustomerView** | Items by Customer | Type A (Execution) |
| **BGSalesByItemLineView** | Rpt Sales By Item, Rpt Sales by Item Line, Rpt Sales By Item By Type Of Customer | Type A (Execution) |
| **BGSalesByItemView** | *NONE of examined reports* | Type B (Direct) |

---

## Impact Analysis

### BGSalesByItemView SQL Fix (Applied 2026-01-29)

**Fix:** Changed Employee JOIN from `sg."Id" = e."BGSalesGroupLookupId"` to `o."BGSalesRepLookupId" = e."Id"`

**Impact:** ❌ Does NOT affect any of the examined reports

| Report | Affected? | Reason |
|--------|-----------|--------|
| Items by Customer | ❌ No | Uses BGItemsByCustomerView |
| Rpt Sales By Item | ❌ No | Uses BGSalesByItemLineView |
| Rpt Sales by Item Line | ❌ No | Uses BGSalesByItemLineView |
| Rpt Sales By Item By Type | ❌ No | Uses BGSalesByItemLineView |

---

## Type A (Execution-Based) Pattern

All reports use the execution-based pattern:

1. **User initiates report** → Frontend calls backend
2. **Backend creates BGReportExecution record** with filters
3. **View joins to BGReportExecution** via BGExecutionId
4. **IntExcelExport queries view** with ExecutionId filter
5. **Data populated into Excel template**

### Required for Type A Reports:
- BGReportExecution record must exist
- ExecutionId must be passed correctly
- View must have BGExecutionId column
- IntExcelExport filter must use @P1@ parameter

---

## Next Steps

1. Investigate BGItemsByCustomerView schema
2. Verify BGReportExecution records are being created
3. Check if custom backend generators bypass IntExcelExport properly
4. Determine why VBA Type mismatch occurs

---

*Created: 2026-01-29*
