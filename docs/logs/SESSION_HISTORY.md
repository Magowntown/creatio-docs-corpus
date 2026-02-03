# Session History

> **Archived:** 2026-01-23 | Session logs moved from CLAUDE.md to reduce file size

---

## Session Log: 2026-01-23 (UI-002 Filter Visibility)

### UI-002: Non-Commission Reports Showing Wrong Filters (PROD)

**Discovered:** 2026-01-22 | **Resolved:** 2026-01-23
**Status:** ✅ **RESOLVED** - v18 handler with attribute binding deployed

**Problem Evolution:**
1. **2026-01-22:** Reports page showed `TypeError: Cannot read properties of undefined (reading 'getSchema')` - attribute binding in wrong schema
2. **2026-01-23:** After restoring parent schema, needed dynamic filter visibility based on report type

**Final Solution:** v18 Handler with Attribute Binding
- **File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v18_AttrBinding.js`
- **Schema UID:** `561d9dd4-8bf2-4f63-a781-54ac48a74972` (BGApp_eykaguu package)

**Key Technical Pattern:**
```javascript
// 1. Define attributes in viewModelConfigDiff
"UsrShowCommissionFilters": { "value": false },
"UsrShowDateStatusFilters": { "value": false }

// 2. Merge visibility binding onto parent elements
{
    "operation": "merge",
    "name": "GridContainer_xdy25v1",
    "values": { "visible": "$UsrShowDateStatusFilters" }
}

// 3. Toggle via handler
request.$context.UsrShowDateStatusFilters = true;
```

**Key Learnings:**
1. Freedom UI `visible: false` = element NOT rendered to DOM
2. Attribute binding is the correct pattern for dynamic visibility
3. Cross-schema binding works if attribute defined in merged viewModelConfigDiff
4. DOM manipulation fails when targeting elements hidden by schema

**See:** `docs/HANDLER_VERSION_HISTORY.md` for complete version details

---

## Session Log: 2026-01-21 (PROD → DEV Sync & IW_Commission Fix)

### DEV-001: PROD → DEV Sync Progress

| Step | Status | Notes |
|------|--------|-------|
| Compare backend service | ✅ | Identical - no changes needed |
| Compare frontend handler | ✅ | PROD was newer |
| Deploy PROD handler to IWQBIntegration (DEV) | ✅ | Hybrid handler deployed |
| Fix BGApp_eykaguu conflict | ✅ | Made minimal (empty schema) |
| Verify SQL views | ✅ | Both views exist |
| Fix IntExcelReport - IW_Commission link | ✅ | Linked to IWCommissionReportDataView |
| Test Commission report | ✅ | Working |
| Test IW_Commission report | ⏳ | Excel column alignment issue |

### IW-001: IW_Commission Excel Template Issues

**Problem:** Report generates but Excel has issues:
1. Columns misaligned (duplicate columns, missing Sales Rep/Group/Account)
2. Commission Rate showing as dates ("1/12/1900" instead of "12%")

**Fixes Applied:**
1. ESQ updated - Mapped to correct view columns
2. View recreated - Fixed IWIsNote boolean issue

**Pending:** ESQ column order must match Excel template header order.

### QB Error Log Cleanup

Cleaned up 645 empty connection timeout entries from `BGQuickBooksIntegrationLogDetail`.
Remaining 202 errors: 197 timeouts, 5 closed period, 1 missing Discount account, 1 RefNumber too long.

---

## Session Log: 2026-01-20 (QB Sync Infrastructure Investigation)

### SYNC-004: QB Web Connector Offline

**Problem:** QB Web Connector at `96.56.203.106:8080` is not responding.
**Impact:** 157+ January 2026 orders cannot sync to QuickBooks.

### SYNC-005: False "Processed" Orders (Historical Bug)

637 orders marked "Processed" with no QB ID (Aug 2023 → Jan 2026).
Root cause: Bug in `BGQuickBooksLogDetail.ProcessCustomerOrders()`.

### Data Pipeline Analysis

Patricia Goncalves Example: 1,250 commission earners → ~400 synced → **27 paid** (2.2%)
97.8% of commission missing because invoices not marked paid in QB.

### Actions Taken

| Action | Result |
|--------|--------|
| Fixed BGHasQuickBooksLog | 626 orders |
| Fixed ProcessListeners | 626 orders |
| Created log entries | 658 orders |
| Ran QB sync | 336 orders synced |

### BGlobal Email Response

Uriel Nusenbaum: BGlobal owns Looker dashboards, will share if we provide user emails.
Says migration was working - e6Solutions responsible for issues.

---

## Session Log: 2026-01-20 (Package Removal & Looker Studio)

### CSP-001: Looker Studio Blocked by Content Security Policy

Freedom UI (Creatio 8) has stricter CSP than Classic UI (v7).
Resolution Required: BGlobal needs to whitelist `lookerstudio.google.com` in Creatio CSP settings.

### LOOKER-001: Looker Studio Google Permissions Issue

URLs in `UsrReportesPampa.UsrURL` are embed-format (designed for authenticated iframe context).
Resolution Required: BGlobal needs to share dashboards with user Google accounts.

### HANDLER-001: Hybrid Handler Deployed

**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js`

Logic:
- Has UsrURL (Looker) → window.open(URL) in new tab
- No UsrURL → UsrExcelReportService for Excel download

### DATA-002 Resolution

After running "Get QuickBooks Commissions" and "QB Customer Integration":
- Jan 2026: 294 records, $168,588.02
- Dec 2025: 106 records, $34,353.57
- Feb 2026: 26 records, $24,462.50

---

## Session Log: 2026-01-19

### UI-001: DEV Reports Page Infinite Loading (FIXED)

Root Cause: `UsrPage_ebkv9e8_Updated.js` used `sdk` objects not available in Freedom UI.
Fix: Deployed `UsrPage_ebkv9e8_Hybrid.js` - minimal handler with only report generation.

### SYNC-003: QB Customer Order Integration 20K Limit

81,803 records in `BGQuickBooksIntegrationLogDetail`, ~56,000+ pending (69%).
Solution: Batch processing using "Re-Process" status rotation.

### EARNERS-001: Brandwise Commission Earners Fix

Created 253 `BGCommissionEarner` records via OData API.
Fixed commission rates using `Employee.BGDefaultCommission`.
Report improvements: Dec 2025 +296%, Jan 2026 +1414%.

### DL-004: Commission Download 404 Fix

Library fallback doesn't store bytes in SessionData.
Fix: Added routing in Generate method + redirect logic in GetReport.

---

## Session Log: 2026-01-16

SYNC-002 reported: QB sync issue blamed on `UsrPage_ebkv9e8` Form page.
Later debunked (2026-01-19): Client-side handlers don't affect server-side QB sync.

---

## Session Log: 2026-01-15

### Key Findings

1. Complete data flow traced: Creatio Orders → QB Invoices → QB Payments → Commission Data
2. December 2025 orders exist in Creatio with BGQuickBooksId
3. Invoices NOT marked as paid in QB → No ReceivePayment records
4. Commission sync working correctly - nothing to sync

**Root Cause:** Dec 2025 invoices exist in QB but awaiting payment processing.
**Action Required:** QB accounting team must process payments against Dec invoices.

### Technical Discovery

`BGQuickBooksService.cs`:
- `GetQuickBooksReceivedPayments()` queries payment receipts, NOT invoices
- Commission sync pulls PAYMENTS, not INVOICES
