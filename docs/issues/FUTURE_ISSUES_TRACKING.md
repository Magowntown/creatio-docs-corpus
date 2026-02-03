# Future Issues Tracking

**Created:** 2026-01-29
**Purpose:** Track potential issues identified during code review that need future attention

---

## Potential Issue 1: BGSalesByItemLineView Reports

**Priority:** Medium
**Status:** Not Started
**Identified:** Session 7 (Ralph Loop)

### Reports Affected
| Report Name | IntName | IntExcelReport ID |
|-------------|---------|-------------------|
| Rpt Sales By Item | Rpt Sales By Item | `c4f4e32c-376d-4b19-b04b-2129dba29d06` |
| Rpt Sales by Item Line | Rpt Sales by Item Line | `1d009377-3cef-4199-9e38-7b47ddb27a0d` |
| Rpt Sales By Item By Type Of Customer | Rpt Sales By Item By Type Of Customer | `53682214-a63c-407a-b3f1-79d8ab235f18` |

### Problem Description
These reports:
1. Use `BGSalesByItemLineView` per PROD IntExcelReport config
2. Have **0 BGReportExecution records** (per COMPREHENSIVE_INVESTIGATION_SUMMARY.md)
3. Have NO custom generator routing in `UsrExcelReportService_Updated.cs`

### Symptoms (Expected)
- Reports may fail with VBA Type mismatch errors
- Reports may show empty or malformed data
- Same pattern as RPT-005 ("Customers did not buy") before fix

### Root Cause (Suspected)
Same as RPT-005:
- `IntEntitySchemaName` column doesn't exist in IntExcelReport
- `GetReportEntitySchemaName()` parses IntEsq JSON for `rootSchemaName`
- IntEsq may have different schema name than expected
- No custom generator intercepts the request

### Proposed Solution
Similar to RPT-005 fix:
1. Create `QuerySalesByItemLineData()` function with correct column mapping
2. Create `GenerateSalesByItemLineWithFilters()` generator
3. Add routing by report IntName:
   ```csharp
   if (reportName == "Rpt Sales By Item" ||
       reportName == "Rpt Sales by Item Line" ||
       reportName == "Rpt Sales By Item By Type Of Customer" ||
       entitySchemaName == "BGSalesByItemLineView")
   {
       return GenerateSalesByItemLineWithFilters(userConnection, request);
   }
   ```

### Column Structure Needed
From PROD_INTEXCELREPORT_CONFIGS.md:

**Rpt Sales By Item:**
- BGItem, BGLine, BGQuantity, BGAmount, BGReportStartDate, BGReportEndDate, Filters

**Rpt Sales by Item Line:**
- BGItem, BGLine, BGPONumber, BGCustomer, BGSalesRep, BGSalesGroup, BGShipDate, BGNumberInvoice, BGQuantity, BGPrice, BGAmount, BGReportStartDate, BGReportEndDate, Filters

**Rpt Sales By Item By Type Of Customer:**
- BGItem, Description, BGCustomerType, BGQuantity, BGAmount, Filters

### Testing Required
1. Run each report without custom generator
2. Document actual errors/behavior
3. Implement fix if needed
4. Test with various filter combinations

### Dependencies
- RPT-005 deployment and verification first
- May need to query PROD for BGSalesByItemLineView column structure

---

## Issue Status Legend

| Status | Description |
|--------|-------------|
| Not Started | Issue identified but no action taken |
| In Progress | Work has begun |
| Testing | Fix implemented, testing in progress |
| Blocked | Waiting on external dependency |
| Complete | Issue resolved and verified |

---

*Last updated: 2026-01-29*
