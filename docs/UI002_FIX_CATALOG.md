# UI-002: Reports Page Fix - Comprehensive Catalog

**Date:** 2026-01-22
**Status:** In Progress
**Priority:** HIGH

---

## 1. PROBLEM UNDERSTANDING

### What I See (From Screenshots)

**PROD State (pampabay.creatio.com):**
- Report dropdown: "Select a report..."
- Warning message (red): VISIBLE (should be HIDDEN until Commission selected)
- Year-Month filter: VISIBLE (should be HIDDEN until Commission selected)
- Sales Group filter: VISIBLE (should be HIDDEN until Commission selected)
- Created From/To: VISIBLE
- Shipping From/To: VISIBLE
- Delivery From/To: VISIBLE
- Status Order: VISIBLE
- **PROBLEM:** ALL filters visible simultaneously - no conditional visibility working

**DEV State (dev-pampabay.creatio.com):**
- Report dropdown visible
- Warning message visible (still showing before report selected - also broken)
- Year-Month and Sales Group visible
- Date filters (Created/Shipping/Delivery) HIDDEN
- Status Order HIDDEN
- **STATE:** Partially working but warning shows prematurely

### Root Causes Identified

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| **Visibility binding not working** | Attribute declared as `{ "value": false }` instead of `{}` | Freedom UI requires empty object for reactive binding |
| **Duplicate business rules** | Two `BGUsrPage_ebkv9e8BusinessRule` schemas (Custom + BGApp_eykaguu) | Custom package rule created 1/20/2026 may override |
| **Looker Studio iframe blocked** | CSP policy blocks external domains | Browser console shows X-Frame-Options error |
| **Warning always visible** | Initial state not set in `HandleViewModelInitRequest` | No init handler setting `UsrShowCommissionFilters = false` |

---

## 2. SCHEMA ARCHITECTURE

### Package Hierarchy

```
BGlobalLookerStudio (Parent Package)
    └── UsrPage_ebkv9e8 (Parent Schema)
            └── Contains: Date filters, Status Order, iframe container, Report button

BGApp_eykaguu (Child Package)
    └── UsrPage_ebkv9e8 (Child Schema - EXTENDS Parent)
            └── Adds: Commission filters, hybrid handler
    └── BGUsrPage_ebkv9e8BusinessRule (Original - 7/14/2025)
            └── Contains: Visibility business rules

Custom (Override Package)
    └── BGUsrPage_ebkv9e8BusinessRule (Newer - 1/20/2026)
            └── May be overriding visibility logic
```

### Element Inventory

| Element | Package | Purpose | Visibility Rule |
|---------|---------|---------|-----------------|
| `LookupAttribute_0as4io2` | Parent | Report selector | Always visible |
| `GridContainer_xdy25v1` | Parent | Date filters container | Hide for Commission |
| `GridContainer_knkow5v` | Parent | Status filter container | Hide for Commission |
| `GridContainer_fh039aq` | Parent | Looker iframe | Always hidden (CSP) |
| `Button_vae0g6x` | Parent | Report button | Always visible |
| `BGCommissionWarning` | Child | QB data warning | Show for Commission only |
| `GridContainer_CommissionFilters` | Child | Commission filters | Show for Commission only |
| `BGYearMonth` | Child | Year-Month combo | Show for Commission only |
| `BGSalesGroup` | Child | Sales Group combo | Show for Commission only |

---

## 3. REPORT INVENTORY (18 Total)

### Commission Reports (2) - Excel Only

| Report Name | Filters Needed | Template |
|-------------|---------------|----------|
| Commission | Year-Month, Sales Group | BGCommissionReportDataView |
| IW_Commission | Year-Month, Sales Group | IWCommissionReportDataView |

### Looker Studio Reports (12) - Open in New Tab

| Report Name | Has UsrURL | Filters |
|-------------|------------|---------|
| Sales By Customer | Yes | Status, Dates, Customer Type |
| Sales By Sales Group | Yes | Status, Dates, Sales Group |
| Sales By Customer Type | Yes | Status, Dates, Customer Type |
| Sales By Line | Yes | Status, Dates |
| Sales By Line With Ranking | Yes | Status, Dates |
| Sales Rep Monthly Report | Yes | Status, Dates, Sales Rep |
| Sales By Sales Rep | Yes | Status, Dates, Sales Rep |
| (+ 5 more similar) | Yes | Various |

### Other Excel Reports (4) - Download via Service

| Report Name | Filters Needed | Template |
|-------------|---------------|----------|
| Sales By Item | Date filters | BGSalesByItemView |
| Sales By Item By Type Of Customer | Date, Customer Type | BGSalesByItemView |
| Items by Customer | Date filters | BGSalesByItemView |
| Customers did not buy over period | Date filters | BGSalesByCustomerView |

---

## 4. EXPECTED BEHAVIOR

### State Machine

```
┌─────────────────────────────────────────────────────────────────┐
│ STATE 1: No Report Selected                                     │
├─────────────────────────────────────────────────────────────────┤
│ Report dropdown:        VISIBLE                                 │
│ Commission warning:     HIDDEN                                  │
│ Year-Month:            HIDDEN                                   │
│ Sales Group:           HIDDEN                                   │
│ Date filters:          VISIBLE (default)                        │
│ Status Order:          VISIBLE (default)                        │
│ Report button:         VISIBLE                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Commission      │ │ Looker Studio   │ │ Other Excel     │
│ Report Selected │ │ Report Selected │ │ Report Selected │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ Warning: SHOW   │ │ Warning: HIDE   │ │ Warning: HIDE   │
│ YearMonth: SHOW │ │ YearMonth: HIDE │ │ YearMonth: HIDE │
│ SalesGroup:SHOW │ │ SalesGroup:HIDE │ │ SalesGroup:HIDE │
│ Dates: HIDE     │ │ Dates: SHOW     │ │ Dates: SHOW     │
│ Status: HIDE    │ │ Status: SHOW    │ │ Status: SHOW    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
   Excel Download      New Tab Open       Excel Download
```

---

## 5. IMPLEMENTATION PLAN

### Task #3: Fix Visibility Business Rules

**Problem:** `$UsrShowCommissionFilters` binding not reactive

**Solution:**
```javascript
// WRONG (v4 Minimal current)
"UsrShowCommissionFilters": {
    "value": false  // This prevents reactive binding
}

// CORRECT (v9 approach)
"UsrShowCommissionFilters": {}  // Empty object enables reactive binding
```

**Plus add init handler:**
```javascript
{
    request: "crt.HandleViewModelInitRequest",
    handler: async (request, next) => {
        request.$context.UsrShowCommissionFilters = false;
        request.$context.UsrShowDateFilters = true;
        return next?.handle(request);
    }
}
```

### Task #4: Resolve Business Rule Conflict

**Investigation needed:**
1. Export content of `BGUsrPage_ebkv9e8BusinessRule` from Custom package
2. Compare with `BGUsrPage_ebkv9e8BusinessRule` from BGApp_eykaguu
3. Determine if Custom version overrides visibility
4. Recommend: Delete Custom version OR merge logic

**Access path:**
```
PROD → Configuration → Packages → Custom → BGUsrPage_ebkv9e8BusinessRule
UId: e42d1bec-59a1-46d1-968b-8efd41a0afe6
```

### Task #5: Configure CSP for Looker Studio

**Steps (from Creatio Academy):**
1. System Designer → Security → Content Security Policy
2. Enable "Log violations" mode first
3. Trusted sources tab → Add source
4. Source URL: `https://lookerstudio.google.com`
5. Associate directives: `child-src`, `frame-ancestors`
6. Save and test iframe embedding
7. If working, enable blocking mode

**Alternative (if CSP config unavailable):**
- Keep current approach: Open Looker Studio in new tab
- Requires users to have Google account access

### Task #6: Verify All 18 Reports

**Test matrix to complete:**

| # | Report | Type | Filters Work | Download/Open Works |
|---|--------|------|--------------|---------------------|
| 1 | Commission | Excel | [ ] | [ ] |
| 2 | IW_Commission | Excel | [ ] | [ ] |
| 3 | Sales By Customer | Looker | [ ] | [ ] |
| 4 | Sales By Sales Group | Looker | [ ] | [ ] |
| ... | ... | ... | ... | ... |

### Task #7: Create v10 Handler

**Merge these elements:**

| From | Element |
|------|---------|
| v4 Minimal | Non-destructive approach (no remove operations) |
| v9 AttrFix | Empty `{}` attribute declaration |
| v9 AttrFix | Init handler for default values |
| VisibilityFix_v2 | Toggle date filters with `$UsrShowDateFilters` |
| VisibilityFix_v2 | Use parent's report dropdown `LookupAttribute_0as4io2` |

---

## 6. FILES REFERENCE

### Handler Versions

| Version | File | Status | Notes |
|---------|------|--------|-------|
| v2 | `Hybrid_v2.js` | Deployed (BROKEN) | Removes elements, breaks other reports |
| v4 | `Hybrid_v4_Minimal.js` | Ready | Non-destructive but wrong attr declaration |
| v9 | `Hybrid_v9_AttrFix.js` | Ready | Fixed attr but doesn't toggle date filters |
| VisibilityFix_v2 | `VisibilityFix_v2.js` | Ready | Best approach, needs attr fix |
| **v10** | `Hybrid_v10_Production.js` | TO CREATE | Final merged version |

### Documentation

| File | Purpose |
|------|---------|
| `REPORT_FILTER_MAPPING.md` | Filter requirements per report |
| `UI002_PROD_INVESTIGATION.md` | PROD investigation results |
| `EMAIL_BGLOBAL_REPORT_ISSUES.md` | Client communication draft |

---

## 7. DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] Create v10 handler with merged fixes
- [ ] Test in DEV environment
- [ ] Verify all 18 reports work
- [ ] Resolve Custom business rule conflict
- [ ] Document rollback procedure

### Deployment Steps
1. [ ] Backup current PROD `UsrPage_ebkv9e8` schema
2. [ ] Deploy v10 handler to BGApp_eykaguu package
3. [ ] Compile package
4. [ ] Clear browser cache
5. [ ] Test Commission report (filters should appear)
6. [ ] Test Looker Studio report (should open in new tab)
7. [ ] Test Excel report (should download)

### Post-Deployment Verification
- [ ] Commission: Year-Month and Sales Group appear
- [ ] Non-Commission: Date filters and Status appear
- [ ] No report selected: Only Report dropdown visible
- [ ] All downloads work
- [ ] All Looker reports open in new tab

---

## 8. CLIENT FEEDBACK TO ADDRESS

From documentation review:
1. **Commission reports missing data** - QB payment backlog (deferred)
2. **Reports page doesn't load correctly** - Visibility issue (this fix)
3. **Looker Studio access issues** - Google permissions + CSP (Task #5)
4. **Excel template errors** - IntExcelReport configuration (verified working)

---

*Catalog created: 2026-01-22*
*Last updated: 2026-01-22*
