# UI-002 Deployment Checklist

**Issue:** Non-Commission reports showing wrong filters in PROD
**Fix:** Deploy v4 Minimal handler
**Date:** 2026-01-22

---

## Pre-Deployment Summary

### Problem
- **Symptom:** "Sales By Line" and other non-Commission reports show Year-Month and Sales Group filters (should be hidden)
- **Missing:** Status filter, Expand All button, date filters
- **Root Cause:** v2 handler uses `operation: "remove"` which permanently destroys UI elements

### Solution
- **v4 Minimal handler:** Non-destructive approach
- **Design principle:** Only ADD Commission filters conditionally, never remove existing elements
- **Verification:** Triple-checked through code analysis, package review, and Creatio docs

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

### Step 3: Replace with v4 Minimal Handler

1. Select all code in the schema designer
2. Paste contents of: `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v4_Minimal.js`

**File location:** `/home/magown/creatio-report-fix/client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v4_Minimal.js`

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
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v4_Minimal.js` | **Deploy this** |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | Current PROD (broken) |
| `docs/REPORT_FILTER_MAPPING.md` | Filter requirements for all 18 reports |

---

*Created: 2026-01-22*
