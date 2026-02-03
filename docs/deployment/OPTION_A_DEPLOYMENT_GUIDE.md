# Option A Deployment Guide: Add BGProductDescription Column

**Date:** 2026-01-29
**Status:** READY FOR DEPLOYMENT

---

## Overview

This guide walks through deploying the fix for "Items by Customer" DESCRIPCION column showing order numbers instead of product descriptions.

**Two changes required:**
1. Add `BGProductDescription` column to BGSalesByItemView (via SQL or Creatio Configuration)
2. Update backend column mapping (UsrExcelReportService.cs line 1836)

---

## Step 1: Modify BGSalesByItemView

### CRITICAL FINDING

The `BGSalesByItemView` is a **SQL View** stored in the PampaBay package. Key discoveries:
- **Product table is ALREADY JOINED** via `JOIN "Product" p ON (p."Id" = op."ProductId")`
- **`BGItem` column is `p."Name"` (Product Name)**, not Product.Code
- **Fix is trivial** - just add `p."Description" AS "BGProductDescription"` to SELECT
- **Pattern exists** - `BGSalesByLineWithRankingView` already has this column

### Option 1A: SQL Script via pgAdmin (Recommended - Same as Commission Fix)

**SQL Script:** `sql/BGSalesByItemView_fix.sql`

Run in pgAdmin (or Creatio SQL Console if available):

```sql
DROP VIEW IF EXISTS "BGSalesByItemView";

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
  p."Name" AS "BGItem",                       -- Product Name (existing)
  p."Description" AS "BGProductDescription",  -- NEW: Product Description
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep"
FROM
    (((((
      "Order" o
      JOIN "Account" ac ON (o."AccountId" = ac."Id"))
      JOIN "OrderStatus" os ON (o."StatusId" = os."Id"))
      JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id"))
      JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId"))
      JOIN "OrderProduct" op ON (op."OrderId" = o."Id"))
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

### Option 1B: Using Creatio Configuration UI

If direct SQL access is not available:

1. Navigate to **Configuration** → **PampaBay** package
2. Find **SqlScript** schema for `BGSalesByItemView` (or the view definition)
3. Add the column to the SELECT clause
4. Save and Publish

---

## Step 2: Update Backend Code

### PROD Backend URL
```
https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

### Find and Replace (around line 1836)

**FIND this block:**
```csharp
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGCustomer", "BGCustomer"),         // Column A: Customer name
    Tuple.Create("BGDeliveryDate", "Created on"),     // Column B: Delivery date
    Tuple.Create("BGAmount", "Last Price"),           // Column C: Amount - VBA SUMS THIS
    Tuple.Create("BGNumber", "Product"),              // Column D: Order number (context)
    Tuple.Create("BGItem", "ProductCode"),            // Column E: Item code - VBA GROUPS BY THIS
    Tuple.Create("BGQuantity", "Quantity"),           // Column F: Quantity
    Tuple.Create("BGPrice", "Filters")                // Column G: Unit price (extra)
};
```

**REPLACE with:**
```csharp
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGCustomer", "BGCustomer"),              // Column A: Customer name
    Tuple.Create("BGDeliveryDate", "Created on"),          // Column B: Delivery date
    Tuple.Create("BGAmount", "Last Price"),                // Column C: Amount - VBA SUMS THIS
    Tuple.Create("BGProductDescription", "Product"),       // Column D: Product description - FIX for DESCRIPCION
    Tuple.Create("BGItem", "ProductCode"),                 // Column E: Item code - VBA GROUPS BY THIS
    Tuple.Create("BGQuantity", "Quantity"),                // Column F: Quantity
    Tuple.Create("BGPrice", "Filters")                     // Column G: Unit price (extra)
};
```

**Key change:** Line 4 changes from `BGNumber` to `BGProductDescription`

### Save and Compile

After making the change:
1. Click **Save**
2. Click **Compile** (or Publish)
3. Wait for compilation to complete

---

## Step 3: Test the Fix

1. **Navigate to Reports page:**
   ```
   https://pampabay.creatio.com/0/ClientApp/#/BGPage_iaptpa6
   ```

2. **Generate "Items by Customer" report:**
   - Select "Items by Customer" from dropdown
   - Select a customer (e.g., "Sisters")
   - Set date range
   - Click Download

3. **Verify Excel output:**
   - Open the downloaded Excel file
   - Check Column D (DESCRIPCION) shows product descriptions (not order numbers like "ORD-16504-3028")
   - Verify VBA macro processes correctly

---

## Deployment Order

**IMPORTANT:** Deploy in this order:

1. **FIRST:** Modify BGSalesByItemView (add column)
2. **SECOND:** Update UsrExcelReportService.cs (use new column)

If you deploy the backend first without the view change, the report will fail because `BGProductDescription` column won't exist.

---

## Rollback Plan

### If Issues After Deployment

**Quick Rollback (Backend only):**
```csharp
// Revert line ~1836 back to:
Tuple.Create("BGNumber", "Product"),
```

This restores order numbers to Column D. The view column can remain.

### Full Rollback

1. Revert backend code change
2. Remove BGProductDescription column from view (optional - won't hurt anything)

---

## Verification Checklist

| Check | Expected Result |
|-------|-----------------|
| View has BGProductDescription column | Yes |
| Backend uses BGProductDescription | Yes |
| Report generates without errors | Yes |
| Column D shows product descriptions | Yes (not "ORD-xxxxx") |
| VBA macro runs correctly | Yes |
| Other BGSalesByItemView reports work | Yes |

---

## Files Modified

| File | Change |
|------|--------|
| BGSalesByItemView (Creatio) | Added BGProductDescription column |
| UsrExcelReportService.cs (line ~1836) | Changed BGNumber → BGProductDescription |

---

*Created: 2026-01-29*
