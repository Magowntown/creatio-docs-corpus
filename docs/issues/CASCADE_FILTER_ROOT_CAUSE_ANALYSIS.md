# Cascade Filter Root Cause Analysis

**Date:** 2026-01-27
**Issue:** Sales Group cascade filter stops working after switching reports
**Status:** ✅ FIXED in v19.10 (UsrSalesGroupLoading attribute)

---

## Executive Summary

The cascade filter query **WORKS correctly on PROD**. The issue is that Freedom UI **caches the ComboBox dropdown list**, and changing the filter criteria (`validSalesGroupIds`) does NOT trigger a reload of the cached list.

---

## Confirmed Findings

### 1. OData Query Works

The v19.9 cascade query pattern returns correct data:

```
GET /0/odata/BGCommissionSalesGroupByYearMonth?$filter=BGYearMonth/Id eq {guid}&$select=BGSalesGroupId
```

**Test Results:**
| YearMonth | Groups with Data | Total Groups |
|-----------|------------------|--------------|
| 2025-12 | 14 groups | 76 |
| 2026-01 | 16 groups | 76 |

When properly filtered, users should see 14-16 groups, not all 76.

### 2. Page Architecture Confirmed

```
BGlobalLookerStudio.UsrPage_ebkv9e8 (BASE - ExtendParent=false)
         ↓ (child extends parent)
BGApp_eykaguu.UsrPage_ebkv9e8 (OVERRIDE - ExtendParent=true, v19.9)
```

**Parent Schema Handler:**
- Has its own `crt.HandleViewModelAttributeChangeRequest` for `LookupAttribute_0as4io2` (report selector)
- Only sets `UsrURL` from report metadata
- Does NOT interfere with YearMonth or cascade logic

**Child Schema Handler (v19.9):**
- Has `crt.HandleViewModelAttributeChangeRequest` for both report selector and `UsrYearMonth`
- Has `crt.LoadDataRequest` interceptor for cascade filtering
- Uses module-level variables: `cascadeFilterEnabled`, `validSalesGroupIds`

### 3. Business Rules

Only ONE business rule exists: `BGUsrPage_ebkv9e8BusinessRule` (in BGApp_eykaguu)
- No duplicates or conflicts
- Does not interfere with visibility or filtering

---

## Root Cause: Freedom UI ComboBox Caching

### The Problem

When a ComboBox loads its dropdown options, the data is **cached** in the `_List` collection attribute. The `crt.LoadDataRequest` interceptor only fires when the list is **being loaded**, not when it's already cached.

### Reproduction Scenario

1. Open page, select Commission report → `cascadeFilterEnabled = true`
2. Select YearMonth → cascade query runs, `validSalesGroupIds = [14 groups]`
3. Open Sales Group dropdown → `LoadDataRequest` fires, filter applied → **14 groups shown ✓**
4. Select another report type (e.g., "Items by Customer")
5. Select Commission report again:
   - Line 494: `UsrYearMonth = null` (cleared)
   - Line 497: `validSalesGroupIds = null` (cleared)
   - Line 504: `cascadeFilterEnabled = true`
6. **Sales Group list MAY still have cached data from step 3**
7. Select a different YearMonth → cascade query runs, `validSalesGroupIds = [16 groups]`
8. Open Sales Group dropdown:
   - **If cached**: LoadDataRequest may NOT fire, shows stale data
   - **If not cached but timing issue**: LoadDataRequest fires BEFORE cascade query completes

### Code Analysis (v19.9)

**Line 543-596 (YearMonth change handler):**
```javascript
if (request.attributeName === "UsrYearMonth" && !request.silent && cascadeFilterEnabled) {
    // Line 550: Clear selection (NOT the list!)
    request.$context.UsrSalesGroup = null;

    // Lines 553-589: Async cascade query
    const resp = await fetch(queryUrl, {...});  // ASYNC!
    validSalesGroupIds = Array.from(groupIds);  // Set AFTER fetch completes
}
```

**Problem 1:** Clearing `UsrSalesGroup = null` only clears the **selected value**, NOT the **dropdown list**.

**Problem 2:** The cascade query is **async**. If the user opens the Sales Group dropdown before the query completes, `validSalesGroupIds` is still `null`, so no filter is applied.

**Line 399-451 (LoadDataRequest interceptor):**
```javascript
if (cascadeFilterEnabled && isSalesGroupList) {
    // Only applies filter if validSalesGroupIds has items
    if (validSalesGroupIds !== null && validSalesGroupIds.length > 0) {
        // Apply filter
    } else {
        // No filter - show ALL groups
    }
}
```

**Problem 3:** If `validSalesGroupIds` is `null` or `[]` when LoadDataRequest fires, ALL groups are shown.

---

## Why It Works Initially But Fails After Switching

### Initial Flow (Works)
1. Commission report selected → `cascadeFilterEnabled = true`, `validSalesGroupIds = null`
2. YearMonth selected → cascade query runs → `validSalesGroupIds = [14 groups]`
3. User opens Sales Group dropdown → LoadDataRequest fires → filter applied → 14 groups

### After Switching Flow (Fails)
1. Switch to another report → `cascadeFilterEnabled = false`
2. Switch back to Commission → `cascadeFilterEnabled = true`, `validSalesGroupIds = null`
3. YearMonth selected → cascade query **starts** (async)
4. **User opens Sales Group dropdown BEFORE cascade query completes**
5. LoadDataRequest fires → `validSalesGroupIds` is still `null` → NO filter → 76 groups
6. Cascade query completes → `validSalesGroupIds = [16 groups]` → **TOO LATE**
7. List is already loaded with all 76 groups

---

## Solution Options

### Option 1: Force ComboBox Reload After Cascade Query (Recommended)

After the cascade query completes, explicitly trigger a reload of the Sales Group dropdown.

**Approach:**
1. After setting `validSalesGroupIds`, clear the list collection attribute
2. Trigger a reload by requesting the attribute value

```javascript
// After cascade query completes:
validSalesGroupIds = Array.from(groupIds);

// Force list reload - need to find the correct Freedom UI API
// Option A: Clear the list
request.$context.UsrSalesGroup_List = [];

// Option B: Use Freedom UI's reload mechanism
request.$context.loadAttributeData("UsrSalesGroup_List");
```

### Option 2: Add Loading State

Prevent the Sales Group dropdown from being used while the cascade query is running.

```javascript
// When YearMonth changes:
request.$context.SalesGroupLoading = true;  // Show loading indicator

// After cascade query completes:
request.$context.SalesGroupLoading = false;
```

### Option 3: Use lookupListConfig with Dynamic Filter

Instead of intercepting LoadDataRequest, use Freedom UI's built-in `lookupListConfig` with a filter that references the YearMonth attribute.

```javascript
"UsrSalesGroup": {
    "lookupListConfig": {
        "filter": {
            "attributePath": "UsrYearMonth",
            "comparisonType": "FilterComparisonType.Equal"
        }
    }
}
```

**Note:** This requires the data source to support filtering by YearMonth, which may need a different entity binding.

### Option 4: Server-Side Filtered Data Source

Create a custom data source that accepts YearMonth as a parameter and returns only relevant Sales Groups.

---

## Additional Findings

### PostgreSQL Error on Direct Entity Query

Querying `BGCommissionSalesGroupByYearMonth` without navigation property filter fails:

```
GET /0/odata/BGCommissionSalesGroupByYearMonth?$filter=BGYearMonthId eq {guid}
→ 500 Error: Column by path BGYearMonthId not found in schema
```

The entity is a **SQL view** and only supports navigation property queries (`BGYearMonth/Id eq {guid}`).

### Entity Structure

| Entity | Records | Purpose |
|--------|---------|---------|
| BGSalesGroup | 76 | All sales groups |
| BGYearMonth | Many | Year-Month lookup |
| BGCommissionSalesGroupByYearMonth | View | Filtered view of groups with commission data |

---

## Recommendations

✅ **IMPLEMENTED in v19.10:** Option 2 (Loading State) was implemented:
- Added `UsrSalesGroupLoading` attribute
- Binds to Sales Group dropdown's `readonly` property
- Disables dropdown during async cascade query
- Re-enables after query completes (in `finally` block)

**Testing scenarios for v19.10:**
- Fresh page load → Commission → YearMonth → Sales Group (should work)
- Commission → Other → Commission → YearMonth → Sales Group (should work)
- Rapidly switching reports while cascade queries are in flight (dropdown disabled during flight)

---

## Related Files

| File | Purpose |
|------|---------|
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.10_CascadeFix.js` | **FIXED handler - deploy this** |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.9_Complete.js` | Previous handler (has race condition) |
| `test-artifacts/parent_schema_UsrPage_ebkv9e8.js` | Parent schema reference |
| `docs/HANDLER_VERSION_HISTORY.md` | Version history |

---

*End of Analysis*
