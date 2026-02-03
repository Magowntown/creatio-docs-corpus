# v19 Deployment Guide

**Date:** 2026-01-23
**Handler:** `UsrPage_ebkv9e8` (v19 Looker Fix)
**Package:** BGApp_eykaguu
**Status:** ✅ **READY FOR DEPLOYMENT** (Pre-deployment checks complete)

---

## Pre-Deployment Checklist ✅

| Check | Status | Notes |
|-------|--------|-------|
| Business rule conflict | ✅ CLEAR | No duplicate in Custom package |
| Package audit | ✅ DONE | 13 packages scanned |
| Schema inheritance | ✅ VERIFIED | BGApp extends BGlobalLookerStudio |
| v19 file ready | ✅ READY | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19_LookerFix.js` |

**Investigation Summary:**
- Investigated `BGUsrPage_ebkv9e8BusinessRule` duplicate concern
- **Result:** Duplicate DOES NOT EXIST in PROD
- Only one business rule exists (in BGApp_eykaguu, same as handler)
- Custom package contains NO schemas
- **Conclusion:** Safe to deploy v19

---

## Summary of Changes

### v19 Fixes (from v18)

1. **Looker reports now SHOW Date+Status filters** (was incorrectly hidden in v18)
2. **Looker reports now BUILD URL params from filters** (was just opening base URL)

### Visibility Logic

| Report Type | Commission Filters | Date+Status Filters | Action |
|-------------|-------------------|---------------------|--------|
| None selected | Hidden | Hidden | - |
| Commission | **VISIBLE** | Hidden | Excel download |
| Non-Commission Excel | Hidden | **VISIBLE** | Excel download |
| Looker Studio | Hidden | **VISIBLE** ✓ | New tab + URL params |

---

## Deployment Steps

### Step 1: Open DEV Schema Designer

```
https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734
```

### Step 2: Replace Schema Code

Replace the entire content with the code from:
```
/home/magown/creatio-report-fix/client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19_LookerFix.js
```

### Step 3: Save and Compile

1. Click "Save" button
2. Wait for compilation to complete
3. Hard refresh browser (`Ctrl+Shift+R`)

### Step 4: Verify Deployment

1. Open browser console (F12)
2. Navigate to Reports page
3. Select "Sales by Sales Group" (Looker report)
4. Verify console shows: `[v19] Report: Sales by Sales Group | Type: LOOKER | Showing date+status filters`
5. Verify Date/Status filter fields are VISIBLE
6. Click "Generate Report"
7. Verify new tab opens with URL params (e.g., `?params=%7B"ds0.additionalFilters":"..."%7D`)

---

## Testing Checklist

### Commission Reports
- [ ] Commission report shows Year-Month and Sales Group filters
- [ ] Commission filters work correctly
- [ ] Commission Excel downloads successfully
- [ ] Console shows `[v19] ... Type: COMMISSION`

### Looker Studio Reports
- [ ] Sales by Sales Group shows Date+Status filters (NOT Commission filters)
- [ ] Sales by Sales Rep shows Date+Status filters
- [ ] Sales by Customer shows Date+Status filters
- [ ] Report opens in new tab
- [ ] URL contains params: `?params=%7B"ds0.additionalFilters":"..."%7D`
- [ ] Console shows `[v19] ... Type: LOOKER | Showing date+status filters`

### Other Excel Reports
- [ ] "Items by Customer" shows Date+Status filters
- [ ] "Customers did not buy" shows Date+Status filters
- [ ] Excel downloads work correctly
- [ ] Console shows `[v19] ... Type: EXCEL`

---

## Rollback

If issues occur, restore v18 from:
```
/home/magown/creatio-report-fix/client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v18_AttrBinding.js
```

---

## Key Code Locations

### Visibility Logic (lines 426-444)
```javascript
if (isCommissionReport) {
    request.$context.UsrShowCommissionFilters = true;
    request.$context.UsrShowDateStatusFilters = false;
} else if (isLookerReport) {
    // v19 FIX: Show date+status for Looker
    request.$context.UsrShowCommissionFilters = false;
    request.$context.UsrShowDateStatusFilters = true;
} else {
    // Non-Commission Excel
    request.$context.UsrShowCommissionFilters = false;
    request.$context.UsrShowDateStatusFilters = true;
}
```

### URL Params Building (lines 493-502)
```javascript
if (reportUrl && reportUrl.length > 0) {
    // v19 FIX: Build URL params from date/status filters
    var params = buildLookerParams(context);
    var fullUrl = reportUrl + params;
    console.log("[v19] Opening Looker Studio with params:", fullUrl);
    window.open(fullUrl, "_blank");
    ...
}
```

### buildLookerParams Function (lines 43-105)
Builds URL params for Looker from:
- Created date range (CreatedFrom/CreatedTo)
- Shipping date range (ShippingFrom/ShippingTo)
- Delivery date range (DeliveryFrom/DeliveryTo)
- Status filter (LookupAttribute_tytkx09)

---

## After DEV Testing

### Deploy to PROD

1. Open PROD Schema Designer:
   ```
   https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
   ```

2. Replace content with v19 code

3. Save and compile

4. Verify with console logs

---

*End of Deployment Guide*
