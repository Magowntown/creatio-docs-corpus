# v19 Pre-Deployment Verification

**Created:** 2026-01-23
**Purpose:** Prevent repeating past mistakes before deploying v19

---

## Past Mistakes Analysis

| Version | Mistake | How v19 Addresses It |
|---------|---------|---------------------|
| v15 | Iframe blocked by X-Frame-Options | Uses `window.open()` in new tab |
| v16 | DOM selectors couldn't find elements | Uses attribute binding (not DOM manipulation) |
| v17 | Schema `visible:false` prevented elements from rendering | Uses `visible: "$Attribute"` binding |
| v18 | Looker filters incorrectly hidden | Changed: `UsrShowDateStatusFilters = true` for Looker |
| v18 | Looker URL didn't include filter params | Added `buildLookerParams()` function |

---

## Code Review Checklist

### 1. Visibility Logic (Lines 426-444)

```javascript
// v19 ORDER: Commission FIRST, then Looker
if (isCommissionReport) {
    request.$context.UsrShowCommissionFilters = true;
    request.$context.UsrShowDateStatusFilters = false;
} else if (isLookerReport) {
    request.$context.UsrShowCommissionFilters = false;
    request.$context.UsrShowDateStatusFilters = true;   // <-- v19 FIX
} else {
    request.$context.UsrShowCommissionFilters = false;
    request.$context.UsrShowDateStatusFilters = true;
}
```

**Verification:**
- [x] Commission reports still show commission filters (Year-Month, Sales Group)
- [x] Looker reports now show date+status filters (v19 fix)
- [x] Non-Commission Excel reports show date+status filters
- [x] No report is both Commission AND has Looker URL (confirmed in PROD data)

### 2. URL Params Building (Lines 43-105)

```javascript
function buildLookerParams(context) {
    var attrs = context.attributes || {};
    // Accesses: attrs.CreatedFrom, attrs.ShippingFrom, etc.
    // Also: attrs.LookupAttribute_tytkx09
}
```

**Bugs Found & Fixed (2026-01-23):**

| Bug | Original Code | Fixed Code |
|-----|---------------|------------|
| Attribute access pattern | `context.CreatedFrom` | `context.attributes.CreatedFrom` |
| Shipping field name | `BGShippingDate` | `BGShipDate` |

**v19.1 Additional Fixes (from DEV testing):**

| Bug | Symptom | Fix |
|-----|---------|-----|
| Missing `selectedReport.value` check | `Cannot read properties of null (reading 'value')` | Added `&& selectedReport.value` to condition |
| Missing `meta` null check | `Cannot read properties of undefined (reading 'UsrURL')` | Added `if (meta && typeof meta.UsrURL !== 'undefined')` |
| Missing `reportMeta` null check | Potential null reference in generate | Added `if (reportMeta)` guard |

**Root Cause:** Parent schema (BGlobalLookerStudio) uses `request.$context.attributes.X` pattern, not `context.X`.

**Fix Applied:**
```javascript
var attrs = context.attributes || {};
if (attrs.CreatedFrom) { ... }  // Was: context.CreatedFrom
filters.push('BGShipDate ge ...');  // Was: BGShippingDate
```

### 3. Date Formatting (Lines 32-41)

```javascript
function formatDateForLooker(dateValue) {
    var d = new Date(dateValue);
    if (isNaN(d.getTime())) return null;  // Safe null check
    ...
}
```

**Mitigation:** Returns `null` for invalid dates, filters skip null values.

---

## Condition Order Change Analysis

**v18 Order:** Looker first → Commission
**v19 Order:** Commission first → Looker

**Impact Analysis:**

| Report Name | Has Commission in Name? | Has Looker URL? | v18 Treatment | v19 Treatment |
|-------------|------------------------|-----------------|---------------|---------------|
| Commission | YES | NO | COMMISSION | COMMISSION |
| Sales by Sales Group | NO | YES | LOOKER | LOOKER |
| Sales by Customer | NO | YES | LOOKER | LOOKER |
| Items by Customer | NO | NO | EXCEL | EXCEL |

**Result:** No behavioral difference for existing reports. Order change is safe.

---

## Console Verification Points

After deploying v19, verify these console messages:

### 1. Page Init
```
[v19] Page init - visibility controlled by attribute binding
[v19] UsrShowCommissionFilters: false
[v19] UsrShowDateStatusFilters: false
```

### 2. Commission Report Selection
```
[v19] Report: Commission | Type: COMMISSION | Showing commission filters
```
- Verify: Commission filters visible, Date+Status hidden

### 3. Looker Report Selection
```
[v19] Report: Sales by Sales Group | Type: LOOKER | Showing date+status filters
```
- Verify: Date+Status filters visible, Commission hidden

### 4. Looker Generate with Params
```
[v19] Opening Looker Studio with params: https://lookerstudio.google.com/...?params=%7B"ds0.additionalFilters":"..."...
```
- Verify: URL contains `?params=` with encoded filter values

### 5. Excel Report Selection
```
[v19] Report: Items by Customer | Type: EXCEL | Showing date+status filters
```
- Verify: Date+Status filters visible

---

## Attribute Binding Verification

**Parent Schema Container Names** (from BGlobalLookerStudio):

| Element | Container Name | Bound to Attribute |
|---------|---------------|-------------------|
| Date Filters | `GridContainer_xdy25v1` | `$UsrShowDateStatusFilters` |
| Status Filter | `GridContainer_knkow5v` | `$UsrShowDateStatusFilters` |
| Commission Warning | `BGWarningLabel` | `$UsrShowCommissionFilters` |
| Commission Filters | `BGCommissionFiltersContainer` | `$UsrShowCommissionFilters` |

**Required:** These container names must exist in parent schema.

---

## Deployment Sequence

### Step 1: DEV Verification
1. Deploy v19 to DEV
2. Hard refresh (`Ctrl+Shift+R`)
3. Open console (F12)
4. Test each scenario above
5. Capture screenshots/console logs

### Step 2: PROD Deployment (only after DEV passes)
1. Deploy v19 to PROD
2. Same verification steps

### Step 3: Rollback Plan
If issues occur:
- Restore v18 from: `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v18_AttrBinding.js`
- v18 is known working (deployed and tested)

---

## Test Matrix

| Report | Expected Filters | Expected Action | Test Result |
|--------|-----------------|-----------------|-------------|
| Commission | Commission (Year-Month, Sales Group) | Excel download | [ ] |
| Sales by Sales Group | Date+Status | New tab + URL params | [ ] |
| Sales by Sales Rep | Date+Status | New tab + URL params | [ ] |
| Sales by Customer | Date+Status | New tab + URL params | [ ] |
| Items by Customer | Date+Status | Excel download | [ ] |
| Customers did not buy | Date+Status | Excel download | [ ] |

---

## Final Sign-Off

- [ ] Code review completed
- [ ] No regression in Commission reports
- [ ] No regression in Excel reports
- [ ] Looker filters now visible
- [ ] Looker URL params working
- [ ] Rollback plan confirmed

---

*Document created: 2026-01-23*
