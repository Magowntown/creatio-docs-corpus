# UI-002 Deployment Checklist

**Issue:** Non-Commission reports showing wrong filters in PROD
**Fix:** Deploy v10 Production handler (merged from v4+v9+VisibilityFix)
**Date:** 2026-01-22 (Updated)

---

## Pre-Deployment Summary

### Problem
- **Symptom:** ALL filters showing simultaneously - no conditional visibility working
- **Evidence:** Warning + Year-Month + Sales Group visible BEFORE selecting any report
- **Root Cause #1:** Attribute declared as `{ "value": false }` instead of `{}` - prevents reactive binding
- **Root Cause #2:** Two business rules with same name in different packages (Custom + BGApp_eykaguu)
- **Root Cause #3:** No init handler to set default visibility state

### Solution
- **v10 Production handler:** Merges best elements from v4 Minimal, v9 AttrFix, VisibilityFix_v2
- **Key fixes:**
  - Empty `{}` attribute declaration for reactive binding
  - Init handler sets defaults: `UsrShowCommissionFilters=false`, `UsrShowDateFilters=true`
  - Toggles BOTH Commission filters AND date filters based on selection
  - Non-destructive (no remove operations)

---

## Pre-Deployment: Resolve Business Rule Conflict

### Step 0: Check/Delete Custom Business Rule

**Two business rules exist with same name:**
| Package | Modified | Action |
|---------|----------|--------|
| Custom | 1/20/2026 | **DELETE** |
| BGApp_eykaguu | 7/14/2025 | Keep |

**Steps:**
1. PROD → Configuration → Packages → Custom
2. Find `BGUsrPage_ebkv9e8BusinessRule`
3. Open and review (check for visibility rules that might conflict)
4. **Delete** the Custom version
5. Compile Custom package

**Why:** Custom package rules can override handler logic. The newer Custom rule may be setting visibility incorrectly.

---

## Deployment Steps

### Step 1: Open PROD Client Unit Schema Designer

**URL:**
```
https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
```

**Alternative path:**
1. Login to PROD: https://pampabay.creatio.com
2. Open Configuration (gear icon)
3. Search for "UsrPage_ebkv9e8"
4. Find the one in **BGApp_eykaguu** package (UID: 561d9dd4-8bf2-4f63-a781-54ac48a74972)
5. Click to open schema designer

---

### Step 2: Backup Current Code (Optional but Recommended)

1. Select all code in the schema designer
2. Copy to clipboard
3. Save to: `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2_BACKUP.js`

---

### Step 3: Replace with v10 Production Handler

1. Select all code in the schema designer
2. Paste contents of: `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v10_Production.js`

**File location:** `/home/magown/creatio-report-fix/client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v10_Production.js`

---

### Step 4: Save and Publish

1. Click **Save** button
2. Wait for save confirmation
3. Click **Publish** button (if available)
4. Wait for compilation to complete

---

### Step 5: Clear Browser Cache

**Important:** Creatio caches client schemas aggressively.

1. Press `Ctrl+Shift+R` (hard refresh)
2. Or: Open DevTools → Network tab → Check "Disable cache" → Refresh

---

### Step 6: Test All Report Types

#### Test A: Non-Commission Report (Sales By Line)

1. Navigate to Reports page
2. Select "Sales By Line" from dropdown
3. **Expected:**
   - ✅ Status filter VISIBLE
   - ✅ Date filters VISIBLE
   - ✅ Year-Month filter HIDDEN
   - ✅ Sales Group filter HIDDEN
4. Click Generate Report
5. **Expected:** Report opens in new tab (Looker Studio)

#### Test B: Commission Report

1. Select "Commission" from dropdown
2. **Expected:**
   - ✅ Year-Month filter VISIBLE
   - ✅ Sales Group filter VISIBLE
   - ✅ Red warning label VISIBLE
3. Select a Year-Month and Sales Group
4. Click Generate Report
5. **Expected:** Excel downloads successfully

#### Test C: IW_Commission Report

1. Select "IW_Commission" from dropdown
2. **Expected:**
   - ✅ Year-Month filter VISIBLE
   - ✅ Sales Group filter VISIBLE
3. Click Generate Report
4. **Expected:** Excel downloads successfully

---

## Rollback Procedure

If issues occur after deployment:

### Quick Rollback

1. Open PROD Client Unit Schema Designer (same URL as Step 1)
2. Replace code with backup: `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2_BACKUP.js`
3. Save and publish
4. Hard refresh browser

---

## Technical Details

### Key Differences: v2 (Broken) vs v4 (Fix)

| Aspect | v2 (Broken) | v4 (Fix) |
|--------|-------------|----------|
| Status filter | `remove` operation | Unchanged (inherits from parent) |
| Date filters | `visible: false` | Unchanged (inherits from parent) |
| Commission filters | Always visible | Conditional via `$UsrShowCommissionFilters` |
| Report selector | Uses original | Uses original |

### viewConfigDiff Operations in v4

| Operation | Target | Purpose |
|-----------|--------|---------|
| `merge` | GridContainer_fh039aq | Hide iframe (CSP blocks it) |
| `merge` | Button_vae0g6x | Wire to report handler |
| `insert` | BGCommissionWarning | Add warning label (conditional) |
| `insert` | GridContainer_CommissionFilters | Add filter container (conditional) |
| `insert` | BGYearMonth | Add Year-Month filter |
| `insert` | BGSalesGroup | Add Sales Group filter |

### Handler Logic

```javascript
// Detects Commission reports by name
const isCommissionReport = reportName.includes("commission");

// Only toggles Commission filter visibility
request.$context.UsrShowCommissionFilters = isCommissionReport;
```

---

## Sign-Off

| Step | Status | Verified By | Date |
|------|--------|-------------|------|
| Code deployed | ☐ | | |
| Browser cache cleared | ☐ | | |
| Sales By Line tested | ☐ | | |
| Commission tested | ☐ | | |
| IW_Commission tested | ☐ | | |
| User acceptance | ☐ | | |

---

## Files Reference

| File | Purpose |
|------|---------|
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v10_Production.js` | **Deploy this** |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | Current PROD (broken) |
| `client-module/BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js` | Parent schema (if restore needed) |
| `docs/REPORT_FILTER_MAPPING.md` | Filter requirements for all 18 reports |
| `docs/UI002_FIX_CATALOG.md` | Full technical catalog |

---

## CSP Configuration (Optional - for iframe embedding)

If you want Looker Studio dashboards to work in iframes instead of new tabs:

1. System Designer → Security → Content Security Policy
2. Enable "Log violations" mode first
3. Trusted sources → Add: `https://lookerstudio.google.com`
4. Associate with directives: `child-src`, `frame-ancestors`
5. Test iframe embedding
6. Enable "Block" mode if working

**Note:** Requires Creatio 8.1.2+ and admin access.

---

*Created: 2026-01-22*
*Updated: 2026-01-22 - v10 handler (merged v4+v9+VisibilityFix)*
