# UI-002 Fix: v12 DEV-Style Deployment

**Issue:** Visibility bindings not working on parent elements in PROD
**Fix:** Deploy v12 handler that follows DEV's proven pattern
**Date:** 2026-01-22

---

## Root Cause (Confirmed)

**Freedom UI Limitation:** `$Attribute` visibility bindings only work when BOTH the attribute AND the UI element are declared in the **same schema**.

Previous attempts tried to use `visible: "$UsrShowDateFilters"` on parent elements, but the attribute was declared in the child schema's `viewModelConfigDiff`. This doesn't work across schema inheritance boundaries.

---

## Solution: Follow DEV's Pattern

DEV's working IWQBIntegration schema uses this approach:

1. **Hide parent elements** with hard-coded `visible: false` (no dynamic binding)
2. **Remove unwanted elements** with `operation: "remove"`
3. **Insert NEW elements** in child schema with `visible: "$Attribute"` bindings
4. Declare the attribute in the **same child schema**

---

## What v12 Does

### Parent Element Modifications (Hard-coded, no bindings)

| Element | Action |
|---------|--------|
| `GridContainer_oshnwh8` | `visible: false` |
| `CreatedFrom`, `CreatedTo` | `visible: false` |
| `ShippingFrom`, `ShippingTo` | `visible: false` |
| `DeliveryFrom`, `DeliveryTo` | `visible: false` |
| `GridContainer_knkow5v` | `remove` |
| `GridContainer_fh039aq` (iframe) | `visible: false` |

### New Elements (Inserted with bindings)

| Element | Purpose | Visibility |
|---------|---------|------------|
| `BGReportContainer` | Report selector container | Always visible |
| `BGPampaReport` | Report dropdown | Always visible |
| `BGWarningLabel` | Commission warning | `$UsrShowCommissionFilters` |
| `BGCommissionFiltersContainer` | Filter container | `$UsrShowCommissionFilters` |
| `BGYearMonth` | Year-Month filter | Always visible (parent hidden) |
| `BGSalesGroup` | Sales Group filter | Always visible (parent hidden) |

---

## Deployment Steps

### Step 1: Open PROD Schema Designer

```
https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
```

This is the **BGApp_eykaguu** child schema.

### Step 2: Backup Current Code

1. Copy all existing code
2. Save to: `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_BACKUP.js`

### Step 3: Deploy v12 Handler

1. Select all code in the designer
2. Paste contents of: `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v12_DEVStyle.js`
3. Click **Save**
4. Click **Publish** (if available)

### Step 4: Clear Browser Cache

```
Ctrl+Shift+R (hard refresh)
```

Or: DevTools → Network → "Disable cache" → Refresh

### Step 5: Test

#### Test A: No Report Selected
- Expected: Report dropdown visible, Commission filters HIDDEN

#### Test B: Select "Commission"
- Console should show: `[v12] Report: Commission | Commission: true`
- Expected: Warning label VISIBLE, Year-Month VISIBLE, Sales Group VISIBLE

#### Test C: Select "Sales By Line" (non-Commission)
- Console should show: `[v12] Report: Sales By Line | Commission: false`
- Expected: Warning label HIDDEN, Commission filters HIDDEN

#### Test D: Generate Commission Report
- Select Year-Month and Sales Group
- Click Generate Report
- Expected: Excel downloads successfully

#### Test E: Generate Looker Studio Report
- Select "Sales By Customer" or another Looker report
- Click Generate Report
- Expected: Opens in new tab (may require Google permissions)

---

## Behavior After Fix

| Report Type | Report Dropdown | Date Filters | Status | Commission Filters |
|-------------|-----------------|--------------|--------|-------------------|
| None selected | Visible | Hidden | Hidden | Hidden |
| Commission | Visible | Hidden | Hidden | **Visible** |
| IW_Commission | Visible | Hidden | Hidden | **Visible** |
| All others | Visible | Hidden | Hidden | Hidden |

**Note:** Date filters are permanently hidden because:
1. Looker Studio reports have their own date filters
2. Excel reports don't use date filters
3. Simplifies the UI

---

## Rollback

If issues occur:

1. Open schema designer (same URL)
2. Paste backup code
3. Save and publish
4. Hard refresh browser

---

## File Reference

| File | Purpose |
|------|---------|
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v12_DEVStyle.js` | **Deploy this** |
| `/tmp/IWQBIntegration_UsrPage_ebkv9e8_DEV.js` | DEV reference (proof it works) |

---

## Technical Details

### Why This Works

```
Child Schema (BGApp_eykaguu):
  - Declares: UsrShowCommissionFilters = { "value": false }
  - Inserts: BGWarningLabel with visible: "$UsrShowCommissionFilters"
  - Inserts: BGCommissionFiltersContainer with visible: "$UsrShowCommissionFilters"

Handler:
  - Sets: request.$context.UsrShowCommissionFilters = isCommissionReport

Result:
  - Attribute and elements in SAME schema = binding works
```

### Why Previous Attempts Failed

```
Child Schema:
  - Declares: UsrShowDateFilters (in child)
  - Merges: GridContainer_xdy25v1 with visible: "$UsrShowDateFilters" (element is in PARENT)

Result:
  - Attribute in child, element in parent = binding resolution fails
```

---

*Created: 2026-01-22*
