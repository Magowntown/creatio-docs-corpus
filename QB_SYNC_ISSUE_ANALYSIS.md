# QuickBooks Sync Issue Analysis

**Date:** January 19, 2026
**Status:** ROOT CAUSE CONFIRMED ✅ (REVISED)

## Executive Summary

Orders imported from **Brandwise** are **NOT syncing to QuickBooks** because they are created with **`BGHasQuickBooksLog = false`**, which the QB sync process uses as a filter condition.

**CORRECTED ROOT CAUSE:**
- ❌ ProcessListeners = 0 is **NOT** the blocking factor (121 synced orders have it)
- ✅ **BGHasQuickBooksLog = false** is the actual blocking factor (0 orders with this have ever synced)

| Order Source | BGHasQuickBooksLog | QB Sync Status |
|--------------|-------------------|----------------|
| **Manual orders** | `true` | ✅ Syncing correctly |
| **WooCommerce imports** | `true` | ✅ Syncing correctly |
| **Brandwise imports** | `false` | ❌ NOT syncing |

---

## Root Cause

### PRIMARY ISSUE: BGHasQuickBooksLog = false on Brandwise Imports

**Evidence (January 2026):**

| Metric | Value |
|--------|-------|
| Orders with HasLog=false + Synced | **0** (never!) |
| Orders with HasLog=true + Synced | **16,777** |
| Orders with HasLog=false + NOT Synced | **624** |
| Orders with HasLog=true + NOT Synced | **258** |

**Brandwise Orders (January 2026):**
- Total: 194 orders
- Synced to QB: 47 (all have `BGHasQuickBooksLog = true`)
- NOT synced to QB: 147 (all have `BGHasQuickBooksLog = false`)

**WooCommerce Orders (January 2026):**
- Total: 88 orders
- `BGHasQuickBooksLog = true`: 88/88 (100%)
- Synced to QB: 72/88 (82%)

### Field Correlation

| Field | Synced Orders (PL=0) | Unsynced Orders (PL=0) |
|-------|---------------------|------------------------|
| **BGHasQuickBooksLog** | `true` (100%) | `false` (55%) / `true` (45%) |
| **BGHasInvoice** | `true` (100%) | `false` (55%) / `true` (45%) |
| **ProcessListeners** | 0 | 0 |

The `BGHasQuickBooksLog` and `BGHasInvoice` fields appear to be set together by a business process.

### Previous Theory (INCORRECT)

The earlier analysis suggested `ProcessListeners = 0` was the root cause. **This was wrong:**
- 121 orders with `ProcessListeners = 0` ARE successfully synced to QuickBooks
- The `QuickBooks Customer Order Changed Log` process is triggered by a parent process, not by the ProcessListeners value

---

## Timeline Analysis

| Date | Event |
|------|-------|
| **2025-12-04** | First Brandwise order with `BGHasQuickBooksLog=false` (ORD-14951) |
| **2026-01-05** | First January unsynced Brandwise orders (ORD-15625, ORD-15626) |
| **2026-01-16** | Batch of Brandwise orders manually fixed and synced (47 orders) |
| **2026-01-17+** | New Brandwise orders continue with `HasLog=false` → NOT syncing |

**Pattern:** The 47 Brandwise orders that synced on January 16 were all modified after creation (different `CreatedOn` vs `ModifiedOn` timestamps), suggesting a manual batch fix was applied.

---

## Impact

### January 2026 (Since Jan 5)
- **Brandwise orders NOT synced:** 147 orders
- **WooCommerce orders NOT synced:** 16 orders (different issue - likely status-related)
- **Total revenue NOT in QuickBooks:** Unknown (orders exist but no QB invoices)

### Commission Data Impact
- No positive commission records since December 10, 2025
- December/January commission reports show empty or refunds-only

---

## Remediation Options

### Option 1: Batch Fix for Existing Orders (IMMEDIATE - VERIFIED SAFE)

**Step 1: Update existing orders to enable sync**
```sql
-- VERIFIED SAFE: Update BGHasQuickBooksLog and BGHasInvoice
UPDATE "Order"
SET "BGHasQuickBooksLog" = true,
    "BGHasInvoice" = true
WHERE "BGHasQuickBooksLog" = false
  AND "CreatedOn" >= '2026-01-01'
  AND "BGQuickBooksId" IS NULL
  AND "StatusId" != '2b9201fc-3891-4ba3-abde-1bb9ce195ecc'  -- Exclude Canceled
;
```

**Verification Count:**
```sql
-- Check how many orders will be affected:
SELECT COUNT(*)
FROM "Order"
WHERE "BGHasQuickBooksLog" = false
  AND "CreatedOn" >= '2026-01-01'
  AND "BGQuickBooksId" IS NULL
  AND "StatusId" != '2b9201fc-3891-4ba3-abde-1bb9ce195ecc';
```

**Step 2: Trigger QB sync**
After updating the flags, you may need to:
- Run the `BGBPRunQBCustomerOrderIntegration` business process manually, OR
- Update `ModifiedOn` to trigger any listening processes:

```sql
UPDATE "Order"
SET "ModifiedOn" = NOW()
WHERE "BGHasQuickBooksLog" = true
  AND "CreatedOn" >= '2026-01-01'
  AND "BGQuickBooksId" IS NULL
  AND "StatusId" != '2b9201fc-3891-4ba3-abde-1bb9ce195ecc';
```

---

### Option 2: Fix Brandwise Import Process (LONG-TERM - RECOMMENDED)

The Brandwise integration code needs to set these fields correctly when creating orders.

**In C# integration code, add:**
```csharp
entity.SetColumnValue("BGHasQuickBooksLog", true);
entity.SetColumnValue("BGHasInvoice", true);
```

**Package to modify:** `PampaBayBrandwise` or relevant Brandwise integration package

---

### Option 3: Scheduled Job (PROACTIVE)

Create a scheduled business process that:
1. Queries for orders where `BGHasQuickBooksLog = false` AND `BGQuickBooksId IS NULL`
2. Updates both `BGHasQuickBooksLog = true` and `BGHasInvoice = true`
3. Triggers the QB sync for those orders

This catches any orders that slip through with incorrect flags.

---

## Safety Verification Results

### No Duplicate Sync Risk
- No orders found with `BGQuickBooksExportCount > 1`
- `BGQuickBooksId` acts as a sync guard (already-synced orders won't re-sync)

### Status Filtering
- 67 unsynced orders are "Canceled" status
- Recommend excluding: `StatusId != '2b9201fc-3891-4ba3-abde-1bb9ce195ecc'`

### ProcessListeners is Safe to Ignore
- ProcessListeners values of -2, 0, and 2 all appear in synced orders
- Changing ProcessListeners is NOT necessary for the fix

---

## Verification Queries

### Check Unsynced Orders Count
```
Order where CreatedOn >= 2026-01-01 AND BGQuickBooksId IS NULL AND BGHasQuickBooksLog = false
```

### Verify After Fix
```
Order where BGQuickBooksId IS NOT NULL AND CreatedOn >= 2026-01-19
```

### Check BGHasQuickBooksLog Distribution
```
Order grouped by BGHasQuickBooksLog where CreatedOn >= 2026-01-01
```

---

## Related Issues

### FLT-004: BGYearMonthId Not Populated
- Separate issue affecting Year-Month filtering in reports
- Fixed via service code update (date-based filtering)

### DATA-002: December 2025 Invoices Not Paid
- December invoices exist in QB but aren't marked as paid
- This is a QB-side accounting workflow issue, not a sync issue

### ProcessListeners Theory (DEPRECATED)
- Earlier analysis suggested `ProcessListeners = 0` blocked sync
- **DISPROVED:** 121 synced orders have `ProcessListeners = 0`
- Focus on `BGHasQuickBooksLog` instead

---

## Files for Reference

- Investigation scripts: `/tmp/investigate_*.py`, `/tmp/check_*.py`, `/tmp/verify_*.py`
- This analysis: `/home/magown/creatio-report-fix/QB_SYNC_ISSUE_ANALYSIS.md`
