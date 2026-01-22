# UI-002: PROD Investigation Results

**Date:** 2026-01-22
**Status:** Root cause identified from actual PROD site inspection

---

## Summary

Investigated the actual PROD Creatio site via browser automation and API queries. The `$UsrShowCommissionFilters` attribute binding is **NOT WORKING** as expected.

---

## Key Findings from PROD Site

### 1. Schema Versions in PROD

| Schema | Package | Modified | Notes |
|--------|---------|----------|-------|
| `UsrPage_ebkv9e8` | BGApp_eykaguu | **2026-01-22 10:45** | Most recent (modified today) |
| `UsrPage_ebkv9e8` | BGlobalLookerStudio | 2026-01-20 11:29 | Parent schema |
| `BGUsrPage_ebkv9e8BusinessRule` | **Custom** | **2026-01-20 10:16** | NEW - Created 2 days ago |
| `BGUsrPage_ebkv9e8BusinessRule` | BGApp_eykaguu | 2025-07-14 | Original business rule |

### 2. Observed Page Behavior (Browser Automation)

**Before selecting any report:**
- Warning label "Date and transaction info derived from QuickBooks synced data." is **VISIBLE** ❌
  - Should be hidden until Commission report is selected
- All date filters visible ✅
- Status Order dropdown visible ✅

**After selecting "Commission" report:**
- Console logs: `[UsrPage_ebkv9e8] Report selected: Commission | Commission filters: VISIBLE`
- Warning label still visible ✅ (correct)
- Year-Month dropdown: **NOT VISIBLE** ❌
- Sales Group dropdown: **NOT VISIBLE** ❌

### 3. Identified Problems

1. **BGWarningLabel** - Always visible, ignoring `"visible": "$UsrShowCommissionFilters"` binding
2. **GridContainer_3asa01r** (Commission filters) - Never renders, even when `UsrShowCommissionFilters = true`
3. **New Business Rule** - `BGUsrPage_ebkv9e8BusinessRule` in Custom package created 2026-01-20 may be interfering

---

## Root Cause Analysis

### The Attribute Binding Issue

The handlers correctly set `request.$context.UsrShowCommissionFilters = isCommissionReport`, as evidenced by console logs. However, the UI elements are NOT responding to this attribute change.

**Possible causes:**

1. **Attribute not declared correctly** - Freedom UI requires attributes to be declared as empty objects `{}` in viewModelConfig, but our code has:
   ```javascript
   "UsrShowCommissionFilters": {
       "value": false  // This might be causing issues
   }
   ```

   Creatio documentation shows:
   ```javascript
   "UsrShowCommissionFilters": {}  // Empty object, no default value
   ```

2. **Business rule override** - The new `BGUsrPage_ebkv9e8BusinessRule` in Custom package (created 2026-01-20) may be setting visibility rules that conflict with our handler logic.

3. **GridContainer not inserted** - The Commission filter container might not be in the DOM at all, meaning the insert operation may have failed silently.

---

## Recommended Fix

### Option A: Fix Attribute Declaration (Recommended)

Update the viewModelConfigDiff to declare the attribute correctly:

```javascript
viewModelConfigDiff: [
    {
        "operation": "merge",
        "path": ["attributes"],
        "values": {
            "UsrShowCommissionFilters": {},  // Empty object - no default value
            // ... other attributes
        }
    }
]
```

And set the initial value in the handler:

```javascript
{
    request: "crt.HandleViewModelInitRequest",
    handler: async (request, next) => {
        request.$context.UsrShowCommissionFilters = false;  // Set here instead
        return next?.handle(request);
    }
}
```

### Option B: Remove/Check Custom Business Rule

The `BGUsrPage_ebkv9e8BusinessRule` in Custom package should be investigated:
- Check what rules it defines
- Remove it if it conflicts with handler logic

**PROD Location:**
```
Configuration → Advanced Settings → Schema: BGUsrPage_ebkv9e8BusinessRule
Package: Custom
UId: e42d1bec-59a1-46d1-968b-8efd41a0afe6
```

### Option C: Use v8 Direct Visibility Approach

Our v8 handler already attempts this - set `visible: false` in viewConfigDiff and use SDK to dynamically change visibility:

```javascript
// In viewConfigDiff - start hidden
{
    "operation": "insert",
    "name": "GridContainer_3asa01r",
    "values": {
        "visible": false,  // Start hidden, not bound
        // ...
    }
}

// In handler - use SDK to set visibility
await handlerChain.process({
    type: "crt.SetAttributeValueRequest",
    $context: request.$context,
    attributeName: "GridContainer_3asa01r_visible",
    value: isCommissionReport
});
```

---

## Investigation Scripts

### Check Business Rule in Custom Package

Need to access:
- **PROD URL:** `https://pampabay.creatio.com/0/ClientApp/#/AdvancedSettings`
- Navigate to: Packages → Custom → BGUsrPage_ebkv9e8BusinessRule

### Verify Handler Deployment

The handler was modified **TODAY (2026-01-22 10:45)** - need to verify what code is actually deployed.

---

## Action Items

1. [ ] Check BGUsrPage_ebkv9e8BusinessRule content in Custom package via PROD Configuration UI
2. [ ] Remove Custom business rule if it conflicts
3. [ ] Deploy v9 handler with corrected attribute declaration
4. [ ] Test in PROD after deployment

---

## Files Reference

| Version | File | Status |
|---------|------|--------|
| v6 | `BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v6_Fixed.js` | Deployed (broken) |
| v7 | `BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v7_Init.js` | Has init handler |
| v8 | `BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v8_Direct.js` | Direct visibility |
| v9 | `BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v9_AttrFix.js` | **READY** - Fixed attribute declaration |
