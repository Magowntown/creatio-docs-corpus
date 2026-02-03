# Handoff Document: Creatio Reports System

**Date:** 2026-01-30
**To:** e6solutions Team

---

## Executive Summary

The Creatio Reports system has been fixed and deployed to both **PROD** and **DEV**. This document explains what was changed, where to find everything in Creatio, and how to continue development.

---

## What Was Fixed

### Report Issues

| Issue | Problem | Solution |
|-------|---------|----------|
| "Items by Customer" wrong column D | Showed order numbers instead of product descriptions | Added `BGProductDescription` column to view, updated backend mapping |
| "Items by Customer" 26x duplicate rows | Employee JOIN pulled all employees in sales group | Changed JOIN to use Order's sales rep lookup |
| "Sales By Item By Type Of Customer" Excel hangs | VBA infinite loop bug | Fixed anchor variable in VBA macro |
| "Rpt Sales By Item" wrong columns | Backend routed to wrong generator | Changed routing to check report name first |
| "Customers did not buy" wrong columns | Backend used wrong ESQ column paths | Fixed to use relationship columns (BGAccount.Name, etc.) |
| Filter visibility not working | Frontend helper functions were missing | Redeployed complete frontend code |

### All Reports Now Working

**Excel Downloads:** Items by Customer, Rpt Sales By Item, Sales By Item By Type Of Customer, Customers did not buy, Rpt Sales By Line, Rpt Open Orders, Commission, IW_Commission

**Looker Studio:** Rpt Sales By Customer, Rpt Sales By Customer Type, Rpt Sales By SalesRep, Sales By Sales Group, Rpt Shipped Order, Rpt Pending Invoices

---

## Creatio Locations

### PROD Environment

| Component | Location |
|-----------|----------|
| **Reports Page** | `https://pampabay.creatio.com/0/ClientApp/#/UsrPage_ebkv9e8` |
| **Frontend Schema** | Configuration → BGApp_eykaguu package → `UsrPage_ebkv9e8` (ClientUnitSchema) |
| **Backend Service** | Configuration → Custom package → `UsrExcelReportService` (SourceCodeSchema) |
| **SQL View** | Configuration → PampaBay package → `BGSalesByItemView` SqlScript |
| **View Object** | Configuration → PampaBay package → `BGSalesByItemView` (Object/Entity) |

### DEV Environment

| Component | Location |
|-----------|----------|
| **Reports Page** | `https://dev-pampabay.creatio.com/0/ClientApp/#/UsrPage_ebkv9e8` |
| **Frontend Schema** | Configuration → BGApp_eykaguu package → `UsrPage_ebkv9e8` (ClientUnitSchema) |
| **Backend Service** | Configuration → Custom package → `UsrExcelReportService` (SourceCodeSchema) |
| **SQL View** | Configuration → PampaBay package → `BGSalesByItemView` SqlScript |
| **View Object** | Configuration → PampaBay package → `BGSalesByItemView` (Object/Entity) |

---

## Architecture Overview

### Report Types

| Type | Identifier | Behavior |
|------|------------|----------|
| **Looker Studio** | Has `UsrURL` in UsrReportesPampa record | Opens iframe with Looker dashboard |
| **Excel Download** | No `UsrURL` | Calls backend service, downloads .xlsm file |

### How Reports Work

```
User selects report from dropdown (UsrReportesPampa lookup)
         ↓
Frontend checks if report has UsrURL
         ↓
    ┌────┴────┐
    ↓         ↓
LOOKER     EXCEL
Shows      Calls /0/rest/UsrExcelReportService/Generate
iframe     with filters (dates, customer, yearmonth, etc.)
           ↓
           Backend finds IntExcelReport template
           ↓
           Routes to specific generator based on report name
           ↓
           Queries data via ESQ
           ↓
           Returns download key
           ↓
           Frontend downloads via hidden iframe
```

### Backend Routing Logic

The backend (`UsrExcelReportService.Generate`) routes reports by checking the **report name first**, then falls back to entity schema:

```
1. Get report name from IntExcelReport.IntName
2. Route by name:
   - "Commission" → Commission generator
   - "IW_Commission" → IW Commission generator
   - "Items by Customer" → Sales by Item generator
   - "Rpt Sales By Item" → Sales by Item Line generator
   - "Rpt Sales By Item By Type Of Customer" → Type of Customer generator
   - "Customers did not buy" / "Rpt CustomersDidNotBuyOverAPeriodOfTime" → Customer Did Not Buy generator
3. If no name match, route by IntEsq.rootSchemaName (entity schema)
```

**⚠️ IMPORTANT:** Always check report name FIRST. Some IntExcelReport records have incorrect `rootSchemaName` in their IntEsq JSON due to legacy data.

---

## Frontend Structure (UsrPage_ebkv9e8)

### Key Elements

| Element | Purpose |
|---------|---------|
| `LookupAttribute_0as4io2` | Report dropdown (UsrReportesPampa lookup) |
| `UsrCommissionFiltersContainer` | YearMonth + SalesGroup filters (Commission reports) |
| `UsrCustomerFilterContainer` | Customer button + label (Items by Customer) |
| `GridContainer_xdy25v1` | Date From/To filters |
| `GridContainer_knkow5v` | Status filter |
| `GridContainer_fh039aq` | Looker iframe container |
| `Button_vae0g6x` | Generate/Download button |

### Visibility Attributes

| Attribute | Controls |
|-----------|----------|
| `UsrShowCommissionFilters` | YearMonth + SalesGroup visibility |
| `UsrShowCustomerFilter` | Customer selection visibility |
| `UsrShowDateFilters` | Date + Status filter visibility |
| `UsrShowLookerFrame` | Looker iframe visibility |

### Handler Requests

| Request | Trigger |
|---------|---------|
| `crt.HandleViewModelInitRequest` | Page load - initializes state |
| `crt.HandleViewModelAttributeChangeRequest` | Report selection or filter change |
| `usr.OpenCustomerLookup` | Customer button click - opens Account lookup |
| `usr.GenerateReportRequest` | Generate button click |
| `crt.LoadDataRequest` | Data loading - applies cascade filter for SalesGroup |

### ⚠️ CRITICAL: Do Not Edit in System Designer

The frontend code has **helper functions defined BEFORE the return statement**:

```javascript
define("UsrPage_ebkv9e8", function(sdk) {
    // HELPER FUNCTIONS - These get STRIPPED if you edit in designer!
    function getBpmcsrf() { ... }
    function toWcfDate(date) { ... }
    function formatDateForLooker(dateValue) { ... }
    function setUsrIframeUrl(url) { ... }

    // STATE VARIABLES - Also get stripped!
    var cascadeFilterEnabled = false;
    var validSalesGroupIds = null;
    var selectedCustomerId = null;
    var selectedCustomerName = "";

    return {
        viewConfigDiff: [...],
        viewModelConfigDiff: [...],
        handlers: [...]
    };
});
```

If you edit directly in the Creatio System Designer, it only preserves code inside `return {}`. The helper functions and state variables get deleted, breaking the page.

**To make changes:** Export the code, edit externally, then paste the COMPLETE file back.

---

## Backend Structure (UsrExcelReportService)

### Key Methods

| Method | Purpose |
|--------|---------|
| `Generate()` | Main entry point - routes to specific generators |
| `GetReportName()` | Gets IntName from IntExcelReport |
| `GenerateWithDateFilter()` | Commission report generator |
| `GenerateIWCommissionWithDateFilter()` | IW_Commission generator |
| `GenerateSalesByItemWithFilters()` | Items by Customer generator |
| `GenerateSalesByItemReportWithFilters()` | Rpt Sales By Item generator |
| `GenerateSalesByItemByTypeOfCustomerWithFilters()` | Sales By Item By Type Of Customer |
| `GenerateCustomerDidNotBuyWithFilters()` | Customers did not buy generator |
| `GenerateSalesByCustomerWithFilters()` | Sales by Customer generator |

### Request Parameters

The frontend sends these parameters to `/0/rest/UsrExcelReportService/Generate`:

```json
{
    "EsqString": "...",           // From IntExcelReport.IntEsq
    "ReportId": "guid",           // IntExcelReport.Id
    "RecordCollection": [],       // Usually empty
    "YearMonthId": "guid",        // For Commission reports
    "SalesRepId": "guid",         // SalesGroup ID for Commission
    "CustomerId": "guid",         // For Items by Customer
    "CustomerName": "string",     // Customer display name
    "CreatedFrom": "/Date(...)/", // WCF date format
    "CreatedTo": "/Date(...)/",   // WCF date format
    "StatusName": "string"        // Status filter value
}
```

---

## SQL View: BGSalesByItemView

### Current Definition (Fixed)

```sql
CREATE VIEW "BGSalesByItemView" AS
SELECT
    o."Id",
    o."CreatedOn",
    o."CreatedById",
    o."ModifiedOn",
    o."ModifiedById",
    o."ProcessListeners",
    o."Number" AS "BGNumber",
    o."BGPONumber",
    o."BGShipDate",
    o."BGDeliveryDate",
    op."Price" AS "BGPrice",
    op."TotalAmount" AS "BGAmount",
    p."Name" AS "BGItem",
    p."Description" AS "BGProductDescription",   -- ADDED: Product description
    op."Quantity" AS "BGQuantity",
    ac."Name" AS "BGCustomer",
    os."Name" AS "BGStatus",
    sg."BGSalesGroupName" AS "BGSalesGroup",
    e."Name" AS "BGSalesRep"
FROM "Order" o
    JOIN "Account" ac ON (o."AccountId" = ac."Id")
    JOIN "OrderStatus" os ON (o."StatusId" = os."Id")
    JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id")
    LEFT JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")  -- FIXED: Was joining on SalesGroup
    JOIN "OrderProduct" op ON (op."OrderId" = o."Id")
    JOIN "Product" p ON (p."Id" = op."ProductId")
WHERE
    o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'::uuid
    AND sg.* IS NOT NULL
    AND os."Id" IN (
        '29fa66e3-ef69-4feb-a5af-ec1de125a614',
        '40de86ee-274d-4098-9b92-9ebdcf83d4fc',
        '8ab0f830-908b-40d7-80a3-7f49ef70ce70'
    );
```

### Key Fixes Applied

1. **Added `BGProductDescription`** - `p."Description" AS "BGProductDescription"`
2. **Fixed Employee JOIN** - Changed from `JOIN Employee e ON (sg."Id" = e."BGSalesGroupLookupId")` to `LEFT JOIN Employee e ON (o."BGSalesRepLookupId" = e."Id")`

The old JOIN was pulling ALL employees in a sales group, causing 26x duplicate rows.

---

## VBA Fix: Sales By Item By Type Of Customer

### Problem

The Excel macro had an infinite loop in `PMPFillReportData` subroutine. The anchor variable `sCurGroupWhile2Val` was being reset inside the While loop, making the condition always TRUE.

### Fix Applied

The anchor reset was moved to BEFORE the While loop:

```vba
' BEFORE the inner While loop - set anchor ONCE
sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
sCurGroupWhile2Val = sCurGroup2Val

While sCurGroup2Val = sCurGroupWhile2Val And sCurGroup2Val <> "" And sCurGroupVal = sCurGroupWhileVal
    ' ... loop body ...
    ' DO NOT reset sCurGroupWhile2Val inside here!

    'Grab next data set
    sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
    ' REMOVED: sCurGroupWhile2Val = sCurGroup2Val  (was causing infinite loop)
Wend
```

The fixed template is deployed to PROD. If you need to update the VBA, the fix is in module `PMPSalesbySalesRep`, subroutine `PMPFillReportData`.

---

## Testing Checklist

### Excel Reports

| Report | Filters to Set | Verify |
|--------|----------------|--------|
| Items by Customer | Customer + Date + Status | Column D has product descriptions, not order numbers |
| Rpt Sales By Item | Date + Status | 7 columns with line info |
| Sales By Item By Type Of Customer | Date + Status | VBA runs without hanging, data grouped correctly |
| Customers did not buy | Date | Shows customer name, address, city, state, ZIP, phone |
| Commission | YearMonth + SalesGroup | Downloads with commission data |
| Rpt Sales By Line | Date + Status | Line-level sales data |

### Looker Reports

| Report | Verify |
|--------|--------|
| Rpt Sales By Customer | Opens in iframe, date filters applied |
| Rpt Sales By Customer Type | Opens in iframe |
| Sales By Sales Group | Opens in iframe |

---

## Common Issues & Solutions

### "Filter fields not showing/hiding correctly"

**Cause:** Frontend helper functions were stripped out.
**Solution:** Redeploy the complete frontend code (don't edit in system designer).

### "Report downloads but Excel macro fails"

**Cause:** Column count/order mismatch between backend and VBA expectations.
**Solution:** Check backend column mapping matches the Excel template's expected columns.

### "Wrong data in report"

**Cause:** Backend routed to wrong generator.
**Solution:** Verify routing in `UsrExcelReportService.Generate()` checks report name first.

### "Duplicate rows in Items by Customer"

**Cause:** BGSalesByItemView Employee JOIN issue.
**Solution:** Verify SqlScript has the fixed JOIN: `LEFT JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")`

---

## Reference: Status GUIDs

### QB Integration Log Status

| Status | GUID |
|--------|------|
| Pending | `c97db3bc-634d-4c90-8432-ec7141c87640` |
| Processing | `fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef` |
| Processed | `e7428193-4cf1-4d1b-abae-00e93ab5e1c5` |
| Error | `bdfc60c7-55fd-4cbd-9a2c-dca2def46d80` |
| Re-Process | `ff92e20c-da27-4255-96bc-57e32f0944f4` |

### Order Status IDs (Used in View WHERE clause)

| Status | GUID |
|--------|------|
| Confirmed | `29fa66e3-ef69-4feb-a5af-ec1de125a614` |
| In Progress | `40de86ee-274d-4098-9b92-9ebdcf83d4fc` |
| Completed | `8ab0f830-908b-40d7-80a3-7f49ef70ce70` |

---

## Looker Studio Limitations

**We cannot modify Looker Studio reports.** These are external dashboards hosted by Google and embedded via iframe.

### What We Control
- Whether the iframe displays (visibility logic in frontend)
- URL parameters passed to Looker (date filters)
- The UsrIframe component that embeds the dashboard

### What We Cannot Control
- Dashboard layout, columns, or formatting
- "Expand all" functionality (UI-005) - this is a Looker Studio feature
- Google account permissions (LOOKER-001)
- Any visual or data changes within the dashboard itself

### Who Controls Looker Reports
BGlobal manages the Looker Studio dashboards. Any changes to:
- Report columns or data
- Visual formatting
- User permissions
- Dashboard structure

...must be requested from BGlobal. The Creatio side only controls the iframe embedding and filter parameters.

### Known Looker Issues

| Issue | Status | Notes |
|-------|--------|-------|
| Google permissions errors | 🔴 BGlobal Action Required | Some users can't access dashboards |
| Missing "expand all" button | ⛔ Not Fixable | Looker Studio feature limitation |

---

## Known Issues (Not Reports-Related)

### QB Sync Offline

- **Status:** QB Web Connector has been offline since 1/28/2026
- **Impact:** 635 records pending sync, January 2026 at ~48% synced
- **Action Required:** IT needs to bring connector online at `96.56.203.106:8080`

---

## Summary

All report issues have been fixed and deployed. The key things to remember:

1. **Don't edit frontend in system designer** - it strips helper functions
2. **Backend routes by report name first** - entity schema is fallback only
3. **BGSalesByItemView has two fixes** - new column + fixed JOIN
4. **VBA fix is in PMPSalesbySalesRep module** - anchor variable pattern
5. **Looker Studio reports are out of scope** - BGlobal controls those dashboards

If you have questions about specific fixes, check the routing logic in `UsrExcelReportService.Generate()` or the visibility logic in `UsrPage_ebkv9e8` handlers.

---

*Document prepared: 2026-01-30*
