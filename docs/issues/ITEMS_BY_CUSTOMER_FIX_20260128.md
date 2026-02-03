# Items by Customer Report Fix

**Date:** 2026-01-28
**Issue:** RPT-004 - "Items by Customer" Row out of range / generation fails
**Status:** ✅ **PROD WORKING** | ⚠️ DEV needs backend code update

---

## Current Status

| Environment | IntEntitySchemaNameId | Backend Code | Status |
|-------------|----------------------|--------------|--------|
| **PROD** | ✅ BGSalesByItemView | ✅ v2 fix (2026-01-28) | ✅ **WORKING** |
| **DEV** | ✅ BGSalesByItemView | ❌ Old (2026-01-20) | ⚠️ Backend update needed |

**PROD Test Result:**
```
success: True
message: Items by Customer: 832 rows for FAB
```

---

## Root Cause Analysis

Two issues were discovered:

### Issue 1: IntExcelReport Misconfiguration
| Aspect | Before | After |
|--------|--------|-------|
| IntEntitySchemaNameId | `01547449...` (BGItemsByCustomerView) | `5f969641...` (BGSalesByItemView) |
| Row Count | 0 (empty view) | 4,802,572 |
| Status | ✅ **FIXED in PROD & DEV** | |

`BGItemsByCustomerView` was an execution-based view (like Commission) that was never populated.
`BGSalesByItemView` contains the actual sales data with customer names.

### Issue 2: Backend Code Resolution Order
| Aspect | Description |
|--------|-------------|
| Function | `GetReportEntitySchemaName()` |
| Problem | GUID resolution returns schema name from `IntEntitySchemaNameId`, which was wrong |
| Effect | Returned "BGItemsByCustomerView" → custom generator condition never triggered |
| Status | ✅ **PROD DEPLOYED** | ⚠️ DEV needs update |

**Key Fix:** Updated `IntEntitySchemaNameId` to point to `BGSalesByItemView` so the GUID resolution returns the correct schema name.

---

## Deployment Checklist

### Step 1: Backend Code Update ⚠️ REQUIRED

**Creatio URL:**
```
https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

**Local File:** `source-code/UsrExcelReportService_Updated.cs`

**Changes to `GetReportEntitySchemaName` function (around line 237):**

**v2 Fix** - Three fallback approaches:

1. **Column Reference** (lines 270-278): Uses ESQ column reference for correct alias
2. **GUID Resolution** (lines 311-333): Queries SysSchema directly using `IntEntitySchemaNameId`
3. **IntEsq Parsing** (lines 335+): Falls back to parsing JSON (original method)

Key additions:
```csharp
// Line 251: Add lookup ID for GUID resolution
esq.AddColumn("IntEntitySchemaNameId");

// Lines 311-333: GUID-based SysSchema lookup
var schemaId = entity.GetTypedColumnValue<Guid>("IntEntitySchemaNameId");
if (schemaId != Guid.Empty)
{
    var schemaEsq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "SysSchema");
    schemaEsq.AddColumn("Name");
    var schemaEntity = schemaEsq.GetEntity(userConnection, schemaId);
    if (schemaEntity != null)
    {
        return schemaEntity.GetTypedColumnValue<string>("Name");
    }
}
```

**Full function replacement:** See `source-code/UsrExcelReportService_Updated.cs` lines 237-350

### Step 2: Verify IntExcelReport Configuration ✅ DONE

Already fixed via OData PATCH:
- IntExcelReport ID: `d213933b-093d-47fc-8da8-422c0d9bf715`
- IntEntitySchemaName: `BGSalesByItemView` (ID: `5f969641-af66-48bd-9fca-b532f479684f`)

### Step 3: Test After Deployment

Run the test script:
```bash
source .env && python3 scripts/testing/test_items_by_customer.py
```

**Expected Results:**
- Generate call should return `success: true`
- Message should show row count: `Items by Customer: X rows for {CustomerName}`
- Excel file should download successfully

### Step 4: Browser Verification

1. Go to DEV Reports page
2. Select "Items by Customer" report
3. Verify filters appear:
   - Date filters (Created From/To, Shipping From/To, Delivery From/To)
   - Status filter
   - Customer filter
4. Select a customer with data
5. Click Generate
6. Excel should download with filtered data

---

## Technical Details

### Data Flow

```
Frontend (v19.16)              Backend (UsrExcelReportService)
─────────────────              ────────────────────────────────
Select "Items by Customer"
  ↓
Show Date+Status+Customer
filters
  ↓
User selects customer
  ↓
Click Generate
  ↓
POST /Generate                 → GetReportEntitySchemaName()
  CustomerName: "Acme Inc"       ↓
                               Returns "BGSalesByItemView"
                                 ↓
                               if (entitySchemaName == "BGSalesByItemView"
                                   && !string.IsNullOrEmpty(CustomerName))
                                 ↓
                               GenerateSalesByItemWithFilters()
                                 ↓
                               QuerySalesByItemData() with filters
                                 ↓
                               Return Excel bytes
  ↓
Download Excel via iframe
```

### Why Custom Generator is Required

The `IntExcelExport` library has issues:
1. Doesn't properly apply `FiltersConfig` to ESQ for some views
2. `BGSalesByItemView` has 4.5M rows - unfiltered query exceeds Excel row limit (1M)
3. Without customer filter, report would fail with "Row out of range"

The custom generator `GenerateSalesByItemWithFilters()` builds ESQ directly with proper filters.

---

## Files Modified

| File | Change | Status |
|------|--------|--------|
| `source-code/UsrExcelReportService_Updated.cs` | Fixed lookup resolution in GetReportEntitySchemaName | ⚠️ Deploy |
| IntExcelReport (d213933b-...) | Changed IntEntitySchemaName to BGSalesByItemView | ✅ Done |
| `scripts/testing/test_items_by_customer.py` | New test script | ✅ Created |

---

## Rollback Plan

If issues occur after deployment:

1. **Backend rollback:** Restore previous `GetReportEntitySchemaName` function
2. **IntExcelReport rollback:** Change IntEntitySchemaNameId back to `01547449-50b0-4328-b51f-c742bdd3cccd` (BGItemsByCustomerView)

---

## Related Issues

- **RPT-004:** "Items by Customer" Row out of range → **This fix**
- **UI-003:** Customer filter missing for "Items by Customer" → Fixed in v19.13
- **v19.16:** Date filters for "Items by Customer" → Ready for deployment

---

*Created: 2026-01-28*
