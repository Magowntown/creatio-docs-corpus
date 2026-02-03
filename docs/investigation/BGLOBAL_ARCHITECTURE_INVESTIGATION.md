# BGlobal Original Architecture Investigation

**Date:** 2026-01-28
**Purpose:** Document BGlobal's original Excel report architecture vs our custom implementation

---

## Summary: What We Learned

### 1. IntGenerateExcelReportUserTask EXISTS

**GUID:** `05c5265c-3f51-4114-9862-fc434abe1f6d`
**Manager:** ProcessUserTaskSchemaManager
**Status:** Deployed in PROD

This is BGlobal's **original business process** for generating Excel reports. It:
- Reads IntExcelReport template definitions
- Uses IntExcelExport library to generate Excel bytes
- Stores bytes in SESSION with generated key
- BGIntExcelReportService2 then downloads those bytes

### 2. BGReportExecution - Filter Storage Mechanism

**Total Records:** 117 (in PROD)
**Reports with records:** Commission (111), Sales By Sales Group (3), Sales By Customer (2), Sales Rep Monthly Report (1)

**Reports WITHOUT records (0 records):**
- Items by Customer
- IW_Commission
- Sales By Item
- Sales By Line
- And several others

**Critical Finding:** "Items by Customer" has **NO BGReportExecution records** - meaning this report was NEVER used with BGlobal's original filter-passing mechanism.

### 3. Original Classic UI (v7) Flow

```
USER CLICKS REPORT BUTTON
        ↓
BGIntExcelreportMixin (Classic UI Mixin)
[Schema UID: a589d29b-9da7-4f66-836b-8e39fe0ca376]
        ↓
Creates BGReportExecution record with filters
        ↓
Triggers IntGenerateExcelReportUserTask business process
        ↓
Business process reads IntExcelReport.IntEsq + filters from BGReportExecution
        ↓
Generates Excel bytes using IntExcelExport library
        ↓
Stores bytes in SessionData[key]
        ↓
BGIntExcelReportService2.GetExportFilteredData(name, key)
        ↓
Downloads bytes from SessionData
        ↓
EXCEL FILE DOWNLOADS
```

### 4. IntExcelReport Configuration Table

| Report | GUID | IntEntitySchemaId | Entity Schema |
|--------|------|------------------|---------------|
| Rpt Commission | 4ba4f203-7088-41dc-b86d-130c590b3594 | e60e7a82-955e-4ea9-ae1a-203dd28a0e64 | BGCommissionReportDataView |
| Items by Customer | d213933b-093d-47fc-8da8-422c0d9bf715 | 209a8e5b-a6e3-40f5-b8fb-b37133439fb6 | BGSalesByItemView |
| Rpt Sales By Line | 0b40d51d-4935-4918-97f2-45352aed341f | 28458bfc-078d-440e-ab86-27adea4d5a88 | BGSalesByLineView |
| Rpt Sales By Customer | 62d81c91-13d2-4edf-9827-1f9e35ce03d9 | c271da12-0ded-4154-b3eb-a9d97510314c | BGSalesByCustomerView |
| Rpt Sales By Sales Group | a935a791-e2ff-4693-9b50-38a8596a3667 | d88712a0-cb0d-48b3-abb1-bfd4f9d4ae64 | BGSalesBySalesGroupView |

---

## Our Custom Implementation vs Original

### What We Built

| Component | File | Purpose |
|-----------|------|---------|
| **UsrExcelReportService** | `source-code/UsrExcelReportService_Updated.cs` | Custom backend service |
| **v21 Handler** | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v21_Complete.js` | Freedom UI frontend handler |

### Why We Built It

1. **Freedom UI Incompatibility:** Classic UI mixins don't work in Freedom UI (v8)
2. **IntExcelReportService Bug:** Built-in service returns 404 on GetReport
3. **Session Data Issue:** Library doesn't store bytes in SessionData properly

### Architectural Comparison

| Aspect | Original BGlobal | Our Custom |
|--------|-----------------|------------|
| Frontend trigger | BGIntExcelreportMixin | v21 Handler |
| Filter storage | BGReportExecution record | Request parameters + BGReportExecution |
| Generation | IntGenerateExcelReportUserTask (business process) | UsrExcelReportService.Generate() |
| Library used | IntExcelExport | IntExcelExport (same) |
| Download service | BGIntExcelReportService2 | UsrExcelReportService.GetReport() |
| Session storage | Business process -> SessionData | Service method -> SessionData |

---

## "Items by Customer" Issue Analysis

### Why It Never Had BGReportExecution Records

Possible explanations:
1. **Never used with original flow** - May have been a newer report added without proper filter configuration
2. **Different filter mechanism** - May have used IntEsq filters instead of BGReportExecution
3. **Never actually worked** - May have been broken even in Classic UI

### Current Implementation

Our `UsrExcelReportService` has a custom generator `GenerateSalesByItemWithFilters` that:
1. Queries `BGSalesByItemView` directly (4.8M rows in view)
2. Filters on `BGCustomer` (varchar) using LIKE '%CustomerName%'
3. Applies optional date filters (CreatedFrom/To, ShippingFrom/To, DeliveryFrom/To)

### Why "No Data Found"

Console log showed: `Customer=Pampa Bay, CreatedFrom=2026-01-26, CreatedTo=2026-01-28`

Possible causes:
1. **Customer name mismatch:** `BGCustomer` varchar may store different format than "Pampa Bay"
2. **Narrow date range:** 2-day window (Jan 26-28) may have no orders
3. **CreatedOn vs other dates:** View may not have `CreatedOn` column, or data uses different date columns

---

## Recommendations

### Option A: Keep Custom Implementation (Recommended)

**Pros:**
- Already working for Commission reports
- We control the code and can debug
- BGReportExecution creation maintains compatibility with SQL views

**Cons:**
- "Items by Customer" needs fixing
- Different from original BGlobal architecture

### Option B: Try to Restore Original Flow

**Pros:**
- Uses BGlobal's original business process
- More consistent with other Creatio installations

**Cons:**
- IntGenerateExcelReportUserTask may not be callable from Freedom UI
- Classic UI mixin (BGIntExcelreportMixin) can't be used
- "Items by Customer" NEVER had BGReportExecution records anyway

### Option C: Hybrid - Fix "Items by Customer" Only

**Action:** Debug why "Items by Customer" returns no data:
1. Query `BGSalesByItemView` directly in SQL to verify data exists for "Pampa Bay"
2. Check exact column name and format for customer
3. Check if date columns exist in view
4. Widen date range for testing

---

## Next Steps

1. **Verify BGSalesByItemView structure:**
   ```sql
   SELECT TOP 10 "BGCustomer", "CreatedOn", "BGDeliveryDate"
   FROM "BGSalesByItemView"
   WHERE "BGCustomer" LIKE '%Pampa%';
   ```

2. **Check if customer "Pampa Bay" exists:**
   ```sql
   SELECT DISTINCT "BGCustomer"
   FROM "BGSalesByItemView"
   WHERE "BGCustomer" LIKE '%Pampa%' OR "BGCustomer" LIKE '%Bay%';
   ```

3. **Test with wider date range** (remove date filters entirely first)

4. **Check IntEsq definition** for "Items by Customer" template to see original filter configuration

---

## Files Reference

| Purpose | File |
|---------|------|
| Original service source | `/mnt/c/Users/amago/Downloads/BGIntExcelReportService2 (1).md` |
| Custom backend | `source-code/UsrExcelReportService_Updated.cs` |
| Frontend handler (PROD) | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v21_Complete.js` |
| BGReportExecution schema | `docs/BGREPORTEXECUTION_SCHEMA.md` |
| Session log | `docs/SESSION_LOG_20260128.md` |
