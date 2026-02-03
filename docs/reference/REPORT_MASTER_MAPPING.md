# Report Master Mapping - Complete Reference

**Date:** 2026-01-30
**Scope:** All 33 IntExcelReport configurations with full relationship mapping
**Purpose:** Single source of truth for all report configurations, relationships, and fixes

---

## Quick Reference

### View Pattern Types

| Pattern | Description | BGReportExecution | Filter Method |
|---------|-------------|-------------------|---------------|
| **Type A** | Execution-Based | `JOIN ... ON true` | Filter by BGExecutionId |
| **Type B** | Direct | No execution JOIN | ESQ filters at query time |

### View Usage Summary

| View | Reports Using | Pattern | Custom Generator | SQL On File |
|------|--------------|---------|------------------|-------------|
| BGCommissionReportDataView | 1 | Type A | ✅ Yes | ✅ Yes |
| BGSalesByCustomerView | 8 | Type A | ✅ Yes | ❌ No |
| BGSalesByItemView | 3 | Type B | ✅ Yes | ✅ Yes (FIXED) |
| BGSalesByItemLineView | 3 | Type A | ❌ No | ❌ No |
| BGSalesBySalesGroupView | 2 | Type A | ❌ No | ❌ No |
| BGSalesBySalesRepView | 3 | Type B | ❌ No | ❌ No |
| BGProductInCatalog | 7 | Type B | ❌ No | ❌ No |
| OrderProduct | 5 | Type B | ❌ No | ❌ No |
| Account | 2 | Type B | ❌ No | ❌ No |
| BGCustomerDidNotBuyView | 0* | Type A | ✅ Yes | ✅ Yes |

*RPT-005 misconfigured to use BGSalesByCustomerView

---

## Report Categories

### Category 1: Commission Reports (2 reports)

#### 13. Rpt Commission
| Field | Value |
|-------|-------|
| **ID** | `4ba4f203-7088-41dc-b86d-130c590b3594` |
| **Sheet** | Data |
| **rootSchemaName** | `BGCommissionReportDataView` |
| **Pattern** | Type A (Execution-Based) |
| **Columns (13)** | Sales Rep, Sales Group, Customer, PO Number, Invoice Date, Amount, Commission, Commission Rate Percentage, Transaction Date, Transaction Type, Is Note, Description, Year-Month |

**SQL View:** `sql/BGCommissionReportDataView.sql`

**Backend Code:**
- Generator: `GenerateWithDateFilter()` (line 1530)
- Query: `QueryCommissionData()` (line 692)
- Columns mapped: SalesRep, Description, TransactionDate, Commission, Amount, CommissionRate, Customer, InvoiceDate, PONumber, TransactionType, IsNote, SalesGroup

**Past Work:**
- ✅ FLT-004: Fixed DateTime filter deserialization
- ✅ Custom generator bypasses IntExcelExport library bug

**Status:** ✅ WORKING - No changes needed

---

#### IW_Commission (Not in IntExcelReport - custom)
| Field | Value |
|-------|-------|
| **View** | `IWCommissionReportDataView` |
| **Pattern** | Type B (Direct) |

**Backend Code:**
- Generator: `GenerateIWCommissionWithDateFilter()` (line 1649)
- Query: `QueryIWCommissionData()` (line 760)

**Status:** ✅ WORKING - Custom view for IW package

---

### Category 2: Sales by Customer Reports (8 reports)

All use `BGSalesByCustomerView` with same 16 columns.

#### 14. Rpt CustomersDidNotBuyOverAPeriodOfTime ⚠️ MISCONFIGURED
| Field | Value |
|-------|-------|
| **ID** | `1f65a56a-d7f4-4ce2-b517-c633872ea545` |
| **Sheet** | Data |
| **rootSchemaName** | `BGSalesByCustomerView` ❌ **WRONG** |
| **Expected View** | `BGCustomerDidNotBuyView` |
| **Pattern** | Type A (Execution-Based) |
| **Columns (16)** | BGStatus, BGCustomer, BGShipDate, BGInvoiceDate, BGAmount, BGPONumber, BGNumber, BGDeliveryDate, BGNumberInvoice, BGInvoiceNumber, BGSalesRep, BGSalesGroup, BGReportEndDate, BGReportStartDate, BGExecutionId, BGFilters |

**SQL View:** `sql/BGCustomerDidNotBuyView_ORIGINAL.sql` (correct view)

**BGCustomerDidNotBuyView Actual Columns:**
| Column | Type | Source |
|--------|------|--------|
| Id | GUID | Account.Id |
| BGAccountId | GUID FK | Account.Id (for relationship) |
| BGLastOrderId | GUID FK | Subquery → Order.Id |
| BGEmail | String | Subquery → AccountCommunication.Number |
| BGPreviousOrderCount | Integer | Subquery COUNT(*) |
| BGFilters | String | Concatenated date range text |
| BGExecutionId | GUID FK | BGReportExecution.Id |

**Relationships (verified via OData):**
| Relationship Path | Target | Status |
|-------------------|--------|--------|
| BGAccount.Name | Account.Name | ✅ Verified |
| BGAccount.Address | Account.Address | ✅ Verified |
| BGAccount.City.Name | City.Name | ✅ Verified |
| BGAccount.Region.Name | Region.Name | ✅ Verified |
| BGAccount.Zip | Account.Zip | ✅ Verified |
| BGAccount.Phone | Account.Phone | ✅ Verified |
| BGLastOrder.CreatedOn | Order.CreatedOn | ✅ Verified |
| BGLastOrder.Amount | Order.Amount | ✅ Verified |
| BGLastOrder.BGSalesRepLookup.Name | Employee.Name | ✅ Verified |
| BGLastOrder.BGSalesGroup.BGSalesGroupName | BGSalesGroup.BGSalesGroupName | ✅ Verified |

**Backend Code:**
- Generator: `GenerateCustomerDidNotBuyWithFilters()` (line 2222)
- Query: `QueryCustomerDidNotBuyData()` (line 2331)
- Helper: `CreateReportExecution()` (line 2421)
- Fallback: `QueryCustomerDidNotBuyDataDirect()` (line 2463)

**Column Mapping in Code:**
```
BGAccount.Name → Account
BGAccount.Address → Address
BGAccount.City.Name → City
BGAccount.Region.Name → State
BGAccount.Zip → ZIP
BGEmail → Email
BGAccount.Phone → Phone
BGLastOrder.CreatedOn → Last Order Date
BGLastOrder.Amount → Last Order Amount
BGPreviousOrderCount → Previous Order Count
BGLastOrder.BGSalesRepLookup.Name → Last Order Sales Rep
BGLastOrder.BGSalesGroup.BGSalesGroupName → Last Order Sales Group
BGFilters → Filters
```

**Past Work:**
- ✅ RPT-005: Identified wrong view reference
- ✅ Added routing by IntName (not just schema)
- ✅ Created execution-based query following V7 pattern
- ✅ Verified all relationship paths via OData

**Status:** 🔴 **DEPLOY NOW** - Fix ready in backend

---

#### 15. Rpt Sales By Customer
| Field | Value |
|-------|-------|
| **ID** | `62d81c91-13d2-4edf-9827-1f9e35ce03d9` |
| **Sheet** | Data |
| **rootSchemaName** | `BGSalesByCustomerView` |
| **Pattern** | Type A (Execution-Based) |
| **EntitySchemaId** | `c271da12-0ded-4154-b3eb-a9d97510314c` |

**Backend Code:**
- Generator: `GenerateSalesByCustomerWithFilters()` (line 1988)
- Query: `QuerySalesByCustomerData()` (line 2081)

**Status:** ✅ WORKING - Custom generator handles date filters

---

#### 16. Rpt Sales By Customer (Collapsed)
| Field | Value |
|-------|-------|
| **ID** | `ddb6bfa4-2c58-44b9-814d-91ee0c02c989` |
| **rootSchemaName** | `BGSalesByCustomerView` |
| **EntitySchemaId** | `c271da12-0ded-4154-b3eb-a9d97510314c` |

**Status:** ✅ Uses same view/generator as #15

---

#### 17. Rpt Sales By Customer Type
| Field | Value |
|-------|-------|
| **ID** | `6e11dc16-df10-47c4-97be-9695f3feb77a` |
| **rootSchemaName** | `BGSalesByCustomerView` |
| **EntitySchemaId** | `d81df5b9-d29a-4b4e-a867-4216d0d09ab5` |

**Status:** ✅ Uses same view/generator

---

#### 18. Rpt Sales by Customer Type (Collapsed)
| Field | Value |
|-------|-------|
| **ID** | `7592aced-1315-4475-bd13-da12e6c5750b` |
| **rootSchemaName** | `BGSalesByCustomerView` |
| **EntitySchemaId** | `d81df5b9-d29a-4b4e-a867-4216d0d09ab5` |

**Status:** ✅ Uses same view/generator

---

#### 19. Rpt Sales by Customer Year Comparison
| Field | Value |
|-------|-------|
| **ID** | `f7e2a69d-8a3e-4f1e-ba8a-d0cd8b3b1a53` |
| **rootSchemaName** | `BGSalesByCustomerView` |
| **EntitySchemaId** | `fff4bd66-8d4f-4b05-8ab7-c10ba35f5085` |

**Status:** ✅ Uses same view/generator

---

#### 20. Rpt Sales By Customer Year Comparison (Collapsed)
| Field | Value |
|-------|-------|
| **ID** | `f336165b-f6b7-4a55-bcf1-3f24bae73d26` |
| **rootSchemaName** | `BGSalesByCustomerView` |
| **EntitySchemaId** | `fff4bd66-8d4f-4b05-8ab7-c10ba35f5085` |

**Status:** ✅ Uses same view/generator

---

### Category 3: Sales by Item Reports (3 reports)

All use `BGSalesByItemView` with same 12 columns.

#### 5. Items by Customer ✅ FIXED
| Field | Value |
|-------|-------|
| **ID** | `d213933b-093d-47fc-8da8-422c0d9bf715` |
| **Sheet** | Data |
| **rootSchemaName** | `BGSalesByItemView` |
| **Pattern** | Type B (Direct) |
| **EntitySchemaId** | `209a8e5b-a6e3-40f5-b8fb-b37133439fb6` |
| **Columns (12)** | BGSalesRep, BGSalesGroup, BGCustomer, BGQuantity, BGItem, BGAmount, BGPrice, BGDeliveryDate, BGShipDate, BGPONumber, BGStatus, BGNumber |

**SQL View:** `sql/VwBGSalesByItemView_FINAL.sql` (with BGProductDescription)

**BGSalesByItemView Actual Columns:**
| Column | Type | Source |
|--------|------|--------|
| Id | GUID | Order.Id |
| CreatedOn | DateTime | Order.CreatedOn |
| BGNumber | String | Order.Number |
| BGPONumber | String | Order.BGPONumber |
| BGShipDate | DateTime | Order.BGShipDate |
| BGDeliveryDate | DateTime | Order.BGDeliveryDate |
| BGPrice | Decimal | OrderProduct.Price |
| BGAmount | Decimal | OrderProduct.TotalAmount |
| BGItem | String | Product.Name |
| **BGProductDescription** | String | Product.Description ✅ **ADDED** |
| BGQuantity | Decimal | OrderProduct.Quantity |
| BGCustomer | String | Account.Name |
| BGStatus | String | OrderStatus.Name |
| BGSalesGroup | String | BGSalesGroup.BGSalesGroupName |
| BGSalesRep | String | Employee.Name |

**Backend Code:**
- Generator: `GenerateSalesByItemWithFilters()` (line 1717)
- Query: `QuerySalesByItemData()` (line 1826)

**Column Mapping in Code (ORDER CRITICAL):**
```
Position A: BGCustomer → BGCustomer
Position B: CreatedOn → Created on
Position C: BGAmount → Last Price (VBA SUMS)
Position D: BGProductDescription → Product (DESCRIPCION)
Position E: BGItem → ProductCode (VBA GROUPS)
Position F: BGQuantity → Quantity
Position G: BGPrice → Filters
```

**Past Work:**
- ✅ RPT-006: Added BGProductDescription to view SQL
- ✅ RPT-007: Fixed Employee JOIN (26x duplicate issue)
- ✅ RPT-008: Added VBA Type mismatch fix (routing)
- ✅ UI-007: Fixed Customer ID "value" bug (v54)
- ✅ Column order matches VBA macro expectations

**Status:** ✅ WORKING - All fixes deployed

---

#### 21. Rpt Sales By Item
| Field | Value |
|-------|-------|
| **ID** | `c4f4e32c-376d-4b19-b04b-2129dba29d06` |
| **rootSchemaName (IntEsq)** | `BGSalesByItemView` ⚠️ |
| **ACTUAL Entity Schema** | `BGSalesByItemLineView` ✅ |
| **EntitySchemaId** | `28458bfc-078d-440e-ab86-27adea4d5a88` |
| **Columns (7)** | BGItem, BGLine, BGQuantity, BGAmount, BGReportStartDate, BGReportEndDate, Filters |

**Status:** ✅ Custom generator with 7 columns (per PROD_INTEXCELREPORT_CONFIGS.md)

> ⚠️ **Note:** IntEsq JSON rootSchemaName may say "BGSalesByItemView" but PROD IntExcelReport Entity Schema is "BGSalesByItemLineView"

---

#### 22. Rpt Sales By Item By Type Of Customer
| Field | Value |
|-------|-------|
| **ID** | `53682214-a63c-407a-b3f1-79d8ab235f18` |
| **rootSchemaName (IntEsq)** | `BGSalesByItemView` ⚠️ |
| **ACTUAL Entity Schema** | `BGSalesByItemLineView` ✅ |
| **EntitySchemaId** | `28458bfc-078d-440e-ab86-27adea4d5a88` |
| **Columns (6)** | BGItem, Description, BGCustomerType, BGQuantity, BGAmount, Filters |

**Status:** ✅ Custom generator with 6 columns (DIFFERENT from "Rpt Sales By Item"!)

> ⚠️ **Note:** Despite same view as "Rpt Sales By Item", VBA expects DIFFERENT 6 columns - separate handler required

---

### Category 4: Sales by Line Reports (3 reports)

#### 24. Rpt Sales By Line
| Field | Value |
|-------|-------|
| **ID** | `0b40d51d-4935-4918-97f2-45352aed341f` |
| **Sheet** | Data |
| **rootSchemaName** | `BGSalesByItemLineView` |
| **Pattern** | Type A (Execution-Based) |
| **EntitySchemaId** | `28458bfc-078d-440e-ab86-27adea4d5a88` |
| **Columns (9)** | BGItem, BGLine, BGQuantity, BGAmount, BGReportStartDate, BGReportEndDate, Filters, BGSalesGroup, BGSalesRep |

**Backend Code:** None (uses IntExcelExport library)

**Status:** ⚠️ No custom generator - may need one if issues arise

---

#### 25. Rpt Sales By Line With Ranking
| Field | Value |
|-------|-------|
| **ID** | `384bf7f6-28fa-4f65-bd64-1a45d96a09e8` |
| **rootSchemaName** | `BGSalesByItemLineView` |
| **EntitySchemaId** | `a8c4ae73-a04a-4a7b-937c-9eb1ef478bbb` |
| **Columns (20)** | BGLine, BGSalesRep, BGSalesGroup, BGStatus, BGCustomer, BGQuantity, BGItem, BGAmount, BGPrice, BGDeliveryDate, BGShipDate, BGPONumber, BGNumber, BGReportStartDate, BGReportEndDate, BGNumberInvoice, BGExecutionId, BGFilters, **BGDescription**, BGCustomerType |

**Note:** This view already has `BGDescription` column

**Status:** ⚠️ No custom generator

---

#### 26. Rpt Sales By Line With Ranking (Collapsed)
| Field | Value |
|-------|-------|
| **ID** | `ba330b02-630e-4f5e-8d60-3e7c0560aa5b` |
| **rootSchemaName** | `BGSalesByItemLineView` |

**Status:** ⚠️ No custom generator

---

### Category 5: Sales by Sales Group Reports (2 reports)

#### 27. Rpt Sales By Sales Group
| Field | Value |
|-------|-------|
| **ID** | `a935a791-e2ff-4693-9b50-38a8596a3667` |
| **Sheet** | Data |
| **rootSchemaName** | `BGSalesBySalesGroupView` |
| **Pattern** | Type A (Execution-Based) |
| **EntitySchemaId** | `d88712a0-cb0d-48b3-abb1-bfd4f9d4ae64` |
| **Columns (17)** | BGSalesRep, BGSalesGroup, BGStatus, BGShipDate, BGInvoiceDate, BGAmount, BGPONumber, BGNumber, BGCustomer, BGDeliveryDate, BGNumberInvoice, BGInvoiceNumber, BGDescription, BGReportEndDate, BGReportStartDate, BGExecutionId, BGFilters |

**Backend Code:** None (uses IntExcelExport library)

**Status:** ⚠️ No custom generator - may need one if issues arise

---

#### 28. Rpt Sales by Sales Group (Collapsed)
| Field | Value |
|-------|-------|
| **ID** | `6e9d462b-99ef-4e6c-9c7c-f425721be455` |
| **rootSchemaName** | `BGSalesBySalesGroupView` |

**Status:** ⚠️ No custom generator

---

### Category 6: Sales by Sales Rep Reports (3 reports)

#### 29. Rpt Sales By Sales Rep
| Field | Value |
|-------|-------|
| **ID** | `50b59be9-1fab-449a-a257-11dce5ec1434` |
| **Sheet** | Data |
| **rootSchemaName** | `BGSalesBySalesRepView` |
| **Pattern** | Type B (Direct) |
| **EntitySchemaId** | `c271da12-0ded-4154-b3eb-a9d97510314c` |
| **Columns (10)** | BGCustomer, BGDeliveryDate, BGShipDate, BGInvoiceDate, BGAmount, BGPONumber, BGNumber, BGSalesRep, BGSalesGroup, BGStatus |

**Backend Code:** None

**Status:** ✅ Uses IntExcelExport library (Type B, no execution issues)

---

#### 30. Rpt Sales by Sales Rep (Collapsed)
| Field | Value |
|-------|-------|
| **ID** | `41afd5e9-7043-4bb8-a52f-0f927bc3505f` |
| **rootSchemaName** | `BGSalesBySalesRepView` |

**Status:** ✅ Uses IntExcelExport library

---

#### 31. Rpt Sales Rep Monthly Report
| Field | Value |
|-------|-------|
| **ID** | `5b39f08f-3b55-4963-b74d-eddfb540bdba` |
| **rootSchemaName** | `BGSalesBySalesRepView` |
| **EntitySchemaId** | `9234a578-cf93-4b52-a830-1f9c358a8f86` |

**Status:** ✅ Uses IntExcelExport library

---

### Category 7: Net Profit Chart Reports (7 reports)

All use `BGProductInCatalog` with same 6 columns: CODE, LINE, DESCRIPTION, QUANTITY, FOB, SALES PRICE

#### 6. Net Profit Chart (catalog)
| Field | Value |
|-------|-------|
| **ID** | `0771aae8-ce47-4f6a-8796-c939ba1ace88` |
| **Sheet** | CatalogProduct |
| **rootSchemaName** | `BGProductInCatalog` |
| **EntitySchemaId** | `3ee864f5-2582-4b87-a5aa-97d9d3c48458` |

**Status:** ✅ Uses IntExcelExport library

---

#### 7-12. Other Net Profit Charts

| # | Name | ID | Sheet |
|---|------|-----|-------|
| 7 | Net Profit Chart (Catalog) Last Price Paid | `6f9f3112-a9b9-4829-870f-278fc172aa29` | NPCLastPricePaid |
| 8 | Net Profit Chart (Catalog) Sales Price | `2b9d3c0e-e5a0-463b-b7ae-49926550a6f1` | CatalogProduct |
| 9 | Net Profit Chart (Customer Order) | `2110ecbc-e240-4828-bf18-a5f0daf62128` | OrderProduct |
| 10 | Net Profit Chart (Customer Orders) | `410dd95c-9b1f-4c75-b195-88c1678b5bc3` | OrderProduct |
| 11 | Net Profit Chart (Factory Order) | `b1c0b66d-3de6-4ddc-91f8-59cede9fbda8` | OrderProduct |
| 12 | Net Profit Chart (product) | `0887cc48-f9eb-4241-b853-71735dccef6a` | Product |

**Status:** All ✅ Use IntExcelExport library

---

### Category 8: Inventory Reports (2 reports)

Both use `OrderProduct` with same 26 columns.

#### 3. Inventory Adjustment Report
| Field | Value |
|-------|-------|
| **ID** | `4bf08cd3-f42d-4ce6-b032-e85dca4f4ddb` |
| **Sheet** | InventoryAdjustment |
| **rootSchemaName** | `OrderProduct` |
| **EntitySchemaId** | `000f3deb-9629-42b3-a911-611f94a30f5b` |
| **Columns (26)** | Storer, ORDER_ID, PO_NUM, PO_Cons, NOTES, Payment Type, Shipping Method, Name, Store Number, ADDRESS1, ADDRESS2, CITY, STATE, ZIP, COUNTRY, PHONE, SHIP_DATE, Line, QUANTITY, EACHES, SKU, UPC, DESCRIPTION, TYPE, DEPARTMENT, CID |

**Status:** ✅ Uses IntExcelExport library

---

#### 4. Inventory Chart
| Field | Value |
|-------|-------|
| **ID** | `7bfec367-e648-44e3-bf24-7569bd215d6e` |
| **Sheet** | InventoryChart |
| **rootSchemaName** | `OrderProduct` |
| **EntitySchemaId** | `a31247aa-b718-40ed-982e-5b569d7d7b0e` |

**Status:** ✅ Uses IntExcelExport library

---

### Category 9: Account Reports (2 reports)

#### 1. Account Address
| Field | Value |
|-------|-------|
| **ID** | `a321f7bf-00cb-4f9a-af7e-02c13913779b` |
| **Sheet** | AccountAddress |
| **rootSchemaName** | `Account` |
| **EntitySchemaId** | `8ab0fe8a-0340-41ac-8b09-b11f65dd83da` |
| **Columns (2)** | Name, Address |

**Status:** ✅ Simple report, uses IntExcelExport library

---

#### 2. Account Email
| Field | Value |
|-------|-------|
| **ID** | `eca07ecf-79b5-493e-9e4d-d4f35fa63323` |
| **Sheet** | AccountCommunication |
| **rootSchemaName** | `Account` |
| **EntitySchemaId** | `81c43461-0619-44dd-8071-b724128085c6` |
| **Columns (3)** | Name, Address, Email |

**Status:** ✅ Simple report, uses IntExcelExport library

---

### Category 10: Item Line Report (1 report)

#### 23. Rpt Sales by Item Line
| Field | Value |
|-------|-------|
| **ID** | `1d009377-3cef-4199-9e38-7b47ddb27a0d` |
| **Sheet** | Data |
| **rootSchemaName** | `OrderProduct` |
| **EntitySchemaId** | `28458bfc-078d-440e-ab86-27adea4d5a88` |
| **Columns (26)** | Same as Inventory reports |

**Note:** Uses OrderProduct directly, not a BG view

**Status:** ✅ Uses IntExcelExport library

---

### Category 11: Warehouse/Test Reports (2 reports)

#### 32. test CSV
| Field | Value |
|-------|-------|
| **ID** | `eade67be-dfd4-4cd5-a07f-86f0b343a71c` |
| **Sheet** | Account |
| **rootSchemaName** | `OrderProduct` |
| **EntitySchemaId** | `25d7c1ab-1de0-4501-b402-02e0e5a72d6e` |

**Status:** ⚠️ Test report - likely unused

---

#### 33. Warehouse Order
| Field | Value |
|-------|-------|
| **ID** | `b652ba04-fa7c-4447-95ba-d73f2d6c1f9e` |
| **Sheet** | WOrder |
| **rootSchemaName** | `OrderProduct` |
| **EntitySchemaId** | `a31247aa-b718-40ed-982e-5b569d7d7b0e` |

**Status:** ✅ Uses IntExcelExport library

---

## SQL Scripts Reference

### On File

| Script | Purpose | View | Status |
|--------|---------|------|--------|
| `BGCommissionReportDataView.sql` | Commission view definition | BGCommissionReportDataView | Reference |
| `BGCustomerDidNotBuyView_ORIGINAL.sql` | Customers didn't buy view | BGCustomerDidNotBuyView | Reference |
| `VwBGSalesByItemView_FINAL.sql` | Items by Customer view | BGSalesByItemView | ✅ Applied to PROD |
| `VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql` | Duplicate row fix | BGSalesByItemView | ✅ Applied |
| `BGSalesByItemView_fix.sql` | Add BGProductDescription | BGSalesByItemView | ✅ Applied |
| `ALL_VIEWS_ADD_PRODUCT_DESCRIPTION.sql` | Multiple view updates | Various | Reference |

### Needed But Not On File

| View | Why Needed |
|------|-----------|
| BGSalesByCustomerView | Type A view, may need for debugging |
| BGSalesByItemLineView | Type A view with BGDescription |
| BGSalesBySalesGroupView | Type A view |

---

## Backend Code Reference

### Custom Generators

| Method | Line | Reports Handled |
|--------|------|-----------------|
| `GenerateWithDateFilter()` | 1530 | Rpt Commission |
| `GenerateWithDateFilterAllTime()` | 1594 | Commission (no filter) |
| `GenerateIWCommissionWithDateFilter()` | 1649 | IW_Commission |
| `GenerateSalesByItemWithFilters()` | 1717 | Items by Customer, Sales By Item |
| `GenerateSalesByCustomerWithFilters()` | 1988 | Sales By Customer (6 variants) |
| `GenerateCustomerDidNotBuyWithFilters()` | 2222 | Customers Did Not Buy |

### Custom Query Methods

| Method | Line | View Queried |
|--------|------|--------------|
| `QueryCommissionData()` | 692 | BGCommissionReportDataView |
| `QueryIWCommissionData()` | 760 | IWCommissionReportDataView |
| `QuerySalesByItemData()` | 1826 | BGSalesByItemView |
| `QuerySalesByCustomerData()` | 2081 | BGSalesByCustomerView |
| `QueryCustomerDidNotBuyData()` | 2331 | BGCustomerDidNotBuyView |
| `QueryCustomerDidNotBuyDataDirect()` | 2463 | Account (fallback) |

---

## Action Items Summary

### Immediate

| Report | Action | Status |
|--------|--------|--------|
| RPT-005 (Customers Did Not Buy) | Deploy backend fix | 🔴 **DEPLOY NOW** |

### Monitor

| Report | Concern | Watch For |
|--------|---------|-----------|
| Sales by Line (24-26) | No custom generator | Performance issues |
| Sales by Sales Group (27-28) | No custom generator | Performance issues |

### None Required

- All other 27 reports working correctly
- No configuration changes needed

---

## EntitySchemaId Mapping

Some reports share EntitySchemaId but different views:

| EntitySchemaId | Reports Using | Notes |
|----------------|---------------|-------|
| `c271da12-0ded-4154-b3eb-a9d97510314c` | #15, #16, #29 | Mixed Customer/Rep |
| `d81df5b9-d29a-4b4e-a867-4216d0d09ab5` | #17, #18, #30 | Mixed Type/Rep |
| `28458bfc-078d-440e-ab86-27adea4d5a88` | #21, #22, #23, #24 | Mixed Item/Line |
| `a31247aa-b718-40ed-982e-5b569d7d7b0e` | #4, #9, #11, #33 | OrderProduct variants |

This mismatch between EntitySchemaId and rootSchemaName is BY DESIGN - IntEntitySchemaId points to configuration, rootSchemaName is the actual query target.

---

*Master mapping completed: 2026-01-30*
*Analyst: Claude Code*
