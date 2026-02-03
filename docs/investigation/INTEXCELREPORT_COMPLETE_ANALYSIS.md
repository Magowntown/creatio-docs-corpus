# IntExcelReport Complete Analysis

> **Generated:** 2026-01-30
> **Purpose:** Cross-reference all 33 IntExcelReport configurations to identify mismatches and potential issues

---

## Executive Summary

| Category | Count | Details |
|----------|-------|---------|
| **Total Reports** | 33 | All PROD IntExcelReport records |
| **Confirmed Issues** | 1 | RPT-005 (wrong view reference) |
| **Potential Issues** | 2 | EntitySchemaId ≠ IntEsq.rootSchemaName mismatches |
| **Working Correctly** | 30 | Proper view/column alignment |

---

## Critical Issue: RPT-005

### "Rpt CustomersDidNotBuyOverAPeriodOfTime"

| Field | Value | Problem |
|-------|-------|---------|
| **ID** | `1f65a56a-d7f4-4ce2-b517-c633872ea545` | |
| **IntEsq.rootSchemaName** | `BGSalesByCustomerView` | ❌ **WRONG VIEW** |
| **Expected View** | `BGCustomerDidNotBuyView` | Should use this |
| **Columns in IntEsq** | BGStatus, BGCustomer, BGShipDate... | Wrong columns |
| **Expected Columns** | Account, Address, City, State, ZIP, Email, Phone | Customer contact info |

**Root Cause:** IntEsq was configured to use `BGSalesByCustomerView` (ID: bd0fefb4-676f-4e31-a6e4-34fae1d3feb3) instead of `BGCustomerDidNotBuyView` (ID: 10647dfc-f999-4cf7-a17c-52a070c36ee6).

**Fix Applied:** Backend routing by report name in `UsrExcelReportService_Updated.cs`:
```csharp
if (reportName == "Rpt CustomersDidNotBuyOverAPeriodOfTime" || entitySchemaName == "BGCustomerDidNotBuyView")
{
    return QueryCustomerDidNotBuyData(esq);
}
```

---

## Complete Report Inventory

### Category 1: Sales by Customer Reports (6 reports)

All use `BGSalesByCustomerView` - **WORKING**

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Rpt Sales By Customer | BGSalesByCustomerView | ✅ |
| Rpt Sales By Customer (Collapsed) | BGSalesByCustomerView | ✅ |
| Rpt Sales By Customer Type | BGSalesByCustomerView | ✅ |
| Rpt Sales by Customer Type (Collapsed) | BGSalesByCustomerView | ✅ |
| Rpt Sales by Customer Year Comparison | BGSalesByCustomerView | ✅ |
| Rpt Sales By Customer Year Comparison (Collapsed) | BGSalesByCustomerView | ✅ |

### Category 2: Sales by Item Reports (3 reports)

All use `BGSalesByItemView` - **WORKING**

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Items by Customer | BGSalesByItemView | ✅ |
| Rpt Sales By Item | BGSalesByItemView | ✅ |
| Rpt Sales By Item By Type Of Customer | BGSalesByItemView | ✅ |

### Category 3: Sales by Line Reports (3 reports)

Use `BGSalesByItemLineView` or `OrderProduct` - **WORKING**

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Rpt Sales by Item Line | OrderProduct | ⚠️ Uses different view |
| Rpt Sales By Line | BGSalesByItemLineView | ✅ |
| Rpt Sales By Line With Ranking | BGSalesByItemLineView | ✅ |
| Rpt Sales By Line With Ranking (Collapsed) | BGSalesByItemLineView | ✅ |

### Category 4: Sales by Sales Group/Rep Reports (5 reports)

Use appropriate views - **WORKING**

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Rpt Sales By Sales Group | BGSalesBySalesGroupView | ✅ |
| Rpt Sales by Sales Group (Collapsed) | BGSalesBySalesGroupView | ✅ |
| Rpt Sales By Sales Rep | BGSalesBySalesRepView | ✅ |
| Rpt Sales by Sales Rep (Collapsed) | BGSalesBySalesRepView | ✅ |
| Rpt Sales Rep Monthly Report | BGSalesBySalesRepView | ✅ |

### Category 5: Commission Report (1 report)

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Rpt Commission | BGCommissionReportDataView | ✅ |

### Category 6: Net Profit Chart Reports (7 reports)

All use `BGProductInCatalog` - **WORKING**

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Net Profit Chart (catalog) | BGProductInCatalog | ✅ |
| Net Profit Chart (Catalog) Last Price Paid | BGProductInCatalog | ✅ |
| Net Profit Chart (Catalog) Sales Price | BGProductInCatalog | ✅ |
| Net Profit Chart (Customer Order) | BGProductInCatalog | ✅ |
| Net Profit Chart (Customer Orders) | BGProductInCatalog | ✅ |
| Net Profit Chart (Factory Order) | BGProductInCatalog | ✅ |
| Net Profit Chart (product) | BGProductInCatalog | ✅ |

### Category 7: Inventory Reports (2 reports)

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Inventory Adjustment Report | OrderProduct | ✅ |
| Inventory Chart | OrderProduct | ✅ |

### Category 8: Account Reports (2 reports)

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Account Address | Account | ✅ |
| Account Email | Account | ✅ |

### Category 9: Warehouse/Test Reports (2 reports)

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| Warehouse Order | OrderProduct | ✅ |
| test CSV | OrderProduct | ✅ |

### Category 10: Problem Report (1 report)

| Report Name | IntEsq.rootSchemaName | Status |
|-------------|----------------------|--------|
| **Rpt CustomersDidNotBuyOverAPeriodOfTime** | BGSalesByCustomerView | ❌ **WRONG** |

---

## EntitySchemaId vs IntEsq.rootSchemaName Mapping

### Observations

1. **EntitySchemaId and rootSchemaName often don't match** - This is BY DESIGN
   - IntEntitySchemaId points to the "parent" or "configuration" schema
   - IntEsq.rootSchemaName is the actual query target

2. **Multiple reports share the same IntEsq.rootSchemaName** - Expected
   - 6 reports use BGSalesByCustomerView
   - 3 reports use BGSalesByItemView
   - 4 reports use BGSalesByItemLineView
   - 3 reports use BGSalesBySalesRepView
   - 7 reports use BGProductInCatalog

3. **Reports with OrderProduct as rootSchemaName:**
   - Inventory Adjustment Report
   - Inventory Chart
   - Rpt Sales by Item Line
   - test CSV
   - Warehouse Order

---

## View to Column Mapping

### BGSalesByCustomerView Columns (16)
```
BGStatus, BGCustomer, BGShipDate, BGInvoiceDate, BGAmount, BGPONumber,
BGNumber, BGDeliveryDate, BGSalesRep, BGSalesGroup, BGReportStartDate,
BGReportEndDate, Filters, BGPastDue, BGTotalOverdue, BGAmountDue
```

### BGSalesByItemView Columns (12)
```
BGSalesRep, BGSalesGroup, BGCustomer, BGQuantity, BGItem, BGAmount,
BGPrice, BGDeliveryDate, BGShipDate, BGStatus, BGInvoiceDate, BGNumber
```
**Note:** Missing `BGProductDescription` - see RPT-006 for DESCRIPCION fix.

### BGSalesByItemLineView Columns (9)
```
BGItem, BGLine, BGQuantity, BGAmount, BGReportStartDate, BGReportEndDate,
Filters, BGSalesGroup, BGSalesRep
```

### BGSalesBySalesGroupView Columns (17)
```
BGSalesRep, BGSalesGroup, BGStatus, BGShipDate, BGInvoiceDate, BGAmount,
BGPONumber, BGNumber, BGDeliveryDate, BGReportStartDate, BGReportEndDate,
Filters, BGCustomer, BGPastDue, BGTotalOverdue, BGAmountDue, BGLine
```

### BGSalesBySalesRepView Columns (10)
```
BGCustomer, BGDeliveryDate, BGShipDate, BGInvoiceDate, BGAmount,
BGPONumber, BGNumber, BGSalesRep, BGSalesGroup, BGStatus
```

### BGCommissionReportDataView Columns (13)
```
Sales Rep, Sales Group, Customer, PO Number, Invoice Date, Amount,
Commission, Commission Rate Percentage, YearMonth, Status, BGDeliveryDate,
BGFilters, BGReportExecutionId
```

### BGCustomerDidNotBuyView Columns (Expected)
```
Id, BGAccountId (FK to Account), BGLastOrderId (FK to Order),
BGEmail (direct), BGPreviousOrderCount (direct), BGFilters, BGExecutionId
```
**Note:** Customer details (Name, Address, City, State, ZIP, Phone) must be accessed via ESQ relationship columns: `BGAccount.Name`, `BGAccount.Address`, etc.

---

## Recommendations

### Immediate Action (RPT-005)

1. ✅ **Backend routing fixed** - Routes by IntName, not just schema
2. 🔄 **Backend column mapping** - Update `QueryCustomerDidNotBuyData()` to use:
   ```csharp
   esq.AddColumn("BGAccount.Name");        // Customer name
   esq.AddColumn("BGAccount.Address");     // Address
   esq.AddColumn("BGAccount.City.Name");   // City (lookup)
   esq.AddColumn("BGAccount.Region.Name"); // State (lookup)
   esq.AddColumn("BGAccount.Zip");         // ZIP
   esq.AddColumn("BGEmail");               // Direct from view
   esq.AddColumn("BGAccount.Phone");       // Phone
   esq.AddColumn("BGPreviousOrderCount");  // Direct from view
   ```

### Long-Term Fixes

1. **Fix IntExcelReport.IntEsq** for "Rpt CustomersDidNotBuyOverAPeriodOfTime":
   - Change rootSchemaName from `BGSalesByCustomerView` to `BGCustomerDidNotBuyView`
   - Update column list to match correct view

2. **Add BGProductDescription to BGSalesByItemView** (RPT-006):
   - View modification to JOIN Product entity
   - Update backend column mapping

---

## Appendix: All IntExcelReport GUIDs

| Report Name | GUID |
|-------------|------|
| Account Address | a321f7bf-00cb-4f9a-af7e-02c13913779b |
| Account Email | eca07ecf-79b5-493e-9e4d-d4f35fa63323 |
| Inventory Adjustment Report | 4bf08cd3-f42d-4ce6-b032-e85dca4f4ddb |
| Inventory Chart | 7bfec367-e648-44e3-bf24-7569bd215d6e |
| Items by Customer | d213933b-093d-47fc-8da8-422c0d9bf715 |
| Net Profit Chart (catalog) | 0771aae8-ce47-4f6a-8796-c939ba1ace88 |
| Net Profit Chart (Catalog) Last Price Paid | 6f9f3112-a9b9-4829-870f-278fc172aa29 |
| Net Profit Chart (Catalog) Sales Price | 2b9d3c0e-e5a0-463b-b7ae-49926550a2f1 |
| Net Profit Chart (Customer Order) | 2110ecbc-e240-4828-bf18-a5f0daf62128 |
| Net Profit Chart (Customer Orders) | 410dd95c-9b1f-4c75-b195-88c1678b5bc3 |
| Net Profit Chart (Factory Order) | b1c0b66d-3de6-4ddc-91f8-59cede9fbda8 |
| Net Profit Chart (product) | 0887cc48-f9eb-4241-b853-71735dccef6a |
| Rpt Commission | 4ba4f203-7088-41dc-b86d-130c590b3594 |
| Rpt CustomersDidNotBuyOverAPeriodOfTime | 1f65a56a-d7f4-4ce2-b517-c633872ea545 |
| Rpt Sales By Customer | 62d81c91-13d2-4edf-9827-1f9e35ce03d9 |
| Rpt Sales By Customer (Collapsed) | ddb6bfa4-2c58-44b9-814d-91ee0c02c989 |
| Rpt Sales By Customer Type | 6e11dc16-df10-47c4-97be-9695f3feb77a |
| Rpt Sales by Customer Type (Collapsed) | 7592aced-1315-4475-bd13-da12e6c5750b |
| Rpt Sales by Customer Year Comparison | f7e2a69d-8a3e-4f1e-ba8a-d0cd8b3b1a53 |
| Rpt Sales By Customer Year Comparison (Collapsed) | f336165b-f6b7-4a55-bcf1-3f24bae73d26 |
| Rpt Sales By Item | c4f4e32c-376d-4b19-b04b-2129dba29d06 |
| Rpt Sales By Item By Type Of Customer | 53682214-a63c-407a-b3f1-79d8ab235f18 |
| Rpt Sales by Item Line | 1d009377-3cef-4199-9e38-7b47ddb27a0d |
| Rpt Sales By Line | 0b40d51d-4935-4918-97f2-45352aed341f |
| Rpt Sales By Line With Ranking | 384bf7f6-28fa-4f65-bd64-1a45d96a09e8 |
| Rpt Sales By Line With Ranking (Collapsed) | ba330b02-630e-4f5e-8d60-3e7c0560aa5b |
| Rpt Sales By Sales Group | a935a791-e2ff-4693-9b50-38a8596a3667 |
| Rpt Sales by Sales Group (Collapsed) | 6e9d462b-99ef-4e6c-9c7c-f425721be455 |
| Rpt Sales By Sales Rep | 50b59be9-1fab-449a-a257-11dce5ec1434 |
| Rpt Sales by Sales Rep (Collapsed) | 41afd5e9-7043-4bb8-a52f-0f927bc3505f |
| Rpt Sales Rep Monthly Report | 5b39f08f-3b55-4963-b74d-eddfb540bdba |
| test CSV | eade67be-dfd4-4cd5-a07f-86f0b343a71c |
| Warehouse Order | b652ba04-fa7c-4447-95ba-d73f2d6c1f9e |

---

*Analysis completed: 2026-01-30*
*Analyst: Claude Code*
